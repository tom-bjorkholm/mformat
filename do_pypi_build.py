#!/usr/bin/env python3
"""Build for PyPI: clean build twice, optionally upload.

Runs the full clean build process twice (the second build
ensures the README contains the test summary from the
first build), and optionally uploads to PyPI via twine.

Usage:
    python3 do_pypi_build.py [python_version] [twine]

Examples:
    python3 do_pypi_build.py python3.14
    python3 do_pypi_build.py python3.14 twine
"""

# Copyright (c) 2024 - 2026 Tom Björkholm
# MIT License

import sys
from pathlib import Path

from build_helpers.build_utils import (
    extract_python_name, run_command, venv_script)
from clean_build import clean_build


def _run_clean_build_or_fail(
    python_name: str | None, run_name: str,
) -> int:
    """Run clean_build once and print an error on failure.

    Args:
        python_name: Target Python name or None for auto-detect.
        run_name: Human-readable run label for error messages.
    Returns:
        Exit code from clean_build.
    """
    result = clean_build(python_name)
    if result != 0:
        print(f'{run_name} failed with exit code {result}.',
              file=sys.stderr)
    return result


def do_pypi_build(python_name: str | None = None,
                  twine_upload: bool = False) -> int:
    """Build for PyPI and optionally upload.

    Runs clean_build twice. The first build tests and
    generates test summary information. The second build
    packs that updated information into the wheel's README.

    Args:
        python_name: Target Python name (e.g. 'python3.14').
            If None, auto-detects.
        twine_upload: If True, upload to PyPI after build.
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    first_result = _run_clean_build_or_fail(python_name, 'First clean build')
    if first_result != 0:
        return first_result
    second_result = _run_clean_build_or_fail(python_name,
                                             'Second clean build')
    if second_result != 0:
        return second_result
    if twine_upload:
        dist_files = sorted(str(f) for f in Path('dist').iterdir())
        run_command([venv_script('twine'), 'upload'] + dist_files)
        return 0
    print('Twine upload not done as it was not requested.')
    print('To upload to PyPI, run: python3 do_pypi_build.py twine')
    return 0


if __name__ == '__main__':
    _python = extract_python_name(sys.argv[1:])
    _twine = 'twine' in sys.argv[1:]
    sys.exit(do_pypi_build(_python, _twine))
