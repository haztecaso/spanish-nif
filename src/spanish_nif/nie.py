"""Utilities for working with Spanish Número de Identidad de Extranjero (NIE) values."""

from __future__ import annotations

import re
from typing import Any

from ._base import InvalidIdentification, PydanticStringID


class InvalidNIE(InvalidIdentification):
    """Raised when an NIE does not comply with format or control-letter rules."""


class NIE(PydanticStringID):
    """Validated Spanish NIE string."""

    _pattern = re.compile(r"^([XYZ])(\d{7})([A-Z])$")
    _prefix_map = {"X": "0", "Y": "1", "Z": "2"}
    _control_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    json_pattern = r"^[XYZ]\d{7}[A-Z]$"
    json_examples = ["X1234567L"]
    json_description = (
        "Número de Identidad de Extranjero: X/Y/Z + 7 digits + control letter."
    )

    def __new__(cls, value: str) -> "NIE":
        return super().__new__(cls, cls._normalize(value))

    @classmethod
    def _normalize(cls, value: Any) -> str:
        normalized = str(value).upper()
        match = cls._pattern.fullmatch(normalized)
        if not match:
            raise InvalidNIE(
                "NIE must start with X, Y or Z followed by 7 digits and a control letter"
            )

        prefix, digits, letter = match.groups()
        numeric_value = int(cls._prefix_map[prefix] + digits)
        expected_letter = cls._control_letters[numeric_value % 23]
        if letter != expected_letter:
            raise InvalidNIE(f"Invalid NIE control letter; expected {expected_letter}")
        return normalized

    @property
    def prefix(self) -> str:
        """Return the leading status letter (X, Y or Z)."""

        return self[0]

    @property
    def digits(self) -> str:
        """Return the 7-digit numeric part."""

        return self[1:8]

    @property
    def number(self) -> int:
        """Return the numeric representation used in the control-letter computation."""

        return int(self._prefix_map[self.prefix] + self.digits)

    @property
    def letter(self) -> str:
        """Return the control letter."""

        return self[8]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Return ``True`` when *value* is a valid NIE."""

        try:
            cls(value)
        except InvalidNIE:
            return False
        return True


__all__ = ["NIE", "InvalidNIE"]
