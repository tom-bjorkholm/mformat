#! /usr/local/bin/python3
"""Test the mformat_docx module core functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from typing import Any, Callable, cast
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
import mammoth  # type: ignore[import-untyped]
from mformat_ext.mformat_docx import MultiFormatDocx
from mformat.mformat import FormatterDescriptor
from mformat.factory import create_mf

# Add base test helpers to path for shared test utilities
_base_test_path = (Path(__file__).parent.parent.parent.parent / 'base' /
                   'test')
sys.path.insert(0, str(_base_test_path))
# pylint: disable=wrong-import-order,wrong-import-position,import-error
from test_mformat.check_capsys import check_capsys  # noqa: E402


def test_file_name_extension(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file_name_extension method."""
    assert MultiFormatDocx.file_name_extension() == '.docx'
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_get_arg_desciption(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_arg_desciption method."""
    assert MultiFormatDocx.get_arg_desciption() == \
        FormatterDescriptor(name='docx', mandatory_args=[],
                            optional_args=[])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def silent_docx_create(capsys: pytest.CaptureFixture[str],
                       func: Callable[[MultiFormatDocx], None],
                       fname: str = 'test.docx') -> str:
    """Check that func can write to a docx file silently.

    func is expected to write to the file silently.
    Check that the file is created and that there are no output on
    stdout or stderr. We also check that the file exist and is not empty
    after func has been called.
    Returns:
        The content of the created file converted to HTML.
    """
    with TemporaryDirectory() as tmp_dir:
        fpath = str(Path(tmp_dir) / fname)
        with create_mf('docx', file_name=fpath) as mfd:
            assert isinstance(mfd, MultiFormatDocx)
            func(mfd)
        assert Path(fpath).exists()
        assert Path(fpath).stat().st_size > 0
        check_capsys(capsys)
        with open(fpath, 'rb') as f:
            content = mammoth.convert_to_html(f)
            for msg in content.messages:
                assert msg.type == 'warning'
            return cast(str, content.value)


@pytest.mark.parametrize('fname', ['test.docx', 'other.docx'])
def test_create_ok(capsys: pytest.CaptureFixture[str], fname: str) -> None:
    """Test the shortcut create function with an OK class."""

    def func(mfd: MultiFormatDocx) -> None:
        assert type(mfd).__name__ == 'MultiFormatDocx'

    silent_docx_create(capsys, func=func, fname=fname)


def test_create_nok(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the shortcut create function with a not OK class."""
    with pytest.raises(TypeError) as exc:
        invalid_args = cast(Any, {'output': 'test.docx'})
        with create_mf('docx', file_name='test.docx', args=invalid_args) as _:
            pass
    assert "MultiFormatDocx.__init__() got an unexpected " + \
        "keyword argument 'output'" in exc.value.args[0]
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


@pytest.mark.parametrize('level', [1, 2, 3, 4, 5, 6])
def test_heading_creation(capsys: pytest.CaptureFixture[str],
                          level: int) -> None:
    """Test creating headings at different levels."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=level, text=f'Heading Level {level}')

    html = silent_docx_create(capsys, func=func)
    assert f'<h{level}>Heading Level {level}</h{level}>' in html


def test_heading_with_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading with additional text."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=1, text='Main Title')
        mfd.add_text(text=' - Extended')

    html = silent_docx_create(capsys, func=func)
    assert '<h1>Main Title - Extended</h1>' in html


def test_heading_with_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading with URL."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=2, text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    html = silent_docx_create(capsys, func=func)
    assert '<h2>' in html
    assert 'Check' in html
    assert '<a href="http://example.com">this link</a>' in html


def test_heading_then_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by paragraph."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=1, text='Title')
        mfd.new_paragraph('Some text')

    html = silent_docx_create(capsys, func=func)
    assert '<h1>Title</h1>' in html
    assert '<p>Some text</p>' in html


def test_multiple_headings(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple headings."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=1, text='Main')
        mfd.new_heading(level=2, text='Sub')
        mfd.new_heading(level=3, text='Subsub')

    html = silent_docx_create(capsys, func=func)
    assert '<h1>Main</h1>' in html
    assert '<h2>Sub</h2>' in html
    assert '<h3>Subsub</h3>' in html


def test_heading_paragraph_heading(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading, paragraph, then another heading."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=1, text='First Heading')
        mfd.new_paragraph('Some content here.')
        mfd.new_heading(level=2, text='Second Heading')

    html = silent_docx_create(capsys, func=func)
    assert '<h1>First Heading</h1>' in html
    assert '<p>Some content here.</p>' in html
    assert '<h2>Second Heading</h2>' in html


@pytest.mark.parametrize('bold, italic', [(True, False), (False, True),
                                          (True, True)])
def test_heading_formatting(capsys: pytest.CaptureFixture[str], bold: bool,
                            italic: bool) -> None:
    """Test heading with bold and italic formatting."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=1,
                        text='Formatted Title',
                        bold=bold,
                        italic=italic)

    html = silent_docx_create(capsys, func=func)
    assert '<h1>' in html
    assert 'Formatted Title' in html
    if bold:
        assert '<strong>' in html
    if italic:
        assert '<em>' in html


# Tests for code blocks


def test_simple_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a simple code block."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.write_code_block(text='print("Hello, World!")')

    html = silent_docx_create(capsys, func=func)
    # Mammoth HTML-escapes double quotes
    assert 'print(' in html
    assert 'Hello, World!' in html


def test_code_block_with_language(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a code block with programming language."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.write_code_block(text='print("Hello")',
                             programming_language='python')

    html = silent_docx_create(capsys, func=func)
    # Mammoth HTML-escapes double quotes
    assert 'print(' in html
    assert 'Hello' in html


def test_code_block_multiline(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a multiline code block."""

    def func(mfd: MultiFormatDocx) -> None:
        code = 'def hello():\n    print("Hello")\n    return True'
        mfd.write_code_block(text=code, programming_language='python')

    html = silent_docx_create(capsys, func=func)
    assert 'def hello():' in html
    # Mammoth HTML-escapes double quotes
    assert 'print(' in html
    assert 'return True' in html


def test_code_block_with_special_chars(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test a code block with special characters."""

    def func(mfd: MultiFormatDocx) -> None:
        code = 'x = "test <>&"\ny = \'another\''
        mfd.write_code_block(text=code)

    html = silent_docx_create(capsys, func=func)
    # Special characters are HTML-escaped in mammoth output
    # Quotes become &quot;, < becomes &lt;, > becomes &gt;, & becomes &amp;
    assert 'x =' in html
    assert 'test' in html
    assert "y = 'another'" in html


def test_paragraph_then_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by code block."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_paragraph(text='Here is some code:')
        mfd.write_code_block(text='x = 42', programming_language='python')

    html = silent_docx_create(capsys, func=func)
    assert '<p>Here is some code:</p>' in html
    assert 'x = 42' in html


def test_code_block_then_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test code block followed by paragraph."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.write_code_block(text='x = 42')
        mfd.new_paragraph(text='That was the code.')

    html = silent_docx_create(capsys, func=func)
    assert 'x = 42' in html
    assert '<p>That was the code.</p>' in html


def test_heading_then_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by code block."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=2, text='Code Example')
        mfd.write_code_block(text='example()', programming_language='python')

    html = silent_docx_create(capsys, func=func)
    assert '<h2>Code Example</h2>' in html
    assert 'example()' in html


def test_multiple_code_blocks(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple code blocks."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.write_code_block(text='x = 1', programming_language='python')
        mfd.write_code_block(text='y = 2', programming_language='python')

    html = silent_docx_create(capsys, func=func)
    assert 'x = 1' in html
    assert 'y = 2' in html


# Tests for block quotes


def test_simple_block_quote(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a simple block quote."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_block_quote(text='This is a quote.')

    html = silent_docx_create(capsys, func=func)
    assert 'This is a quote.' in html


def test_block_quote_with_add_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote with additional text."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_block_quote(text='Start of quote')
        mfd.add_text(text=' and more text.')

    html = silent_docx_create(capsys, func=func)
    assert 'Start of quote' in html
    assert 'and more text.' in html


@pytest.mark.parametrize('bold, italic', [
    (True, False),
    (False, True),
    (True, True),
])
def test_block_quote_formatting(capsys: pytest.CaptureFixture[str], bold: bool,
                                italic: bool) -> None:
    """Test block quote with bold and italic formatting."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_block_quote(text='Formatted quote', bold=bold, italic=italic)

    html = silent_docx_create(capsys, func=func)
    assert 'Formatted quote' in html
    if bold:
        assert '<strong>' in html
    if italic:
        assert '<em>' in html


def test_block_quote_with_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote with URL."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_block_quote(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    html = silent_docx_create(capsys, func=func)
    assert 'Check' in html
    assert '<a href="http://example.com">this link</a>' in html


def test_block_quote_with_code_in_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote with inline code."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_block_quote(text='Use the')
        mfd.add_code_in_text(text='print()')
        mfd.add_text(text='function.')

    html = silent_docx_create(capsys, func=func)
    assert 'Use the' in html
    assert 'print()' in html
    assert 'function.' in html


def test_block_quote_then_paragraph(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote followed by paragraph."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_block_quote(text='A quoted text.')
        mfd.new_paragraph(text='A normal paragraph.')

    html = silent_docx_create(capsys, func=func)
    assert 'A quoted text.' in html
    assert '<p>A normal paragraph.</p>' in html


def test_paragraph_then_block_quote(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by block quote."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_paragraph(text='A normal paragraph.')
        mfd.new_block_quote(text='A quoted text.')

    html = silent_docx_create(capsys, func=func)
    assert '<p>A normal paragraph.</p>' in html
    assert 'A quoted text.' in html


def test_heading_then_block_quote(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by block quote."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=2, text='Quote Section')
        mfd.new_block_quote(text='This is quoted.')

    html = silent_docx_create(capsys, func=func)
    assert '<h2>Quote Section</h2>' in html
    assert 'This is quoted.' in html


def test_multiple_block_quotes(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple block quotes in sequence."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_block_quote(text='First quote.')
        mfd.new_block_quote(text='Second quote.')

    html = silent_docx_create(capsys, func=func)
    assert 'First quote.' in html
    assert 'Second quote.' in html


def test_block_quote_then_code_block(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote followed by code block."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_block_quote(text='Here is some code:')
        mfd.write_code_block(text='x = 42', programming_language='python')

    html = silent_docx_create(capsys, func=func)
    assert 'Here is some code:' in html
    assert 'x = 42' in html
