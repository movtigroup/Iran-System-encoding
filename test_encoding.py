#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify the Iran System encoding implementation
"""

from iran_encoding import encode, decode

def test_encoding():
    # Test the specific example mentioned: "سلام" should produce F4 91 F3 A8
    text = "سلام"
    encoded = encode(text)
    hex_result = ' '.join([f'{byte:02X}' for byte in encoded])
    print(f"Original Text: {text}")
    print(f"Encoded Result: {encoded}")
    print(f"Hex Code: {hex_result}")
    
    # Expected: F4 91 F3 A8
    expected_hex = "F4 91 F3 A8"
    print(f"Expected: {expected_hex}")
    print(f"Match: {hex_result == expected_hex}")
    
    # Test decoding back
    decoded = decode(encoded)
    print(f"Decoded: {decoded}")
    print(f"Round-trip successful: {decoded == text}")

if __name__ == "__main__":
    test_encoding()