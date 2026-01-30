# -*- coding: utf-8 -*-
"""
Comprehensive test suite for Iran System encoding functions
"""
import unittest
from iran_encoding import encode, decode, decode_hex, unicode_number_to_iransystem, iransystem_to_unicode_number

class TestIranSystemEncodingFunctions(unittest.TestCase):
    
    def test_basic_persian_encoding_decoding(self):
        """Test basic Persian text encoding and decoding"""
        test_cases = [
            "سلام",
            "تست",
            "برنامه",
            "پارسی",
            "خانه"
        ]
        
        for text in test_cases:
            with self.subTest(text=text):
                encoded = encode(text)
                decoded = decode(encoded)
                self.assertEqual(text, decoded)
    
    def test_persian_text_with_numbers(self):
        """Test Persian text mixed with numbers"""
        test_cases = [
            "سلام ۱۲۳",
            "تست 456",
            "عدد ۷۸۹"
        ]
        
        for text in test_cases:
            with self.subTest(text=text):
                encoded = encode(text)
                decoded = decode(encoded)
                self.assertEqual(text, decoded)
    
    def test_unicode_number_conversion(self):
        """Test conversion of Unicode numbers to Iran System numbers"""
        test_cases = [
            ("123", [0x81, 0x82, 0x83]),
            ("0987", [0x80, 0x89, 0x88, 0x87]),
            ("456", [0x84, 0x85, 0x86])
        ]
        
        for unicode_num, expected_bytes in test_cases:
            with self.subTest(unicode_num=unicode_num):
                result = unicode_number_to_iransystem(unicode_num)
                expected = bytes(expected_bytes)
                self.assertEqual(result, expected)
    
    def test_iransystem_number_to_unicode(self):
        """Test conversion of Iran System numbers back to Unicode"""
        test_cases = [
            ([0x81, 0x82, 0x83], "123"),
            ([0x80, 0x89, 0x88, 0x87], "0987"),
            ([0x84, 0x85, 0x86], "456")
        ]
        
        for iran_bytes, expected_unicode in test_cases:
            with self.subTest(iran_bytes=iran_bytes):
                result = iransystem_to_unicode_number(bytes(iran_bytes))
                self.assertEqual(result, expected_unicode)
    
    def test_hex_decoding(self):
        """Test hex string decoding"""
        # Test with a known hex sequence
        hex_str = "818283"  # Iran System representation of 123
        result = decode_hex(hex_str)
        # The result depends on the exact Iran System mapping
        self.assertIsInstance(result, str)
        
        # Test invalid hex string
        invalid_result = decode_hex("invalid")
        self.assertIn("Error", invalid_result)
    
    def test_empty_string_handling(self):
        """Test handling of empty strings"""
        self.assertEqual(encode(""), b"")
        self.assertEqual(decode(b""), "")
        self.assertEqual(decode_hex(""), "Error: Invalid hex string")
        self.assertEqual(decode_hex("invalid"), "Error: Invalid hex string")
    
    def test_special_characters(self):
        """Test encoding/decoding of special characters and punctuation"""
        test_cases = [
            "!",
            "?",
            "،",
            "؟",
            ".",
            ",",
            ";",
            ":"
        ]
        
        for char in test_cases:
            with self.subTest(char=char):
                encoded = encode(char)
                decoded = decode(encoded)
                self.assertEqual(char, decoded)
    
    def test_english_text(self):
        """Test encoding/decoding of English text"""
        test_cases = [
            "Hello",
            "World",
            "Test123",
            "ABC abc 123"
        ]
        
        for text in test_cases:
            with self.subTest(text=text):
                encoded = encode(text)
                decoded = decode(encoded)
                self.assertEqual(text, decoded)
    
    def test_persian_numbers_roundtrip(self):
        """Test roundtrip conversion with Persian numbers"""
        persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
        encoded = encode(persian_numbers)
        decoded = decode(encoded)
        self.assertEqual(persian_numbers, decoded)

    def test_complex_sentences(self):
        """Test encoding/decoding of complex sentences"""
        sentences = [
            "سلام دنیا",
            "این یک تست است",
            "عدد ۱۲۳ مهم است"
        ]
        
        for sentence in sentences:
            with self.subTest(sentence=sentence):
                encoded = encode(sentence)
                decoded = decode(encoded)
                self.assertEqual(sentence, decoded)

    def test_visual_ordering_consistency(self):
        """Test that visual ordering maintains consistency"""
        text = "سلام"
        encoded = encode(text, visual_ordering=True)
        decoded = decode(encoded)
        self.assertEqual(text, decoded)

    def test_encode_decode_roundtrip(self):
        """Test that encode/decode roundtrip preserves original text"""
        test_cases = [
            "سلام",
            "Hello",
            "123",
            "تست 123",
            "متن فارسی",
            "Mixed English and فارسی"
        ]
        
        for text in test_cases:
            with self.subTest(text=text):
                encoded = encode(text)
                decoded = decode(encoded)
                self.assertEqual(text, decoded)

if __name__ == '__main__':
    unittest.main()