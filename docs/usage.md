# Usage Guide

This guide explains how to use the `iran-encoding` library for common tasks.

## Installation

Install the library using pip:

```bash
pip install iran-encoding
```

## Basic Encoding and Decoding

To encode or decode text, create an instance of the `IranSystemEncoder` class and call its methods.

```python
from iran_encoding import IranSystemEncoder

# Create an encoder instance
encoder = IranSystemEncoder()

# Encode a string
text = "سلام دنیا"
encoded_bytes = encoder.encode(text)
print(f"Encoded: {encoded_bytes.hex()}")

# Decode the bytes
decoded_text = encoder.decode(encoded_bytes)
print(f"Decoded: {decoded_text}")
```

## Advanced Options

You can configure the encoder with several options during initialization:

- `visual_ordering` (bool): Set to `False` to get a logical (non-visual) representation.
- `fallback_char` (str): Provide a character to use for any symbols not found in the encoding map. If not set, an `EncodingError` will be raised for unsupported characters.
- `cache_enabled` (bool): Enable caching for improved performance on repetitive tasks.

```python
encoder = IranSystemEncoder(
    visual_ordering=False,
    fallback_char='?',
    cache_enabled=True
)
```
