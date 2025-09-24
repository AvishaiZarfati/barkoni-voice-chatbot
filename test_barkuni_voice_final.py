#!/usr/bin/env python3
"""Final test of Barkuni with voice"""

import subprocess
import sys

def test_final_barkuni():
    """Test Barkuni chatbot with voice working"""

    inputs = [
        "2",              # Command line interface
        "Barkuni",        # Character name
        "1",              # Claude API
        "",               # No API key
        "Hello Barkuni",  # English message
        "How are you?",   # Second message
        "quit"            # Exit
    ]

    input_data = "\n".join(inputs)

    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=20
        )

        print("=== FINAL BARKUNI VOICE TEST ===")
        print(result.stdout)

        # Check for success indicators
        success_indicators = [
            "SUCCESS: System voice ready",
            "voice_ready = True",
            "Using voice: Microsoft David",
            "SPEAKING Barkuni:",
            "AUDIO: Using system voice"
        ]

        print("\n=== CHECKING VOICE INDICATORS ===")
        for indicator in success_indicators:
            if indicator in result.stdout:
                print(f"✅ FOUND: {indicator}")
            else:
                print(f"❌ MISSING: {indicator}")

        if result.returncode == 0:
            print("\n🎉 CHATBOT RAN SUCCESSFULLY!")
            print("🔊 If you heard David's voice speaking, the audio is working!")
        else:
            print(f"\n❌ Chatbot failed with exit code: {result.returncode}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_final_barkuni()