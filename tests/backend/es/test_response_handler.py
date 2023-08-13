import pytest

from backend.es.response_handler import (
    translate_facets,
    translate_results,
    translate_summary,
)
from backend.es.searcher import EsResponse, HitItem, HitsData
from backend.models import (
    FacetData,
    FacetItem,
    Filter,
    SearchOptions,
    SearchQuery,
    SearchRequest,
    SearchResult,
)


@pytest.mark.parametrize(
    ("es_res", "search_req", "expected"),
    [
        (
            EsResponse(
                took=36,
                timed_out=False,
                _shards={},
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
                took=36,
                timed_out=False,
                _shards={},
                hits=HitsData(total={"value": 59}, max_score=100, hits=[]),
                aggregations=None,
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
                _shards={},
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
                            _id="B08X3LS1V5",
                            _score=565.36646,
                            _source={
                                "product_id": "B08X3LS1V5",
                                "product_title": "M’ｓカニカン 12ｍｍ 100個 シルバー マスクチェーン ネックレス メガネチェーン ハンドメイド チャーム",
                                "product_brand": "ノーブランド品",
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
                            },
                        },
                        "product_id": {"raw": "B08X3LS1V5"},
                        "product_title": {"raw": "M’ｓカニカン 12ｍｍ 100個 シルバー マスクチェーン ネックレス メガネチェーン ハンドメイド チャーム"},
                        "product_brand": {"raw": "ノーブランド品"},
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


@pytest.mark.parametrize(
    ("es_res", "search_req", "expected"),
    [
        (
            EsResponse(
                timed_out=False,
                took=0,
                _shards={},
                hits=HitsData(total=0, max_score=0, hits=[]),
                aggregations={
                    "facet_bucket_all": {
                        "doc_count": 5885,
                        "product_locale": {
                            "doc_count_error_upper_bound": 0,
                            "sum_other_doc_count": 0,
                            "buckets": [{"key": "jp", "doc_count": 5885}],
                        },
                        "product_color": {
                            "doc_count_error_upper_bound": 0,
                            "sum_other_doc_count": 1985,
                            "buckets": [
                                {"key": "ブラック", "doc_count": 434},
                                {"key": "ホワイト", "doc_count": 416},
                                {"key": "シルバー", "doc_count": 164},
                                {"key": "グレー", "doc_count": 118},
                                {"key": "ピンク", "doc_count": 110},
                                {"key": "白", "doc_count": 97},
                                {"key": "ブルー", "doc_count": 68},
                                {"key": "ゴールド", "doc_count": 59},
                                {"key": "クリア", "doc_count": 48},
                                {"key": "レッド", "doc_count": 47},
                                {"key": "ネイビー", "doc_count": 40},
                                {"key": "ベージュ", "doc_count": 34},
                                {"key": "グリーン", "doc_count": 31},
                                {"key": "黒", "doc_count": 29},
                                {"key": "クリスタル · クリア", "doc_count": 25},
                                {"key": "パープル", "doc_count": 24},
                                {"key": "ブラウン", "doc_count": 22},
                                {"key": "イエロー", "doc_count": 21},
                                {"key": "オレンジ", "doc_count": 17},
                                {"key": "赤", "doc_count": 16},
                            ],
                        },
                    },
                },
            ),
            SearchRequest(
                query=SearchQuery(filters=[]),
                options=SearchOptions(),
            ),
            SearchResult(
                facets={
                    "product_locale": [FacetItem(data=[FacetData(value="jp", count=5885)], type="value")],
                    "product_color": [
                        FacetItem(
                            data=[
                                FacetData(value="ブラック", count=434),
                                FacetData(value="ホワイト", count=416),
                                FacetData(value="シルバー", count=164),
                                FacetData(value="グレー", count=118),
                                FacetData(value="ピンク", count=110),
                                FacetData(value="白", count=97),
                                FacetData(value="ブルー", count=68),
                                FacetData(value="ゴールド", count=59),
                                FacetData(value="クリア", count=48),
                                FacetData(value="レッド", count=47),
                                FacetData(value="ネイビー", count=40),
                                FacetData(value="ベージュ", count=34),
                                FacetData(value="グリーン", count=31),
                                FacetData(value="黒", count=29),
                                FacetData(value="クリスタル · クリア", count=25),
                                FacetData(value="パープル", count=24),
                                FacetData(value="ブラウン", count=22),
                                FacetData(value="イエロー", count=21),
                                FacetData(value="オレンジ", count=17),
                                FacetData(value="赤", count=16),
                            ],
                            type="value",
                        )
                    ],
                }
            ),
        ),
        (
            EsResponse(
                timed_out=False,
                took=0,
                _shards={},
                hits=HitsData(total=0, max_score=0, hits=[]),
                aggregations={
                    "facet_bucket_product_locale": {
                        "doc_count": 12,
                        "product_locale": {
                            "doc_count_error_upper_bound": 0,
                            "sum_other_doc_count": 0,
                            "buckets": [{"key": "jp", "doc_count": 12}],
                        },
                    },
                    "facet_bucket_all": {"doc_count": 12},
                    "facet_bucket_product_color": {
                        "doc_count": 39,
                        "product_color": {
                            "doc_count_error_upper_bound": 0,
                            "sum_other_doc_count": 0,
                            "buckets": [
                                {"key": "ホワイト", "doc_count": 12},
                                {"key": "ピンクベージュ", "doc_count": 3},
                                {"key": "シルクベージュ", "doc_count": 2},
                                {"key": "ピンク(5枚入)", "doc_count": 2},
                                {"key": "ブラック(5枚入)", "doc_count": 2},
                                {"key": "1)ホワイト", "doc_count": 1},
                                {"key": "2)グレー", "doc_count": 1},
                                {"key": "ウォールナットブラウン", "doc_count": 1},
                                {"key": "オリーブカーキ", "doc_count": 1},
                                {"key": "グレー", "doc_count": 1},
                                {"key": "ストームグレー", "doc_count": 1},
                                {"key": "ネイビー", "doc_count": 1},
                                {"key": "ホワイト(7枚入)", "doc_count": 1},
                            ],
                        },
                    },
                },
            ),
            SearchRequest(
                query=SearchQuery(
                    filters=[
                        Filter(field="product_color", values=["ホワイト"], type="all"),
                    ]
                ),
                options=SearchOptions(),
            ),
            SearchResult(
                facets={
                    "product_locale": [FacetItem(data=[FacetData(value="jp", count=12)], type="value")],
                    "product_color": [
                        FacetItem(
                            data=[
                                FacetData(value="ホワイト", count=12),
                                FacetData(value="ピンクベージュ", count=3),
                                FacetData(value="シルクベージュ", count=2),
                                FacetData(value="ピンク(5枚入)", count=2),
                                FacetData(value="ブラック(5枚入)", count=2),
                                FacetData(value="1)ホワイト", count=1),
                                FacetData(value="2)グレー", count=1),
                                FacetData(value="ウォールナットブラウン", count=1),
                                FacetData(value="オリーブカーキ", count=1),
                                FacetData(value="グレー", count=1),
                                FacetData(value="ストームグレー", count=1),
                                FacetData(value="ネイビー", count=1),
                                FacetData(value="ホワイト(7枚入)", count=1),
                            ],
                            type="value",
                        )
                    ],
                }
            ),
        ),
    ],
)
def test_translate_facets(es_res, search_req, expected):
    tmp = SearchResult()
    result = translate_facets(es_res=es_res, search_request=search_req, search_result=tmp)
    assert result == expected
