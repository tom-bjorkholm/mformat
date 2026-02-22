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
    extract_python_name,run_command, venv_script)
from clean_build import clean_build


def do_pypi_build(python_name: str | None = None,
                  twine_upload: bool = False) -> None:
    """Build for PyPI and optionally upload.

    Runs clean_build twice. The first build tests and
    generates test summary information. The second build
    packs that updated information into the wheel's README.

    Args:
        python_name: Target Python name (e.g. 'python3.14').
            If None, auto-detects.
        twine_upload: If True, upload to PyPI after build.
    """
    clean_build(python_name)
    clean_build(python_name)
    if twine_upload:
        dist_files = sorted(str(f) for f in Path('dist').iterdir())
        run_command([venv_script('twine'), 'upload'] + dist_files)
    else:
        print('Twine upload not done as it was not requested.')
        print('To upload to PyPI, run: python3 do_pypi_build.py twine')


if __name__ == '__main__':
    _python = extract_python_name(sys.argv[1:])
    _twine = 'twine' in sys.argv[1:]
    do_pypi_build(_python, _twine)
