"""
Test runner script for Barie AI test suite
"""
import sys
import subprocess
from pathlib import Path


def main():
    """Main test runner"""
    # Get command line arguments
    args = sys.argv[1:]
    
    # Default pytest arguments
    pytest_args = [
        "pytest",
        "-v",
        "--tb=short",
        "--html=reports/report.html",
        "--self-contained-html"
    ]
    
    # Add custom arguments
    if args:
        pytest_args.extend(args)
    else:
        # Default: run all tests
        pytest_args.append("tests/")
    
    # Run pytest
    print("Running tests with command:", " ".join(pytest_args))
    result = subprocess.run(pytest_args)
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())

