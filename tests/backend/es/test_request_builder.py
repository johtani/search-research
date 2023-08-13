import json

import pytest

from backend.es.request_builder import (
    build_aggs,
    build_query,
    build_size_offset,
    build_source,
)
from backend.es.searcher import EsHighlight, EsReqeust, EsRequestSource
from backend.models import SearchOptions, SearchQuery, SearchRequest


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (SearchQuery(current=1, results_per_page=20), EsReqeust(size=20, from_=0)),
        (SearchQuery(current=2, results_per_page=20), EsReqeust(size=20, from_=20)),
    ],
)
def test_build_size_offset(input, expected):
    tmp = EsReqeust()
    result = build_size_offset(query=input, es_request=tmp)
    assert result == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (
            SearchOptions(
                result_fields={
                    "a": {},
                    "b": {"snippet": {"size": 3, "fallback": True}},
                    "c": {},
                    "d": {"snippet": {"size": 3, "fallback": True}},
                }
            ),
            EsReqeust(
                source=EsRequestSource(includes=["a", "b", "c", "d"]), highlight=EsHighlight(fields={"b": {}, "d": {}})
            ),
        )
    ],
)
def test_build_source(input, expected):
    tmp = EsReqeust()
    result = build_source(options=input, es_request=tmp)
    assert result == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (
            SearchRequest(
                query=SearchQuery(search_term="マスク　チェーン"),
                options=SearchOptions(search_fields={"a": {"weight": 3}, "b": {}, "c": {}}),
            ),
            EsReqeust(
                query=json.loads(
                    """
                {
                    "bool": {
                        "should": [
                            {
                                "multi_match": {
                                    "query": "マスク　チェーン",
                                    "fields": ["a^3", "b^1", "c^1"],
                                    "type": "best_fields",
                                    "operator": "and"
                                }
                            },
                            {
                                "multi_match": {
                                    "query": "マスク　チェーン",
                                    "fields": ["a^3", "b^1", "c^1"],
                                    "type": "cross_fields"
                                }
                            },
                            {"multi_match": {"query": "マスク　チェーン", "fields": ["a^3", "b^1", "c^1"], "type": "phrase"}},
                            {
                                "multi_match": {
                                    "query": "マスク　チェーン",
                                    "fields": ["a^3", "b^1", "c^1"],
                                    "type": "phrase_prefix"
                                }
                            }
                        ]
                    }
                }"""
                )
            ),
        ),
        (
            SearchRequest(
                query=SearchQuery(search_term=""),
                options=SearchOptions(search_fields={"a": {"weight": 3}, "b": {}, "c": {}}),
            ),
            EsReqeust(
                query=json.loads(
                    """
    { "match_all": {}}
    """
                )
            ),
        ),
    ],
)
def test_build_query(input, expected):
    tmp = EsReqeust()
    result = build_query(request=input, es_request=tmp)
    assert result == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (
            SearchRequest(
                query=SearchQuery(),
                options=SearchOptions(
                    facets={
                        "a": {"type": "value"},
                        "b": {"type": "value", "sort": {"key": "asc"}},
                        "c": {"type": "value", "size": 30},
                    }
                ),
            ),
            EsReqeust(
                aggs=json.loads(
                    """
                    {
                        "facet_bucket_all": {
                            "aggs": {
                                "a": {
                                    "terms": {
                                        "field": "a",
                                        "size": 20,
                                        "order": { "_count": "desc" }
                                    }
                                },
                                "b": {
                                    "terms": {
                                        "field": "b",
                                        "size": 20,
                                        "order": { "_key": "asc" }
                                    }
                                },
                                "c": {
                                    "terms": {
                                        "field": "c",
                                        "size": 30,
                                        "order": { "_count": "desc" }
                                    }
                                }
                            },
                            "filter": { "bool": { "must": [] } }
                        }
                    }
                    """
                )
            ),
        ),
    ],
)
def test_build_aggs(input, expected):
    tmp = EsReqeust()
    result = build_aggs(request=input, es_request=tmp)
    assert result == expected
