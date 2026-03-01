#! /usr/bin/env python3
"""Custom build hook functions for this repository."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
from pathlib import Path
import subprocess
import sys

COMMON_BUILD_TOOLS_SRC = (
    Path(__file__).resolve().parents[1] / 'common_build_tools' / 'src'
)
sys.path.insert(0, str(COMMON_BUILD_TOOLS_SRC))
# pylint: disable=wrong-import-position
from build_spec import BuildInformation, BuildSpec  # noqa: E402


def _venv_python(project_root: Path) -> Path:
    """Return venv Python path for current platform."""
    if os.name == 'nt':
        return project_root / 'venv' / 'Scripts' / 'python.exe'
    return project_root / 'venv' / 'bin' / 'python'


def _run_script_with_venv(script_file: Path, project_root: Path) -> None:
    """Run one script file with venv Python and fail on non-zero exit."""
    command = [str(_venv_python(project_root)), str(script_file)]
    process = subprocess.run(command, check=False, cwd=project_root)
    if process.returncode == 0:
        return
    raise RuntimeError(
        f'Custom hook script failed: {script_file} '
        f'(exit code {process.returncode}).'
    )


def run_examples_hook(build_spec: BuildSpec,
                      build_information: BuildInformation) -> None:
    """Run all example programs."""
    _ = build_spec
    project_root = Path(build_information['project_root'])
    _run_script_with_venv(project_root / 'custom_build_tools' /
                          'run_examples.py', project_root)


def generate_readmes_hook(build_spec: BuildSpec,
                          build_information: BuildInformation) -> None:
    """Generate project-specific README files from custom scripts."""
    _ = build_spec
    project_root = Path(build_information['project_root'])
    custom_folder = project_root / 'custom_build_tools'
    _run_script_with_venv(custom_folder / 'create_example_readme.py',
                          project_root)
    _run_script_with_venv(custom_folder / 'create_pypi_readme.py',
                          project_root)


def restore_equiv_docx_odt_hook(build_spec: BuildSpec,
                                build_information: BuildInformation) -> None:
    """Restore unchanged docx/odt files that git reports as modified."""
    _ = build_spec
    project_root = Path(build_information['project_root'])
    custom_folder = project_root / 'custom_build_tools'
    _run_script_with_venv(
        custom_folder / 'git_restore_equiv_docx_odt.py',
        project_root
    )
