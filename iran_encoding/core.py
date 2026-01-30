"""
Core implementation of Iran System encoding logic, ported from C.
This module provides a pure Python implementation of the original C code
to ensure consistent behavior across all platforms without external dependencies.
"""
from typing import List, Union, Optional

# Character mapping tables ported from iran_system.c
UNICODE_NUMBER_STR: List[int] = [0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39]
IRANSYSTEM_NUMBER_STR: List[int] = [0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89]

UNICODE_STR: List[int] = [
    0xC2, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2,
    0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3,
    0xE4, 0xE6, 0x80, 0x8A, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20,
    0xA1, 0xC1
]

IRANSYSTEM_UPPER_STR: List[int] = [
    0x8D, 0x92, 0x94, 0x96, 0x98, 0x9A, 0x9C, 0x9E, 0xA0, 0xA2, 0xA3, 0xA4, 0xA5,
    0xA6, 0xA7, 0xA9, 0xAB, 0xAD, 0xAF, 0xE0, 0xE9, 0xEB, 0xED, 0xEF, 0xF1, 0xF4,
    0xF6, 0xF8, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20,
    0x8A, 0x8F
]

IRANSYSTEM_LOWER_STR: List[int] = [
    0x8D, 0x93, 0x95, 0x97, 0x99, 0x9B, 0x9D, 0x9F, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5,
    0xA6, 0xA8, 0xAA, 0xAC, 0xAE, 0xAF, 0xE0, 0xEA, 0xEC, 0xEE, 0xF0, 0xF3, 0xF5,
    0xF7, 0xF8, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x20,
    0x8A, 0x8E
]

NEXT_CHAR_STR: List[int] = [
    0xC2, 0xC7, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1,
    0xD2, 0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDD, 0xDE, 0x98, 0x90, 0xE1,
    0xE3, 0xE4, 0xE6, 0xDA, 0xDB, 0xED, 0xE5, 0xC1
]

PREV_CHAR_STR: List[int] = [
    0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8,
    0xD9, 0xDA, 0xDB, 0xDD, 0xDE, 0x98, 0x90, 0xE1, 0xE3, 0xE4, 0xE5, 0xED, 0xC1
]

UNICODE_STR_TAIL: List[int] = [0xDA, 0xDB, 0xE5, 0xC7, 0xED]
IRANSYSTEM_UPPER_STR_TAIL: List[int] = [0xE1, 0xE5, 0xF9, 0x90, 0xFD]
IRANSYSTEM_LOWER_STR_TAIL: List[int] = [
    0xE2, 0xE3, 0xE4,  # ein
    0xE6, 0xE7, 0xE8,  # ghein
    0xFA, 0xFB, 0xFB,  # he
    0x91, 0x91, 0x91,  # alef
    0xFC, 0xFE, 0xFE   # ye
]

WIDE_CHAR_STR: List[int] = [
    0x0622, 0x0628, 0x067E, 0x062A, 0x062B, 0x062C, 0x0686, 0x062D, 0x062E, 0x062F,
    0x0630, 0x0631, 0x0632, 0x0698, 0x0633, 0x0634, 0x0635, 0x0636, 0x0637, 0x0638,
    0x0639, 0x063A, 0x0641, 0x0642, 0x06A9, 0x06AF, 0x0644, 0x0645, 0x0646, 0x0648,
    0x0647, 0x06CC, 0x06F0, 0x06F1, 0x06F2, 0x06F3, 0x06F4, 0x06F5, 0x06F6, 0x06F7,
    0x06F8, 0x06F9, 0x0020, 0x060C, 0x0627, 0x0626, 0x064A, 0x0621, 0x0643, 0x02DC,
    0x00C6
]

UTF8_STR: List[int] = [
    0xC2, 0xC8, 0x81, 0xCA, 0xCB, 0xCC, 0x8D, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2,
    0x8E, 0xD3, 0xD4, 0xD5, 0xD6, 0xD8, 0xD9, 0xDA, 0xDB, 0xDD, 0xDE, 0x98, 0x90,
    0xE1, 0xE3, 0xE4, 0xE6, 0xE5, 0xED, 0x80, 0x8A, 0x82, 0x83, 0x84, 0x85, 0x86,
    0x87, 0x88, 0x89, 0x20, 0xA1, 0xC7, 0xED, 0xED, 0xC1, 0x98, 0x98, 0xC1
]


def is_digit_irs(c: Union[int, str]) -> bool:
    """Check if character is a digit or Iran System digit."""
    val = c if isinstance(c, int) else ord(c)
    return (ord('0') <= val <= ord('9')) or (0x80 <= val <= 0x89)


def find_pos(in_byte: int, area_list: List[int]) -> int:
    """Find position of a byte in a list."""
    try:
        return area_list.index(in_byte)
    except ValueError:
        return -1


def find_pos16(in_val: int, area_list: List[int]) -> int:
    """Find position of a 16-bit value in a list."""
    try:
        return area_list.index(in_val)
    except ValueError:
        return -1


def iransystem_to_upper(in_bytes: bytes) -> bytes:
    """Convert Iran System lower forms to upper (isolated/final) forms."""
    out_list = []
    for b in in_bytes:
        pos_index = find_pos(b, IRANSYSTEM_LOWER_STR)
        if pos_index < 0:
            pos_index = find_pos(b, IRANSYSTEM_LOWER_STR_TAIL)
            if pos_index < 0:
                out_list.append(b)
            else:
                out_list.append(IRANSYSTEM_UPPER_STR_TAIL[pos_index // 3])
        else:
            out_list.append(IRANSYSTEM_UPPER_STR[pos_index])
    return bytes(out_list)


def iransystem_to_unicode_script(in_bytes: bytes) -> bytes:
    """Convert Iran System bytes to the intermediate Unicode script representation."""
    out_list = []
    for b in in_bytes:
        pos_index = find_pos(b, IRANSYSTEM_UPPER_STR)
        if pos_index < 0:
            pos_index = find_pos(b, IRANSYSTEM_UPPER_STR_TAIL)
            if pos_index < 0:
                out_list.append(b)
            else:
                out_list.append(UNICODE_STR_TAIL[pos_index])
        else:
            out_list.append(UNICODE_STR[pos_index])
    return bytes(out_list)


def reverse(in_bytes: bytes) -> bytes:
    """Reverse a byte array."""
    return in_bytes[::-1]


def reverse_alpha_numeric(in_bytes: bytes) -> bytes:
    """
    Reverse alphanumeric sequences in a way that respects Iran System visual order.
    Matches the improved logic in the C implementation.
    """
    length = len(in_bytes)
    out = bytearray(in_bytes)
    number_position = 0

    for byte_count in range(length + 1):
        current = in_bytes[byte_count] if byte_count < length else 0xFF

        if current > 0x7E or current < 0x20:
            if (byte_count - number_position) > 1:
                for number_count in range(number_position, byte_count):
                    out[number_count] = in_bytes[byte_count - (number_count - number_position) - 1]
            number_position = byte_count + 1

        if byte_count < length:
            out[byte_count] = in_bytes[byte_count]

    return bytes(out)


def reverse_iransystem(in_bytes: bytes) -> bytes:
    """Reverse Iran System bytes while keeping non-Iran System characters in order."""
    length = len(in_bytes)
    out = bytearray(in_bytes)
    number_position = 0

    for byte_count in range(length + 1):
        current = in_bytes[byte_count] if byte_count < length else ord(' ')

        if current < 80:
            if (byte_count - number_position) > 1:
                for number_count in range(number_position, byte_count):
                    out[number_count] = in_bytes[byte_count - (number_count - number_position) - 1]
            number_position = byte_count + 1
            if byte_count < length:
                out[byte_count] = in_bytes[byte_count]

    return bytes(out)


def unicode_number_to_iransystem(unicode_str: str) -> bytes:
    """Convert Unicode numbers to Iran System numbers."""
    in_bytes = unicode_str.encode('utf-8', errors='replace')
    out_list = []
    for b in in_bytes:
        pos_index = find_pos(b, UNICODE_NUMBER_STR)
        if pos_index >= 0:
            out_list.append(IRANSYSTEM_NUMBER_STR[pos_index])
        else:
            out_list.append(b)
    return bytes(out_list)


def unicode_to_persian_script(unicode_char_code: int) -> int:
    """Convert a single Unicode character code to the intermediate Persian script byte."""
    pos_index = find_pos16(unicode_char_code, WIDE_CHAR_STR)
    if pos_index >= 0:
        return UTF8_STR[pos_index]
    else:
        return unicode_char_code if unicode_char_code < 256 else ord('?')


def unicode_to_iransystem(unicode_string: str, reverse_flag: bool = True) -> bytes:
    """
    Main function to convert Unicode string to Iran System bytes.
    Matches the logic of UnicodeToIransystem in C.
    """
    # First convert Unicode to the intermediate "Persian Script" bytes
    script_bytes = bytearray()
    for char in unicode_string:
        script_bytes.append(unicode_to_persian_script(ord(char)))

    if reverse_flag:
        input_bytes = reverse_alpha_numeric(bytes(script_bytes))
    else:
        input_bytes = bytes(script_bytes)

    result = bytearray(input_bytes)
    length = len(input_bytes)

    for byte_count in range(length):
        prev_byte = input_bytes[byte_count - 1] if byte_count > 0 else 0
        next_byte = input_bytes[byte_count + 1] if byte_count < (length - 1) else 0

        current_byte = input_bytes[byte_count]
        pos_index = find_pos(current_byte, UNICODE_STR)

        if pos_index >= 0:
            if find_pos(next_byte, NEXT_CHAR_STR) >= 0:
                result[byte_count] = IRANSYSTEM_LOWER_STR[pos_index]
            else:
                result[byte_count] = IRANSYSTEM_UPPER_STR[pos_index]
        else:
            # Special cases for complex Persian characters
            if current_byte == 218:  # ein
                if find_pos(next_byte, NEXT_CHAR_STR) >= 0:
                    if find_pos(prev_byte, PREV_CHAR_STR) >= 0:
                        result[byte_count] = 227  # medial
                    else:
                        result[byte_count] = 228  # initial
                else:
                    if find_pos(prev_byte, PREV_CHAR_STR) >= 0:
                        result[byte_count] = 226  # final connected
                    else:
                        result[byte_count] = 225  # final isolated
            elif current_byte == 219:  # ghein
                if find_pos(next_byte, NEXT_CHAR_STR) >= 0:
                    if find_pos(prev_byte, PREV_CHAR_STR) >= 0:
                        result[byte_count] = 231  # medial
                    else:
                        result[byte_count] = 232  # initial
                else:
                    if find_pos(prev_byte, PREV_CHAR_STR) >= 0:
                        result[byte_count] = 230  # final connected
                    else:
                        result[byte_count] = 229  # final isolated
            elif current_byte == 229:  # he
                if find_pos(next_byte, NEXT_CHAR_STR) >= 0:
                    if find_pos(prev_byte, PREV_CHAR_STR) >= 0:
                        result[byte_count] = 250  # medial
                    else:
                        result[byte_count] = 251  # initial
                else:
                    result[byte_count] = 249  # final
            elif current_byte == 199:  # alef
                if find_pos(prev_byte, PREV_CHAR_STR) >= 0:
                    result[byte_count] = 145  # connected
                else:
                    result[byte_count] = 144  # isolated
            elif current_byte == 237:  # ye
                if find_pos(next_byte, NEXT_CHAR_STR) >= 0:
                    result[byte_count] = 254  # medial
                else:
                    if find_pos(prev_byte, PREV_CHAR_STR) >= 0:
                        result[byte_count] = 252  # final connected
                    else:
                        result[byte_count] = 253  # final isolated
            else:
                # Handle numbers
                if ord('0') <= current_byte <= ord('9'):
                    p_idx = find_pos(current_byte, UNICODE_NUMBER_STR)
                    if p_idx >= 0:
                        result[byte_count] = IRANSYSTEM_NUMBER_STR[p_idx]

    return bytes(result)


def persian_script_to_unicode(utf8_char_byte: int) -> int:
    """Convert a Persian script byte back to Unicode code point."""
    pos_index = find_pos(utf8_char_byte, UTF8_STR)
    if pos_index >= 0:
        return WIDE_CHAR_STR[pos_index]
    else:
        return utf8_char_byte


def iransystem_to_unicode(in_bytes: bytes) -> str:
    """
    Convert Iran System bytes to Unicode string.
    Ported from IransystemToUnicode in C, improved to handle all forms.
    """
    # First convert to upper (isolated/final) forms to handle all visual variants
    upper_bytes = iransystem_to_upper(in_bytes)

    script_bytes = bytearray()
    for b in upper_bytes:
        pos_index = find_pos(b, IRANSYSTEM_UPPER_STR)
        if pos_index < 0:
            pos_index = find_pos(b, IRANSYSTEM_UPPER_STR_TAIL)
            if pos_index < 0:
                script_bytes.append(b)
            else:
                script_bytes.append(UNICODE_STR_TAIL[pos_index])
        else:
            script_bytes.append(UNICODE_STR[pos_index])

    unicode_chars = []
    for b in script_bytes:
        unicode_chars.append(chr(persian_script_to_unicode(b)))

    return "".join(unicode_chars)
