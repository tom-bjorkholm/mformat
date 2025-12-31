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
                          ('_write_text',
                           ('test', MultiFormatState.PARAGRAPH,
                            False, False), 'test'),
                          ('_write_text',
                           ('test\ntest', MultiFormatState.PARAGRAPH,
                            False, False), 'test\ntest'),
                          ('_write_text',
                           ('bold', MultiFormatState.PARAGRAPH,
                            True, False), '**bold**'),
                          ('_write_text',
                           ('italic', MultiFormatState.PARAGRAPH,
                            False, True), '*italic*'),
                          ('_write_text',
                           ('both', MultiFormatState.PARAGRAPH,
                            True, True), '***both***')])
def test_methods(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                 method, arg, expected):
    """Test the trivial methods of the MultiFormatMd class."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.md'
        with MultiFormatMd(file_name=fname) as mfd:
            assert type(mfd).__name__ == 'MultiFormatMd'
            assert mfd.state == MultiFormatState.EMPTY
            if arg is not None:
                if isinstance(arg, tuple):
                    getattr(mfd, method)(*arg)
                else:
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
def test_start_paragraph(capsys, text, expected):
    """Test the start_paragraph method."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.md'
        with create_mf('md', file_name=fname) as mfd:
            assert type(mfd).__name__ == 'MultiFormatMd'
            assert mfd.state == MultiFormatState.EMPTY
            mfd.start_paragraph(text=text)
            assert mfd.state == MultiFormatState.PARAGRAPH
        with open(fname, 'rt', encoding='utf-8') as file:
            assert file.read() == expected
        check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('bold text', True, False, '\n**bold text**\n'),
                          ('italic text', False, True, '\n*italic text*\n'),
                          ('both', True, True, '\n***both***\n')])
def test_start_paragraph_formatting(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                                    text, bold, italic, expected):
    """Test the start_paragraph method with bold and italic."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.md'
        with create_mf('md', file_name=fname) as mfd:
            assert type(mfd).__name__ == 'MultiFormatMd'
            assert mfd.state == MultiFormatState.EMPTY
            mfd.start_paragraph(text=text, bold=bold, italic=italic)
            assert mfd.state == MultiFormatState.PARAGRAPH
        with open(fname, 'rt', encoding='utf-8') as file:
            assert file.read() == expected
        check_capsys(capsys)
