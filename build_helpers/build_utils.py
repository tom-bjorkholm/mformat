"""Shared utilities for cross-platform Python project builds.

Provides functions for resolving Python commands across
platforms, running subprocess commands with error handling,
and working with virtual environments.
"""

# Copyright (c) 2024 - 2026 Tom Björkholm
# MIT License

import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path


def resolve_python_command(python_name: str) -> list[str]:
    """Resolve a Python name to a subprocess command list.

    Given a name like 'python3.14', returns the command
    needed to invoke that Python version. Uses the absolute
    executable path from PATH when available. On Windows,
    falls back to the py launcher if the name is not directly
    available.

    Args:
        python_name: e.g. 'python3.14'.

    Returns:
        Command list, e.g. ['C:/.../python3.14.exe'] or
        ['py', '-3.14']. Empty list if not found.
    """
    executable_path = shutil.which(python_name)
    if executable_path:
        return [executable_path]
    return _try_py_launcher(python_name)


def _try_py_launcher(python_name: str) -> list[str]:
    """Try to resolve python_name via the Windows py launcher.

    Args:
        python_name: e.g. 'python3.14'.

    Returns:
        Command list via py launcher, or empty list.
    """
    if not is_windows() or not shutil.which('py'):
        return []
    match = re.match(r'python(\d+\.\d+)', python_name)
    if not match:
        return []
    flag = f'-{match.group(1)}'
    try:
        proc = subprocess.run(['py', flag, '--version'], capture_output=True,
                              text=True, timeout=10, check=False)
        if proc.returncode == 0:
            return ['py', flag]
    except subprocess.TimeoutExpired:
        pass
    return []


def venv_python(venv_dir: str = 'venv') -> list[str]:
    """Return the command to invoke the venv's Python.

    Args:
        venv_dir: Virtual environment directory name.

    Returns:
        Command list with the path to the venv Python.
    """
    if is_windows():
        path = Path(venv_dir) / 'Scripts' / 'python.exe'
    else:
        path = Path(venv_dir) / 'bin' / 'python'
    return [str(path)]


def venv_script(name: str, venv_dir: str = 'venv') -> str:
    """Return path to a script installed in the venv.

    Args:
        name: Script name, e.g. 'pytest' or 'twine'.
        venv_dir: Virtual environment directory name.

    Returns:
        Path string to the script executable.
    """
    if is_windows():
        path = Path(venv_dir) / 'Scripts' / f'{name}.exe'
    else:
        path = Path(venv_dir) / 'bin' / name
    return str(path)


def run_command(cmd: list[str], check: bool = True) -> int:
    """Run a command, echoing it and optionally exiting.

    Prints the command before executing. If check is True
    and the command returns a non-zero exit code, prints a
    colored error message to stderr and exits.

    Args:
        cmd: The command and its arguments.
        check: If True, exit on non-zero return code.

    Returns:
        The command's exit code.
    """
    print(f'+ {" ".join(cmd)}')
    result = subprocess.run(cmd, check=False)
    if check and result.returncode != 0:
        _print_error(result.returncode)
        sys.exit(result.returncode)
    return result.returncode


def run_command_logged(cmd: list[str], log_file: Path, check: bool = True,
                       append: bool = True) -> int:
    """Run a command, streaming output to screen and log.

    Combines the behavior of the Unix 'tee' command with
    subprocess execution. Output is displayed in real time
    and simultaneously written to the log file.

    Args:
        cmd: The command and its arguments.
        log_file: Path to the log file.
        check: If True, exit on non-zero return code.
        append: If True, append to log; otherwise overwrite.

    Returns:
        The command's exit code.
    """
    print(f'+ {" ".join(cmd)}')
    mode = 'a' if append else 'w'
    returncode = _tee_to_file(cmd, log_file, mode)
    if check and returncode != 0:
        _print_error(returncode)
        sys.exit(returncode)
    return returncode


def _tee_to_file(
    cmd: list[str], log_file: Path, mode: str,
) -> int:
    """Run a command, writing output to file and stdout."""
    with open(log_file, mode, encoding='utf-8') as log:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True) as proc:
            for line in (proc.stdout or []):
                sys.stdout.write(line)
                sys.stdout.flush()
                log.write(line + '\n')
    return proc.returncode  # set by Popen.__exit__


def _print_error(returncode: int) -> None:
    """Print a colored error message for a failed command."""
    print(f'\033[31mExiting due to error code from command: {returncode}' +
          '\033[0m', file=sys.stderr)


def is_in_virtualenv() -> bool:
    """Check if running inside a virtual environment."""
    return bool(os.environ.get('VIRTUAL_ENV'))


def exit_if_in_virtualenv(action: str) -> None:
    """Exit with an error if inside a virtual environment.

    Args:
        action: What cannot be done, e.g.
            'delete virtual environment'.
    """
    if not is_in_virtualenv():
        return
    print(f'Cannot {action} if already in virtual environment')
    print('First do: deactivate')
    sys.exit(1)


def validate_python_name(name: str) -> None:
    """Validate that a string looks like a Python executable.

    Exits with an error if the name does not contain
    'python'.

    Args:
        name: The name to validate, e.g. 'python3.14'.
    """
    if 'python' not in name:
        print(
            f'{name} does not look like a python version'
        )
        sys.exit(1)


def extract_python_name(
    args: list[str],
) -> str | None:
    """Extract a Python version name from command-line args.

    Looks for an argument containing 'python' that is not
    a .py script path. Returns the first match, or None.

    Args:
        args: Command-line arguments (sys.argv[1:]).

    Returns:
        A name like 'python3.14', or None.
    """
    for arg in args:
        if 'python' in arg and not arg.endswith('.py'):
            return arg
    return None


def get_version_from_file(path: Path) -> str:
    """Extract version string from setup.py or pyproject.toml.

    Looks for a line starting with 'version =' or
    'version=' and returns the version value.

    Args:
        path: Path to the file to read.

    Returns:
        The version string, or empty string if not found.
    """
    with open(path, encoding='utf-8') as fobj:
        for line in fobj:
            stripped = line.strip()
            if stripped.startswith(('version =', 'version=')):
                value = stripped.split('=', 1)[1]
                return value.strip(' \t\n\r"\',')
    return ''


def is_windows() -> bool:
    """Return True if running on Windows."""
    return platform.system() == 'Windows'
