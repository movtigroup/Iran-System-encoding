import asyncio
import websockets
from iran_encoding.core import IranSystemEncoder
from iran_encoding.exceptions import IranSystemError

async def websocket_handler(websocket, path):
    """
    WebSocket handler that processes incoming messages using IranSystemEncoder.
    """
    encoder = IranSystemEncoder()
    async for message in websocket:
        try:
            command, data = message.split(":", 1)

            if command == "encode":
                response = encoder.encode(data).hex()
            elif command == "decode":
                response = encoder.decode(bytes.fromhex(data))
            else:
                response = f"Error: Unknown command '{command}'"
        except IranSystemError as e:
            response = f"Error: {e}"
        except Exception as e:
            response = f"A general error occurred: {e}"

        await websocket.send(response)

async def start_websocket_server(host="localhost", port=8765):
    """
    Starts the WebSocket server.
    """
    async with websockets.serve(websocket_handler, host, port):
        print(f"WebSocket server started on ws://{host}:{port}")
        await asyncio.Future()  # run forever

async def websocket_client(uri, message):
    """
    Connects to the WebSocket server, sends a message, and prints the response.
    """
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Received response: {response}")
    except Exception as e:
        print(f"Error connecting to WebSocket server: {e}")
