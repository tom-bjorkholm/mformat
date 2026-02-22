#!/usr/bin/env python3
"""Find the best (highest version) installed Python 3.x.

Can be run as a standalone script or imported as a module.
When run as a script, prints the Python name (e.g.
'python3.14') to stdout.
"""

# Copyright (c) 2024 - 2026 Tom Björkholm
# MIT License

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from build_helpers.build_utils import (
        is_windows, resolve_python_command, validate_python_name)
except ImportError:
    from build_utils import (  # type: ignore
        is_windows, resolve_python_command, validate_python_name)


def _find_via_py_launcher() -> list[tuple[int, int]]:
    """Discover Python 3.x versions via the Windows py launcher.

    Returns:
        List of (major, minor) tuples found.
    """
    if not shutil.which('py'):
        return []
    results: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    try:
        proc = subprocess.run(['py', '--list'], capture_output=True,
                              text=True, timeout=10, check=False)
        if proc.returncode != 0:
            return results
        for line in proc.stdout.splitlines():
            match = re.search(r'-(\d+)\.(\d+)', line)
            if not match:
                continue
            major = int(match.group(1))
            minor = int(match.group(2))
            version = (major, minor)
            if major == 3 and version not in seen:
                seen.add(version)
                results.append(version)
    except subprocess.TimeoutExpired:
        pass
    return results


def _is_executable_file(path: Path) -> bool:
    """Check whether a path points to an executable file."""
    if not path.is_file():
        return False
    if is_windows():
        return True
    return os.access(path, os.X_OK)


def _find_via_path_scan() -> list[tuple[int, int]]:
    """Discover Python 3.x versions by scanning PATH.

    Returns:
        List of (major, minor) tuples found.
    """
    results: list[tuple[int, int]] = []
    seen: set[int] = set()
    suffix = r'\.exe' if is_windows() else ''
    pattern = re.compile(r'^python3\.(\d+)' + suffix + r'$')
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    for dir_str in path_dirs:
        dir_path = Path(dir_str)
        if not dir_path.is_dir():
            continue
        try:
            _scan_directory(dir_path, pattern, seen, results)
        except (PermissionError, OSError):
            continue
    return results


def _scan_directory(dir_path: Path, pattern: re.Pattern[str], seen: set[int],
                    results: list[tuple[int, int]]) -> None:
    """Scan a single directory for python3.X executables."""
    for entry in dir_path.iterdir():
        match = pattern.match(entry.name)
        if not match:
            continue
        if not _is_executable_file(entry):
            continue
        minor = int(match.group(1))
        if minor not in seen:
            seen.add(minor)
            results.append((3, minor))


def find_best_python_name() -> str:
    """Find the name of the highest-versioned Python 3.x.

    On Windows, tries the py launcher first, then falls
    back to scanning PATH directories. On other platforms,
    scans PATH only.

    Returns:
        A name like 'python3.14'.
    """
    candidates: list[tuple[int, int]] = []
    if is_windows():
        candidates = _find_via_py_launcher()
    if not candidates:
        candidates = _find_via_path_scan()
    if not candidates:
        print('Error: No Python 3.x installation found.', file=sys.stderr)
        sys.exit(1)
    candidates.sort()
    major, minor = candidates[-1]
    return f'python{major}.{minor}'


def resolve_target_python(python_name: str | None = None) -> tuple[str,
                                                                   list[str]]:
    """Determine which Python to use for the build.

    If a Python name is provided, validates and uses it.
    Otherwise, auto-detects the best installed Python.

    Args:
        python_name: e.g. 'python3.14', or None for
            auto-detection.

    Returns:
        A (python_name, command_list) tuple.
    """
    if python_name:
        validate_python_name(python_name)
        name = python_name
    else:
        name = find_best_python_name()
    cmd = resolve_python_command(name)
    if not cmd:
        print(f'Cannot find executable for {name}')
        sys.exit(1)
    print(f'Using PYTHON {name}')
    return name, cmd


if __name__ == '__main__':
    print(find_best_python_name())
