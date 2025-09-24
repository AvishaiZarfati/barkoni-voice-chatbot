#!/usr/bin/env python3
"""
Deep personality tests for Barkuni character validation
Tests authentic character traits, energy levels, and behavioral patterns
"""

import sys
import os
import time
import re
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
class PersonalityTestResult:
    """Personality test result data structure"""
    test_name: str
    category: str
    input_text: str
    response: str
    energy_score: float
    authenticity_score: float
    hebrew_integration: float
    overall_score: float
    passed: bool
    traits_detected: List[str]
    recommendations: List[str]

class BarkuniPersonalityTester:
    """Deep personality testing for Barkuni character authenticity"""

    def __init__(self):
        self.chatbot = None
        self.test_results: List[PersonalityTestResult] = []

        # Define Barkuni's authentic personality patterns
        self.personality_patterns = {
            'hyperactive_energy': {
                'indicators': ['!', '!!', '!!!', 'WOOO', 'YESSS', 'BOOM', 'WOW', 'AMAZING', 'INCREDIBLE'],
                'weight': 25,
                'description': 'High-energy expressions and exclamations'
            },
            'gaming_enthusiasm': {
                'indicators': ['game', 'gaming', 'play', 'stream', 'streaming', 'level', 'boss', 'epic', 'legend'],
                'weight': 20,
                'description': 'Gaming-related vocabulary and enthusiasm'
            },
            'israeli_expressions': {
                'indicators': ['achla', 'yalla', 'sababa', 'eizeh kef', 'ma nishma', 'toda', 'shalom', 'chabibi', 'achi'],
                'weight': 25,
                'description': 'Authentic Israeli Hebrew expressions'
            },
            'stream_consciousness': {
                'indicators': ['and then', 'also', 'but wait', 'oh and', 'by the way', 'speaking of', 'you know what'],
                'weight': 15,
                'description': 'Stream-of-consciousness speaking patterns'
            },
            'sound_effects': {
                'indicators': ['HAHA', 'HEHE', 'BOOM', 'POW', 'WHOOSH', 'DING', 'beep', 'buzz'],
                'weight': 15,
                'description': 'Characteristic sound effects and verbal sounds'
            }
        }

        # Behavioral test scenarios
        self.test_scenarios = [
            {
                'category': 'Energy Level',
                'tests': [
                    {'name': 'Morning Greeting', 'input': 'Good morning Barkuni!', 'expected': ['hyperactive_energy', 'israeli_expressions']},
                    {'name': 'Excitement Response', 'input': 'I just got a new game!', 'expected': ['hyperactive_energy', 'gaming_enthusiasm']},
                    {'name': 'Energy Sustain', 'input': 'How are you feeling today?', 'expected': ['hyperactive_energy', 'sound_effects']}
                ]
            },
            {
                'category': 'Gaming Personality',
                'tests': [
                    {'name': 'Favorite Game', 'input': 'What\'s your favorite game?', 'expected': ['gaming_enthusiasm', 'hyperactive_energy']},
                    {'name': 'Gaming Advice', 'input': 'Any tips for gaming?', 'expected': ['gaming_enthusiasm', 'stream_consciousness']},
                    {'name': 'Stream Discussion', 'input': 'Tell me about streaming', 'expected': ['gaming_enthusiasm', 'israeli_expressions']}
                ]
            },
            {
                'category': 'Hebrew Integration',
                'tests': [
                    {'name': 'Hebrew Greeting', 'input': 'Shalom! Ma nishma?', 'expected': ['israeli_expressions', 'hyperactive_energy']},
                    {'name': 'Israeli Culture', 'input': 'What do you love about Israel?', 'expected': ['israeli_expressions', 'hyperactive_energy']},
                    {'name': 'Hebrew Mixing', 'input': 'Yalla, let\'s chat!', 'expected': ['israeli_expressions', 'stream_consciousness']}
                ]
            },
            {
                'category': 'Conversational Flow',
                'tests': [
                    {'name': 'Topic Jumping', 'input': 'What do you think about technology?', 'expected': ['stream_consciousness', 'hyperactive_energy']},
                    {'name': 'Storytelling', 'input': 'Tell me a funny story', 'expected': ['stream_consciousness', 'sound_effects']},
                    {'name': 'Random Chat', 'input': 'Just wanted to chat randomly', 'expected': ['hyperactive_energy', 'israeli_expressions']}
                ]
            },
            {
                'category': 'Authentic Reactions',
                'tests': [
                    {'name': 'Surprise Reaction', 'input': 'Guess what? I won the lottery!', 'expected': ['hyperactive_energy', 'sound_effects']},
                    {'name': 'Confusion Response', 'input': 'I don\'t understand quantum physics', 'expected': ['hyperactive_energy', 'israeli_expressions']},
                    {'name': 'Agreement Style', 'input': 'Gaming is the best hobby ever!', 'expected': ['gaming_enthusiasm', 'israeli_expressions']}
                ]
            }
        ]

    def setup_chatbot(self) -> bool:
        """Initialize the chatbot for personality testing"""
        try:
            self.chatbot = CharacterVoiceChatbot(
                character_name="Barkuni",
                claude_api_key=os.getenv('ANTHROPIC_API_KEY'),
                use_character_voice=False,
                ai_provider="claude"
            )
            return True
        except Exception as e:
            print(f"❌ Failed to initialize chatbot: {e}")
            return False

    def analyze_personality_patterns(self, text: str) -> Tuple[Dict[str, float], List[str], float]:
        """Analyze personality patterns in the response"""
        text_lower = text.lower()
        text_upper = text.upper()

        pattern_scores = {}
        detected_traits = []
        total_score = 0

        for pattern_name, pattern_data in self.personality_patterns.items():
            indicators_found = []
            score = 0

            for indicator in pattern_data['indicators']:
                if indicator.lower() in text_lower or indicator.upper() in text_upper:
                    indicators_found.append(indicator)
                    score += 10  # 10 points per indicator found

            # Cap the score at the pattern's weight
            score = min(score, pattern_data['weight'])
            pattern_scores[pattern_name] = score

            if indicators_found:
                detected_traits.append(f"{pattern_name}: {', '.join(indicators_found)}")

            total_score += score

        return pattern_scores, detected_traits, total_score

    def calculate_energy_score(self, text: str) -> float:
        """Calculate energy level score based on text analysis"""
        # Count exclamation marks
        exclamation_count = text.count('!')
        # Count capital words (excluding normal capitalization)
        capital_words = len(re.findall(r'\b[A-Z]{2,}\b', text))
        # Count energy words
        energy_words = ['amazing', 'awesome', 'incredible', 'fantastic', 'wow', 'yes', 'yeah']
        energy_count = sum(1 for word in energy_words if word in text.lower())

        # Calculate energy score (0-100)
        energy_score = min(
            (exclamation_count * 10) +
            (capital_words * 15) +
            (energy_count * 8),
            100
        )

        return energy_score

    def calculate_authenticity_score(self, response: str, expected_patterns: List[str]) -> float:
        """Calculate how authentic the response is to Barkuni's character"""
        pattern_scores, _, total_score = self.analyze_personality_patterns(response)

        # Check if expected patterns are present
        expected_score = 0
        for expected in expected_patterns:
            if expected in pattern_scores and pattern_scores[expected] > 0:
                expected_score += 20

        # Combine total pattern score and expected pattern fulfillment
        authenticity = min(total_score + expected_score, 100)
        return authenticity

    def calculate_hebrew_integration(self, text: str) -> float:
        """Calculate Hebrew language integration score"""
        hebrew_expressions = ['achla', 'yalla', 'sababa', 'eizeh', 'kef', 'shalom', 'toda', 'chabibi', 'achi']
        hebrew_count = sum(1 for expr in hebrew_expressions if expr in text.lower())

        # Hebrew script detection
        hebrew_chars = re.findall(r'[\u0590-\u05FF]+', text)
        has_hebrew_script = len(hebrew_chars) > 0

        hebrew_score = (hebrew_count * 15) + (40 if has_hebrew_script else 0)
        return min(hebrew_score, 100)

    def run_personality_test(self, test_name: str, category: str, input_text: str, expected_patterns: List[str]) -> PersonalityTestResult:
        """Run a single personality test"""
        print(f"\n🎭 Testing: {test_name} ({category})")
        print(f"📝 Input: '{input_text}'")

        if not self.chatbot:
            return PersonalityTestResult(
                test_name=test_name,
                category=category,
                input_text=input_text,
                response="",
                energy_score=0,
                authenticity_score=0,
                hebrew_integration=0,
                overall_score=0,
                passed=False,
                traits_detected=[],
                recommendations=["Chatbot not initialized"]
            )

        try:
            # Generate response
            response = self.chatbot.generate_response(input_text)
            print(f"🎤 Barkuni: {response}")

            # Calculate scores
            energy_score = self.calculate_energy_score(response)
            authenticity_score = self.calculate_authenticity_score(response, expected_patterns)
            hebrew_integration = self.calculate_hebrew_integration(response)

            # Calculate overall score
            overall_score = (energy_score * 0.4 + authenticity_score * 0.4 + hebrew_integration * 0.2)

            # Analyze personality patterns
            _, traits_detected, _ = self.analyze_personality_patterns(response)

            # Determine pass/fail
            passed = (
                energy_score >= 30 and
                authenticity_score >= 40 and
                overall_score >= 50
            )

            # Generate recommendations
            recommendations = []
            if energy_score < 30:
                recommendations.append("Increase energy level with more exclamations and enthusiasm")
            if authenticity_score < 40:
                recommendations.append("Add more characteristic Barkuni traits and expressions")
            if hebrew_integration < 20:
                recommendations.append("Integrate more Hebrew expressions and language")
            if not traits_detected:
                recommendations.append("Response lacks distinctive personality traits")

            result = PersonalityTestResult(
                test_name=test_name,
                category=category,
                input_text=input_text,
                response=response,
                energy_score=energy_score,
                authenticity_score=authenticity_score,
                hebrew_integration=hebrew_integration,
                overall_score=overall_score,
                passed=passed,
                traits_detected=traits_detected,
                recommendations=recommendations
            )

            # Print scores
            print(f"⚡ Energy: {energy_score:.1f}/100")
            print(f"🎯 Authenticity: {authenticity_score:.1f}/100")
            print(f"🇮🇱 Hebrew Integration: {hebrew_integration:.1f}/100")
            print(f"🏆 Overall: {overall_score:.1f}/100 - {'✅ PASSED' if passed else '❌ FAILED'}")

            if traits_detected:
                print(f"🔍 Traits Detected: {len(traits_detected)}")

            return result

        except Exception as e:
            print(f"❌ Test failed: {e}")
            return PersonalityTestResult(
                test_name=test_name,
                category=category,
                input_text=input_text,
                response="",
                energy_score=0,
                authenticity_score=0,
                hebrew_integration=0,
                overall_score=0,
                passed=False,
                traits_detected=[],
                recommendations=[f"Error: {str(e)}"]
            )

    def run_comprehensive_personality_tests(self):
        """Run the complete personality test suite"""
        print("🚀 STARTING COMPREHENSIVE BARKUNI PERSONALITY TEST SUITE")
        print("=" * 80)

        # Initialize chatbot
        if not self.setup_chatbot():
            print("❌ Failed to setup chatbot. Exiting tests.")
            return

        print(f"✅ Chatbot initialized successfully")
        print(f"🤖 AI Provider: {self.chatbot.ai_provider}")

        # Run all test scenarios
        total_tests = 0
        for scenario in self.test_scenarios:
            print(f"\n{'='*60}")
            print(f"📂 CATEGORY: {scenario['category'].upper()}")
            print(f"{'='*60}")

            for test in scenario['tests']:
                result = self.run_personality_test(
                    test['name'],
                    scenario['category'],
                    test['input'],
                    test['expected']
                )
                self.test_results.append(result)
                total_tests += 1

                # Small delay between tests
                time.sleep(1)

        # Generate comprehensive report
        self.generate_personality_report()

    def generate_personality_report(self):
        """Generate comprehensive personality test report"""
        print("\n" + "=" * 80)
        print("📋 COMPREHENSIVE BARKUNI PERSONALITY REPORT")
        print("=" * 80)

        if not self.test_results:
            print("❌ No test results to report")
            return

        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.passed)

        avg_energy = sum(result.energy_score for result in self.test_results) / total_tests
        avg_authenticity = sum(result.authenticity_score for result in self.test_results) / total_tests
        avg_hebrew = sum(result.hebrew_integration for result in self.test_results) / total_tests
        avg_overall = sum(result.overall_score for result in self.test_results) / total_tests

        # Summary
        print(f"📊 SUMMARY STATISTICS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed Tests: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"   Average Energy Score: {avg_energy:.1f}/100")
        print(f"   Average Authenticity Score: {avg_authenticity:.1f}/100")
        print(f"   Average Hebrew Integration: {avg_hebrew:.1f}/100")
        print(f"   Average Overall Score: {avg_overall:.1f}/100")

        # Category breakdown
        categories = {}
        for result in self.test_results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)

        print(f"\n📈 CATEGORY BREAKDOWN:")
        for category, results in categories.items():
            passed = sum(1 for r in results if r.passed)
            avg_score = sum(r.overall_score for r in results) / len(results)
            print(f"   {category}: {passed}/{len(results)} passed (avg: {avg_score:.1f}/100)")

        # Detailed results
        print(f"\n📝 DETAILED RESULTS BY CATEGORY:")
        print("-" * 80)

        for category, results in categories.items():
            print(f"\n🏷️  {category.upper()}")
            print("-" * 40)

            for result in results:
                status = "✅ PASSED" if result.passed else "❌ FAILED"
                print(f"   {result.test_name}: {status}")
                print(f"      Energy: {result.energy_score:.0f} | Authenticity: {result.authenticity_score:.0f} | Hebrew: {result.hebrew_integration:.0f} | Overall: {result.overall_score:.0f}")

                if result.traits_detected:
                    print(f"      Traits: {len(result.traits_detected)} detected")

                if result.recommendations and not result.passed:
                    print(f"      Recommendations: {'; '.join(result.recommendations[:2])}")
                print()

        # Pattern analysis
        print(f"🔍 PERSONALITY PATTERN ANALYSIS:")
        all_detected_traits = []
        for result in self.test_results:
            all_detected_traits.extend(result.traits_detected)

        trait_frequency = {}
        for trait in all_detected_traits:
            trait_name = trait.split(':')[0]
            trait_frequency[trait_name] = trait_frequency.get(trait_name, 0) + 1

        print(f"   Most Frequent Traits:")
        for trait, count in sorted(trait_frequency.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_tests) * 100
            print(f"      {trait}: {count}/{total_tests} tests ({percentage:.1f}%)")

        # Recommendations
        print(f"\n💡 OVERALL RECOMMENDATIONS:")

        if avg_energy < 50:
            print("   ⚡ ENERGY: Increase hyperactive expressions, exclamations, and enthusiasm")

        if avg_authenticity < 60:
            print("   🎯 AUTHENTICITY: Strengthen character-specific traits and behavioral patterns")

        if avg_hebrew < 40:
            print("   🇮🇱 HEBREW: Integrate more Hebrew expressions and Israeli cultural references")

        if passed_tests == total_tests:
            print("   🎉 EXCELLENT: All personality tests passed! Barkuni character is authentic!")
        elif passed_tests >= total_tests * 0.8:
            print("   👍 GOOD: Most tests passed, minor personality adjustments needed")
        elif passed_tests >= total_tests * 0.6:
            print("   ⚠️  MODERATE: Character traits present but need strengthening")
        else:
            print("   🚨 NEEDS WORK: Significant personality development required")

        # Final assessment
        print(f"\n🏆 FINAL PERSONALITY ASSESSMENT:")

        if avg_overall >= 80:
            assessment = "EXCELLENT - Authentic Barkuni personality with strong character consistency"
            grade = "A+"
        elif avg_overall >= 70:
            assessment = "VERY GOOD - Strong personality traits with room for minor improvements"
            grade = "A"
        elif avg_overall >= 60:
            assessment = "GOOD - Character traits present, moderate improvements needed"
            grade = "B"
        elif avg_overall >= 50:
            assessment = "FAIR - Basic character elements, significant improvements needed"
            grade = "C"
        else:
            assessment = "NEEDS SIGNIFICANT IMPROVEMENT - Character personality requires major development"
            grade = "D"

        print(f"   Overall Personality Score: {avg_overall:.1f}/100")
        print(f"   Personality Grade: {grade}")
        print(f"   Assessment: {assessment}")

def main():
    """Run the comprehensive Barkuni personality test suite"""
    tester = BarkuniPersonalityTester()
    tester.run_comprehensive_personality_tests()

if __name__ == "__main__":
    main()