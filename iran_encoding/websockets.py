import asyncio
import websockets
from . import encode, decode, decode_hex

async def handler(websocket, path):
    """
    WebSocket handler that processes incoming messages.
    """
    async for message in websocket:
        try:
            # The message should be in the format "command:data"
            command, data = message.split(":", 1)

            if command == "encode":
                response = encode(data).hex()
            elif command == "decode":
                response = decode(bytes.fromhex(data))
            elif command == "decode_hex":
                response = decode_hex(data)
            else:
                response = f"Error: Unknown command '{command}'"
        except Exception as e:
            response = f"Error: {e}"

        await websocket.send(response)

async def server(host, port):
    """
    Starts the WebSocket server.
    """
    async with websockets.serve(handler, host, port):
        await asyncio.Future()  # run forever

async def client(uri, message):
    """
    Connects to the WebSocket server, sends a message, and prints the response.
    """
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(response)
