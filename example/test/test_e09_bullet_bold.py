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
from e09_bullet_bold import bullet_bold_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '# Bullet list with bold text example\n\n',
    '- This is the first bullet point item. '
    'This is not bold or italic. **However,\n'
    '  this bold text is added to it.** '
    '*And this italic text is added to it.*\n\n',
    '- **This is the bold bullet point item.** '
    'This non-bold text is added to it.\n\n',
    '- *This is the italic bullet point item.* '
    'This non-italic text is added to it.\n\n',
    '- ***This is the bold and italic bullet point item.*** '
    'This non-bold and\n'
    '  non-italic text is added to it.\n\n',
    '  - This is in item in a nested bullet list. '
    '**Bold text added to it.** *And\n'
    '    italic text added to it.*\n\n',
    '  - ***Second nested bullet point item.*** This non-bold ',
    'and non-italic text is\n'
    '    added to it. **And bold** *and italic text added to it.*\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Bullet list with bold text example',
    '</h1>',
    '<ul>', '<li>',
    'This is the first bullet point item.',
    'This is not bold or italic.',
    '<strong>',
    'However, this bold text is added to it.',
    '</strong>', '<em>',
    'And this italic text is added to it.',
    '</em>', '</li>', '<li>', '<strong>',
    'This is the bold bullet point item.',
    '</strong>',
    'This non-bold text is added to it.',
    '</li>', '<li>', '<em>',
    'This is the italic bullet point item.',
    '</em>',
    'This non-italic text is added to it.',
    '</li>', '<li>', '<em>', '<strong>',
    'This is the bold and italic bullet point item.',
    '</strong>', '</em>',
    'This non-bold and non-italic text is added to it.',
    '</li>', '<ul>', '<li>',
    'This is in item in a nested bullet list.',
    '<strong>',
    'Bold text added to it.',
    '</strong>', '<em>',
    'And italic text added to it.',
    '</em>', '</li>', '<li>', '<em>', '<strong>',
    'Second nested bullet point item.',
    '</strong>','</em>',
   'This non-bold and non-italic text is added to it.',
    '<strong>',
    'And bold',
    '</strong>', '<em>',
    'and italic text added to it.',
    '</em>','</li>','</ul>','</ul>'
]
EXPECTED_DOCX_HTML_BODY_TEXT = [
    '<h1>',
    'Bullet list with bold text example',
    '</h1>',
    '<ul>', '<li>',
    'This is the first bullet point item.',
    'This is not bold or italic.',
    '<strong>',
    'However, this bold text is added to it.',
    '</strong>', '<em>',
    'And this italic text is added to it.',
    '</em>', '</li>', '<li>', '<strong>',
    'This is the bold bullet point item.',
    '</strong>',
    'This non-bold text is added to it.',
    '</li>', '<li>', '<em>',
    'This is the italic bullet point item.',
    '</em>',
    'This non-italic text is added to it.',
    '</li>', '<li>', '<em>', '<strong>',
    'This is the bold and italic bullet point item.',
    '</strong>', '</em>',
    'This non-bold and non-italic text is added to it.',
    '</li>', 
#    '<ul>',  # Check is docx can make this real nested list.
    '<li>',
    'This is in item in a nested bullet list.',
    '<strong>',
    'Bold text added to it.',
    '</strong>', '<em>',
    'And italic text added to it.',
    '</em>', '</li>', '<li>', '<em>', '<strong>',
    'Second nested bullet point item.',
    '</strong>','</em>',
   'This non-bold and non-italic text is added to it.',
    '<strong>',
    'And bold',
    '</strong>', '<em>',
    'and italic text added to it.',
    '</em>', '</li>',
#   '</ul>',
    '</ul>'
]
EXPECTED_ODT_HTML_BODY_TEXT = [
    '<h1>',
    'Bullet list with bold text example',
    '</h1>',
    '<ul>', '<li>',
    'This is the first bullet point item.',
    'This is not bold or italic.',
    '<strong>',
    'However, this bold text is added to it.',
    '</strong>', '<em>',
    'And this italic text is added to it.',
    '</em>', '</li>', '<li>', '<strong>',
    'This is the bold bullet point item.',
    '</strong>',
    'This non-bold text is added to it.',
    '</li>', '<li>', '<em>',
    'This is the italic bullet point item.',
    '</em>',
    'This non-italic text is added to it.',
    '</li>', '<li>', '<em>', '<strong>',
    'This is the bold and italic bullet point item.',
    '</strong>', '</em>',
    'This non-bold and non-italic text is added to it.',
#   '</li>',  # ODT nested lists are in list item.
    '<ul>', '<li>',
    'This is in item in a nested bullet list.',
    '<strong>',
    'Bold text added to it.',
    '</strong>', '<em>',
    'And italic text added to it.',
    '</em>', '</li>', '<li>', '<em>', '<strong>',
    'Second nested bullet point item.',
    '</strong>','</em>',
   'This non-bold and non-italic text is added to it.',
    '<strong>',
    'And bold',
    '</strong>', '<em>',
    'and italic text added to it.',
    '</em>','</li>','</ul>','</ul>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_ODT_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e09_bullet_bold_md(capsys):
    """Test the bullet_bold_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(bullet_bold_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e09_bullet_bold_html(capsys):
    """Test the bullet_bold_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(bullet_bold_example, expected_txt)
    check_capsys_silent(capsys)


def test_e09_bullet_bold_docx(capsys):
    """Test the bullet_bold_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(bullet_bold_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e09_bullet_bold_odt(capsys):
    """Test the bullet_bold_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(bullet_bold_example, expected_txt)
    check_capsys_silent(capsys)
