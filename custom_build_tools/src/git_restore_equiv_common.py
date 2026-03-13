#! /usr/bin/env python3
"""Shared helpers for restoring equivalent generated files."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from collections.abc import Callable
import subprocess
from pathlib import Path
import sys
from tempfile import TemporaryDirectory


def get_committed_file(file: Path, temp_dir: Path) -> Path:
    """Get the latest committed version of one file into temp_dir."""
    temp_dir.mkdir(parents=True, exist_ok=True)
    committed_file = temp_dir / file.name
    git_str = f'cd {file.parent} >/dev/null 2>/dev/null; '
    git_str += f'git show HEAD:./{file.name}'
    with open(committed_file, 'wb') as file_obj:
        cpi = subprocess.run(
            git_str,
            shell=True,
            stdout=file_obj,
            check=True
        )
        cpi.check_returncode()
    return committed_file


def is_git_status_modified(file: Path) -> bool:
    """Check if one file is modified in git status."""
    git_str = f'git status --short {file}'
    cpi = subprocess.run(
        git_str,
        shell=True,
        stdout=subprocess.PIPE,
        check=True
    )
    if cpi.returncode != 0:
        raise RuntimeError(
            f'Failed to check if {file} is modified in the git status'
        )
    return cpi.stdout.decode('utf-8').strip() != ''


def restore_sorted_files(unchanged_files: list[str]) -> None:
    """Restore unchanged files in sorted order."""
    for file in sorted(unchanged_files):
        git_str = f'git restore {file}'
        subprocess.run(git_str, shell=True, check=True)
        print(f'git restored {file}')
    print(f'Restored {len(unchanged_files)} unchanged files.')


def exit_for_missing_venv_dependency(exc: ImportError) -> None:
    """Print a consistent message and exit on missing venv dependencies."""
    print('You need to run this with venv activated.')
    print(f'str(exc): {str(exc)}')
    sys.exit(1)


def list_equivalent_files(
        module_file: str,
        pattern_dispatch: dict[str, Callable[[Path, Path], bool]],
        status_func: Callable[[Path], bool],
        committed_file_func: Callable[[Path, Path], Path]) -> list[str]:
    """List modified generated files equivalent to their HEAD version."""
    with TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        unchanged_files: list[str] = []
        result_dir = (
            Path(module_file).resolve().parents[2] / 'example' / 'result'
        )
        for pattern, compare_files in pattern_dispatch.items():
            for file in result_dir.glob(pattern):
                if not status_func(file):
                    continue
                committed_file = committed_file_func(file, temp_dir)
                if compare_files(file, committed_file):
                    unchanged_files.append(str(file))
        return unchanged_files
