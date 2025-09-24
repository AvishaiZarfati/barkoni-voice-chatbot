#!/usr/bin/env python3
"""
Direct audio test to fix TTS issues
"""

import pyttsx3
import time

def fix_audio_output():
    """Test and fix audio output"""

    print("Fixing Audio Output Issues")
    print("=" * 30)

    try:
        # Initialize TTS engine
        engine = pyttsx3.init()

        # Check current settings
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        voice = engine.getProperty('voice')

        print(f"Current rate: {rate}")
        print(f"Current volume: {volume}")
        print(f"Current voice: {voice}")

        # Fix settings for better audio
        engine.setProperty('rate', 120)  # Slower speech
        engine.setProperty('volume', 1.0)  # Max volume

        # Test English first
        print("\nTesting English speech...")
        print("You should hear: 'Testing audio output'")
        engine.say("Testing audio output")
        engine.runAndWait()

        # Test Hebrew
        print("\nTesting Hebrew speech...")
        print("You should hear Hebrew: שלום")
        engine.say("שלום")
        engine.runAndWait()

        print("\nAudio test complete!")
        return True

    except Exception as e:
        print(f"Audio error: {e}")
        return False

def test_alternative_audio():
    """Test alternative audio methods"""

    print("\nTesting Alternative Audio...")
    print("-" * 20)

    try:
        import pygame
        pygame.mixer.init()

        # Try system beep as test
        import winsound
        print("Testing system beep...")
        winsound.Beep(1000, 500)  # 1000Hz for 500ms

        print("If you heard a beep, your speakers work!")
        return True

    except Exception as e:
        print(f"Alternative audio failed: {e}")
        return False

if __name__ == "__main__":
    print("Audio Diagnostic Tool")
    print("=" * 40)

    # Test main TTS
    tts_works = fix_audio_output()

    # Test alternative
    speakers_work = test_alternative_audio()

    print("\n" + "=" * 40)
    print("Diagnosis:")
    print(f"TTS Engine: {'✅ Working' if tts_works else '❌ Failed'}")
    print(f"Speakers: {'✅ Working' if speakers_work else '❌ Check volume/connection'}")

    if not tts_works and not speakers_work:
        print("\n🔧 Try these fixes:")
        print("1. Check if speakers/headphones are connected")
        print("2. Increase Windows volume")
        print("3. Check Windows sound settings")
        print("4. Try different audio device in Windows Sound settings")