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
- The library uses a sophisticated **in-place reversal** logic for mixed text.
- **English and Numbers** remain in their logical Left-To-Right (LTR) order even when part of a Persian sequence.
- **Persian letters and symbols** are correctly reversed for visual display.
- This ensures that a string like `"hi سلام 123"` results in a byte stream that displays correctly on visual terminals.
- If a string contains **only English letters and numbers**, it is processed using the English (ASCII) flow for maximum compatibility.

## Performance Optimization
For high-volume processing, it is recommended to compile the C extension:
```bash
python3 build_c_extension.py
```
The library will automatically detect and use the compiled binary for encoding.
