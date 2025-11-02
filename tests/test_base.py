from __future__ import annotations

import pytest
from pydantic import BaseModel

from spanish_nif._base import InvalidIdentification, PydanticStringID


class _ExampleID(PydanticStringID):
    json_pattern = r"^ABC$"
    json_examples = ["ABC"]
    json_description = "Example ID"

    @classmethod
    def _normalize(cls, value):
        if str(value).upper() != "ABC":
            raise InvalidIdentification("invalid")
        return "ABC"


def test_instantiation_normalizes():
    assert _ExampleID("abc") == "ABC"


def test_invalid_raises():
    with pytest.raises(InvalidIdentification):
        _ExampleID("nope")


def test_validate_instance_returns_existing_instance():
    instance = _ExampleID("abc")
    assert _ExampleID._validate_instance(instance) is instance
    new_instance = _ExampleID._validate_instance("abc")
    assert isinstance(new_instance, _ExampleID)
    assert new_instance == "ABC"
    assert new_instance is not instance


class _ExampleModel(BaseModel):
    identifier: _ExampleID


def test_pydantic_integration_accepts_normalized():
    model = _ExampleModel.model_validate({"identifier": "abc"})
    assert model.identifier == "ABC"
    assert isinstance(model.identifier, _ExampleID)


def test_json_schema_metadata():
    schema = _ExampleModel.model_json_schema()
    props = schema["properties"]["identifier"]
    assert props["pattern"] == "^ABC$"
    assert props["examples"] == ["ABC"]
    assert props["description"] == "Example ID"
