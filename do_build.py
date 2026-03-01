#! /usr/bin/env python3
"""Thin wrapper calling common_build_tools/src/do_build.py."""

from pathlib import Path
import subprocess
import sys


def main(args: list[str]) -> int:
    """Run the target script in common_build_tools/src."""
    script_path = (
        Path(__file__).resolve().parent /
        'common_build_tools' /
        'src' /
        'do_build.py'
    )
    process = subprocess.run(
        [sys.executable, str(script_path), *args],
        check=False,
    )
    return process.returncode


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
