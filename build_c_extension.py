#!/usr/bin/env python3
"""
Professional build script for the Iran System C extension.
Optimized for production and PyPI distribution.
"""
import os
import platform
import subprocess
import sys
from pathlib import Path

def build():
    """Build the shared library for the current platform."""
    print("Building Iran System C extension...")
    
    root_dir = Path(__file__).parent.absolute()
    iran_encoding_dir = root_dir / "iran_encoding"
    c_source = iran_encoding_dir / "iran_system.c"
    
    if not c_source.exists():
        print(f"Error: Source file {c_source} not found.")
        sys.exit(1)

    system = platform.system()
    if system == "Windows":
        lib_name = "iran_system.dll"
    elif system == "Darwin":
        lib_name = "libiran_system.dylib"
    else:
        lib_name = "libiran_system.so"

    output_path = iran_encoding_dir / lib_name
    
    # Compilation flags
    flags = ["-shared", "-fPIC", "-O3"]
    
    # Try GCC
    try:
        print(f"Compiling {c_source.name} with GCC...")
        subprocess.run(["gcc"] + flags + ["-o", str(output_path), str(c_source)], check=True)
        print(f"Successfully built: {output_path.name}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Try Clang
    try:
        print(f"Compiling {c_source.name} with Clang...")
        subprocess.run(["clang"] + flags + ["-o", str(output_path), str(c_source)], check=True)
        print(f"Successfully built: {output_path.name}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    print("Error: Failed to build C extension. Please ensure GCC or Clang is installed.")
    return False

if __name__ == "__main__":
    if build():
        print("\nBuild completed successfully.")
    else:
        print("\nBuild failed.")
        sys.exit(1)
