#!/usr/bin/env python3
"""
Simple audio test for Windows TTS
"""

import pyttsx3
import time

def test_windows_tts():
    """Test Windows text-to-speech"""
    print("Testing Windows TTS Audio...")

    try:
        # Initialize TTS
        engine = pyttsx3.init()

        # Get voices
        voices = engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")

        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name}")

        # Set properties
        rate = engine.getProperty('rate')
        print(f"Current speech rate: {rate}")

        volume = engine.getProperty('volume')
        print(f"Current volume: {volume}")

        # Set volume to maximum
        engine.setProperty('volume', 1.0)
        engine.setProperty('rate', 150)  # Slower for clarity

        print("\nTesting Hebrew-style speech...")
        print("You should hear: 'Shalom! This is Barkuni speaking with Hebrew accent!'")

        # Test speech
        engine.say("Shalom! This is Barkuni speaking with Hebrew accent!")
        engine.runAndWait()

        print("Audio test complete!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_windows_tts()