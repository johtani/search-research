import dataclasses
from dataclasses import field
from typing import Any, List

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


class EsSearchRepository:
    config: Config
    esclient: Elasticsearch

    def __init__(self, config: Config) -> None:
        self.config = config
        self.esclient = Elasticsearch(config.url)

    def search(self, request: EsReqeust):
        res = self.esclient.search(
            index=self.config.index,
            query=request.query,
            aggs=request.aggs,
            from_=request.from_,
            size=request.size,
            highlight=request.highlight,
            source=dataclasses.asdict(request.source),
        )
        return res.body

    def autocomplete(self, request):
        return None
