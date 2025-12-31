#! /usr/local/bin/python3
"""Test the mformat_md module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
import pytest
from check_capsys import check_capsys
from mformat.mformat_md import MultiFormatMd
from mformat.mformat import FormatterDescriptor, MultiFormatState
from mformat.factory import create_mf


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


@pytest.mark.parametrize('method, arg, expected',
                         [('_write_file_prefix', None, ''),
                          ('_write_file_suffix', None, ''),
                          ('_start_paragraph', None, '\n'),
                          ('_end_paragraph', None, '\n'),
                          ('_write_in_paragraph', 'test', 'test'),
                          ('_write_in_paragraph', 'test\ntest', 'test\ntest')])
def test_methods(capsys, method, arg, expected):
    """Test the trivial methods of the MultiFormatMd class."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.md'
        with MultiFormatMd(file_name=fname) as mfd:
            assert type(mfd).__name__ == 'MultiFormatMd'
            assert mfd.state == MultiFormatState.EMPTY
            if arg is not None:
                getattr(mfd, method)(text=arg)
            else:
                getattr(mfd, method)()
            assert mfd.state == MultiFormatState.EMPTY
        with open(fname, 'rt', encoding='utf-8') as file:
            assert file.read() == expected
        check_capsys(capsys)


@pytest.mark.parametrize('text, expected',
                         [('test', '\ntest\n'),
                          ('test\ntest', '\ntest\ntest\n')])
def test_write_paragraph(capsys, text, expected):
    """Test the write_paragraph method."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.md'
        with create_mf('md', file_name=fname) as mfd:
            assert type(mfd).__name__ == 'MultiFormatMd'
            assert mfd.state == MultiFormatState.EMPTY
            mfd.write_paragraph(text=text)
            assert mfd.state == MultiFormatState.PARAGRAPH
        with open(fname, 'rt', encoding='utf-8') as file:
            assert file.read() == expected
        check_capsys(capsys)
