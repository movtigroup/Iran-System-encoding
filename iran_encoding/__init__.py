"""
Iran System Encoding Package - Main Module

This package provides encoding and decoding functions for the Iran System character set,
with support for both Persian and English text processing, number handling based on locale,
and various utility functions.
"""
from .converter import convert_iransystem_to_unicode
from .mappings import IRAN_SYSTEM_MAP, REVERSE_IRAN_SYSTEM_MAP, IRAN_SYSTEM_UNICODE_NUMBERS, UNICODE_IRAN_SYSTEM_NUMBERS
import arabic_reshaper
from bidi.algorithm import get_display
import re


def detect_locale(text):
    """
    Detect if the text is primarily Persian/Farsi ('fa') or English ('en').
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        str: 'fa' if Persian dominant, 'en' if English dominant
    """
    persian_chars = len(re.findall(r'[ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    return 'fa' if persian_chars > english_chars else 'en'


def _find_pos(byte_val, byte_array):
    """
    Find position of a byte in a byte array, similar to FindPos function in C code.
    """
    for idx, val in enumerate(byte_array):
        if val == byte_val:
            return idx
    return -1


def _find_pos16(byte_val, byte_array):
    """
    Find position of a value in a 16-bit integer array, similar to FindPos16 function in C code.
    """
    for idx, val in enumerate(byte_array):
        if val == byte_val:
            return idx
    return -1


def _unicode_to_iransystem_internal(text):
    """
    Internal function to convert Unicode to Iran System encoding,
    implementing the exact same logic as the C code.
    """
    # Define the arrays from the C code
    unicode_str = [0xC2, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2, 0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3, 0xE4, 0xE6, 0x80, 0x8A, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20, 0xA1, 0xC1, 0]
    iransystem_upper_str = [0x8D, 0x92, 0x94, 0x96, 0x98, 0x9A, 0x9C, 0x9E, 0xA0, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA9, 0xAB, 0xAD, 0xAF, 0xE0, 0xE9, 0xEB, 0xED, 0xEF, 0xF1, 0xF4, 0xF6, 0xF8, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20, 0x8A, 0x8F, 0]
    iransystem_lower_str = [0x8D, 0x93, 0x95, 0x97, 0x99, 0x9B, 0x9D, 0x9F, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA8, 0xAA, 0xAC, 0xAE, 0xAF, 0xE0, 0xEA, 0xEC, 0xEE, 0xF0, 0xF3, 0xF5, 0xF7, 0xF8, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20, 0x8A, 0x8E, 0]
    next_char_str = [0xC2, 0xC7, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2, 0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3, 0xE4, 0xE6, 0xDA, 0xDB, 0xED, 0xE5, 0xC1, 0]
    prev_char_str = [0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDA, 0xDB, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3, 0xE4, 0xE5, 0xED, 0xC1, 0]
    unicode_str_tail = [0xDA, 0xDB, 0xE5, 0xC7, 0xED, 0]
    iransystem_upper_str_tail = [0xE1, 0xE5, 0xF9, 0x90, 0xFD, 0]
    iransystem_lower_str_tail = [0xE2, 0xE3, 0xE4, 0xE6, 0xE7, 0xE8, 0xFA, 0xFB, 0xFB, 0x91, 0x91, 0x91, 0xFC, 0xFE, 0xFE, 0]
    
    # First, convert the text from Unicode to Persian script representation
    # We need to convert the text to the UTF-8 byte representation used in the C code
    # The wideCharStr and UTF8Str arrays in the C code map Unicode to UTF-8 bytes
    
    # Let's first create a mapping from Unicode characters to the UTF-8 bytes
    # used in the Iran System encoding
    wide_char_str = [0x0622, 0x0628, 0x067E, 0x062A, 0x062B, 0x062C, 0x0686, 0x062D, 0x062E, 0x062F, 0x0630, 0x0631, 0x0632, 0x0698, 0x0633, 0x0634, 0x0635, 0x0636, 0x0637, 0x0638, 0x0639, 0x063A, 0x0641, 0x0642, 0x06A9, 0x06AF, 0x0644, 0x0645, 0x0646, 0x0648, 0x0647, 0x06CC, 0x0660, 0x0661, 0x0662, 0x0663, 0x0664, 0x0665, 0x0666, 0x0667, 0x0668, 0x0669, 0x0020, 0x060C, 0x0627, 0x0626, 0x064A, 0x0621, 0x0643, 0x02DC, 0x00C6, 0]
    utf8_str = [0xC2, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2, 0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDA, 0xDB, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3, 0xE4, 0xE6, 0xE5, 0xED, 0x80, 0x8A, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20, 0xA1, 0xC7, 0xED, 0xED, 0xC1, 0x98, 0x98, 0xC1, 0]
    
    # Convert the input text to the UTF-8 representation used in Iran System
    converted_text = []
    for char in text:
        # Get the Unicode code point of the character
        unicode_code = ord(char)
        # Find if it's in the wide character string
        pos_index = _find_pos16(unicode_code, wide_char_str)
        if pos_index != -1:
            # Found in the wide character string, use corresponding UTF-8 byte
            converted_text.append(utf8_str[pos_index])
        else:
            # Not found, just add the character code (ASCII for non-Persian chars)
            converted_text.append(unicode_code)
    
    # Now apply the main algorithm from the C code
    # This mimics the UnicodeToIransystem function
    input_codes = converted_text
    result = input_codes[:]  # Copy the input initially
    
    # Process each character according to the C algorithm
    for byte_count in range(len(input_codes)):
        # Get previous and next characters for context
        if byte_count > 0:
            prev_byte = input_codes[byte_count - 1]
        else:
            prev_byte = 0
            
        if byte_count < (len(input_codes) - 1):
            next_byte = input_codes[byte_count + 1]
        else:
            next_byte = 0

        # Find position in unicode string (using the C code logic)
        pos_index = _find_pos(input_codes[byte_count], unicode_str)
        
        if pos_index >= 0:
            # Check if next character is in next_char_str
            next_pos = _find_pos(next_byte, next_char_str)
            
            if next_pos >= 0:
                # Use lower form (connected to next character)
                if pos_index < len(iransystem_lower_str):
                    result[byte_count] = iransystem_lower_str[pos_index]
            else:
                # Use upper form (not connected to next character)
                if pos_index < len(iransystem_upper_str):
                    result[byte_count] = iransystem_upper_str[pos_index]
        else:
            # Handle special cases that are not in the main mapping
            # This covers the switch statement in the C code
            current_char_code = input_codes[byte_count]
            
            if current_char_code == 218:  # 0xDA - ain
                next_pos = _find_pos(next_byte, next_char_str)
                prev_pos = _find_pos(prev_byte, prev_char_str)
                
                if next_pos >= 0:
                    if prev_pos >= 0:
                        result[byte_count] = 227  # 0xE3 vasat (medial)
                    else:
                        result[byte_count] = 228  # 0xE4 aval (initial)
                else:
                    if prev_pos >= 0:
                        result[byte_count] = 226  # 0xE2 akhar chasbon (final connected)
                    else:
                        result[byte_count] = 225  # 0xE1 akhar (final isolated)
            elif current_char_code == 219:  # 0xDB - ghein
                next_pos = _find_pos(next_byte, next_char_str)
                prev_pos = _find_pos(prev_byte, prev_char_str)
                
                if next_pos >= 0:
                    if prev_pos >= 0:
                        result[byte_count] = 231  # 0xE7 vasat (medial)
                    else:
                        result[byte_count] = 232  # 0xE8 aval (initial)
                else:
                    if prev_pos >= 0:
                        result[byte_count] = 230  # 0xE6 akhar chasbon (final connected)
                    else:
                        result[byte_count] = 229  # 0xE5 akhar (final isolated)
            elif current_char_code == 229:  # 0xE5 - he
                next_pos = _find_pos(next_byte, next_char_str)
                prev_pos = _find_pos(prev_byte, prev_char_str)
                
                if next_pos >= 0:
                    if prev_pos >= 0:
                        result[byte_count] = 250  # 0xFA vasat (medial)
                    else:
                        result[byte_count] = 251  # 0xFB aval (initial)
                else:
                    result[byte_count] = 249  # 0xF9 akhar (final)
            elif current_char_code == 199:  # 0xC7 - alef
                prev_pos = _find_pos(prev_byte, prev_char_str)
                
                if prev_pos >= 0:
                    result[byte_count] = 145  # 0x91 chasbon (final connected)
                else:
                    result[byte_count] = 144  # 0x90 joda (isolated)
            elif current_char_code == 237:  # 0xED - ye
                next_pos = _find_pos(next_byte, next_char_str)
                
                if next_pos >= 0:
                    result[byte_count] = 254  # 0xFE vasat (medial)
                else:
                    prev_pos = _find_pos(prev_byte, prev_char_str)
                    
                    if prev_pos >= 0:
                        result[byte_count] = 252  # 0xFC akhar chasbon (final connected)
                    else:
                        result[byte_count] = 253  # 0xFD akhar (final isolated)
            else:
                # For other characters, check if it's a number
                if 0x30 <= current_char_code <= 0x39:  # ASCII digits 0-9
                    # Handle ASCII numbers
                    pos_index = _find_pos(current_char_code, [0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0])
                    if pos_index != -1:
                        result[byte_count] = [0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0][pos_index]
    
    # Filter out any invalid values and convert to bytes
    # Make sure all values are in the range 0-255
    result = [b % 256 for b in result if b is not None and b != 0]
    return bytes(result)


def encode(text, visual_ordering=True, configuration=None):
    """
    Encode a Unicode string to Iran System encoding bytes.
    
    Args:
        text (str): The Unicode string to encode
        visual_ordering (bool): Whether to use visual ordering (default True)
        configuration: Additional configuration for reshaping
        
    Returns:
        bytes: Iran System encoded bytes
    """
    # Detect locale to handle numbers appropriately
    locale = detect_locale(text)
    
    # Handle numbers based on locale
    processed_text = _handle_numbers_by_locale(text, locale)
    
    # Apply Arabic reshaping if needed
    if visual_ordering:
        # Create reshaper with default configuration
        default_config = {
            'delete_harakat': True,
            'delete_tatweel': True,
            'support_ligatures': True,
        }
        
        # Override with user configuration if provided
        if configuration:
            default_config.update(configuration)
        
        try:
            # Try with configuration parameter first
            reshaped_text = arabic_reshaper.reshape(processed_text, default_config)
        except TypeError:
            # Fallback for versions that don't accept configuration parameter
            reshaped_text = arabic_reshaper.reshape(processed_text)
        
        processed_text = get_display(reshaped_text)
    
    # Use the internal function that implements the C algorithm
    encoded_bytes = _unicode_to_iransystem_internal(processed_text)
    
    # If the internal function didn't work properly, fall back to basic mapping
    if len(encoded_bytes) == 0 or all(b == 0 for b in encoded_bytes):
        result = []
        for char in processed_text:
            if char in REVERSE_IRAN_SYSTEM_MAP:
                result.append(REVERSE_IRAN_SYSTEM_MAP[char])
            elif char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                if locale == 'fa' and char in IRAN_SYSTEM_UNICODE_NUMBERS:
                    result.append(IRAN_SYSTEM_UNICODE_NUMBERS[char])
                else:
                    result.append(ord(char))
            else:
                result.append(0x3F)  # Question mark fallback
        return bytes(result)
    
    return encoded_bytes


def decode(iransystem_bytes):
    """
    Decode Iran System encoded bytes to a Unicode string.
    
    Args:
        iransystem_bytes (bytes): Iran System encoded bytes
        
    Returns:
        str: Decoded Unicode string
    """
    from .converter import convert_iransystem_to_unicode
    return convert_iransystem_to_unicode(iransystem_bytes)


def decode_hex(hex_string):
    """
    Decode a hex string representing Iran System encoded bytes.
    
    Args:
        hex_string (str): Hex string to decode
        
    Returns:
        str: Decoded Unicode string
    """
    iransystem_bytes = bytes.fromhex(hex_string.replace(" ", ""))
    return decode(iransystem_bytes)


def _handle_numbers_by_locale(text, locale):
    """
    Handle numbers based on detected locale.
    
    Args:
        text (str): Input text
        locale (str): Detected locale ('fa' or 'en')
        
    Returns:
        str: Text with numbers handled according to locale
    """
    if locale == 'fa':
        # Replace ASCII numbers with Persian numbers in the text
        for ascii_num, persian_num in [('0', '۰'), ('1', '۱'), ('2', '۲'), ('3', '۳'), 
                                      ('4', '۴'), ('5', '۵'), ('6', '۶'), ('7', '۷'), 
                                      ('8', '۸'), ('9', '۹')]:
            text = text.replace(ascii_num, persian_num)
    # For English locale, keep numbers as ASCII
    
    return text


__version__ = "1.0.0"
__author__ = "Community Contributors"
__all__ = ['encode', 'decode', 'decode_hex', 'detect_locale']