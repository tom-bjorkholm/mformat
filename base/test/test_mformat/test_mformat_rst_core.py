#! /usr/local/bin/python3
"""Test the mformat_rst module core functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
import pytest
from mformat.factory import create_mf
from mformat.mformat import FormatterDescriptor
from mformat.mformat_rst import MultiFormatRst
from mformat.plain_text_table import TableAlignment
from .check_capsys import check_capsys
from .rst_test_helpers import RST_FILE_EXTENSION, check_rst_output
from .test_helpers import (check_character_encoding_bytes,
                           check_formatter_constructor_attributes,
                           check_formatter_constructor_raises,
                           check_invalid_character_encoding_constructor,
                           create_paragraph_file_bytes)


def test_file_name_extension(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file_name_extension method."""
    assert MultiFormatRst.file_name_extension() == '.rst'
    check_capsys(capsys)


def test_get_arg_desciption(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_arg_desciption method."""
    assert MultiFormatRst.get_arg_desciption() == FormatterDescriptor(
        name='reST',
        mandatory_args=[],
        optional_args=['line_length', 'table_max_line_length',
                       'table_alignment', 'character_encoding'])
    check_capsys(capsys)


def test_constructor_defaults(capsys: pytest.CaptureFixture[str]) -> None:
    """Test constructor defaults for reST formatter."""
    check_formatter_constructor_attributes(
        formatter_class=MultiFormatRst,
        file_extension=RST_FILE_EXTENSION,
        constructor_args=None,
        expected_attrs={
            'line_length': 79,
            'table_max_line_length': 79,
            'table_alignment': TableAlignment.LEFT,
        },
        expected_file_extension=RST_FILE_EXTENSION)
    check_capsys(capsys)


def test_constructor_table_max_line_length_none(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test table_max_line_length None fallback to line_length."""
    check_formatter_constructor_attributes(
        formatter_class=MultiFormatRst,
        file_extension=RST_FILE_EXTENSION,
        constructor_args={'line_length': 42, 'table_max_line_length': None},
        expected_attrs={'table_max_line_length': 42})
    check_capsys(capsys)


@pytest.mark.parametrize('table_max_line_length', [0, 9, -1])
def test_constructor_table_max_line_length_too_short(
        capsys: pytest.CaptureFixture[str],
        table_max_line_length: int) -> None:
    """Test table_max_line_length validation for short values."""
    check_formatter_constructor_raises(
        formatter_class=MultiFormatRst,
        file_extension=RST_FILE_EXTENSION,
        constructor_args={
            'line_length': 20,
            'table_max_line_length': table_max_line_length,
        },
        exception_type=ValueError,
        expected_message='Table max line length must be at least 10, got '
        + str(table_max_line_length))
    check_capsys(capsys)


@pytest.mark.parametrize('table_max_line_length', ['', '10'])
def test_constructor_table_max_line_length_must_be_int(
        capsys: pytest.CaptureFixture[str],
        table_max_line_length: str) -> None:
    """Test table_max_line_length assertion for invalid types."""
    check_formatter_constructor_raises(
        formatter_class=MultiFormatRst,
        file_extension=RST_FILE_EXTENSION,
        constructor_args={
            'line_length': 20,
            'table_max_line_length': table_max_line_length,
        },
        exception_type=AssertionError)
    check_capsys(capsys)


@pytest.mark.parametrize('line_length', [10, -1])
def test_constructor_line_length_too_short(
        capsys: pytest.CaptureFixture[str], line_length: int) -> None:
    """Test constructor line length validation for short line lengths."""
    check_formatter_constructor_raises(
        formatter_class=MultiFormatRst,
        file_extension=RST_FILE_EXTENSION,
        constructor_args={'line_length': line_length},
        exception_type=ValueError,
        expected_message=f'Line length must be greater than 10, got '
        f'{line_length}')
    check_capsys(capsys)


@pytest.mark.parametrize('line_length', [0, None, '79'])
def test_constructor_line_length_must_be_int(
        capsys: pytest.CaptureFixture[str],
        line_length: Optional[int]) -> None:
    """Test constructor line length assertion for invalid types."""
    check_formatter_constructor_raises(
        formatter_class=MultiFormatRst,
        file_extension=RST_FILE_EXTENSION,
        constructor_args={'line_length': line_length},
        exception_type=AssertionError)
    check_capsys(capsys)


@pytest.mark.parametrize(
    'level, expected',
    [
        (1, 'Title\n=====\n\n'),
        (2, 'Title\n-----\n\n'),
        (3, 'Title\n~~~~~\n\n'),
        (6, "Title\n'''''\n\n"),
        (7, 'Title\n`````\n\n'),
        (9, 'Title\n:::::\n\n'),
    ]
)
def test_heading_levels(capsys: pytest.CaptureFixture[str],
                        level: int, expected: str) -> None:
    """Test heading underline style by heading level."""
    check_rst_output(
        capsys=capsys,
        method_calls=[('new_heading', {'level': level, 'text': 'Title'})],
        expected_text=expected)


def test_heading_add_text_url_and_code(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test adding text, URL and code in heading state."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_heading', {'level': 2, 'text': 'Check'}),
            ('add_text', {'text': ' this'}),
            ('add_url', {'url': 'http://example.com'}),
            ('add_code_in_text', {'text': ' now'}),
        ],
        expected_text='Check this `http://example.com <http://example.com>`_ '
                      '``now``\n'
                      '-------------------------------------------------------'
                      '------\n\n')


def test_heading_not_wrapped_by_line_length(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading is not wrapped even with short configured line length."""
    check_rst_output(
        capsys=capsys,
        method_calls=[('new_heading',
                       {'level': 1, 'text': 'a b c d e f g h i'})],
        expected_text='a b c d e f g h i\n=================\n\n',
        args={'line_length': 11})


@pytest.mark.parametrize(
    'programming_language, expected',
    [
        (None,
         '::\n'
         '\n'
         '    print(1)\n'
         '\n'),
        ('python',
         '.. code:: python\n'
         '\n'
         '    print(1)\n'
         '\n'),
    ]
)
def test_write_code_block(capsys: pytest.CaptureFixture[str],
                          programming_language: str,
                          expected: str) -> None:
    """Test code block start and end markers."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('write_code_block', {
                'text': 'print(1)\n',
                'programming_language': programming_language,
            }),
        ],
        expected_text=expected)


def test_encode_text_restructuredtext_escapes(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test _encode_text escapes reST-sensitive characters."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.rst')
        with create_mf('reST', file_name) as mfd:
            assert type(mfd).__name__ == 'MultiFormatRst'
            # pylint: disable=protected-access
            assert mfd._encode_text(r'a*b `c` |d \e') == \
                r'a\*b \`c\` \|d \\e'
    check_capsys(capsys)


@pytest.mark.parametrize(
    'character_encoding, expected_text_bytes',
    [('utf-8', b'Caf\xc3\xa9'), ('iso-8859-1', b'Caf\xe9')]
)
def test_character_encoding_writes_expected_bytes(
        capsys: pytest.CaptureFixture[str],
        character_encoding: str,
        expected_text_bytes: bytes) -> None:
    """Test that reST output bytes match selected character encoding."""
    raw_content = create_paragraph_file_bytes(
        formatter_class=MultiFormatRst,
        file_extension=RST_FILE_EXTENSION,
        character_encoding=character_encoding)
    check_character_encoding_bytes(
        raw_content=raw_content,
        character_encoding=character_encoding,
        expected_text_bytes=expected_text_bytes)
    check_capsys(capsys)


def test_invalid_character_encoding_raises_lookup_error(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test invalid encoding is propagated from Python open."""
    check_invalid_character_encoding_constructor(
        formatter_class=MultiFormatRst,
        file_extension=RST_FILE_EXTENSION)
    check_capsys(capsys)
