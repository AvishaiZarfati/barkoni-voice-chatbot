#!/usr/bin/env python3
import speech_recognition as sr

def test_improved_speech():
    """Test the improved speech recognition"""
    recognizer = sr.Recognizer()

    # Configure recognizer with improved settings
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_ratio = 1.5
    recognizer.pause_threshold = 0.8
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.5

    # Test microphones in order
    microphone_configs = [
        (None, "Default microphone"),
        (1, "Intel Smart Sound"),
        (5, "Intel Smart Sound Technology"),
        (9, "Intel Smart Sound Technology (2)"),
        (14, "Realtek HD Audio"),
    ]

    for device_index, name in microphone_configs:
        try:
            print(f"\n--- Testing {name} ---")

            if device_index is None:
                microphone = sr.Microphone()
            else:
                microphone = sr.Microphone(device_index=device_index)

            with microphone as source:
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

            print("Speak now (you have 5 seconds):")
            with microphone as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            print("Processing...")

            # Try multiple languages
            languages = ["en-US", "he-IL", None]
            for lang in languages:
                try:
                    if lang:
                        text = recognizer.recognize_google(audio, language=lang)
                        lang_name = "English" if lang == "en-US" else "Hebrew"
                    else:
                        text = recognizer.recognize_google(audio)
                        lang_name = "Default"

                    if text and text.strip():
                        print(f"✅ SUCCESS ({lang_name}): '{text}'")
                        return True

                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print(f"Request error for {lang_name}: {e}")
                    continue

            print(f"❌ Could not understand audio with {name}")

        except Exception as e:
            print(f"❌ Error with {name}: {e}")
            continue

    print("\n❌ All microphones failed")
    return False

if __name__ == "__main__":
    print("🎤 Testing Improved Speech Recognition")
    print("=" * 45)

    success = test_improved_speech()

    if success:
        print("\n✅ Speech recognition is working!")
    else:
        print("\n❌ Speech recognition failed")
        print("\nTips:")
        print("- Speak clearly and loudly")
        print("- Check Windows microphone permissions")
        print("- Ensure internet connection for Google Speech API")
        print("- Try different phrases")