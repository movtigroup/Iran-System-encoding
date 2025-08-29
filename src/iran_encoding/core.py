# -*- coding: utf-8 -*-
import re
import unicodedata
from typing import List, Dict, Optional
import arabic_reshaper
from bidi.algorithm import get_display
from .exceptions import EncodingError, DecodeError, TextShapingError

# --- Mappings ---
IRAN_SYSTEM_MAP = {
    0x20: " ", 0x21: "!", 0x22: "\"", 0x23: "#", 0x24: "$", 0x25: "%", 0x26: "&", 0x27: "'",
    0x28: "(", 0x29: ")", 0x2A: "*", 0x2B: "+", 0x2C: ",", 0x2D: "-", 0x2E: ".", 0x2F: "/",
    0x30: "0", 0x31: "1", 0x32: "2", 0x33: "3", 0x34: "4", 0x35: "5", 0x36: "6", 0x37: "7",
    0x38: "8", 0x39: "9", 0x3A: ":", 0x3B: ";", 0x3C: "<", 0x3D: "=", 0x3E: ">", 0x3F: "?",
    0x40: "@", 0x41: "A", 0x42: "B", 0x43: "C", 0x44: "D", 0x45: "E", 0x46: "F", 0x47: "G",
    0x48: "H", 0x49: "I", 0x4A: "J", 0x4B: "K", 0x4C: "L", 0x4D: "M", 0x4E: "N", 0x4F: "O",
    0x50: "P", 0x51: "Q", 0x52: "R", 0x53: "S", 0x54: "T", 0x55: "U", 0x56: "V", 0x57: "W",
    0x58: "X", 0x59: "Y", 0x5A: "Z", 0x5B: "[", 0x5C: "\\", 0x5D: "]", 0x5E: "^", 0x5F: "_",
    0x60: "`", 0x61: "a", 0x62: "b", 0x63: "c", 0x64: "d", 0x65: "e", 0x66: "f", 0x67: "g",
    0x68: "h", 0x69: "i", 0x6A: "j", 0x6B: "k", 0x6C: "l", 0x6D: "m", 0x6E: "n", 0x6F: "o",
    0x70: "p", 0x71: "q", 0x72: "r", 0x73: "s", 0x74: "t", 0x75: "u", 0x76: "v", 0x77: "w",
    0x78: "x", 0x79: "y", 0x7A: "z", 0x7B: "{", 0x7C: "|", 0x7D: "}", 0x7E: "~",
    0x80: "۰", 0x81: "۱", 0x82: "۲", 0x83: "۳", 0x84: "۴", 0x85: "۵", 0x86: "۶", 0x87: "۷",
    0x88: "۸", 0x89: "۹", 0x8A: "،", 0x8B: "ـ", 0x8C: "؟", 0x8D: "ﺁ", 0x8E: "ﺋ", 0x8F: "ﺀ",
    0x90: "ﺍ", 0x91: "ﺎ", 0x92: "ﺏ", 0x93: "ﺑ", 0x94: "ﭖ", 0x95: "ﭘ", 0x96: "ﺕ", 0x97: "ﺗ",
    0x98: "ﺙ", 0x99: "ﺛ", 0x9A: "ﺝ", 0x9B: "ﺟ", 0x9C: "ﭺ", 0x9D: "ﭼ", 0x9E: "ﺡ", 0x9F: "ﺣ",
    0xA0: "ﺥ", 0xA1: "ﺧ", 0xA2: "ﺩ", 0xA3: "ﺫ", 0xA4: "ﺭ", 0xA5: "ﺯ", 0xA6: "ﮊ", 0xA7: "ﺱ",
    0xA8: "ﺳ", 0xA9: "ﺵ", 0xAA: "ﺷ", 0xAB: "ﺹ", 0xAC: "ﺻ", 0xAD: "ﺽ", 0xAE: "ﺿ", 0xAF: "ﻁ",
    0xE0: "ﻅ", 0xE1: "ﻉ", 0xE2: "ﻊ", 0xE3: "ﻌ", 0xE4: "ﻋ", 0xE5: "ﻍ", 0xE6: "ﻎ", 0xE7: "ﻐ",
    0xE8: "ﻏ", 0xE9: "ﻑ", 0xEA: "ﻓ", 0xEB: "ﻕ", 0xEC: "ﻗ", 0xED: "ﮎ", 0xEE: "ﮐ", 0xEF: "ﮒ",
    0xF0: "ﮔ", 0xF1: "ﻝ", 0xF2: "ﻻ", 0xF3: "ﻟ", 0xF4: "ﻡ", 0xF5: "ﻣ", 0xF6: "ﻥ", 0xF7: "ﻧ",
    0xF8: "ﻭ", 0xF9: "ﻩ", 0xFA: "ﻬ", 0xFB: "ﻫ", 0xFC: "ﯽ", 0xFD: "ﯼ", 0xFE: "ﯾ",
}
REVERSE_IRAN_SYSTEM_MAP = {v: k for k, v in IRAN_SYSTEM_MAP.items()}
EXTRA_FORMS = { 'ﺒ': 0x93, 'ﺐ': 0x92, 'ﭙ': 0x95, 'ﭗ': 0x94, 'ﺘ': 0x97, 'ﺖ': 0x96, 'ﺜ': 0x99, 'ﺚ': 0x98, 'ﺠ': 0x9B, 'ﺞ': 0x9A, 'ﭽ': 0x9D, 'ﭻ': 0x9C, 'ﺤ': 0x9F, 'ﺢ': 0x9E, 'ﺨ': 0xA1, 'ﺦ': 0xA0, 'ﺪ': 0xA2, 'ﺬ': 0xA3, 'ﺮ': 0xA4, 'ﺰ': 0xA5, 'ﮋ': 0xA6, 'ﺴ': 0xA8, 'ﺲ': 0xA7, 'ﺸ': 0xAA, 'ﺶ': 0xA9, 'ﺼ': 0xAC, 'ﺺ': 0xAB, 'ﻀ': 0xAE, 'ﺾ': 0xAD, 'ﻂ': 0xAF, 'ﻇ': 0xE0, 'ﻈ': 0xE0, 'ﻆ': 0xE0, 'ﻌ': 0xE3, 'ﻊ': 0xE2, 'ﻐ': 0xE7, 'ﻎ': 0xE6, 'ﻔ': 0xEA, 'ﻒ': 0xE9, 'ﻘ': 0xEC, 'ﻖ': 0xEB, 'ﮑ': 0xEE, 'ﮏ': 0xED, 'ﮕ': 0xF0, 'ﮓ': 0xEF, 'ﻠ': 0xF3, 'ﻞ': 0xF1, 'ﻤ': 0xF5, 'ﻢ': 0xF4, 'ﻨ': 0xF7, 'ﻦ': 0xF6, 'ﻮ': 0xF8, 'ﻬ': 0xFA, 'ﻪ': 0xF9, 'ﺌ': 0x8E, 'ﯿ': 0xFE, 'ﯽ': 0xFC, 'ﻻ': 0xF2, 'ﻼ': 0xF2 }
REVERSE_IRAN_SYSTEM_MAP.update(EXTRA_FORMS)

class IranSystemEncoder:
    def __init__(self, visual_ordering: bool = True, fallback_char: Optional[str] = None, cache_enabled: bool = False):
        self.visual_ordering = visual_ordering
        self.fallback_char = fallback_char
        self.cache_enabled = cache_enabled
        self.reshaper = arabic_reshaper.ArabicReshaper({'delete_harakat': True, 'support_ligatures': True})
        if self.cache_enabled:
            self._encode_cache: Dict[str, bytes] = {}
            self._decode_cache: Dict[bytes, str] = {}

    def shape_text(self, text: str) -> str:
        try:
            return self.reshaper.reshape(text)
        except Exception as e:
            raise TextShapingError(f"Error during text shaping: {e}") from e

    def encode(self, text: str, visual_ordering: Optional[bool] = None) -> bytes:
        if visual_ordering is None:
            visual_ordering = self.visual_ordering
        if self.cache_enabled and text in self._encode_cache:
            return self._encode_cache[text]

        reshaped_text = self.shape_text(text)
        if visual_ordering:
            # This logic is adapted from the original library to handle bidi part-by-part
            rtl_char_pattern = re.compile(r'([\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+)')
            parts = rtl_char_pattern.split(reshaped_text)
            processed_parts = []
            for part in parts:
                if rtl_char_pattern.match(part):
                    visual_part = get_display(part, base_dir='R')
                    processed_parts.append(visual_part)
                else:
                    processed_parts.append(part)
            output_text = "".join(processed_parts)
        else:
            output_text = reshaped_text

        byte_codes = []
        for char in output_text:
            code = REVERSE_IRAN_SYSTEM_MAP.get(char)
            if code is None:
                if self.fallback_char:
                    code = REVERSE_IRAN_SYSTEM_MAP.get(self.fallback_char)
                    if code is None:
                        raise EncodingError(f"Fallback character '{self.fallback_char}' not found in encoding map.")
                else:
                    raise EncodingError(f"Character '{char}' not found in encoding map and no fallback is set.")
            byte_codes.append(code)

        result = bytes(byte_codes)
        if self.cache_enabled:
            self._encode_cache[text] = result
        return result

    def decode(self, data: bytes) -> str:
        if self.cache_enabled and data in self._decode_cache:
            return self._decode_cache[data]

        try:
            chars = [IRAN_SYSTEM_MAP[byte] for byte in data]
        except KeyError as e:
            raise DecodeError(f"Invalid byte {e} in input data.") from e

        visual_text = "".join(chars)

        # Manually reverse RTL segments to get logical text
        rtl_char_pattern = re.compile(r'([\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+)')
        parts = rtl_char_pattern.split(visual_text)
        logical_parts = []
        for part in parts:
            if rtl_char_pattern.match(part):
                logical_parts.append(part[::-1])
            else:
                logical_parts.append(part)
        logical_text = "".join(logical_parts)

        normalized_text = unicodedata.normalize('NFKC', logical_text)

        if self.cache_enabled:
            self._decode_cache[data] = normalized_text
        return normalized_text
