import dataclasses
import json
from dataclasses import field
from typing import Any, Dict, List, Optional, TypedDict, Union

from elasticsearch import Elasticsearch

from backend.es.config import Config


@dataclasses.dataclass
class EsRequestSource:
    includes: List[str] = field(default_factory=list)


@dataclasses.dataclass
class EsReqeust:
    query: Any | None = None
    aggs: Any | None = None
    from_: int = 0
    size: int = 20
    sort: Any | None = None
    highlight: Any | None = None
    source: EsRequestSource = field(default_factory=EsRequestSource)


class HitItem(TypedDict, total=False):
    _index: str
    _id: str
    _score: float
    _source: Dict[str, Any]
    _ignored: Optional[List[str]]
    highlight: Dict[str, List[str]]


class HitsData(TypedDict):
    total: int | Dict[str, Union[int, str]]
    max_score: float
    hits: List[HitItem]


class AggregationsData(TypedDict):
    facet_bucket_all: Dict[str, Any]


class EsResponse(TypedDict):
    timed_out: bool
    took: int
    hits: HitsData
    aggregations: Optional[AggregationsData]


class EsSearchRepository:
    config: Config
    esclient: Elasticsearch

    def __init__(self, config: Config) -> None:
        self.config = config
        self.esclient = Elasticsearch(config.url)

    def search(self, request: EsReqeust) -> EsResponse:
        res = self.esclient.search(
            index=self.config.index,
            query=request.query,
            aggs=request.aggs,
            from_=request.from_,
            size=request.size,
            highlight=request.highlight,
            source=dataclasses.asdict(request.source),
        )
        es_res: EsResponse = json.loads(res.body)
        return es_res

    def autocomplete(self, request):
        return None
