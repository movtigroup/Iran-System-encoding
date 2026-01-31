# Iran System Encoding Library for Python

[![PyPI version](https://img.shields.io/pypi/v/iran-encoding.svg)](https://pypi.org/project/iran-encoding/)
[![Python versions](https://img.shields.io/pypi/pyversions/iran-encoding.svg)](https://pypi.org/project/iran-encoding/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, professional library for converting between Unicode and the legacy **Iran System** visual encoding.

## ✨ Features

- **🚀 Dual Core Engine**: Fast C extension with a 100% pure Python fallback.
- **📦 Zero Dependencies**: No external libraries required (`arabic_reshaper` and `python-bidi` are now built-in).
- **🧠 Smart Visual RTL**: Advanced context-aware engine that handles mixed Persian and English text correctly.
- **🔢 Number Reversal**: Support for visual number reversal (e.g., "10" becoming "01" in the byte stream) as required by legacy systems.
- **🛡️ Industrial Grade**: Full support for all Persian characters, ligatures (Lam-Alef), and visual forms.

## 📥 Installation

```bash
pip install iran-encoding
```

## 🚀 Quick Start

```python
from iran_encoding import encode, decode

# Unicode to Iran System (Visual RTL)
text = "سلام 123"
encoded = encode(text)
print(encoded.hex())  # Output: 81828320f491f3a8

# Iran System to Unicode
decoded = decode(encoded)
print(decoded)  # Output: سلام ۱۲۳
```

## 📖 Advanced Usage

### Smart Global RTL
The library uses a "Smart Global RTL" strategy. It reverses the entire line for visual display but detects English words and numbers, keeping them in their correct LTR order within the visual stream.

### Persian vs English Digits
- **English Digits** (`0-9`): Kept in LTR order (e.g., "123" stays "123").
- **Persian Digits** (`۰-۹`): Visually reversed per legacy terminal requirements (e.g., "۱۰" becomes "۰۱").

## 🛠️ Performance
For heavy workloads, the library automatically uses a compiled C extension. If GCC is not available during installation, it seamlessly falls back to the optimized Python implementation.

## 📄 License
MIT License. Created and maintained for the Iranian developer community.
