import json
import logging
import math
from typing import Any, Dict, List

from backend.es.searcher import EsResponse, HitItem
from backend.models import FacetData, FacetItem, SearchRequest, SearchResult
from backend.templates.search_results_template import DocFields, DocTemplate, Field

logger = logging.getLogger(__file__)


def translate_summary(es_res: EsResponse, search_request: SearchRequest, search_result: SearchResult) -> SearchResult:
    search_result.result_search_term = search_request.query.search_term
    match es_res["hits"]["total"]:
        case int():
            search_result.total_results = es_res["hits"]["total"]
        case dict():
            search_result.total_results = int(es_res["hits"]["total"]["value"])
        case _:
            logger.error(f"Cannot get hits.total from response. {es_res['hits']['total']}")
    search_result.paging_start = (search_request.query.current - 1) * search_request.query.results_per_page + 1
    search_result.paging_end = min(
        search_result.total_results, (search_request.query.current * search_request.query.results_per_page)
    )
    search_result.total_pages = math.ceil(search_result.total_results / search_request.query.results_per_page)
    return search_result


def hits2doc(hit: HitItem) -> DocFields:
    fields: Dict[str, Field] = {}
    # highlightsと_sourceに取得するべきフィールドは入っているものとして処理をする。
    source_keys = hit["_source"].keys()
    if "highlight" in hit and hit["highlight"] is not None:
        highlights = hit["highlight"]
    else:
        highlights = {}
    highlight_keys = highlights.keys()
    for key in source_keys | highlight_keys:
        fields[key] = Field(raw=hit["_source"].get(key, ""), snippets=highlights.get(key, []))
    return DocFields(id=hit["_id"], raw=hit, fields=fields)


def translate_results(es_res: EsResponse, search_result: SearchResult) -> SearchResult:
    if es_res["hits"]["hits"] is not None:
        template = DocTemplate()
        for hit in es_res["hits"]["hits"]:
            # create DocFields from hits
            search_result.results.append(json.loads(template.render(hits2doc(hit=hit))))
    else:
        logger.debug("No hits")
    return search_result


def translate_facets(es_res: EsResponse, search_request: SearchRequest, search_result: SearchResult) -> SearchResult:
    if es_res["aggregations"]:
        if search_request.query.filters:
            search_result = translate_facets_with_post_filter(aggs=es_res["aggregations"], search_result=search_result)
        else:
            search_result = translate_facets_all(aggs=es_res["aggregations"], search_result=search_result)
    else:
        logger.debug("No aggregations")
    return search_result


def translate_facets_all(aggs: Dict[str, Dict[str, Any]], search_result: SearchResult) -> SearchResult:
    facets: Dict[str, List[FacetItem]] = {}
    for label in aggs["facet_bucket_all"].keys():
        if label != "doc_count":
            buckets = []
            for bucket in aggs["facet_bucket_all"][label]["buckets"]:
                buckets.append(FacetData(value=bucket["key"], count=bucket["doc_count"]))
            facet_item = FacetItem(data=buckets, type="value")
            facets[label] = [facet_item]
    search_result.facets = facets
    return search_result


def translate_facets_with_post_filter(aggs: Dict[str, Dict[str, Any]], search_result: SearchResult) -> SearchResult:
    facets: Dict[str, List[FacetItem]] = {}
    for label, item in aggs.items():
        if label != "facet_bucket_all":
            for field, value in item.items():
                if field != "doc_count":
                    buckets = []
                    for bucket in value["buckets"]:
                        buckets.append(FacetData(value=bucket["key"], count=bucket["doc_count"]))
                    facet_item = FacetItem(data=buckets, type="value")
                    facets[field] = [facet_item]
    search_result.facets = facets
    return search_result
