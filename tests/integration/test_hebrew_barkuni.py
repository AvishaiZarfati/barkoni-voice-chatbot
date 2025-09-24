#!/usr/bin/env python3
"""Test the updated Hebrew-English mixed Barkuni personality"""

from main import CharacterVoiceChatbot

def test_barkuni_hebrew():
    """Test Barkuni Hebrew responses"""
    print("🎭 Testing Barkuni Hebrew-English Mix")
    print("=" * 45)

    # Initialize chatbot
    chatbot = CharacterVoiceChatbot(
        character_name="Barkuni",
        claude_api_key=None,  # Test without API to use fallback responses
        use_character_voice=False,
        ai_provider="claude"
    )

    test_inputs = [
        "hello",
        "how are you?", 
        "thanks",
        "that is great",
        "tell me about yourself"
    ]

    print("Testing fallback responses (no AI API):")
    for user_input in test_inputs:
        print(f"\n👤 User: {user_input}")
        response = chatbot.generate_response(user_input)
        print(f"🎭 Barkuni: {response}")

if __name__ == "__main__":
    test_barkuni_hebrew()
