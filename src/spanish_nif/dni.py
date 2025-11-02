"""Utilities for working with Spanish Documento Nacional de Identidad (DNI) numbers."""

from __future__ import annotations

import re
from typing import Any

from ._base import InvalidIdentification, PydanticStringID


class InvalidDNI(InvalidIdentification):
    """Raised when a DNI does not comply with format or control-letter rules."""


class DNI(PydanticStringID):
    """Validated Spanish DNI string.

    A DNI comprises 8 digits followed by a control letter. The letter is derived
    from the numeric part modulo 23 and mapped to the sequence
    ``TRWAGMYFPDXBNJZSQVHLCKE``.
    """

    _pattern = re.compile(r"^(\d{8})([A-Z])$")
    _control_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    json_pattern = r"^\d{8}[A-Z]$"
    json_examples = ["12345678Z"]
    json_description = (
        "Spanish Documento Nacional de Identidad: 8 digits plus control letter."
    )

    def __new__(cls, value: str) -> "DNI":
        return super().__new__(cls, cls._normalize(value))

    @classmethod
    def _normalize(cls, value: Any) -> str:
        normalized = str(value).upper()
        match = cls._pattern.fullmatch(normalized)
        if not match:
            raise InvalidDNI(
                "DNI must consist of 8 digits followed by an uppercase letter"
            )

        digits, letter = match.groups()
        expected_letter = cls._control_letters[int(digits) % 23]
        if letter != expected_letter:
            raise InvalidDNI(f"Invalid DNI control letter; expected {expected_letter}")
        return normalized

    @property
    def digits(self) -> str:
        """Return the zero-padded 8-digit numeric part."""

        return self[:8]

    @property
    def number(self) -> int:
        """Return the numeric portion of the DNI as an integer."""

        return int(self[:8])

    @property
    def letter(self) -> str:
        """Return the control letter."""

        return self[8]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Return ``True`` when *value* is a valid DNI."""

        try:
            cls(value)
        except InvalidDNI:
            return False
        return True


__all__ = ["DNI", "InvalidDNI"]
