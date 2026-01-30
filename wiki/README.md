# Iran System Encoding Library Documentation

## Introduction

The Iran System Encoding Library is a Python library designed for encoding and decoding Persian text using the Iran System standard. This library implements the exact same algorithm as the original C code for maximum accuracy, providing proper handling of visual forms and bidirectional text layout for Persian text.

## Features

- **Advanced Persian Text Reshaping**: Properly handles different visual forms of Persian letters (initial, medial, final, and isolated).
- **Bidirectional Text Support**: Enables correct mixing of Persian (right-to-left) and English (left-to-right) text.
- **Round-trip Conversion**: Provides reliable conversion between Unicode and Iran System encoding using the exact same algorithm as the C implementation.
- **CLI Support**: Includes command-line interface for direct terminal usage.
- **Locale Detection**: Automatically detects if text is Persian (fa) or English (en) and handles numbers accordingly.
- **Smart Number Handling**: Converts numbers to Persian numerals when locale is Persian, keeps ASCII numerals when locale is English.
- **Pure Python Implementation**: Fully implemented in Python with no external dependencies.

## Installation

Install via pip:

```bash
pip install iran-encoding
```

## Usage

### Encoding Text

```python
from iran_encoding import encode, decode, detect_locale

# Encode Persian text
text = "Hello سلام 123"
encoded = encode(text)
print(f"Encoded: {encoded.hex()}")

# Decode back
decoded = decode(encoded)
print(f"Decoded: {decoded}")  # Will show Persian numbers if text is detected as Persian

# Detect locale
locale = detect_locale(text)
print(f"Detected locale: {locale}")  # 'fa' if Persian dominant, 'en' if English dominant
```

### Command-Line Interface

Encoding:
```bash
iran-encoding encode "سلام دنیا"
```

Decoding:
```bash
iran-encoding decode "b'\\x91\\x9d\\x8f'"
```

Hex decoding:
```bash
iran-encoding decode-hex 919d8f
```

## Iran System Encoding

Iran System encoding is a proprietary standard for displaying Persian text in systems that don't support Arabic script. This encoding solves the problems of correct letter form display and bidirectional layout using the exact same algorithm as the original C implementation.

### Technical Details

The Iran System character set includes:
- Standard ASCII characters (0x00-0x7F)
- Persian numbers (0x80-0x89) mapped to Persian digits ۰۱۲۳۴۵۶۷۸۹
- Persian letters in different visual forms
- Box-drawing characters and symbols

## Locale Detection and Number Handling

The library includes intelligent locale detection that determines whether input text is primarily Persian (fa) or English (en):

- **Persian locale (fa)**: Numbers are converted to Persian numerals (0123456789 → ۰۱۲۳۴۵۶۷۸۹)
- **English locale (en)**: Numbers remain as ASCII numerals

## Development

For local development:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest tests/`

## Contribution

Contributions to improve this library are highly welcomed.