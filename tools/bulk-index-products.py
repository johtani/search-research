import argparse
import logging
import pathlib
from dataclasses import dataclass

import pandas as pd
import tqdm
from pandas import DataFrame

import backend.es.config
from backend.es.indexer import EsIndexRepository
from backend.es.pipelines import ja_clip_es_pipeline, raw_es_pipeline
from backend.indexer import Indexer
from backend.processor import Pipeline

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# JSONL形式のデータファイル
FILE = pathlib.Path("./esci-raw-jsonl/products/esci-data-products-jp.json")
BULK_SIZE = 500


@dataclass
class Args:
    search_engine: str
    pipeline: str
    delete_if_exists: bool = False


def parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Bulk loader for search engine")
    parser.add_argument("search_engine", type=str, choices=["elasticsearch", "es"], help="search engine type")
    parser.add_argument("pipeline", type=str, choices=["raw", "with_vector_by_ja_clip"], help="Pipeline type")
    parser.add_argument(
        "-d",
        "--delete_if_exists",
        action="store_true",
        help="If true, delete the index before indexing if the index exists.",
    )

    return Args(**vars(parser.parse_args()))


def generate_bulk_actions(df: DataFrame, pipeline: Pipeline):
    for row in df.itertuples():
        product = row._asdict()
        doc = pipeline.apply_pipelines(product)
        yield doc


def main():
    args: Args = parse_args()
    if args.search_engine in ["elasticsearch", "es"]:
        LOGGER.info(f"Creating {args.search_engine} repository...")
        config = backend.es.config.load_config()
        repository = EsIndexRepository(config)
    else:
        LOGGER.error(f"Does not support {args.search_engine} yet...")
        quit()
    if args.pipeline == "raw":
        pipeline = Pipeline(raw_es_pipeline())
    elif args.pipeline == "with_vector_by_ja_clip":
        pipeline = Pipeline(ja_clip_es_pipeline())
    else:
        LOGGER.error(f"Does not support {args.pipeline} yet...")
        quit()
    LOGGER.info(f"{args.pipeline=}")
    LOGGER.info(f"{args.delete_if_exists=}")

    LOGGER.info("Start bulk indexing to raw index...")
    indexer = Indexer(repository=repository)
    error = indexer.create_index(args.delete_if_exists)

    if not error:
        LOGGER.info(" Indexing documents...")
        df_data_jsonl = pd.read_json(FILE, orient="records", lines=True)
        number_of_docs = len(df_data_jsonl)
        # プログレスバー表示用
        progress = tqdm.tqdm(unit="docs", total=number_of_docs)
        successes = indexer.bulk_index(generate_bulk_actions(df_data_jsonl, pipeline), lambda: progress.update(1))
        LOGGER.info(" Indexed %d/%d documents" % (successes, number_of_docs))

    else:
        LOGGER.info(" Error during create_index...")
    LOGGER.info("Finish bulk index")


if __name__ == "__main__":
    main()
