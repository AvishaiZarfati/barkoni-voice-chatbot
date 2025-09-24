#!/usr/bin/env python3
"""Test Claude API integration"""

import subprocess
import sys

def test_claude_chatbot():
    """Test the chatbot with Claude API selection"""

    # Inputs for the chatbot - test Claude without API key
    inputs = [
        "2",              # Choose command line interface
        "ClaudeBot",      # Character name
        "1",              # Choose Claude (Anthropic)
        "",               # No Claude API key (will use simple responses)
        "Hello",          # Test message 1
        "How are you?",   # Test message 2
        "Tell me something interesting", # Test message 3
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

        print("=== CLAUDE CHATBOT TEST ===")
        print(result.stdout)

        if result.stderr:
            print("=== ERRORS ===")
            print(result.stderr)

        print(f"=== EXIT CODE: {result.returncode} ===")

        if result.returncode == 0:
            print("\nSUCCESS: Claude integration working!")
        else:
            print("\nFAILED: Claude integration has issues")

    except subprocess.TimeoutExpired:
        print("Test timed out")
    except Exception as e:
        print(f"Error running test: {e}")

if __name__ == "__main__":
    test_claude_chatbot()