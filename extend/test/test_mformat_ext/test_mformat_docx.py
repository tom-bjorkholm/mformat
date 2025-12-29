#! /usr/local/bin/python3
"""Test the mformat_docx module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

import pytest
from mformat_ext.mformat_docx import MultiFormatDocx
from mformat.mformat import FormatterDescriptor


def test_file_name_extension(capsys):
    """Test the file_name_extension method."""
    assert MultiFormatDocx.file_name_extension() == '.docx'
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_get_arg_desciption(capsys):
    """Test the get_arg_desciption method."""
    assert MultiFormatDocx.get_arg_desciption() == \
        FormatterDescriptor(name='docx', mandatory_args=[],
                            optional_args=[])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
