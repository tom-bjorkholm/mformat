#! /usr/bin/env python3
"""Run all example programs and generate files in example/result."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import shutil
import subprocess
import sys


def _project_root() -> Path:
    """Return project root path from custom_build_tools folder."""
    return Path(__file__).resolve().parents[1]


def run_examples() -> None:
    """Run every python example script with all supported output formats."""
    project_root = _project_root()
    source_dir = project_root / 'example' / 'src'
    result_dir = project_root / 'example' / 'result'
    shutil.rmtree(result_dir, ignore_errors=True)
    result_dir.mkdir(parents=True, exist_ok=True)
    for source_file in sorted(source_dir.glob('*.py')):
        output_base = result_dir / source_file.stem
        command = [
            sys.executable,
            str(source_file),
            '-f',
            'all',
            '-o',
            str(output_base),
        ]
        process = subprocess.run(command, check=False, cwd=project_root)
        if process.returncode == 0:
            continue
        raise RuntimeError(
            f'Example failed: {source_file} exit code {process.returncode}'
        )


if __name__ == '__main__':
    run_examples()
