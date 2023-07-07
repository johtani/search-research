import logging
import pathlib

import pandas as pd

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def main():
    LOGGER.info("Starting to create JSONL file from esci-data products...")
    esci_path = pathlib.Path("./esci-data/shopping_queries_dataset")
    LOGGER.info(" Reading parquet file...")
    df_products = pd.read_parquet(esci_path.joinpath("shopping_queries_dataset_products.parquet"))

    LOGGER.info(" Making output path...")
    output_path = pathlib.Path("./esci-raw-jsonl/products")
    output_path.mkdir(exist_ok=True, parents=True)

    LOGGER.info(" Extracting products data that product_locale is 'jp'...")
    df_products[df_products["product_locale"] == "jp"].to_json(
        output_path.joinpath("esci-data-products-jp.json"), orient="records", lines=True
    )
    LOGGER.info(" Extracting products data that product_locale is 'us'...")
    df_products[df_products["product_locale"] == "us"].to_json(
        output_path.joinpath("esci-data-products-us.json"), orient="records", lines=True
    )
    LOGGER.info(" Extracting products data that product_locale is 'es'...")
    df_products[df_products["product_locale"] == "es"].to_json(
        output_path.joinpath("esci-data-products-es.json"), orient="records", lines=True
    )
    LOGGER.info("Finish extract-products")


if __name__ == "__main__":
    main()
