# spanish-nif

<div align="center">
<em>Pydantic validators for spanish identification codes: NIF, DNI and NIE.</em>
</div>


<div align="center">
<a href="https://github.com/haztecaso/spanish-nif/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/haztecaso/spanish-nif/actions/workflows/test.yml/badge.svg" alt="test badge" />
</a>
<a href="https://github.com/haztecaso/spanish-nif/blob/main/pyproject.toml">
<img src="https://img.shields.io/badge/python-3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue" alt="Supported Python versions"/>
</a>
<a href="https://pypi.org/project/spanish-nif/" target="_blank">
    <img src="https://img.shields.io/pypi/v/spanish-nif.svg" alt="PyPI version" />
</a>
</div>

[**Documentation**](https://haztecaso.github.io/spanish-nif)

---

> ⚠️ **AI-generated library:** This library may contain severe vulnerabilities
> and should not be trusted for critical workflows. Use at your own risk; it was
> produced with the Codex AI assistant.

This library turns Spanish identification numbers into first-class Python types.
Each class (`NIF`, `DNI`, `NIE`) subclasses `str`, validates its control letter on
construction, and plugs straight into [Pydantic](https://docs.pydantic.dev/) so you can drop it into your
data models without writing bespoke validators.

## Installation

- **pip**

  ```bash
  python -m pip install spanish-nif
  ```

- **uv**

  ```bash
  uv pip install spanish-nif
  ```

## Quick examples

```python
from spanish_nif import DNI, NIE, NIF

DNI("12345678Z")          # returns a validated DNI string
NIE.is_valid("X1234567L") # -> True
NIF("K0867756N").variant  # -> "legacy"
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
