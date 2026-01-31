# -*- coding: utf-8 -*-
import unittest
from iran_encoding import encode, decode

class TestMixedReversal(unittest.TestCase):
    def test_hi_salam(self):
        # "hi سلام"
        # Logical: "hi سلام"
        # Global RTL: "سلام hi"
        # "سلام" -> f4 91 f3 a8
        # "hi " -> 68 69 20
        expected_hex = "f491f3a8206869"
        result = encode("hi سلام")
        self.assertEqual(result.hex(), expected_hex)

        # Test decode
        decoded = decode(result)
        self.assertEqual(decoded, "hi سلام")

    def test_salam_123_english_input(self):
        # "سلام 123" (English digits input)
        # Global RTL: "123 سلام"
        # "123" -> 81 82 83 (converted to Persian digits in Persian context)
        # "سلام" -> f4 91 f3 a8
        expected_hex = "81828320f491f3a8"
        result = encode("سلام 123")
        self.assertEqual(result.hex(), expected_hex)

        # Test decode
        decoded = decode(result)
        self.assertEqual(decoded, "سلام ۱۲۳")

    def test_salam_123_persian_input(self):
        # "سلام ۱۲۳" (Persian digits input)
        # Global RTL: "۱۲۳ سلام"
        expected_hex = "81828320f491f3a8"
        result = encode("سلام ۱۲۳")
        self.assertEqual(result.hex(), expected_hex)

        # Test decode
        decoded = decode(result)
        self.assertEqual(decoded, "سلام ۱۲۳")

    def test_complex_mixed(self):
        # "123 hi سلام 456"
        # Reverse: "654 malas ih 321"
        # Fix: "456 malas hi 123"
        # 456 (84 85 86) + " " (20) + malas (f4 91 f3 a8) + " " (20) + hi (68 69 20) + 123 (81 82 83)
        expected_hex = "84858620f491f3a820686920818283"
        result = encode("123 hi سلام 456")
        self.assertEqual(result.hex(), expected_hex)

        # Test decode
        decoded = decode(result)
        self.assertEqual(decoded, "۱۲۳ hi سلام ۴۵۶")

if __name__ == "__main__":
    unittest.main()
