#!/usr/bin/env python3
import pyttsx3
import pygame
import time

def test_system_tts():
    """Test system TTS functionality"""
    print("Testing system TTS (pyttsx3)...")
    try:
        engine = pyttsx3.init()

        # List available voices
        voices = engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name} - {voice.id}")

        # Test speaking
        print("Testing TTS with simple message...")
        engine.say("Hello, this is a test of the text to speech system")
        engine.runAndWait()

        print("✅ System TTS test completed")
        return True

    except Exception as e:
        print(f"❌ System TTS error: {e}")
        return False

def test_pygame_audio():
    """Test pygame audio system"""
    print("\nTesting pygame audio system...")
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096)
        print("✅ Pygame mixer initialized successfully")

        # Test if we can create a simple beep
        import numpy as np
        import tempfile
        import wave

        # Generate a simple beep
        duration = 1.0  # seconds
        sample_rate = 22050
        frequency = 440  # A4 note

        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave_data = np.sin(frequency * 2 * np.pi * t)

        # Convert to 16-bit integers
        wave_data = (wave_data * 32767).astype(np.int16)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            temp_file = tmp.name

        with wave.open(temp_file, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(wave_data.tobytes())

        # Test playback
        print("Playing test beep...")
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        print("✅ Pygame audio test completed")

        # Cleanup
        import os
        os.unlink(temp_file)
        return True

    except Exception as e:
        print(f"❌ Pygame audio error: {e}")
        return False

def test_character_voice_availability():
    """Test if character voice libraries are available"""
    print("\nTesting character voice availability...")
    try:
        from TTS.api import TTS
        import torch
        import librosa
        import soundfile as sf

        print("✅ TTS library available")
        print("✅ PyTorch available")
        print("✅ Librosa available")
        print("✅ Soundfile available")

        # Test TTS initialization
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        print("Loading XTTS model (this may take a moment)...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        print("✅ XTTS model loaded successfully")

        return True

    except ImportError as e:
        print(f"❌ Character voice libraries not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Character voice error: {e}")
        return False

if __name__ == "__main__":
    print("🔊 Audio System Test")
    print("=" * 30)

    # Test all audio components
    system_tts_ok = test_system_tts()
    pygame_ok = test_pygame_audio()
    character_voice_ok = test_character_voice_availability()

    print("\n=== RESULTS ===")
    print(f"System TTS: {'✅ Working' if system_tts_ok else '❌ Failed'}")
    print(f"Pygame Audio: {'✅ Working' if pygame_ok else '❌ Failed'}")
    print(f"Character Voice: {'✅ Available' if character_voice_ok else '❌ Not Available'}")

    if system_tts_ok:
        print("\n✅ Basic audio output should work")
    else:
        print("\n❌ Audio system has issues")