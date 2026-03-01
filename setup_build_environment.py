#! /usr/bin/env python3
"""Backward compatible wrapper for common build environment setup."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import subprocess
import sys


def main(args: list[str]) -> int:
    """Run common build tool setup_build_environment.py with provided args."""
    script_path = (
        Path(__file__).resolve().parent /
        'common_build_tools' /
        'src' /
        'setup_build_environment.py'
    )
    command = [sys.executable, str(script_path), *args]
    process = subprocess.run(command, check=False)
    return process.returncode


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
