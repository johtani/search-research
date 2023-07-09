import logging
from abc import abstractmethod
from typing import Any, Dict, List


class Processor:
    @abstractmethod
    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        pass


class PipelineManager:
    processors: List[Processor]
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def __init__(self, processors: List[Processor]):
        self.processors = processors

    def apply_pipelines(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        for processor in self.processors:
            doc = processor.apply(doc)
        return doc
