from backend.models import Product, EsProduct
from backend.processor import Processor
class SetIdProcessor(Processor):
    """
    _idを設定するドキュメントプロセッサー
    """
    def apply(self, doc: Product) -> Product:
        return EsProduct(doc | {"_id": doc["product_id"]})

