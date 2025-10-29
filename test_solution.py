#!/usr/bin/env python3
"""Basic tests for TTS solution."""

import sys
import os
import subprocess
from pathlib import Path


def run_command(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"


def test_imports():
    print("Test 1: Checking imports...")
    try:
        import torch
        import numpy
        import scipy
        print("  ✓ Core dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_help():
    print("\nTest 2: Checking help command...")
    code, stdout, stderr = run_command("python solution.py --help")
    if code == 0 and "text-to-speech" in stdout.lower():
        print("  ✓ Help command works")
        return True
    else:
        print(f"  ✗ Help command failed (exit code: {code})")
        return False


def test_argument_parsing():
    print("\nTest 3: Checking argument validation...")
    code, stdout, stderr = run_command("python solution.py")
    if code != 0:
        print("  ✓ Correctly rejects missing arguments")
        return True
    else:
        print("  ✗ Should reject missing arguments")
        return False


def test_file_structure():
    print("\nTest 4: Checking file structure...")
    required_files = [
        "solution.py",
        "requirements.txt",
        "README.md",
        ".gitignore"
    ]

    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file} exists")
        else:
            print(f"  ✗ {file} missing")
            all_exist = False

    return all_exist


def test_code_quality():
    print("\nTest 5: Checking code quality...")

    with open("solution.py", "r") as f:
        code = f.read()

    checks = [
        ("Docstrings present", '"""' in code),
        ("Error handling present", "try:" in code and "except" in code),
        ("Argument parser present", "argparse" in code),
        ("Main function present", "def main()" in code),
        ("Class defined", "class EmotionalTTS" in code),
    ]

    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ✗ {check_name}")
            all_passed = False

    return all_passed


def main():
    print("=" * 60)
    print("TTS Solution Test Suite")
    print("=" * 60)

    tests = [
        test_file_structure,
        test_code_quality,
        test_help,
        test_argument_parsing,
        test_imports,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ✗ Test crashed: {e}")

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n✓ All tests passed! Solution is ready to use.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run: python solution.py 'Hello world' hello.wav")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
