#!/usr/bin/env python3
"""
Test the Realistic Barkuni Voice in a simple chatbot
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from realistic_barkuni_voice import RealisticBarkuniVoice, create_barkuni_personality_responses
import random

class TestRealisticBarkuniChatbot:
    def __init__(self):
        """Initialize test chatbot with realistic voice"""
        print("Initializing Realistic Barkuni Test Chatbot...")

        # Initialize realistic voice system
        self.voice = RealisticBarkuniVoice()
        self.responses = create_barkuni_personality_responses()

        print("✅ Realistic Barkuni voice ready!")
        print("✅ Hebrew pronunciation training loaded")
        print("✅ Authentic expressions available")

    def get_barkuni_response(self, user_input):
        """Get appropriate Barkuni response based on input"""

        user_lower = user_input.lower()

        # Determine response type
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'shalom', 'שלום']):
            return random.choice(self.responses['greetings'])
        elif any(word in user_lower for word in ['thank', 'toda', 'תודה']):
            return random.choice(self.responses['thanks'])
        elif '?' in user_input:
            return random.choice(self.responses['questions'])
        elif any(word in user_lower for word in ['good', 'great', 'awesome', 'sababa', 'achla']):
            return random.choice(self.responses['positive'])
        else:
            return random.choice(self.responses['general'])

    def chat_session(self):
        """Start interactive chat session"""

        print("\n" + "="*50)
        print("🎤 Realistic Barkuni Voice Chatbot")
        print("Type 'quit' to exit")
        print("="*50)

        # Welcome message
        welcome = random.choice(self.responses['greetings'])
        print(f"\nBarkuni: {welcome}")
        self.voice.speak_as_barkuni(welcome)

        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()

                if user_input.lower() in ['quit', 'exit', 'bye']:
                    farewell = "Shalom! Lehitra'ot! See you later my friend!"
                    print(f"Barkuni: {farewell}")
                    self.voice.speak_as_barkuni(farewell)
                    break

                if not user_input:
                    continue

                # Get Barkuni response
                response = self.get_barkuni_response(user_input)
                print(f"Barkuni: {response}")

                # Speak with realistic voice
                self.voice.speak_as_barkuni(response)

            except KeyboardInterrupt:
                print("\n\nShalom! Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def test_voice_samples():
    """Test different voice samples"""

    print("Testing Realistic Barkuni Voice Samples...")
    print("-" * 40)

    chatbot = TestRealisticBarkuniChatbot()

    # Test different scenarios
    test_inputs = [
        "Hello Barkuni!",
        "How are you today?",
        "Thank you for helping!",
        "That's awesome!",
        "Tell me something interesting"
    ]

    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n{i}. Testing: '{test_input}'")
        response = chatbot.get_barkuni_response(test_input)
        print(f"   Response: {response}")
        chatbot.voice.speak_as_barkuni(response)

        # Pause between tests
        import time
        time.sleep(1)

    print("\n✅ Voice testing complete!")
    return chatbot

def main():
    """Main test function"""

    print("Realistic Barkuni Voice Test")
    print("=" * 30)

    # Option 1: Test voice samples
    print("\n1. Testing voice samples...")
    chatbot = test_voice_samples()

    # Option 2: Interactive chat
    print("\n2. Starting interactive chat...")
    chatbot.chat_session()

if __name__ == "__main__":
    main()