"""
Iran System Encoding Package - Main Module

This package provides encoding and decoding functions for the Iran System character set.
It uses a pure Python implementation of the original C logic by default,
ensuring consistent behavior and professional results.
"""
import re
from .core import unicode_to_iransystem, iransystem_to_unicode

__version__ = "1.1.0"
__author__ = "Community Contributors"
__all__ = ['encode', 'decode', 'decode_hex', 'detect_locale']

# Persian letters range (approximate, covering main Persian alphabet)
PERSIAN_LETTERS_PATTERN = re.compile(r'[\u0621-\u064A\u067E\u0686\u0698\u06AF\u06A9\u06CC]')
PERSIAN_DIGITS_MAP = {
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
}

def detect_locale(text):
    """
    Detect if the text should be treated as Persian ('fa') or English ('en').
    
    Returns:
        str: 'fa' if text contains Persian letters, 'en' otherwise.
    """
    if PERSIAN_LETTERS_PATTERN.search(text):
        return 'fa'
    return 'en'

def encode(text, visual_ordering=True):
    """
    Encode a Unicode string to Iran System encoding bytes.
    
    Args:
        text (str): The Unicode string to encode.
        visual_ordering (bool): Whether to apply visual ordering (default True).
                               This follows the original C logic.
        
    Returns:
        bytes: Iran System encoded bytes or ASCII bytes depending on locale.
    """
    locale = detect_locale(text)
    
    if locale == 'fa':
        # Use the core Iran System logic
        return unicode_to_iransystem(text, reverse_flag=visual_ordering)
    else:
        # English/ASCII locale
        # Convert Persian digits to ASCII if present
        processed_text = text
        for p_digit, a_digit in PERSIAN_DIGITS_MAP.items():
            processed_text = processed_text.replace(p_digit, a_digit)

        return processed_text.encode('ascii', errors='replace')

def decode(iransystem_bytes):
    """
    Decode Iran System encoded bytes to a Unicode string.
    
    Args:
        iransystem_bytes (bytes): Iran System encoded bytes.
        
    Returns:
        str: Decoded Unicode string.
    """
    # If the bytes look like pure ASCII (all < 128) and we don't see typical Iran System markers,
    # it might just be ASCII. However, Iran System is a superset of ASCII for 0-127.
    # The core logic handles this correctly.
    return iransystem_to_unicode(iransystem_bytes)

def decode_hex(hex_string):
    """
    Decode a hex string representing Iran System encoded bytes.
    
    Args:
        hex_string (str): Hex string to decode.
        
    Returns:
        str: Decoded Unicode string.
    """
    clean_hex = re.sub(r'[^0-9a-fA-F]', '', hex_string)
    iransystem_bytes = bytes.fromhex(clean_hex)
    return decode(iransystem_bytes)
