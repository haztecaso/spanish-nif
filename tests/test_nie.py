import random

import pytest
from pydantic import BaseModel, ValidationError

from spanish_nif import NIE, InvalidNIE


def test_nie_valid_instance():
    nie = NIE("x1234567l")
    assert isinstance(nie, str)
    assert nie == "X1234567L"
    assert nie.prefix == "X"
    assert nie.digits == "1234567"
    assert nie.number == int("0" + "1234567")
    assert nie.letter == "L"


@pytest.mark.parametrize(
    "value, expected_message",
    [
        ("A1234567L", "NIE must start with X, Y or Z"),
        ("X123456L", "NIE must start with X, Y or Z"),
        ("X1234567A", "Invalid NIE control letter"),
    ],
)
def test_nie_invalid(value, expected_message):
    with pytest.raises(InvalidNIE) as excinfo:
        NIE(value)
    assert expected_message in str(excinfo.value)


def test_nie_is_valid_helper():
    assert NIE.is_valid("X1234567L") is True
    assert NIE.is_valid("X1234567A") is False


class _NIEModel(BaseModel):
    nie: NIE


def test_pydantic_accepts_valid_nie():
    model = _NIEModel.model_validate({"nie": "Y1234567X"})
    assert isinstance(model.nie, NIE)
    assert model.nie == "Y1234567X"


def test_pydantic_rejects_invalid_nie():
    with pytest.raises(ValidationError) as excinfo:
        _NIEModel.model_validate({"nie": "Z1234567A"})
    assert "Invalid NIE control letter" in str(excinfo.value)


def test_nie_random_generates_reproducible_values():
    rng = random.Random(42)
    values = [NIE.random(rng) for _ in range(3)]
    assert values == [NIE("Z1867825T"), NIE("X4614226N"), NIE("X3744854V")]
