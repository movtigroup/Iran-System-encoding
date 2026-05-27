import pytest
import iran_encoding

def test_pe_at_start():
    """
    Test that 'Pe' at the start of a word (possibly after a space)
    is correctly handled by visual ordering.
    """
    text = "پلیس"
    encoded = iran_encoding.encode(text)
    # encoded:
    # 'پلیس' (logical)
    # script: 81 e1 ed d3
    # reverse_alpha_numeric (if 81 is trigger): d3 ed e1 81
    # unicode_to_iransystem logic (reshaping):
    # d3 -> isolated sin (a7)
    # ed -> medial ye (fe)
    # e1 -> medial lam (f3)
    # 81 -> initial pe (95)
    # result: a7 fe f3 95
    # final reversal: 95 f3 fe a7

    # Wait, my reproduce_bug.py showed:
    # Text: 'پلیس'
    # Hex:  a7 fe f3 95
    # Decoded: 'پلیس'

    # Let's check " پلیس" (space + پلیس)
    text_with_space = " پلیس"
    encoded_with_space = iran_encoding.encode(text_with_space)
    # Currently: a7 fe f3 20 94
    # Expected: 95 f3 fe a7 20

    print(f"\nHex for ' پلیس': {encoded_with_space.hex(' ')}")

    # If it's correctly ordered, ' ' (20) should be at the end (left-most in visual)
    # or start depending on how we define it, but it should NOT be in the middle of the word.

    # In Iran System, visual 95 f3 fe a7 20 means " پلیس"
    # Current output a7 fe f3 20 94 means " پ لیس" (because 20 interrupted the word)

    assert encoded_with_space.endswith(b'\x20') or encoded_with_space.startswith(b'\x20')
    # Actually, visual RTL means if Unicode is " پلیس",
    # visual order should be "س ی ل پ "
    # Hex: a7 fe f3 95 20

    assert encoded_with_space.hex() == "a7fef39520"

def test_pe_vs_be():
    """Compare 'Pe' behavior with 'Be' which works."""
    be_text = " بلیس"
    pe_text = " پلیس"

    be_encoded = iran_encoding.encode(be_text)
    pe_encoded = iran_encoding.encode(pe_text)

    # be_encoded should be a7 fe f3 93 20
    # pe_encoded should be a7 fe f3 95 20

    assert be_encoded.endswith(b'\x20')
    assert pe_encoded.endswith(b'\x20'), f"Pe encoded as {pe_encoded.hex()} should end with space"

if __name__ == "__main__":
    pytest.main([__file__])
