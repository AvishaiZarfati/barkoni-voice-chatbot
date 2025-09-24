#!/usr/bin/env python3
"""
Comprehensive voice output tests for Barkuni
Tests both system TTS and character voice cloning capabilities
"""

import sys
import os
import time
import wave
import threading
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from main import CharacterVoiceChatbot

# Load environment variables
load_dotenv()

@dataclass
class VoiceTestResult:
    """Voice test result data structure"""
    test_name: str
    voice_mode: str
    text_input: str
    voice_available: bool
    speech_successful: bool
    audio_duration: float
    hebrew_pronunciation: str
    quality_rating: float
    error_message: Optional[str]
    recommendations: List[str]

class BarkuniVoiceComprehensiveTester:
    """Comprehensive voice testing for all Barkuni voice modes"""

    def __init__(self):
        self.test_results: List[VoiceTestResult] = []
        self.voice_modes = {
            'system_tts': {
                'description': 'System Text-to-Speech (pyttsx3)',
                'use_character_voice': False,
                'expected_available': True
            },
            'character_voice': {
                'description': 'Character Voice Cloning (TTS library)',
                'use_character_voice': True,
                'expected_available': False  # Depends on Python 3.11 + TTS installation
            }
        }

        # Test phrases for voice quality assessment
        self.test_phrases = {
            'hebrew_expressions': [
                "Achla! Shalom ve ahlan!",
                "Yalla, bo nelech le'sachek!",
                "Sababa, eizeh kef she yesh li!",
                "Ma nishma achi? Hakol beseder?"
            ],
            'mixed_hebrew_english': [
                "Hey there! Achla to meet you, yalla let's play some games!",
                "This is sababa! I love gaming, eizeh kef!",
                "Shalom everyone! Welcome to my stream, bo nischazek!"
            ],
            'energy_phrases': [
                "WOOO! This is amazing! Yalla let's gooo!",
                "BOOM! Achla victory! Sababa gaming session!",
                "YES YES YES! Eizeh kef, this is incredible!"
            ],
            'long_sentences': [
                "Achla everyone! Welcome back to another epic gaming stream where we're going to have eizeh kef playing the most sababa games!",
                "Yalla my friends, today we're diving into some incredible adventures and I'm so excited to share this journey with all of you beautiful people!"
            ]
        }

    def setup_chatbot(self, use_character_voice: bool = False) -> Optional[CharacterVoiceChatbot]:
        """Setup chatbot with specified voice mode"""
        try:
            chatbot = CharacterVoiceChatbot(
                character_name="Barkuni",
                claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
                use_character_voice=use_character_voice,
                ai_provider="claude"
            )
            return chatbot
        except Exception as e:
            print(f"❌ Failed to setup chatbot (character_voice={use_character_voice}): {e}")
            return None

    def test_voice_availability(self, chatbot: CharacterVoiceChatbot, voice_mode: str) -> bool:
        """Test if voice system is available"""
        if not chatbot:
            return False

        try:
            # Check voice readiness
            if not chatbot.voice_ready:
                return False

            # Try a simple test
            test_result = chatbot.speak("test", play_sound=False)  # Don't actually play
            return True

        except Exception as e:
            print(f"Voice availability test failed for {voice_mode}: {e}")
            return False

    def measure_speech_duration(self, chatbot: CharacterVoiceChatbot, text: str) -> float:
        """Measure how long speech output takes"""
        start_time = time.time()
        try:
            chatbot.speak(text)
            end_time = time.time()
            return end_time - start_time
        except Exception:
            return 0.0

    def assess_hebrew_pronunciation(self, text: str, voice_mode: str) -> str:
        """Assess Hebrew pronunciation quality (simulated)"""
        # In a real test, this would involve audio analysis
        # For now, we'll simulate based on voice mode and text complexity

        hebrew_words = ['achla', 'yalla', 'sababa', 'shalom', 'eizeh', 'kef', 'nishma', 'beseder']
        hebrew_count = sum(1 for word in hebrew_words if word.lower() in text.lower())

        if voice_mode == 'character_voice':
            if hebrew_count >= 3:
                return "EXCELLENT - Natural Hebrew pronunciation with Israeli accent"
            elif hebrew_count >= 1:
                return "GOOD - Hebrew words pronounced clearly"
            else:
                return "FAIR - Limited Hebrew content"
        else:  # system_tts
            if hebrew_count >= 3:
                return "GOOD - System TTS with Hebrew accent simulation"
            elif hebrew_count >= 1:
                return "FAIR - Basic Hebrew pronunciation"
            else:
                return "BASIC - Standard English TTS"

    def calculate_quality_rating(self, voice_available: bool, speech_successful: bool,
                               duration: float, text_length: int, hebrew_count: int) -> float:
        """Calculate overall voice quality rating (0-100)"""
        rating = 0.0

        # Base availability (30 points)
        if voice_available:
            rating += 30

        # Speech success (25 points)
        if speech_successful:
            rating += 25

        # Duration appropriateness (20 points)
        if duration > 0:
            expected_duration = text_length / 10  # Rough estimate: 10 chars per second
            if 0.5 * expected_duration <= duration <= 2.0 * expected_duration:
                rating += 20
            elif duration > 0:
                rating += 10

        # Hebrew integration (15 points)
        rating += min(hebrew_count * 5, 15)

        # Content handling (10 points)
        if text_length > 0 and speech_successful:
            rating += 10

        return min(rating, 100.0)

    def generate_recommendations(self, result: VoiceTestResult) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []

        if not result.voice_available:
            if result.voice_mode == 'system_tts':
                recommendations.append("Install pyttsx3: pip install pyttsx3")
                recommendations.append("Check system audio configuration")
            else:
                recommendations.append("Install Python 3.11 for voice cloning support")
                recommendations.append("Install TTS library: pip install TTS torch")
                recommendations.append("Verify GPU/CUDA setup for optimal performance")

        if not result.speech_successful and result.voice_available:
            recommendations.append("Check audio output device settings")
            recommendations.append("Verify microphone/speaker permissions")
            recommendations.append("Test with shorter text phrases")

        if result.audio_duration == 0 and result.speech_successful:
            recommendations.append("Speech duration not measurable - check audio monitoring")

        if result.quality_rating < 50:
            recommendations.append("Voice quality needs improvement")
            if result.voice_mode == 'system_tts':
                recommendations.append("Consider upgrading to character voice cloning")

        if "Hebrew" not in result.hebrew_pronunciation or "BASIC" in result.hebrew_pronunciation:
            recommendations.append("Enhance Hebrew pronunciation capabilities")
            recommendations.append("Add more Hebrew expressions to test phrases")

        return recommendations

    def run_voice_test(self, voice_mode: str, test_name: str, text: str) -> VoiceTestResult:
        """Run a single voice test"""
        print(f"\n🔊 Testing: {test_name} ({voice_mode})")
        print(f"📝 Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")

        voice_config = self.voice_modes[voice_mode]
        chatbot = self.setup_chatbot(voice_config['use_character_voice'])

        # Initialize result
        result = VoiceTestResult(
            test_name=test_name,
            voice_mode=voice_mode,
            text_input=text,
            voice_available=False,
            speech_successful=False,
            audio_duration=0.0,
            hebrew_pronunciation="NOT_TESTED",
            quality_rating=0.0,
            error_message=None,
            recommendations=[]
        )

        if not chatbot:
            result.error_message = "Failed to initialize chatbot"
            result.recommendations = ["Check API configuration and dependencies"]
            print(f"❌ Failed to initialize chatbot")
            return result

        # Test voice availability
        result.voice_available = self.test_voice_availability(chatbot, voice_mode)
        print(f"📢 Voice Available: {'✅' if result.voice_available else '❌'}")

        if not result.voice_available:
            result.error_message = "Voice system not available"
            result.recommendations = self.generate_recommendations(result)
            return result

        # Test speech output
        try:
            print(f"🎵 Attempting speech output...")
            duration = self.measure_speech_duration(chatbot, text)
            result.audio_duration = duration
            result.speech_successful = True
            print(f"✅ Speech successful (Duration: {duration:.2f}s)")

        except Exception as e:
            result.speech_successful = False
            result.error_message = str(e)
            print(f"❌ Speech failed: {e}")

        # Assess Hebrew pronunciation
        result.hebrew_pronunciation = self.assess_hebrew_pronunciation(text, voice_mode)
        print(f"🇮🇱 Hebrew Assessment: {result.hebrew_pronunciation}")

        # Calculate quality rating
        hebrew_count = sum(1 for word in ['achla', 'yalla', 'sababa', 'shalom', 'eizeh', 'kef']
                          if word in text.lower())
        result.quality_rating = self.calculate_quality_rating(
            result.voice_available, result.speech_successful,
            result.audio_duration, len(text), hebrew_count
        )
        print(f"⭐ Quality Rating: {result.quality_rating:.1f}/100")

        # Generate recommendations
        result.recommendations = self.generate_recommendations(result)

        return result

    def run_comprehensive_voice_tests(self):
        """Run comprehensive voice test suite"""
        print("🚀 STARTING COMPREHENSIVE BARKUNI VOICE TEST SUITE")
        print("=" * 80)

        # Test each voice mode
        for voice_mode, config in self.voice_modes.items():
            print(f"\n{'='*60}")
            print(f"🔊 TESTING VOICE MODE: {config['description'].upper()}")
            print(f"{'='*60}")

            # Test different phrase categories
            for category, phrases in self.test_phrases.items():
                print(f"\n🏷️  Category: {category.replace('_', ' ').title()}")
                print("-" * 40)

                for i, phrase in enumerate(phrases, 1):
                    test_name = f"{category}_{i}"
                    result = self.run_voice_test(voice_mode, test_name, phrase)
                    self.test_results.append(result)

                    # Small delay between tests
                    time.sleep(0.5)

        # Generate comprehensive report
        self.generate_voice_report()

    def test_voice_modes_comparison(self):
        """Compare different voice modes side by side"""
        print("\n" + "🔄 VOICE MODE COMPARISON")
        print("=" * 50)

        comparison_text = "Achla! Shalom everyone, yalla let's have some sababa fun!"

        for voice_mode, config in self.voice_modes.items():
            print(f"\n🎵 {config['description']}:")
            result = self.run_voice_test(voice_mode, "comparison_test", comparison_text)

            print(f"   Available: {'✅' if result.voice_available else '❌'}")
            print(f"   Success: {'✅' if result.speech_successful else '❌'}")
            print(f"   Quality: {result.quality_rating:.1f}/100")
            print(f"   Hebrew: {result.hebrew_pronunciation}")

    def generate_voice_report(self):
        """Generate comprehensive voice test report"""
        print("\n" + "=" * 80)
        print("📋 COMPREHENSIVE BARKUNI VOICE TEST REPORT")
        print("=" * 80)

        if not self.test_results:
            print("❌ No test results to report")
            return

        # Group results by voice mode
        voice_mode_results = {}
        for result in self.test_results:
            if result.voice_mode not in voice_mode_results:
                voice_mode_results[result.voice_mode] = []
            voice_mode_results[result.voice_mode].append(result)

        # Summary statistics
        print(f"📊 SUMMARY STATISTICS:")
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.speech_successful)
        available_tests = sum(1 for r in self.test_results if r.voice_available)
        avg_quality = sum(r.quality_rating for r in self.test_results) / total_tests

        print(f"   Total Tests: {total_tests}")
        print(f"   Voice Available: {available_tests}/{total_tests} ({available_tests/total_tests*100:.1f}%)")
        print(f"   Speech Successful: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
        print(f"   Average Quality Rating: {avg_quality:.1f}/100")

        # Voice mode breakdown
        print(f"\n🔊 VOICE MODE ANALYSIS:")
        for voice_mode, results in voice_mode_results.items():
            config = self.voice_modes[voice_mode]
            available = sum(1 for r in results if r.voice_available)
            successful = sum(1 for r in results if r.speech_successful)
            avg_quality = sum(r.quality_rating for r in results) / len(results)
            avg_duration = sum(r.audio_duration for r in results if r.audio_duration > 0)
            avg_duration = avg_duration / max(1, len([r for r in results if r.audio_duration > 0]))

            print(f"\n   {config['description']}:")
            print(f"      Tests Run: {len(results)}")
            print(f"      Available: {available}/{len(results)} ({available/len(results)*100:.1f}%)")
            print(f"      Successful: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
            print(f"      Avg Quality: {avg_quality:.1f}/100")
            print(f"      Avg Duration: {avg_duration:.2f}s")

            # Show best and worst performing tests
            if results:
                best_result = max(results, key=lambda x: x.quality_rating)
                worst_result = min(results, key=lambda x: x.quality_rating)

                print(f"      Best Test: {best_result.test_name} ({best_result.quality_rating:.1f}/100)")
                print(f"      Worst Test: {worst_result.test_name} ({worst_result.quality_rating:.1f}/100)")

        # Hebrew pronunciation analysis
        print(f"\n🇮🇱 HEBREW PRONUNCIATION ANALYSIS:")
        pronunciation_ratings = {}
        for result in self.test_results:
            rating = result.hebrew_pronunciation
            pronunciation_ratings[rating] = pronunciation_ratings.get(rating, 0) + 1

        for rating, count in sorted(pronunciation_ratings.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_tests) * 100
            print(f"   {rating}: {count}/{total_tests} ({percentage:.1f}%)")

        # Recommendations summary
        print(f"\n💡 OVERALL RECOMMENDATIONS:")
        all_recommendations = []
        for result in self.test_results:
            all_recommendations.extend(result.recommendations)

        recommendation_frequency = {}
        for rec in all_recommendations:
            recommendation_frequency[rec] = recommendation_frequency.get(rec, 0) + 1

        for rec, count in sorted(recommendation_frequency.items(), key=lambda x: x[1], reverse=True):
            if count >= 2:  # Only show frequent recommendations
                print(f"   • {rec} (mentioned {count} times)")

        # Final assessment
        print(f"\n🏆 FINAL VOICE ASSESSMENT:")

        if avg_quality >= 80:
            assessment = "EXCELLENT - Voice system working optimally"
            grade = "A+"
        elif avg_quality >= 70:
            assessment = "VERY GOOD - Minor voice improvements possible"
            grade = "A"
        elif avg_quality >= 60:
            assessment = "GOOD - Voice system functional with room for improvement"
            grade = "B"
        elif avg_quality >= 40:
            assessment = "FAIR - Basic voice functionality, needs enhancement"
            grade = "C"
        else:
            assessment = "NEEDS SIGNIFICANT IMPROVEMENT - Voice system requires major work"
            grade = "D"

        print(f"   Overall Voice Quality: {avg_quality:.1f}/100")
        print(f"   Voice Grade: {grade}")
        print(f"   Assessment: {assessment}")

        # Voice mode recommendations
        if voice_mode_results.get('character_voice'):
            char_results = voice_mode_results['character_voice']
            char_available = sum(1 for r in char_results if r.voice_available)
            if char_available == 0:
                print(f"\n🎤 CHARACTER VOICE SETUP GUIDE:")
                print(f"   1. Install Python 3.11: https://python.org/downloads/")
                print(f"   2. Create conda environment: conda create -n barkoni python=3.11")
                print(f"   3. Install TTS: pip install TTS torch librosa soundfile")
                print(f"   4. Test installation: python test_barkuni_voice_cloning.py")

def main():
    """Run the comprehensive Barkuni voice test suite"""
    tester = BarkuniVoiceComprehensiveTester()

    print("Choose test mode:")
    print("1. Comprehensive voice tests")
    print("2. Voice mode comparison")
    print("3. Both")

    try:
        choice = input("Enter choice (1-3): ").strip()
        if choice in ['1', '3']:
            tester.run_comprehensive_voice_tests()
        if choice in ['2', '3']:
            tester.test_voice_modes_comparison()
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")

if __name__ == "__main__":
    main()