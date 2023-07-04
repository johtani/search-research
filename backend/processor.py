import logging
from backend.models import Product
from typing import List
from abc import ABC, abstractmethod

class Processor(ABC):
    @abstractmethod
    def apply(self, doc: Product) -> Product:
        pass

class PipelineManager:

    processors: List[Processor]
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def __init__(self, processors: List[Processor]):
        self.processors = processors

    def apply_pipelines(self, doc: Product) -> Product:
        for processor in self.processors:
            doc = processor.apply(doc)
        return doc