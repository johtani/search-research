import logging
from dataclasses import asdict
from typing import Any, Dict, List

import japanese_clip as ja_clip
import torch

from backend.processor import Metadata, Processor


class Pipeline:
    processors: List[Processor]
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def __init__(self, processors: List[Processor]):
        self.processors = processors

    def apply_pipelines(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        for processor in self.processors:
            doc = processor.apply(doc)
        return doc

    def metadatas_asdict(self) -> Dict[str, List[Dict[str, Any]]]:
        metadatas: List[Dict[str, Any]] = []
        for processor in self.processors:
            metadatas.append(asdict(processor.metadata()))
        return {"metadatas": metadatas}


class JaClipEncodeProcessor(Processor):
    """
    rinna/japanese-clipを利用して、embeddingsのベクトルを生成してMappingに設定する。
    設定先は、target_fieldで指定
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    _MODEL_NAME = "rinna/japanese-clip-vit-b-16"

    def __init__(self, target_field: str):
        self.logger.debug("Creating Model and Tokenizer...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.debug(f"device is {self.device}")
        self.model, preprocess = ja_clip.load(self._MODEL_NAME, device=self.device)
        self.tokenizer = ja_clip.load_tokenizer()
        self.target_field = target_field

    def metadata(self) -> Any:
        return Metadata(
            name=self.__class__.__name__,
            description=f"embeddings using {self._MODEL_NAME}",
            inputs="product_title",
            vector_size=512,
        )

    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """

        @param doc:
        @return:
        """
        text = doc["product_title"]
        encodings = ja_clip.tokenize(
            texts=text,
            device=self.device,
            tokenizer=self.tokenizer,
        )
        with torch.no_grad():
            embeddings = self.model.get_text_features(**encodings)[0].tolist()
        doc[self.target_field] = embeddings
        return doc


class PipelineManager:
    _registory: Dict[str, Pipeline] = {}

    def __init__(self, registory: Dict[str, Pipeline]) -> None:
        self._registory = registory

    def pipeline_names(self) -> List[str]:
        return list(self._registory.keys())

    def get_pipeline(self, name: str) -> Pipeline | None:
        return self._registory.get(name)
