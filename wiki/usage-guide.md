# Usage Guide

## Quick Start

### Installation

```bash
pip install iran-encoding
```

### Basic Encoding/Decoding

```python
from iran_encoding import encode, decode

# Encode Persian text
text = "سلام دنیا"
encoded_bytes = encode(text)
print(f"Encoded (hex): {encoded_bytes.hex()}")

# Decode back to text
decoded_text = decode(encoded_bytes)
print(f"Decoded: {decoded_text}")
```

## Locale Detection

The library automatically detects whether your text is primarily Persian or English and handles numbers accordingly:

```python
from iran_encoding import encode, detect_locale

# Persian-dominant text
fa_text = "سلام 123"  # Contains Persian and numbers
locale = detect_locale(fa_text)
print(f"Detected locale: {locale}")  # Output: 'fa'

encoded = encode(fa_text)
# Numbers '123' will be converted to Persian numerals '۱۲۳'

# English-dominant text
en_text = "Hello 123"  # Contains English and numbers
locale = detect_locale(en_text)
print(f"Detected locale: {locale}")  # Output: 'en'

encoded = encode(en_text)
# Numbers '123' will remain as ASCII
```

## Advanced Options

### Visual vs Logical Ordering

By default, the encoder uses visual ordering which is typical for Iran System:

```python
# Visual ordering (default)
encoded_visual = encode("سلام", visual_ordering=True)

# Logical ordering (for specific use cases)
encoded_logical = encode("سلام", visual_ordering=False)
```

### Custom Configuration

You can pass additional configuration to the Arabic reshaper:

```python
config = {
    # Custom reshaping options can be passed here
}

encoded = encode("سلام دنیا", configuration=config)
```

## Command-Line Interface

The package includes a command-line interface for easy usage:

### Encoding

```bash
# Encode text to Iran System hex
iran-encoding encode "سلام دنیا"

# Encode with logical ordering
iran-encoding encode --logical "سلام دنیا"

# Encode with custom configuration (JSON format)
iran-encoding encode --config '{"rtl_shaping_type": "general"}' "سلام دنیا"
```

### Decoding

```bash
# Decode hex string to text
iran-encoding decode-hex "a8f391f4"

# Decode byte string to text
iran-encoding decode "b'\\xa8\\xf3\\x91\\xf4'"
```

## Integration Examples

### Web Application Integration

```python
from flask import Flask, request, jsonify
from iran_encoding import encode, decode

app = Flask(__name__)

@app.route('/encode', methods=['POST'])
def api_encode():
    data = request.json
    text = data.get('text', '')
    encoded = encode(text)
    return jsonify({
        'input': text,
        'encoded': encoded.hex(),
        'encoded_bytes': list(encoded)
    })

@app.route('/decode', methods=['POST'])
def api_decode():
    data = request.json
    hex_string = data.get('hex', '')
    try:
        decoded = decode(bytes.fromhex(hex_string))
        return jsonify({
            'hex': hex_string,
            'decoded': decoded
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
```

### File Processing

```python
def process_text_file(input_file, output_file):
    """Convert text file from Unicode to Iran System encoding"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    encoded_bytes = encode(content)
    
    with open(output_file, 'wb') as f:
        f.write(encoded_bytes)

def read_iran_system_file(file_path):
    """Read Iran System encoded file and convert to Unicode"""
    with open(file_path, 'rb') as f:
        iran_system_bytes = f.read()
    
    decoded_text = decode(iran_system_bytes)
    return decoded_text
```

## Error Handling

```python
from iran_encoding import encode, decode

try:
    # Attempt to encode text
    encoded = encode("نمونه متن")
    decoded = decode(encoded)
    print(f"Success: {decoded}")
except Exception as e:
    print(f"Encoding/decoding failed: {e}")

# Safe hex decoding
def safe_decode_hex(hex_string):
    try:
        return decode_hex(hex_string)
    except ValueError as e:
        print(f"Invalid hex string: {e}")
        return None
```

## Performance Tips

- Cache encoder/decoder instances if processing many texts
- Use batch processing when converting multiple files
- Consider locale detection overhead when processing large texts frequently