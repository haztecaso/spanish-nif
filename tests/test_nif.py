import pytest
from pydantic import BaseModel, ValidationError

from spanish_nif import DNI, NIE, NIF, InvalidNIF


class _NIFModel(BaseModel):
    nif: NIF


@pytest.mark.parametrize(
    "value, variant",
    [
        ("12345678z", "dni"),
        ("k0867756n", "legacy"),
        ("X1234567l", "nie"),
    ],
)
def test_nif_variants_normalize(value, variant):
    nif = NIF(value)
    assert nif == value.upper()
    assert nif.variant == variant


def test_nif_digits_number_letter_properties():
    standard = NIF("12345678Z")
    assert standard.digits == "12345678"
    assert standard.number == 12345678
    assert standard.letter == "Z"

    legacy = NIF("K0867756N")
    assert legacy.digits == "0867756"
    assert legacy.number == 867756
    assert legacy.letter == "N"

    nie_variant = NIF("Y1234567X")
    assert nie_variant.digits == NIE._prefix_map["Y"] + "1234567"
    assert nie_variant.number == int(NIE._prefix_map["Y"] + "1234567")


@pytest.mark.parametrize(
    "value",
    ["", "1234", "K1234567A", "Z1234567A", "A12345678", "12345678A"],
)
def test_nif_invalid_values(value):
    with pytest.raises(InvalidNIF):
        NIF(value)


def test_nif_is_valid_helper():
    assert NIF.is_valid("12345678Z") is True
    assert NIF.is_valid("K0867756N") is True
    assert NIF.is_valid("X1234567L") is True
    assert NIF.is_valid("12345678A") is False


def test_nif_pydantic_integration_accepts_variants():
    model = _NIFModel.model_validate({"nif": "k0867756n"})
    assert isinstance(model.nif, NIF)
    assert model.nif == "K0867756N"


def test_nif_pydantic_rejects_invalid():
    with pytest.raises(ValidationError):
        _NIFModel.model_validate({"nif": "K0867756A"})


def test_nif_accepts_existing_dni_and_nie_instances():
    nif_from_dni = NIF(DNI("12345678Z"))
    assert nif_from_dni.variant == "dni"

    nif_from_nie = NIF(NIE("X1234567L"))
    assert nif_from_nie.variant == "nie"
