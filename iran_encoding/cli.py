"""
This module provides the command-line interface for the iran-encoding package.
"""
import argparse
import ast
from iran_encoding import encode, decode

def main():
    """The main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Encode and decode Persian text using the Iran System encoding.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encode command
    encode_parser = subparsers.add_parser("encode", help="Encode a string.")
    encode_parser.add_argument("text", type=str, help="The string to encode.")

    # Decode command
    decode_parser = subparsers.add_parser("decode", help="Decode a byte string.")
    decode_parser.add_argument("data", type=str, help="The byte string to decode (e.g., \"b'\\xde\\xad'\").")

    args = parser.parse_args()

    if args.command == "encode":
        try:
            encoded_result = encode(args.text)
            # Print the raw bytes to stdout
            import sys
            sys.stdout.buffer.write(encoded_result)
        except ValueError as e:
            print(f"Error: {e}")
            exit(1)
    elif args.command == "decode":
        try:
            # Safely evaluate the byte string literal
            byte_data = ast.literal_eval(args.data)
            if not isinstance(byte_data, bytes):
                raise TypeError("Input must be a byte string literal (e.g., b'...')")
            decoded_result = decode(byte_data)
            print(decoded_result)
        except (ValueError, SyntaxError, TypeError) as e:
            print(f"Error: Invalid input for decoding. {e}")
            exit(1)

if __name__ == "__main__":
    main()
