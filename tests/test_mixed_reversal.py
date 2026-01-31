import unittest
from iran_encoding import encode, decode

class TestMixedReversal(unittest.TestCase):
    def test_hi_salam(self):
        # "hi سلام" -> Global RTL: "سلام hi"
        expected_hex = "f491f3a8206869"
        result = encode("hi سلام")
        self.assertEqual(result.hex(), expected_hex)
        self.assertEqual(decode(result), "hi سلام")

    def test_salam_123_english_input(self):
        # "سلام 123" -> Global RTL: "123 سلام" (123 as LTR)
        expected_hex = "81828320f491f3a8"
        result = encode("سلام 123")
        self.assertEqual(result.hex(), expected_hex)

    def test_salam_123_persian_input(self):
        # "سلام ۱۲۳" -> Global RTL: "۳۲۱ سلام" (۱۲۳ as RTL per user rule)
        expected_hex = "83828120f491f3a8"
        result = encode("سلام ۱۲۳")
        self.assertEqual(result.hex(), expected_hex)

    def test_complex_mixed(self):
        # "123 hi سلام 456" -> "456 سلام hi 123"
        expected_hex = "84858620f491f3a820686920818283"
        result = encode("123 hi سلام 456")
        self.assertEqual(result.hex(), expected_hex)
