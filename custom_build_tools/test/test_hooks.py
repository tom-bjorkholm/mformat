#! /usr/local/bin/python3
"""Tests for custom_build_tools/src/hooks.py."""

import subprocess
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Callable
import pytest
_TEST_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_TEST_DIR))
# pylint: disable=wrong-import-position,wrong-import-order
from helpers_custom_build_tools import (  # noqa: E402
    load_source_module
)
# pylint: enable=wrong-import-position,wrong-import-order

hooks = load_source_module('hooks', 'hooks.py')


@pytest.mark.parametrize(
    'os_name, expected_tail',
    [('posix', Path('venv/bin/python')),
     ('nt', Path('venv/Scripts/python.exe'))]
)
def test_venv_python_path_for_platform(monkeypatch: pytest.MonkeyPatch,
                                       os_name: str,
                                       expected_tail: Path) -> None:
    """Test selection of venv Python path for posix and Windows."""
    venv_python: Callable[[Path], Path] = getattr(hooks, '_venv_python')
    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        monkeypatch.setattr(hooks.os, 'name', os_name)
        path = venv_python(project_root)
    assert path == project_root / expected_tail


def test_run_script_with_venv_runs_subprocess(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test _run_script_with_venv calls subprocess with expected arguments."""
    run_script: Callable[[Path, Path], None] = getattr(
        hooks, '_run_script_with_venv'
    )
    calls: list[tuple[list[str], Path]] = []

    def fake_run(command: list[str], check: bool,
                 cwd: Path) -> subprocess.CompletedProcess[str]:
        """Record command and report success."""
        assert check is False
        calls.append((command, cwd))
        return subprocess.CompletedProcess(command, 0)

    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        script_file = project_root / 'custom_build_tools' / 'src' / 'script.py'
        script_file.parent.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(hooks.subprocess, 'run', fake_run)
        monkeypatch.setattr(hooks, '_venv_python',
                            lambda _: project_root / 'venv' / 'bin' / 'python')
        run_script(script_file, project_root)
    assert calls == [([
        str(project_root / 'venv' / 'bin' / 'python'),
        str(script_file)
    ], project_root)]


def test_run_script_with_venv_raises_on_failure(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test _run_script_with_venv raises RuntimeError on failure."""
    run_script: Callable[[Path, Path], None] = getattr(
        hooks, '_run_script_with_venv'
    )

    def fake_run(command: list[str], check: bool,
                 cwd: Path) -> subprocess.CompletedProcess[str]:
        """Return failing completed process."""
        _ = command
        _ = check
        _ = cwd
        return subprocess.CompletedProcess(command, 7)

    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        script_file = project_root / 'custom_build_tools' / 'src' / 'script.py'
        script_file.parent.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(hooks.subprocess, 'run', fake_run)
        monkeypatch.setattr(hooks, '_venv_python',
                            lambda _: project_root / 'venv' / 'bin' / 'python')
        with pytest.raises(RuntimeError) as exc:
            run_script(script_file, project_root)
    assert 'Custom hook script failed:' in str(exc.value)
    assert '(exit code 7).' in str(exc.value)


def test_run_examples_hook_calls_expected_script(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test run_examples_hook resolves path and calls script runner once."""
    calls: list[tuple[Path, Path]] = []

    def fake_run_script(script_file: Path, project_root: Path) -> None:
        """Record one call."""
        calls.append((script_file, project_root))

    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        info = {'project_root': str(project_root)}
        monkeypatch.setattr(hooks, '_run_script_with_venv', fake_run_script)
        hooks.run_examples_hook(object(), info)
    assert calls == [(
        project_root / 'custom_build_tools' / 'src' / 'run_examples.py',
        project_root
    )]


def test_generate_readmes_hook_calls_both_scripts(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test generate_readmes_hook runs both README generation scripts."""
    calls: list[tuple[Path, Path]] = []

    def fake_run_script(script_file: Path, project_root: Path) -> None:
        """Record one call."""
        calls.append((script_file, project_root))

    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        info = {'project_root': str(project_root)}
        monkeypatch.setattr(hooks, '_run_script_with_venv', fake_run_script)
        hooks.generate_readmes_hook(object(), info)
    assert calls == [
        (
            project_root / 'custom_build_tools' / 'src' /
            'create_example_readme.py',
            project_root
        ),
        (
            project_root / 'custom_build_tools' / 'src' /
            'create_pypi_readme.py',
            project_root
        )
    ]


def test_restore_equiv_docx_odt_hook_calls_expected_script(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test restore_equiv_docx_odt_hook calls the expected script path."""
    calls: list[tuple[Path, Path]] = []

    def fake_run_script(script_file: Path, project_root: Path) -> None:
        """Record one call."""
        calls.append((script_file, project_root))

    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        info = {'project_root': str(project_root)}
        monkeypatch.setattr(hooks, '_run_script_with_venv', fake_run_script)
        hooks.restore_equiv_docx_odt_hook(
            object(),
            info
        )
    assert calls == [(
        project_root / 'custom_build_tools' / 'src' /
        'git_restore_equiv_docx_odt.py',
        project_root
    )]
