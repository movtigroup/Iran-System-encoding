# -*- coding: utf-8 -*-

"""
This module provides encoding and decoding functionality for the Iran System
character set, including bidirectional text handling.
"""

import re
import unicodedata
from typing import List
import arabic_reshaper
from bidi.algorithm import get_display
from .mappings import IRAN_SYSTEM_MAP, REVERSE_IRAN_SYSTEM_MAP, UNKNOWN_CHAR_CODE

def encode(text: str, visual_ordering: bool = True) -> bytes:
    """
    Encodes a string into a sequence of bytes using the Iran System map.
    It handles text shaping and optional visual reordering for RTL text.

    Args:
        text: The input string to encode.
        visual_ordering: If True (default), produces a visually ordered output
            for simple LTR displays. If False, produces a logically ordered
            output for systems that support bidi.

    Returns:
        A bytes object representing the encoded string.
    """
    if not isinstance(text, str):
        return b''

    # Configure the reshaper
    configuration = {
        'support_ligatures': False,
    }
    reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)

    # Reshape the text to get correct presentation forms
    reshaped_text = reshaper.reshape(text)

    if visual_ordering:
        # This regex finds sequences of RTL characters (Arabic, Persian, etc.).
        rtl_char_pattern = re.compile(r'([\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+)')
        parts = rtl_char_pattern.split(reshaped_text)
        processed_parts = []
        for part in parts:
            if rtl_char_pattern.match(part):
                # This is an RTL segment, apply bidi
                # A bit of a hack for Persian numbers, which bidi.get_display doesn't seem to handle correctly.
                is_all_digits = all('\u06F0' <= c <= '\u06F9' for c in part)
                if is_all_digits:
                    visual_part = part[::-1]
                else:
                    visual_part = get_display(part, base_dir='R')
                processed_parts.append(visual_part)
            else:
                # This is an LTR segment, no change needed
                processed_parts.append(part)

        output_text = "".join(processed_parts)
    else:
        output_text = reshaped_text

    byte_codes = []
    for char in output_text:
        code = REVERSE_IRAN_SYSTEM_MAP.get(char, UNKNOWN_CHAR_CODE)
        byte_codes.append(code)

    return bytes(byte_codes)

def decode(data: bytes) -> str:
    """
    Decodes a byte string from the Iran System encoding back to a string.

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

    # The Iran System encoding is visual. To get a logical string, we need to
    # reverse the RTL segments.
    rtl_char_pattern = re.compile(r'([\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+)')
    parts = rtl_char_pattern.split(visual_text)
    logical_parts = []
    for part in parts:
        if rtl_char_pattern.match(part):
            logical_parts.append(part[::-1])
        else:
            logical_parts.append(part)

    logical_text = "".join(logical_parts)

    # Normalize presentation forms to base characters
    return unicodedata.normalize('NFKD', logical_text)

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
