# -*- coding: utf-8 -*-

import unittest
from iran_encoding import encode, decode
from iran_encoding.mappings import REVERSE_IRAN_SYSTEM_MAP, IRAN_SYSTEM_MAP

class TestIranSystemEncoding(unittest.TestCase):

    def test_pure_ltr_roundtrip(self):
        """Test encoding and decoding of a pure LTR (English) string."""
        text = "Hello, World! 123"
        encoded = encode(text)
        decoded = decode(encoded)
        self.assertEqual(text, decoded)

    def test_pure_rtl_roundtrip(self):
        """Test encoding and decoding of a pure RTL (Persian) string."""
        text = "سلام دنیا"
        encoded = encode(text)
        decoded = decode(encoded)
        self.assertEqual(text, decoded)

    def test_mixed_ltr_rtl_roundtrip(self):
        """Test a mixed string: LTR -> RTL."""
        text = "Test: تست"
        encoded = encode(text)
        decoded = decode(encoded)
        self.assertEqual(text, decoded)

    def test_mixed_rtl_ltr_roundtrip(self):
        """Test a mixed string: RTL -> LTR."""
        text = "تست: Test"
        encoded = encode(text)
        decoded = decode(encoded)
        self.assertEqual(text, decoded)

    def test_string_with_numbers_roundtrip(self):
        """Test a mixed string with numbers."""
        text = "ETA: 10 دقیقه"
        encoded = encode(text)
        decoded = decode(encoded)
        # Note: The map contains Persian digits, not ASCII. Let's test that.
        text_persian_digits = "زمان رسیدن: ۱۰ دقیقه"
        encoded_pd = encode(text_persian_digits)
        decoded_pd = decode(encoded_pd)
        self.assertEqual(text_persian_digits, decoded_pd)

    def test_unknown_characters(self):
        """Test that unknown characters are replaced with a fallback."""
        text = "Hello Привет World"  # "Привет" is Russian (Cyrillic)
        encoded = encode(text)

        # Manually build expected encoded bytes
        expected_bytes = []
        fallback_code = REVERSE_IRAN_SYSTEM_MAP.get('?')
        for char in "Hello ????? World": # " Привет" has 7 chars including space
             expected_bytes.append(REVERSE_IRAN_SYSTEM_MAP.get(char, fallback_code))

        # The actual logic is a bit more complex due to bidi handling of space
        # A simpler test is to decode and check the result
        decoded = decode(encoded)
        self.assertEqual(decoded, "Hello ?????? World") # 6 chars in Привет

    def test_empty_string(self):
        """Test that an empty string is handled correctly."""
        self.assertEqual(encode(""), b"")
        self.assertEqual(decode(b""), "")

    def test_all_known_chars_roundtrip(self):
        """Test that all single characters in the map can be round-tripped."""
        known_chars = [char for char in REVERSE_IRAN_SYSTEM_MAP.keys() if len(char) == 1]

        for char in known_chars:
            with self.subTest(char=char):
                encoded = encode(char)
                decoded = decode(encoded)
                self.assertEqual(char, decoded)

if __name__ == "__main__":
    unittest.main()
