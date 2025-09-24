#!/usr/bin/env python3
"""Test voice functionality directly"""

import subprocess
import sys

def test_voice():
    """Test if Barkuni can speak"""

    # Simple test with voice
    inputs = [
        "2",              # Choose command line interface
        "Barkuni",        # Character name (Hebrew personality)
        "1",              # Choose Claude
        "",               # No API key
        "Hello",          # Simple message
        "quit"            # Exit
    ]

    input_data = "\n".join(inputs)

    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=15
        )

        print("=== VOICE TEST OUTPUT ===")
        print(result.stdout)

        # Check for voice indicators
        if "AUDIO: Using system voice" in result.stdout:
            print("\n✅ SUCCESS: Voice system detected!")
        if "SPEAKING Barkuni:" in result.stdout:
            print("✅ SUCCESS: Voice output attempted!")
        if "voice_ready" in result.stdout:
            print("✅ SUCCESS: Voice ready flag set!")

        print(f"\nExit code: {result.returncode}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_voice()