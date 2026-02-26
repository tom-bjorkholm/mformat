#! /usr/local/bin/python3
"""Test the mformat_txt module core functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
from pathlib import Path
import pytest
from check_capsys import check_capsys
from test_helpers import check_run_with_context_manager
from mformat.factory import create_mf
from mformat.mformat import FormatterDescriptor
from mformat.mformat_txt import MultiFormatTxt
from mformat.plain_text_table import TableAlignment


def test_file_name_extension(capsys):
    """Test the file_name_extension method."""
    assert MultiFormatTxt.file_name_extension() == '.txt'
    check_capsys(capsys)


def test_get_arg_desciption(capsys):
    """Test the get_arg_desciption method."""
    assert MultiFormatTxt.get_arg_desciption() == \
        FormatterDescriptor(
            name='txt',
            mandatory_args=[],
            optional_args=['line_length', 'table_max_line_length',
                           'table_alignment']
        )
    check_capsys(capsys)


def test_constructor_defaults(capsys):
    """Test constructor defaults for TXT formatter."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatTxt(file_name=file_name)
        assert mfd.file_name.endswith('.txt')
        assert mfd.line_length == 79
        assert mfd.table_max_line_length == 79
        assert mfd.table_alignment == TableAlignment.CENTER_BUT_DIGITS_RIGHT
    check_capsys(capsys)


def test_constructor_table_max_line_length_none(capsys):
    """Test table_max_line_length None fallback to line_length."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatTxt(file_name=file_name, line_length=42,
                             table_max_line_length=None)
        assert mfd.table_max_line_length == 42
    check_capsys(capsys)


@pytest.mark.parametrize('table_max_line_length', [0, 9, -1])
def test_constructor_table_max_line_length_too_short(
        capsys, table_max_line_length):
    """Test table_max_line_length validation for short values."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.txt')
        with pytest.raises(ValueError) as exc:
            _ = MultiFormatTxt(file_name=file_name, line_length=20,
                               table_max_line_length=table_max_line_length)
        assert exc.value.args[0] == \
            'Table max line length must be at least 10, got ' + \
            str(table_max_line_length)
    check_capsys(capsys)


@pytest.mark.parametrize('table_max_line_length', ['', '10'])
def test_constructor_table_max_line_length_must_be_int(
        capsys, table_max_line_length):
    """Test table_max_line_length assertion for invalid types."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.txt')
        with pytest.raises(AssertionError):
            _ = MultiFormatTxt(file_name=file_name, line_length=20,
                               table_max_line_length=table_max_line_length)
    check_capsys(capsys)


@pytest.mark.parametrize('line_length', [10, -1])
def test_constructor_line_length_too_short(capsys, line_length):
    """Test constructor line length validation for short line lengths."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.txt')
        with pytest.raises(ValueError) as exc:
            _ = MultiFormatTxt(file_name=file_name, line_length=line_length)
        assert exc.value.args[0] == \
            f'Line length must be greater than 10, got {line_length}'
    check_capsys(capsys)


@pytest.mark.parametrize('line_length', [0, None, '79'])
def test_constructor_line_length_must_be_int(capsys, line_length):
    """Test constructor line length assertion for invalid types."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.txt')
        with pytest.raises(AssertionError):
            _ = MultiFormatTxt(file_name=file_name,
                               line_length=line_length)
    check_capsys(capsys)


@pytest.mark.parametrize(
    'level, expected',
    [
        (1, 'Title\n*****\n\n'),
        (2, 'Title\n=====\n\n'),
        (3, 'Title\n-----\n\n'),
        (6, "Title\n'''''\n\n"),
        (7, 'Title\n\n'),
    ]
)
def test_heading_levels(capsys, level, expected):
    """Test heading underline style by heading level."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_heading(level=level, text='Title')

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_add_text_url_and_code(capsys):
    """Test adding text, URL and code in heading state."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_heading(level=2, text='Check')
        mfd.add_text(text=' this')
        mfd.add_url(url='http://example.com')
        mfd.add_code_in_text(text=' now')

    expected = ('Check this http://example.com now\n'
                '=================================\n\n')
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_wraps_using_line_length(capsys):
    """Test heading wrapping uses configured line length."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_heading(level=1, text='a b c d e f g h i')

    expected = ('a b c d e f\n'
                '***********\n'
                '\n'
                'g h i\n'
                '*****\n'
                '\n')
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   args={'line_length': 11},
                                   capsys=capsys)


@pytest.mark.parametrize(
    'programming_language, expected',
    [
        (None,
         '----- Start of code block -----\n'
         'print(1)\n'
         '\n'
         '------ End of code block ------\n'),
        ('python',
         '----- Start of python code block -----\n'
         'print(1)\n'
         '\n'
         '------ End of python code block ------\n'),
    ]
)
def test_write_code_block(capsys, programming_language, expected):
    """Test code block start and end markers."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.write_code_block(text='print(1)\n',
                             programming_language=programming_language)

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_encode_text_no_changes(capsys):
    """Test _encode_text returns plain text unchanged."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.txt')
        with create_mf('txt', file_name) as mfd:
            assert type(mfd).__name__ == 'MultiFormatTxt'
            # pylint: disable=protected-access
            assert mfd._encode_text(
                'a*b [c] {d}') == 'a*b [c] {d}'
    check_capsys(capsys)
