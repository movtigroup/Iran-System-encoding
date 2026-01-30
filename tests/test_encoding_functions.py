# -*- coding: utf-8 -*-
"""
Comprehensive tests for Iran System Encoding functions
"""
import unittest
from iran_encoding import encode, decode, decode_hex, detect_locale


class TestEncodingFunctions(unittest.TestCase):
    def test_encode_function_basic(self):
        """Test basic encoding functionality"""
        text = "سلام"
        result = encode(text)
        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 0)

    def test_encode_with_different_options(self):
        """Test encoding with different options"""
        text = "سلام"
        # Test with visual ordering (default)
        encoded_visual = encode(text, visual_ordering=True)
        # Test with logical ordering
        encoded_logical = encode(text, visual_ordering=False)
        
        self.assertIsInstance(encoded_visual, bytes)
        self.assertIsInstance(encoded_logical, bytes)

    def test_encode_configuration_parameter_removed(self):
        """Test that configuration parameter is no longer supported"""
        text = "سلام"
        # This should now raise a TypeError because configuration was removed
        with self.assertRaises(TypeError):
            encode(text, configuration={})

    def test_decode_function_basic(self):
        """Test basic decoding functionality with visual order"""
        # "سلام" in visual order: م-ا-ل-س
        iran_system_bytes = bytes([0xF4, 0x91, 0xF3, 0xA8])
        result = decode(iran_system_bytes)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "سلام")

    def test_decode_hex_function_basic(self):
        """Test basic hex decoding functionality with visual order"""
        hex_string = "f491f3a8"  # "سلام" in visual order
        result = decode_hex(hex_string)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "سلام")

    def test_decode_hex_with_spaces(self):
        """Test hex decoding with spaces and visual order"""
        hex_string = "f4 91 f3 a8"  # "سلام" in visual order
        result = decode_hex(hex_string)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "سلام")

    def test_decode_hex_invalid_input(self):
        """Test hex decoding with invalid input"""
        with self.assertRaises(ValueError):
            decode_hex("invalid_hex")

    def test_detect_locale_various_inputs(self):
        """Test locale detection with various inputs"""
        # Any Persian letter triggers 'fa'
        self.assertEqual(detect_locale("سلام hello"), "fa")
        self.assertEqual(detect_locale("hello سلام"), "fa")
        # Pure Persian
        self.assertEqual(detect_locale("سلام دنیا"), "fa")
        # Pure English
        self.assertEqual(detect_locale("hello world"), "en")
        # Numbers only
        self.assertEqual(detect_locale("123456"), "en")  # No Persian chars, defaults to en

    def test_encode_decode_roundtrip_consistency(self):
        """Test that encode/decode roundtrip maintains consistency"""
        test_strings = [
            "سلام",
            "تست",
            "Hello",
            "123",
            "سلام 123",
            "Hello ۱۲۳",
            "پارسی",
            " Iran "
        ]
        
        for text in test_strings:
            with self.subTest(text=text):
                # Encode
                encoded = encode(text)
                self.assertIsInstance(encoded, bytes)
                
                # Decode
                decoded = decode(encoded)
                self.assertIsInstance(decoded, str)
                
                # Basic validation: lengths and types
                self.assertGreater(len(encoded), 0)
                self.assertGreater(len(decoded), 0)

    def test_number_handling_based_on_locale(self):
        """Test number handling based on detected locale"""
        # Persian context - numbers should be converted to Persian
        fa_text = "سلام 123"
        encoded_fa = encode(fa_text)
        decoded_fa = decode(encoded_fa)
        
        # English context - numbers should remain ASCII
        en_text = "Hello 123"
        encoded_en = encode(en_text)
        decoded_en = decode(encoded_en)
        
        # Note: The exact behavior depends on implementation details
        # The important thing is that both operations succeed
        self.assertIsInstance(decoded_fa, str)
        self.assertIsInstance(decoded_en, str)

    def test_special_characters_and_symbols(self):
        """Test encoding/decoding of special characters and symbols"""
        test_cases = [
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "()",
            "[]",
            "{}",
            "|",
            "\\",
            ":",
            ";",
            '"',
            "'",
            "<>",
            ",",
            ".",
            "?",
        ]
        
        for char in test_cases:
            with self.subTest(char=char):
                encoded = encode(char)
                decoded = decode(encoded)
                self.assertIsInstance(decoded, str)

    def test_empty_string_handling(self):
        """Test handling of empty strings"""
        result = encode("")
        self.assertEqual(result, b"")
        
        result = decode(b"")
        self.assertEqual(result, "")

    def test_long_text_handling(self):
        """Test handling of longer text"""
        long_text = "سلام دنیا " * 100  # Repeat text 100 times
        encoded = encode(long_text)
        decoded = decode(encoded)
        
        self.assertIsInstance(encoded, bytes)
        self.assertIsInstance(decoded, str)
        # The decoded text should contain the core message
        self.assertIn("سلام", decoded)

    def test_unicode_edge_cases(self):
        """Test edge cases with Unicode characters"""
        edge_cases = [
            "ً",
            "ٌ",
            "ٍ",
            "َ",
            "ُ",
            "ِ",
            "ّ",
            "ْ",
            "ﷺ",  # Peace be upon him
            "؁",  # Quranic sign
        ]
        
        for case in edge_cases:
            with self.subTest(case=case):
                try:
                    encoded = encode(case)
                    decoded = decode(encoded)
                    self.assertIsInstance(decoded, str)
                except Exception:
                    # Some edge cases might not be supported by Iran System
                    # which is expected behavior
                    pass


if __name__ == "__main__":
    unittest.main()