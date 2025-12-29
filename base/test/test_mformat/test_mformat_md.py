#! /usr/local/bin/python3
"""Test the mformat_md module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from mformat.mformat_md import MultiFormatMd
from mformat.mformat import FormatterDescriptor


def test_file_name_extension(capsys):
    """Test the file_name_extension method."""
    assert MultiFormatMd.file_name_extension() == '.md'
    check_capsys(capsys)


def test_get_arg_desciption(capsys):
    """Test the get_arg_desciption method."""
    assert MultiFormatMd.get_arg_desciption() == \
        FormatterDescriptor(name='md', mandatory_args=[],
                            optional_args=[])
    check_capsys(capsys)
