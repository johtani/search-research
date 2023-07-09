import logging
import pathlib

import pandas as pd
import tqdm
from pandas import DataFrame

import backend.es.config
from backend.es.indexer import EsIndexRepository
from backend.es.pipelines import ja_clip_es_pipeline
from backend.indexer import Indexer
from backend.processor import PipelineManager

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# JSONL形式のデータファイル
FILE = pathlib.Path("./esci-raw-jsonl/products/esci-data-products-jp.json")
# 既存インデックスを削除してからデータ登録する場合はTrue
DELETE_IF_EXISTS = True
BULK_SIZE = 500


def generate_bulk_actions(df: DataFrame, pipeline: PipelineManager):
    for row in df.itertuples():
        product = row._asdict()
        doc = pipeline.apply_pipelines(product)
        yield doc


def main():
    LOGGER.info("Start bulk indexing to raw index...")
    config = backend.es.config.load_config()
    repository = EsIndexRepository(config)
    indexer = Indexer(repository=repository)
    error = indexer.create_index(DELETE_IF_EXISTS)
    # pipeline = PipelineManager(raw_es_pipeline())
    pipeline = PipelineManager(ja_clip_es_pipeline())

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
