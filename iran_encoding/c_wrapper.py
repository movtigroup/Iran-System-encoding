import ctypes
import os
import sys

_lib = None

def _get_lib():
    global _lib
    if _lib is None:
        suffix = "so" if os.name != "nt" else "dll"
        # Try different possible filenames
        names = [f"libiransystem.{suffix}", f"iran_system.{suffix}"]
        path = None
        for name in names:
            p = os.path.join(os.path.dirname(__file__), name)
            if os.path.exists(p):
                path = p
                break

        if not path:
            return None

        try:
            _lib = ctypes.CDLL(path)
            _lib.unicode_to_iransystem.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
            _lib.iransystem_to_unicode.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, ctypes.c_char_p]
        except Exception:
            return None
    return _lib

def encode(text: str, reverse: bool = True) -> bytes:
    lib = _get_lib()
    if not lib:
        from .core import unicode_to_iransystem
        return unicode_to_iransystem(text, reverse)

    out = (ctypes.c_ubyte * (len(text) * 4))()
    out_len = ctypes.c_int(0)
    lib.unicode_to_iransystem(text.encode("utf-8"), out, ctypes.byref(out_len), 1 if reverse else 0)
    return bytes(out[:out_len.value])

def decode(data: bytes) -> str:
    lib = _get_lib()
    if not lib:
        from .core import iransystem_to_unicode
        return iransystem_to_unicode(data)

    out = ctypes.create_string_buffer(len(data) * 4)
    lib.iransystem_to_unicode((ctypes.c_ubyte * len(data))(*data), len(data), out)
    return out.value.decode("utf-8")
