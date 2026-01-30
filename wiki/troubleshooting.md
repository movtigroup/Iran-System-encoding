# Troubleshooting Guide

## Common Issues

### 1. Incorrect Character Display

**Problem**: Characters don't display correctly after encoding/decoding.

**Solution**: 
- Ensure you're using the correct encoding when displaying the text
- Some applications may need specific font support for Persian characters
- Check that your terminal/editor supports Persian text rendering

### 2. Number Handling Issues

**Problem**: Numbers are not being converted according to locale as expected.

**Solution**:
- The locale detection algorithm analyzes character frequency
- Mixed text with equal Persian and English characters defaults to 'en'
- For consistent behavior, ensure text has clear language dominance

### 3. Round-trip Conversion Problems

**Problem**: Encoding and then decoding doesn't return the original text.

**Solution**:
- Iran System uses visual ordering, which loses some logical information
- Some Unicode sequences may have multiple Iran System representations
- This is inherent to the Iran System encoding design

### 4. Missing Dependencies

**Problem**: Import errors related to `arabic_reshaper` or `python-bidi`.

**Solution**:
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that your Python version is compatible (3.7+)

## Debugging Tips

### Enable Verbose Logging

Add debug information to understand the conversion process:

```python
from iran_encoding import encode, decode, detect_locale

# Debug locale detection
text = "Your text here"
locale = detect_locale(text)
print(f"Text: {repr(text)}")
print(f"Detected locale: {locale}")

# Debug encoding process
encoded = encode(text)
print(f"Encoded bytes: {encoded}")
print(f"Encoded as hex: {encoded.hex()}")

# Debug decoding process
decoded = decode(encoded)
print(f"Decoded text: {repr(decoded)}")
```

### Testing Specific Characters

If you're having issues with specific characters, test them individually:

```python
# Test individual characters
test_chars = ['ا', 'ب', 'پ', 'ت', 'س', 'ش', '۰', '۱', '۲', '0', '1', '2']

for char in test_chars:
    try:
        encoded = encode(char)
        decoded = decode(encoded)
        print(f"'{char}' -> {encoded.hex()} -> '{decoded}' (Match: {char == decoded})")
    except Exception as e:
        print(f"Error with '{char}': {e}")
```

## Performance Issues

### Slow Processing

If encoding/decoding is slow:

- Large texts take more time to process for locale detection
- Consider processing texts in smaller chunks
- Cache results if processing the same texts repeatedly

### Memory Usage

For large files, consider streaming:

```python
def process_large_file(input_path, output_path):
    """Process large files in chunks to manage memory"""
    chunk_size = 1024  # Process in 1KB chunks
    
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'wb') as outfile:
        
        while True:
            chunk = infile.read(chunk_size)
            if not chunk:
                break
                
            encoded_chunk = encode(chunk)
            outfile.write(encoded_chunk)
```

## Platform-Specific Issues

### Windows

- Make sure your console supports UTF-8: `chcp 65001`
- Some older Windows versions may have font rendering issues

### Linux/Mac

- Font support is usually better but may still need Persian fonts installed
- Terminal encoding should be UTF-8

## Testing Your Setup

Verify that everything works correctly:

```python
from iran_encoding import encode, decode, detect_locale

def test_setup():
    print("Testing Iran System Encoding setup...")
    
    # Test basic functionality
    test_text = "سلام"
    encoded = encode(test_text)
    decoded = decode(encoded)
    
    print(f"Original: {test_text}")
    print(f"Encoded: {encoded.hex()}")
    print(f"Decoded: {decoded}")
    print(f"Round-trip successful: {test_text == decoded or test_text in decoded}")
    
    # Test locale detection
    fa_text = "سلام 123"
    en_text = "Hello 123"
    
    print(f"Persian text '{fa_text}' locale: {detect_locale(fa_text)}")
    print(f"English text '{en_text}' locale: {detect_locale(en_text)}")
    
    print("Setup test complete!")

if __name__ == "__main__":
    test_setup()
```

## Getting Help

If you encounter issues not covered here:

1. Check the existing GitHub issues: https://github.com/movtigroup/Iran-System-encoding/issues
2. Run the test suite to confirm basic functionality: `python -m pytest tests/`
3. Create a minimal reproducible example when reporting issues