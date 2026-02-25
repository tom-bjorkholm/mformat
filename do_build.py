#!/usr/bin/env python3
"""Build the mformat project and run all tests.

Builds wheel packages, installs them in the virtual
environment, runs all linters and tests, and generates
build reports.

Usage:
    python3 do_build.py [python_version]

Example:
    python3 do_build.py python3.14
"""

# Copyright (c) 2024 - 2026 Tom Björkholm
# MIT License

import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from build_helpers.best_installed_python import resolve_target_python
from build_helpers.build_utils import (
    extract_python_name,
    get_version_from_file,
    run_command_logged,
    venv_python,
    venv_script,
)
from setup_build_environment import setup_build_environment

PKG1 = 'mformat'
PKG2 = 'mformat_ext'

REPORT_DIR = Path('reports')
BUILD_LOG = REPORT_DIR / 'build_log.txt'
PYTEST_LOG = REPORT_DIR / 'pytest_log.txt'
FLAKE_DIR = REPORT_DIR / 'flake_report'
FLAKE_LOG = REPORT_DIR / 'flake8_log.txt'
MYPY_DIR = REPORT_DIR / 'mypy_report'
MYPY_FILE = REPORT_DIR / 'mypy_errors.txt'

_REPORT_LINKS = [
    (
        'pytest_report.html?visible='
        'failed,error,xfailed,xpassed,rerun',
        'pytest report',
    ),
    ('coverage/index.html', 'coverage report'),
    ('flake_report/index.html', 'flake8 report'),
    ('mypy_report/index.html', 'mypy report'),
    ('mypy_errors.txt', 'mypy errors'),
    ('build_log.txt', 'build log'),
    ('pytest_log.txt', 'pytest log'),
]


# ---------------------------------------------------
# Phase 1: Setup
# ---------------------------------------------------

def _ensure_venv(python_name: str | None) -> None:
    """Create the virtual environment if missing."""
    venv_path = Path(venv_python()[0])
    if not venv_path.exists():
        print('No venv found, running setup...')
        setup_build_environment(python_name)


def _prepare_directories() -> None:
    """Clean and create build output directories."""
    for dirname in ['build', 'dist', 'base/build', 'base/dist',
                    'extend/build', 'extend/dist']:
        shutil.rmtree(dirname, ignore_errors=True)
    shutil.rmtree(REPORT_DIR, ignore_errors=True)
    Path('dist').mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)
    MYPY_DIR.mkdir(parents=True, exist_ok=True)
    FLAKE_DIR.mkdir(parents=True, exist_ok=True)
    _clean_pycache()


def _clean_pycache() -> None:
    """Remove __pycache__ from source and test trees."""
    for src_dir in ['base/src', 'base/test', 'extend/src', 'extend/test']:
        base = Path(src_dir)
        if base.is_dir():
            for cache in base.rglob('__pycache__'):
                shutil.rmtree(cache, ignore_errors=True)


# ---------------------------------------------------
# Phase 2: Build and install
# ---------------------------------------------------

def _find_wheel(pkg_name: str) -> str:
    """Find the wheel file for a package in dist/.

    Args:
        pkg_name: Package name, e.g. 'mformat'.

    Returns:
        The wheel filename (without directory prefix).
    """
    wheels = list(Path('dist').glob(f'{pkg_name}-*.whl'))
    if not wheels:
        print(f'Build of wheel for {pkg_name} failed.', file=sys.stderr)
        sys.exit(1)
    return wheels[0].name


def _build_and_install(vcmd: list[str]) -> None:
    """Build both wheel packages and install them."""
    pip1 = PKG1.replace('_', '-')
    pip2 = PKG2.replace('_', '-')
    run_command_logged([*vcmd, '-m', 'build', 'base', '--outdir', 'dist'],
                       log_file=BUILD_LOG)
    whl1 = _find_wheel(PKG1)
    run_command_logged([*vcmd, '-m', 'pip', 'uninstall', '-y', pip1, pip2],
                       log_file=BUILD_LOG)
    run_command_logged([*vcmd, '-m', 'pip', 'install', f'dist/{whl1}'],
                       log_file=BUILD_LOG)
    run_command_logged([*vcmd, '-m', 'build', 'extend', '--outdir', 'dist'],
                       log_file=BUILD_LOG)
    whl2 = _find_wheel(PKG2)
    run_command_logged([*vcmd, '-m', 'pip', 'uninstall', '-y', pip2],
                       log_file=BUILD_LOG)
    run_command_logged([*vcmd, '-m', 'pip', 'install', f'dist/{whl2}'],
                       log_file=BUILD_LOG)

# ---------------------------------------------------
# Phase 3: Lint and test
# ---------------------------------------------------


def _collect_py_files(*dirs: str) -> list[str]:
    """Collect all .py file paths from directories."""
    files: list[str] = []
    for directory in dirs:
        dir_path = Path(directory)
        if dir_path.is_dir():
            files.extend(str(f) for f in sorted(dir_path.glob('*.py')))
    return files


def _run_linters(vcmd: list[str]) -> None:
    """Run all linters. Failures are logged, not fatal."""
    shutil.rmtree(FLAKE_DIR, ignore_errors=True)
    FLAKE_DIR.mkdir(parents=True, exist_ok=True)
    pylint_files = _collect_py_files('example/src', 'example/test')
    if pylint_files:
        run_command_logged([*vcmd, '-m', 'pylint'] + pylint_files,
                           log_file=PYTEST_LOG, check=False, append=False)
    run_command_logged([*vcmd, '-m', 'mypy', 'base/src', 'extend/src',
                        'example/src', 'build_helpers', '--strict',
                        '--html-report', str(MYPY_DIR)], log_file=MYPY_FILE,
                       check=False, append=False)
    run_command_logged([*vcmd, '-m', 'flake8',
                        '--format=html', f'--htmldir={FLAKE_DIR}',
                        'base/src', 'base/test', 'extend/src',
                        'extend/test', 'example/src', 'build_helpers'],
                       log_file=FLAKE_LOG, check=False, append=False)


def _run_pytest() -> int:
    """Run pytest with coverage. Returns exit code."""
    pytest_path = venv_script('pytest')
    return run_command_logged([pytest_path, '--pylint', '--pylint-jobs=16',
                               f'--html={REPORT_DIR}/pytest_report.html',
                               f'--cov={PKG1}', f'--cov={PKG2}',
                               f'--cov-report=html:{REPORT_DIR}/coverage'],
                              log_file=PYTEST_LOG, check=False, append=False)


# ---------------------------------------------------
# Phase 4: Examples and report generation
# ---------------------------------------------------

def _run_examples(vcmd: list[str]) -> None:
    """Run all example programs."""
    result_dir = Path('example/result')
    shutil.rmtree(result_dir, ignore_errors=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    for py_file in sorted(
        Path('example/src').glob('*.py')
    ):
        run_command_logged(
            [*vcmd, str(py_file),
             '-f', 'all',
             '-o', str(result_dir / py_file.stem)],
            log_file=BUILD_LOG,
        )


def _run_readme_generators(vcmd: list[str]) -> None:
    """Run scripts that generate README files."""
    for script in [
        'build_helpers/create_example_readme.py',
        'build_helpers/create_pypi_readme.py',
    ]:
        run_command_logged(
            [*vcmd, script],
            log_file=BUILD_LOG,
        )


def _parse_pytest_summary() -> tuple[str, bool, bool]:
    """Parse the pytest log for the result summary.

    Returns:
        (summary_text, has_skipped, has_failed).
    """
    if not PYTEST_LOG.exists():
        return '', False, False
    last_passed_line = ''
    with open(PYTEST_LOG, encoding='utf-8') as fobj:
        for line in fobj:
            if 'passed' in line:
                last_passed_line = line
    if not last_passed_line:
        return '', False, False
    result = last_passed_line.replace('=', '').strip()
    result = re.sub(r'\.\d\ds', 's', result)
    has_skipped = 'skipped' in last_passed_line
    has_failed = 'failed' in last_passed_line
    return result, has_skipped, has_failed


def _check_flake8_clean() -> bool:
    """Return True if flake8 found no errors."""
    index = FLAKE_DIR / 'index.html'
    if not index.exists():
        return False
    content = index.read_text(encoding='utf-8')
    return 'No flake8 errors found' in content


def _check_mypy_clean() -> bool:
    """Return True if mypy found no issues."""
    if not MYPY_FILE.exists():
        return False
    content = MYPY_FILE.read_text(encoding='utf-8')
    return 'Success: no issues found' in content


def _get_python_version_str(vcmd: list[str]) -> str:
    """Get the Python version string from the venv."""
    result = subprocess.run(
        [*vcmd, '--version'],
        capture_output=True,
        text=True,
        check=False,
    )
    version_str = result.stdout.strip()
    if version_str:
        return version_str
    return result.stderr.strip()


def _write_html_report(version: str, test_result: str,
                       flake8_clean: bool, mypy_clean: bool,
                       python_version: str) -> None:
    """Write the HTML report index page."""
    pip1 = PKG1.replace('_', '-')
    pip2 = PKG2.replace('_', '-')
    now = datetime.now().astimezone()
    title = now.strftime(
        f'<h1>{pip1} and {pip2} {version} '
        f'test report %Y-%m-%d %H:%M </h1>'
    )
    doc_index = REPORT_DIR / 'index.html'
    with open(doc_index, 'w', encoding='utf-8') as f:
        f.write(
            '<!DOCTYPE html>\n<html>\n<head>\n'
            '  <meta charset="utf-8" />\n'
            f'  <title>{pip1} report</title>\n'
            '</head>\n<body>\n'
        )
        f.write(f'{title}\n')
        f.write(
            f'<h2>Building version {version}</h2>\n'
        )
        f.write(f'{test_result}\n')
        if not flake8_clean:
            f.write('<br>Flake8 errors/warnings<br>\n')
        if mypy_clean:
            f.write('<br>No mypy issues found<br>\n')
        else:
            f.write('<br>mypy errors<br>\n')
        f.write(
            'Build and test using python version: '
            f'{python_version}\n'
        )
        f.write('<ul>\n')
        for href, text in _REPORT_LINKS:
            f.write(
                f'<li><a href="{href}">'
                f'{text}</a></li>\n'
            )
        f.write('</ul>\n</body>\n</html>\n')


def _write_test_summary(version: str, test_result: str, flake8_clean: bool,
                        mypy_clean: bool, python_version: str) -> None:
    """Write the test summary markdown file."""
    tsum = REPORT_DIR / 'test_summary.md'
    with open(tsum, 'w', encoding='utf-8') as f:
        f.write('## Test summary\n\n')
        f.write(f'- Test result: {test_result}\n')
        if flake8_clean:
            f.write('- No Flake8 warnings.\n')
        else:
            f.write('- Flake8 errors/warnings.\n')
        if mypy_clean:
            f.write('- No mypy errors found.\n')
        else:
            f.write('- mypy errors\n')
        f.write(
            f'- {version} built and tested using '
            f'python version: {python_version}\n'
        )


def _replace_test_summary_in_readme(readme_path: Path,
                                    summary_path: Path) -> None:
    """Replace the test summary section in a README."""
    lines = readme_path.read_text(encoding='utf-8').\
        splitlines(keepends=True)
    cutoff = len(lines)
    for i, line in enumerate(lines):
        if line.startswith('## Test summary'):
            cutoff = i
            break
    summary_text = summary_path.read_text(encoding='utf-8')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.writelines(lines[:cutoff])
        f.write(summary_text)


def _update_readmes() -> None:
    """Update README files with the test summary."""
    tsum = REPORT_DIR / 'test_summary.md'
    if not tsum.exists():
        return
    for readme_name in ['README.md', 'base/README_pypi.md',
                        'extend/README_pypi.md']:
        readme = Path(readme_name)
        if readme.exists():
            _replace_test_summary_in_readme(readme, tsum)


def _generate_api_docs() -> None:
    """Generate API documentation with pydoc-markdown."""
    pydoc_md = venv_script('pydoc-markdown')
    for yml in ['build_helpers/pydoc-markdown.yml',
                'build_helpers/pydoc-markdown_protected.yml']:
        run_command_logged([pydoc_md, '--render-toc', yml],
                           log_file=BUILD_LOG)


def _generate_report(version: str, vcmd: list[str]) -> int:
    """Generate reports and return the test status.

    Args:
        version: Package version string.
        vcmd: Command to invoke the venv Python.
    Returns:
        0 for success, 1 for failure.
    """
    test_status = 0
    tres, has_skipped, has_failed = _parse_pytest_summary()
    if has_failed:
        print('Pytest/pylint errors', file=sys.stderr)
        test_status = 1
    flake8_clean = _check_flake8_clean()
    if not flake8_clean:
        print('Flake8 errors/warnings.', file=sys.stderr)
        test_status = 1
    mypy_clean = _check_mypy_clean()
    if mypy_clean:
        print('No mypy errors found.', file=sys.stderr)
    else:
        print('mypy errors', file=sys.stderr)
        test_status = 1
    pyver = _get_python_version_str(vcmd)
    _write_html_report(version, tres, flake8_clean, mypy_clean, pyver)
    _write_test_summary(version, tres, flake8_clean, mypy_clean, pyver)
    print(f'Build and test using python version: {pyver}')
    if not has_skipped:
        _update_readmes()
    return test_status


# ---------------------------------------------------
# Main entry point
# ---------------------------------------------------

def do_build(python_name: str | None = None) -> int:
    """Build the project, run tests, generate reports.

    Builds wheel packages for both mformat and mformat_ext,
    installs them, runs all linters and tests, generates
    API documentation, and creates build reports.

    Args:
        python_name: Target Python name (e.g. 'python3.14').
            If None, auto-detects.
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    _name, _cmd = resolve_target_python(python_name)
    _ensure_venv(python_name)
    vcmd = venv_python()
    _prepare_directories()
    version = get_version_from_file(Path('base/setup.py'))
    now = datetime.now().astimezone()
    BUILD_LOG.write_text(
        now.strftime('Build started %Y-%m-%d %H:%M:%S %Z\n'),
        encoding='utf-8',
    )
    _build_and_install(vcmd)
    now = datetime.now().astimezone()
    with open(BUILD_LOG, 'a', encoding='utf-8') as f:
        f.write(now.strftime('Build ready %Y-%m-%d %H:%M:%S %Z\n'))
    for _ in range(5):
        print()
    _run_linters(vcmd)
    _run_pytest()
    _run_examples(vcmd)
    _run_readme_generators(vcmd)
    _generate_api_docs()
    return _generate_report(version, vcmd)


if __name__ == '__main__':
    _python = extract_python_name(sys.argv[1:])
    sys.exit(do_build(_python))
