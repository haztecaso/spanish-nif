# spanish-nif

*Pydantic validators for spanish identification codes: NIF, DNI and NIE.*

[![test badge](https://github.com/haztecaso/spanish-nif/actions/workflows/test.yml/badge.svg)](https://github.com/haztecaso/spanish-nif/actions/workflows/test.yml)
[![Supported Python versions](https://img.shields.io/badge/python-3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/haztecaso/spanish-nif/blob/main/pyproject.toml)
[![PyPI version](https://img.shields.io/pypi/v/spanish-nif.svg)](https://pypi.org/project/spanish-nif)
[![Static Badge](https://img.shields.io/badge/Documentation-2B8AE2)](https://haztecaso.github.io/spanish-nif)

[//]: # (start)

This library turns Spanish identification numbers into first-class Python types.
Each class (`NIF`, `DNI`, `NIE`) subclasses `str`, validates its control letter on
construction, and plugs straight into [Pydantic](https://docs.pydantic.dev/) so you can drop it into your
data models without writing bespoke validators.

> ⚠️ **AI-generated library:** This library may contain severe vulnerabilities
> and should not be trusted for critical workflows. Use at your own risk; it was
> produced with the Codex AI assistant.

## Installation

### pip

```bash
python -m pip install spanish-nif
```

### uv

```bash
uv pip install spanish-nif
```

## Quick examples

```python
from spanish_nif import DNI, NIE, NIF

DNI("12345678Z")          # returns a validated DNI string
NIE.is_valid("X1234567L") # -> True
NIF("K0867756N").variant  # -> "klm"
```

```python
from spanish_nif import DNI, NIF

fresh_dni = DNI.random()
some_nif = NIF.random()          # variant chosen automatically
klm_nif = NIF.random(variant="klm")
```

```python
from pydantic import BaseModel
from spanish_nif import NIF

class TaxPayer(BaseModel):
    nif: NIF

tax_payer = TaxPayer(nif="12345678Z")
assert tax_payer.nif == "12345678Z"
```

* Invalid inputs raise an `InvalidIdentification` subclass with a helpful message.
* Normalisation uppercases the value and validates the control-letter sequence; inputs must already be correctly formatted.
* Need dummy data for tests or demos? Each class exposes a `.random()` helper; pass a `random.Random` instance only if you require deterministic output.

## Related Projects

- [validarnif](https://pypi.org/project/validarnif/) – Python module exposing procedural validators for NIF/NIE/CIF and optional preprocessing utilities; _spanish-nif_ instead wraps those rules in reusable string subclasses with Pydantic/JSON Schema integration.
- [spanish-dni](https://pypi.org/project/spanish-dni/) – Python package with validator functions and generators focused on list processing; our library prioritises strong typing and schema metadata for application models.
- [spain-id](https://www.npmjs.com/package/spain-id) – TypeScript/Node toolkit validating NIF/NIE/CIF in browser and server environments, whereas _spanish-nif_ targets Python workflows.
- [ulabox/nif-validator](https://packagist.org/packages/ulabox/nif-validator) – PHP utility offering static `isValid*` helpers for CIF, DNI and NIE; our package emphasises typed models and Pydantic interoperability rather than imperative checks.
- [criptalia/spanish_dni_validator](https://github.com/criptalia/spanish_dni_validator) – Go port of the ulabox/NIF validator covering DNI, NIE and CIF with `IsValid*` helpers; _spanish-nif_ instead provides Python string subclasses with declarative Pydantic integration.
