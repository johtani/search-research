import pathlib
import pandas as pd
import tqdm

from elasticsearch import TransportError, ApiError, Elasticsearch
from elasticsearch.helpers import streaming_bulk

import backend.es.config
from backend.es.indexer import EsIndexer
from backend.models import Product, EsProduct

# JSONL形式のデータファイル
FILE = pathlib.Path("./esci-raw-jsonl/products/esci-data-products-jp.json")
# スキーマファイル
SCHEMA_FILE = pathlib.Path("./schema/es/product-raw-index-schema.json")
# 既存インデックスを削除してからデータ登録する場合はTrue
DELETE_IF_EXISTS = False
BULK_SIZE = 500

def generate_bulk_actions(file: pathlib.Path):
    df_data_jsonl = pd.read_json(file, orient="records", lines=True)
    for row in df_data_jsonl.itertuples():
        doc = backend.models.to_es_product(Product(row._asdict()))
        yield doc

def create_index(indexer: EsIndexer) -> bool:
    error = False
    try:
        is_exists = indexer.is_exist_index()
        if DELETE_IF_EXISTS:
            if is_exists:
                print(" Deleting existing %s" % indexer.config.index)
                indexer.delete_index()
            is_exists = indexer.is_exist_index()
        if not is_exists:
            print(" Creating index %s" % indexer.config.index)
            indexer.create_index()
        else:
            print(" Already exists %s, then skip to create the index" % indexer.config.index)

    except (ApiError, TransportError) as err:
        print(f"Error {err}")
        error = True
    return error


def main():
    print("Start bulk indexing to raw index...")
    config = backend.es.config.load_config()
    indexer = backend.es.indexer.EsIndexer(config)
    create_index(indexer)

    print(" Indexing documents...")
    # TODO 総件数はデータから計算したほうがいいかも
    number_of_docs = 339059
    # プログレスバー表示用
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=indexer.esclient, index=indexer.config.index, actions=generate_bulk_actions(FILE)
    ):
        progress.update(1)
        successes += ok

    print(" Indexed %d/%d documents" % (successes, number_of_docs))
    print("Finish bulk index")

if __name__ == '__main__':
    main()
