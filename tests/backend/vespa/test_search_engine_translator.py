import json

import pytest

from backend.models import SearchRequest, SearchResult
from backend.vespa.search_engine_translator import VespaTranslator
from backend.vespa.searcher import VespaRequest

# , VespaResponse


def get_search_result_from_file(request: pytest.FixtureRequest) -> SearchResult:
    rootdir = request.config.rootpath
    search_result_path = rootdir.joinpath("tests/data/search-ui/search_result.json")
    with open(search_result_path, "r") as f:
        raw_json = json.load(f)
    return SearchResult(**raw_json)


def get_search_request_from_file(request: pytest.FixtureRequest) -> SearchRequest:
    rootdir = request.config.rootpath
    search_request_path = rootdir.joinpath("tests/data/search-ui/search_request.json")
    with open(search_request_path, "r") as f:
        raw_json = json.load(f)
    return SearchRequest(**raw_json)


@pytest.fixture
def target() -> type[VespaTranslator]:
    return VespaTranslator


@pytest.mark.parametrize(
    ("expected"),
    [
        (
            VespaRequest(
                yql='select product_id, product_brand, product_title, product_title.ja, product_description.ja from product where default contains "マスク"',
                hits=20,
                offset=0,
                type_="all",
                ranking="",
                select="all(all(group(product_locale) order(-count()) each(output(count()))) \
all(group(product_brand) order(-count()) each(output(count()))) all(group(product_color) order(-count()) each(output(count()))) )",
            )
        )
    ],
)
def test__translate_request(request, target, expected):
    input = get_search_request_from_file(request=request)

    translator: VespaTranslator = target()
    result = translator._translate_request(request=input)

    assert result == expected


# def test__translate_response(request, target):
#     search_request = get_search_request_from_file(request=request)
#     vespa_response = get_vespa_response_from_file(request=request)
#     expected = get_search_result_from_file(request=request)

#     translator: VespaTranslator = target()
#     result = translator._translate_response(request=search_request, es_response=es_response)

#     assert result == expected
