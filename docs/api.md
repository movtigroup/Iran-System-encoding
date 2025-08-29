# API Reference

## `IranSystemEncoder`

```python
class IranSystemEncoder:
    """
    Main encoder class for Iran System encoding operations.

    Attributes:
        visual_ordering (bool): Enable visual ordering for output
        fallback_char (str): Character to use for unknown symbols
        cache_enabled (bool): Enable encoding cache for performance

    Methods:
        encode(text: str) -> bytes: Encode Unicode text to Iran System
        decode(data: bytes) -> str: Decode Iran System to Unicode
        shape_text(text: str) -> str: Apply Arabic text shaping
    """

    def encode(self, text: str, visual_ordering: bool = True) -> bytes:
        """
        Encode Unicode text to Iran System encoding.

        Args:
            text (str): Unicode text to encode
            visual_ordering (bool): Apply visual ordering to output

        Returns:
            bytes: Encoded text in Iran System encoding

        Raises:
            EncodingError: If text contains unsupported characters
        """
        pass

    def decode(self, data: bytes) -> str:
        """
        Decode Iran System encoded bytes to Unicode text.

        Args:
            data (bytes): Iran System encoded bytes

        Returns:
            str: Decoded Unicode text

        Raises:
            DecodeError: If input bytes are invalid
        """
        pass
```
