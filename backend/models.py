import dataclasses
from typing import TypedDict, Optional


class Product(TypedDict):
    """
    productのデータ
    """
    product_id: str
    product_title: str
    product_description: Optional[str]
    product_bullet_point: Optional[str]
    product_brand: Optional[str]
    product_color: Optional[str]
    product_locale: str


class EsProduct(Product):
    _id: str


def to_es_product(data: Product) -> EsProduct:
    return EsProduct(data | {"_id": data["product_id"]})
