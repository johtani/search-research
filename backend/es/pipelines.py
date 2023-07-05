from typing import List

from backend.es.processors import SetIdProcessor
from backend.processor import Processor


def raw_es_pipeline() -> List[Processor]:
    return [SetIdProcessor()]
