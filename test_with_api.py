#!/usr/bin/env python3
"""Test Barkuni with Claude API for full AI responses"""

import os
from dotenv import load_dotenv
from main import CharacterVoiceChatbot

# Load environment variables
load_dotenv()

def test_barkuni_with_api():
    """Test Barkuni with Claude API"""
    print("🎭 Testing Barkuni with Claude AI")
    print("=" * 40)

    # Initialize chatbot with API
    chatbot = CharacterVoiceChatbot(
        character_name="Barkuni",
        claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
        use_character_voice=False,
        ai_provider="claude"
    )

    test_inputs = [
        "hello, how are you?",
        "what do you think about technology?",
        "tell me a funny story",
        "what's your opinion on AI?"
    ]

    print("Testing with Claude AI (should be much more Hebrew!):")
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n{i}. 👤 User: {user_input}")

        try:
            response = chatbot.generate_response(user_input)
            print(f"   🎭 Barkuni: {response}")

            # Test voice output
            if chatbot.voice_ready:
                print(f"   🔊 Speaking: {response[:50]}...")
                chatbot.speak(response)

        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_barkuni_with_api()