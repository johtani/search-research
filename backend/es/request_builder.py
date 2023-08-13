import json
import logging

from backend.es.searcher import EsHighlight, EsReqeust
from backend.es.templates.aggs_template import (
    BucketAllTemplate,
    BucketAllWithFilterTemplate,
    FilterTemplate,
    PostFilterTemplate,
)
from backend.es.templates.query_template import (
    MatchAllQueryTemplate,
    SearchUIQueryTemplate,
)
from backend.models import ResultField, SearchOptions, SearchQuery, SearchRequest

logger = logging.getLogger(__file__)


def build_query(request: SearchRequest, es_request: EsReqeust) -> EsReqeust:
    if request.query.search_term:
        template = SearchUIQueryTemplate()
        query = template.render(request)
        logger.debug(query)
        es_request.query = json.loads(query)
    else:
        es_request.query = json.loads(MatchAllQueryTemplate().render())
    return es_request


def build_aggs_and_post_filter(request: SearchRequest, es_request: EsReqeust) -> EsReqeust:
    post_filters: dict[str, str] = {}
    if request.query.filters:
        for filter in request.query.filters:
            filter_template = FilterTemplate()
            post_filters[filter.field] = filter_template.render(filter=filter)
        post_filter_template = PostFilterTemplate()
        post_filter = post_filter_template.render(filters=post_filters)
        logger.debug(post_filter)
        es_request.post_filter = json.loads(post_filter)
    if request.options.facets:
        if post_filters:
            bucket_with_filter_template = BucketAllWithFilterTemplate()
            aggs = bucket_with_filter_template.render(post_filters=post_filters, options=request.options)
            logger.debug(aggs)
            es_request.aggs = json.loads(aggs)
            logger.debug(aggs)
        else:
            bucket_template = BucketAllTemplate()
            aggs = bucket_template.render(options=request.options)
            logger.debug(aggs)
            es_request.aggs = json.loads(aggs)
            logger.debug(aggs)
    return es_request


def build_size_offset(query: SearchQuery, es_request: EsReqeust) -> EsReqeust:
    es_request.from_ = (query.current - 1) * query.results_per_page
    es_request.size = query.results_per_page
    return es_request


def build_source(options: SearchOptions, es_request: EsReqeust) -> EsReqeust:
    if options.result_fields:
        for field in options.result_fields.keys():
            es_request.source.includes.append(field)
            if type(options.result_fields[field]) is ResultField and options.result_fields[field].snippet:
                if es_request.highlight is None:
                    es_request.highlight = EsHighlight()
                es_request.highlight.fields[field] = {}

    return es_request


def build_sort(query: SearchQuery, es_request: EsReqeust) -> EsReqeust:
    if query.sort_list is not None:
        logger.error("build_sort not implemented yet")
    return es_request
