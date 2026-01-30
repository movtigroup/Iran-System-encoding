# Iran System Encoding

A Python package for encoding and decoding Persian text using the Iran System character set, with automatic locale detection and number handling based on language context.

## Features

- **Bidirectional Encoding/Decoding**: Convert between Unicode Persian text and Iran System encoding
- **Locale Detection**: Automatically detects if text is Persian (`fa`) or English (`en`) and handles numbers accordingly
- **Smart Number Handling**: Converts numbers to Persian numerals when locale is Persian, keeps ASCII numbers when locale is English
- **Pure Python Implementation**: Fully implemented in Python with no external dependencies (C extension support removed for simplicity)
- **Command-Line Interface**: Easy-to-use CLI for encoding/decoding operations
- **Accurate Algorithm**: Implements the exact same logic as the original C code for Iran System encoding

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Python API

```python
from iran_encoding import encode, decode, detect_locale

# Detect locale (fa/en)
locale = detect_locale("Hello world سلام")
print(locale)  # Output: 'fa' (since Persian characters are more dominant)

# Encode Persian text
text = "سلام 123"
encoded = encode(text)
print(encoded.hex())  # Iran System encoded bytes as hex

# Decode Iran System bytes
decoded = decode(encoded)
print(decoded)  # Output: "سلام ۱۲۳" (with Persian numbers)

# Encode with logical ordering (instead of visual)
encoded_logical = encode(text, visual_ordering=False)
```

### Command-Line Interface

```bash
# Encode text
iran-encoding encode "سلام دنیا"

# Decode hex string
iran-encoding decode-hex "a8 f3 91 f4"

# Decode byte string
iran-encoding decode "b'\\xa8\\xf3\\x91\\xf4'"
```

## Locale Detection

The package includes intelligent locale detection that determines whether the input text is primarily Persian (`fa`) or English (`en`). Based on this detection:

- **Persian locale (`fa`)**: Numbers are converted to Persian numerals (0123456789 → ۰۱۲۳۴۵۶۷۸۹)
- **English locale (`en`)**: Numbers remain as ASCII numerals

Example:
```python
from iran_encoding import encode

# Text with Persian locale - numbers become Persian
text_fa = "Hello سلام 123"
encoded_fa = encode(text_fa)
# Numbers '123' will be encoded as Persian numerals '۱۲۳'

# Text with English locale - numbers stay ASCII
text_en = "Only English text here 123"
encoded_en = encode(text_en)
# Numbers '123' will remain as ASCII
```

## Iran System Encoding

Iran System is a legacy Persian character encoding that predates Unicode. This package provides:

- Full character mapping for Persian text
- Support for Persian numbers (۰۱۲۳۴۵۶۷۸۹)
- Box drawing characters and other symbols
- Proper handling of joining and non-joining Arabic/Persian letters
- Implementation of the exact same algorithm as the original C code

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual tests:

```bash
python -m tests.test_converter
python -m tests.test_encoding_functions
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.