import logging
from typing import Any, Dict

import backend.es.request_builder as rb
from backend.es.config import Config, load_config
from backend.es.searcher import EsReqeust, EsSearchRepository
from backend.models import SearchRequest


class EsTranslator:
    logger = logging.getLogger("EsTranslator")

    def __init__(self) -> None:
        self.config: Config = load_config()
        self.searcher: EsSearchRepository = EsSearchRepository(self.config)

    def translate_and_search(self, request: SearchRequest) -> Dict[str, Any]:
        es_request = self._translate_request(request=request)
        es_response = self.searcher.search(request=es_request)
        return self._translate_response(es_response=es_response)

    def _translate_request(self, request: SearchRequest) -> EsReqeust:
        es_req = EsReqeust()
        # qeury rewrite
        es_req = rb.build_query(request=request, es_request=es_req)
        # filter query
        es_req = rb.build_filter_query(request=request, es_request=es_req)
        # knn query?

        # aggs
        es_req = rb.build_aggs(request=request, es_request=es_req)
        # size & offset
        es_req = rb.build_size_offset(query=request.query, es_request=es_req)
        # source
        es_req = rb.build_source(options=request.options, es_request=es_req)
        self.logger.warn("Not Implemented yet")
        return es_req

    def _translate_response(self, es_response: Dict[str, Any]) -> Dict[str, Any]:
        return es_response
