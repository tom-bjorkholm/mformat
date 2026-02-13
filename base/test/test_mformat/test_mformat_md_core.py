#! /usr/local/bin/python3
"""Test the mformat_md module core functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
import pytest
from check_capsys import check_capsys
from test_helpers import (
    run_protected_method,
    check_run_with_context_manager
)
from mformat.mformat_md import MultiFormatMd, split_whitespace
from mformat.mformat_state import MultiFormatState, Formatting
from mformat.mformat import FormatterDescriptor


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
def test_split_whitespace(text, expected):
    """Test the split_whitespace function."""
    assert split_whitespace(text) == expected


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
def test_start_heading(capsys, level, expected_prefix):
    """Test the _start_heading method."""
    txt = run_protected_method('md', '.md', '_start_heading', (level,))
    assert txt == expected_prefix
    check_capsys(capsys)


def test_end_heading(capsys):
    """Test the _end_heading method."""
    txt = run_protected_method('md', '.md', '_end_heading', (1,))
    assert txt == '\n'
    check_capsys(capsys)


@pytest.mark.parametrize('level, text, expected',
                         [(1, 'Main Title', '# Main Title\n'),
                          (2, 'Subtitle', '## Subtitle\n'),
                          (3, 'Section', '### Section\n')])
def test_heading_integration(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             level, text, expected):
    """Test complete heading creation."""
    def test_action(mfd):
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
def test_heading_formatting(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                            level, text, bold, italic, expected):
    """Test heading with bold and italic formatting."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=level, text=text, bold=bold, italic=italic)

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_add_text(capsys):
    """Test adding text to a heading."""
    def test_action(mfd):
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
def test_ws_add_url(capsys, ws, url, utxt, expected):
    """Test adding URL with whitespace."""
    def test_action(mfd):
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
def test_heading_add_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         htxt, url, utxt, bold, expected):
    """Test adding URL to a heading."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=2, text=htxt)
        mfd.add_url(url=url, text=utxt, bold=bold)

    # pylint: disable=duplicate-code
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_paragraph(capsys):
    """Test heading followed by paragraph."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=1, text='Title')
        mfd.new_paragraph('Some text')

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text='# Title\n\nSome text\n',
                                   capsys=capsys)


def test_multiple_headings(capsys):
    """Test multiple headings."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=1, text='Main')
        mfd.new_heading(level=2, text='Sub')
        mfd.new_heading(level=3, text='Subsub')

    # pylint: disable=duplicate-code
    expected = '# Main\n\n## Sub\n\n### Subsub\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_paragraph_heading(capsys):
    """Test heading, paragraph, then another heading."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=1, text='First Heading')
        mfd.new_paragraph('Some content here.')
        mfd.new_heading(level=2, text='Second Heading')

    expected = '# First Heading\n\nSome content here.\n\n## Second Heading\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


# Tests for code blocks


def test_simple_code_block(capsys):
    """Test a simple code block."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_code_block(text='print("Hello, World!")')

    expected = '\n````text\nprint("Hello, World!")\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_code_block_with_language(capsys):
    """Test a code block with programming language."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_code_block(text='print("Hello")',
                             programming_language='python')

    expected = '\n````python\nprint("Hello")\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_code_block_multiline(capsys):
    """Test a multiline code block."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        code = 'def hello():\n    print("Hello")\n    return True'
        mfd.write_code_block(text=code, programming_language='python')

    expected = ('\n````python\ndef hello():\n    print("Hello")\n'
                '    return True\n````\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_code_block_with_special_chars(capsys):
    """Test a code block with special characters."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        code = 'x = "test <>&"\ny = \'another\''
        mfd.write_code_block(text=code)

    expected = '\n````text\nx = "test <>&"\ny = \'another\'\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_paragraph_then_code_block(capsys):
    """Test paragraph followed by code block."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_paragraph(text='Here is some code:')
        mfd.write_code_block(text='x = 42', programming_language='python')

    expected = 'Here is some code:\n\n````python\nx = 42\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_code_block_then_paragraph(capsys):
    """Test code block followed by paragraph."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_code_block(text='x = 42')
        mfd.new_paragraph(text='That was the code.')

    expected = '\n````text\nx = 42\n````\n\nThat was the code.\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_code_block(capsys):
    """Test heading followed by code block."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.new_heading(level=2, text='Code Example')
        mfd.write_code_block(text='example()', programming_language='python')

    expected = '## Code Example\n\n````python\nexample()\n````\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_multiple_code_blocks(capsys):
    """Test multiple code blocks."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_code_block(text='x = 1', programming_language='python')
        mfd.write_code_block(text='y = 2', programming_language='python')

    expected = ('\n````python\nx = 1\n````\n'
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
def test_format_text_space(capsys, bold, italic, text, expected):
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
def test_format_text_formatting(capsys, text, bold, italic, expected):
    """Test the format_text method with formatting."""
    # pylint: disable=protected-access
    formatting = Formatting(bold=bold, italic=italic)
    assert MultiFormatMd._format_text(text, formatting) == expected
    check_capsys(capsys)
