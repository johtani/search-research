import logging
import pathlib
from pathlib import Path

import pandas as pd
from pandas import DataFrame

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

INPUT_DIR = "./esci-data/shopping_queries_dataset"
PRODUCT_FILENAME = "shopping_queries_dataset_products.parquet"
OUTPUT_DIR = "./esci-jsonl/raw-products"


def output_filename(locale: str) -> str:
    return f"esci-data-products-{locale}.json"


def output_json(df_products: DataFrame, output_path: Path, locale: str):
    LOGGER.info(f" Extracting products data that product_locale is '{locale}'...")
    df_products[df_products["product_locale"] == locale].to_json(
        output_path.joinpath(output_filename(locale)), orient="records", lines=True
    )


def main():
    LOGGER.info("Starting to create JSONL file from esci-data products...")
    esci_path = pathlib.Path(INPUT_DIR)
    LOGGER.info(" Reading parquet file...")
    df_products = pd.read_parquet(esci_path.joinpath(PRODUCT_FILENAME))
    df_products.sort_values(by="product_id", inplace=True)

    LOGGER.info(" Making output path...")
    output_path = pathlib.Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True, parents=True)

    locales: list[str] = df_products["product_locale"].unique().tolist()
    for locale in locales:
        output_json(df_products=df_products, output_path=output_path, locale=locale)
    LOGGER.info("Finish extract-products")


if __name__ == "__main__":
    main()
