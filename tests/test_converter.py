# -*- coding: utf-8 -*-
import unittest
from iran_encoding import encode, decode

class TestConverter(unittest.TestCase):
    def test_roundtrip(self):
        test_cases = [
            {"name": "Basic word 'سلام'", "bytes": bytes([0xA8, 0xF3, 0x91, 0xF4]), "expected": "سلام"},
            {"name": "Word with right-joining 'برنامه'", "bytes": bytes([0x93,0xA4,0xF7,0x91,0xF5,0xF9]), "expected": "برنامه"},
            {"name": "Key ZWNJ case 'خانه‌ها'", "bytes": bytes([0xA1, 0x91, 0xF7, 0xF9, 0xFB, 0x91]), "expected": "خانه‌ها"},
            {"name": "Ezafe construct 'خانه‌ی'", "bytes": bytes([0xA1, 0x91, 0xF7, 0xF9, 0xFE]), "expected": "خانه‌ی"},
            {"name": "Numbers do not join '۱۲۳'", "bytes": bytes([0x81,0x82,0x83]), "expected": "۱۲۳"},
            {"name": "Ligature 'طلا'", "bytes": bytes([0xAF, 0xF2]), "expected": "طلا"},
            {"name": "Box drawing '┌─┐'", "bytes": bytes([0xDA, 0xC4, 0xBF]), "expected": "┌─┐"},
        ]
        for test in test_cases:
            with self.subTest(msg=test["name"]):
                decoded = decode(test["bytes"])
                self.assertEqual(decoded, test["expected"])
                # We can't guarantee byte-perfect roundtrip because of visual ambiguity
                # but we can check for logical consistency
                encoded = encode(decoded)
                reddecoded = decode(encoded)
                self.assertEqual(decoded, reddecoded)

if __name__ == "__main__":
    unittest.main()
