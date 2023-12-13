import logging
import math
from typing import Dict, List

from backend.models import FacetItem, SearchRequest, SearchResult
from backend.vespa.searcher import VespaResponse

logger = logging.getLogger(__file__)


def translate_summary(
    vespa_res: VespaResponse, search_request: SearchRequest, search_result: SearchResult
) -> SearchResult:
    search_result.total_results = vespa_res.number_of_hits
    search_result.result_search_term = search_request.query.search_term
    search_result.paging_start = (search_request.query.current - 1) * search_request.query.results_per_page + 1
    search_result.paging_end = min(
        search_result.total_results, (search_request.query.current * search_request.query.results_per_page)
    )
    search_result.total_pages = math.ceil(search_result.total_results / search_request.query.results_per_page)
    return search_result


def translate_results_and_facets(vespa_res: VespaResponse, search_request: SearchRequest, search_result: SearchResult):
    for item in vespa_res.hits:
        if item[""]:
            _translate_facets(vespa_res=vespa_res, search_request=search_request, search_result=search_result)
        else:
            _translate_results(vespa_res=vespa_res, search_request=search_request, search_result=search_result)
    return search_result


def _translate_facets(vespa_res: VespaResponse, search_request: SearchRequest, search_result: SearchResult):
    facets: Dict[str, List[FacetItem]] = {}
    logger.debug(facets)
    pass


def _translate_results(vespa_res: VespaResponse, search_request: SearchRequest, search_result: SearchResult):
    pass
