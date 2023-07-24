from typing import Any, Dict, List

import pytest

from backend.processor import PipelineManager, Processor


# Test for apply_pipelines
# Create sample processors
# add a field
class AProcessor(Processor):
    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        doc["A"] = "A"
        return doc


# add b field
class BProcesssor(Processor):
    def apply(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        doc["B"] = "B"
        return doc


@pytest.mark.parametrize(
    ("pipeline", "input_doc", "expected_doc"), [([AProcessor()], {"C": "C"}, {"A": "A", "C": "C"})]
)
def test_single_processor(pipeline: List[Processor], input_doc: Dict[str, Any], expected_doc: Dict[str, Any]):
    target = PipelineManager(pipeline)

    actual = target.apply_pipelines(input_doc)

    assert actual == expected_doc


@pytest.mark.parametrize(
    ("pipeline", "input_doc", "expected_doc"),
    [([AProcessor(), BProcesssor()], {"C": "C"}, {"A": "A", "B": "B", "C": "C"})],
)
def test_multi_processors(pipeline: List[Processor], input_doc: Dict[str, Any], expected_doc: Dict[str, Any]):
    target = PipelineManager(pipeline)

    actual = target.apply_pipelines(input_doc)

    assert actual == expected_doc
