#!/usr/bin/env python3
"""Direct TTS test"""

import pyttsx3
import time

def test_direct_tts():
    """Test TTS directly"""
    print("Testing TTS directly...")

    try:
        # Initialize TTS engine
        engine = pyttsx3.init()

        # Get available voices
        voices = engine.getProperty('voices')
        print(f"\nAvailable voices: {len(voices)}")
        for i, voice in enumerate(voices):
            print(f"{i}: {voice.name} - {voice.id}")

        # Set properties
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.9)

        # Test Hebrew text
        print("\n🎤 Testing Hebrew TTS...")
        hebrew_text = "שלום, אני ברקוני!"
        print(f"Speaking: {hebrew_text}")
        engine.say(hebrew_text)
        engine.runAndWait()

        print("\n🎤 Testing English TTS...")
        english_text = "Hello, I am Barkuni!"
        print(f"Speaking: {english_text}")
        engine.say(english_text)
        engine.runAndWait()

        print("\n✅ TTS test completed!")

    except Exception as e:
        print(f"❌ TTS Error: {e}")

if __name__ == "__main__":
    test_direct_tts()