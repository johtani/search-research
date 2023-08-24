from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, TypedDict, Union

from dataclasses_json import DataClassJsonMixin, config
from elasticsearch import Elasticsearch

from backend.es.config import Config


@dataclass
class EsRequestSource:
    includes: List[str] = field(default_factory=list)


@dataclass
class EsHighlight:
    fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EsRequest(DataClassJsonMixin):
    query: Any | None = None
    post_filter: Any | None = None
    aggs: Any | None = None
    from_: int = field(metadata=config(field_name="from"), default=0)
    size: int = 20
    sort: Any | None = None
    highlight: EsHighlight | None = None
    _source: EsRequestSource = field(default_factory=EsRequestSource)


class HitItem(TypedDict, total=False):
    _index: str
    _id: str
    _score: float
    _source: Dict[str, Any]
    _ignored: Optional[List[str]]
    highlight: Optional[Dict[str, List[str]]]


class HitsData(TypedDict):
    total: int | Dict[str, Union[int, str]]
    max_score: float
    hits: List[HitItem]


class EsResponse(TypedDict):
    timed_out: bool
    took: int
    _shards: Dict[str, Any]
    hits: HitsData
    aggregations: Optional[Dict[str, Dict[str, Any]]]


class EsSearchRepository:
    config: Config
    esclient: Elasticsearch

    def __init__(self, config: Config) -> None:
        self.config = config
        self.esclient = Elasticsearch(config.url)

    def search(self, request: EsRequest) -> EsResponse:
        res = self.esclient.search(
            index=self.config.index,
            query=request.query,
            aggs=request.aggs,
            from_=request.from_,
            size=request.size,
            post_filter=request.post_filter,
            highlight=None if request.highlight is None else asdict(request.highlight),
            source=asdict(request._source),
        )
        es_res: EsResponse = res.body
        return es_res

    def autocomplete(self, request):
        return None
