# -*- coding: utf-8 -*-
"""
A professional Python library for Iran System character encoding.
"""

from .core import IranSystemEncoder
from .exceptions import IranSystemError, EncodingError, DecodeError, TextShapingError

__version__ = "1.1.0"

__all__ = [
    "IranSystemEncoder",
    "IranSystemError",
    "EncodingError",
    "DecodeError",
    "TextShapingError",
    "__version__",
]
