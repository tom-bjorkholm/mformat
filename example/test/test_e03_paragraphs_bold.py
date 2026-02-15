#! /usr/local/bin/python3
"""Test the e50_simple_complete example."""

# Copyright (c) 2025 - 2026 Tom Björkholm
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
from e03_paragraphs_bold import paragraphs_bold_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '**With new_paragraph we can start a paragraph with the first sentence '
    'in bold.**',
    'Use add_text to add text without bold to the paragraph. '
    '*Use add_text to add',
    'text in italic to the paragraph.* ***Use add_text to add '
    'text in bold and',
    'italic.***', '\n\n',
    '*With new_paragraph we can start a second paragraph with the first '
    'sentence in',
    'italic.* Use add_text to add text without italic to the second '
    'paragraph. **Use',
    'add_text to add text in bold to the second paragraph.** '
    '***Use add_text to add',
    'text in italic and bold to the second paragraph.***', '\n\n',
    '**(As this example does not have a heading the generated '
    'markdown file will not',
    'have a heading. If markdownlint is used on the generated '
    'markdown file it will',
    'report an error for the missing heading.)**'
]
EXPECTED_HTML_BODY_TEXT = [
    '<p>',
    '<strong>',
    'With new_paragraph we can start a paragraph with the first',
    'sentence in bold.',
    '</strong>',
    'Use add_text to add text without bold to the paragraph.',
    '<em>',
    'Use add_text to add text in italic to the paragraph.',
    '</em>', '<em>', '<strong>',
    'Use add_text to add text in bold and italic.',
    '</strong>', '</em>', '</p>',
    '<p>',
    '<em>',
    'With new_paragraph we can start a second paragraph with the',
    'first sentence in italic.',
    '</em>',
    'Use add_text to add text without italic to the second paragraph.',
    '<strong>',
    'Use add_text to add text in bold to the second paragraph.',
    '</strong>', '<em>', '<strong>',
    'Use add_text to add text in italic and bold to the second paragraph.',
    '</strong>', '</em>', '</p>',
    '<p>',
    '<strong>',
    '(As this example does not have a heading the generated markdown',
    'file will not have a heading. If markdownlint is used on the generated',
    'markdown file it will report an error for the missing heading.)',
    '</strong>',
    '</p>']
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e03_paragraphs_bold_md(capsys):
    """Test the paragraphs_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # MD041: First line in file should be a top level heading
    expected_error = ['MD041']
    check_markdown_func(paragraphs_bold_example, expected_txt, expected_error)
    check_capsys_silent(capsys)


def test_e03_paragraphs_bold_html(capsys):
    """Test the paragraphs_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(paragraphs_bold_example, expected_txt)
    check_capsys_silent(capsys)


def test_e03_paragraphs_bold_docx(capsys):
    """Test the paragraphs_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(paragraphs_bold_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e03_paragraphs_bold_odt(capsys):
    """Test the paragraphs_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(paragraphs_bold_example, expected_txt)
    check_capsys_silent(capsys)
