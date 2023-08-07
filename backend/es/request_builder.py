import json
import logging

from backend.es.searcher import EsReqeust
from backend.es.templates.default_query_template import DefaultTemplate
from backend.models import SearchOptions, SearchQuery, SearchRequest

logger = logging.getLogger(__file__)


def build_query(request: SearchRequest, es_request: EsReqeust) -> EsReqeust:
    if request.query.search_term is not None:
        template = DefaultTemplate()
        query = template.template.render(query=request.query, fields=template.fields(request.options))
        logger.debug(query)
        es_request.query = json.loads(query)
    else:
        es_request.query = "*"
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
        for field in options.result_fields.keys():
            es_request.source.includes.append(field)
    return es_request
