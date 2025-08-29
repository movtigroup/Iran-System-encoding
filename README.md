# Iran System Encoding Library

A Python library for Iran System character encoding, supporting multiple languages, advanced date utilities, and cross-platform bindings.

## Features

- Comprehensive Iran System encoding and decoding.
- Support for Persian, Arabic, Kurdish, and Tati languages.
- Advanced date and time utilities.
- JavaScript and C++ bindings.

## Usage

### Encoding and Decoding

```python
from iran_encoding.core import IranSystemEncoder

text = "Hello, World!"
encoded_bytes = IranSystemEncoder().encode(text)
decoded_text = IranSystemEncoder().decode(encoded_bytes)
assert decoded_text == text
```

### Date and Time Conversion

```python
from iran_encoding.utils import PersianDateTime

gregorian_date = "2025-08-30"
persian_date = PersianDateTime().convert(gregorian_date, lang='en')
print(persian_date)  # Output: 8 Shahrivar 1404
```

## Contributing

1. Clone the repository.
2. Install dependencies.
3. Run tests.
4. Fork and submit a pull request.

## License

MIT License
