#!/usr/bin/env python3
"""
Test Hebrew Barkoni responses
"""

import sys
sys.path.append('.')

from main import CharacterVoiceChatbot

def test_hebrew_barkoni():
    """Test Barkoni Hebrew responses"""

    print("Testing Hebrew Barkoni Responses")
    print("=" * 40)

    # Initialize Barkoni
    barkoni = CharacterVoiceChatbot(
        character_name="Barkoni",
        claude_api_key=None,  # Test fallback Hebrew responses
        use_character_voice=False,
        ai_provider="claude"
    )

    # Test Hebrew responses
    test_messages = [
        "hello",
        "שלום",
        "how are you",
        "מה שלומך",
        "thanks",
        "תודה",
        "what do you think"
    ]

    print("\nTesting Authentic Hebrew Responses:")
    print("-" * 40)

    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = barkoni.generate_response(msg)
        print(f"Barkoni: {response}")

        # Test if we can speak Hebrew
        print("Speaking Hebrew response...")
        barkoni.speak(response)

        print("-" * 20)

if __name__ == "__main__":
    test_hebrew_barkoni()