import dataclasses
import datetime
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
