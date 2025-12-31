#! /usr/local/bin/python3
"""Test the reg_pkg_formats module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import builtins
import sys
import pytest  # pylint: disable=unused-import # noqa: F401
from check_capsys import check_capsys
from mformat.reg_pkg_formats import register_formats_in_pkg
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat_md import MultiFormatMd


def test_register_pkg_formats1(capsys, monkeypatch):
    """Test the register_formats_in_pkg function."""
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        # Fail only for the specific module (or package)
        if name.startswith('mformat_ext'):
            raise ImportError('mformat_ext is not installed')
        return real_import(name, *args, **kwargs)

    # Ensure it's not already loaded
    monkeypatch.delitem(sys.modules,
                        'mformat_ext.reg_extpkg_formats.' +
                        'register_formats_in_ext_pkg',
                        raising=False)
    monkeypatch.delitem(sys.modules, "mformat_ext.reg_extpkg_formats",
                        raising=False)
    monkeypatch.delitem(sys.modules, "mformat_ext", raising=False)
    # Intercept imports
    monkeypatch.setattr(builtins, "__import__", fake_import)
    assert register_formats_in_pkg() == [MultiFormatHtml, MultiFormatMd]
    check_capsys(capsys)


def test_register_pkg_formats2(capsys):
    """Test the register_formats_in_pkg function."""
    # pylint: disable=import-outside-toplevel,wrong-import-order
    from mformat_ext.mformat_docx import MultiFormatDocx
    assert register_formats_in_pkg() == \
        [MultiFormatHtml, MultiFormatMd, MultiFormatDocx]
    check_capsys(capsys)
