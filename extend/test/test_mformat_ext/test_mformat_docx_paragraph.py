#! /usr/local/bin/python3
"""Test the mformat_docx module paragraph functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

# import sys
# from pathlib import Path
from test_mformat_docx_core import silent_docx_create
from mformat_ext.mformat_docx import MultiFormatDocx

# Add base test helpers to path for shared test utilities
# _base_test_path = (
#   Path(__file__).parent.parent.parent.parent /
#    'base' / 'test' / 'test_mformat'
# )
# sys.path.insert(0, str(_base_test_path))
# # pylint: disable=wrong-import-order,wrong-import-position,import-error


def test_add_url(capsys):
    """Test the add_url method creates a docx file."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_paragraph('Check this link:')
        mfd.add_url(url='http://example.com', text='Example')

    silent_docx_create(capsys, func=func)


def test_add_url_as_text(capsys):
    """Test the add_url method with url_as_text=True."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_paragraph('Check this:')
        mfd.add_url(url='http://example.com', text='Here')

    silent_docx_create(capsys, func=func)
