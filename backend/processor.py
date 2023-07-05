import logging
from abc import abstractmethod
from typing import Any, List, Mapping


class Processor:
    @abstractmethod
    def apply(self, doc: Mapping[str, Any]) -> Mapping[str, Any]:
        pass


class PipelineManager:
    processors: List[Processor]
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def __init__(self, processors: List[Processor]):
        self.processors = processors

    def apply_pipelines(self, doc: Mapping[str, Any]) -> Mapping[str, Any]:
        for processor in self.processors:
            doc = processor.apply(doc)
        return doc
