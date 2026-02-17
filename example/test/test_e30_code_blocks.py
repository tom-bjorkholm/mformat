#! /usr/local/bin/python3
"""Test the e30_code_blocks example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest  # pylint: disable=unused-import
from test_e01_paragraph import EXPECTED_HTML_PRE, EXPECTED_HTML_POST, EXPECTED_ODT_PRE
from example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_docx_func, check_odt_func, docx_version_of_html, odt_version_of_html)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e30_code_blocks import code_blocks_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501


def replace_in_beginning_of_lines(text: list[str],
                                  from_char: str, to_char: str) -> list[str]:
    """Replace all from_char with to_char in the beginning of the lines in text.

    All occurences of from_char in the beginning of the lines in text are
    replaced with to_char, until the first non-matching character is found.
    Args:
        text: The list of lines to replace in.
        from_char: The character to replace.
        to_char: The character to replace with.
    Returns:
        The list of lines with the replaced text.
    """
    result = []
    for line in text:
        stripped_line = line.lstrip(from_char)
        diff = len(line) - len(stripped_line)
        result.append(to_char * diff + stripped_line)
    return result


@pytest.mark.parametrize("text, from_char, to_char, expected",
                         [(['a b c', 'd e f'], 'a', 'x',
                           ['x b c', 'd e f']),
                          (['a b c', 'd e f'], 'a', 'new',
                           ['new b c', 'd e f']),
                          (['a b c', '  d e f'], ' ', '&#160;',
                           ['a b c', '&#160;&#160;d e f'])])
def test_replace_in_beginning_of_lines(text, from_char, to_char, expected):
    """Test the replace_in_beginning_of_lines function."""
    assert replace_in_beginning_of_lines(text, from_char, to_char) == expected


EXPECTED_MD_TEXT = [
    '# Code blocks example\n\n',
    'This is a normal paragraph with some text.',
    'Paragraphs are not useable for',
    'showing code as the text is usually shown in variable',
    'width fonts, and line',
    'wrapping is not easy to control. Code blocks on the other hand are',
    'designed to',
    'show code in a monospace font, and line wrapping is easy to control.',
    'Code blocks are written using the `write_code_block()` method.',
    'The function',
    'names mentioned in this paragraph are written using the `add_code_in_text()`',
    'method.',
    '\n````python\n\n',
    'def hello_world(i: int) -> int:\n'
    '    print("Hello, World!")\n'
    '    if i > 0:\n'
    '        print("i is positive")\n'
    '    elif i < 0:\n',
    '        print("i is negative")\n'
    '    else:\n'
    '        print("i is zero")\n',
    '    print("This is another line of code.")\n'
    '    return 42\n',
    '````\n'
]
EXPECTED_HTML_BODY_TEXT1 = [
    '<h1>',
    'Code blocks example',
    '</h1>',
    '<p>',
    'This is a normal paragraph with some text.',
    'Paragraphs are not useable for',
    'showing code as the text is usually shown in variable',
    'width fonts, and line',
    'wrapping is not easy to control. Code blocks on the other hand are',
    'designed to',
    'show code in a monospace font, and line wrapping is easy to control.',
    '</p>',
    '<p>',
    'Code blocks are written using the',
    '<code>',
    'write_code_block()',
    '</code>',
    'method. The function names mentioned in this paragraph are written',
    'using the',
    '<code>',
    'add_code_in_text()',
    '</code>',
    'method.'
    '</p>'
]
EXPECTED_HTML_BODY_TEXT2 = [
    '<pre>', '<code>',
    '<span class="language-python">',
    '\ndef hello_world(i: int) -&gt; int:\n'
    '    print(&quot;Hello, World!&quot;)\n'
    '    if i &gt; 0:\n'
    '        print(&quot;i is positive&quot;)\n'
    '    elif i &lt; 0:\n'
    '        print(&quot;i is negative&quot;)\n'
    '    else:\n'
    '        print(&quot;i is zero&quot;)\n'
    '    print(&quot;This is another line of code.&quot;)\n'
    '    return 42\n',
    '</span>', '</code>', '</pre>'
]
EXPECTED_DOCX_HTML_TEXT2 = [
    'def hello_world(i: int) -&gt; int:',
    '    print(&quot;Hello, World!&quot;)',
    '    if i &gt; 0:',
    '        print(&quot;i is positive&quot;)',
    '    elif i &lt; 0:',
    '        print(&quot;i is negative&quot;)',
    '    else:',
    '        print(&quot;i is zero&quot;)',
    '    print(&quot;This is another line of code.&quot;)',
    '    return 42'
]
EXPECTED_ODT_HTML_TEXT2 = \
    replace_in_beginning_of_lines(EXPECTED_DOCX_HTML_TEXT2, ' ', '&#160;')
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT1 + \
    EXPECTED_HTML_BODY_TEXT2 + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT1 +
                                             EXPECTED_ODT_HTML_TEXT2)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + \
    EXPECTED_HTML_POST



def test_e30_code_blocks_md(capsys):
    """Test the code_blocks_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(code_blocks_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e30_code_blocks_html(capsys):
    """Test the code_blocks_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(code_blocks_example, expected_txt)
    check_capsys_silent(capsys)


def test_e30_code_blocks_docx(capsys):
    """Test the code_blocks_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT1 +
                                        EXPECTED_DOCX_HTML_TEXT2)
    expected_warnings = []
    check_docx_func(code_blocks_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e30_code_blocks_odt(capsys):
    """Test the code_blocks_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(code_blocks_example, expected_txt)
    check_capsys_silent(capsys)
