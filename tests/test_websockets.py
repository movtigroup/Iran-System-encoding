import asyncio
import unittest
from unittest.mock import MagicMock, AsyncMock
from iran_encoding.apps import websockets as ws

class TestWebSockets(unittest.TestCase):

    async def run_handler_test(self, message, expected_response):
        websocket = MagicMock()
        # Ensure the mock is awaitable and can be used in an async for loop
        websocket.__aiter__.return_value = [message]
        websocket.send = AsyncMock()

        await ws.handler(websocket, "/")

        if expected_response.startswith("Error:"):
            self.assertTrue(websocket.send.call_args[0][0].startswith("Error:"))
        else:
            websocket.send.assert_called_once_with(expected_response)

    def test_handler_encode(self):
        asyncio.run(self.run_handler_test("encode:سلام", "f491f3a8"))

    def test_handler_decode(self):
        asyncio.run(self.run_handler_test("decode:f491f3a8", "سلام"))

    def test_handler_decode_hex(self):
        asyncio.run(self.run_handler_test("decode_hex:f491f3a8", "سلام"))

    def test_handler_unknown_command(self):
        asyncio.run(self.run_handler_test("unknown:test", "Error: Unknown command 'unknown'"))

    def test_handler_invalid_message(self):
        asyncio.run(self.run_handler_test("invalid_message", "Error: not enough values to unpack"))

if __name__ == "__main__":
    unittest.main()
