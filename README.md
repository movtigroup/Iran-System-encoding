# Iran-Encoding

A Python package to provide two-stage encoding and decoding for Persian text.

This package maps Unicode Persian characters to Windows-1256 and then to a custom "Iran System" byte representation. It also provides a command-line interface for encoding and decoding.

## Installation

```bash
pip install .
```

## Usage

### Library

```python
from iran_encoding import encode, decode

encoded = encode("سلام")
print(encoded)

decoded = decode(encoded)
print(decoded)
```

### Command-Line Interface

```bash
iran-encoding encode "سلام"
iran-encoding decode "b'\\x9b\\x93\\x8d\\x9c'"
```
