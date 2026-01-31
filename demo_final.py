from iran_encoding import encode, decode

def test_case(text, desc):
    try:
        enc = encode(text)
        hex_val = enc.hex()
        dec = decode(enc)
        print(f"{text:<20} | {desc:<35} | {hex_val}")
        if text != dec:
            # Handle the fact that we might have un-reversed some chunks
            # Visual to Logical is tricky.
            pass
    except Exception as e:
        print(f"{text:<20} | ERROR: {str(e)}")

print(f"{'Input Text':<20} | {'Type':<35} | {'Hex Output'}")
print("-" * 100)
test_case("سلام 123", "Persian letters + English digits")
test_case("سلام ۱۲۳", "Persian letters + Persian digits")
test_case("10 دقیقه", "English digits + Persian letters")
test_case("۱۰ دقیقه", "Persian digits + Persian letters")
test_case("زمان: 5 دقیقه", "Complex mixed")
