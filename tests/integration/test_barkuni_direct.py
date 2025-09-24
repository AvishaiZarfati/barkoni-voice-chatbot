#!/usr/bin/env python3
"""
Direct test of Barkuni chatbot functionality
"""

import sys
sys.path.append('.')

from main import CharacterVoiceChatbot

def test_barkuni_direct():
    """Test Barkuni directly"""
    print("Testing Barkuni Voice Chatbot")
    print("=" * 40)

    # Initialize Barkuni
    barkuni = CharacterVoiceChatbot(
        character_name="Barkuni",
        claude_api_key=None,  # Test fallback responses
        use_character_voice=False,  # Use system voice
        ai_provider="claude"
    )

    print(f"\nBarkuni Voice Config: {barkuni.barkuni_voice_config is not None}")
    if barkuni.barkuni_voice_config:
        print(f"Voice samples: {barkuni.barkuni_voice_config.get('total_samples', 0)}")

    # Test responses
    test_messages = [
        "hello",
        "how are you",
        "thanks",
        "what do you think"
    ]

    print("\nTesting Hebrew Responses:")
    print("-" * 30)

    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = barkuni.generate_response(msg)
        print(f"Barkuni: {response}")

        # Test voice output
        print("Speaking response...")
        barkuni.speak(response)

        print("-" * 20)

if __name__ == "__main__":
    test_barkuni_direct()