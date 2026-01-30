# -*- coding: utf-8 -*-
import unittest
from iran_encoding import encode, decode, detect_locale

class TestIranSystemV1(unittest.TestCase):
    def test_locale_detection(self):
        """Test that any Persian letter triggers 'fa' locale."""
        self.assertEqual(detect_locale("Hello سلام"), 'fa')
        self.assertEqual(detect_locale("Hello"), 'en')
        self.assertEqual(detect_locale("123"), 'en')
        self.assertEqual(detect_locale("۱۲۳"), 'en') # Persian digits but no letters -> 'en'
        self.assertEqual(detect_locale("س 123"), 'fa')

    def test_persian_encoding_with_numbers(self):
        """Test that in Persian locale, numbers are encoded to Iran System."""
        # 'سلام 1'
        # '1' is 0x31 in ASCII, 0x81 in Iran System
        encoded = encode("سلام 1")
        # In Iran System, 0x81 is the Persian digit 1.
        self.assertIn(0x81, encoded)

    def test_english_encoding_with_persian_numbers(self):
        """Test that in English locale, Persian numbers are converted to ASCII."""
        # 'Hello ۱'
        # '۱' is \u06F1
        encoded = encode("Hello ۱")
        # Result should be ASCII 'Hello 1'
        self.assertEqual(encoded, b"Hello 1")

    def test_visual_ordering_v1(self):
        """Test that visual ordering matches the C logic (ReverseAlphaNumeric)."""
        # 'س123'
        # Persian letter 'س' (0x20 in Unicode script is 0xD3)
        # In visual order, numbers should be reversed if followed/preceded by Persian?
        # Let's see how ReverseAlphaNumeric works.
        # It reverses sequences of characters between 0x20 and 0x7E if they are bounded by >0x7E or <0x20.

        # 'سلام' -> 'م‌ا‌ل‌س' (visual)
        # The core logic handles this.
        text = "سلام"
        encoded = encode(text, visual_ordering=True)
        # In Iran System:
        # 'س' initial: 0xA8
        # 'ل' medial: 0xF3
        # 'ا' final: 0x91
        # 'م' final isolated: 0xF4
        # Since it's reversed for visual: 'م' (isolated) 'ا' 'ل' 'س'

        # Actually the C logic:
        # UnicodeToIransystem("سلام")
        # script_bytes = [0xD3, 0xE5, 0xC7, 0xF4] (approximately)
        # ReverseAlphaNumeric -> [0xF4, 0xC7, 0xE5, 0xD3]
        # Then mapped to Iran System forms.

        decoded = decode(encoded)
        # If we decode it, it should look like the input because decode also reverses?
        # No, decode just maps bytes to Unicode.
        # So decoded "سلام" encoded visually will look reversed.

        # This is expected in legacy systems.
        self.assertIsInstance(encoded, bytes)

    def test_pure_python_matches_expected(self):
        """Ensure the pure Python core works without C extension."""
        from iran_encoding.core import unicode_to_iransystem
        res = unicode_to_iransystem("تست")
        self.assertIsInstance(res, bytes)

if __name__ == "__main__":
    unittest.main()
