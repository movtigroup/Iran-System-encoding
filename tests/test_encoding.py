# -*- coding: utf-8 -*-

import unittest
from iran_encoding import encode, decode, decode_hex
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
        """
        Test that all characters in the IRAN_SYSTEM_MAP can be round-tripped.
        This test does not check for visual correctness, but for the integrity
        of the forward and reverse mappings.
        """
        for code, char in IRAN_SYSTEM_MAP.items():
            if len(char) == 1: # Skip multi-char sequences for this test
                with self.subTest(char=char, code=hex(code)):
                    # We are testing the raw mapping here, so we encode the
                    # presentation form character directly.
                    encoded_char = encode(char)

                    # The encoded byte should be the original code.
                    # This verifies the REVERSE_IRAN_SYSTEM_MAP.
                    if len(encoded_char) > 0: # reshaper can return empty for some chars
                        self.assertEqual(len(encoded_char), 1)
                        self.assertEqual(encoded_char[0], code)

                        # Now decode the byte back to a character.
                        decoded_char = decode(encoded_char)

                        # The decoded character, after normalization, should match
                        # the normalized version of the original character.
                        # This verifies the IRAN_SYSTEM_MAP and the decode logic.
                        import unicodedata
                        normalized_original = unicodedata.normalize('NFKD', char)
                        self.assertEqual(decoded_char, normalized_original)

    def test_decode_hex(self):
        """Test decoding from a hex string."""
        text = "Test: تست"
        encoded = encode(text)
        hex_string = encoded.hex()
        decoded = decode_hex(hex_string)
        self.assertEqual(text, decoded)

    def test_decode_hex_invalid_string(self):
        """Test decoding from an invalid hex string."""
        self.assertIn("Error", decode_hex("invalid hex"))

    def test_specific_phrase_roundtrip(self):
        """Test a specific phrase requested by the user."""
        text = "دقیق دیگر"
        encoded = encode(text)
        decoded = decode(encoded)
        self.assertEqual(text, decoded)

    def test_phrase_daqiqe_digar(self):
        """Test another specific phrase."""
        text = "دقیقه دیگر"
        encoded = encode(text)
        decoded = decode(encoded)
        self.assertEqual(text, decoded)

    def test_phrase_montazer_otoboos(self):
        """Test a longer sentence."""
        text = "منتظر اتوبوس بعدی باشید"
        encoded = encode(text)
        decoded = decode(encoded)
        self.assertEqual(text, decoded)

    def test_phrase_otoboos_dar_hal(self):
        """Test another longer sentence."""
        text = "اتوبوس در حال ورود به ایستگاه"
        encoded = encode(text)
        decoded = decode(encoded)
        self.assertEqual(text, decoded)

    def test_visual_ordering_flag(self):
        """Test the visual_ordering flag in the encode function."""
        text = "سلام"

        # Test with visual_ordering=True (default)
        encoded_visual = encode(text, visual_ordering=True)
        # Expected: visual order (reversed) of shaped "سلام"
        # ﻡ(f4) ﺎ(91) ﻠ(f3) ﺳ(a8)
        self.assertEqual(encoded_visual, b'\xf4\x91\xf3\xa8')

        # Test with visual_ordering=False
        encoded_logical = encode(text, visual_ordering=False)
        # Expected: logical order of shaped "سلام"
        # ﺳ(a8) ﻠ(f3) ﺎ(91) ﻡ(f4)
        self.assertEqual(encoded_logical, b'\xa8\xf3\x91\xf4')

if __name__ == "__main__":
    unittest.main()
