# Número de Identificación Fiscal (NIF) {: .no-toc }

## Overview
The NIF is the umbrella identifier for natural persons in Spain. In practice it
accepts three historical variants:

- Standard DNIs (eight digits plus the control letter).
- NIEs for foreign residents (prefix `X`/`Y`/`Z` plus seven digits and the control letter).
- Legacy cards with prefixes `K`, `L`, or `M`.

## Algorithm Walkthrough
1. **Canonicalise** by uppercasing the input; values must already include only significant characters.
2. **Reject empties** – a missing identifier is invalid.
3. **Attempt NIE validation** if the prefix is `X`, `Y`, or `Z`. The NIE logic
   translates the prefix and reuses the DNI control-letter rules.
4. **Attempt DNI validation** for pure eight-digit numbers.
5. **Fallback to legacy prefixes** `K`, `L`, or `M`: treat the following seven
   digits as the numeric part, reuse the DNI control-letter mapping on that number, and verify
   the trailing letter.
6. **Fail** if none of the previous branches succeed.

## Worked Examples
- `12345678Z`: standard DNI branch, remainder `14` → letter `Z`.
- `X1234567L`: NIE branch; control letter from numeric value `01234567`.
- `K0867756N`: legacy branch; digits `0867756`, remainder `13` → `N`.

## Formal Specification
- Input must be 9 ASCII characters after removing separators.
- Valid prefixes: digits `0-9`, legacy `KLM`, or NIE `XYZ`.
- Let `letters = "TRWAGMYFPDXBNJZSQVHLCKE"`.
- For NIE prefixes, set `n = int(prefix_map[prefix] + digits)`, where
  `prefix_map = {"X": "0", "Y": "1", "Z": "2"}`.
- For legacy prefixes, set `n = int(digits)` where `digits` are positions 2–8.
- For DNI-like values, set `n = int(first eight digits)`.
- Valid iff `letters[n % 23] == final_letter`.

## Using the Library
```python
from spanish_nif import NIF, InvalidNIF

nif = NIF("K0867756N")
assert nif.variant == "legacy"
assert nif.letter == "N"

if not NIF.is_valid("12345678A"):
    print("Control letter mismatch")
```

### Generating Sample NIFs

`NIF.random()` builds valid identifiers for tests and demos and lets you pin the
variant you need:

```python
from spanish_nif import NIF

some_nif = NIF.random()               # variant picked automatically
legacy_nif = NIF.random(variant="legacy")
assert legacy_nif[0] in {"K", "L", "M"}
```

Supply a `random.Random` instance if you need deterministic output (for example,
inside test suites).

## Official References

- [Real Decreto 1065/2007, de 27 de julio, por el que se aprueba el Reglamento General de las actuaciones y los procedimientos de gestión e inspección tributaria](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2007-15017) — el artículo 18 concreta la composición del número de identificación fiscal para personas físicas.
- [Orden EHA/451/2008, de 20 de febrero, por la que se regula el número de identificación fiscal](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2008-3580) — establece los códigos y caracteres de control para personas jurídicas y otros sujetos.
- [Agencia Tributaria: Número de identificación fiscal (NIF)](https://sede.agenciatributaria.gob.es/Sede/ayuda/normativas-criterios-interpretativos/normativa/no-tributaria/numero-identificacion-fiscal.html) — resumen oficial sobre la asignación y estructura del NIF según el tipo de contribuyente.
