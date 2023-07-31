import logging

from backend.es.searcher import EsReqeust
from backend.models import SearchOptions, SearchQuery, SearchRequest

logger = logging.getLogger("es_request_builder")


def build_query(request: SearchRequest, es_request: EsReqeust) -> EsReqeust:
    if request.query.search_term is not None:
        logger.error("not implemented yet")
    return es_request


def build_filter_query(request: SearchRequest, es_request: EsReqeust) -> EsReqeust:
    if request.query.filters is not None:
        logger.error("not implemented yet")
    return es_request


def build_aggs(request: SearchRequest, es_request: EsReqeust) -> EsReqeust:
    if request.options.facets is not None:
        logger.error("not implemented yet")
    return es_request


def build_size_offset(query: SearchQuery, es_request: EsReqeust) -> EsReqeust:
    es_request.from_ = (query.current - 1) * query.results_per_page
    es_request.size = query.results_per_page
    return es_request


def build_source(options: SearchOptions, es_request: EsReqeust) -> EsReqeust:
    if options.result_fields is not None:
        logger.error("not implemented yet")
    return es_request
