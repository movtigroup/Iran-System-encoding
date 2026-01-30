#!/usr/bin/env python3
"""
Demo script showing Iran System encoding functionality
"""

from iran_encoding import encode, decode, unicode_number_to_iransystem, iransystem_to_unicode_number

def main():
    print("Iran System Encoding Library Demo")
    print("=" * 50)
    
    # Basic encoding/decoding
    print("\n1. Basic Persian text encoding/decoding:")
    texts = ["سلام", "تست", "برنامه", "پارسی"]
    
    for text in texts:
        encoded = encode(text)
        decoded = decode(encoded)
        print(f"   Original: {text}")
        print(f"   Encoded (hex): {encoded.hex()}")
        print(f"   Decoded: {decoded}")
        print(f"   Match: {text == decoded}")
        print()
    
    # Number encoding
    print("2. Number encoding/decoding:")
    numbers = ["123", "۴۵۶", "0987"]
    
    for num in numbers:
        encoded = unicode_number_to_iransystem(num)
        decoded = iransystem_to_unicode_number(encoded)
        print(f"   Original: {num}")
        print(f"   Encoded (hex): {encoded.hex()}")
        print(f"   Decoded: {decoded}")
        print(f"   Match: {num == decoded}")
        print()
    
    # Mixed text
    print("3. Mixed text encoding/decoding:")
    mixed_texts = ["سلام 123", "تست ABC", "عدد ۴۵۶"]
    
    for text in mixed_texts:
        encoded = encode(text)
        decoded = decode(encoded)
        print(f"   Original: {text}")
        print(f"   Encoded (hex): {encoded.hex()}")
        print(f"   Decoded: {decoded}")
        print(f"   Match: {text == decoded}")
        print()
    
    # Hex decoding
    print("4. Hex string decoding:")
    hex_examples = ["f491f3a8", "a8f391f4"]  # These are sample hex values
    
    for hex_str in hex_examples:
        decoded = decode_hex_from_lib(hex_str)
        print(f"   Hex: {hex_str}")
        print(f"   Decoded: {decoded}")
        print()
    
    print("Demo completed successfully!")

def decode_hex_from_lib(hex_string):
    """Helper function to decode hex string using the library"""
    from iran_encoding import decode_hex
    return decode_hex(hex_string)

if __name__ == "__main__":
    main()