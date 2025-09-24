#!/usr/bin/env python3
"""
Comprehensive tests to verify Barkuni is speaking in Hebrew
and maintaining authentic character personality
"""

import sys
import os
import re
import time
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from dotenv import load_dotenv
from main import CharacterVoiceChatbot

# Load environment variables
load_dotenv()

@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    input_text: str
    response: str
    hebrew_score: float
    character_score: float
    voice_output: bool
    passed: bool
    details: Dict[str, Any]

class BarkuniHebrewCharacterTester:
    """Test suite for Barkuni Hebrew language and character validation"""

    def __init__(self):
        self.chatbot = None
        self.test_results: List[TestResult] = []

        # Hebrew words and expressions Barkuni should use
        self.hebrew_expressions = [
            'achla', 'yalla', 'sababa', 'eizeh', 'kef', 'shalom',
            'toda', 'bevakasha', 'ma nishma', 'ma kore', 'chabibi',
            'achi', 'metuka', 'magniv', 'chazak', 'beseder'
        ]

        # Character traits Barkuni should display
        self.character_traits = {
            'hyperactive': ['!', 'WOOO', 'YESSS', 'BOOM', 'WOW'],
            'gaming': ['game', 'play', 'stream', 'gaming', 'gamer', 'level'],
            'israeli_slang': ['achi', 'chabibi', 'metuka', 'magniv'],
            'excitement': ['!', '?', 'amazing', 'awesome', 'incredible'],
            'sound_effects': ['HAHA', 'WOOO', 'BOOM', 'YESSS', 'WOW']
        }

    def setup_chatbot(self, use_character_voice: bool = False) -> bool:
        """Initialize the chatbot for testing"""
        try:
            self.chatbot = CharacterVoiceChatbot(
                character_name="Barkuni",
                claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
                use_character_voice=use_character_voice,
                ai_provider="claude"
            )
            return True
        except Exception as e:
            print(f"❌ Failed to initialize chatbot: {e}")
            return False

    def analyze_hebrew_content(self, text: str) -> Tuple[float, Dict[str, Any]]:
        """Analyze Hebrew content in the response"""
        text_lower = text.lower()
        details = {
            'hebrew_words_found': [],
            'hebrew_word_count': 0,
            'total_words': len(text.split()),
            'hebrew_percentage': 0.0
        }

        # Count Hebrew expressions
        for word in self.hebrew_expressions:
            if word in text_lower:
                details['hebrew_words_found'].append(word)

        details['hebrew_word_count'] = len(details['hebrew_words_found'])

        if details['total_words'] > 0:
            details['hebrew_percentage'] = (details['hebrew_word_count'] / details['total_words']) * 100

        # Hebrew script detection (actual Hebrew characters)
        hebrew_chars = re.findall(r'[\u0590-\u05FF]+', text)
        details['hebrew_script_found'] = len(hebrew_chars) > 0
        details['hebrew_characters'] = hebrew_chars

        # Calculate Hebrew score (0-100)
        hebrew_score = 0
        if details['hebrew_word_count'] > 0:
            hebrew_score += min(details['hebrew_word_count'] * 15, 60)  # Up to 60 points for expressions
        if details['hebrew_script_found']:
            hebrew_score += 40  # 40 points for Hebrew script

        return min(hebrew_score, 100), details

    def analyze_character_traits(self, text: str) -> Tuple[float, Dict[str, Any]]:
        """Analyze Barkuni character traits in the response"""
        text_upper = text.upper()
        text_lower = text.lower()

        details = {
            'traits_found': {},
            'trait_scores': {},
            'total_trait_indicators': 0
        }

        total_score = 0
        max_score = len(self.character_traits) * 20  # 20 points per trait category

        for trait_name, indicators in self.character_traits.items():
            found_indicators = []
            trait_count = 0

            for indicator in indicators:
                if indicator.upper() in text_upper or indicator.lower() in text_lower:
                    found_indicators.append(indicator)
                    trait_count += 1

            details['traits_found'][trait_name] = found_indicators
            details['trait_scores'][trait_name] = min(trait_count * 5, 20)  # Max 20 per trait
            total_score += details['trait_scores'][trait_name]
            details['total_trait_indicators'] += trait_count

        character_score = (total_score / max_score) * 100 if max_score > 0 else 0

        return character_score, details

    def test_voice_output(self, text: str) -> bool:
        """Test if voice output is working"""
        if not self.chatbot or not self.chatbot.voice_ready:
            return False

        try:
            # Attempt to speak the text (this would be audible in real environment)
            self.chatbot.speak(text)
            return True
        except Exception as e:
            print(f"Voice output error: {e}")
            return False

    def run_single_test(self, test_name: str, input_text: str, expected_traits: List[str] = None) -> TestResult:
        """Run a single test case"""
        print(f"\n🧪 Running Test: {test_name}")
        print(f"📝 Input: '{input_text}'")

        if not self.chatbot:
            return TestResult(
                test_name=test_name,
                input_text=input_text,
                response="",
                hebrew_score=0,
                character_score=0,
                voice_output=False,
                passed=False,
                details={"error": "Chatbot not initialized"}
            )

        try:
            # Generate response
            response = self.chatbot.generate_response(input_text)
            print(f"🎭 Barkuni Response: {response}")

            # Analyze Hebrew content
            hebrew_score, hebrew_details = self.analyze_hebrew_content(response)

            # Analyze character traits
            character_score, character_details = self.analyze_character_traits(response)

            # Test voice output
            voice_output = self.test_voice_output(response)

            # Determine if test passed
            passed = (
                hebrew_score >= 30 and  # At least 30% Hebrew score
                character_score >= 40 and  # At least 40% character score
                len(response) > 10  # Response is substantial
            )

            result = TestResult(
                test_name=test_name,
                input_text=input_text,
                response=response,
                hebrew_score=hebrew_score,
                character_score=character_score,
                voice_output=voice_output,
                passed=passed,
                details={
                    "hebrew_analysis": hebrew_details,
                    "character_analysis": character_details,
                    "response_length": len(response)
                }
            )

            # Print analysis
            print(f"📊 Hebrew Score: {hebrew_score:.1f}/100")
            print(f"🎭 Character Score: {character_score:.1f}/100")
            print(f"🔊 Voice Output: {'✅' if voice_output else '❌'}")
            print(f"✅ Test Result: {'PASSED' if passed else 'FAILED'}")

            return result

        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            return TestResult(
                test_name=test_name,
                input_text=input_text,
                response="",
                hebrew_score=0,
                character_score=0,
                voice_output=False,
                passed=False,
                details={"error": str(e)}
            )

    def run_comprehensive_test_suite(self):
        """Run comprehensive test suite"""
        print("🚀 STARTING COMPREHENSIVE BARKUNI HEBREW CHARACTER TEST SUITE")
        print("=" * 70)

        # Initialize chatbot
        if not self.setup_chatbot(use_character_voice=False):
            print("❌ Failed to setup chatbot. Exiting tests.")
            return

        print(f"✅ Chatbot initialized successfully")
        print(f"🎯 AI Provider: {self.chatbot.ai_provider}")
        print(f"🔊 Voice Ready: {'Yes' if self.chatbot.voice_ready else 'No'}")

        # Define test cases
        test_cases = [
            {
                "name": "Greeting Test",
                "input": "shalom barkuni! ma nishma?",
                "expected_traits": ["hebrew", "greeting", "excitement"]
            },
            {
                "name": "Gaming Question",
                "input": "what's your favorite game to play?",
                "expected_traits": ["gaming", "hyperactive", "hebrew_expressions"]
            },
            {
                "name": "Hebrew Response Test",
                "input": "תגיד לי משהו בעברית",
                "expected_traits": ["hebrew_script", "israeli_slang"]
            },
            {
                "name": "Energy Level Test",
                "input": "how are you feeling today?",
                "expected_traits": ["hyperactive", "sound_effects", "hebrew"]
            },
            {
                "name": "Stream Discussion",
                "input": "tell me about streaming and content creation",
                "expected_traits": ["gaming", "excitement", "hebrew"]
            },
            {
                "name": "Israeli Culture",
                "input": "what do you love about Israel?",
                "expected_traits": ["hebrew", "israeli_slang", "excitement"]
            },
            {
                "name": "Casual Chat",
                "input": "yalla, let's chat about something fun",
                "expected_traits": ["hebrew", "hyperactive", "sound_effects"]
            },
            {
                "name": "Technology Topic",
                "input": "what do you think about AI and technology?",
                "expected_traits": ["hebrew", "excitement", "gaming"]
            }
        ]

        # Run all tests
        for test_case in test_cases:
            result = self.run_single_test(
                test_case["name"],
                test_case["input"],
                test_case.get("expected_traits", [])
            )
            self.test_results.append(result)

            # Small delay between tests
            time.sleep(1)

        # Generate comprehensive report
        self.generate_test_report()

    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 70)
        print("📋 COMPREHENSIVE TEST REPORT")
        print("=" * 70)

        if not self.test_results:
            print("❌ No test results to report")
            return

        # Summary statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.passed)
        avg_hebrew_score = sum(result.hebrew_score for result in self.test_results) / total_tests
        avg_character_score = sum(result.character_score for result in self.test_results) / total_tests
        voice_working_count = sum(1 for result in self.test_results if result.voice_output)

        print(f"📊 SUMMARY STATISTICS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed Tests: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"   Average Hebrew Score: {avg_hebrew_score:.1f}/100")
        print(f"   Average Character Score: {avg_character_score:.1f}/100")
        print(f"   Voice Output Working: {voice_working_count}/{total_tests} tests")

        # Detailed results
        print(f"\n📝 DETAILED TEST RESULTS:")
        print("-" * 70)

        for i, result in enumerate(self.test_results, 1):
            status = "✅ PASSED" if result.passed else "❌ FAILED"
            print(f"{i}. {result.test_name}: {status}")
            print(f"   Input: {result.input_text}")
            print(f"   Hebrew: {result.hebrew_score:.1f}/100 | Character: {result.character_score:.1f}/100 | Voice: {'✅' if result.voice_output else '❌'}")

            if result.response:
                preview = result.response[:100] + "..." if len(result.response) > 100 else result.response
                print(f"   Response: {preview}")

            if result.details.get("hebrew_analysis"):
                hebrew_words = result.details["hebrew_analysis"]["hebrew_words_found"]
                if hebrew_words:
                    print(f"   Hebrew Words Found: {', '.join(hebrew_words)}")

            print()

        # Hebrew analysis summary
        print(f"🔍 HEBREW LANGUAGE ANALYSIS:")
        all_hebrew_words = set()
        hebrew_script_count = 0

        for result in self.test_results:
            if result.details.get("hebrew_analysis"):
                hebrew_analysis = result.details["hebrew_analysis"]
                all_hebrew_words.update(hebrew_analysis["hebrew_words_found"])
                if hebrew_analysis.get("hebrew_script_found"):
                    hebrew_script_count += 1

        print(f"   Unique Hebrew Expressions Used: {len(all_hebrew_words)}")
        print(f"   Hebrew Expressions: {', '.join(sorted(all_hebrew_words))}")
        print(f"   Hebrew Script Responses: {hebrew_script_count}/{total_tests}")

        # Character traits analysis
        print(f"\n🎭 CHARACTER TRAITS ANALYSIS:")
        all_traits = {}

        for result in self.test_results:
            if result.details.get("character_analysis"):
                traits = result.details["character_analysis"]["traits_found"]
                for trait_name, indicators in traits.items():
                    if trait_name not in all_traits:
                        all_traits[trait_name] = set()
                    all_traits[trait_name].update(indicators)

        for trait_name, indicators in all_traits.items():
            print(f"   {trait_name.capitalize()}: {', '.join(sorted(indicators)) if indicators else 'None found'}")

        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")

        if avg_hebrew_score < 50:
            print("   - Hebrew usage could be improved. Add more Hebrew expressions and responses.")

        if avg_character_score < 60:
            print("   - Character personality could be more pronounced. Add more hyperactive traits and sound effects.")

        if voice_working_count < total_tests:
            print("   - Voice output issues detected. Check TTS configuration.")

        if passed_tests == total_tests:
            print("   🎉 All tests passed! Barkuni is successfully speaking Hebrew with authentic character!")

        # Overall assessment
        overall_score = (avg_hebrew_score + avg_character_score) / 2
        print(f"\n🏆 OVERALL ASSESSMENT:")

        if overall_score >= 80:
            assessment = "EXCELLENT - Authentic Barkuni character with strong Hebrew integration"
        elif overall_score >= 60:
            assessment = "GOOD - Character traits present with moderate Hebrew usage"
        elif overall_score >= 40:
            assessment = "FAIR - Some character traits, Hebrew usage needs improvement"
        else:
            assessment = "NEEDS IMPROVEMENT - Character and Hebrew traits need significant work"

        print(f"   Overall Score: {overall_score:.1f}/100")
        print(f"   Assessment: {assessment}")

def main():
    """Run the comprehensive Barkuni Hebrew Character test suite"""
    tester = BarkuniHebrewCharacterTester()
    tester.run_comprehensive_test_suite()

if __name__ == "__main__":
    main()