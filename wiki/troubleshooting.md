# Troubleshooting Guide

Common issues and solutions for working with the Iran System encoding.

## 1. Characters look reversed
**Symptoms:** Decoded text looks like "م‌ا‌ل‌س" instead of "سلام".
**Cause:** The source data was encoded without `visual_ordering`. Or, you are viewing encoded text in a terminal that doesn't support Iran System visual display.
**Solution:** Check the `visual_ordering` parameter during `encode`.

## 2. Numbers are not converting
**Symptoms:** In a Persian string, numbers stay as 123 instead of Iran System Persian digits.
**Cause:** The string might not contain any Persian letters, triggering the English locale flow.
**Solution:** Ensure the string contains at least one Persian letter if you want full Persian processing.

## 3. C Extension build fails
**Symptoms:** `python3 build_c_extension.py` results in errors.
**Cause:** Missing `gcc` or `clang` compiler.
**Solution:** Install a C compiler. On Ubuntu: `sudo apt install build-essential`. On Windows: Install MinGW or Visual Studio C++ build tools. Note that the library will still work using the pure Python fallback.
