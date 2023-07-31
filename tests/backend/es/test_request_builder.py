import pytest

from backend.es.request_builder import build_size_offset, build_source
from backend.es.searcher import EsReqeust, EsRequestSource
from backend.models import SearchOptions, SearchQuery


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (SearchQuery(current=1, results_per_page=20), EsReqeust(size=20, from_=0)),
        (SearchQuery(current=2, results_per_page=20), EsReqeust(size=20, from_=20)),
    ],
)
def test_build_size_offset(input, expected):
    tmp = EsReqeust()
    result = build_size_offset(input, tmp)
    assert result == expected


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (
            SearchOptions(result_fields={"a": {}, "b": {"snippet": {"size": 3, "fallback": True}}, "c": {}}),
            EsReqeust(source=EsRequestSource(includes=["a", "b", "c"])),
        )
    ],
)
def test_build_source(input, expected):
    tmp = EsReqeust()
    result = build_source(input, tmp)
    assert result == expected
