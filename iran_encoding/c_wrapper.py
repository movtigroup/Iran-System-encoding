"""
Professional Python wrapper for the Iran System C library.
Provides performance-optimized alternatives to the pure Python core implementation.
"""
import ctypes
import os
import platform
import subprocess
from pathlib import Path

def _compile_c_library():
    """Compile the Iran System C library if a compiler is available."""
    current_dir = Path(__file__).parent
    c_source = current_dir / "iran_system.c"
    
    system = platform.system()
    if system == "Windows":
        lib_name = "iran_system.dll"
    elif system == "Darwin":
        lib_name = "libiran_system.dylib"
    else:
        lib_name = "libiran_system.so"
    
    lib_path = current_dir / lib_name
    
    # Check if we need to recompile
    if lib_path.exists():
        if c_source.exists() and lib_path.stat().st_mtime >= c_source.stat().st_mtime:
            return str(lib_path)
    
    if not c_source.exists():
        return None

    # Compilation commands to try
    compilers = [
        ["gcc", "-shared", "-fPIC", "-O3", "-o", str(lib_path), str(c_source)],
        ["clang", "-shared", "-fPIC", "-O3", "-o", str(lib_path), str(c_source)],
    ]
    
    for cmd in compilers:
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return str(lib_path)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    return None

def _load_c_library():
    """Attempt to load the C library, compiling it if necessary."""
    lib_path = _compile_c_library()
    if not lib_path:
        return None

    try:
        lib = ctypes.CDLL(lib_path)

        # Configure function signatures
        lib.UnicodeToIransystem.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib.UnicodeToIransystem.restype = None
        
        lib.IransystemToUnicode.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib.IransystemToUnicode.restype = None
        
        lib.UnicodeNumberToIransystem.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib.UnicodeNumberToIransystem.restype = None
        
        lib.ReverseIransystem.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib.ReverseIransystem.restype = None
        
        lib.UnicodeToPersianScript.argtypes = [ctypes.c_uint]
        lib.UnicodeToPersianScript.restype = ctypes.c_ubyte
        
        return lib
    except Exception:
        return None

# Singleton instance of the loaded C library
C_LIB = _load_c_library()

def is_available():
    """Check if the C extension is available for use."""
    return C_LIB is not None

def unicode_to_iransystem_c(unicode_str):
    """
    Convert Unicode string to Iran System using C implementation.
    """
    if not C_LIB:
        return None
        
    try:
        # Step 1: Convert Unicode to Persian Script bytes using C helper
        script_bytes = bytearray()
        for char in unicode_str:
            script_bytes.append(C_LIB.UnicodeToPersianScript(ord(char)))

        # Step 2: Use the main conversion logic
        max_size = len(script_bytes) + 256
        output = ctypes.create_string_buffer(max_size)
        C_LIB.UnicodeToIransystem(bytes(script_bytes), output)
        
        return output.value
    except Exception:
        return None

def iransystem_to_unicode_c(iransystem_bytes):
    """
    Convert Iran System bytes to Unicode using C implementation.
    """
    if not C_LIB:
        return None
        
    try:
        max_size = len(iransystem_bytes) * 4 + 256
        output = ctypes.create_string_buffer(max_size)
        C_LIB.IransystemToUnicode(iransystem_bytes, output)
        
        # The result from C is the intermediate "Persian Script" bytes
        # We need to map them back to actual Unicode characters
        script_bytes = output.value
        result = []
        # Since we don't have a vectorized version of PersianScriptToUnicode in C header yet,
        # we can do it in Python or just use the Python core for decoding
        # because decoding is usually less performance-critical than encoding.
        from .core import persian_script_to_unicode
        for b in script_bytes:
            result.append(chr(persian_script_to_unicode(b)))
        
        return "".join(result)
    except Exception:
        return None
