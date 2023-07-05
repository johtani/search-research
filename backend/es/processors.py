from typing import Any, Mapping

from backend.processor import Processor


class SetIdProcessor(Processor):
    """
    _idを設定するドキュメントプロセッサー
    """

    def apply(self, doc: Mapping[str, Any]) -> Mapping[str, Any]:
        tmp: Mapping[str, Any] = doc | {"_id": doc["product_id"]}
        return tmp
