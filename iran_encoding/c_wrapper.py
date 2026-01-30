"""
Python wrapper for the Iran System C library functions.
"""
import ctypes
import os
import sys
from ctypes import c_char, c_uint, c_int, POINTER, c_char_p, c_ubyte

# Load the C library
# We'll compile the C code to a shared library when needed
def load_c_library():
    """Attempt to load the compiled C library."""
    lib_name = ""
    if sys.platform.startswith("win"):
        lib_name = "iran_system.dll"
    elif sys.platform.startswith("darwin"):
        lib_name = "libiran_system.dylib"
    else:
        lib_name = "libiran_system.so"
    
    lib_path = os.path.join(os.path.dirname(__file__), lib_name)
    
    if os.path.exists(lib_path):
        try:
            return ctypes.CDLL(lib_path)
        except OSError:
            return None
    return None

# Try to load the C library
c_lib = load_c_library()

def unicode_to_iransystem_c(unicode_str):
    """
    Convert Unicode string to Iran System encoding using C implementation.
    """
    if c_lib is None:
        # Fallback to Python implementation if C library not available
        return None
    
    # Prepare input/output buffers
    input_bytes = unicode_str.encode('utf-8')
    input_buffer = ctypes.create_string_buffer(input_bytes)
    output_buffer = ctypes.create_string_buffer(len(input_bytes) * 2)  # Allocate enough space
    
    # Call the C function
    c_lib.UnicodeToIransystem(input_buffer, output_buffer)
    
    # Get the result
    result_bytes = output_buffer.raw
    # Find the null terminator
    null_pos = result_bytes.find(b'\x00')
    if null_pos != -1:
        result_bytes = result_bytes[:null_pos]
    
    return result_bytes

def unicode_number_to_iransystem_c(unicode_str):
    """
    Convert Unicode numbers to Iran System numbers using C implementation.
    """
    if c_lib is None:
        return None
    
    input_bytes = unicode_str.encode('utf-8')
    input_buffer = ctypes.create_string_buffer(input_bytes)
    output_buffer = ctypes.create_string_buffer(len(input_bytes) * 2)
    
    c_lib.UnicodeNumberToIransystem(input_buffer, output_buffer)
    
    result_bytes = output_buffer.raw
    null_pos = result_bytes.find(b'\x00')
    if null_pos != -1:
        result_bytes = result_bytes[:null_pos]
    
    return result_bytes