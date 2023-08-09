import pytest

from backend.es.response_handler import (
    translate_facets,
    translate_results,
    translate_summary,
)
from backend.es.searcher import EsResponse, HitItem, HitsData
from backend.models import SearchOptions, SearchQuery, SearchRequest, SearchResult


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
    ("es_res", "expected"),
    [
        (
            EsResponse(
                timed_out=False,
                took=0,
                aggregations=None,
                hits=HitsData(
                    total=0,
                    max_score=0,
                    hits=[
                        HitItem(
                            _index="esci-products",
                            _id="B08X3LS1V5",
                            _score=565.36646,
                            _source={
                                "product_id": "B08X3LS1V5",
                                "product_title": "M’ｓカニカン 12ｍｍ 100個 シルバー マスクチェーン ネックレス メガネチェーン ハンドメイド チャーム",
                                "product_brand": "ノーブランド品",
                            },
                            highlight={
                                "product_title.ja": [
                                    "M’ｓカニカン 12ｍｍ 100個 シルバー <em>マスク</em><em>チェーン</em> ネックレス メガネ<em>チェーン</em> ハンドメイド チャーム"
                                ],
                                "product_description.ja": [
                                    "ジュエリー修復、手作りアクセサリー、ハンドメイド作品への飾り付け、DIYなど様々な用途にお使いいただけます メガネチャーム、<em>マスク</em>チャーム、ネックレスの修理などにも最適です"
                                ],
                            },
                        ),
                        HitItem(
                            _index="esci-products",
                            _id="B071J4TRNW",
                            _score=28.356335,
                            _source={
                                "product_id": "B071J4TRNW",
                                "product_title": "自転車 チェーンクリーナー BeiLan 自転車 チェーン自転車 チェーン オイル 洗浄 掃除 チェーン洗浄器＋チェーンブラシ 3点セット",
                                "product_brand": "BeiLan",
                            },
                            _ignored=["product_bullet_point"],
                            highlight={
                                "product_title.ja": [
                                    "自転車 <em>チェーン</em>クリーナー BeiLan 自転車 <em>チェーン</em>自転車 <em>チェーン</em> オイル 洗浄 掃除 <em>チェーン</em>洗浄器＋<em>チェーン</em>ブラシ 3点セット"
                                ],
                                "product_description.ja": [
                                    "<em>チェーン</em>洗浄器：<em>チェーン</em>を挟んで、洗浄剤をいれてペダルをまわして、簡単に自転車<em>チェーン</em>の洗浄ができます 。",
                                    "<em>チェーン</em>ブラシ：適度なカーブの付いたギザ状の刃は、ギアの間に深く詰まった泥を確実にかき出し、ナイロンブラシはディレーラーや<em>チェーン</em>などの汚れ落としに。",
                                    "<em>チェーン</em>のブラッシングから、拭き取らないに<em>チェーン</em>洗浄システム。手作業では行いにくい<em>チェーン</em>プレートの内側に入り込んだ汚れもかき出します。",
                                ],
                            },
                        ),
                    ],
                ),
            ),
            SearchResult(
                results=[
                    {
                        "id": {"raw": "B08X3LS1V5"},
                        "_meta": {
                            "id": "B08X3LS1V5",
                            "rawHit": {
                                "_id": "B08X3LS1V5",
                                "_index": "esci-products",
                                "_score": 565.36646,
                                "_source": {
                                    "product_id": "B08X3LS1V5",
                                    "product_title": "M’ｓカニカン 12ｍｍ 100個 シルバー マスクチェーン ネックレス メガネチェーン ハンドメイド チャーム",
                                    "product_brand": "ノーブランド品",
                                },
                                "highlight": {
                                    "product_title.ja": [
                                        "M’ｓカニカン 12ｍｍ 100個 シルバー <em>マスク</em><em>チェーン</em> ネックレス メガネ<em>チェーン</em> ハンドメイド チャーム"
                                    ],
                                    "product_description.ja": [
                                        "ジュエリー修復、手作りアクセサリー、ハンドメイド作品への飾り付け、DIYなど様々な用途にお使いいただけます メガネチャーム、<em>マスク</em>チャーム、ネックレスの修理などにも最適です"
                                    ],
                                },
                            },
                        },
                        "product_id": {"raw": "B08X3LS1V5"},
                        "product_title": {"raw": "M’ｓカニカン 12ｍｍ 100個 シルバー マスクチェーン ネックレス メガネチェーン ハンドメイド チャーム"},
                        "product_brand": {"raw": "ノーブランド品"},
                        "product_title.ja": {
                            "snippet": [
                                "M’ｓカニカン 12ｍｍ 100個 シルバー <em>マスク</em><em>チェーン</em> ネックレス メガネ<em>チェーン</em> ハンドメイド チャーム"
                            ]
                        },
                        "product_description.ja": {
                            "snippet": [
                                "ジュエリー修復、手作りアクセサリー、ハンドメイド作品への飾り付け、DIYなど様々な用途にお使いいただけます メガネチャーム、<em>マスク</em>チャーム、ネックレスの修理などにも最適です"
                            ]
                        },
                    },
                    {
                        "id": {"raw": "B071J4TRNW"},
                        "_meta": {
                            "id": "B071J4TRNW",
                            "rawHit": {
                                "_index": "esci-products",
                                "_id": "B071J4TRNW",
                                "_score": 28.356335,
                                "_ignored": ["product_bullet_point"],
                                "_source": {
                                    "product_id": "B071J4TRNW",
                                    "product_title": "自転車 チェーンクリーナー BeiLan 自転車 チェーン自転車 チェーン オイル 洗浄 掃除 チェーン洗浄器＋チェーンブラシ 3点セット",
                                    "product_brand": "BeiLan",
                                },
                                "highlight": {
                                    "product_title.ja": [
                                        "自転車 <em>チェーン</em>クリーナー BeiLan 自転車 <em>チェーン</em>自転車 <em>チェーン</em> オイル 洗浄 掃除 <em>チェーン</em>洗浄器＋<em>チェーン</em>ブラシ 3点セット"
                                    ],
                                    "product_description.ja": [
                                        "<em>チェーン</em>洗浄器：<em>チェーン</em>を挟んで、洗浄剤をいれてペダルをまわして、簡単に自転車<em>チェーン</em>の洗浄ができます 。",
                                        "<em>チェーン</em>ブラシ：適度なカーブの付いたギザ状の刃は、ギアの間に深く詰まった泥を確実にかき出し、ナイロンブラシはディレーラーや<em>チェーン</em>などの汚れ落としに。",
                                        "<em>チェーン</em>のブラッシングから、拭き取らないに<em>チェーン</em>洗浄システム。手作業では行いにくい<em>チェーン</em>プレートの内側に入り込んだ汚れもかき出します。",
                                    ],
                                },
                            },
                        },
                        "product_id": {"raw": "B071J4TRNW"},
                        "product_title": {
                            "raw": "自転車 チェーンクリーナー BeiLan 自転車 チェーン自転車 チェーン オイル 洗浄 掃除 チェーン洗浄器＋チェーンブラシ 3点セット"
                        },
                        "product_brand": {"raw": "BeiLan"},
                        "product_title.ja": {
                            "snippet": [
                                "自転車 <em>チェーン</em>クリーナー BeiLan 自転車 <em>チェーン</em>自転車 <em>チェーン</em> オイル 洗浄 掃除 <em>チェーン</em>洗浄器＋<em>チェーン</em>ブラシ 3点セット"
                            ]
                        },
                        "product_description.ja": {
                            "snippet": [
                                "<em>チェーン</em>洗浄器：<em>チェーン</em>を挟んで、洗浄剤をいれてペダルをまわして、簡単に自転車<em>チェーン</em>の洗浄ができます 。",
                                "<em>チェーン</em>ブラシ：適度なカーブの付いたギザ状の刃は、ギアの間に深く詰まった泥を確実にかき出し、ナイロンブラシはディレーラーや<em>チェーン</em>などの汚れ落としに。",
                                "<em>チェーン</em>のブラッシングから、拭き取らないに<em>チェーン</em>洗浄システム。手作業では行いにくい<em>チェーン</em>プレートの内側に入り込んだ汚れもかき出します。",
                            ]
                        },
                    },
                ]
            ),
        )
    ],
)
def test_translate_results(es_res, expected):
    tmp = SearchResult()
    result = translate_results(es_res=es_res, search_result=tmp)
    assert result == expected


@pytest.mark.parametrize(("expected"), [(None)])
def test_translate_facets(expected):
    print(f"not impremented {expected}")
    tmp = SearchResult()
    translate_facets(es_res=None, search_request=None, search_result=tmp)
