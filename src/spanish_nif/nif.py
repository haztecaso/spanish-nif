"""Utilities for working with Spanish Número de Identificación Fiscal (NIF)."""

from __future__ import annotations

import re
from typing import Any

from ._base import InvalidIdentification, PydanticStringID
from .dni import DNI, InvalidDNI
from .nie import NIE, InvalidNIE


class InvalidNIF(InvalidIdentification):
    """Raised when a NIF does not comply with format or control-letter rules."""


class NIF(PydanticStringID):
    """Validated Spanish NIF string.

    This covers natural-person identifiers: standard DNI numbers, NIE numbers
    (foreign residents), and legacy prefixes K/L/M.
    """

    json_pattern = r"^(?:\d{8}|[KLMXYZ]\d{7})[A-Z]$"
    json_examples = ["12345678Z", "K0867756N", "X1234567L"]
    json_description = (
        "Número de Identificación Fiscal for natural persons. Accepts DNI, NIE, "
        "and legacy K/L/M prefixes."
    )

    _klm_pattern = re.compile(r"^([KLM])(\d{7})([A-Z])$")

    def __new__(cls, value: Any) -> "NIF":
        return super().__new__(cls, value)

    @classmethod
    def _normalize(cls, value: Any) -> str:
        normalized = str(value).upper()
        if not normalized:
            raise InvalidNIF("NIF cannot be empty")

        # NIE handling (X/Y/Z prefixes)
        try:
            return str(NIE(normalized))
        except InvalidNIE:
            pass

        # Standard DNI (8 digits)
        try:
            return str(DNI(normalized))
        except InvalidDNI:
            pass

        # Legacy K/L/M prefixes (7 digits + letter)
        match = cls._klm_pattern.fullmatch(normalized)
        if match:
            _, digits, letter = match.groups()
            expected = DNI._control_letters[int(digits) % 23]
            if letter != expected:
                raise InvalidNIF(f"Invalid NIF control letter; expected {expected}")
            return normalized

        raise InvalidNIF(
            "NIF must correspond to a valid DNI, NIE, or legacy K/L/M format"
        )

    @property
    def variant(self) -> str:
        """Return the identifier variant: ``dni``, ``nie`` or ``legacy``."""

        prefix = self[0]
        if prefix in "XYZ":
            return "nie"
        if prefix in "KLM":
            return "legacy"
        return "dni"

    @property
    def digits(self) -> str:
        """Return the digits used to compute the control letter."""

        if self.variant == "nie":
            numeric = NIE._prefix_map[self[0]] + self[1:8]
            return numeric
        if self.variant == "legacy":
            return self[1:8]
        return self[:8]

    @property
    def number(self) -> int:
        """Return the numeric component that drives the control letter."""

        return int(self.digits)

    @property
    def letter(self) -> str:
        """Return the control letter."""

        return self[-1]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Return ``True`` when *value* is a valid NIF."""

        try:
            cls(value)
        except InvalidNIF:
            return False
        return True


__all__ = ["NIF", "InvalidNIF"]
