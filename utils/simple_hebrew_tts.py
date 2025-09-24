#!/usr/bin/env python3
"""
Simple Hebrew TTS test without encoding issues
"""

import pyttsx3
import time

def test_simple_hebrew():
    """Test Hebrew TTS with transliteration"""

    print("Simple Hebrew TTS Test")
    print("=" * 30)

    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)

        # Test Hebrew words in English transliteration
        hebrew_phrases = [
            "Shalom",  # שלום
            "Ma nishma",  # מה נשמע
            "Sababa",  # סבבה
            "Achla",  # אחלה
            "Yalla",  # יאללה
            "Toda raba"  # תודה רבה
        ]

        print("Testing Hebrew pronunciation in English...")
        for phrase in hebrew_phrases:
            print(f"Speaking: {phrase}")
            engine.say(phrase)
            engine.runAndWait()
            time.sleep(0.5)

        # Test Hebrew-style English responses
        barkoni_responses = [
            "Shalom! Ma nishma today?",
            "Sababa! That sounds great!",
            "Achla! Tell me more about that!",
            "Yalla, let's talk!"
        ]

        print("\nTesting Barkoni-style responses...")
        for response in barkoni_responses:
            print(f"Barkoni says: {response}")
            engine.say(response)
            engine.runAndWait()
            time.sleep(0.5)

        print("\nHebrew TTS test complete!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_simple_hebrew()