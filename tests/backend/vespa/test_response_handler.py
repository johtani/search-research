import pytest
from vespa.io import VespaQueryResponse

from backend.models import (
    FacetData,
    FacetItem,
    SearchOptions,
    SearchQuery,
    SearchRequest,
    SearchResult,
)
from backend.vespa.response_handler import (
    translate_results_and_facets,
    translate_summary,
)
from backend.vespa.searcher import VespaResponse


@pytest.mark.parametrize(
    ("vespa_res", "search_req", "expected"),
    [
        (
            VespaResponse(
                VespaQueryResponse(
                    status_code=200,
                    url="url",
                    json={
                        "root": {
                            "id": "toplevel",
                            "relevance": 1.0,
                            "fields": {"totalCount": 1356},
                            "coverage": {
                                "coverage": 100,
                                "documents": 339053,
                                "full": True,
                                "nodes": 1,
                                "results": 1,
                                "resultsFull": 1,
                            },
                        }
                    },
                )
            ),
            SearchRequest(
                query=SearchQuery(search_term="マスク", current=1, results_per_page=20), options=SearchOptions()
            ),
            SearchResult(
                result_search_term="マスク",
                total_pages=68,
                paging_start=1,
                paging_end=20,
                was_searched=False,
                total_results=1356,
            ),
        )
    ],
)
def test_translate_summary(vespa_res, search_req, expected):
    tmp = SearchResult()

    result = translate_summary(vespa_res=vespa_res, search_request=search_req, search_result=tmp)

    assert result == expected


@pytest.mark.parametrize(
    ("vespa_res", "search_req", "expected"),
    [
        (
            VespaResponse(
                VespaQueryResponse(
                    status_code=200,
                    url="url",
                    json={
                        "root": {
                            "id": "toplevel",
                            "relevance": 1.0,
                            "fields": {"totalCount": 1356},
                            "coverage": {
                                "coverage": 100,
                                "documents": 339053,
                                "full": True,
                                "nodes": 1,
                                "results": 1,
                                "resultsFull": 1,
                            },
                            "children": [
                                {
                                    "id": "group:root:0",
                                    "relevance": 1.0,
                                    "continuation": {"this": ""},
                                    "children": [
                                        {
                                            "id": "grouplist:product_locale",
                                            "relevance": 1.0,
                                            "label": "product_locale",
                                            "children": [
                                                {
                                                    "id": "group:string:jp",
                                                    "relevance": 1.0,
                                                    "value": "jp",
                                                    "fields": {"count()": 1356},
                                                }
                                            ],
                                        },
                                        {
                                            "id": "grouplist:product_color",
                                            "relevance": 1.0,
                                            "label": "product_color",
                                            "continuation": {"next": "BGAABEBMCBEBC"},
                                            "children": [
                                                {
                                                    "id": "group:string:",
                                                    "relevance": 1.0,
                                                    "value": "",
                                                    "fields": {"count()": 291},
                                                },
                                                {
                                                    "id": "group:string:ホワイト",
                                                    "relevance": 0.9,
                                                    "value": "ホワイト",
                                                    "fields": {"count()": 167},
                                                },
                                                {
                                                    "id": "group:string:ブラック",
                                                    "relevance": 0.8,
                                                    "value": "ブラック",
                                                    "fields": {"count()": 104},
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    "id": "index:esci-products/0/52864f27764293ae8dbafb8d",
                                    "relevance": 0.3606210779349873,
                                    "source": "esci-products",
                                    "fields": {
                                        "product_id": "B08F7QYBCF",
                                        "product_title": "マスク 50枚 3層構造 日本国内検品 【100枚入】 飛沫防止99% 使い捨てマスク 不織布 PM2.5 抗菌 風邪予防 防塵 花粉対策 超快適マスク お出かけ安心 ふつうサイズ 男女兼用 大人用 ホワイト (100枚)",
                                        "product_brand": "GOOSERA",
                                    },
                                },
                                {
                                    "id": "index:esci-products/0/57a1a2f13c535b6deb790772",
                                    "relevance": 0.3407388863177134,
                                    "source": "esci-products",
                                    "fields": {
                                        "product_id": "B08L5WDGVL",
                                        "product_title": "マスク 日本製 10枚 【個包装 カケンテスト認証済】不織布 白い 使い捨てマスク ES繊維 三層構造 不織布マスク 花粉 ほこり 高密度フィルター 長時間着用 ふつうサイズ 男女兼用 箱付き (マスク 10枚入り)",
                                        "product_brand": "Elcis",
                                    },
                                },
                                {
                                    "id": "index:esci-products/0/d7184acf6d4360040555d0e1",
                                    "relevance": 0.3388784631234001,
                                    "source": "esci-products",
                                    "fields": {
                                        "product_id": "B08M937NVY",
                                        "product_title": "マスク 日本製 150枚 【個包装 カケンテスト認証済】MARUBI 不織布 白い 使い捨てマスク ES繊維 三層構造 不織布マスク 花粉 ほこり 高密度フィルター 長時間着用 ふつうサイズ 男女兼用 箱付き (日本製マスク 150枚)",
                                        "product_brand": "MRB",
                                    },
                                },
                            ],
                        }
                    },
                )
            ),
            SearchRequest(query=SearchQuery(search_term="マスク", current=1, results_per_page=3), options=SearchOptions()),
            SearchResult(
                facets={
                    "product_locale": [FacetItem(data=[FacetData(value="jp", count=1356)], type="value")],
                    "product_color": [
                        FacetItem(
                            data=[
                                FacetData(value="", count=291),
                                FacetData(value="ホワイト", count=167),
                                FacetData(value="ブラック", count=104),
                            ],
                            type="value",
                        )
                    ],
                },
                results=[],
            ),
        )
    ],
)
def test_translate_results_and_facets(vespa_res, search_req, expected):
    tmp = SearchResult()

    result = translate_results_and_facets(vespa_res=vespa_res, search_request=search_req, search_result=tmp)

    assert result == expected
