"""
Complete test suite for Iran System Encoding package
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import iran_encoding
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Add current directory to path to allow direct imports of other test modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_converter import TestConverter
from test_encoding_functions import TestEncodingFunctions
from test_exact_behavior import TestExactBehavior
from test_iran_system_v1 import TestIranSystemV1
from test_mixed_reversal import TestMixedReversal


def create_test_suite():
    """Create a complete test suite combining all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestConverter, TestEncodingFunctions, TestExactBehavior,
        TestIranSystemV1, TestMixedReversal
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_all_tests():
    """Run all tests and return success status."""
    print("Running complete Iran System Encoding test suite...")
    print("=" * 60)
    
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
