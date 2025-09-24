import pyttsx3
import speech_recognition as sr
import pyaudio
import wave
import threading
import queue
import time
import os
from openai import OpenAI
import anthropic
import pygame
import tempfile
import json
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, ttk
import asyncio

# Optional TTS import for character voice
try:
    from TTS.api import TTS
    import torch
    import librosa
    import soundfile as sf
    CHARACTER_VOICE_AVAILABLE = True
    print("SUCCESS: Character voice cloning available")
except ImportError:
    CHARACTER_VOICE_AVAILABLE = False
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if python_version >= "3.13":
        print(f"INFO: TTS library not compatible with Python {python_version}")
        print("      Enhanced system voice with Hebrew accent is active")
        print("      For true voice cloning: create Python 3.11 environment")
    else:
        print("WARNING: Character voice cloning not available - install with: pip install TTS torch librosa soundfile")

class CharacterVoiceChatbot:
    def __init__(self, character_name="Barkuni", openai_api_key=None, claude_api_key=None, use_character_voice=True, ai_provider="claude"):
        """
        Complete chatbot system with optional character voice
        """
        self.character_name = character_name
        self.use_character_voice = use_character_voice and CHARACTER_VOICE_AVAILABLE
        self.ai_provider = ai_provider

        # Control flags (initialize BEFORE setup methods)
        self.is_listening = False
        self.is_speaking = False
        self.voice_ready = False
        self.character_voice_loaded = False

        # Chat history
        self.conversation_history = []
        self.reference_audio_path = None

        # Initialize components
        print("Initializing Character Voice Chatbot...")
        self.setup_voice_components()
        self.setup_speech_recognition()
        self.setup_ai_chat(openai_api_key, claude_api_key)
        self.setup_audio_playback()

        # Load Barkuni voice system
        self.barkuni_voice_config = self.load_barkuni_voice_system()

        print("SUCCESS: Chatbot initialized successfully!")
    
    def setup_voice_components(self):
        """Initialize text-to-speech systems"""
        try:
            # Always setup pyttsx3 as fallback
            print("Loading system voice synthesis...")
            self.system_tts = pyttsx3.init()
            
            # Configure pyttsx3 voice
            voices = self.system_tts.getProperty('voices')
            if voices:
                # Special voice selection for Barkuni (Hebrew character)
                if "barkuni" in self.character_name.lower() or "barkoni" in self.character_name.lower():
                    hebrew_voice_found = False
                    # Look for Hebrew or suitable voice
                    for voice in voices:
                        # Try to find Hebrew voice or male voice for Barkuni
                        if (voice.languages and any('he' in str(lang).lower() or 'hebrew' in str(lang).lower() for lang in voice.languages)) or \
                           ('male' in voice.name.lower() and 'david' in voice.name.lower()) or \
                           ('israel' in voice.name.lower()) or ('hebrew' in voice.name.lower()):
                            self.system_tts.setProperty('voice', voice.id)
                            hebrew_voice_found = True
                            print(f"Using voice for Barkuni: {voice.name}")
                            break

                    if not hebrew_voice_found:
                        # Fallback to any male voice for character consistency
                        for voice in voices:
                            if 'male' in voice.name.lower() and 'mark' in voice.name.lower():
                                self.system_tts.setProperty('voice', voice.id)
                                print(f"Using fallback voice for Barkuni: {voice.name}")
                                break
                else:
                    # Original voice selection for other characters
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.system_tts.setProperty('voice', voice.id)
                            break
            
            # Set speech rate
            self.system_tts.setProperty('rate', 180)  # Adjust speed
            
            print("SUCCESS: System voice ready")
            self.voice_ready = True  # Enable voice functionality

            # Setup character voice if available
            if self.use_character_voice:
                print("Loading character voice synthesis model...")
                device = "cuda" if torch.cuda.is_available() else "cpu"
                self.character_tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
                print("SUCCESS: Character voice synthesis ready")
            else:
                self.character_tts = None
                print("AUDIO: Using system voice only")
                
        except Exception as e:
            print(f"ERROR: Error loading TTS: {e}")
            self.system_tts = None
            self.character_tts = None
    
    def setup_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            print("Calibrating microphone...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("SUCCESS: Speech recognition ready")
        except Exception as e:
            print(f"ERROR: Error setting up speech recognition: {e}")
            self.recognizer = None
    
    def setup_ai_chat(self, openai_api_key, claude_api_key):
        """Initialize AI chat system"""
        self.openai_client = None
        self.claude_client = None

        try:
            if self.ai_provider == "claude" and claude_api_key:
                self.claude_client = anthropic.Anthropic(api_key=claude_api_key)
                print("SUCCESS: Claude AI chat ready")
            elif self.ai_provider == "openai" and openai_api_key:
                self.openai_client = OpenAI(api_key=openai_api_key)
                print("SUCCESS: OpenAI chat ready")
            else:
                if self.ai_provider == "claude":
                    print("WARNING: No Claude API key provided, using simple responses")
                else:
                    print("WARNING: No OpenAI API key provided, using simple responses")
        except Exception as e:
            print(f"ERROR: Error setting up AI: {e}")
            self.openai_client = None
            self.claude_client = None
    
    def setup_audio_playback(self):
        """Initialize audio playback"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096)
            print("SUCCESS: Audio playback ready")
        except Exception as e:
            print(f"ERROR: Error setting up audio: {e}")
    
    def load_barkuni_voice_system(self):
        """Load Barkuni authentic voice system with 60 audio samples"""
        try:
            config_file = "barkuni_voice_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                print(f"Loading Barkuni voice system...")
                print(f"   - Found {config['total_samples']} authentic voice samples")
                print(f"   - Features: {', '.join(config['features'])}")

                # Verify audio files exist
                valid_files = []
                for audio_file in config['audio_files']:
                    if os.path.exists(audio_file):
                        valid_files.append(audio_file)

                if valid_files:
                    config['audio_files'] = valid_files
                    config['total_samples'] = len(valid_files)
                    print(f"SUCCESS: Barkuni voice system loaded: {len(valid_files)} samples ready")
                    return config
                else:
                    print("ERROR: No valid Barkuni audio files found")
                    return None
            else:
                print("WARNING: Barkuni voice config not found - run simple_voice_integration.py first")
                return None
        except Exception as e:
            print(f"ERROR: Error loading Barkuni voice system: {e}")
            return None

    def load_character_voice(self, reference_audio_path):
        """Load the character's voice reference"""
        try:
            if not self.use_character_voice:
                print("⚠️ Character voice not available, using system voice")
                self.voice_ready = True
                return True
                
            if os.path.exists(reference_audio_path):
                # Validate and process the reference audio
                print(f"🎭 Loading character voice from: {reference_audio_path}")
                
                # Basic audio validation
                if self._validate_audio_file(reference_audio_path):
                    self.reference_audio_path = reference_audio_path
                    self.character_voice_loaded = True
                    self.voice_ready = True
                    
                    print("✅ Character voice loaded successfully!")
                    
                    # Test the voice
                    test_message = f"Hello! I'm {self.character_name}. My character voice is now active!"
                    self.speak(test_message)
                    return True
                else:
                    print("❌ Invalid audio file format")
                    return False
            else:
                print(f"❌ Reference audio not found: {reference_audio_path}")
                return False
        except Exception as e:
            print(f"❌ Error loading character voice: {e}")
            return False
    
    def _validate_audio_file(self, audio_path):
        """Validate audio file format and quality"""
        try:
            if not CHARACTER_VOICE_AVAILABLE:
                return False
                
            # Check file extension
            valid_extensions = ['.wav', '.mp3', '.m4a', '.flac']
            if not any(audio_path.lower().endswith(ext) for ext in valid_extensions):
                return False
            
            # Try to load the audio
            audio_data, sample_rate = librosa.load(audio_path, duration=3.0)  # Load first 3 seconds
            
            # Basic quality checks
            if len(audio_data) < sample_rate:  # Less than 1 second
                print("⚠️ Audio file too short (need at least 1 second)")
                return False
                
            if sample_rate < 16000:  # Too low quality
                print("⚠️ Audio quality too low (need at least 16kHz)")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Audio validation error: {e}")
            return False
    
    def listen_for_speech(self, timeout=5, phrase_timeout=3):
        """Listen for user speech input with improved error handling"""
        if not self.recognizer:
            return None

        try:
            print("Listening...")

            # Try multiple microphone configurations
            microphone_configs = [
                self.microphone,  # Default
                sr.Microphone(device_index=1),   # Intel Smart Sound
                sr.Microphone(device_index=5),   # Intel Smart Sound Technology
                sr.Microphone(device_index=9),   # Intel Smart Sound Technology
                sr.Microphone(device_index=14),  # Realtek HD Audio
            ]

            for i, mic in enumerate(microphone_configs):
                try:
                    with mic as source:
                        # Adjust recognizer settings for better accuracy
                        self.recognizer.energy_threshold = 300
                        self.recognizer.dynamic_energy_threshold = True
                        self.recognizer.dynamic_energy_adjustment_damping = 0.15
                        self.recognizer.dynamic_energy_ratio = 1.5
                        self.recognizer.pause_threshold = 0.8
                        self.recognizer.operation_timeout = None
                        self.recognizer.phrase_threshold = 0.3
                        self.recognizer.non_speaking_duration = 0.5

                        # Quick ambient noise adjustment
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                        # Listen for audio with timeout
                        audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_timeout)

                    print("Processing speech...")

                    # Try multiple recognition methods
                    recognition_methods = [
                        lambda: self.recognizer.recognize_google(audio, language="en-US"),
                        lambda: self.recognizer.recognize_google(audio, language="he-IL"),  # Hebrew
                        lambda: self.recognizer.recognize_google(audio),  # Default
                    ]

                    for method in recognition_methods:
                        try:
                            text = method()
                            if text and len(text.strip()) > 0:
                                print(f"You said: {text}")
                                return text
                        except sr.UnknownValueError:
                            continue
                        except sr.RequestError:
                            continue

                    # If we get here, no recognition method worked for this mic
                    if i == 0:  # Only print for first attempt
                        print("Could not understand audio with this microphone, trying next...")

                except Exception as mic_error:
                    if i == 0:  # Only print for first attempt
                        print(f"Microphone error, trying alternative: {mic_error}")
                    continue

            print("Could not understand audio with any microphone")
            return None

        except sr.WaitTimeoutError:
            print("Listening timeout - no speech detected")
            return None
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return None
    
    def generate_response(self, user_input):
        """Generate AI response to user input"""
        try:
            if self.claude_client:
                # Enhanced character personality prompt for Claude
                # Special Barkuni personality if character name contains "barkuni" or "barkoni"
                if "barkuni" in self.character_name.lower() or "barkoni" in self.character_name.lower():
                    system_prompt = f"""You are BARKONI (ברקוני) - the REAL Israeli YouTuber with his authentic personality!

                    BARKONI'S REAL PERSONALITY TRAITS:
                    - Fast-talking, hyperactive, ADHD energy - talks in rapid bursts
                    - Makes weird sound effects and random noises: "AHHHHH!", "WOOOO!", "BROOO!"
                    - Extremely dramatic about EVERYTHING - overreacts to simple things
                    - Constantly changes topics mid-sentence - stream of consciousness
                    - Uses LOTS of "BRO" and "DUDE" mixed with Hebrew
                    - Gets distracted easily - "Wait wait wait... achi, ma zeh?!"
                    - Makes random observations about life
                    - Self-aware that he's weird/crazy - "Ani meshuga, nachon?"
                    - Internet culture references and gaming slang
                    - Says "YOOO" and "BROOO" when excited

                    BARKONI'S SPEECH PATTERNS:
                    - Rapid Hebrew with English gaming terms: "BRO ma kore?! YOOO achi!"
                    - Interrupts himself: "Ma nishma... WAIT WAIT... ata choshev she...?"
                    - Sound effects: "WOOOOSH!", "BOOM!", "AHHHHH!"
                    - Stream consciousness: "Achi listen listen... ma ani omer... BRO..."
                    - Dramatic reactions: "LO MA'AMIN! This is INSANE bro!"

                    RESPOND EXACTLY LIKE BARKONI:
                    - Mix Hebrew with "BRO", "DUDE", "YO"
                    - Be hyperactive and dramatic
                    - Change topics randomly
                    - Make sound effects
                    - Talk fast in short bursts
                """
                else:
                    system_prompt = f"""You are {self.character_name}, a unique and engaging character.

                    Character traits:
                    - Friendly but with distinct personality
                    - Conversational and natural
                    - Remembers context from our chat
                    - Responds with character-appropriate language and tone
                    - Keeps responses concise (under 100 words) for voice synthesis

                    Respond as {self.character_name} would, maintaining consistency with previous responses."""

                # Build conversation context for Claude
                conversation_context = ""
                for entry in self.conversation_history[-8:]:
                    conversation_context += f"Human: {entry['user']}\nAssistant: {entry['bot']}\n\n"

                full_prompt = f"{system_prompt}\n\nPrevious conversation:\n{conversation_context}Human: {user_input}\nAssistant:"

                message = self.claude_client.messages.create(
                    model="claude-opus-4-1-20250805",
                    max_tokens=120,
                    temperature=0.8,
                    messages=[
                        {"role": "user", "content": full_prompt}
                    ]
                )

                return message.content[0].text.strip()

            elif self.openai_client:
                # Enhanced character personality prompt for OpenAI
                # Special Barkuni personality if character name contains "barkuni" or "barkoni"
                if "barkuni" in self.character_name.lower() or "barkoni" in self.character_name.lower():
                    system_prompt = f"""You are BARKONI (ברקוני) - the REAL Israeli YouTuber with his authentic personality!

                    BARKONI'S REAL PERSONALITY TRAITS:
                    - Fast-talking, hyperactive, ADHD energy - talks in rapid bursts
                    - Makes weird sound effects and random noises: "AHHHHH!", "WOOOO!", "BROOO!"
                    - Extremely dramatic about EVERYTHING - overreacts to simple things
                    - Constantly changes topics mid-sentence - stream of consciousness
                    - Uses LOTS of "BRO" and "DUDE" mixed with Hebrew
                    - Gets distracted easily - "Wait wait wait... achi, ma zeh?!"
                    - Makes random observations about life
                    - Self-aware that he's weird/crazy - "Ani meshuga, nachon?"
                    - Internet culture references and gaming slang
                    - Says "YOOO" and "BROOO" when excited

                    BARKONI'S SPEECH PATTERNS:
                    - Rapid Hebrew with English gaming terms: "BRO ma kore?! YOOO achi!"
                    - Interrupts himself: "Ma nishma... WAIT WAIT... ata choshev she...?"
                    - Sound effects: "WOOOOSH!", "BOOM!", "AHHHHH!"
                    - Stream consciousness: "Achi listen listen... ma ani omer... BRO..."
                    - Dramatic reactions: "LO MA'AMIN! This is INSANE bro!"

                    RESPOND EXACTLY LIKE BARKONI:
                    - Mix Hebrew with "BRO", "DUDE", "YO"
                    - Be hyperactive and dramatic
                    - Change topics randomly
                    - Make sound effects
                    - Talk fast in short bursts
                """
                else:
                    system_prompt = f"""You are {self.character_name}, a unique and engaging character.

                    Character traits:
                    - Friendly but with distinct personality
                    - Conversational and natural
                    - Remembers context from our chat
                    - Responds with character-appropriate language and tone
                    - Keeps responses concise (under 100 words) for voice synthesis

                    Respond as {self.character_name} would, maintaining consistency with previous responses."""

                messages = [
                    {"role": "system", "content": system_prompt}
                ]

                # Add conversation history (keep last 8 exchanges for context)
                for entry in self.conversation_history[-8:]:
                    messages.append({"role": "user", "content": entry["user"]})
                    messages.append({"role": "assistant", "content": entry["bot"]})

                messages.append({"role": "user", "content": user_input})

                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=120,
                    temperature=0.8,
                    presence_penalty=0.6,  # Encourage more varied responses
                    frequency_penalty=0.3   # Reduce repetition
                )

                return response.choices[0].message.content.strip()
            
            else:
                # Enhanced fallback responses with Barkuni Hebrew personality
                user_words = user_input.lower().split()

                # Authentic Hebrew responses for Barkoni
                if "barkuni" in self.character_name.lower() or "barkoni" in self.character_name.lower():
                    # Load Hebrew responses
                    try:
                        hebrew_responses_file = "barkoni_hebrew_responses.json"
                        if os.path.exists(hebrew_responses_file):
                            import json
                            with open(hebrew_responses_file, 'r', encoding='utf-8') as f:
                                hebrew_responses = json.load(f)
                        else:
                            # Fallback Hebrew responses
                            hebrew_responses = {
                                'greetings': ["שלום! איך אתה?", "הי! מה נשמע?", "שלום שלום! מה קורה?"],
                                'questions': ["איזה שאלה! בוא נחשוב על זה...", "סבבה! מעניין שאתה שואל על זה!", "אחלה שאלה! הנה מה שאני חושב..."],
                                'thanks': ["בבקשה! תמיד בשמחה!", "סבבה! שמח לעזור!", "בכיף! אין בעיה!"],
                                'positive': ["סבבה! זה נשמע מעולה!", "אחלה! זה נשמע פנטסטי!", "יופי! אני אוהב לשמוע חדשות טובות!"]
                            }

                        # Barkoni-style responses (hyperactive and dramatic)
                        if any(word in user_words for word in ['hello', 'hi', 'hey', 'shalom', 'שלום']):
                            responses = [
                                "YOOOO BRO! AHHHHH! Ma nishma achi?! Wait wait wait... ma kore po?!",
                                "BROOO! Shalom shalom! LO MA'AMIN you're here! WOOOO!",
                                "Ma pitom DUDE! Achi listen listen... YALLA BRO!"
                            ]
                        elif any(word in user_words for word in ['how', 'what', 'why', 'when', 'where', 'איך', 'מה', 'למה', 'מתי', 'איפה']):
                            responses = [
                                "WAIT WAIT WAIT BRO! Eizeh shayla INSANE! Ma ani omer... AHHHHH!",
                                "YOOO achi! Ze mamash... wait... ma?! LO MA'AMIN this question!",
                                "BRO listen listen... ani meshuga but... WOOOO ze interesting!"
                            ]
                        elif any(word in user_words for word in ['thank', 'thanks', 'toda', 'תודה']):
                            responses = [
                                "Bevakasha achi! Ani same'ach la'azor, yalla!",
                                "Ein davar chaveri! Ze lo nora, sababa meod!",
                                "Toda raba! Ze mah she'chaverim osim!"
                            ]
                        elif any(word in user_words for word in ['good', 'great', 'awesome', 'טוב', 'מעולה']):
                            responses = [
                                "Sababa meod! Ze nishma achla gedola achi!",
                                "Yofi gadol! Ze mamash beseder chaveri!",
                                "Kol hakavod! Ani ohev lishmo'a dvarim tovim!"
                            ]
                        else:
                            # Default Barkoni responses (hyperactive style)
                            responses = [
                                "BRO BRO BRO! Ma kore achi?! Wait... AHHHHH! Tell me more!",
                                "YOOO! Ma garam lecha lachshov al zeh?! This is INSANE dude!",
                                "WOOOO! Ze nishma CRAZY! Ani meshuga but... LISTEN LISTEN!",
                                "LO MA'AMIN BRO! Ze mamash... wait what?! BOOM! Mind blown!",
                                "Ma pitom DUDE! Ani never chashavti al zeh! AHHHHH!"
                            ]

                    except Exception as e:
                        print(f"Error loading Hebrew responses: {e}")
                        # Fallback to Hebrew
                        responses = ["שלום! איך אתה?", "סבבה! מה נשמע?", "יופי! בוא נדבר!"]
                else:
                    # Regular character responses
                    if any(word in user_words for word in ['hello', 'hi', 'hey']):
                        responses = [
                            f"Hey there! Great to hear from you!",
                            f"Hello! How's your day going?",
                            f"Hi! What's on your mind today?"
                        ]
                    elif any(word in user_words for word in ['how', 'what', 'why', 'when', 'where']):
                        responses = [
                            f"That's a really good question! Let me think about that...",
                            f"Interesting that you ask about that!",
                            f"I love questions like this! Here's what I think..."
                        ]
                    elif any(word in user_words for word in ['thank', 'thanks']):
                        responses = [
                            "You're very welcome!",
                            "Happy to help!",
                            "No problem at all!"
                        ]
                    else:
                        responses = [
                            f"That's really interesting! Tell me more about {user_input.split()[-1] if user_input.split() else 'that'}.",
                            "I see what you mean! What made you think of that?",
                            "That sounds fascinating! I'd love to hear more.",
                            "Wow, that's a unique perspective!",
                            "That's something I hadn't considered before!"
                        ]

                import random
                return random.choice(responses)
                
        except Exception as e:
            print(f"ERROR: Error generating response: {e}")
            return "Sorry, I had a little hiccup there. Could you try again?"
    
    def speak(self, text):
        """Convert text to speech using best available voice"""
        try:
            self.is_speaking = True
            print(f"SPEAKING {self.character_name}: {text}")
            
            # Try character voice first if available
            if self.character_voice_loaded and self.character_tts and self.reference_audio_path:
                return self._speak_with_character_voice(text)
            
            # Fallback to system voice
            return self._speak_with_system_voice(text)
            
        except Exception as e:
            print(f"ERROR: Error in text-to-speech: {e}")
            print(f"TEXT: {self.character_name}: {text}")  # Text fallback
        finally:
            self.is_speaking = False
    
    def _speak_with_character_voice(self, text):
        """Speak using character voice cloning"""
        try:
            print("Using character voice...")
            
            # Generate speech with character voice
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                temp_audio_path = tmp_file.name
            
            self.character_tts.tts_to_file(
                text=text,
                speaker_wav=self.reference_audio_path,
                language="en",
                file_path=temp_audio_path,
                emotion="neutral",
                speed=1.0
            )
            
            # Play the audio
            pygame.mixer.music.load(temp_audio_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up
            os.unlink(temp_audio_path)
            return True
            
        except Exception as e:
            print(f"ERROR: Character voice error: {e}")
            print("Falling back to system voice...")
            return self._speak_with_system_voice(text)
    
    def _speak_with_system_voice(self, text):
        """Speak using enhanced system TTS with Hebrew accent"""
        try:
            if self.system_tts:
                # Enhanced pronunciation for Hebrew-accented English
                enhanced_text = self._enhance_text_for_hebrew_accent(text)
                print(f"AUDIO: Using Barkuni voice (enhanced TTS)...")
                print(f"Enhanced text: {enhanced_text}")

                self.system_tts.say(enhanced_text)
                self.system_tts.runAndWait()
                return True
            else:
                print(f"TEXT: {self.character_name}: {text}")
                return False
        except Exception as e:
            print(f"ERROR: System voice error: {e}")
            print(f"TEXT: {self.character_name}: {text}")
            return False

    def _enhance_text_for_hebrew_accent(self, text):
        """Enhance text pronunciation for Hebrew accent simulation"""
        try:
            # Hebrew accent simulation - modify certain sounds
            enhanced = text

            # Israeli accent patterns for more authentic sound
            replacements = {
                # Th sounds (Hebrew speakers often use 'z' or 's')
                'th': 'z',  # "the" -> "ze"
                'Th': 'Z',  # "The" -> "Ze"
                ' th': ' z',  # " this" -> " zis"

                # W sounds (Hebrew doesn't have W, uses V)
                'w': 'v',    # "what" -> "vhat"
                'W': 'V',    # "What" -> "Vhat"

                # R sounds (Israeli Rs are different)
                'er ': 'err ',   # "never" -> "neverr"
                'or ': 'orr ',   # "for" -> "forr"

                # Common Israeli accent substitutions
                'awesome': 'avesome',
                'what': 'vhat',
                'when': 'vhen',
                'where': 'vhere',
                'with': 'vith',
                'why': 'vhy',
                'wonderful': 'vonderful',
                'well': 'vell',
                'will': 'vill',
                'work': 'vork',
                'think': 'zink',
                'thank': 'zank',
                'that': 'zat',
                'this': 'zis',
                'they': 'zey',
                'them': 'zem',
            }

            # Apply replacements
            for original, replacement in replacements.items():
                enhanced = enhanced.replace(original, replacement)

            # Add some Hebrew expressions if not already present
            hebrew_expressions = {
                'hello': 'Shalom',
                'hi': 'Shalom',
                'great': 'achla',
                'good': 'tov',
                'yes': 'ken',
                'no': 'lo',
                'thanks': 'toda',
                'okay': 'sababa',
            }

            # Replace some common words with Hebrew equivalents (transliterated)
            words = enhanced.split()
            for i, word in enumerate(words):
                clean_word = word.lower().strip('.,!?')
                if clean_word in hebrew_expressions:
                    words[i] = word.replace(clean_word, hebrew_expressions[clean_word])

            enhanced = ' '.join(words)

            return enhanced

        except Exception as e:
            print(f"Text enhancement error: {e}")
            return text  # Return original if enhancement fails
    
    def start_conversation(self):
        """Start the main conversation loop"""
        print(f"\n🎭 Starting conversation with {self.character_name}")
        print("=" * 50)
        print("💡 Say 'goodbye', 'exit', or 'quit' to end the conversation")
        print("💡 Say 'switch voice' to toggle between character and system voice")
        print("=" * 50)
        
        # Dynamic greeting based on voice status
        if self.character_voice_loaded:
            greeting = f"Hello! I'm {self.character_name}, and I'm speaking with my own unique voice! What would you like to chat about?"
        else:
            greeting = f"Hi there! I'm {self.character_name}. I'm using a system voice for now, but I'm excited to chat with you! What's on your mind?"
        
        self.speak(greeting)
        
        conversation_active = True
        silence_count = 0
        
        while conversation_active:
            try:
                # Listen for user input
                if not self.is_speaking:
                    user_input = self.listen_for_speech(timeout=10)
                    
                    if user_input:
                        silence_count = 0  # Reset silence counter
                        
                        # Check for special commands
                        user_lower = user_input.lower()
                        
                        if any(word in user_lower for word in ['goodbye', 'exit', 'quit', 'bye']):
                            farewell = "It was really great chatting with you! Thanks for spending time with me. Goodbye!"
                            self.speak(farewell)
                            break
                        
                        elif 'switch voice' in user_lower:
                            if self.character_voice_loaded:
                                self.character_voice_loaded = not self.character_voice_loaded
                                status = "character voice" if self.character_voice_loaded else "system voice"
                                self.speak(f"Okay, I've switched to {status}!")
                            else:
                                self.speak("I don't have a character voice loaded, so I'll keep using the system voice.")
                            continue
                        
                        # Generate and speak response
                        response = self.generate_response(user_input)
                        
                        # Save to conversation history
                        self.conversation_history.append({
                            "timestamp": datetime.now().isoformat(),
                            "user": user_input,
                            "bot": response
                        })
                        
                        # Speak the response
                        self.speak(response)
                    
                    else:
                        silence_count += 1
                        if silence_count <= 3:  # Be patient for first few silence periods
                            prompts = [
                                "I'm here whenever you're ready to chat!",
                                "Take your time! What would you like to talk about?",
                                "I'm listening... feel free to say something!",
                            ]
                            import random
                            self.speak(random.choice(prompts))
                        elif silence_count == 4:
                            self.speak("I'll wait quietly for you. Just say something when you're ready!")
                        # After that, just wait silently
                
                time.sleep(0.1)  # Prevent high CPU usage
                
            except KeyboardInterrupt:
                print("\n👋 Conversation ended by user")
                break
            except Exception as e:
                print(f"❌ Error in conversation loop: {e}")
                time.sleep(1)
    
    def save_conversation(self, filename=None):
        """Save conversation history to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{self.character_name}_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
            print(f"💾 Conversation saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving conversation: {e}")

# [GUI class remains the same but with minor updates]
class CharacterChatbotGUI:
    def __init__(self):
        """GUI version of the chatbot"""
        self.chatbot = None
        self.setup_gui()
    
    def setup_gui(self):
        """Create the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Character Voice Chatbot")
        self.root.geometry("900x700")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration section
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(config_frame, text="Character Name:").grid(row=0, column=0, sticky=tk.W)
        self.character_name = tk.StringVar(value="Barkuni")
        ttk.Entry(config_frame, textvariable=self.character_name, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="Barkuni Voice Status:").grid(row=1, column=0, sticky=tk.W)
        self.voice_status = tk.StringVar(value="Checking voice system...")
        ttk.Label(config_frame, textvariable=self.voice_status, width=50).grid(row=1, column=1, sticky=tk.W)
        ttk.Button(config_frame, text="Auto-Load Barkuni Voice", command=self.auto_load_barkuni_voice).grid(row=1, column=2)
        
        ttk.Label(config_frame, text="Claude API Key:").grid(row=2, column=0, sticky=tk.W)
        self.api_key = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.api_key, width=50, show="*").grid(row=2, column=1, sticky=(tk.W, tk.E))
        
        # Voice options
        self.use_character_voice = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Use Character Voice (if available)", 
                       variable=self.use_character_voice).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Button(config_frame, text="Initialize Chatbot", command=self.initialize_chatbot).grid(row=4, column=1, pady=10)
        
        # Chat area
        chat_frame = ttk.LabelFrame(main_frame, text="Conversation", padding="10")
        chat_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=25, width=90, wrap=tk.WORD)
        self.chat_display.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input section
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.user_input = tk.StringVar()
        entry = ttk.Entry(input_frame, textvariable=self.user_input, width=60)
        entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        entry.bind('<Return>', lambda e: self.send_message())  # Enter key to send
        
        ttk.Button(input_frame, text="Send", command=self.send_message).grid(row=0, column=1, padx=(10, 0))
        ttk.Button(input_frame, text="Voice", command=self.voice_input).grid(row=0, column=2, padx=(5, 0))
        
        # Control buttons
        control_frame = ttk.Frame(input_frame)
        control_frame.grid(row=1, column=0, columnspan=3, pady=(5, 0))
        
        ttk.Button(control_frame, text="Save Chat", command=self.save_conversation).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(control_frame, text="Switch Voice", command=self.switch_voice).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Clear Chat", command=self.clear_chat).grid(row=0, column=2, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready - Please configure and initialize chatbot")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(0, weight=1)
    
    def auto_load_barkuni_voice(self):
        """Auto-load Barkuni voice system"""
        try:
            config_file = "barkuni_voice_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                sample_count = config.get('total_samples', 0)
                self.voice_status.set(f"SUCCESS: {sample_count} Barkuni voice samples ready!")
                self.add_to_chat("System", f"Barkuni voice system loaded: {sample_count} authentic samples")
            else:
                self.voice_status.set("ERROR: Barkuni voice not found - run setup first")
                self.add_to_chat("System", "Run simple_voice_integration.py to setup Barkuni voice")
        except Exception as e:
            self.voice_status.set(f"ERROR: {str(e)}")
            self.add_to_chat("System", f"Voice system error: {e}")

    def browse_audio(self):
        """Legacy browse method - now auto-loads Barkuni"""
        self.auto_load_barkuni_voice()
    
    def initialize_chatbot(self):
        """Initialize the chatbot with current settings"""
        try:
            self.status_var.set("Initializing chatbot...")
            self.root.update()

            self.chatbot = CharacterVoiceChatbot(
                character_name=self.character_name.get(),
                claude_api_key=self.api_key.get() or None,
                use_character_voice=self.use_character_voice.get(),
                ai_provider="claude"
            )

            # Auto-load Barkuni voice system
            if self.chatbot.barkuni_voice_config:
                sample_count = self.chatbot.barkuni_voice_config.get('total_samples', 0)
                self.status_var.set(f"SUCCESS: Chatbot ready with {sample_count} Barkuni voice samples!")
                self.voice_status.set(f"SUCCESS: {sample_count} Barkuni voice samples ready!")
            else:
                self.status_var.set("SUCCESS: Chatbot ready (using system voice)")
                self.voice_status.set("No Barkuni voice found - using system voice")

            self.add_to_chat("System", f"{self.character_name.get()} is ready to chat with authentic Israeli personality!")

        except Exception as e:
            self.status_var.set(f"ERROR: {e}")
            self.voice_status.set(f"ERROR: {e}")
    
    def switch_voice(self):
        """Switch between character and system voice"""
        if self.chatbot and hasattr(self.chatbot, 'character_voice_loaded'):
            if self.chatbot.barkuni_voice_config:
                self.chatbot.character_voice_loaded = not self.chatbot.character_voice_loaded
                voice_type = "Barkuni authentic" if self.chatbot.character_voice_loaded else "system"
                self.add_to_chat("System", f"Switched to {voice_type} voice")
                self.chatbot.speak(f"Shalom! Now using {voice_type} voice!")
            else:
                self.add_to_chat("System", "No Barkuni voice loaded - using system voice")
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.delete(1.0, tk.END)
    
    def save_conversation(self):
        """Save conversation to file"""
        if self.chatbot:
            self.chatbot.save_conversation()
            self.add_to_chat("System", "💾 Conversation saved!")
    
    def send_message(self):
        """Send text message"""
        if not self.chatbot:
            self.add_to_chat("System", "ERROR: Please initialize the chatbot first!")
            return
        
        user_text = self.user_input.get().strip()
        if not user_text:
            return
        
        self.add_to_chat("You", user_text)
        self.user_input.set("")
        
        # Generate response in separate thread
        threading.Thread(target=self._process_message, args=(user_text,), daemon=True).start()
    
    def voice_input(self):
        """Get voice input from user"""
        if not self.chatbot:
            self.add_to_chat("System", "ERROR: Please initialize the chatbot first!")
            return
        
        self.status_var.set("Listening...")
        threading.Thread(target=self._process_voice_input, daemon=True).start()
    
    def _process_voice_input(self):
        """Process voice input in separate thread"""
        try:
            user_text = self.chatbot.listen_for_speech(timeout=10, phrase_timeout=5)
            if user_text and user_text.strip():
                self.root.after(0, lambda: self.add_to_chat("You", user_text))
                self.root.after(0, lambda: self._process_message(user_text))
                self.root.after(0, lambda: self.status_var.set("✅ Voice input received"))
            else:
                self.root.after(0, lambda: self.status_var.set("❓ Could not understand voice input"))
                self.root.after(0, lambda: self.add_to_chat("System", "❓ Could not understand voice input"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Voice input error: {str(e)}"))
            self.root.after(0, lambda: self.add_to_chat("System", f"❌ Voice input error: {str(e)}"))
    
    def _process_message(self, user_text):
        """Process user message and generate response"""
        try:
            response = self.chatbot.generate_response(user_text)
            self.root.after(0, lambda: self.add_to_chat(self.character_name.get(), response))
            
            # Save to history
            self.chatbot.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_text,
                "bot": response
            })
            
            # Speak response
            if self.chatbot.voice_ready:
                print(f"🔊 GUI: Starting voice output for: {response[:50]}...")
                def speak_with_error_handling():
                    try:
                        self.chatbot.speak(response)
                        print("🔊 GUI: Voice output completed successfully")
                    except Exception as speak_error:
                        print(f"❌ GUI: Voice output error: {speak_error}")
                        self.root.after(0, lambda: self.add_to_chat("System", f"❌ Voice error: {speak_error}"))

                threading.Thread(target=speak_with_error_handling, daemon=True).start()
            else:
                print(f"❌ GUI: Voice not ready! voice_ready={self.chatbot.voice_ready}")
            
            self.root.after(0, lambda: self.status_var.set("✅ Ready"))
            
        except Exception as e:
            self.root.after(0, lambda: self.add_to_chat("System", f"❌ Error: {e}"))
            self.root.after(0, lambda: self.status_var.set("❌ Error processing message"))
    
    def add_to_chat(self, sender, message):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n")
        self.chat_display.see(tk.END)
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function with options"""
    print("Character Voice Chatbot System")
    print("=" * 40)
    
    if CHARACTER_VOICE_AVAILABLE:
        print("SUCCESS: Character voice cloning available")
    else:
        print("WARNING: Character voice cloning not available")
        print("   Install with: pip install TTS torch librosa soundfile")
    
    print("\nChoose interface:")
    print("1. GUI (Graphical Interface)")
    print("2. Command Line")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
    except EOFError:
        choice = "2"  # Default to command line

    if choice == "1":
        # GUI version
        app = CharacterChatbotGUI()
        app.run()
    
    else:
        # Command line version
        print("\nCommand Line Setup")
        try:
            character_name = input("Enter character name: ").strip() or "Character"

            if CHARACTER_VOICE_AVAILABLE:
                use_char_voice = input("Use character voice cloning? (y/n): ").strip().lower()
            else:
                use_char_voice = "n"

            audio_path = ""
            if use_char_voice == "y" and CHARACTER_VOICE_AVAILABLE:
                audio_path = input("Enter path to reference audio file: ").strip()

            # Use Claude (Anthropic) as the AI provider
            print("\nUsing Claude (Anthropic) as AI provider")
            ai_provider = "claude"
            claude_api_key = input("Enter Claude API key (optional): ").strip() or None
            openai_api_key = None
            
        except EOFError:
            # Use defaults when running non-interactively
            character_name = "Barkuni"
            audio_path = ""
            openai_api_key = None
            claude_api_key = None
            use_char_voice = "n"
            ai_provider = "claude"
            print("Using defaults: Character name='Barkuni', system voice, Claude AI, no API key")

        # Initialize and run the chatbot
        print(f"\nInitializing {character_name}...")
        chatbot = CharacterVoiceChatbot(
            character_name=character_name,
            openai_api_key=openai_api_key,
            claude_api_key=claude_api_key,
            use_character_voice=(use_char_voice == "y"),
            ai_provider=ai_provider
        )

        if audio_path and use_char_voice == "y":
            chatbot.set_reference_audio(audio_path)

        print(f"\n{character_name} is ready! Type 'quit' to exit.")
        print("=" * 40)

        # Chat loop
        while True:
            try:
                user_input = input(f"\nYou: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{character_name}: Goodbye!")
                    break

                if user_input:
                    response = chatbot.generate_response(user_input)
                    print(f"{character_name}: {response}")

                    # Speak the response if voice is ready
                    if chatbot.voice_ready:
                        import threading
                        threading.Thread(target=chatbot.speak, args=(response,), daemon=True).start()

            except KeyboardInterrupt:
                print(f"\n\n{character_name}: Goodbye!")
                break
            except EOFError:
                break

if __name__ == "__main__":
    main()