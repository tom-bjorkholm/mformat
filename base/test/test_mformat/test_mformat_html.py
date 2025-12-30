#! /usr/local/bin/python3
"""Test the mformat_html module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

import pytest  # pylint: disable=unused-import # noqa: F401
from check_capsys import check_capsys
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat import FormatterDescriptor


def test_file_name_extension(capsys):
    """Test the file_name_extension method."""
    assert MultiFormatHtml.file_name_extension() == '.html'
    check_capsys(capsys)


def test_get_arg_desciption(capsys):
    """Test the get_arg_desciption method."""
    assert MultiFormatHtml.get_arg_desciption() == \
        FormatterDescriptor(name='html', mandatory_args=[],
                            optional_args=['title', 'css_file'])
    check_capsys(capsys)
