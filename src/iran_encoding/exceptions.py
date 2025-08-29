class IranSystemError(Exception):
    """Base exception for Iran System encoding errors."""
    pass

class EncodingError(IranSystemError):
    """Raised when encoding fails."""
    pass

class DecodeError(IranSystemError):
    """Raised when decoding fails."""
    pass

class TextShapingError(IranSystemError):
    """Raised when text shaping fails."""
    pass
