# Usage Guide for Iran System Encoding

This guide provides detailed instructions on how to use the `iran-encoding` library effectively.

## Core API Functions

### `encode(text, visual_ordering=True)`
Converts a Unicode string to Iran System encoded bytes.

- **Parameters:**
    - `text` (str): Input Unicode string.
    - `visual_ordering` (bool): If True, applies reshaping and visual reversal.
- **Return:** `bytes`

### `decode(iransystem_bytes)`
Converts Iran System encoded bytes back to a Unicode string.

- **Parameters:**
    - `iransystem_bytes` (bytes): Input bytes.
- **Return:** `str`

### `detect_locale(text)`
Determines if text contains Persian characters.

- **Return:** `'fa'` or `'en'`

## Intelligent Behavior

### Mixed Language Strings
- If a string contains **at least one Persian letter**, the entire string is processed using the Iran System flow. Numbers within this string are converted to Iran System Persian digits.
- If a string contains **only English letters and numbers** (even Persian digits), it is processed using the English (ASCII) flow. Persian digits are normalized to ASCII 0-9.

## Performance Optimization
For high-volume processing, it is recommended to compile the C extension:
```bash
python3 build_c_extension.py
```
The library will automatically detect and use the compiled binary for encoding.
