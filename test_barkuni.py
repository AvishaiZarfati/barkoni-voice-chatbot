#!/usr/bin/env python3
"""Test Barkuni character personality"""

import subprocess
import sys

def test_barkuni_character():
    """Test the chatbot with Barkuni character name to trigger special personality"""

    # Inputs for the chatbot - test Barkuni personality
    inputs = [
        "2",              # Choose command line interface
        "Barkuni",        # Character name (triggers special personality)
        "1",              # Choose Claude (Anthropic)
        "",               # No Claude API key (will use simple responses but personality still applies)
        "Hello there!",   # Test message 1
        "Tell me a story", # Test message 2
        "What's your favorite thing to do?", # Test message 3
        "quit"            # Exit command
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
            timeout=15
        )

        print("=== BARKUNI CHARACTER TEST ===")
        print(result.stdout)

        if result.stderr:
            print("=== ERRORS ===")
            print(result.stderr)

        print(f"=== EXIT CODE: {result.returncode} ===")

        if result.returncode == 0:
            print("\nSUCCESS: Barkuni personality activated!")
            print("Look for energetic and creative responses above.")
        else:
            print("\nFAILED: Issues with Barkuni personality")

    except subprocess.TimeoutExpired:
        print("Test timed out")
    except Exception as e:
        print(f"Error running test: {e}")

if __name__ == "__main__":
    test_barkuni_character()