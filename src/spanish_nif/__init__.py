"""Pydantic validators for Spanish identification codes: NIF, DNI and NIE."""

from ._base import InvalidIdentification
from .dni import DNI, InvalidDNI
from .nie import NIE, InvalidNIE
from .nif import NIF, InvalidNIF

__all__ = [
    "InvalidIdentification",
    "DNI",
    "InvalidDNI",
    "NIE",
    "InvalidNIE",
    "NIF",
    "InvalidNIF",
]
