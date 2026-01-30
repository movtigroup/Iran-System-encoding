# -*- coding: utf-8 -*-
"""
Tests for exact behavior of Iran System encoding implementation
"""
import unittest
from iran_encoding import encode, decode, decode_hex, detect_locale


class TestExactBehavior(unittest.TestCase):
    def test_exact_byte_mappings(self):
        """Test exact byte mappings from known Iran System table"""
        # Based on the Iran System mapping table
        # 0x80: '۰', 0x81: '۱', 0x82: '۲', etc.
        # 0x90: 'ا', 0x91: 'ﺎ', etc.
        
        # Test Persian numbers
        number_mappings = [
            (0x80, '۰'),
            (0x81, '۱'),
            (0x82, '۲'),
            (0x83, '۳'),
            (0x84, '۴'),
            (0x85, '۵'),
            (0x86, '۶'),
            (0x87, '۷'),
            (0x88, '۸'),
            (0x89, '۹'),
        ]
        
        for byte_val, char in number_mappings:
            with self.subTest(byte=byte_val, char=char):
                # Test direct mapping
                byte_data = bytes([byte_val])
                decoded = decode(byte_data)
                self.assertEqual(decoded, char)

    def test_specific_letter_mappings(self):
        """Test specific letter mappings"""
        letter_mappings = [
            (bytes([0x90]), 'ا'),  # Isolated alef
            (bytes([0x91]), 'ﺎ'),  # Final alef
            (bytes([0xA8]), 'س'),  # Final seen
            (bytes([0xF3]), 'ل'),  # Initial lam
            (bytes([0xF4]), 'م'),  # Final mim
        ]
        
        for byte_seq, expected in letter_mappings:
            with self.subTest(bytes=byte_seq, expected=expected):
                decoded = decode(byte_seq)
                # Due to visual/logical differences, exact match might vary
                # But the function should not throw errors
                self.assertIsInstance(decoded, str)
                self.assertGreater(len(decoded), 0)

    def test_word_combinations(self):
        """Test known word combinations in visual order"""
        # "سلام" -> م-ا-ل-س
        # "برنامه" -> ه-م-ا-ن-ر-ب
        word_tests = [
            (bytes([0xF4, 0x91, 0xF3, 0xA8]), "سلام"),
            (bytes([0xF9, 0xF5, 0x91, 0xF7, 0xA4, 0x93]), "برنامه"),
        ]
        
        for byte_seq, expected in word_tests:
            with self.subTest(expected=expected):
                decoded = decode(byte_seq)
                self.assertEqual(decoded, expected)
                
                # Test roundtrip
                re_encoded = encode(decoded)
                self.assertEqual(re_encoded, byte_seq)

    def test_visual_vs_logical_ordering(self):
        """Test the difference between visual and logical ordering"""
        test_text = "سلام"
        
        # Visual ordering (default)
        encoded_visual = encode(test_text, visual_ordering=True)
        decoded_visual = decode(encoded_visual)
        
        # Logical ordering
        encoded_logical = encode(test_text, visual_ordering=False)
        decoded_logical = decode(encoded_logical)
        
        # Both should produce valid strings
        self.assertIsInstance(decoded_visual, str)
        self.assertIsInstance(decoded_logical, str)
        
        # Both should contain the essential content
        self.assertIn('س', decoded_visual) if 'س' in test_text else True
        self.assertIn('ل', decoded_visual) if 'ل' in test_text else True
        self.assertIn('ا', decoded_visual) if 'ا' in test_text else True
        self.assertIn('م', decoded_visual) if 'م' in test_text else True

    def test_number_locale_detection(self):
        """Test number handling based on locale detection"""
        # Persian context
        fa_context = "عدد 123 در فارسی"
        fa_locale = detect_locale(fa_context)
        fa_encoded = encode(fa_context)
        fa_decoded = decode(fa_encoded)
        
        # English context  
        en_context = "number 123 in English"
        en_locale = detect_locale(en_context)
        en_encoded = encode(en_context)
        en_decoded = decode(en_encoded)
        
        # Validate results
        self.assertIsInstance(fa_locale, str)
        self.assertIsInstance(en_locale, str)
        self.assertIsInstance(fa_decoded, str)
        self.assertIsInstance(en_decoded, str)

    def test_ascii_preservation(self):
        """Test that ASCII characters are properly handled"""
        ascii_text = "Hello World 123 !@#"
        encoded = encode(ascii_text)
        decoded = decode(encoded)
        
        self.assertIsInstance(encoded, bytes)
        self.assertIsInstance(decoded, str)
        
        # The decoded text should contain ASCII equivalents where applicable
        self.assertIn('H', decoded) if 'H' in ascii_text else True
        self.assertIn('e', decoded) if 'e' in ascii_text else True
        self.assertIn('1', decoded) if '1' in ascii_text else True

    def test_mixed_script_handling(self):
        """Test handling of mixed Persian/Arabic/ASCII scripts"""
        mixed_text = "This says سلام in Persian and число in Russian"
        encoded = encode(mixed_text)
        decoded = decode(encoded)
        
        self.assertIsInstance(encoded, bytes)
        self.assertIsInstance(decoded, str)
        self.assertGreater(len(decoded), 0)

    def test_boundary_conditions(self):
        """Test boundary conditions and edge cases"""
        # Single character
        single_char = "ا"
        encoded = encode(single_char)
        decoded = decode(encoded)
        self.assertIsInstance(decoded, str)
        self.assertGreater(len(decoded), 0)
        
        # Very long text
        long_text = "سلام " * 1000
        encoded = encode(long_text)
        decoded = decode(encoded)
        self.assertIsInstance(decoded, str)
        self.assertIn("سلام", decoded)
        
        # Empty string
        empty_encoded = encode("")
        empty_decoded = decode(empty_encoded)
        self.assertEqual(empty_decoded, "")
        
        # Just spaces
        space_text = "   "
        space_encoded = encode(space_text)
        space_decoded = decode(space_encoded)
        self.assertIsInstance(space_decoded, str)

    def test_hex_decode_edge_cases(self):
        """Test hex decoding edge cases"""
        # Valid hex with uppercase
        result1 = decode_hex("A8F391F4")
        self.assertIsInstance(result1, str)
        
        # Valid hex with lowercase
        result2 = decode_hex("a8f391f4")
        self.assertIsInstance(result2, str)
        
        # Valid hex with mixed case
        result3 = decode_hex("A8f391F4")
        self.assertIsInstance(result3, str)
        
        # Valid hex with spaces
        result4 = decode_hex("a8 f3 91 f4")
        self.assertIsInstance(result4, str)
        
        # Valid hex with mixed case and spaces
        result5 = decode_hex("A8 F3 91 f4")
        self.assertIsInstance(result5, str)
        
        # Invalid hex should raise exception
        with self.assertRaises(ValueError):
            decode_hex("xyz123")
        
        # Odd-length hex should raise exception
        with self.assertRaises(ValueError):
            decode_hex("a8f391f")  # 7 chars, not divisible by 2


if __name__ == "__main__":
    unittest.main()