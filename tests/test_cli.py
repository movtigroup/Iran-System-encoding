import subprocess
import sys
import pytest

def run_cli_command(command):
    """Helper function to run a CLI command."""
    # We need to use the same python interpreter that is running the tests
    process = subprocess.run(
        [sys.executable, "-m", "iran_encoding.cli"] + command,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    return process

def test_cli_encode():
    """Test the CLI encode command."""
    result = run_cli_command(["encode", "سلام"])
    print(f"CLI output for encode: '{result.stdout}'")
    assert result.returncode == 0
    # The hex output can vary with shaping, so just check it's a hex string
    assert all(c in "0123456789abcdef\\n" for c in result.stdout.strip())

def test_cli_decode():
    """Test the CLI decode command."""
    # Hex for a simple shaped "سلام"
    hex_str = "f491f3a8"
    result = run_cli_command(["decode", hex_str])
    assert result.returncode == 0
    assert "سلام" in result.stdout

def test_cli_encode_no_visual():
    """Test the --no-visual flag for the encode command."""
    result_visual = run_cli_command(["encode", "سلام"])
    result_logical = run_cli_command(["encode", "سلام", "--no-visual"])
    assert result_visual.returncode == 0
    assert result_logical.returncode == 0
    assert result_visual.stdout != result_logical.stdout

def test_cli_unsupported_char_error():
    """Test that the CLI handles encoding errors."""
    result = run_cli_command(["encode", "€"])
    assert result.returncode == 1
    assert "Error" in result.stdout

def test_cli_fallback():
    """Test the --fallback flag."""
    result = run_cli_command(["encode", "€", "--fallback", "?"])
    assert result.returncode == 0
    # The fallback character '?' is 3f in hex
    assert "3f" in result.stdout
