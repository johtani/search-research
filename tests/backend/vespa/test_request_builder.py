import pytest

from backend.models import SearchOptions, SearchQuery
from backend.vespa.request_builder import VespaRequestBuilder
from backend.vespa.searcher import VespaRequest


@pytest.fixture
def target() -> VespaRequestBuilder:
    return VespaRequestBuilder(index="index")


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (
            SearchQuery(current=1, results_per_page=20),
            VespaRequest(hits=20, offset=0, yql="select * from index where true"),
        ),
        (
            SearchQuery(current=2, results_per_page=20),
            VespaRequest(hits=20, offset=20, yql="select * from index where true"),
        ),
    ],
)
def test_only_parse_limit_offset(target: VespaRequestBuilder, input, expected):
    target.limit_offset(input)
    result = target.build()
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
            VespaRequest(yql="select a, b, c, d from index where true", offset=0, hits=0),
        )
    ],
)
def test_only_summary_fields(target: VespaRequestBuilder, input, expected):
    target.summary_fields(options=input)
    result = target.build()
    assert result == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (
            SearchQuery(search_term="term"),
            VespaRequest(yql="select * from index where default contains term", offset=0, hits=0),
        )
    ],
)
def test_only_conditions(target: VespaRequestBuilder, input, expected):
    target.conditions(query=input)
    result = target.build()
    assert result == expected
