import pathlib
import pandas as pd
import tqdm
import json

from elasticsearch import TransportError, ApiError, Elasticsearch
from elasticsearch.helpers import streaming_bulk

# JSONL形式のデータファイル
FILE = pathlib.Path("./esci-raw-jsonl/products/esci-data-products-jp.json")
# スキーマファイル
SCHEMA_FILE = pathlib.Path("./schema/es/product-raw-index-schema.json")
# 既存インデックスを削除してからデータ登録する場合はTrue
DELETE_IF_EXISTS = False
# Elasticsearchの接続文字列
ESHOST = "http://192.168.1.240:9200"
INDEX_NAME = "esci-raw-data"
BULK_SIZE = 500

def generate_bulk_actions(file: pathlib.Path):
    df_data_jsonl = pd.read_json(file, orient="records", lines=True)
    for row in df_data_jsonl.itertuples():
        doc = dataframe2dict(row)
        yield doc

# Documentへの変換処理
def dataframe2dict(row):
    return {
        "_id": row.product_id,
        "product_id": row.product_id,
        "product_locale": row.product_locale,
        "product_title": row.product_title,
        "product_description": row.product_description,
        "product_bullet_point": row.product_bullet_point,
        "product_color": row.product_color,
        "product_brand": row.product_brand
    }

def create_index(esclient: Elasticsearch) -> bool:
    error = False
    with open(SCHEMA_FILE, "r") as config_file:
        config = json.loads(config_file.read())
        try:
            is_exists = esclient.options(ignore_status=[400, 404]).indices.exists(index=INDEX_NAME)
            if DELETE_IF_EXISTS:
                if is_exists:
                    print(" Deleting existing %s" % INDEX_NAME)
                    esclient.options(ignore_status=[400, 404]).indices.delete(index=INDEX_NAME)
            if not is_exists:
                print(" Creating index %s" % INDEX_NAME)
                resp = esclient.options(
                    request_timeout=1
                ).indices.create(
                    index=INDEX_NAME,
                    mappings=config["mappings"],
                    settings=config["settings"]
                )
            else:
                print(" Already exists %s, then skip to create the index" % INDEX_NAME)

        except (ApiError, TransportError) as err:
            print(f"Error {err}")
            error = True
    return error

# Elasticsearch client生成処理
def create_esclient() -> Elasticsearch:
    esclient = Elasticsearch(ESHOST)
    return esclient

def main():
    print("Start bulk indexing to raw index...")
    esclient = create_esclient()
    create_index(esclient)

    print(" Indexing documents...")
    # TODO 総件数はデータから計算したほうがいいかも
    number_of_docs = 339059
    # プログレスバー表示用
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=esclient, index=INDEX_NAME, actions=generate_bulk_actions(FILE)
    ):
        progress.update(1)
        successes += ok

    print(" Indexed %d/%d documents" % (successes, number_of_docs))
    print("Finish bulk index")

if __name__ == '__main__':
    main()
