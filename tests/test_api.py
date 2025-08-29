import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock
from iran_encoding.api import websocket

@pytest.mark.asyncio
async def test_websocket_handler_encode():
    """Test the websocket handler for the encode command."""
    ws_mock = MagicMock()
    ws_mock.__aiter__.return_value = ["encode:سلام"]
    ws_mock.send = AsyncMock()

    await websocket.websocket_handler(ws_mock, "/")
    ws_mock.send.assert_called_once()
    # The exact hex can vary with shaping, so we just check it's a hex string
    response = ws_mock.send.call_args[0][0]
    assert all(c in "0123456789abcdef" for c in response)

@pytest.mark.asyncio
async def test_websocket_handler_decode():
    """Test the websocket handler for the decode command."""
    ws_mock = MagicMock()
    # Hex for a simple shaped "سلام"
    hex_str = "f491f3a8"
    ws_mock.__aiter__.return_value = [f"decode:{hex_str}"]
    ws_mock.send = AsyncMock()

    await websocket.websocket_handler(ws_mock, "/")
    ws_mock.send.assert_called_once_with("سلام")

@pytest.mark.asyncio
async def test_websocket_handler_unknown_command():
    """Test the websocket handler for an unknown command."""
    ws_mock = MagicMock()
    ws_mock.__aiter__.return_value = ["unknown:data"]
    ws_mock.send = AsyncMock()

    await websocket.websocket_handler(ws_mock, "/")
    ws_mock.send.assert_called_once_with("Error: Unknown command 'unknown'")
