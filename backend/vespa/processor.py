from typing import Any, Dict

from backend.processor import Metadata, Processor


class ConvertVespaDocProcessor(Processor):
    """
    Vespaの形式（{id: ID, fields: PRODUCT}）に変換する
    """

    def metadata(self) -> Metadata:
        return Metadata(name=self.__class__.__name__, description="Vespa形式に変換", inputs="")

    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        doc.pop("Index", None)
        return {"id": doc["product_id"], "fields": doc}
