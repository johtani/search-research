import dataclasses
import datetime
import json
import logging
import pathlib
from abc import abstractmethod
from typing import Any, Dict


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
