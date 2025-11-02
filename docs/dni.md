# Documento Nacional de Identidad (DNI) {: .no-toc }

## Overview
The Spanish DNI is the standard identification number for Spanish citizens. It
is eight digits plus a control letter. The letter guards against typos by
encoding the remainder of the numeric part modulo 23.

## Algorithm Walkthrough
1. **Canonicalise** the input by uppercasing it; values must already be the correct length and contain no separators.
2. **Format check** that the result matches ``\d{8}[A-Z]``.
3. **Compute the remainder** of the eight-digit number divided by 23.
4. **Map the remainder** to the fixed sequence ``TRWAGMYFPDXBNJZSQVHLCKE``.
5. **Compare** the expected letter with the provided one. A mismatch means the
   identifier is invalid.

## Worked Examples
- `12345678Z`: `12345678 % 23 == 14`, and the sequence at position 14 is `Z`.
- `00000000T`: the remainder is 0, yielding the first letter `T`.
- `12345678A`: remainder 14 → `Z`, so the provided `A` is rejected.

## Formal Specification
- Input must be exactly 9 ASCII characters.
- Characters 1–8: digits `0-9`.
- Character 9: uppercase letter `A-Z`.
- Let `n` be the integer formed by the first eight digits.
- Let `letters = "TRWAGMYFPDXBNJZSQVHLCKE"`.
- Valid if and only if `letters[n % 23] == character9`.

## Using the Library
```python
from spanish_nif import DNI, InvalidDNI

dni = DNI("12345678Z")
assert dni.digits == "12345678"
assert dni.letter == "Z"

try:
    DNI("12345678A")
except InvalidDNI as error:
    print(error)
```

## Official References

- [Real Decreto 1553/2005, de 23 de diciembre, por el que se regula la expedición del Documento Nacional de Identidad](https://www.boe.es/eli/es/rd/2005/12/23/1553/con) — el artículo 11 fija que el DNI incorpora el número del NIF como ocho dígitos más la letra de control.
