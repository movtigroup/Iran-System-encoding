"""
Python wrapper for the Iran System C library functions.
"""
import ctypes
import os
import sys
import platform
import subprocess
import tempfile


def _compile_c_library():
    """Compile the Iran System C library if needed."""
    current_dir = os.path.dirname(__file__)
    c_source = os.path.join(current_dir, "iran_system.c")
    lib_name = ""
    
    # Determine library name based on platform
    if platform.system() == "Windows":
        lib_name = "iran_system.dll"
    elif platform.system() == "Darwin":
        lib_name = "libiran_system.dylib"
    else:
        lib_name = "libiran_system.so"
    
    lib_path = os.path.join(current_dir, lib_name)
    
    # Check if library already exists and is newer than the source
    if os.path.exists(lib_path):
        if os.path.exists(c_source) and os.path.getmtime(lib_path) >= os.path.getmtime(c_source):
            return lib_path
    
    # Try to compile the C code
    try:
        if platform.system() == "Windows":
            # Try with different Windows compilers
            compilers = [
                ["gcc", "-shared", "-fPIC", "-o", lib_path, c_source],
                ["clang", "-shared", "-fPIC", "-o", lib_path, c_source]
            ]
        else:
            compilers = [
                ["gcc", "-shared", "-fPIC", "-o", lib_path, c_source],
                ["clang", "-shared", "-fPIC", "-o", lib_path, c_source]
            ]
        
        for cmd in compilers:
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                return lib_path
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        print("Warning: Could not compile C library. Falling back to Python implementation.")
        return None
    except Exception as e:
        print(f"Warning: Could not compile C library: {e}. Falling back to Python implementation.")
        return None


def _load_c_library():
    """Load the compiled C library."""
    current_dir = os.path.dirname(__file__)
    
    # Determine library name based on platform
    if platform.system() == "Windows":
        possible_names = ["iran_system.dll"]
    elif platform.system() == "Darwin":
        possible_names = ["libiran_system.dylib", "iran_system.dylib"]
    else:
        possible_names = ["libiran_system.so", "iran_system.so"]
    
    # Try to find existing library
    for lib_name in possible_names:
        lib_path = os.path.join(current_dir, lib_name)
        if os.path.exists(lib_path):
            try:
                lib = ctypes.CDLL(lib_path)
                # Set up function signatures
                _setup_function_signatures(lib)
                return lib
            except OSError:
                continue
    
    # If no library exists, try to compile it
    compiled_path = _compile_c_library()
    if compiled_path and os.path.exists(compiled_path):
        try:
            lib = ctypes.CDLL(compiled_path)
            # Set up function signatures
            _setup_function_signatures(lib)
            return lib
        except OSError:
            pass
    
    return None


def _setup_function_signatures(lib):
    """Set up function signatures for the C library."""
    try:
        # Define the function signatures based on the C header
        lib.UnicodeToIransystem.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
        lib.UnicodeToIransystem.restype = None
        
        lib.IransystemToUnicode.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
        lib.IransystemToUnicode.restype = None
        
        lib.UnicodeNumberToIransystem.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
        lib.UnicodeNumberToIransystem.restype = None
        
        lib.IransystemToUpper.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
        lib.IransystemToUpper.restype = None
        
        lib.Reverse.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
        lib.Reverse.restype = None
        
        lib.ReverseAlphaNumeric.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
        lib.ReverseAlphaNumeric.restype = None
    except AttributeError:
        # Some functions might not exist in the compiled library
        pass


# Load the C library
c_lib = _load_c_library()


def unicode_to_iransystem_c(unicode_str):
    """
    Convert Unicode string to Iran System encoding using C implementation.
    """
    if c_lib is None:
        return None
    
    try:
        # Prepare input/output buffers
        input_bytes = unicode_str.encode('utf-8')
        max_output_size = len(input_bytes) * 4  # Allocate enough space
        
        # Create buffers
        input_buffer = ctypes.create_string_buffer(input_bytes)
        output_buffer = ctypes.create_string_buffer(max_output_size)
        
        # Call the C function
        c_lib.UnicodeToIransystem(input_buffer, output_buffer)
        
        # Get the result
        result_bytes = output_buffer.raw
        # Find the null terminator
        null_pos = result_bytes.find(b'\x00')
        if null_pos != -1:
            result_bytes = result_bytes[:null_pos]
        else:
            # Remove trailing null bytes
            result_bytes = result_bytes.rstrip(b'\x00')
        
        return result_bytes
    except Exception:
        return None


def unicode_number_to_iransystem_c(unicode_str):
    """
    Convert Unicode numbers to Iran System numbers using C implementation.
    """
    if c_lib is None:
        return None
    
    try:
        # Prepare input/output buffers
        input_bytes = unicode_str.encode('utf-8')
        max_output_size = len(input_bytes) * 4  # Allocate enough space
        
        # Create buffers
        input_buffer = ctypes.create_string_buffer(input_bytes)
        output_buffer = ctypes.create_string_buffer(max_output_size)
        
        # Call the C function
        c_lib.UnicodeNumberToIransystem(input_buffer, output_buffer)
        
        # Get the result
        result_bytes = output_buffer.raw
        # Find the null terminator
        null_pos = result_bytes.find(b'\x00')
        if null_pos != -1:
            result_bytes = result_bytes[:null_pos]
        else:
            # Remove trailing null bytes
            result_bytes = result_bytes.rstrip(b'\x00')
        
        return result_bytes
    except Exception:
        return None


def iransystem_to_unicode_c(iransystem_bytes):
    """
    Convert Iran System bytes to Unicode using C implementation.
    """
    if c_lib is None:
        return None
    
    try:
        # Prepare input/output buffers
        max_output_size = len(iransystem_bytes) * 4  # Allocate enough space
        
        # Create buffers
        input_buffer = ctypes.create_string_buffer(iransystem_bytes)
        output_buffer = ctypes.create_string_buffer(max_output_size)
        
        # Call the C function
        c_lib.IransystemToUnicode(input_buffer, output_buffer)
        
        # Get the result
        result_bytes = output_buffer.raw
        # Find the null terminator
        null_pos = result_bytes.find(b'\x00')
        if null_pos != -1:
            result_bytes = result_bytes[:null_pos]
        else:
            # Remove trailing null bytes
            result_bytes = result_bytes.rstrip(b'\x00')
        
        return result_bytes.decode('utf-8')
    except (UnicodeDecodeError, Exception):
        return None