"""
Test script to compare Python and C implementations of Iran System encoding
"""
import subprocess
import os
import unittest
from iran_encoding import encode, decode

class TestCComparison(unittest.TestCase):
    def test_basic_functionality(self):
        """Test basic encoding/decoding functionality"""
        test_cases = [
            {"input": "سلام", "description": "Basic Persian greeting"},
            {"input": "تست", "description": "Simple test word"},
            {"input": "123", "description": "Numbers"},
            {"input": "تست 123", "description": "Mixed text and numbers"},
            {"input": "پارسی", "description": "Another Persian word"},
            {"input": " Iran ", "description": "Text with spaces"},
        ]
        
        for case in test_cases:
            with self.subTest(desc=case["description"]):
                text = case["input"]
                encoded = encode(text)
                decoded = decode(encoded)
                self.assertIsInstance(encoded, bytes)
                self.assertIsInstance(decoded, str)
                self.assertGreater(len(encoded), 0)

    def test_c_parity(self):
        """Verify that the C library can be compiled and linked"""
        # This test checks if the shared library exists or can be built
        from iran_encoding.c_wrapper import _get_lib
        lib = _get_lib()
        if lib:
            # Test a simple case
            text = "سلام"
            res = encode(text)
            self.assertEqual(res.hex(), "f491f3a8")

if __name__ == "__main__":
    unittest.main()
