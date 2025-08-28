# Iran System Encoding
[![Python package CI](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/ci.yml)[![Python Package using Conda](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/movtigroup/Iran-System-encoding/actions/workflows/python-package-conda.yml)

A Python package for encoding and decoding text using the Iran System character set, designed for environments like NDS Station Displays.

This library provides a direct mapping from Unicode characters to the custom Iran System byte representation. It includes robust support for both English (LTR) and Persian (RTL) text, automatically handling the complexities of bidirectional text display.

## Key Features

- **Direct Encoding**: A single-stage mapping from Unicode to the Iran System character set.
- **Bidirectional Text Support**: Automatically detects and reverses Right-to-Left (Persian) text segments for correct logical-to-visual ordering, while leaving Left-to-Right (English) segments untouched.
- **Full ASCII and Persian Support**: The character map includes standard ASCII, Persian letters, and Persian digits.
- **Fallback for Unknown Characters**: Gracefully handles characters not in the map by replacing them with a `'?'`.
- **Command-Line Interface**: Includes a CLI tool for easy encoding and decoding from the terminal.

## Installation

To install the package directly from GitHub:

```bash
pip install git+https://github.com/movtigroup/Iran-System-encoding.git
```

## Library Usage

The library provides simple `encode()` and `decode()` functions.

### Example 1: Pure Persian (RTL)

```python
from iran_encoding import encode, decode

text = "سلام دنیا"
encoded = encode(text)
print(f"Original: {text}")
print(f"Encoded: {encoded.hex()}")

decoded = decode(encoded)
print(f"Decoded: {decoded}")
# Correctly prints: سلام دنیا
```

### Example 2: Pure English (LTR)

```python
from iran_encoding import encode, decode

text = "Hello, World!"
encoded = encode(text)
print(f"\nOriginal: {text}")
print(f"Encoded: {encoded.hex()}")

decoded = decode(encoded)
print(f"Decoded: {decoded}")
# Correctly prints: Hello, World!
```

### Example 3: Mixed Bidirectional Text

The library automatically handles the ordering of text segments.

```python
from iran_encoding import encode, decode

text = "Final ETA: ۱۰ دقیقه"
encoded = encode(text)
print(f"\nOriginal: {text}")
print(f"Encoded: {encoded.hex()}")

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
This will print the raw encoded bytes to standard output.

### `decode`

The `decode` command requires the input to be a Python bytes literal string.

```bash
iran-encoding decode "b'\\x54\\x65\\x73\\x74\\x3a\\x20\\x91\\x9d\\x8f'"
```
This will print the decoded string: `Test: تست`

**Note**: You need to wrap the byte string in quotes (`" "`) and prefix it with `b''` to ensure it is correctly parsed by the command line.
