#! /usr/local/bin/python3
"""Test the mformat_docx module core functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from typing import Callable
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from mformat_ext.mformat_docx import MultiFormatDocx
from mformat.mformat import FormatterDescriptor
from mformat.factory import create_mf

# Add base test helpers to path for shared test utilities
_base_test_path = (
    Path(__file__).parent.parent.parent.parent /
    'base' / 'test' / 'test_mformat'
)
sys.path.insert(0, str(_base_test_path))
# pylint: disable=wrong-import-order,wrong-import-position,import-error
from check_capsys import check_capsys  # noqa: E402


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


def silent_docx_create(capsys,
                       func: Callable[[MultiFormatDocx], None],
                       fname: str = 'test.docx') -> None:
    """Check that func can write to a docx file silently.

    func is expected to write to the file silently.
    Check that the file is created and that there are no output on
    stdout or stderr. We also check that the file exist and is not empty
    after func has been called.
    """
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/' + fname
        with create_mf('docx', file_name=fpath) as mfd:
            func(mfd)
        assert os.path.exists(fpath)
        assert os.path.getsize(fpath) > 0
        check_capsys(capsys)


@pytest.mark.parametrize('fname', ['test.docx', 'other.docx'])
def test_create_ok(capsys, fname):
    """Test the shortcut create function with an OK class."""
    def func(mfd: MultiFormatDocx) -> None:
        assert type(mfd).__name__ == 'MultiFormatDocx'

    silent_docx_create(capsys, func=func, fname=fname)


def test_create_nok(capsys):
    """Test the shortcut create function with a not OK class."""
    with pytest.raises(TypeError) as exc:
        args = {'output': 'test.docx'}
        with create_mf('docx', file_name='test.docx', args=args) as _:
            pass
    assert "MultiFormatDocx.__init__() got an unexpected " + \
        "keyword argument 'output'" in exc.value.args[0]
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


@pytest.mark.parametrize('level', [1, 2, 3, 4, 5, 6])
def test_heading_creation(capsys, level):
    """Test creating headings at different levels."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=level, text=f'Heading Level {level}')

    silent_docx_create(capsys, func=func)


def test_heading_with_text(capsys):
    """Test heading with additional text."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=1, text='Main Title')
        mfd.add_text(text=' - Extended')

    silent_docx_create(capsys, func=func)


def test_heading_with_url(capsys):
    """Test heading with URL."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=2, text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    silent_docx_create(capsys, func=func)


def test_heading_then_paragraph(capsys):
    """Test heading followed by paragraph."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=1, text='Title')
        mfd.start_paragraph('Some text')

    silent_docx_create(capsys, func=func)


def test_multiple_headings(capsys):
    """Test multiple headings."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=1, text='Main')
        mfd.start_heading(level=2, text='Sub')
        mfd.start_heading(level=3, text='Subsub')
    silent_docx_create(capsys, func=func)


def test_heading_paragraph_heading(capsys):
    """Test heading, paragraph, then another heading."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=1, text='First Heading')
        mfd.start_paragraph('Some content here.')
        mfd.start_heading(level=2, text='Second Heading')

    silent_docx_create(capsys, func=func)


@pytest.mark.parametrize('bold, italic',
                         [(True, False),
                          (False, True),
                          (True, True)])
def test_heading_formatting(capsys, bold, italic):
    """Test heading with bold and italic formatting."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=1, text='Formatted Title',
                          bold=bold, italic=italic)

    silent_docx_create(capsys, func=func)


# Tests for code blocks


def test_simple_code_block(capsys):
    """Test a simple code block."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.write_code_block(text='print("Hello, World!")')

    silent_docx_create(capsys, func=func)


def test_code_block_with_language(capsys):
    """Test a code block with programming language."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.write_code_block(text='print("Hello")',
                             programming_language='python')

    silent_docx_create(capsys, func=func)


def test_code_block_multiline(capsys):
    """Test a multiline code block."""
    def func(mfd: MultiFormatDocx) -> None:
        code = 'def hello():\n    print("Hello")\n    return True'
        mfd.write_code_block(text=code, programming_language='python')

    silent_docx_create(capsys, func=func)


def test_code_block_with_special_chars(capsys):
    """Test a code block with special characters."""
    def func(mfd: MultiFormatDocx) -> None:
        code = 'x = "test <>&"\ny = \'another\''
        mfd.write_code_block(text=code)

    silent_docx_create(capsys, func=func)


def test_paragraph_then_code_block(capsys):
    """Test paragraph followed by code block."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_paragraph(text='Here is some code:')
        mfd.write_code_block(text='x = 42', programming_language='python')

    silent_docx_create(capsys, func=func)


def test_code_block_then_paragraph(capsys):
    """Test code block followed by paragraph."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.write_code_block(text='x = 42')
        mfd.start_paragraph(text='That was the code.')

    silent_docx_create(capsys, func=func)


def test_heading_then_code_block(capsys):
    """Test heading followed by code block."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=2, text='Code Example')
        mfd.write_code_block(text='example()', programming_language='python')

    silent_docx_create(capsys, func=func)


def test_multiple_code_blocks(capsys):
    """Test multiple code blocks."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.write_code_block(text='x = 1', programming_language='python')
        mfd.write_code_block(text='y = 2', programming_language='python')

    silent_docx_create(capsys, func=func)
