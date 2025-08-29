# Contributing to Iran-System-encoding

## Development Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to your branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Standards
- Follow PEP 8 style guide
- Type hints for all functions
- 100% test coverage for new code
- Comprehensive docstrings (Google style)
- Clear commit messages

## Testing
```python
def test_encode_decode():
    """Test the basic encoding and decoding functionality."""
    original = "سلام دنیا"
    encoded = encode(original)
    decoded = decode(encoded)
    assert decoded == original
```

## Documentation
- Update relevant documentation
- Add docstrings for new functions
- Include examples in README.md
- Update CHANGELOG.md

## Pull Request Process
1. Update documentation
2. Add/update tests
3. Update CHANGELOG.md
4. Get review from maintainers

## Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Follow project guidelines
