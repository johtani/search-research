import argparse
import logging
import pathlib
from dataclasses import dataclass

import pandas as pd
import tqdm
from pandas import DataFrame

import backend.es.config
from backend.es.indexer import EsIndexRepository
from backend.es.processors import SetIdProcessor
from backend.indexer import Indexer
from backend.pipelines import Pipeline, PipelineManager
from backend.processor import MergeESCISMetadataProcessor, MergeProcessor

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# JSONL形式のデータファイル
FILE = pathlib.Path("./esci-jsonl/raw-products/esci-data-products-jp.json")
BULK_SIZE = 500
pipeline_mgr = PipelineManager(
    # TODO define 'ja_clip' somewhere for standardization
    registory={
        "ja_clip": Pipeline(
            processors=[
                SetIdProcessor(),
                MergeESCISMetadataProcessor(target_fields=["image", "type"]),
                MergeProcessor("ja_clip"),
            ]
        ),
        "raw": Pipeline(processors=[SetIdProcessor(), MergeESCISMetadataProcessor(target_fields=["image", "type"])]),
    }
)


@dataclass
class Args:
    search_engine: str
    pipeline: str
    delete_if_exists: bool = False


def parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Bulk loader for search engine")
    parser.add_argument("search_engine", type=str, choices=["elasticsearch", "es"], help="search engine type")
    parser.add_argument("pipeline", type=str, choices=pipeline_mgr.pipeline_names(), help="Pipeline type")
    parser.add_argument(
        "-d",
        "--delete_if_exists",
        default=False,
        action="store_true",
        help="If true, delete the index before indexing if the index exists.",
    )

    return Args(**vars(parser.parse_args()))


def generate_bulk_actions(df: DataFrame, pipeline: Pipeline):
    for row in df.itertuples():
        product = row._asdict()
        doc = pipeline.apply_pipelines(product)
        # DataFrameにより付与されている項目を削除
        doc.pop("Index", None)
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
    pipeline = pipeline_mgr.get_pipeline(args.pipeline)
    LOGGER.info(f"{args.pipeline=}")
    LOGGER.info(f"{args.delete_if_exists=}")

    LOGGER.info("Start bulk indexing to the index...")
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
