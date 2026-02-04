# -*- coding: utf-8 -*-
from iran_encoding import encode, decode, detect_locale

def demo():
    test_cases = [
        "سلام",
        "hi سلام",
        "سلام 123",
        "hi سلام 123"
    ]

    print(f"{'Input Text':<20} | {'Locale':<6} | {'Hex Output':<30} | {'Decoded'}")
    print("-" * 80)

    for text in test_cases:
        locale = detect_locale(text)
        encoded = encode(text)
        decoded = decode(encoded)
        print(f"{text:<20} | {locale:<6} | {encoded.hex():<30} | {decoded}")

if __name__ == "__main__":
    demo()
