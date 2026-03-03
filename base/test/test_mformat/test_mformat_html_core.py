#! /usr/local/bin/python3
"""Test the mformat_html module core functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Any, Optional
import pytest
from mformat.factory import OptArgsDict
from mformat.mformat import FormatterDescriptor
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat_state import Formatting, MultiFormatState
from .check_capsys import check_capsys
from .test_helpers import (check_character_encoding_bytes,
                           check_invalid_character_encoding_constructor,
                           check_run_with_context_manager,
                           create_paragraph_file_bytes, run_protected_method)


def test_file_name_extension(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file_name_extension method."""
    assert MultiFormatHtml.file_name_extension() == '.html'
    check_capsys(capsys)


def test_get_arg_desciption(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_arg_desciption method."""
    assert MultiFormatHtml.get_arg_desciption() == \
        FormatterDescriptor(name='html', mandatory_args=[],
                            optional_args=['title', 'css_file', 'lang',
                                           'character_encoding'])
    check_capsys(capsys)


PFDT = '<!DOCTYPE html>\n<html lang="'
PTAL = '">\n<head>\n<meta charset="utf-8">\n<title>'
PFAT = '</title>\n'
PFCSS = '<link rel="stylesheet" href="'
PFCSSE = '">\n'
PFLS = '</head>\n<body>\n'

SFTOT = '</body>\n</html>\n'

PF_EN_NT_NC = PFDT + 'en' + PTAL + 'HTML file' + PFAT + PFLS
PF_SV_TS_C1 = PFDT + 'sv' + PTAL + 'Something' + PFAT + PFCSS + \
    'style1.css' + PFCSSE + PFLS


def args_for_file_prefix(lang: str, title: Optional[str],
                         css_file: Optional[str]) -> OptArgsDict:
    """Get the arguments for the file prefix."""
    args: OptArgsDict = {'lang': lang}
    if title is not None:
        args['title'] = title
    if css_file is not None:
        args['css_file'] = css_file
    return args


@pytest.mark.parametrize('lang, title, css_file, expected',
                         [('en', None, None, PF_EN_NT_NC),
                          ('sv', 'Something', 'style1.css', PF_SV_TS_C1)])
def test_write_file_prefix(capsys: pytest.CaptureFixture[str],
                           lang: str, title: Optional[str],
                           css_file: Optional[str], expected: str) -> None:
    """Test the write_file_prefix method."""
    args = args_for_file_prefix(lang, title, css_file)
    txt = run_protected_method('html', '.html', '_write_file_prefix',
                               args=args)
    assert txt == expected
    check_capsys(capsys)


def test_write_file_suffix(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the write_file_suffix method."""
    txt = run_protected_method('html', '.html', '_write_file_suffix')
    assert txt == SFTOT
    check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('Hello, world!', False, False, 'Hello, world!'),
                          ('Something else', False, False,
                           'Something else'),
                          ('Bold text', True, False,
                           '<strong>Bold text</strong>'),
                          ('Italic text', False, True,
                           '<em>Italic text</em>'),
                          ('Both', True, True,
                           '<em><strong>Both</strong></em>')])
def test_write_text(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                    text: str, bold: bool, italic: bool,
                    expected: str) -> None:
    """Test the _write_text method."""
    txt = run_protected_method('html', '.html', '_write_text',
                               (text, MultiFormatState.PARAGRAPH,
                                Formatting(bold=bold, italic=italic)))
    assert txt == expected
    check_capsys(capsys)


EN_NT_NC_T1 = PF_EN_NT_NC + '<p>\nHello, world!</p>\n<p>\nBye!</p>\n' + SFTOT
SV_TS_C1_T2 = PF_SV_TS_C1 + '<p>\nSomething else</p>\n<p>\nYeah!</p>\n' + \
    SFTOT
EN_NT_NC_BOLD = PF_EN_NT_NC + '<p>\n<strong>Bold text</strong></p>\n' + SFTOT
EN_NT_NC_ITALIC = PF_EN_NT_NC + '<p>\n<em>Italic text</em></p>\n' + SFTOT
EN_NT_NC_BOTH = PF_EN_NT_NC + \
    '<p>\n<em><strong>Both styles</strong></em></p>\n' + SFTOT


@pytest.mark.parametrize('level, expected',
                         [(1, '<h1>\n'),
                          (2, '<h2>\n'),
                          (3, '<h3>\n'),
                          (4, '<h4>\n'),
                          (5, '<h5>\n'),
                          (6, '<h6>\n')])
def test_start_heading(capsys: pytest.CaptureFixture[str],
                       level: int, expected: str) -> None:
    """Test the _start_heading method."""
    txt = run_protected_method('html', '.html', '_start_heading', (level,))
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('level, expected',
                         [(1, '</h1>\n'),
                          (2, '</h2>\n'),
                          (3, '</h3>\n'),
                          (4, '</h4>\n'),
                          (5, '</h5>\n'),
                          (6, '</h6>\n')])
def test_end_heading(capsys: pytest.CaptureFixture[str],
                     level: int, expected: str) -> None:
    """Test the _end_heading method."""
    txt = run_protected_method('html', '.html', '_end_heading', (level,))
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('level, text, expected',
                         [(1, 'Main Title',
                           PF_EN_NT_NC + '<h1>\nMain Title</h1>\n' + SFTOT),
                          (2, 'Subtitle',
                           PF_EN_NT_NC + '<h2>\nSubtitle</h2>\n' + SFTOT),
                          (3, 'Section',
                           PF_EN_NT_NC + '<h3>\nSection</h3>\n' + SFTOT)])
def test_heading_integration(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             level: int, text: str,
                             expected: str) -> None:
    """Test complete heading creation."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=level, text=text)

    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


@pytest.mark.parametrize('level, text, bold, italic, expected',
                         [(1, 'Bold Title', True, False,
                           '<h1>\n<strong>Bold Title</strong></h1>\n'),
                          (2, 'Italic Title', False, True,
                           '<h2>\n<em>Italic Title</em></h2>\n'),
                          (3, 'Both', True, True,
                           '<h3>\n<em><strong>Both</strong></em></h3>\n')])
def test_heading_formatting(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                            level: int, text: str,
                            bold: bool, italic: bool,
                            expected: str) -> None:
    """Test heading with bold and italic formatting."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=level, text=text, bold=bold, italic=italic)

    exp = PF_EN_NT_NC + expected + SFTOT
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_heading_add_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test adding text to a heading."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=1, text='Title')
        mfd.add_text(text=' and more')

    exp = PF_EN_NT_NC + '<h1>\nTitle and more</h1>\n' + SFTOT
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_heading_add_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test adding URL to a heading."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=2, text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    exp = (PF_EN_NT_NC + '<h2>\nCheck ' +
           '<a href="http://example.com">this link</a></h2>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_heading_then_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by paragraph."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=1, text='Title')
        mfd.new_paragraph('Some text')

    exp = (PF_EN_NT_NC + '<h1>\nTitle</h1>\n' +
           '<p>\nSome text</p>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_multiple_headings(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple headings."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=1, text='Main')
        mfd.new_heading(level=2, text='Sub')
        mfd.new_heading(level=3, text='Subsub')

    exp = (PF_EN_NT_NC + '<h1>\nMain</h1>\n' +
           '<h2>\nSub</h2>\n<h3>\nSubsub</h3>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_heading_paragraph_heading(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading, paragraph, then another heading."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=1, text='First Heading')
        mfd.new_paragraph('Some content here.')
        mfd.new_heading(level=2, text='Second Heading')

    exp = (PF_EN_NT_NC + '<h1>\nFirst Heading</h1>\n' +
           '<p>\nSome content here.</p>\n' +
           '<h2>\nSecond Heading</h2>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)

# Tests for code blocks


def test_simple_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a simple code block."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_code_block(text='print("Hello, World!")')

    exp = (PF_EN_NT_NC +
           '<pre><code>\nprint(&quot;Hello, World!&quot;)' +
           '</code></pre>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_code_block_with_language(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a code block with programming language."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_code_block(text='print("Hello")',
                             programming_language='python')

    exp = (PF_EN_NT_NC + '<pre><code>\n' +
           '<span class="language-python">print(&quot;Hello&quot;)</span>\n' +
           '</code></pre>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_code_block_multiline(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a multiline code block."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        code = 'def hello():\n    print("Hello")\n    return True'
        mfd.write_code_block(text=code, programming_language='python')

    # <pre> preserves whitespace including newlines, so no <br> needed
    exp = (PF_EN_NT_NC + '<pre><code>\n' +
           '<span class="language-python">def hello():\n' +
           '    print(&quot;Hello&quot;)\n' +
           '    return True</span>\n' +
           '</code></pre>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_code_block_with_special_chars(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test a code block with special characters."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        code = 'x = "test <>&"\ny = \'another\''
        mfd.write_code_block(text=code)
    # <pre> preserves whitespace including newlines, so no <br> needed
    exp = (PF_EN_NT_NC +
           '<pre><code>\nx = &quot;test &lt;&gt;&amp;&quot;\n' +
           'y = &#x27;another&#x27;</code></pre>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_paragraph_then_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by code block."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_paragraph(text='Here is some code:')
        mfd.write_code_block(text='x = 42', programming_language='python')

    exp = (PF_EN_NT_NC + '<p>\nHere is some code:</p>\n' +
           '<pre><code>\n<span class="language-python">x = 42' +
           '</span>\n</code></pre>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_code_block_then_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test code block followed by paragraph."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_code_block(text='x = 42')
        mfd.new_paragraph(text='That was the code.')

    exp = (PF_EN_NT_NC + '<pre><code>\nx = 42</code></pre>\n' +
           '<p>\nThat was the code.</p>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_heading_then_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by code block."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=2, text='Code Example')
        mfd.write_code_block(text='example()', programming_language='python')

    exp = (PF_EN_NT_NC + '<h2>\nCode Example</h2>\n' +
           '<pre><code>\n<span class="language-python">example()' +
           '</span>\n</code></pre>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_multiple_code_blocks(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple code blocks."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_code_block(text='x = 1', programming_language='python')
        mfd.write_code_block(text='y = 2', programming_language='python')

    exp = (PF_EN_NT_NC + '<pre><code>\n' +
           '<span class="language-python">x = 1</span>\n' +
           '</code></pre>\n<pre><code>\n' +
           '<span class="language-python">y = 2</span>\n' +
           '</code></pre>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)

# Tests for block quotes


def test_block_quote_1(capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_block_quote(text='Here is text')
    exp = (PF_EN_NT_NC + '<blockquote>\nHere is text</blockquote>\n' +
           SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_block_quote_2(capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_block_quote(text='Block quote')
        mfd.add_text(text='More text')
    exp = (PF_EN_NT_NC +
           '<blockquote>\nBlock quote More text</blockquote>\n' +
           SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


def test_block_quote_3(capsys: pytest.CaptureFixture[str]) -> None:
    """Test block quote."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_block_quote(text='Block quote')
        mfd.new_paragraph(text='Paragraph text')
    exp = (PF_EN_NT_NC + '<blockquote>\nBlock quote</blockquote>\n' +
           '<p>\nParagraph text</p>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


@pytest.mark.parametrize('character_encoding, expected_text_bytes',
                         [('utf-8', b'Caf\xc3\xa9'),
                          ('iso-8859-1', b'Caf\xe9')])
def test_character_encoding_writes_expected_bytes(
        capsys: pytest.CaptureFixture[str],
        character_encoding: str,
        expected_text_bytes: bytes) -> None:
    """Test that HTML output bytes match the selected character encoding."""
    raw_content = create_paragraph_file_bytes(
        formatter_class=MultiFormatHtml, file_extension='.html',
        character_encoding=character_encoding)
    check_character_encoding_bytes(
        raw_content=raw_content, character_encoding=character_encoding,
        expected_text_bytes=expected_text_bytes, expected_html_meta=True)
    check_capsys(capsys)


def test_invalid_character_encoding_raises_lookup_error(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test invalid encoding is propagated from Python open."""
    check_invalid_character_encoding_constructor(
        formatter_class=MultiFormatHtml, file_extension='.html')
    check_capsys(capsys)
