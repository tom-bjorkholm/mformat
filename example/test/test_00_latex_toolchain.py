#! /usr/local/bin/python3
"""Test availability of the local LaTeX toolchain for example tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import pytest
from .example_checkers import check_capsys_silent, check_latex_toolchain


def test_latex_toolchain(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that pdflatex is available and can compile a smoke test."""
    check_latex_toolchain()
    check_capsys_silent(capsys)
