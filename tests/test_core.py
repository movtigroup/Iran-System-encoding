import pytest
from iran_encoding.core import IranSystemEncoder
from iran_encoding.exceptions import EncodingError, DecodeError

def test_basic_roundtrip():
    """Test basic encoding and decoding of a simple string."""
    encoder = IranSystemEncoder()
    original = "سلام دنیا"
    encoded = encoder.encode(original)
    decoded = encoder.decode(encoded)
    assert decoded == original

def test_english_roundtrip():
    """Test encoding and decoding of a pure English string."""
    encoder = IranSystemEncoder()
    original = "Hello, World! 123"
    encoded = encoder.encode(original)
    decoded = encoder.decode(encoded)
    assert decoded == original

def test_mixed_string_roundtrip():
    """Test a mixed Persian/English string."""
    encoder = IranSystemEncoder()
    original = "این یک تست است: Test 123"
    encoded = encoder.encode(original)
    decoded = encoder.decode(encoded)
    assert decoded == original

def test_visual_ordering_option():
    """Test the visual_ordering option."""
    encoder_visual = IranSystemEncoder(visual_ordering=True)
    encoder_logical = IranSystemEncoder(visual_ordering=False)
    text = "سلام"

    # This is a simplified check. The exact bytes depend on the shaping.
    # A logical encoder should produce different output than a visual one.
    assert encoder_visual.encode(text) != encoder_logical.encode(text)

def test_unsupported_character_error():
    """Test that an unsupported character raises EncodingError without a fallback."""
    encoder = IranSystemEncoder(fallback_char=None)
    with pytest.raises(EncodingError):
        encoder.encode("This contains an unsupported character: €")

def test_unsupported_character_fallback():
    """Test that an unsupported character uses the fallback character if provided."""
    encoder = IranSystemEncoder(fallback_char='?')
    text = "Unsupported: €"
    encoded = encoder.encode(text)
    # The exact decoding is complex, but it should not raise an error.
    assert '?' in encoder.decode(encoded)

def test_invalid_decode_bytes():
    """Test that invalid bytes raise DecodeError."""
    encoder = IranSystemEncoder()
    # 0xFF is not a valid byte in the simplified map in core.py
    invalid_bytes = b'\x48\x65\x6c\x6c\x6f\xff'
    with pytest.raises(DecodeError):
        encoder.decode(invalid_bytes)

def test_caching():
    """Test that the encoding/decoding cache works."""
    encoder = IranSystemEncoder(cache_enabled=True)
    text = "تست کش"

    # First call, should populate the cache
    encoded = encoder.encode(text)
    decoded = encoder.decode(encoded)

    # Check if the values are in the cache
    assert text in encoder._encode_cache
    assert encoded in encoder._decode_cache

    # Subsequent calls should return the cached values
    assert encoder.encode(text) is encoded
    assert encoder.decode(encoded) is decoded
