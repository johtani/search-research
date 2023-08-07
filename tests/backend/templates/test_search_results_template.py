import json

import pytest

from backend.templates.search_results_template import DocFields, DocTemplate, Field


class TestDocTemplate:
    @pytest.fixture
    def target(self) -> type[DocTemplate]:
        from backend.templates.search_results_template import DocTemplate

        return DocTemplate

    @pytest.mark.parametrize(
        ("input", "expected"),
        [
            (
                DocFields(
                    id="id_str",
                    raw={"hoge": 1, "fuga": True},
                    fields={
                        "a": Field(raw="a_str", snippets=None),
                        "b": Field(raw="b_str", snippets=["b_str_1", "b_str_2"]),
                    },
                ),
                {
                    "id": {"raw": "id_str"},
                    "_meta": {"id": "id_str", "rawHit": {"hoge": 1, "fuga": True}},
                    "a": {"raw": "a_str"},
                    "b": {"snippet": ["b_str_1", "b_str_2"]},
                },
            )
        ],
    )
    def test_render(self, target: type[DocTemplate], input: DocFields, expected: str):
        actual = target().render(input)
        assert json.loads(actual) == expected
