#!/usr/bin/env python3
"""Clean, set up environment, and build with full testing.

Performs a clean build by removing all artifacts, creating
a fresh virtual environment, and running the full build
and test suite.

Usage:
    python3 clean_build.py [python_version]

Example:
    python3 clean_build.py python3.14
"""

# Copyright (c) 2024 - 2026 Tom Björkholm
# MIT License

import sys

from build_helpers.best_installed_python import (
    resolve_target_python,
)
from build_helpers.build_utils import (
    exit_if_in_virtualenv,
    extract_python_name,
)
from clean import clean
from do_build import do_build
from setup_build_environment import (
    setup_build_environment,
)


def clean_build(
    python_name: str | None = None,
) -> int:
    """Perform a clean build with full testing.

    Cleans all artifacts, creates a fresh virtual
    environment, and runs the full build and test suite.

    Args:
        python_name: Target Python name (e.g. 'python3.14').
            If None, auto-detects the best installed Python.

    Returns:
        Exit code from the build (0 = success).
    """
    exit_if_in_virtualenv('delete virtual environment')

    name, _cmd = resolve_target_python(python_name)

    clean()
    setup_build_environment(name)
    return do_build(name)


if __name__ == '__main__':
    _python = extract_python_name(sys.argv[1:])
    sys.exit(clean_build(_python))
