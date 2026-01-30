"""
Test script to compare Python and C implementations of Iran System encoding
"""
import subprocess
import sys
import os

def test_python_vs_c():
    """Compare Python and C implementations"""
    print("Testing Python vs C implementations...")
    
    # Import the Python implementation
    from iran_encoding import encode, decode
    
    # Test cases
    test_cases = [
        "سلام",
        "تست",
        "123",
        "تست 123",
        "پارسی",
        " Iran "
    ]
    
    print("\nTesting basic encoding/decoding:")
    for text in test_cases:
        print(f"\nInput: {repr(text)}")
        
        # Python implementation
        encoded_py = encode(text)
        decoded_py = decode(encoded_py)
        print(f"Python -> Encoded: {encoded_py.hex()}, Decoded: {repr(decoded_py)}")
        
        # Test with various configurations
        encoded_visual = encode(text, visual_ordering=True)
        decoded_visual = decode(encoded_visual)
        print(f"Python (Visual) -> Encoded: {encoded_visual.hex()}, Decoded: {repr(decoded_visual)}")
        
        encoded_logical = encode(text, visual_ordering=False)
        decoded_logical = decode(encoded_logical)
        print(f"Python (Logical) -> Encoded: {encoded_logical.hex()}, Decoded: {repr(decoded_logical)}")

def run_c_test():
    """Try to compile and run C test if possible"""
    print("\n" + "="*50)
    print("Attempting C code compilation and test...")
    
    # Try to compile the C code to a simple test executable
    c_test_code = '''
#include <stdio.h>
#include <string.h>
#include "iran_encoding/iran_system.h"

// Include the actual C implementation
''' + open("iran_encoding/iran_system.c").read() + '''

int main() {
    unsigned char input[] = "سلام";
    unsigned char output[256];
    
    printf("Testing C implementation:\\n");
    printf("Input: %s\\n", input);
    
    UnicodeToIransystem(input, output);
    printf("Output: ");
    for(int i = 0; output[i] != 0; i++) {
        printf("%02X ", output[i]);
    }
    printf("\\n");
    
    return 0;
}
'''
    
    # Write temporary C test file
    with open("test_c.c", "w", encoding="utf-8") as f:
        f.write(c_test_code)
    
    # Try to compile
    try:
        result = subprocess.run([
            "gcc", "-o", "test_c", "test_c.c"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("C code compiled successfully!")
            # Run the test
            run_result = subprocess.run(["./test_c"], capture_output=True, text=True)
            print("C Output:", run_result.stdout)
            if run_result.stderr:
                print("C Errors:", run_result.stderr)
        else:
            print("C compilation failed:", result.stderr)
            
    except FileNotFoundError:
        print("GCC compiler not found. Cannot test C implementation directly.")
    except Exception as e:
        print(f"Error running C test: {e}")
    finally:
        # Clean up temp files
        for file in ["test_c.c", "test_c.exe", "test_c"]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except:
                    pass

if __name__ == "__main__":
    print("Iran System Encoding - Python vs C Comparison Test")
    print("="*50)
    
    test_python_vs_c()
    run_c_test()
    
    print("\n" + "="*50)
    print("Test completed!")