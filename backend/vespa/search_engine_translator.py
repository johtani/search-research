import logging

from backend.models import SearchRequest, SearchResult
from backend.search_engine_translator import SearchEngineTranslator
from backend.vespa.config import Config, load_config
from backend.vespa.request_builder import VespaRequestBuilder
from backend.vespa.searcher import VespaRequest, VespaResponse, VespaSearchRepository


class VespaTranslator(SearchEngineTranslator):
    logger = logging.getLogger("VespaTranslator")

    def __init__(self) -> None:
        self.config: Config = load_config()
        self.searcher: VespaSearchRepository = VespaSearchRepository(self.config)

    def translate_and_search(self, request: SearchRequest) -> SearchResult:
        vespa_req = self._translate_request(request=request)
        self.logger.debug(f"{vespa_req=}")
        vespa_res = self.searcher.search(request=vespa_req)
        return self._translate_response(response=vespa_res)

    def _translate_request(self, request: SearchRequest) -> VespaRequest:
        builder: VespaRequestBuilder = VespaRequestBuilder(index=self.config.index)
        # set summary fields
        builder.summary_fields(options=request.options)
        # build where condition
        builder.conditions(query=request.query)
        # set limit / offset
        builder.limit_offset(query=request.query)
        # grouping (facets)
        builder.grouping(request=request)

        return builder.build()

    def _translate_response(self, response: VespaResponse) -> SearchResult:
        res = SearchResult()
        # build summary
        # build hits
        # build facets
        return res
