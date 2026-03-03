#! /usr/local/bin/python3
"""Test the mformat_md module core functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from mformat.mformat import FormatterDescriptor
from mformat.mformat_md import MultiFormatMd
from mformat.mformat_state import Formatting, MultiFormatState
from mformat.mformat_textbased import split_whitespace
from .check_capsys import check_capsys
from .test_helpers import (check_formatter_character_encoding,
                           check_invalid_character_encoding_constructor,
                           check_run_with_context_manager,
                           run_protected_method)


@pytest.mark.parametrize('text, expected',
                         [('', ('', '', '')),
                          (' ', (' ', '', '')),
                          ('text', ('', 'text', '')),
                          ('  text  ', ('  ', 'text', '  ')),
                          ('  text ', ('  ', 'text', ' ')),
                          (' text  ', (' ', 'text', '  ')),
                          ('text  ', ('', 'text', '  ')),
                          ('  text', ('  ', 'text', '')),
                          ('  text  ', ('  ', 'text', '  '))])
def test_split_whitespace(text, expected) -> None:
    """Test the split_whitespace function."""
    assert split_whitespace(text) == expected


def test_file_name_extension(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file_name_extension method."""
    assert MultiFormatMd.file_name_extension() == '.md'
    check_capsys(capsys)


def test_get_arg_desciption(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_arg_desciption method."""
    assert MultiFormatMd.get_arg_desciption() == \
        FormatterDescriptor(name='md', mandatory_args=[],
                            optional_args=['character_encoding'])
    check_capsys(capsys)


@pytest.mark.parametrize('method, arg, expected',
                         [('_write_file_prefix', None, ''),
                          ('_write_file_suffix', None, ''),
                          ('_start_paragraph', None, ''),
                          ('_end_paragraph', None, '\n'),
                          ('_write_text',
                           ('test', MultiFormatState.PARAGRAPH,
                            Formatting(bold=False, italic=False)), 'test.'),
                          ('_write_text',
                           ('test\ntest', MultiFormatState.PARAGRAPH,
                            Formatting(bold=False, italic=False)),
                           'test\ntest.'),
                          ('_write_text',
                           ('bold', MultiFormatState.PARAGRAPH,
                            Formatting(bold=True, italic=False)), '**bold**.'),
                          ('_write_text',
                           ('italic', MultiFormatState.PARAGRAPH,
                            Formatting(bold=False, italic=True)), '*italic*.'),
                          ('_write_text',
                           ('both', MultiFormatState.PARAGRAPH,
                            Formatting(bold=True, italic=True)),
                           '***both***.'),
                          ('_write_text',
                           (' bold  ', MultiFormatState.PARAGRAPH,
                            Formatting(bold=True, italic=False)),
                           ' **bold**  .'),
                          ('_write_text',
                           ('  italic ', MultiFormatState.PARAGRAPH,
                            Formatting(bold=False, italic=True)),
                           '  *italic* .'),
                          ('_write_text',
                           ('  both  ', MultiFormatState.PARAGRAPH,
                            Formatting(bold=True, italic=True)),
                           '  ***both***  .')])
def test_methods(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                 method, arg, expected) -> None:
    """Test the trivial methods of the MultiFormatMd class."""
    with TemporaryDirectory() as tmp_dir:
        fname = str(Path(tmp_dir) / 'test.md')
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
            if method == '_write_text':
                mfd._write_text(text='.',  # pylint: disable=protected-access
                                state=MultiFormatState.PARAGRAPH,
                                formatting=Formatting(bold=False,
                                                      italic=False))
        with open(fname, 'rt', encoding='utf-8') as file:
            assert file.read() == expected
        check_capsys(capsys)


@pytest.mark.parametrize('level, expected_prefix',
                         [(1, '# '),
                          (2, '## '),
                          (3, '### '),
                          (4, '#### '),
                          (5, '##### '),
                          (6, '###### ')])
def test_start_heading(capsys: pytest.CaptureFixture[str],
                       level: int, expected_prefix: str) -> None:
    """Test the _start_heading method."""
    txt = run_protected_method('md', '.md', '_start_heading', (level,))
    assert txt == expected_prefix
    check_capsys(capsys)


def test_end_heading(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the _end_heading method."""
    txt = run_protected_method('md', '.md', '_end_heading', (1,))
    assert txt == '\n'
    check_capsys(capsys)


@pytest.mark.parametrize('level, text, expected',
                         [(1, 'Main Title', '# Main Title\n'),
                          (2, 'Subtitle', '## Subtitle\n'),
                          (3, 'Section', '### Section\n')])
def test_heading_integration(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             level, text, expected) -> None:
    """Test complete heading creation."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=level, text=text)

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


@pytest.mark.parametrize('level, text, bold, italic, expected',
                         [(1, 'Bold Title', True, False,
                           '# **Bold Title**\n'),
                          (2, 'Italic Title', False, True,
                           '## *Italic Title*\n'),
                          (3, 'Both', True, True,
                           '### ***Both***\n')])
def test_heading_formatting(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                            level, text, bold, italic, expected) -> None:
    """Test heading with bold and italic formatting."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=level, text=text, bold=bold, italic=italic)

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_add_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test adding text to a heading."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=1, text='Title')
        mfd.add_text(text=' and more')

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text='# Title and more\n',
                                   capsys=capsys)


@pytest.mark.parametrize('ws,url,utxt,expected',
                         [(False, 'http://example.com', 'this link',
                           '[this link](http://example.com)\n'),
                          (True, 'http://example.com', 'this link',
                           ' [this link](http://example.com)\n')])
def test_ws_add_url(capsys: pytest.CaptureFixture[str],
                    ws: bool, url: str, utxt: str, expected: str) -> None:
    """Test adding URL with whitespace."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.state = MultiFormatState.HEADING
        mfd.heading_level = 1
        mfd.ws_needed_at_append = ws
        mfd.add_url(url=url, text=utxt)

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


@pytest.mark.parametrize('htxt, url, utxt, bold, expected',
                         [('Check ', 'http://example.com', 'this link', False,
                           '## Check [this link](http://example.com)\n'),
                          ('Check', 'http://example.com', 'this link', False,
                           '## Check [this link](http://example.com)\n'),
                          ('Check ', 'http://example.com', None, False,
                           '## Check [http://example.com]' +
                           '(http://example.com)\n'),
                          ('Check ', 'http://example.com', 'this link', True,
                           '## Check **[this link](http://example.com)**\n'),
                          ('Check', 'http://example.com', 'this link', True,
                           '## Check **[this link](http://example.com)**\n'),
                          ('Check ', 'http://example.com', None, True,
                           '## Check **[http://example.com]' +
                           '(http://example.com)**\n'),])
def test_heading_add_url(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         htxt, url, utxt, bold, expected) -> None:
    """Test adding URL to a heading."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=2, text=htxt)
        mfd.add_url(url=url, text=utxt, bold=bold)

    # pylint: disable=duplicate-code
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by paragraph."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=1, text='Title')
        mfd.new_paragraph('Some text')

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text='# Title\n\nSome text\n',
                                   capsys=capsys)


def test_multiple_headings(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple headings."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=1, text='Main')
        mfd.new_heading(level=2, text='Sub')
        mfd.new_heading(level=3, text='Subsub')

    # pylint: disable=duplicate-code
    expected = '# Main\n\n## Sub\n\n### Subsub\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_paragraph_heading(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading, paragraph, then another heading."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=1, text='First Heading')
        mfd.new_paragraph('Some content here.')
        mfd.new_heading(level=2, text='Second Heading')

    expected = '# First Heading\n\nSome content here.\n\n## Second Heading\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


# Tests for code blocks


def test_simple_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a simple code block."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_code_block(text='print("Hello, World!")')

    expected = '````text\nprint("Hello, World!")\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_code_block_with_language(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a code block with programming language."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_code_block(text='print("Hello")',
                             programming_language='python')

    expected = '````python\nprint("Hello")\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_code_block_multiline(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a multiline code block."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        code = 'def hello():\n    print("Hello")\n    return True'
        mfd.write_code_block(text=code, programming_language='python')

    expected = ('````python\ndef hello():\n    print("Hello")\n'
                '    return True\n````\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_code_block_with_special_chars(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test a code block with special characters."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        code = 'x = "test <>&"\ny = \'another\''
        mfd.write_code_block(text=code)

    expected = '````text\nx = "test <>&"\ny = \'another\'\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_paragraph_then_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by code block."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_paragraph(text='Here is some code:')
        mfd.write_code_block(text='x = 42', programming_language='python')

    expected = 'Here is some code:\n\n````python\nx = 42\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_code_block_then_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test code block followed by paragraph."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_code_block(text='x = 42')
        mfd.new_paragraph(text='That was the code.')

    expected = '````text\nx = 42\n````\n\nThat was the code.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by code block."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=2, text='Code Example')
        mfd.write_code_block(text='example()', programming_language='python')

    expected = '## Code Example\n\n````python\nexample()\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_multiple_code_blocks(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple code blocks."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_code_block(text='x = 1', programming_language='python')
        mfd.write_code_block(text='y = 2', programming_language='python')

    expected = ('````python\nx = 1\n````\n'
                '\n````python\ny = 2\n````\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


@pytest.mark.parametrize('bold', [True, False])
@pytest.mark.parametrize('italic', [True, False])
@pytest.mark.parametrize('text, expected',
                         [('', ''),
                          (' ', ' '),
                          ('   ', '   ')])
def test_format_text_space(capsys: pytest.CaptureFixture[str],
                           bold: bool, italic: bool,
                           text: str, expected: str) -> None:
    """Test the format_text method with space."""
    # pylint: disable=protected-access
    formatting = Formatting(bold=bold, italic=italic)
    assert MultiFormatMd._format_text(text, formatting) == expected
    check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('bold text', True, False, '**bold text**'),
                          ('italic text', False, True, '*italic text*'),
                          ('both', True, True, '***both***'),
                          ('  bold text', True, False, '  **bold text**'),
                          ('italic text  ', False, True, '*italic text*  '),
                          (' both ', True, True, ' ***both*** ')])
def test_format_text_formatting(capsys: pytest.CaptureFixture[str],
                                text: str, bold: bool, italic: bool,
                                expected: str) -> None:
    """Test the format_text method with formatting."""
    # pylint: disable=protected-access
    formatting = Formatting(bold=bold, italic=italic)
    assert MultiFormatMd._format_text(text, formatting) == expected
    check_capsys(capsys)


def test_add_code_in_text_heading(capsys: pytest.CaptureFixture[str]) -> None:
    """Test add_code_in_text in heading."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=1, text='Code Example')
        mfd.add_code_in_text(text='example()')
        mfd.add_text('and more')
        mfd.new_paragraph(text='A paragraph.')

    expected = '# Code Example `example()` and more\n\nA paragraph.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


# Tests for block quotes


def test_simple_block_quote(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a simple block quote."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_block_quote(text='This is a quote.')

    expected = '> This is a quote.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_block_quote_with_add_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote with additional text."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_block_quote(text='Start of quote')
        mfd.add_text(text='and more text.')

    expected = '> Start of quote and more text.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


@pytest.mark.parametrize('bold, italic, expected', [
    (True, False, '> **Bold quote**\n'),
    (False, True, '> *Italic quote*\n'),
    (True, True, '> ***Bold and italic***\n'),
])
def test_block_quote_formatting(capsys: pytest.CaptureFixture[str],
                                bold: bool, italic: bool,
                                expected: str) -> None:
    """Test block quote with bold and italic formatting."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        text = 'Bold quote' if bold and not italic else \
               'Italic quote' if italic and not bold else \
               'Bold and italic'
        mfd.new_block_quote(text=text, bold=bold, italic=italic)

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_block_quote_with_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote with URL."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_block_quote(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    expected = '> Check [this link](http://example.com)\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_block_quote_with_code_in_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote with inline code."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_block_quote(text='Use the')
        mfd.add_code_in_text(text='print()')
        mfd.add_text(text='function.')

    expected = '> Use the `print()` function.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_block_quote_line_wrapping(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that block quote wraps lines with > prefix."""
    with TemporaryDirectory() as tmp_dir:
        fname = str(Path(tmp_dir) / 'test.md')
        with MultiFormatMd(file_name=fname) as mfd:
            long_text = ('This is a very long quote that should wrap to '
                         'multiple lines in the output because it exceeds '
                         'the maximum line length.')
            mfd.new_block_quote(text=long_text)
        with open(fname, 'rt', encoding='utf-8') as f:
            content = f.read()
        # Check that all lines start with >
        lines = content.strip().split('\n')
        for line in lines:
            msg = f"Line '{line}' should start with '> '"
            assert line.startswith('> '), msg
        check_capsys(capsys)


def test_block_quote_then_paragraph(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote followed by paragraph."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_block_quote(text='A quoted text.')
        mfd.new_paragraph(text='A normal paragraph.')

    expected = '> A quoted text.\n\nA normal paragraph.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_paragraph_then_block_quote(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by block quote."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_paragraph(text='A normal paragraph.')
        mfd.new_block_quote(text='A quoted text.')

    expected = 'A normal paragraph.\n\n> A quoted text.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_block_quote(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by block quote."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=2, text='Quote Section')
        mfd.new_block_quote(text='This is quoted.')

    expected = '## Quote Section\n\n> This is quoted.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_multiple_block_quotes(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple block quotes in sequence."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_block_quote(text='First quote.')
        mfd.new_block_quote(text='Second quote.')

    expected = '> First quote.\n\n> Second quote.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_block_quote_then_code_block(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote followed by code block."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_block_quote(text='Here is some code:')
        mfd.write_code_block(text='x = 42', programming_language='python')

    expected = '> Here is some code:\n\n````python\nx = 42\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


@pytest.mark.parametrize('character_encoding, expected_text_bytes',
                         [('utf-8', b'Caf\xc3\xa9'),
                          ('iso-8859-1', b'Caf\xe9')])
def test_character_encoding_writes_expected_bytes(
        capsys, character_encoding, expected_text_bytes) -> None:
    """Test that Markdown output bytes match selected character encoding."""
    check_formatter_character_encoding(
        formatter_class=MultiFormatMd, file_extension='.md',
        character_encoding=character_encoding,
        expected_text_bytes=expected_text_bytes)
    check_capsys(capsys)


def test_invalid_character_encoding_raises_lookup_error(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test invalid encoding is propagated from Python open."""
    check_invalid_character_encoding_constructor(
        formatter_class=MultiFormatMd, file_extension='.md')
    check_capsys(capsys)
