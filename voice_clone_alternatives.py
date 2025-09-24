#!/usr/bin/env python3
"""
Alternative voice cloning solutions for Python 3.13
Since TTS library doesn't support Python 3.13, here are alternative approaches
"""

import os
import random
import pygame
import tempfile
import subprocess

class AlternativeVoiceCloner:
    """Alternative voice cloning using available tools"""

    def __init__(self, voice_config_path="barkuni_voice_config.json"):
        self.voice_config = None
        self.available_samples = []
        self.load_voice_config(voice_config_path)

    def load_voice_config(self, config_path):
        """Load voice configuration"""
        try:
            import json
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.voice_config = json.load(f)

                # Check which audio files actually exist
                valid_samples = []
                for audio_file in self.voice_config['audio_files']:
                    if os.path.exists(audio_file):
                        valid_samples.append(audio_file)

                self.available_samples = valid_samples
                print(f"Loaded {len(valid_samples)} Barkuni voice samples")
                return True
            else:
                print("Voice config not found")
                return False
        except Exception as e:
            print(f"Error loading voice config: {e}")
            return False

    def play_sample_voice(self, text=""):
        """Play a random Barkuni voice sample"""
        if not self.available_samples:
            print("No voice samples available")
            return False

        try:
            # Pick a random sample
            sample_file = random.choice(self.available_samples)
            print(f"Playing Barkuni sample: {os.path.basename(sample_file)}")

            # Convert webm to wav if needed
            wav_file = self.convert_to_wav(sample_file)
            if wav_file:
                pygame.mixer.music.load(wav_file)
                pygame.mixer.music.play()

                # Wait for playback
                while pygame.mixer.music.get_busy():
                    import time
                    time.sleep(0.1)

                # Clean up temporary file
                if wav_file != sample_file:
                    os.unlink(wav_file)

                return True
        except Exception as e:
            print(f"Error playing sample: {e}")
            return False

    def convert_to_wav(self, input_file):
        """Convert audio file to WAV format"""
        try:
            if input_file.endswith('.wav'):
                return input_file

            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                temp_wav = tmp.name

            # Try using ffmpeg if available
            try:
                subprocess.run([
                    'ffmpeg', '-i', input_file, '-ar', '22050', '-ac', '1', temp_wav
                ], check=True, capture_output=True)
                return temp_wav
            except (subprocess.CalledProcessError, FileNotFoundError):
                # FFmpeg not available, try with librosa
                import librosa
                import soundfile as sf

                audio, sr = librosa.load(input_file, sr=22050)
                sf.write(temp_wav, audio, sr)
                return temp_wav

        except Exception as e:
            print(f"Error converting audio: {e}")
            return input_file  # Return original if conversion fails

def suggest_voice_cloning_solutions():
    """Suggest better voice cloning solutions"""
    print("🎭 Voice Cloning Solutions for Python 3.13")
    print("=" * 50)

    print("\n📋 CURRENT SITUATION:")
    print("✅ You have 60 authentic Barkuni voice samples")
    print("❌ TTS library doesn't support Python 3.13")
    print("✅ PyTorch and audio libraries are installed")

    print("\n🎯 RECOMMENDED SOLUTIONS:")
    print("\n1. 🔄 DOWNGRADE PYTHON (Easiest)")
    print("   - Install Python 3.11 in a separate environment")
    print("   - Use conda: conda create -n barkuni python=3.11")
    print("   - Install TTS library in that environment")

    print("\n2. 🎪 ALTERNATIVE VOICE CLONING LIBRARIES:")
    print("   - RVC (Retrieval-based Voice Conversion)")
    print("   - Bark (by Suno AI)")
    print("   - OpenVoice")
    print("   - Voicebox")

    print("\n3. 🌐 CLOUD-BASED SOLUTIONS:")
    print("   - ElevenLabs Voice Cloning API")
    print("   - Murf.ai")
    print("   - Resemble.ai")
    print("   - Azure Speech Custom Voice")

    print("\n4. 🔧 WORKAROUND FOR NOW:")
    print("   - Use the authentic samples as-is")
    print("   - Play random Barkuni samples for responses")
    print("   - Enhance system voice with Hebrew accent")

    print("\n💡 IMMEDIATE ACTION:")
    print("I'll create a hybrid system that:")
    print("- Uses system voice for text-to-speech")
    print("- Plays authentic Barkuni samples occasionally")
    print("- Maintains the Israeli personality in responses")

if __name__ == "__main__":
    suggest_voice_cloning_solutions()

    print("\n🔊 Testing Alternative Voice System...")
    cloner = AlternativeVoiceCloner()

    if cloner.available_samples:
        print(f"✅ Found {len(cloner.available_samples)} Barkuni samples")
        print("Playing a sample...")
        cloner.play_sample_voice()
    else:
        print("❌ No Barkuni samples found")