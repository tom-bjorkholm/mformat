#!/usr/bin/env python3
"""Set up the build environment for the mformat project.

Creates a virtual environment and installs all required
packages for building and testing.

Usage:
    python3 setup_build_environment.py [python_version]

Example:
    python3 setup_build_environment.py python3.14
"""

# Copyright (c) 2024 - 2026 Tom Björkholm
# MIT License

import shutil
import sys
from pathlib import Path

from build_helpers.best_installed_python import resolve_target_python
from build_helpers.build_utils import (
    exit_if_in_virtualenv, extract_python_name, run_command, venv_python)

GLOBAL_PACKAGES = [
    'pip', 'setuptools', 'build', 'pylint',
    'mypy', 'coverage', 'pytest',
]

GLOBAL_PINNED_PACKAGES = [
    'twine==6.0.1',
]

VENV_PACKAGES = [
    'pip', 'pytest', 'pytest-html',
    'flake8', 'flake8-html', 'pytest-flake8',
    'pytest-skip-slow', 'flake8-docstrings',
    'pytest-pylint', 'pytest-cov',
    'wheel', 'pypi-simple', 'requests',
    'types-requests', 'argcomplete',
    'pylint', 'mypy', 'coverage',
    'build', 'setuptools', 'wheel',
    'lxml', 'python-docx', 'odfdo',
    'mammoth', 'odfpy', 'pydoc-markdown',
    'pymarkdownlnt', 'restructuredtext-lint',
    'html5lib', 'htmlcompare',
]

VENV_PINNED_PACKAGES = [
    'twine==6.0.1',
]


def _check_not_in_virtualenv() -> None:
    """Exit if already inside a virtual environment."""
    exit_if_in_virtualenv('set up build environment')


def _handle_existing_venv() -> None:
    """Prompt user and remove venv if it already exists."""
    venv_path = Path('venv')
    if not venv_path.is_dir():
        return
    print('Virtual environment already present. ')
    print('To delete virtual environment and reinitialize type any character '
          'and press <enter>')
    print('To abort press ctrl-C')
    input()
    shutil.rmtree(venv_path)


def _install_global_packages(
    python_cmd: list[str],
) -> None:
    """Install required packages into the system Python.

    Args:
        python_cmd: Command to invoke the target Python.
    """
    for pkg in GLOBAL_PACKAGES + GLOBAL_PINNED_PACKAGES:
        run_command([*python_cmd, '-m', 'pip', 'install', '--upgrade', pkg])


def _create_venv(python_cmd: list[str]) -> None:
    """Create a new virtual environment.

    Args:
        python_cmd: Command to invoke the target Python.
    """
    run_command([*python_cmd, '-m', 'venv', 'venv'])


def _install_venv_packages() -> None:
    """Install required packages inside the venv."""
    vcmd = venv_python()
    for pkg in VENV_PACKAGES + VENV_PINNED_PACKAGES:
        run_command([*vcmd, '-m', 'pip', 'install', '--upgrade', pkg])


def setup_build_environment(python_name: str | None = None) -> None:
    """Set up the build environment.

    Creates a virtual environment and installs all packages
    needed for building and testing.

    Args:
        python_name: Target Python name (e.g. 'python3.14').
            If None, auto-detects the best installed Python.
    """
    _name, python_cmd = resolve_target_python(python_name)
    _check_not_in_virtualenv()
    _handle_existing_venv()
    _install_global_packages(python_cmd)
    _create_venv(python_cmd)
    _install_venv_packages()


if __name__ == '__main__':
    setup_build_environment(extract_python_name(sys.argv[1:]))
