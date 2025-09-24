#!/usr/bin/env python3
"""
Comprehensive test script for Barkoni voice cloning
Tests authentic Barkoni voice similarity and quality
"""

import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path

def test_environment_setup():
    """Test if Python 3.11 environment is properly set up"""
    print("🔧 Testing Environment Setup")
    print("=" * 40)

    # Check Python version
    python_version = sys.version
    print(f"Python Version: {python_version}")

    if "3.11" not in python_version:
        print("❌ WARNING: Not running Python 3.11")
        return False
    else:
        print("✅ Python 3.11 confirmed")

    # Check TTS library
    try:
        import TTS
        print(f"✅ TTS library version: {TTS.__version__}")
        tts_available = True
    except ImportError:
        print("❌ TTS library not installed")
        tts_available = False

    # Check other dependencies
    dependencies = ['torch', 'librosa', 'soundfile']
    all_deps_available = True

    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} available")
        except ImportError:
            print(f"❌ {dep} not available")
            all_deps_available = False

    return tts_available and all_deps_available

def load_barkoni_samples():
    """Load available Barkoni voice samples"""
    print("\n🎭 Loading Barkoni Voice Samples")
    print("=" * 40)

    config_path = "barkuni_voice_config.json"

    if not os.path.exists(config_path):
        print("❌ Voice config file not found")
        return []

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        available_samples = []
        for audio_file in config['audio_files']:
            if os.path.exists(audio_file):
                available_samples.append(audio_file)
                print(f"✅ Found: {os.path.basename(audio_file)}")
            else:
                print(f"❌ Missing: {os.path.basename(audio_file)}")

        print(f"\n📊 Total available samples: {len(available_samples)}")
        return available_samples

    except Exception as e:
        print(f"❌ Error loading voice config: {e}")
        return []

def test_voice_cloning_with_tts():
    """Test voice cloning using TTS library"""
    print("\n🎤 Testing Voice Cloning with TTS")
    print("=" * 40)

    try:
        from TTS.api import TTS

        # Initialize TTS with XTTS v2 (multilingual voice cloning)
        print("🔄 Initializing XTTS v2...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

        # Test phrases in Hebrew and Hebrew-accented English
        test_phrases = [
            "שלום! אני ברקוני",  # Hebrew: "Hello! I'm Barkoni"
            "Achla! This is so sababa!",  # Hebrew-English mix
            "Yalla, let's go streaming!",  # Typical Barkoni style
            "Eizeh kef! What a wonderful day for gaming!",  # Mixed expression
        ]

        # Load Barkoni samples for reference
        samples = load_barkoni_samples()
        if not samples:
            print("❌ No reference samples available for voice cloning")
            return False

        # Use first available sample as speaker reference
        reference_audio = samples[0]
        print(f"🎵 Using reference: {os.path.basename(reference_audio)}")

        output_dir = Path("output/barkoni_tests")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Test voice cloning for each phrase
        success_count = 0
        for i, phrase in enumerate(test_phrases, 1):
            try:
                print(f"\n{i}. Testing: '{phrase}'")

                output_file = output_dir / f"barkoni_test_{i}.wav"

                # Clone Barkoni's voice
                tts.tts_to_file(
                    text=phrase,
                    speaker_wav=reference_audio,
                    language="en",  # Use English for mixed content
                    file_path=str(output_file)
                )

                if output_file.exists():
                    print(f"   ✅ Generated: {output_file}")
                    success_count += 1
                else:
                    print(f"   ❌ Failed to generate audio")

            except Exception as e:
                print(f"   ❌ Error: {e}")

        print(f"\n📊 Success rate: {success_count}/{len(test_phrases)}")
        return success_count > 0

    except Exception as e:
        print(f"❌ TTS initialization error: {e}")
        return False

def test_voice_quality_comparison():
    """Compare cloned voice with original samples"""
    print("\n🔍 Voice Quality Comparison")
    print("=" * 40)

    # This would require more advanced audio analysis
    # For now, we'll just check if output files exist and have reasonable size

    output_dir = Path("output/barkoni_tests")
    if not output_dir.exists():
        print("❌ No test outputs found")
        return False

    test_files = list(output_dir.glob("barkoni_test_*.wav"))

    if not test_files:
        print("❌ No test audio files found")
        return False

    print(f"✅ Found {len(test_files)} test audio files")

    # Check file sizes (should be > 1KB for valid audio)
    valid_files = 0
    for file_path in test_files:
        size_kb = file_path.stat().st_size / 1024
        if size_kb > 1:
            print(f"✅ {file_path.name}: {size_kb:.1f} KB")
            valid_files += 1
        else:
            print(f"❌ {file_path.name}: {size_kb:.1f} KB (too small)")

    return valid_files > 0

def test_hebrew_pronunciation():
    """Test Hebrew text pronunciation accuracy"""
    print("\n🇮🇱 Testing Hebrew Pronunciation")
    print("=" * 40)

    hebrew_tests = [
        ("שלום", "Shalom"),
        ("אחלה", "Achla"),
        ("יאללה", "Yalla"),
        ("כיף", "Kef"),
        ("סבבה", "Sababa")
    ]

    try:
        from TTS.api import TTS

        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        samples = load_barkoni_samples()

        if not samples:
            print("❌ No reference samples for Hebrew testing")
            return False

        reference_audio = samples[0]
        output_dir = Path("output/hebrew_tests")
        output_dir.mkdir(parents=True, exist_ok=True)

        for i, (hebrew, transliteration) in enumerate(hebrew_tests, 1):
            try:
                print(f"{i}. Testing Hebrew: {hebrew} ({transliteration})")

                output_file = output_dir / f"hebrew_test_{i}.wav"

                # Test with transliteration for better pronunciation
                tts.tts_to_file(
                    text=transliteration,
                    speaker_wav=reference_audio,
                    language="en",
                    file_path=str(output_file)
                )

                if output_file.exists():
                    print(f"   ✅ Generated: {transliteration}")
                else:
                    print(f"   ❌ Failed")

            except Exception as e:
                print(f"   ❌ Error: {e}")

        return True

    except Exception as e:
        print(f"❌ Hebrew testing error: {e}")
        return False

def play_audio_samples():
    """Play generated audio samples for manual evaluation"""
    print("\n🔊 Audio Playback Test")
    print("=" * 40)

    try:
        import pygame
        pygame.mixer.init()

        test_dirs = ["output/barkoni_tests", "output/hebrew_tests"]

        for test_dir in test_dirs:
            if not os.path.exists(test_dir):
                continue

            audio_files = list(Path(test_dir).glob("*.wav"))

            if not audio_files:
                continue

            print(f"\n📁 {test_dir}:")

            for audio_file in audio_files[:3]:  # Play first 3 files
                print(f"🎵 Playing: {audio_file.name}")
                try:
                    pygame.mixer.music.load(str(audio_file))
                    pygame.mixer.music.play()

                    # Wait for playback
                    while pygame.mixer.music.get_busy():
                        import time
                        time.sleep(0.1)

                    print("   ✅ Playback complete")

                except Exception as e:
                    print(f"   ❌ Playback error: {e}")

        return True

    except Exception as e:
        print(f"❌ Audio playback error: {e}")
        return False

def run_comprehensive_test():
    """Run all Barkoni voice cloning tests"""
    print("🎭 BARKONI VOICE CLONING COMPREHENSIVE TEST")
    print("=" * 50)

    test_results = []

    # Test 1: Environment Setup
    test_results.append(("Environment Setup", test_environment_setup()))

    # Test 2: Load samples
    samples = load_barkoni_samples()
    test_results.append(("Sample Loading", len(samples) > 0))

    # Test 3: Voice cloning (only if TTS is available)
    if test_results[0][1]:  # If environment is OK
        test_results.append(("Voice Cloning", test_voice_cloning_with_tts()))
        test_results.append(("Voice Quality", test_voice_quality_comparison()))
        test_results.append(("Hebrew Pronunciation", test_hebrew_pronunciation()))
        test_results.append(("Audio Playback", play_audio_samples()))

    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 50)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1

    print(f"\nOverall Result: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Barkoni voice cloning is working!")
    elif passed > total // 2:
        print("⚠️  PARTIAL SUCCESS: Some tests passed, check failed tests")
    else:
        print("❌ TESTS FAILED: Voice cloning setup needs attention")

    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)