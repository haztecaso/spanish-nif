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
