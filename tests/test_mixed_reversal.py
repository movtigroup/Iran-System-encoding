# -*- coding: utf-8 -*-
import unittest
from iran_encoding import encode, decode

class TestMixedReversal(unittest.TestCase):
    def test_hi_salam(self):
        # "hi سلام"
        # hi (logical ASCII) + سلام (reversed)
        # "سلام" -> f4 91 f3 a8
        # "hi " -> 68 69 20
        expected_hex = "686920f491f3a8"
        result = encode("hi سلام")
        self.assertEqual(result.hex(), expected_hex)

        # Test decode
        decoded = decode(result)
        self.assertEqual(decoded, "hi سلام")

    def test_salam_123_english_input(self):
        # "سلام 123" (English digits input)
        # In Persian context, ASCII digits are converted to Iran System digits (81 82 83)
        # "سلام" (reversed: f4 91 f3 a8) + " " (20) + "123" -> (81 82 83)
        expected_hex = "f491f3a820818283"
        result = encode("سلام 123")
        self.assertEqual(result.hex(), expected_hex)

        # Test decode - returns Persian digits in Persian context
        decoded = decode(result)
        self.assertEqual(decoded, "سلام ۱۲۳")

    def test_salam_123_persian_input(self):
        # "سلام ۱۲۳" (Persian digits input)
        # "سلام" (reversed: f4 91 f3 a8) + " " (20) + "۱۲۳" (81 82 83)
        expected_hex = "f491f3a820818283"
        result = encode("سلام ۱۲۳")
        self.assertEqual(result.hex(), expected_hex)

        # Test decode
        decoded = decode(result)
        self.assertEqual(decoded, "سلام ۱۲۳")

    def test_complex_mixed(self):
        # "123 hi سلام 456"
        # Mixed: 123 (81 82 83) + hi (68 69 20) + سلام (f4 91 f3 a8) + 456 (20 84 85 86)
        expected_hex = "81828320686920f491f3a820848586"
        result = encode("123 hi سلام 456")
        self.assertEqual(result.hex(), expected_hex)

        # Test decode
        decoded = decode(result)
        self.assertEqual(decoded, "۱۲۳ hi سلام ۴۵۶")

if __name__ == "__main__":
    unittest.main()
