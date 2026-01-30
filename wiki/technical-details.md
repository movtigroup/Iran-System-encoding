# Technical Details of Iran System Encoding

## Overview

Iran System is a legacy character encoding for Persian/Farsi text that predates Unicode adoption in Iran. Unlike Unicode, Iran System uses visual ordering of characters rather than logical ordering, which means characters are stored in the order they appear visually rather than in the order they are typed.

## Character Mapping

The Iran System character set maps 256 possible byte values to various characters:

- **0x00-0x7F**: Standard ASCII characters
- **0x80-0x8F**: Persian numbers ۰۱۲۳۴۵۶۷۸۹ and punctuation
- **0x90-0xAF**: Persian letters in different joining forms
- **0xB0-0xDF**: Box-drawing characters
- **0xE0-0xFF**: Additional Persian letters and symbols

## Joining Behavior

Unlike logical encodings, Iran System requires careful handling of joining behavior:

- **Dual Joining Characters**: Characters that join both left and right (most Persian consonants)
- **Right Joining Characters**: Characters that join only to the previous character (alef, dal, etc.)
- **Non-Joining Characters**: Characters that don't join (hamza, etc.)

## Zero Width Non-Joiner (ZWNJ)

The Iran System encoding handles joining behavior differently than Unicode. In some contexts, a ZWNJ character (\u200C) is needed to prevent unwanted joining.

## Implementation Algorithm

Our implementation replicates the exact algorithm from the original C code:

1. **Context Analysis**: Examines previous and next characters to determine correct visual form
2. **Form Selection**: Chooses between isolated, initial, medial, and final forms based on context
3. **Character Mapping**: Maps Unicode characters to Iran System byte values using the same tables as the C implementation

## Number Handling in Different Locales

Our implementation provides locale-aware number handling:

- When locale is detected as Persian (fa), Arabic numerals are converted to Persian numerals
- When locale is detected as English (en), numerals remain as ASCII
- The detection algorithm analyzes character frequency to determine primary language

## API Reference

### Functions

#### `encode(text, visual_ordering=True, configuration=None)`
Converts Unicode text to Iran System encoded bytes.

Parameters:
- `text`: Unicode string to encode
- `visual_ordering`: Whether to apply visual ordering transformations
- `configuration`: Additional configuration for text reshaping

Returns: `bytes` - Iran System encoded bytes

#### `decode(iransystem_bytes)`
Converts Iran System encoded bytes to Unicode text.

Parameters:
- `iransystem_bytes`: Iran System encoded bytes

Returns: `str` - Decoded Unicode string

#### `decode_hex(hex_string)`
Converts hex string representation of Iran System bytes to Unicode text.

Parameters:
- `hex_string`: Hex string (with or without spaces)

Returns: `str` - Decoded Unicode string

#### `detect_locale(text)`
Detects if text is primarily Persian (fa) or English (en).

Parameters:
- `text`: Input text to analyze

Returns: `str` - 'fa' if Persian dominant, 'en' if English dominant