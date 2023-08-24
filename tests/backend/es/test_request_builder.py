import json

import pytest

from backend.es.request_builder import (
    build_aggs_and_post_filter,
    build_query,
    build_size_offset,
    build_source,
)
from backend.es.searcher import EsHighlight, EsRequest, EsRequestSource
from backend.models import Filter, SearchOptions, SearchQuery, SearchRequest


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (SearchQuery(current=1, results_per_page=20), EsRequest(size=20, from_=0)),
        (SearchQuery(current=2, results_per_page=20), EsRequest(size=20, from_=20)),
    ],
)
def test_build_size_offset(input, expected):
    tmp = EsRequest()
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
            EsRequest(
                _source=EsRequestSource(includes=["a", "b", "c", "d"]), highlight=EsHighlight(fields={"b": {}, "d": {}})
            ),
        )
    ],
)
def test_build_source(input, expected):
    tmp = EsRequest()
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
            EsRequest(
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
            EsRequest(
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
    tmp = EsRequest()
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
            EsRequest(
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
        (
            SearchRequest(
                query=SearchQuery(
                    filters=[
                        Filter(field="a", values=["e"], type="all"),
                        Filter(field="c", values=["d"], type="all"),
                    ]
                ),
                options=SearchOptions(
                    facets={
                        "a": {"type": "value"},
                        "b": {"type": "value", "sort": {"key": "asc"}},
                        "c": {"type": "value", "size": 30},
                    }
                ),
            ),
            EsRequest(
                post_filter=json.loads(
                    """
                    {
                        "bool": {
                            "must": [
                                { "bool": { "should": [{ "term": { "a": "e" } }] } },
                                { "bool": { "should": [{ "term": { "c": "d" } }] } }
                            ]
                        }
                    }
                    """
                ),
                aggs=json.loads(
                    """
                    {
                        "facet_bucket_all": {
                            "aggs": {},
                            "filter": {
                                "bool": {
                                    "must": [
                                        { "bool": { "should": [{ "term": { "a": "e" } }] } },
                                        { "bool": { "should": [{ "term": { "c": "d" } }] } }
                                    ]
                                }
                            }
                        },
                        "facet_bucket_a": {
                            "aggs": {
                                "a": {
                                    "terms": {
                                        "field": "a",
                                        "size": 20,
                                        "order": { "_count": "desc" }
                                    }
                                }
                            },
                            "filter": {
                                "bool": {
                                    "must": [
                                        { "bool": { "should": [{ "term": { "c": "d" } }] } }
                                    ]
                                }
                            }
                        },
                        "facet_bucket_b": {
                            "aggs": {
                                "b": {
                                    "terms": {
                                        "field": "b",
                                        "size": 20,
                                        "order": { "_key": "asc" }
                                    }
                                }
                            },
                            "filter": {
                                "bool": {
                                    "must": [
                                        { "bool": { "should": [{ "term": { "a": "e" } }] } },
                                        { "bool": { "should": [{ "term": { "c": "d" } }] } }
                                    ]
                                }
                            }
                        },
                        "facet_bucket_c": {
                            "aggs": {
                                "c": {
                                    "terms": {
                                        "field": "c",
                                        "size": 30,
                                        "order": { "_count": "desc" }
                                    }
                                }
                            },
                            "filter": {
                                "bool": {
                                    "must": [
                                        { "bool": { "should": [{ "term": { "a": "e" } }] } }
                                    ]
                                }
                            }
                        }
                    }
                    """
                ),
            ),
        ),
    ],
)
def test_build_aggs_and_post_filter(input, expected):
    tmp = EsRequest()
    result = build_aggs_and_post_filter(request=input, es_request=tmp)
    assert result == expected
