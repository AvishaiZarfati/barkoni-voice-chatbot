#!/usr/bin/env python3
"""
Check for Hebrew TTS voices on Windows
"""

import pyttsx3

def check_hebrew_voices():
    """Check available voices for Hebrew"""

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    print("Checking for Hebrew TTS voices...")
    print("=" * 40)

    hebrew_voices = []
    male_voices = []

    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name}")
        if voice.languages:
            print(f"   Languages: {voice.languages}")

        # Check for Hebrew indicators
        voice_name_lower = voice.name.lower()

        if any(term in voice_name_lower for term in ['hebrew', 'israel', 'he-il']):
            hebrew_voices.append(voice)
            print("   → HEBREW VOICE FOUND!")

        if any(term in voice_name_lower for term in ['david', 'male', 'mark']):
            male_voices.append(voice)
            print("   → Male voice (good for Barkuni)")

        print()

    print("Summary:")
    print(f"Hebrew voices found: {len(hebrew_voices)}")
    print(f"Male voices found: {len(male_voices)}")

    if hebrew_voices:
        print("\nHebrew voices available:")
        for voice in hebrew_voices:
            print(f"  - {voice.name}")
    else:
        print("\nNo Hebrew voices detected.")
        print("Your system will use English with Hebrew expressions.")

    return hebrew_voices

if __name__ == "__main__":
    check_hebrew_voices()