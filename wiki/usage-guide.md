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
- The library implements **Global RTL** reversal with local chunk correction.
- When encoding mixed text (e.g., `"hi سلام 123"`), the entire line is oriented for Right-To-Left display.
- **English words and Numbers** are automatically identified as LTR chunks and are un-reversed to maintain their internal logical order.
- This ensures that on a visual terminal, the text appears as: `123 سلام hi` (which is the correct RTL visual layout of the logical input).
- If a string contains **only ASCII characters**, it is processed using a standard logical flow to ensure compatibility with modern English text systems.

## Performance Optimization
For high-volume processing, it is recommended to compile the C extension:
```bash
python3 build_c_extension.py
```
The library will automatically detect and use the compiled binary for encoding.
