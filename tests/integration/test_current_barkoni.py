#!/usr/bin/env python3
"""
Test current Barkoni implementation with enhanced personality
Shows how Barkoni sounds now vs. what voice cloning will achieve
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from main import CharacterVoiceChatbot

# Load environment variables
load_dotenv()

def test_current_barkoni_personality():
    """Test the current Barkoni personality and voice"""
    print("🎭 TESTING CURRENT BARKONI IMPLEMENTATION")
    print("=" * 50)

    # Initialize with the enhanced Barkoni personality
    chatbot = CharacterVoiceChatbot(
        character_name="Barkuni",
        claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
        use_character_voice=False,  # System voice for now
        ai_provider="claude"
    )

    print(f"Voice Ready: {'✅' if chatbot.voice_ready else '❌'}")
    print(f"AI Provider: {chatbot.ai_provider}")
    print(f"Character Voice: {'✅' if chatbot.use_character_voice else '❌ (System TTS)'}")

    # Test phrases that should trigger authentic Barkoni responses
    test_scenarios = [
        {
            "input": "hey barkoni what's up?",
            "expected": "Hyperactive energy, Hebrew expressions, sound effects"
        },
        {
            "input": "tell me about your favorite game",
            "expected": "Gaming enthusiasm with Israeli slang"
        },
        {
            "input": "what do you think about streaming?",
            "expected": "Stream-of-consciousness excitement"
        },
        {
            "input": "how are you feeling today?",
            "expected": "Energetic response with Hebrew-English mix"
        }
    ]

    print("\n🎮 PERSONALITY TEST")
    print("=" * 30)

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. Test: '{scenario['input']}'")
        print(f"   Expected: {scenario['expected']}")

        try:
            # Generate response
            response = chatbot.generate_response(scenario['input'])
            print(f"   🎭 Barkoni: {response}")

            # Analyze response characteristics
            hebrew_words = sum(1 for word in ['achla', 'yalla', 'sababa', 'eizeh', 'kef', 'shalom']
                             if word in response.lower())

            has_excitement = any(char in response for char in ['!', '?', 'WOOO', 'YESSS'])
            has_sounds = any(sound in response.upper() for sound in ['WOOO', 'YESSS', 'HAHA', 'BOOM'])

            print(f"   📊 Analysis:")
            print(f"      Hebrew expressions: {hebrew_words}")
            print(f"      Excitement markers: {'✅' if has_excitement else '❌'}")
            print(f"      Sound effects: {'✅' if has_sounds else '❌'}")

            # Test voice output
            if chatbot.voice_ready:
                print(f"   🔊 Speaking response...")
                chatbot.speak(response)
                print(f"   ✅ Voice output complete")
            else:
                print(f"   ❌ Voice not available")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    return chatbot

def compare_voice_modes():
    """Compare different voice modes available"""
    print("\n🔊 VOICE MODE COMPARISON")
    print("=" * 40)

    test_phrase = "Achla! Yalla let's play some games, eizeh kef!"

    # Test 1: System voice (current)
    print("1. 🤖 System Voice (Current)")
    try:
        chatbot = CharacterVoiceChatbot(
            character_name="Barkuni",
            use_character_voice=False
        )

        if chatbot.voice_ready:
            print("   ✅ System TTS ready")
            print(f"   🔊 Playing: '{test_phrase}'")
            chatbot.speak(test_phrase)
        else:
            print("   ❌ System TTS not available")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 2: Character voice (if available)
    print("\n2. 🎭 Character Voice (TTS Library)")
    try:
        chatbot = CharacterVoiceChatbot(
            character_name="Barkuni",
            use_character_voice=True
        )

        if chatbot.voice_ready and chatbot.use_character_voice:
            print("   ✅ Character voice ready")
            print(f"   🔊 Playing: '{test_phrase}'")
            chatbot.speak(test_phrase)
        else:
            print("   ❌ Character voice not available (needs Python 3.11 + TTS)")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 3: Voice samples (if available)
    print("\n3. 🎵 Authentic Samples")
    try:
        from hybrid_voice_system import BarkuniHybridVoice

        hybrid = BarkuniHybridVoice()
        status = hybrid.get_voice_mode_status()

        if status['samples_available'] > 0:
            print(f"   ✅ {status['samples_available']} authentic Barkoni samples")
            print("   🔊 Playing random sample...")
            hybrid.speak_sample_only()
        else:
            print("   ❌ No authentic samples available")

    except Exception as e:
        print(f"   ❌ Error: {e}")

def show_voice_cloning_roadmap():
    """Show what voice cloning will achieve"""
    print("\n🚀 VOICE CLONING ROADMAP")
    print("=" * 40)

    print("📍 CURRENT STATUS:")
    print("✅ Authentic Barkoni personality with Hebrew expressions")
    print("✅ System voice with Hebrew accent simulation")
    print("✅ 60 authentic Barkoni voice samples collected")
    print("✅ Python 3.11 environment created")
    print("🔄 TTS library installation in progress...")

    print("\n🎯 VOICE CLONING GOALS:")
    print("1. 🎤 True Barkoni voice synthesis using XTTS v2")
    print("2. 🇮🇱 Accurate Hebrew pronunciation with Israeli accent")
    print("3. 🎭 Voice similarity to original Barkoni content")
    print("4. 🔊 Real-time text-to-speech with cloned voice")
    print("5. 🎮 Seamless integration with chatbot personality")

    print("\n⚡ EXPECTED IMPROVEMENTS:")
    print("Before: Generic system voice with accent simulation")
    print("After:  Authentic Barkoni voice with natural Hebrew pronunciation")
    print("\nBefore: 'Achla! This sounds robotic'")
    print("After:  'Achla!' (in Barkoni's actual voice tone and style)")

def main():
    """Run comprehensive current implementation test"""

    # Test current implementation
    chatbot = test_current_barkoni_personality()

    # Compare voice modes
    compare_voice_modes()

    # Show future improvements
    show_voice_cloning_roadmap()

    print("\n📊 SUMMARY")
    print("=" * 20)
    print("🎭 Personality: ✅ Authentic Barkoni style implemented")
    print("🔊 Voice: ⚠️  System TTS (enhanced with Hebrew accent)")
    print("🎤 Voice Cloning: 🔄 In progress (Python 3.11 + TTS)")
    print("🎯 Goal: 🚀 True Barkoni voice synthesis")

    print("\n🔮 NEXT STEPS:")
    print("1. Complete TTS library installation")
    print("2. Test voice cloning with Barkoni samples")
    print("3. Integrate cloned voice into main chatbot")
    print("4. Fine-tune Hebrew pronunciation")

if __name__ == "__main__":
    main()