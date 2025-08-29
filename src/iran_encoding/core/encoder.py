import re
import unicodedata
from typing import List
import arabic_reshaper
from bidi.algorithm import get_display
from .mappings import IRAN_SYSTEM_MAP, REVERSE_IRAN_SYSTEM_MAP, UNKNOWN_CHAR_CODE

class IranSystemEncoder:
    """
    A class to handle encoding and decoding for the Iran System character set.
    """
    rtl_char_pattern = re.compile(r'([\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+)')

    def __init__(self):
        configuration = {
            'support_ligatures': False,
        }
        self.reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)

    def encode(self, text: str, visual_ordering: bool = True) -> bytes:
        """
        Encodes a string into a sequence of bytes using the Iran System map.
        """
        if not isinstance(text, str):
            return b''

        reshaped_text = self.reshaper.reshape(text)

        if visual_ordering:
            parts = self.rtl_char_pattern.split(reshaped_text)
            processed_parts = []
            for part in parts:
                if self.rtl_char_pattern.match(part):
                    visual_part = get_display(part, base_dir='R')
                    processed_parts.append(visual_part)
                else:
                    processed_parts.append(part)
            output_text = "".join(processed_parts)
        else:
            output_text = reshaped_text

        byte_codes = [REVERSE_IRAN_SYSTEM_MAP.get(char, UNKNOWN_CHAR_CODE) for char in output_text]
        return bytes(byte_codes)

    def decode(self, data: bytes) -> str:
        """
        Decodes a byte string from the Iran System encoding back to a string.
        """
        if not isinstance(data, bytes):
            return ''

        visual_chars: List[str] = [IRAN_SYSTEM_MAP.get(byte, '�') for byte in data]
        visual_text = "".join(visual_chars)

        parts = self.rtl_char_pattern.split(visual_text)
        logical_parts = []
        for part in parts:
            if self.rtl_char_pattern.match(part):
                is_all_digits = all('\u06F0' <= c <= '\u06F9' for c in part)
                if is_all_digits:
                    logical_parts.append(part)  # Do not reverse numbers
                else:
                    logical_parts.append(part[::-1])
            else:
                logical_parts.append(part)
        logical_text = "".join(logical_parts)

        return unicodedata.normalize('NFKD', logical_text)

    def decode_hex(self, hex_string: str) -> str:
        """
        Decodes a hex string into a UTF-8 string using the Iran System map.
        """
        try:
            data = bytes.fromhex(hex_string)
            return self.decode(data)
        except (ValueError, TypeError):
            return "Error: Invalid hex string"
