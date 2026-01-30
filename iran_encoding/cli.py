"""
This module provides the command-line interface for the iran-encoding package.
"""
import argparse
import ast
import json
from iran_encoding import encode, decode, decode_hex

def main():
    """The main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Encode and decode Persian text using the Iran System encoding.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encode command
    encode_parser = subparsers.add_parser("encode", help="Encode a string.")
    encode_parser.add_argument("text", type=str, help="The string to encode.")
    encode_parser.add_argument("--logical", action="store_true", help="Output in logical order instead of visual order.")
    encode_parser.add_argument("--config", type=str, help="A JSON string with configuration options for the reshaper.")

    # Decode command
    decode_parser = subparsers.add_parser("decode", help="Decode a byte string.")
    decode_parser.add_argument("data", type=str, help="The byte string to decode (e.g., \"b'\\xde\\xad'\").")

    # Decode-hex command
    decode_hex_parser = subparsers.add_parser("decode-hex", help="Decode a hex string.")
    decode_hex_parser.add_argument("hex_string", type=str, help="The hex string to decode (e.g., 'deadbeef').")

    args = parser.parse_args()

    if args.command == "encode":
        try:
            encoded_result = encode(args.text, visual_ordering=not args.logical)
            # Print a space-separated hex string
            hex_output = " ".join(f"{b:02x}" for b in encoded_result)
            print(hex_output)
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
    elif args.command == "decode-hex":
        try:
            decoded_result = decode_hex(args.hex_string)
            print(decoded_result)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)

if __name__ == "__main__":
    main()