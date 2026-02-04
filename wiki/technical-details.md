# Technical Details: Iran System Implementation

The `iran-encoding` library is built as a bridge between modern Unicode systems and legacy visual-based Iran System character sets.

## Visual vs. Logical Ordering
Modern Unicode stores text in logical order (as it is read) and relies on the display engine to handle the right-to-left layout and character shaping.

**Iran System** (predating Unicode) stores characters in **visual order**. The byte code for a "Seen" (س) at the beginning of a word is different from a "Seen" at the end of a word.

## Porting the C Engine
The core of this library is a direct port of the logic from `iran_system.c`. This logic performs two main steps:
1. **Contextual Reshaping**: It looks at the surrounding bytes to choose the correct visual form (initial, medial, final, isolated).
2. **BiDi Handling**: It uses a refined **In-place Persian reversal** algorithm to ensure that numbers and English words embedded in Persian text remain Left-To-Right (LTR) while Persian letters are correctly reversed for visual display.

## Dual Implementation (Python & C)
The library provides two engines for processing:
1. **Pure Python Core**: A clean, zero-dependency implementation in `iran_encoding/core.py` that ensures compatibility across all Python environments (including PyPy and WASM).
2. **C Extension**: A high-performance version in `iran_encoding/iran_system.c` that can be compiled for maximum throughput in production environments. Both engines are tested for 100% parity.

## Data Structures
The mapping tables in `iran_encoding/core.py` (like `UNICODE_STR`, `IRANSYSTEM_UPPER_STR`, etc.) are byte-for-byte identical to the original legacy implementation, ensuring flawless integration with historical data.
