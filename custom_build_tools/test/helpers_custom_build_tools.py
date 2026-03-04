#! /usr/local/bin/python3
"""Shared helpers for custom build tool tests."""

import subprocess
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

_SRC_DIR = Path(__file__).resolve().parents[1] / 'src'


def load_source_module(module_name: str, file_name: str) -> ModuleType:
    """Load one module from custom_build_tools/src by file name."""
    file_path = _SRC_DIR / file_name
    spec = spec_from_file_location(module_name, file_path)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_text(path: Path, text: str) -> None:
    """Write UTF-8 text to a file and ensure parent directories exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def write_bytes(path: Path, content: bytes) -> None:
    """Write bytes to a file and ensure parent directories exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def run_git(repo_dir: Path, args: list[str]) -> None:
    """Run one git command in the provided repository directory."""
    _ = subprocess.run(['git'] + args, cwd=repo_dir, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def init_git_repo(repo_dir: Path) -> None:
    """Create and configure a local git repository for one test."""
    repo_dir.mkdir(parents=True, exist_ok=True)
    run_git(repo_dir, ['init'])
    run_git(repo_dir, ['config', 'user.name', 'Test User'])
    run_git(repo_dir, ['config', 'user.email', 'test@example.com'])
