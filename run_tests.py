#!/usr/bin/env python3
"""
Barkoni Test Runner
Comprehensive test suite runner for the Barkoni Voice Cloning Chatbot
"""

import sys
import os
import argparse
import importlib.util
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def discover_tests(test_dir: Path) -> List[Path]:
    """Discover all test files in a directory"""
    test_files = []
    if test_dir.exists():
        for test_file in test_dir.glob("test_*.py"):
            test_files.append(test_file)
    return sorted(test_files)

def run_test_file(test_file: Path) -> Dict[str, Any]:
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {test_file.name}")
    print(f"{'='*60}")

    result = {
        'file': test_file.name,
        'success': False,
        'error': None
    }

    try:
        # Import and run the test module
        spec = importlib.util.spec_from_file_location(test_file.stem, test_file)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load {test_file}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Try to run main function if it exists
        if hasattr(module, 'main'):
            module.main()
        else:
            print(f"WARNING: No main() function found in {test_file.name}")

        result['success'] = True
        print(f"\nSUCCESS: {test_file.name} completed successfully")

    except Exception as e:
        result['error'] = str(e)
        print(f"\nFAILED: {test_file.name} failed: {e}")

    return result

def run_test_category(category: str, test_dirs: Dict[str, Path]) -> List[Dict[str, Any]]:
    """Run all tests in a category"""
    if category not in test_dirs:
        print(f"ERROR: Unknown test category: {category}")
        return []

    test_dir = test_dirs[category]
    test_files = discover_tests(test_dir)

    if not test_files:
        print(f"WARNING: No test files found in {test_dir}")
        return []

    print(f"\nRUNNING {category.upper()} TESTS")
    print(f"Found {len(test_files)} test files")

    results = []
    for test_file in test_files:
        result = run_test_file(test_file)
        results.append(result)

    return results

def generate_test_report(results: List[Dict[str, Any]]):
    """Generate a comprehensive test report"""
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE TEST REPORT")
    print(f"{'='*80}")

    if not results:
        print("ERROR: No test results to report")
        return

    total_tests = len(results)
    successful_tests = len([r for r in results if r['success']])
    failed_tests = total_tests - successful_tests

    print(f"SUMMARY:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Successful: {successful_tests} ({successful_tests/total_tests*100:.1f}%)")
    print(f"   Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")

    if failed_tests > 0:
        print(f"\nFAILED TESTS:")
        for result in results:
            if not result['success']:
                print(f"   - {result['file']}: {result['error']}")

    if successful_tests > 0:
        print(f"\nSUCCESSFUL TESTS:")
        for result in results:
            if result['success']:
                print(f"   - {result['file']}")

    # Overall assessment
    if successful_tests == total_tests:
        print(f"\nALL TESTS PASSED! Barkuni is working perfectly!")
    elif successful_tests >= total_tests * 0.8:
        print(f"\nMOSTLY SUCCESSFUL! Most tests passed.")
    elif successful_tests >= total_tests * 0.5:
        print(f"\nMIXED RESULTS. Some issues need attention.")
    else:
        print(f"\nSIGNIFICANT ISSUES. Multiple tests failed.")

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description='Run Barkoni chatbot tests')
    parser.add_argument('category', nargs='?', choices=['unit', 'integration', 'voice', 'personality', 'all'],
                       default='all', help='Test category to run')
    parser.add_argument('--list', action='store_true', help='List available tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Define test directories
    test_dirs = {
        'unit': project_root / 'tests' / 'unit',
        'integration': project_root / 'tests' / 'integration',
        'voice': project_root / 'tests' / 'voice',
        'personality': project_root / 'tests' / 'personality'
    }

    print("BARKONI VOICE CLONING CHATBOT TEST SUITE")
    print("=" * 50)

    if args.list:
        print("AVAILABLE TESTS:")
        for category, test_dir in test_dirs.items():
            test_files = discover_tests(test_dir)
            print(f"\n{category.upper()} ({len(test_files)} tests):")
            for test_file in test_files:
                print(f"   - {test_file.name}")
        return

    # Run tests
    all_results = []

    if args.category == 'all':
        for category in test_dirs.keys():
            results = run_test_category(category, test_dirs)
            all_results.extend(results)
    else:
        results = run_test_category(args.category, test_dirs)
        all_results.extend(results)

    # Generate report
    generate_test_report(all_results)

    print(f"\nTEST SUITE COMPLETED")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest runner failed: {e}")
        sys.exit(1)