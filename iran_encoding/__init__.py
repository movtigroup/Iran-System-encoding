# -*- coding: utf-8 -*-

"""
This module provides encoding and decoding functionality for the Iran System
character set, including bidirectional text handling.
"""

import re
from typing import List
from .mappings import IRAN_SYSTEM_MAP, REVERSE_IRAN_SYSTEM_MAP, UNKNOWN_CHAR_CODE

# This regex finds sequences of RTL characters (Arabic, Persian, etc.).
# The pattern is non-capturing so that split() returns the delimiters as well.
RTL_CHAR_PATTERN = re.compile(r'([\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+)')

def _process_bidi(text: str, reverse_rtl: bool) -> str:
    """Helper function to handle bidirectional text segments."""
    parts = RTL_CHAR_PATTERN.split(text)
    processed_parts = []
    for part in parts:
        if RTL_CHAR_PATTERN.match(part):
            # This is an RTL segment
            if reverse_rtl:
                processed_parts.append(part[::-1])
            else:
                processed_parts.append(part)
        else:
            # This is an LTR segment
            processed_parts.append(part)
    return "".join(processed_parts)

def encode(text: str) -> bytes:
    """
    Encodes a string into a sequence of bytes using the Iran System map.
    It handles bidirectional text by reversing segments of RTL characters.

    Args:
        text: The input string to encode.

    Returns:
        A bytes object representing the encoded string.
    """
    if not isinstance(text, str):
        return b''

    # Reverse RTL segments for logical-to-visual conversion
    visual_text = _process_bidi(text, reverse_rtl=True)

    byte_codes = []
    for char in visual_text:
        code = REVERSE_IRAN_SYSTEM_MAP.get(char, UNKNOWN_CHAR_CODE)
        byte_codes.append(code)

    return bytes(byte_codes)

def decode(data: bytes) -> str:
    """
    Decodes a byte string from the Iran System encoding back to a string.
    It handles bidirectional text by reordering the decoded RTL segments.

    Args:
        data: The input bytes to decode.

    Returns:
        The decoded string.
    """
    if not isinstance(data, bytes):
        return ''

    # First, decode the bytes to a "visual" string
    visual_chars: List[str] = []
    for byte in data:
        char = IRAN_SYSTEM_MAP.get(byte, '�')  # Use Unicode replacement char for unknown bytes
        visual_chars.append(char)

    visual_text = "".join(visual_chars)

    # Reverse RTL segments for visual-to-logical conversion
    logical_text = _process_bidi(visual_text, reverse_rtl=True)

    return logical_text

def decode_hex(hex_string: str) -> str:
    """
    Decodes a hex string into a UTF-8 string using the Iran System map.

    Args:
        hex_string: The input hex string to decode.

    Returns:
        The decoded string.
    """
    try:
        data = bytes.fromhex(hex_string)
        return decode(data)
    except (ValueError, TypeError):
        return "Error: Invalid hex string"
