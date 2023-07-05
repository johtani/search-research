from typing import Optional, TypedDict


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
