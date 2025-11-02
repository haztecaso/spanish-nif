import pytest
from pydantic import BaseModel, ValidationError

from spanish_nif import DNI, InvalidDNI


def test_dni_valid_instance():
    dni = DNI("12345678z")
    assert isinstance(dni, str)
    assert dni == "12345678Z"
    assert dni.digits == "12345678"
    assert dni.number == 12345678
    assert dni.letter == "Z"


@pytest.mark.parametrize(
    "value, expected_message",
    [
        ("1234567A", "DNI must consist of 8 digits followed by an uppercase letter"),
        ("12345678A", "Invalid DNI control letter"),
        ("ABCDEFGHX", "DNI must consist of 8 digits followed by an uppercase letter"),
    ],
)
def test_dni_invalid(value, expected_message):
    with pytest.raises(InvalidDNI) as excinfo:
        DNI(value)
    assert expected_message in str(excinfo.value)


def test_dni_is_valid_helper():
    assert DNI.is_valid("12345678Z") is True
    assert DNI.is_valid("12345678A") is False


class _DNIModel(BaseModel):
    dni: DNI


def test_pydantic_accepts_valid_dni():
    model = _DNIModel.model_validate({"dni": "12345678Z"})
    assert isinstance(model.dni, DNI)
    assert model.dni == "12345678Z"


def test_pydantic_rejects_invalid_dni():
    with pytest.raises(ValidationError) as excinfo:
        _DNIModel.model_validate({"dni": "12345678A"})
    assert "Invalid DNI control letter" in str(excinfo.value)
