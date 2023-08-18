from typing import List

from backend.es.processors import SetIdProcessor
from backend.pipelines import JaClipEncodeProcessor
from backend.processor import Processor


def raw_es_pipeline() -> List[Processor]:
    return [SetIdProcessor()]


def ja_clip_es_pipeline() -> List[Processor]:
    return [JaClipEncodeProcessor("products_dense_vector"), SetIdProcessor()]
