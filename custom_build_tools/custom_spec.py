#! /usr/bin/env python3
"""Repository-specific build specification for common_build_tools."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from pathlib import Path
import sys

COMMON_BUILD_TOOLS_SRC = (
    Path(__file__).resolve().parents[1] / 'common_build_tools' / 'src'
)
sys.path.insert(0, str(COMMON_BUILD_TOOLS_SRC))
# pylint: disable=wrong-import-position
from build_spec import BuildSpec  # noqa: E402
from hooks import generate_readmes_hook, run_examples_hook  # noqa: E402


def custom_spec() -> Optional[BuildSpec]:
    """Return custom build spec for this repository."""
    return BuildSpec(
        package_folders=None,
        identical_versions=True,
        mypy_on_test=True,
        additional_venv_packages=[
            'pypi-simple',
            'requests',
            'types-requests',
            'argcomplete',
            'pymarkdownlnt',
            'restructuredtext-lint',
            'html5lib',
            'mammoth',
            'odfpy',
            'htmlcompare',
        ],
        custom_after_test=[run_examples_hook, generate_readmes_hook],
    )
