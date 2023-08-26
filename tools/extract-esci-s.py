import json
import logging
import os
import pathlib
import subprocess
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Dict, List

import tqdm

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# for sample.json
# INPUT_DIR = "./esci-s/"
# METADATA_FILENAME = "sample.json"
# for full json
INPUT_DIR = "./esci-s-full/"
METADATA_FILENAME = "esci.json"


class OutputManager:
    output_dir: Path = pathlib.Path("./esci-jsonl/raw-esci-s")
    review_fp: Dict[str, TextIOWrapper] = {}
    metadata_fp: Dict[str, TextIOWrapper] = {}

    def __init__(self):
        LOGGER.info(" Making output path...")
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def output_metadata(self, metadata: Dict[str, Any]):
        locale: str = metadata["locale"]
        reviews: List[Dict[str, Any]] = metadata.pop("reviews", [])
        self._output_metadata_without_reviews(metadata=metadata, locale=locale)
        self._output_reviews(asin=metadata["asin"], reviews=reviews, locale=locale)

    def _create_metadata_fp(self, locale: str):
        file = self.output_dir.joinpath(f"esci-s-metadata-{locale}.json")
        fp = open(file, "w")
        self.metadata_fp[locale] = fp
        return fp

    def _create_review_fp(self, locale: str):
        file = self.output_dir.joinpath(f"esci-s-reviews-{locale}.json")
        fp = open(file, "w")
        self.review_fp[locale] = fp
        return fp

    def _output_metadata_without_reviews(self, metadata: Dict[str, Any], locale: str):
        fp = self.metadata_fp.get(locale, None)
        if fp is None:
            fp = self._create_metadata_fp(locale)
        json.dump(metadata, fp=fp, sort_keys=True)
        fp.write("\n")

    def _output_reviews(self, asin: str, reviews: List[Dict[str, Any]], locale: str):
        fp = self.review_fp.get(locale, None)
        if fp is None:
            fp = self._create_review_fp(locale)
        json.dump({"asin": asin, "reviews": reviews}, fp=fp)
        fp.write("\n")

    def fp_closes(self):
        for fp in self.metadata_fp.values():
            fp.close()
        for fp in self.review_fp.values():
            fp.close()


def main():
    LOGGER.info("Starting to create JSONL file from esci-s products...")
    esci_path = pathlib.Path(INPUT_DIR)
    output_mgr = OutputManager()
    LOGGER.info(" Reading json file and extracting esci-s...")
    progress = tqdm.tqdm(unit="docs")
    # 1行ずつ読み込み
    with open(esci_path.joinpath(METADATA_FILENAME), "r") as f:
        for line in f:
            metadata = json.loads(line)
            output_mgr.output_metadata(metadata)
            progress.update()
    output_mgr.fp_closes()
    # 最後にファイルをソート？
    for file in output_mgr.output_dir.glob("*.json"):
        file_path = str(file.resolve())
        subprocess.run(["sort", "-o", file_path.replace(".json", "_sorted.json"), file_path])
        os.remove(file_path)

    LOGGER.info("Finish extract-esci-s")


if __name__ == "__main__":
    main()
