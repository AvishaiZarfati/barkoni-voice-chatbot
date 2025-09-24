#!/usr/bin/env python3
import speech_recognition as sr
import pyaudio

def test_microphone():
    """Test microphone functionality for speech recognition"""
    print("Testing microphone setup...")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # List available microphones
    print("\nAvailable microphones:")
    microphone_names = sr.Microphone.list_microphone_names()
    for i, name in enumerate(microphone_names):
        print(f"{i}: {name}")

    # Try different microphones
    preferred_mics = [1, 5, 9, 14]  # Intel Smart Sound and Realtek mics

    for mic_index in preferred_mics:
        if mic_index < len(microphone_names):
            try:
                print(f"\n--- Testing microphone {mic_index}: {microphone_names[mic_index]} ---")

                # Initialize microphone with specific device
                microphone = sr.Microphone(device_index=mic_index)

                # Adjust for ambient noise
                print("Adjusting for ambient noise... Please stay quiet for 2 seconds.")
                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source, duration=2.0)
                    print(f"Energy threshold: {recognizer.energy_threshold}")
                    print(f"Dynamic energy threshold: {recognizer.dynamic_energy_threshold}")

                # Test listening
                print("Testing speech recognition... Say something!")
                with microphone as source:
                    # Listen with shorter timeout
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

                print("Processing speech...")
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"✅ SUCCESS! You said: '{text}'")
                    return mic_index, text
                except sr.UnknownValueError:
                    print("❌ Could not understand audio")
                except sr.RequestError as e:
                    print(f"❌ Speech recognition request error: {e}")

            except Exception as e:
                print(f"❌ Error with microphone {mic_index}: {e}")
                continue

    # Test default microphone
    print(f"\n--- Testing default microphone ---")
    try:
        microphone = sr.Microphone()

        print("Adjusting for ambient noise... Please stay quiet for 2 seconds.")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=2.0)
            print(f"Energy threshold: {recognizer.energy_threshold}")

        print("Testing speech recognition... Say something!")
        with microphone as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

        print("Processing speech...")
        text = recognizer.recognize_google(audio)
        print(f"✅ SUCCESS! You said: '{text}'")
        return None, text

    except sr.WaitTimeoutError:
        print("❌ Listening timeout - no speech detected")
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except sr.RequestError as e:
        print(f"❌ Speech recognition request error: {e}")
    except Exception as e:
        print(f"❌ Error with default microphone: {e}")

    print("\n❌ No microphone worked successfully")
    return None, None

def test_audio_system():
    """Test PyAudio system"""
    print("\n=== Testing PyAudio System ===")
    try:
        p = pyaudio.PyAudio()
        print(f"PyAudio version: {pyaudio.__version__}")

        print("\nAudio devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(f"{i}: {info['name']} - Max input channels: {info['maxInputChannels']}")

        p.terminate()
        return True
    except Exception as e:
        print(f"❌ PyAudio error: {e}")
        return False

if __name__ == "__main__":
    print("🎤 Microphone Test for Barkuni Chatbot")
    print("=" * 50)

    # Test audio system
    audio_ok = test_audio_system()
    if not audio_ok:
        print("❌ Audio system test failed")
        exit(1)

    # Test microphone
    print("\n=== Testing Speech Recognition ===")
    working_mic, test_text = test_microphone()

    if working_mic is not None:
        print(f"\n✅ Working microphone found: {working_mic}")
        print(f"✅ Speech recognition working: '{test_text}'")
    else:
        print("\n❌ No working microphone found")
        print("\nTroubleshooting tips:")
        print("1. Check microphone permissions in Windows settings")
        print("2. Make sure microphone is not muted")
        print("3. Try speaking louder and clearer")
        print("4. Check internet connection (needed for Google Speech Recognition)")