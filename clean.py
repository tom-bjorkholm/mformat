#!/usr/bin/env python3
"""Clean all build artifacts and caches.

Removes virtual environment, build outputs, test caches,
and other generated files.

Usage:
    python3 clean.py
"""

# Copyright (c) 2024 - 2026 Tom Björkholm
# MIT License

import shutil
from pathlib import Path

from build_helpers.build_utils import exit_if_in_virtualenv

DIRS_TO_REMOVE = [
    'build', 'dist', 'reports', 'venv',
    '.pytest_cache', '.mypy_cache',
]

PATTERNS_TO_REMOVE = [
    '__pycache__',
    '*~',
    '*.egg-info',
    '*.pyc',
    '.coverage',
    '.tox',
    'nosetests.xml',
]


def _remove_matching(pattern: str) -> None:
    """Remove all files and dirs matching pattern."""
    for item in list(Path('.').rglob(pattern)):
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        elif item.exists():
            item.unlink(missing_ok=True)


def clean() -> None:
    """Remove all build artifacts and caches."""
    exit_if_in_virtualenv('delete virtual environment')

    for dirname in DIRS_TO_REMOVE:
        shutil.rmtree(dirname, ignore_errors=True)

    for item in list(Path('.').glob('.coverage*')):
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        elif item.exists():
            item.unlink(missing_ok=True)

    for pattern in PATTERNS_TO_REMOVE:
        _remove_matching(pattern)


if __name__ == '__main__':
    clean()
