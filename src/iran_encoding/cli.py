import argparse
import asyncio
from iran_encoding.core import IranSystemEncoder
from iran_encoding.exceptions import IranSystemError
from iran_encoding.api import websocket

def main():
    """
    Command-line interface for the Iran System Encoding library.
    """
    parser = argparse.ArgumentParser(description="Professional Iran System encoding library.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Encode command
    encode_parser = subparsers.add_parser("encode", help="Encode a string to Iran System.")
    encode_parser.add_argument("text", help="The Unicode string to encode.")
    encode_parser.add_argument("--no-visual", action="store_true", help="Disable visual ordering.")
    encode_parser.add_argument("--fallback", type=str, help="Fallback character for unsupported symbols.")

    # Decode command
    decode_parser = subparsers.add_parser("decode", help="Decode a hex string from Iran System.")
    decode_parser.add_argument("hex_string", help="The hex string to decode.")

    # WebSocket server command
    ws_parser = subparsers.add_parser("websocket", help="Start a WebSocket server.")
    ws_parser.add_argument("--host", default="localhost", help="Host for the server.")
    ws_parser.add_argument("--port", type=int, default=8765, help="Port for the server.")

    args = parser.parse_args()

    encoder = IranSystemEncoder(
        visual_ordering=not args.no_visual if 'no_visual' in args else True,
        fallback_char=args.fallback if 'fallback' in args else None
    )

    try:
        if args.command == "encode":
            encoded = encoder.encode(args.text)
            print(encoded.hex())
        elif args.command == "decode":
            decoded = encoder.decode(bytes.fromhex(args.hex_string))
            print(decoded)
        elif args.command == "websocket":
            asyncio.run(websocket.start_websocket_server(args.host, args.port))
    except IranSystemError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
