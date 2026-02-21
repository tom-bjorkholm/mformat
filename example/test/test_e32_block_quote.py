#! /usr/local/bin/python3
"""Test the e32_block_quote example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest  # pylint: disable=unused-import # noqa: F401
from test_e01_paragraph import EXPECTED_HTML_PRE, EXPECTED_HTML_POST, \
    EXPECTED_ODT_PRE
from example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_docx_func, check_odt_func)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e32_block_quote import block_quote_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# Block Quote Example\n\n',
    'Block quotes are used to highlight quoted text',
    '> This is a simple block quote.',
    '> Block quotes can have',
    '**bold**',
    '*italic*',
    '> For more information, visit',
    '[Example Website](http://example.com)',
    '> The function',
    '`new_block_quote()`',
    '`add_text()`',
    'Block quotes cannot be nested.'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Block Quote Example',
    '</h1>',
    '<p>',
    'Block quotes are used to highlight quoted text',
    '</p>',
    '<h2>',
    'Simple Block Quote',
    '</h2>',
    '<blockquote>',
    'This is a simple block quote.',
    '</blockquote>',
    '<h2>',
    'Block Quote with Formatting',
    '</h2>',
    '<blockquote>',
    'Block quotes can have',
    '<strong>',
    'bold',
    '</strong>',
    '<em>',
    'italic',
    '</em>',
    '</blockquote>',
    '<h2>',
    'Block Quote with URL',
    '</h2>',
    '<blockquote>',
    'For more information, visit',
    '<a href="http://example.com">Example Website</a>',
    '</blockquote>',
    '<h2>',
    'Block Quote with Code',
    '</h2>',
    '<blockquote>',
    'The function',
    '<code>new_block_quote()</code>',
    '<code>add_text()</code>',
    '</blockquote>',
    '<p>',
    'Block quotes cannot be nested.',
    '</p>'
]
EXPECTED_DOCX_BODY_TEXT = [
    '<h1>',
    'Block Quote Example',
    '</h1>',
    '<p>',
    'Block quotes are used to highlight quoted text',
    '</p>',
    '<h2>',
    'Simple Block Quote',
    '</h2>',
    '<p>',
    'This is a simple block quote.',
    '</p>',
    '<h2>',
    'Block Quote with Formatting',
    '</h2>',
    '<p>',
    'Block quotes can have',
    '<strong>',
    'bold',
    '</strong>',
    '<em>',
    'italic',
    '</em>',
    '</p>',
    '<h2>',
    'Block Quote with URL',
    '</h2>',
    '<p>',
    'For more information, visit',
    '<a href="http://example.com">Example Website</a>',
    '</p>',
    '<h2>',
    'Block Quote with Code',
    '</h2>',
    '<p>',
    'The function',
    'new_block_quote()',
    'add_text()',
    '</p>',
    '<p>',
    'Block quotes cannot be nested.',
    '</p>'
]
EXPECTED_ODT_BODY_TEXT = [
    '<h1',
    'Block Quote Example',
    '</h1>',
    '<p',
    'Block quotes are used to highlight quoted text',
    '</p>',
    '<h2',
    'Simple Block Quote',
    '</h2>',
    '<p class="P-block-quote">',
    'This is a simple block quote.',
    '</p>',
    '<h2',
    'Block Quote with Formatting',
    '</h2>',
    '<p class="P-block-quote">',
    'Block quotes can have',
    '<span',
    'bold',
    '</span',
    '<span',
    'italic',
    '</span',
    '</p>',
    '<h2',
    'Block Quote with URL',
    '</h2>',
    '<p class="P-block-quote">',
    'For more information, visit',
    '<a href="http://example.com">Example Website</a>',
    '</p>',
    '<h2',
    'Block Quote with Code',
    '</h2>',
    '<p class="P-block-quote">',
    'The function',
    'new_block_quote()',
    'add_text()',
    '</p>',
    '<p',
    'Block quotes cannot be nested.',
    '</p>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + \
    EXPECTED_HTML_POST
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + \
    EXPECTED_HTML_POST


def test_e32_block_quote_md(capsys):
    """Test the block_quote_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(block_quote_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e32_block_quote_html(capsys):
    """Test the block_quote_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(block_quote_example, expected_txt)
    check_capsys_silent(capsys)


def test_e32_block_quote_docx(capsys):
    """Test the block_quote_example function with the docx format."""
    expected_txt = EXPECTED_DOCX_BODY_TEXT
    expected_warnings = []
    check_docx_func(block_quote_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e32_block_quote_odt(capsys):
    """Test the block_quote_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(block_quote_example, expected_txt)
    check_capsys_silent(capsys)
