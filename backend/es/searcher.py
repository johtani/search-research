from typing import Any, TypedDict

from elasticsearch import Elasticsearch

from backend.es.config import Config


class EsReqeust(TypedDict):
    query: Any
    aggs: Any
    from_: int
    size: int
    sort: Any


class EsSearchRepository:
    config: Config
    esclient: Elasticsearch

    def __init__(self, config: Config) -> None:
        self.config = config
        self.esclient = Elasticsearch(config.url)

    def search(self, request):
        res = self.esclient.search(index=self.config.index)
        return res.body

    def autocomplete(self, request):
        return None
