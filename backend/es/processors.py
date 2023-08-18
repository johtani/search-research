import logging
from typing import Any, Dict

import japanese_clip as ja_clip
import torch

from backend.processor import Metadata, Processor


class SetIdProcessor(Processor):
    """
    _idを設定するドキュメントプロセッサー
    """

    def metadata(self) -> Metadata:
        return Metadata(description="ID付与", inputs="product_id")

    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        return doc | {"_id": doc["product_id"]}


class JaClipEncodeProcessor(Processor):
    """
    rinna/japanese-clipを利用して、embeddingsのベクトルを生成してMappingに設定する。
    設定先は、target_fieldで指定
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    _MODEL_NAME = "rinna/japanese-clip-vit-b-16"

    def __init__(self, target_field: str):
        self.logger.info("Creating Model and Tokenizer...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.debug(f"device is {self.device}")
        self.model, preprocess = ja_clip.load(self._MODEL_NAME, device=self.device)
        self.tokenizer = ja_clip.load_tokenizer()
        self.target_field = target_field

    def metadata(self) -> Any:
        return Metadata(description=f"embeddings using {self._MODEL_NAME}", inputs="product_title")

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
