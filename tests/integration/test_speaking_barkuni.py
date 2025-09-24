#!/usr/bin/env python3
"""Test speaking Barkuni with Hebrew-English mix"""

import subprocess
import sys

def test_speaking_barkuni():
    """Test Barkuni with voice and Hebrew-English personality"""

    inputs = [
        "2",              # Command line interface
        "Barkuni",        # Character name (triggers Israeli personality)
        "1",              # Claude API
        "",               # No API key (uses enhanced fallback)
        "Shalom Barkuni!", # Hebrew greeting
        "Ma nishma?",     # What's up?
        "Tell me something", # General question
        "quit"            # Exit
    ]

    input_data = "\n".join(inputs)

    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=25
        )

        print("=== SPEAKING BARKUNI TEST ===")
        print(result.stdout)

        if "SUCCESS: System voice ready" in result.stdout:
            print("\n🔊 VOICE SYSTEM: Ready!")

        if "Barkuni:" in result.stdout:
            print("🎭 PERSONALITY: Barkuni is responding!")

        if result.returncode == 0:
            print("\n✅ SUCCESS: Barkuni should be speaking!")
            print("🗣️ Listen for David's voice with Israeli personality!")
            print("💬 Barkuni should use Hebrew-English mix like 'Shalom', 'Achla', 'Yalla'")
        else:
            print(f"\n❌ Error: Exit code {result.returncode}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_speaking_barkuni()