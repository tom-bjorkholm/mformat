#! /usr/bin/env python3
"""Helper for thin root wrapper scripts."""

from pathlib import Path
import subprocess
import sys


def run_target_script(target_script_name: str, args: list[str]) -> int:
    """Run one common_build_tools/src script from repository root."""
    script_path = (
        Path(__file__).resolve().parent /
        'common_build_tools' /
        'src' /
        target_script_name
    )
    process = subprocess.run(
        [sys.executable, str(script_path), *args],
        check=False,
    )
    return process.returncode
