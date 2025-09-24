#!/usr/bin/env python3
"""
Hybrid Voice System for Barkuni Chatbot
Combines system TTS with authentic Barkuni voice samples
"""

import os
import json
import random
import pygame
import tempfile
import librosa
import soundfile as sf
import pyttsx3

class BarkuniHybridVoice:
    """Enhanced voice system that combines TTS with authentic Barkuni samples"""

    def __init__(self, voice_config_path="barkuni_voice_config.json"):
        self.voice_config = None
        self.available_samples = []
        self.system_tts = None
        self.sample_mode = True  # Toggle between sample and TTS

        # Initialize components
        self.init_pygame()
        self.init_system_tts()
        self.load_voice_samples(voice_config_path)

    def init_pygame(self):
        """Initialize pygame mixer"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096)
            print("✅ Audio system initialized")
        except Exception as e:
            print(f"❌ Audio system error: {e}")

    def init_system_tts(self):
        """Initialize system TTS with Hebrew-friendly voice"""
        try:
            self.system_tts = pyttsx3.init()

            # Configure for Barkuni (Hebrew character)
            voices = self.system_tts.getProperty('voices')
            if voices:
                # Look for suitable voice for Barkuni
                for voice in voices:
                    if ('male' in voice.name.lower() and 'david' in voice.name.lower()):
                        self.system_tts.setProperty('voice', voice.id)
                        print(f"✅ Using voice: {voice.name}")
                        break

            # Set speech parameters
            self.system_tts.setProperty('rate', 160)  # Slightly slower for accent
            self.system_tts.setProperty('volume', 1.0)

            print("✅ System TTS ready")
        except Exception as e:
            print(f"❌ System TTS error: {e}")

    def load_voice_samples(self, config_path):
        """Load Barkuni voice samples"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.voice_config = json.load(f)

                # Check which samples exist and are playable
                valid_samples = []
                for audio_file in self.voice_config['audio_files']:
                    if os.path.exists(audio_file):
                        valid_samples.append(audio_file)

                self.available_samples = valid_samples
                print(f"✅ Loaded {len(valid_samples)} authentic Barkuni samples")
                return True
            else:
                print("❌ Voice config not found")
                return False
        except Exception as e:
            print(f"❌ Error loading voice samples: {e}")
            return False

    def speak_hybrid(self, text, use_sample_intro=True):
        """
        Hybrid speaking: Play Barkuni sample intro + TTS for content
        """
        try:
            print(f"🎭 Barkuni (Hybrid): {text}")

            # Option 1: Play authentic sample first, then TTS
            if use_sample_intro and self.available_samples and random.random() < 0.3:
                print("🎵 Playing authentic Barkuni intro...")
                sample_file = random.choice(self.available_samples)
                self.play_audio_sample(sample_file, duration_limit=2.0)  # 2-second intro

                # Short pause
                import time
                time.sleep(0.5)

            # Then speak the text with TTS
            if self.system_tts:
                self.system_tts.say(text)
                self.system_tts.runAndWait()

            return True

        except Exception as e:
            print(f"❌ Hybrid voice error: {e}")
            return False

    def speak_sample_only(self, text=""):
        """Play only authentic Barkuni sample"""
        if not self.available_samples:
            return self.speak_tts_only(text)

        try:
            sample_file = random.choice(self.available_samples)
            print(f"🎵 Playing authentic Barkuni: {os.path.basename(sample_file)}")
            return self.play_audio_sample(sample_file)
        except Exception as e:
            print(f"❌ Sample playback error: {e}")
            return self.speak_tts_only(text)

    def speak_tts_only(self, text):
        """Speak using only system TTS"""
        try:
            if self.system_tts:
                print(f"🔊 TTS: {text}")
                self.system_tts.say(text)
                self.system_tts.runAndWait()
                return True
            return False
        except Exception as e:
            print(f"❌ TTS error: {e}")
            return False

    def play_audio_sample(self, sample_file, duration_limit=None):
        """Play audio sample with optional duration limit"""
        try:
            # Convert to playable format
            wav_file = self.convert_to_wav(sample_file)
            if not wav_file:
                return False

            # Load and play
            pygame.mixer.music.load(wav_file)
            pygame.mixer.music.play()

            # Wait for playback (with optional time limit)
            import time
            start_time = time.time()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                if duration_limit and (time.time() - start_time) > duration_limit:
                    pygame.mixer.music.stop()
                    break

            # Clean up temp file
            if wav_file != sample_file:
                try:
                    os.unlink(wav_file)
                except:
                    pass

            return True

        except Exception as e:
            print(f"❌ Audio playback error: {e}")
            return False

    def convert_to_wav(self, input_file):
        """Convert audio file to WAV format"""
        try:
            if input_file.endswith('.wav'):
                return input_file

            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                temp_wav = tmp.name

            # Convert using librosa
            audio, sr = librosa.load(input_file, sr=22050)
            sf.write(temp_wav, audio, sr)
            return temp_wav

        except Exception as e:
            print(f"❌ Audio conversion error: {e}")
            return None

    def get_voice_mode_status(self):
        """Get current voice system status"""
        status = {
            "system_tts_ready": self.system_tts is not None,
            "samples_available": len(self.available_samples),
            "pygame_ready": pygame.mixer.get_init() is not None,
            "hybrid_mode": True
        }
        return status

def test_hybrid_voice():
    """Test the hybrid voice system"""
    print("🎭 Testing Barkuni Hybrid Voice System")
    print("=" * 45)

    voice = BarkuniHybridVoice()
    status = voice.get_voice_mode_status()

    print(f"System TTS: {'✅' if status['system_tts_ready'] else '❌'}")
    print(f"Audio Samples: {'✅' if status['samples_available'] > 0 else '❌'} ({status['samples_available']} files)")
    print(f"Audio System: {'✅' if status['pygame_ready'] else '❌'}")

    if status['system_tts_ready']:
        print("\n🔊 Testing TTS...")
        voice.speak_tts_only("Shalom! Ani Barkuni, ve'ani medaber angliyim with Israeli accent!")

    if status['samples_available'] > 0:
        print("\n🎵 Testing authentic sample...")
        voice.speak_sample_only()

    if status['system_tts_ready'] and status['samples_available'] > 0:
        print("\n🎭 Testing hybrid mode...")
        voice.speak_hybrid("Achla! This is hybrid mode - authentic Barkuni intro plus TTS!")

if __name__ == "__main__":
    test_hybrid_voice()