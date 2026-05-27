import pytest
import iran_encoding

def test_pe_at_start():
    """Test 'Pe' at the start of words with leading spaces."""
    text_with_space = " پلیس"
    encoded_with_space = iran_encoding.encode(text_with_space)
    assert encoded_with_space.hex() == "a7fef39520"

def test_user_requested_cases():
    """Test specific words requested by the user."""
    cases = ["پارمیس", "هیپ هاپ", "هیپاپلوجیست", "شاه پالایشگاه"]
    for case in cases:
        res = iran_encoding.encode(case)
        decoded = iran_encoding.decode(res)
        assert decoded == case, f"Failed for word '{case}'"

def test_100_chars():
    """Test a long string of various characters to ensure stability."""
    # Mixing Pe with other characters and spaces
    long_text = "پ" * 50 + " " + "ب" * 50
    res = iran_encoding.encode(long_text)
    decoded = iran_encoding.decode(res)
    assert decoded == long_text

def test_trigger_audit():
    """
    Ensure all Persian characters that should be triggers ARE triggers.
    Any character in UTF8_STR that corresponds to a Persian letter should be a trigger.
    """
    from iran_encoding.core import UTF8_STR, WIDE_CHAR_STR

    def is_trigger(code):
        return (code > 0x8C and code != 0xFF) or code < 0x20 or                code == 0x8E or code == 0x8F or code == 0x81

    for i, code in enumerate(UTF8_STR):
        u_code = WIDE_CHAR_STR[i]
        # If it's a Persian letter (approx range 0x0600-0x06FF)
        if 0x0600 <= u_code <= 0x06FF:
            # Exclude digits as they are handled in chunks
            if not (0x06F0 <= u_code <= 0x06F9):
                assert is_trigger(code), f"Character U+{u_code:04X} (code {hex(code)}) should be an RTL trigger"

if __name__ == "__main__":
    pytest.main([__file__])
