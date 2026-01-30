# Iran System Encoding

[![Python package CI](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/ci.yml)[![Python Package using Conda](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/python-package-conda.yml)
[![Qodana Scan](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/qodana-ci.yml/badge.svg)](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/qodana-ci.yml)
[![Publish Python Package to PyPI](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/publish-to-pypi.yml)

A Python package for encoding and decoding text using the Iran System character set, designed for environments that require visually correct Persian text but lack native support for Arabic script rendering.

This library provides robust two-way conversion between Unicode and the Iran System character set. It correctly handles the complexities of Persian text, including text shaping and bidirectional layout.

## Key Features

- **Accurate Text Shaping**: Utilizes the `arabic_reshaper` library to correctly shape Persian text, ensuring that characters take on their correct contextual forms (initial, medial, final, isolated).
- **Bidirectional Text Support**: Leverages the `python-bidi` library to handle the Unicode Bidirectional Algorithm, ensuring correct visual ordering of right-to-left (Persian) and left-to-right (English) text segments.
- **Comprehensive Character Set**: The character map is based on the Iran System standard and includes a wide range of presentation forms for Persian letters, as well as standard ASCII and Persian digits.
- **Fallback for Unknown Characters**: Gracefully handles characters not in the map by replacing them with a `'?'`.
- **Command-Line Interface**: Includes a CLI tool for easy encoding and decoding from the terminal.

## Installation

To install the package from PyPI:

```bash
pip install iran-encoding
```

This will also install the necessary dependencies: `arabic_reshaper` and `python-bidi`.

## Library Usage

The library provides simple `encode()` and `decode()` functions.

### Example 1: Encoding Persian Text

The `encode` function takes a logical string (like what you would type) and returns the byte representation in the Iran System encoding. By default, it produces a *visually ordered* output suitable for simple LTR displays.

You can control this behavior with the `visual_ordering` parameter:
- `encode(text, visual_ordering=True)` (default): Returns a visually ordered string.
- `encode(text, visual_ordering=False)`: Returns a logically ordered string (for systems that handle bidi).

```python
from iran_encoding import encode, decode

text = "سلام دنیا"
encoded = encode(text)
print(f"Original: {text}")
print(f"Encoded (hex): {encoded.hex()}")

# The decoded text will be the same as the original logical string.
decoded = decode(encoded)
print(f"Decoded: {decoded}")
# Correctly prints: سلام دنیا
```
The `encoded` bytes represent the visually correct string, with letters shaped and ordered correctly for display in a simple left-to-right environment.

### Example 2: Mixed Bidirectional Text

The library automatically handles the ordering of mixed English and Persian text.

```python
from iran_encoding import encode, decode

text = "Final ETA: ۱۰ دقیقه"
encoded = encode(text)
print(f"\nOriginal: {text}")
print(f"Encoded (hex): {encoded.hex()}")

decoded = decode(encoded)
print(f"Decoded: {decoded}")
# Correctly prints: Final ETA: ۱۰ دقیقه
```

## Command-Line Interface

You can also use the package from the command line.

### `encode`

```bash
iran-encoding encode "Test: تست"
```
This will print a space-separated hex string of the encoded text in visual order.

To get the output in logical order, use the `--logical` flag:
```bash
iran-encoding encode "Test: تست" --logical
```

### `decode`

The `decode` command requires the input to be a Python bytes literal string.

```bash
iran-encoding decode "b'\\x54\\x65\\x73\\x74\\x3a\\x20\\x91\\x9d\\x8f'"
```
This will print the decoded string: `Test: تست`

**Note**: You need to wrap the byte string in quotes (`" "`) and prefix it with `b''` to ensure it is correctly parsed by the command line.

### `decode-hex`

The `decode-hex` command decodes a string of hexadecimal characters into text.

```bash
iran-encoding decode-hex 546573743a20919d8f
```
This will print the decoded string: `Test: تست`
