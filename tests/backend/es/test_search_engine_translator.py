import json

import pytest

from backend.es.search_engine_translator import EsTranslator
from backend.es.searcher import EsRequest, EsResponse
from backend.models import SearchRequest, SearchResult


def get_es_response_from_file(request: pytest.FixtureRequest) -> EsResponse:
    rootdir = request.config.rootpath
    es_response_path = rootdir.joinpath("tests/data/es/es_response_with_post_filter.json")
    with open(es_response_path, "r") as f:
        raw_json = json.load(f)
    return raw_json


def get_search_result_from_file(request: pytest.FixtureRequest) -> SearchResult:
    rootdir = request.config.rootpath
    search_result_path = rootdir.joinpath("tests/data/search-ui/search_result.json")
    with open(search_result_path, "r") as f:
        raw_json = json.load(f)
    return SearchResult(**raw_json)


def get_es_request_from_file(request: pytest.FixtureRequest) -> EsRequest:
    rootdir = request.config.rootpath
    es_response_path = rootdir.joinpath("tests/data/es/es_request_with_post_filter.json")
    with open(es_response_path, "r") as f:
        raw_json = json.load(f)
    return EsRequest.from_dict(raw_json)


def get_search_request_from_file(request: pytest.FixtureRequest) -> SearchRequest:
    rootdir = request.config.rootpath
    search_request_path = rootdir.joinpath("tests/data/search-ui/search_request.json")
    with open(search_request_path, "r") as f:
        raw_json = json.load(f)
    return SearchRequest(**raw_json)


@pytest.fixture
def target() -> type[EsTranslator]:
    return EsTranslator


def test__translate_request(request, target):
    input = get_search_request_from_file(request=request)
    expected = get_es_request_from_file(request=request)

    translator: EsTranslator = target()
    result = translator._translate_request(request=input)

    assert result == expected


def test__translate_response(request, target):
    search_request = get_search_request_from_file(request=request)
    es_response = get_es_response_from_file(request=request)
    expected = get_search_result_from_file(request=request)

    translator: EsTranslator = target()
    result = translator._translate_response(request=search_request, es_response=es_response)

    assert result == expected
