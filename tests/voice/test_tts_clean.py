#!/usr/bin/env python3
"""Clean TTS test without Unicode issues"""

import pyttsx3
import time

def test_clean_tts():
    """Test TTS without Unicode issues"""
    print("Testing TTS directly...")

    try:
        # Initialize TTS engine
        engine = pyttsx3.init()

        # Get available voices
        voices = engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")
        for i, voice in enumerate(voices):
            print(f"{i}: {voice.name}")

        # Set David voice for Barkuni (male voice)
        if len(voices) > 0:
            # Use David (voice 0) for male Barkuni character
            engine.setProperty('voice', voices[0].id)  # David
            print(f"Using voice: {voices[0].name}")

        # Set properties
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.9)

        # Test Hebrew text
        print("Testing Hebrew TTS...")
        hebrew_text = "שלום, אני ברקוני!"
        print(f"Speaking: {hebrew_text}")
        engine.say(hebrew_text)
        engine.runAndWait()
        time.sleep(0.5)

        print("Testing English TTS...")
        english_text = "Hello, I am Barkuni!"
        print(f"Speaking: {english_text}")
        engine.say(english_text)
        engine.runAndWait()
        time.sleep(0.5)

        print("Testing Hebrew greeting...")
        greeting = "אחלה יום!"
        print(f"Speaking: {greeting}")
        engine.say(greeting)
        engine.runAndWait()

        print("TTS test completed successfully!")

    except Exception as e:
        print(f"TTS Error: {e}")

if __name__ == "__main__":
    test_clean_tts()