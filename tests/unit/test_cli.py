#!/usr/bin/env python3
"""Simple test of the command line chatbot interface"""

import subprocess
import sys

def test_chatbot():
    """Test the chatbot with predefined inputs"""

    # Inputs for the chatbot
    inputs = [
        "2",           # Choose command line interface
        "TestBot",     # Character name
        "n",           # Don't use character voice
        "",            # No audio path
        "",            # No API key (optional)
        "Hello, how are you?",  # Test message
        "quit"         # Exit command
    ]

    # Join inputs with newlines
    input_data = "\n".join(inputs)

    try:
        # Run the main script with inputs
        result = subprocess.run(
            [sys.executable, "main.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=30
        )

        print("=== CHATBOT OUTPUT ===")
        print(result.stdout)

        if result.stderr:
            print("=== ERRORS ===")
            print(result.stderr)

        print(f"=== EXIT CODE: {result.returncode} ===")

    except subprocess.TimeoutExpired:
        print("Test timed out - chatbot may be waiting for input")
    except Exception as e:
        print(f"Error running test: {e}")

if __name__ == "__main__":
    test_chatbot()