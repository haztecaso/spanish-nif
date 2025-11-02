"""Common helpers for Spanish identification string types."""

from __future__ import annotations

from typing import Any, ClassVar, Iterator, TypeVar, cast

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import CoreSchema, core_schema


class InvalidIdentification(ValueError):
    """Base error for invalid Spanish identification strings."""


_PydanticStringID = TypeVar("_PydanticStringID", bound="PydanticStringID")


class PydanticStringID(str):
    """String subclass with shared Pydantic integration helpers."""

    #: Regular expression pattern added to the generated JSON schema.
    json_pattern: ClassVar[str | None] = None
    #: Example value in generated JSON schema.
    json_examples: ClassVar[list[str]] = []
    #: Human readable description for schema consumers.
    json_description: ClassVar[str | None] = None

    @classmethod
    def _normalize(cls, value: Any) -> str:
        """Validate and normalize *value* into the canonical string form."""

        raise NotImplementedError("Subclasses must implement _normalize().")

    def __new__(cls: type[_PydanticStringID], value: Any) -> _PydanticStringID:
        normalized = cls._normalize(value)
        base_cls = cast("type[PydanticStringID]", cls)
        instance = str.__new__(base_cls, normalized)
        return cast(_PydanticStringID, instance)

    @classmethod
    def _validate_instance(
        cls: type[_PydanticStringID], value: Any
    ) -> _PydanticStringID:
        if isinstance(value, cls):
            return value
        return cls(value)

    @classmethod
    def __get_validators__(cls) -> Iterator[Any]:  # pragma: no cover - Pydantic v1
        yield cls._validate_instance

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:  # pragma: no cover - runtime exercised via tests
        return core_schema.no_info_after_validator_function(
            cls._validate_instance, core_schema.str_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:  # pragma: no cover - derived metadata
        json_schema = handler(schema)
        json_schema.setdefault("type", "string")
        if cls.json_pattern:
            json_schema.setdefault("pattern", cls.json_pattern)
        if cls.json_examples:
            json_schema.setdefault("examples", cls.json_examples)
        if cls.json_description:
            json_schema.setdefault("description", cls.json_description)
        return json_schema


__all__ = ["InvalidIdentification", "PydanticStringID"]
