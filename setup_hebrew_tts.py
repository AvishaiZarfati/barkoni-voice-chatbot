#!/usr/bin/env python3
"""
Setup Hebrew TTS for authentic Barkoni speech
"""

import pyttsx3
import subprocess
import os

def check_hebrew_support():
    """Check if Hebrew is supported on this system"""

    print("Checking Hebrew Language Support")
    print("=" * 40)

    # Check Windows language packs
    try:
        result = subprocess.run(['powershell', 'Get-WinUserLanguageList'],
                              capture_output=True, text=True, encoding='utf-8')

        if 'he-IL' in result.stdout or 'Hebrew' in result.stdout:
            print("✅ Hebrew language pack found!")
            return True
        else:
            print("❌ Hebrew language pack not installed")
            return False

    except Exception as e:
        print(f"Could not check language packs: {e}")
        return False

def install_hebrew_voices():
    """Try to install Hebrew TTS voices"""

    print("\nInstalling Hebrew TTS Support...")
    print("-" * 30)

    # Check if we can install Hebrew voices
    try:
        # Try to install Hebrew language pack
        print("Attempting to install Hebrew language support...")

        # PowerShell command to install Hebrew
        cmd = """
        $language = "he-IL"
        $capabilities = Get-WindowsCapability -Online | Where-Object Name -like "*$language*"
        foreach ($capability in $capabilities) {
            if ($capability.State -eq "NotPresent") {
                Add-WindowsCapability -Online -Name $capability.Name
            }
        }
        """

        result = subprocess.run(['powershell', '-Command', cmd],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Hebrew language support installation attempted")
        else:
            print("❌ Could not install Hebrew automatically")
            print("Manual installation required")

    except Exception as e:
        print(f"Installation error: {e}")

def setup_hebrew_fallback():
    """Setup Hebrew text responses even without Hebrew TTS"""

    print("\nSetting up Hebrew Text Responses...")
    print("-" * 30)

    # Create Hebrew response system
    hebrew_responses = {
        'greetings': [
            'שלום! איך אתה?',
            'הי! מה נשמע?',
            'שלום שלום! מה קורה?'
        ],
        'questions': [
            'איזה שאלה! בוא נחשוב על זה...',
            'סבבה! מעניין שאתה שואל על זה!',
            'אחלה שאלה! הנה מה שאני חושב...'
        ],
        'thanks': [
            'בבקשה! תמיד בשמחה!',
            'סבבה! שמח לעזור!',
            'בכיף! אין בעיה!'
        ],
        'positive': [
            'סבבה! זה נשמע מעולה!',
            'אחלה! זה נשמע פנטסטי!',
            'יופי! אני אוהב לשמוע חדשות טובות!'
        ]
    }

    # Save Hebrew responses
    import json
    with open('barkoni_hebrew_responses.json', 'w', encoding='utf-8') as f:
        json.dump(hebrew_responses, f, ensure_ascii=False, indent=2)

    print("✅ Hebrew responses saved to barkoni_hebrew_responses.json")
    return hebrew_responses

def test_hebrew_tts():
    """Test if Hebrew TTS works"""

    print("\nTesting Hebrew TTS...")
    print("-" * 20)

    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Look for Hebrew voices
        hebrew_voice = None
        for voice in voices:
            if voice.languages and any('he' in str(lang).lower() for lang in voice.languages):
                hebrew_voice = voice
                break

        if hebrew_voice:
            print(f"✅ Hebrew voice found: {hebrew_voice.name}")
            engine.setProperty('voice', hebrew_voice.id)

            # Test Hebrew speech
            test_text = "שלום! אני ברקוני!"
            print(f"Testing: {test_text}")
            engine.say(test_text)
            engine.runAndWait()

            return True
        else:
            print("❌ No Hebrew TTS voices found")
            print("Using alternative approach...")
            return False

    except Exception as e:
        print(f"Hebrew TTS test failed: {e}")
        return False

def main():
    """Main setup function"""

    print("Barkoni Hebrew TTS Setup")
    print("Setting up authentic Hebrew speech for Barkoni")
    print("=" * 50)

    # Step 1: Check Hebrew support
    has_hebrew = check_hebrew_support()

    # Step 2: Try to install Hebrew if not available
    if not has_hebrew:
        install_hebrew_voices()

    # Step 3: Setup Hebrew responses
    hebrew_responses = setup_hebrew_fallback()

    # Step 4: Test Hebrew TTS
    hebrew_tts_works = test_hebrew_tts()

    # Summary
    print("\n" + "=" * 50)
    print("Setup Summary:")
    print(f"Hebrew Language Pack: {'✅' if has_hebrew else '❌'}")
    print(f"Hebrew TTS Voices: {'✅' if hebrew_tts_works else '❌'}")
    print(f"Hebrew Text Responses: ✅")

    if hebrew_tts_works:
        print("\n🎉 Success! Barkoni can now speak Hebrew!")
    else:
        print("\n⚠️ Hebrew TTS not available.")
        print("Barkoni will use Hebrew text with English TTS as fallback.")
        print("\nTo get Hebrew speech:")
        print("1. Go to Windows Settings > Time & Language > Language")
        print("2. Add Hebrew (Israel) language pack")
        print("3. Install speech recognition and TTS for Hebrew")

    return hebrew_tts_works

if __name__ == "__main__":
    main()