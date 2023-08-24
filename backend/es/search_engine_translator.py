import logging

import backend.es.request_builder as rb
import backend.es.response_handler as rh
from backend.es.config import Config, load_config
from backend.es.searcher import EsRequest, EsResponse, EsSearchRepository
from backend.models import SearchRequest, SearchResult


class EsTranslator:
    logger = logging.getLogger("EsTranslator")

    def __init__(self) -> None:
        self.config: Config = load_config()
        self.searcher: EsSearchRepository = EsSearchRepository(self.config)

    def translate_and_search(self, request: SearchRequest) -> SearchResult:
        es_request = self._translate_request(request=request)
        self.logger.debug(f"{es_request=}")
        es_response = self.searcher.search(request=es_request)
        return self._translate_response(request=request, es_response=es_response)

    def _translate_request(self, request: SearchRequest) -> EsRequest:
        es_req = EsRequest()
        # qeury rewrite
        es_req = rb.build_query(request=request, es_request=es_req)
        # knn query?

        # aggs & post filter
        es_req = rb.build_aggs_and_post_filter(request=request, es_request=es_req)
        # size & offset
        es_req = rb.build_size_offset(query=request.query, es_request=es_req)
        # source
        es_req = rb.build_source(options=request.options, es_request=es_req)
        # sort
        es_req = rb.build_sort(query=request.query, es_request=es_req)
        return es_req

    def _translate_response(self, request: SearchRequest, es_response: EsResponse) -> SearchResult:
        res = SearchResult()
        # summary
        res = rh.translate_summary(search_request=request, es_res=es_response, search_result=res)
        # results
        res = rh.translate_results(es_res=es_response, search_result=res)
        # fasets
        res = rh.translate_facets(search_request=request, es_res=es_response, search_result=res)
        return res
