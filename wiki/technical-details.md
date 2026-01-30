# Technical Details: Iran System Implementation

The `iran-encoding` library is built as a bridge between modern Unicode systems and legacy visual-based Iran System character sets.

## Visual vs. Logical Ordering
Modern Unicode stores text in logical order (as it is read) and relies on the display engine to handle the right-to-left layout and character shaping.

**Iran System** (predating Unicode) stores characters in **visual order**. The byte code for a "Seen" (س) at the beginning of a word is different from a "Seen" at the end of a word.

## Porting the C Engine
The core of this library is a direct port of the logic from `iran_system.c`. This logic performs two main steps:
1. **Contextual Reshaping**: It looks at the surrounding bytes to choose the correct visual form (initial, medial, final, isolated).
2. **BiDi Handling**: It uses an algorithm similar to `ReverseAlphaNumeric` to ensure that numbers and English words embedded in Persian text are stored in a way that displays correctly on simple visual terminals.

## Data Structures
The mapping tables in `iran_encoding/core.py` (like `UNICODE_STR`, `IRANSYSTEM_UPPER_STR`, etc.) are byte-for-byte identical to the original implementation. This ensures parity when interacting with legacy databases that were written using the original C software.
