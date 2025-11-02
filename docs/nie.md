# Número de Identidad de Extranjero (NIE) {: .no-toc }

## Overview
The NIE identifies foreign residents. It resembles the DNI but starts with a
prefix letter `X`, `Y`, or `Z`, followed by seven digits and the familiar
control letter. Each prefix maps to a digit so that NIEs share the same
control-letter logic as DNIs.

## Algorithm Walkthrough
1. **Canonicalise** by uppercasing the value; inputs must already be the correct length without separators.
2. **Format check** against the regular expression ``[XYZ]\d{7}[A-Z]``.
3. **Translate the prefix** to a digit using `{"X": "0", "Y": "1", "Z": "2"}` and
   concatenate it with the seven digits to create an eight-digit number.
4. **Compute the remainder** of that number divided by 23.
5. **Map to the control letter** using the same `TRWAGMYFPDXBNJZSQVHLCKE` sequence
   used for DNIs.
6. **Validate** that the calculated letter matches the provided letter.

## Worked Examples
- `X1234567L`: prefix `X` → `0`, number `01234567`, remainder `11`, expected
  letter `L`.
- `Y1234567X`: prefix `Y` → `1`, number `11234567`, remainder `21`, expected
  letter `X`.
- `Z1234567R`: prefix `Z` → `2`, number `21234567`, remainder `18`, expected
  letter `R`.

## Formal Specification
- Input must be exactly 9 ASCII characters.
- Character 1: `X`, `Y`, or `Z`.
- Characters 2–8: digits `0-9`.
- Character 9: uppercase letter `A-Z`.
- Let `prefix_map = {"X": "0", "Y": "1", "Z": "2"}`.
- Let `n = int(prefix_map[char1] + chars2to8)`.
- Let `letters = "TRWAGMYFPDXBNJZSQVHLCKE"`.
- Valid iff `letters[n % 23] == character9`.

## Using the Library
```python
from spanish_nif import NIE, InvalidNIE

nie = NIE("X1234567L")
assert nie.prefix == "X"
assert nie.number == 1234567  # numeric value used for the control-letter calculation

if not NIE.is_valid("x1234567l"):  # uppercased internally, so this returns True
    raise RuntimeError("Unexpected validation failure")
```
