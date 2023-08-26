import dataclasses
import datetime
import json
import logging
import pathlib
from abc import abstractmethod
from io import TextIOWrapper
from typing import Any, Dict

import tqdm


@dataclasses.dataclass
class Metadata:
    name: str = ""
    date: str = datetime.date.today().strftime("%Y/%m/%d")
    description: str = ""
    inputs: str = ""
    vector_size: int = -1


class Processor:
    @abstractmethod
    def metadata(self) -> Metadata:
        pass

    @abstractmethod
    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        pass


class MergeProcessor(Processor):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    BASE_INPUT_DIR = pathlib.Path("./esci-jsonl/")
    target_dir: str
    skipped: bool = False
    line: str

    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self._load_data_file()

    def metadata(self) -> Metadata:
        # TODO No need metadata for MergeProcessor...
        return Metadata()

    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        product_id = doc["product_id"]
        if not self.skipped:
            self.line = self.fp.readline()
        if self.line:
            extra_data = json.loads(self.line)
            if product_id == extra_data["product_id"]:
                self.skipped = False
                for key in extra_data.keys():
                    doc[key] = extra_data[key]
            else:
                self.skipped = True
                self.logger.info(f"Difference the product_id: input[{product_id}]  read[{extra_data['product_id']}]")
        else:
            self.logger.info("The end of file...")
        return doc

    def _load_data_file(self):
        target = self.BASE_INPUT_DIR.joinpath(self.target_dir)
        if not target.exists():
            self.logger.error(f"Not exist target directory[{self.target_dir}]")
            raise IOError("Cannot read the target dir")
        data_file = target.joinpath("data.json")
        if not data_file.exists():
            self.logger.error(f"Not exist target file[{self.target_dir}/data.json]")
            raise IOError("Cannot read the target file")
        self.fp = open(data_file, "r")


class MergeESCISMetadataProcessor(Processor):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    BASE_INPUT_DIR = pathlib.Path("./esci-jsonl/raw-esci-s/")
    fps: Dict[str, TextIOWrapper] = {}
    target_fields: list[str]
    skipped: bool = False
    line: str

    def __init__(self, target_fields: list[str]) -> None:
        self.target_fields = target_fields
        self.skip_counter = tqdm.tqdm(desc="skip doc count...", unit="docs")

    def metadata(self) -> Metadata:
        # TODO No need metadata for MergeProcessor...
        return Metadata()

    def _find_target_file(self, locale: str) -> TextIOWrapper:
        fp = self.fps.get(locale, None)
        if fp is None:
            fp = open(self.BASE_INPUT_DIR.joinpath(f"esci-s-metadata-{locale}_sorted.json"), "r")
            self.fps[locale] = fp
        return fp

    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        locale = doc["product_locale"]
        fp = self._find_target_file(locale)
        if not self.skipped:
            self.line = fp.readline()
        if self.line:
            product_id = doc["product_id"]
            esci_s_metadata = json.loads(self.line)
            if product_id == esci_s_metadata["asin"]:
                self.skipped = False
                for key in self.target_fields:
                    doc[key] = esci_s_metadata.get(key, None)
            else:
                self.skipped = True
                self.logger.debug(f"Difference the product_id: input[{product_id}]  read[{esci_s_metadata['asin']}]")
                self.skip_counter.update()
        else:
            self.logger.info("The end of file...")
        return doc
