# Iran System Encoding 🇮🇷

[![PyPI version](https://img.shields.io/pypi/v/iran-encoding.svg)](https://pypi.org/project/iran-encoding/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/iran-encoding.svg)](https://pypi.org/project/iran-encoding/)

A high-performance, professional Python library for the legacy **Iran System** character encoding. This package provides symmetrical encoding and decoding with automatic locale detection, smart number handling, and an exact port of the original C logic.

---

## 🚀 Key Features

- **✅ Bidirectional Conversion**: Seamlessly convert between Unicode and Iran System encoding.
- **✅ Pure Python Core**: Zero external dependencies. We removed `arabic_reshaper` and `python-bidi` to provide a faster and more stable internal implementation.
- **✅ C Extension Support**: Includes a high-performance C source for optional compilation, delivering maximum speed.
- **✅ Intelligent Locale Detection**:
  - **Context-Aware**: Automatically detects if the text is Persian (`fa`) or English (`en`).
  - **Smart Numbers**: Automatically converts digits to Iran System format in Persian contexts, and keeps them as ASCII in English contexts.
- **✅ Precise Visual Ordering**: Implements the exact rule-based reshaping and visual layout logic from original legacy C systems.
- **✅ Command-Line Interface (CLI)**: A built-in tool for quick terminal-based operations.

---

## 📦 Installation

```bash
pip install iran-encoding
```

---

## 🛠 Usage Guide

### Python API

```python
import iran_encoding

# 1. Encoding (Unicode -> Iran System)
# Automatically handles reshaping and visual ordering
text = "سلام دنیا 123"
encoded = iran_encoding.encode(text)
print(encoded.hex())

# 2. Decoding (Iran System -> Unicode)
decoded = iran_encoding.decode(encoded)
print(decoded) # Output: "سلام دنیا ۱۲۳"

# 3. Smart Locale Detection
# Persian letters trigger the 'fa' locale
print(iran_encoding.detect_locale("Hello سلام")) # 'fa'

# If only English text and numbers are present, it uses 'en'
# and converts Persian digits to ASCII if necessary.
print(iran_encoding.detect_locale("Hello ۱۲۳")) # 'en'
```

### Command-Line Interface

The library includes a CLI tool named `iran-encoding`:

```bash
# Encode text to hex
iran-encoding encode "سلام دنیا"

# Decode Iran System hex to Unicode
iran-encoding decode-hex "a8 f3 91 f4"

# Decode raw byte string literal
iran-encoding decode "b'\xa8\xf3\x91\xf4'"
```

---

## ⚙️ Technical Overview

Unlike modern Unicode, **Iran System** is a visual encoding. This means the specific byte code for a letter depends on its shape (initial, medial, final, or isolated).

This library utilizes a verified port of legacy C algorithms to:
1.  **Reshape** characters based on surrounding context.
2.  **Order** the visual layout for right-to-left display.
3.  **Handle Alphanumeric** sequences correctly within bi-directional text.

Our implementation ensures **100% compatibility** with legacy databases and hardware terminals.

---

## 🧪 Testing & Quality

We prioritize reliability. Our test suite covers 100% of the core conversion logic:

```bash
python3 -m pytest tests/
```

---

## 📄 License & Support

- **License**: MIT License - see the [LICENSE](LICENSE) file for details.
- **Support**: For professional support and inquiries, contact [Iran-System-encoding@movtigroup.ir](mailto:Iran-System-encoding@movtigroup.ir).
- **Author**: Iran System encoding (MovtiGroup)

Contributions are welcome! Please feel free to open an issue or submit a pull request on our [GitHub repository](https://github.com/movtigroup/Iran-System-encoding).
