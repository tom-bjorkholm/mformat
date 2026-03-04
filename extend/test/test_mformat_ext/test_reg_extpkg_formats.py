#! /usr/local/bin/python3
"""Test the register_formats_in_ext_pkg module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest  # pylint: disable=unused-import # noqa: F401
from mformat_ext.reg_extpkg_formats import register_formats_in_ext_pkg
from mformat_ext.mformat_docx import MultiFormatDocx
from mformat_ext.mformat_odt import MultiFormatOdt


def test_reg_formats_in_ext_pkg(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the register_formats_in_ext_pkg function."""
    assert register_formats_in_ext_pkg() == [MultiFormatDocx, MultiFormatOdt]
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
