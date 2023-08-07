import json

import pytest

from backend.es.response_handler import (
    translate_facets,
    translate_results,
    translate_summary,
)
from backend.es.searcher import EsResponse, HitsData
from backend.models import SearchOptions, SearchQuery, SearchRequest, SearchResult


def get_es_response_from_file(request: pytest.FixtureRequest) -> EsResponse:
    rootdir = request.config.rootpath
    es_response_path = rootdir.joinpath("tests/data/es/es_response.json")
    with open(es_response_path, "r") as f:
        raw_json = json.load(f)
    return raw_json


@pytest.mark.parametrize(
    ("es_res", "search_req", "expected"),
    [
        (
            EsResponse(
                took=36,
                timed_out=False,
                hits=HitsData(total={"value": 5885}, max_score=100, hits=[]),
                aggregations=None,
            ),
            SearchRequest(
                query=SearchQuery(search_term="マスク　チェーン", current=1, results_per_page=20), options=SearchOptions()
            ),
            SearchResult(
                result_search_term="マスク　チェーン",
                total_pages=295,
                paging_start=1,
                paging_end=20,
                was_searched=False,
                total_results=5885,
            ),
        ),
        (
            EsResponse(
                took=36, timed_out=False, hits=HitsData(total={"value": 59}, max_score=100, hits=[]), aggregations=None
            ),
            SearchRequest(
                query=SearchQuery(search_term="グローブ", current=3, results_per_page=20), options=SearchOptions()
            ),
            SearchResult(
                result_search_term="グローブ",
                total_pages=3,
                paging_start=41,
                paging_end=59,
                was_searched=False,
                total_results=59,
            ),
        ),
    ],
)
def test_translate_summary(es_res, search_req, expected):
    tmp = SearchResult()
    result = translate_summary(es_res=es_res, search_request=search_req, search_result=tmp)
    assert result == expected


@pytest.mark.parametrize(
    ("expected"),
    [
        (
            SearchResult(
                result_search_term="マスク　チェーン",
                total_pages=295,
                paging_start=1,
                paging_end=20,
                was_searched=False,
                total_results=5885,
            )
        )
    ],
)
def test_translate_results(request, expected):
    es_res = get_es_response_from_file(request)
    tmp = SearchResult()
    result = translate_results(es_res=es_res, search_result=tmp)
    assert result == expected


@pytest.mark.parametrize(("expected"), [(None)])
def test_translate_facets(request, expected):
    print(f"not impremented {expected}")
    tmp = SearchResult()
    translate_facets(es_res=None, search_request=None, search_result=tmp)
