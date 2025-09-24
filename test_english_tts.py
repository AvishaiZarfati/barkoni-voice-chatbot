#!/usr/bin/env python3
"""Test English TTS only"""

import pyttsx3
import time

def test_english_tts():
    """Test TTS with English only"""
    print("Testing English TTS...")

    try:
        # Initialize TTS engine
        engine = pyttsx3.init()

        # Get available voices
        voices = engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")

        # Set David voice for Barkuni (male voice)
        if len(voices) > 0:
            engine.setProperty('voice', voices[0].id)  # David
            print(f"Using voice: {voices[0].name}")

        # Set properties
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.9)

        # Test English text
        print("Testing English TTS...")
        english_text = "Hello, I am Barkuni!"
        print(f"Speaking: {english_text}")
        engine.say(english_text)
        engine.runAndWait()
        time.sleep(0.5)

        print("Testing second message...")
        message2 = "How are you doing today?"
        print(f"Speaking: {message2}")
        engine.say(message2)
        engine.runAndWait()
        time.sleep(0.5)

        print("Testing third message...")
        message3 = "I am ready to chat with you!"
        print(f"Speaking: {message3}")
        engine.say(message3)
        engine.runAndWait()

        print("SUCCESS: English TTS test completed!")

    except Exception as e:
        print(f"TTS Error: {e}")

if __name__ == "__main__":
    test_english_tts()