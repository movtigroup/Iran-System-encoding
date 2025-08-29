from iran_encoding import IranSystemEncoder

# Create encoder instance
encoder = IranSystemEncoder(
    visual_ordering=True,
    fallback_char='?',
    cache_enabled=True
)

# Basic encoding
text = "سلام دنیا"
encoded = encoder.encode(text)
decoded = encoder.decode(encoded)

print(f"Original text: {text}")
print(f"Encoded (hex): {encoded.hex()}")
print(f"Decoded text: {decoded}")

assert decoded == text
print("\nRoundtrip successful!")
