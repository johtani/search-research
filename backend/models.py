from typing import Any, Dict, List, Optional, TypedDict

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


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


class BaseReqResModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class SearchQuery(BaseReqResModel):
    current: int = 1
    filters: Any = []
    results_per_page: int = 20
    search_term: str = ""
    sort_direction: str = ""
    sort_field: str = ""
    sort_list: Any = []


class ResultField(BaseReqResModel):
    snippet: Optional[Dict[str, Any]]


class SearchOptions(BaseReqResModel):
    search_fields: Dict[str, Any] = {}
    result_fields: Dict[str, ResultField | Any] = {}
    disjunctive_facets: list[str] = []
    facets: Dict[str, Any] = {}


class SearchRequest(BaseReqResModel):
    query: SearchQuery
    options: SearchOptions


class FacetData(BaseReqResModel):
    value: str
    count: int


class FacetItem(BaseReqResModel):
    data: List[FacetData]
    type: str


class HighlightData(BaseReqResModel):
    snippet: List[str]


class SourceData(BaseReqResModel):
    product_id: str
    product_title: str
    product_brand: str


class RawHitItem(BaseReqResModel):
    _index: str
    _id: str
    _score: float
    _source: SourceData
    highlight: Dict[str, HighlightData]


class ResultItem(BaseReqResModel):
    id: Dict[str, str]
    _meta: Dict[str, RawHitItem]
    product_id: Dict[str, str]
    product_title: Dict[str, str]
    product_brand: Dict[str, str]
    product_title_ja: HighlightData
    product_description_ja: HighlightData


class SearchResult(BaseReqResModel):
    result_search_term: str = ""
    total_pages: int = 0
    paging_start: int = 0
    paging_end: int = 0
    was_searched: bool = False
    total_results: int = 0
    facets: Dict[str, List[FacetItem]] = {}
    results: List[ResultItem] = []
    request_id: str | None = None
    raw_response: Any | None = None
