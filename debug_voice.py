#!/usr/bin/env python3
from main import CharacterVoiceChatbot

def test_voice_initialization():
    """Test voice initialization in the chatbot"""
    print("Testing Barkuni chatbot voice initialization...")

    try:
        # Initialize chatbot like the GUI does
        chatbot = CharacterVoiceChatbot(
            character_name="Barkuni",
            claude_api_key=None,
            use_character_voice=True,
            ai_provider="claude"
        )

        print(f"Voice ready: {chatbot.voice_ready}")
        print(f"System TTS available: {chatbot.system_tts is not None}")
        print(f"Character voice loaded: {chatbot.character_voice_loaded}")
        print(f"Character TTS available: {chatbot.character_tts is not None}")

        # Test speaking
        if chatbot.voice_ready:
            print("\nTesting voice output...")
            test_text = "Shalom! This is a test of Barkuni's voice system!"
            chatbot.speak(test_text)
            print("Voice test completed.")
        else:
            print("Voice system not ready!")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_voice_initialization()