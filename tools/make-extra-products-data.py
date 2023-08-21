import argparse
import json
import logging
import pathlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import tqdm

from backend.models import Product
from backend.pipelines import JaClipEncodeProcessor, Pipeline, PipelineManager

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# TODO
INPUT_FILE = pathlib.Path("./esci-jsonl/raw-products/esci-data-products-jp.json")
BASE_OUTPUT_DIR = pathlib.Path("./esci-jsonl/")
pipeline_mgr = PipelineManager(
    registory={"ja_clip": Pipeline(processors=[JaClipEncodeProcessor("products_dense_vector")])}
)


@dataclass
class Args:
    pipeline: str


def parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Make extra data from products as JSONL")
    parser.add_argument("pipeline", type=str, choices=pipeline_mgr.pipeline_names(), help="Pipeline type")
    return Args(**vars(parser.parse_args()))


def to_extra_dict(target: Dict[str, Any]) -> Dict[str, Any]:
    # Index from dataframe...
    target.pop("Index", None)
    for key in Product.__annotations__.keys():
        # Need key
        if key != "product_id":
            target.pop(key, None)
    return target


def making_extra_data(pipeline: Pipeline, output_dir: Path):
    LOGGER.info("Start making extra data...")
    df_data_jsonl = pd.read_json(INPUT_FILE, orient="records", lines=True)
    progress = tqdm.tqdm(unit="docs", total=len(df_data_jsonl))
    output_data_file = output_dir.joinpath("data.json")
    with open(output_data_file, "a") as f:
        for row in df_data_jsonl.itertuples():
            product = row._asdict()
            doc = pipeline.apply_pipelines(product)
            json.dump(to_extra_dict(doc), f)
            f.write("\n")
            progress.update()


def making_metadata(pipeline: Pipeline, output_dir: Path):
    LOGGER.info("Making _metadata.json file...")
    output_meta_file = output_dir.joinpath("_metadata.json")
    with open(output_meta_file, "w") as f:
        json.dump(pipeline.metadatas_asdict(), f)


def main():
    args: Args = parse_args()
    pipeline = pipeline_mgr.get_pipeline(args.pipeline)
    LOGGER.info(f"{args.pipeline=}")
    output_dir = BASE_OUTPUT_DIR.joinpath(args.pipeline)
    # if output_dir exists, print error and finish
    if output_dir.exists():
        LOGGER.error(f"Already exists {args.pipeline} directory. Please remove it before run this batch.")
        quit()
    output_dir.mkdir()
    making_extra_data(pipeline, output_dir)
    making_metadata(pipeline, output_dir)
    LOGGER.info("Finish making extra products data!")


if __name__ == "__main__":
    main()
