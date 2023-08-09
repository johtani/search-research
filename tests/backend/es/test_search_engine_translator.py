import json

import pytest

from backend.es.searcher import EsResponse


def get_es_response_from_file(request: pytest.FixtureRequest) -> EsResponse:
    rootdir = request.config.rootpath
    es_response_path = rootdir.joinpath("tests/data/es/es_response.json")
    with open(es_response_path, "r") as f:
        raw_json = json.load(f)
    return raw_json
