#!/usr/bin/env python
"""
Build script for Iran System C extension.
This script compiles the Iran System C code into a shared library
that can be used by the Python wrapper.
"""
import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


def build_c_library():
    """Build the Iran System C library."""
    print("Building Iran System C extension...")
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent.absolute()
    iran_encoding_dir = script_dir / "iran_encoding"
    
    # Define source and destination paths
    c_source = iran_encoding_dir / "iran_system.c"
    c_header = iran_encoding_dir / "iran_system.h"
    
    if not c_source.exists():
        print(f"Error: {c_source} not found!")
        return False
    
    if not c_header.exists():
        print(f"Error: {c_header} not found!")
        return False
    
    # Determine output library name based on platform
    system = platform.system()
    if system == "Windows":
        lib_name = "iran_system.dll"
    elif system == "Darwin":  # macOS
        lib_name = "libiran_system.dylib"
    else:  # Linux and other Unix-like systems
        lib_name = "libiran_system.so"
    
    output_path = iran_encoding_dir / lib_name
    
    print(f"Compiling for {system} -> {lib_name}")
    
    # Try different compiler commands
    compiler_commands = []
    
    if system == "Windows":
        # Windows: Try different compilers
        compiler_commands = [
            ["gcc", "-shared", "-fPIC", "-o", str(output_path), str(c_source)],
            ["clang", "-shared", "-fPIC", "-o", str(output_path), str(c_source)],
            ["cl", "/LD", str(c_source), "/Fe:" + str(output_path)]  # MSVC
        ]
    else:
        # Unix-like systems
        compiler_commands = [
            ["gcc", "-shared", "-fPIC", "-o", str(output_path), str(c_source)],
            ["clang", "-shared", "-fPIC", "-o", str(output_path), str(c_source)],
            ["cc", "-shared", "-fPIC", "-o", str(output_path), str(c_source)]
        ]
    
    # Try each compiler command
    for i, cmd in enumerate(compiler_commands):
        print(f"Trying command {i+1}: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(iran_encoding_dir)
            )
            
            if result.returncode == 0:
                print(f"✓ Successfully compiled with: {' '.join(cmd)}")
                print(f"Library created at: {output_path}")
                
                # Verify the library exists and is readable
                if output_path.exists():
                    file_size = output_path.stat().st_size
                    print(f"Library size: {file_size} bytes")
                    return True
                else:
                    print(f"✗ Library file was not created at expected location: {output_path}")
                    continue
            else:
                print(f"✗ Command failed with return code {result.returncode}")
                print(f"  stderr: {result.stderr}")
                
        except FileNotFoundError:
            print(f"✗ Compiler not found: {cmd[0]}")
            continue
        except Exception as e:
            print(f"✗ Error running command: {e}")
            continue
    
    print("✗ Failed to compile C library with any available compiler")
    print("Note: The Python implementation will be used as fallback")
    return False


def main():
    """Main function to build the C extension."""
    print("Iran System C Extension Builder")
    print("=" * 40)
    
    success = build_c_library()
    
    if success:
        print("\n✓ C extension built successfully!")
        print("The library is ready to be used with the Python wrapper.")
        print("\nTo use with CLion or other IDEs:")
        print("- Open the iran_encoding folder in CLion")
        print("- Create a C library project")
        print("- Add iran_system.c and iran_system.h")
        print("- Build the shared library")
        print("- Place the resulting .dll/.so/.dylib file in the iran_encoding folder")
    else:
        print("\n✗ C extension build failed!")
        print("The package will work using the Python fallback implementation.")
        print("To build manually:")
        print("  - Use CLion, Visual Studio, Xcode, or gcc/clang")
        print("  - Compile iran_system.c as a shared library")
        print("  - Name the output file according to your platform:")
        print("    Windows: iran_system.dll")
        print("    macOS: libiran_system.dylib")
        print("    Linux: libiran_system.so")
        print("  - Place the library file in the iran_encoding folder")


if __name__ == "__main__":
    main()