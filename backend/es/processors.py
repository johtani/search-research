from typing import Any, Dict

from backend.processor import Metadata, Processor


class SetIdProcessor(Processor):
    """
    _idを設定するドキュメントプロセッサー
    """

    def metadata(self) -> Metadata:
        return Metadata(name=self.__class__.__name__, description="ID付与", inputs="product_id")

    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        return doc | {"_id": doc["product_id"]}
