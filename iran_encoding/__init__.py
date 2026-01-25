# -*- coding: utf-8 -*-
"""
This module provides encoding and decoding functionality for the Iran System
character set, including bidirectional text handling.
"""
from .converter import convert_iransystem_to_unicode, IRANSYSTEM_MAP, UNICODE_JOIN_PROPS, ZWNJ
from .mappings import UNKNOWN_CHAR_CODE

# Create a reverse map for encoding
REVERSE_IRAN_SYSTEM_MAP = {}
for code, value in IRANSYSTEM_MAP.items():
    if isinstance(value, tuple):
        char, form = value
        # Ensure the key is a tuple of (character, form)
        REVERSE_IRAN_SYSTEM_MAP[(char, form)] = code

def encode(text: str) -> bytes:
    """
    Encodes a logical Unicode string into a sequence of IranSystem bytes.
    This function is the inverse of decode, ensuring that decode(encode(text)) == text.
    """
    if not isinstance(text, str):
        return b''

    byte_codes = []
    i = 0
    while i < len(text):
        char = text[i]

        if char == ZWNJ:
            i += 1
            continue

        # --- Ligature check: Lookahead for 'لا' ---
        if char == 'ل' and i + 1 < len(text) and text[i + 1] == 'ا':
            # The 'laa' ligature is always final/isolated in this encoding
            code = REVERSE_IRAN_SYSTEM_MAP.get(('لا', 'final'))
            if code is not None:
                byte_codes.append(code)
                i += 2  # Consumed both 'ل' and 'ا'
                continue

        # --- Determine Joining Properties ---
        def joins_forward(c):
            """Check if a character joins with the next one."""
            prop = UNICODE_JOIN_PROPS.get(c)
            return prop == 'dual'

        def joins_backward(c):
            """Check if a character joins with the previous one."""
            prop = UNICODE_JOIN_PROPS.get(c)
            return prop in ('dual', 'right')

        # Determine connectivity based on context
        connects_to_prev = False
        if i > 0 and text[i - 1] != ZWNJ:
            prev_char = text[i - 1]
            if joins_forward(prev_char) and joins_backward(char):
                connects_to_prev = True

        connects_to_next = False
        if i + 1 < len(text) and text[i + 1] != ZWNJ:
            next_char = text[i + 1]
            if joins_forward(char) and joins_backward(next_char):
                connects_to_next = True

        # --- Determine Form ---
        if connects_to_prev and connects_to_next:
            form = "medial"
        elif connects_to_prev:
            form = "final"
        elif connects_to_next:
            form = "initial"
        else:
            form = "isolated"

        # --- Find Code with intelligent fallbacks ---
        code = REVERSE_IRAN_SYSTEM_MAP.get((char, form))

        if code is None:
            # If a specific form isn't found, try a visually similar one.
            # Medial forms often resemble initial forms.
            if form == "medial":
                code = REVERSE_IRAN_SYSTEM_MAP.get((char, "initial"))
            # Isolated forms often resemble final forms.
            elif form == "isolated":
                code = REVERSE_IRAN_SYSTEM_MAP.get((char, "final"))

        if code is None:
            # As a general fallback for any connecting form, try the isolated shape.
            if form in ["medial", "initial", "final"]:
                code = REVERSE_IRAN_SYSTEM_MAP.get((char, "isolated"))

        if code is None:
            # Fallback for non-Arabic characters like numbers and punctuation.
            code = REVERSE_IRAN_SYSTEM_MAP.get((char, "neutral"))

        if code is None:
            # If all else fails, use the unknown character code.
            code = UNKNOWN_CHAR_CODE

        byte_codes.append(code)
        i += 1

    return bytes(byte_codes)

def decode(data: bytes) -> str:
    """
    Decodes a byte string from the Iran System encoding back to a logical string.
    """
    return convert_iransystem_to_unicode(data)

def decode_hex(hex_string: str) -> str:
    """
    Decodes a hex string into a UTF-8 string using the Iran System map.
    """
    try:
        data = bytes.fromhex(hex_string)
        return decode(data)
    except (ValueError, TypeError):
        return "Error: Invalid hex string"
