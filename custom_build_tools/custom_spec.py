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
CUSTOM_BUILD_TOOLS_SRC = Path(__file__).resolve().parent / 'src'
sys.path.insert(0, str(COMMON_BUILD_TOOLS_SRC))
sys.path.insert(0, str(CUSTOM_BUILD_TOOLS_SRC))
# pylint: disable=wrong-import-position,import-error
from build_spec import (  # noqa: E402
    BuildSpec,
)
from hooks import (  # noqa: E402
    create_example_readme_hook,
    create_pypi_readme_hook,
    restore_equiv_docx_odt_hook,
    restore_equiv_pdf_hook,
    run_examples_hook,
)


def custom_spec() -> Optional[BuildSpec]:
    """Return custom build spec for this repository."""
    return BuildSpec(
        package_folders=None,
        identical_versions=True,
        mypy_on_test=True,
        mypy_paths=[Path('base/test'), Path('custom_build_tools/test')],
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
            'types-html5lib',
            'PyMuPDF'
        ],
        custom_after_test=[
            run_examples_hook,
            create_example_readme_hook,
            create_pypi_readme_hook
        ],
        custom_final=[restore_equiv_docx_odt_hook, restore_equiv_pdf_hook],
    )
