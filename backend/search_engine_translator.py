import logging
from typing import Any, Dict

from pydantic import BaseModel

from backend.es.config import Config, load_config
from backend.es.searcher import EsSearchRepository


class SearchQuery(BaseModel):
    current: int
    filters: Any
    resultsPerPage: int
    searchTerm: str
    sortDirection: str
    sortField: str
    sortList: Any


class SearchOptions(BaseModel):
    search_fields: Dict[str, Any]
    result_fields: Dict[str, Any]
    disjunctiveFacets: list[str]
    facets: Dict[str, Any]


class SearchRequest(BaseModel):
    query: SearchQuery
    options: SearchOptions


class EsTranslator:
    logger = logging.getLogger("EsTranslator")

    def __init__(self) -> None:
        self.config: Config = load_config()
        self.searcher: EsSearchRepository = EsSearchRepository(self.config)

    def translateAndSearch(self, request: SearchRequest) -> Dict[str, Any]:
        esRequest = self._translateRequest(request=request)
        esResponse = self.searcher.search(request=esRequest)
        return self._translateResponse(esResponse=esResponse)

    def _translateRequest(self, request: SearchRequest) -> Dict[str, Any]:
        # qeury rewrite
        # filter query
        # knn query?
        # aggs
        # size & offset
        self.logger.warn("Not Implemented yet")
        return {}

    def _translateResponse(self, esResponse: Dict[str, Any]) -> Dict[str, Any]:
        return esResponse
