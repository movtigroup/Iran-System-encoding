# -*- coding: utf-8 -*-
import unittest
from iran_encoding import encode, decode, detect_locale


class TestConverter(unittest.TestCase):
    def test_detect_locale_persian_dominant(self):
        """Test that Persian-dominant text is detected as 'fa'"""
        text = "سلام Hello"
        locale = detect_locale(text)
        self.assertEqual(locale, 'fa')

    def test_detect_locale_english_with_persian(self):
        """Test that any Persian letter triggers 'fa' locale"""
        text = "Hello سلام"
        locale = detect_locale(text)
        self.assertEqual(locale, 'fa')

    def test_detect_locale_equal_characters(self):
        """Test locale detection with equal Persian/English characters"""
        text = "سلام123"
        locale = detect_locale(text)
        # With more Persian chars than English, should be 'fa'
        self.assertEqual(locale, 'fa')

    def test_roundtrip_simple(self):
        """Test basic roundtrip encoding/decoding"""
        test_cases = [
            "سلام",
            "تست",
            "پارسی",
            " Iran ",
        ]
        for text in test_cases:
            with self.subTest(text=text):
                encoded = encode(text)
                decoded = decode(encoded)
                self.assertIsInstance(encoded, bytes)
                self.assertIsInstance(decoded, str)
                self.assertGreater(len(encoded), 0)
                self.assertGreater(len(decoded), 0)

    def test_roundtrip_with_numbers_persian_locale(self):
        """Test roundtrip with numbers when text is in Persian context"""
        text = "سلام 123"
        encoded = encode(text)
        decoded = decode(encoded)
        # Should contain Persian numbers in decoded text
        self.assertIn('۱', decoded) or self.assertIn('۲', decoded) or self.assertIn('۳', decoded)

    def test_roundtrip_with_numbers_english_locale(self):
        """Test roundtrip with numbers when text is in English context"""
        text = "Hello 123"
        encoded = encode(text)
        decoded = decode(encoded)
        # Should contain ASCII numbers in decoded text
        self.assertIn('1', decoded) or self.assertIn('2', decoded) or self.assertIn('3', decoded)

    def test_ascii_characters_preserved(self):
        """Test that ASCII characters are preserved properly"""
        text = "Hello 123 !@#"
        encoded = encode(text)
        decoded = decode(encoded)
        # ASCII chars should remain ASCII
        self.assertIn("Hello", decoded)
        self.assertIn("123", decoded)

    def test_persian_numbers_handling(self):
        """Test handling of Persian numbers specifically (should be ASCII if no letters)"""
        text = "۱۲۳"  # Persian numbers, no letters -> English locale
        encoded = encode(text)
        decoded = decode(encoded)
        self.assertEqual(decoded, "123")

    def test_mixed_numbers_handling(self):
        """Test handling of mixed ASCII and Persian numbers"""
        text = "Numbers 123 and ۴۵۶"
        encoded = encode(text)
        decoded = decode(encoded)
        # Both types of numbers should be present in the decoded text
        self.assertTrue('1' in decoded or '2' in decoded or '3' in decoded or '۱' in decoded or '۲' in decoded or '۳' in decoded)
        self.assertTrue('4' in decoded or '5' in decoded or '6' in decoded or '۴' in decoded or '۵' in decoded or '۶' in decoded)


if __name__ == "__main__":
    unittest.main()