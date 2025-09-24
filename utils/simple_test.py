#!/usr/bin/env python3
"""Simple interactive test of the chatbot"""

import subprocess
import sys

def test_simple_chat():
    """Test the chatbot with a simple conversation"""

    # Inputs for the chatbot - no API key for simple responses
    inputs = [
        "2",              # Choose command line interface
        "TestBot",        # Character name
        "n",              # Don't use character voice
        "",               # No audio path (not asked since character voice = n)
        "",               # No API key (will use simple responses)
        "Hello",          # Test message 1
        "How are you?",   # Test message 2
        "Tell me a joke", # Test message 3
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

        print("=== CHATBOT CONVERSATION ===")
        print(result.stdout)

        if result.stderr:
            print("=== ERRORS ===")
            print(result.stderr)

        print(f"=== EXIT CODE: {result.returncode} ===")

        if result.returncode == 0:
            print("\n✅ SUCCESS: Chatbot ran successfully!")
        else:
            print("\n❌ FAILED: Chatbot encountered errors")

    except subprocess.TimeoutExpired:
        print("❌ Test timed out - chatbot may be stuck")
    except Exception as e:
        print(f"❌ Error running test: {e}")

if __name__ == "__main__":
    test_simple_chat()