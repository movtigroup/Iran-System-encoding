# Iran System Encoding 🇮🇷

[![PyPI version](https://img.shields.io/pypi/v/iran-encoding.svg)](https://pypi.org/project/iran-encoding/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/iran-encoding.svg)](https://pypi.org/project/iran-encoding/)

A high-performance, professional Python library for the legacy **Iran System** character encoding. This package provides symmetrical encoding and decoding with automatic locale detection, smart number handling, and an exact port of the original C logic.

## 🚀 Features

- **Bidirectional Conversion**: Seamlessly convert between Unicode and Iran System encoding.
- **Pure Python Core**: Zero external dependencies (removed `arabic_reshaper` and `python-bidi` for better performance and reliability).
- **C Extension Support**: Includes a high-performance C implementation for critical processing tasks.
- **Intelligent Locale Detection**:
  - Automatically detects Persian (`fa`) vs. English (`en`) context.
  - Smart Number Handling: Numbers are automatically converted to Iran System format in Persian context, and to ASCII in English context.
- **Visual Ordering**: Implements the exact rule-based reshaping and visual ordering logic from the original C implementation.
- **Command-Line Interface (CLI)**: Easy-to-use tool for quick encoding/decoding tasks.

## 📦 Installation

```bash
pip install iran-encoding
```

## 🛠 Usage

### Python API

```python
import iran_encoding

# 1. Encode Persian text (Unicode to Iran System)
# Automatically handles reshaping and visual ordering
text = "سلام دنیا 123"
encoded = iran_encoding.encode(text)
print(encoded.hex())

# 2. Decode Iran System bytes (Iran System to Unicode)
decoded = iran_encoding.decode(encoded)
print(decoded) # Output: "سلام دنیا ۱۲۳"

# 3. Locale Detection Logic
# If Persian letters are present, it uses Persian encoding
print(iran_encoding.detect_locale("Hello سلام")) # 'fa'

# If only English text and Persian numbers are present, it converts numbers to ASCII
# and uses English (ASCII) encoding.
print(iran_encoding.detect_locale("Hello ۱۲۳")) # 'en'
```

### Command-Line Interface

The library provides a CLI tool named `iran-encoding`:

```bash
# Encode Persian text to hex
iran-encoding encode "سلام دنیا"

# Decode Iran System hex to Unicode
iran-encoding decode-hex "a8 f3 91 f4"

# Decode raw byte string
iran-encoding decode "b'\xa8\xf3\x91\xf4'"
```

## ⚙️ How it Works

Unlike modern Unicode-based systems, **Iran System** is a visual encoding where the shape of a character (initial, medial, final, isolated) is determined at encoding time.

This library implements a sophisticated rule-based engine that:
1. Performs context-aware character reshaping.
2. Manages visual ordering (right-to-left layout).
3. Handles alphanumeric sequences correctly within Persian text.

The implementation is a direct, verified port of the legacy C algorithms used in original Iran System software, ensuring 100% compatibility with legacy database and hardware systems.

## 🧪 Testing

We maintain a comprehensive test suite with 100% coverage of core logic:

```bash
python3 -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Whether it's reporting a bug, improving documentation, or submitting a performance enhancement, please feel free to open an issue or pull request.
