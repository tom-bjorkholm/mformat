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
from e04_paragraphs_smart_ws import paragraphs_smart_ws_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    'With new_paragraph we can start a paragraph. '
    'Thanks to smart whitespace\n'
    'handling, we do not need to add whitespace between text '
    'fragments from different\n'
    'calls to add_text or new_paragraph calls. If we have extra '
    'whitespace, it will\n'
    'be consolidated into a single space.\n\n',
    'With new_paragraph we can start another paragraph. '
    'With smart_ws=False the\n'
    'whitespace between text fragments will be preserved.So we can '
    'have no whitespae\n'
    'or multiple spaces between text fragments if we want to. '
    'We can at any time\n'
    'switch on smart whitespace handling by ommitting the '
    'smart_ws=False argument, or\n'
    'by explicitly setting smart_ws=True.\n\n',
    '**(As this example does not have a heading the generated',
    'markdown file will not',
    'have a heading. If markdownlint is used on the generated',
    'markdown file it will',
    'report an error for the missing heading.)**'
]
EXPECTED_HTML_BODY_TEXT = [
    '<p>',
    'With new_paragraph we can start a paragraph.',
    'Thanks to smart whitespace handling, we do not need to add',
    'whitespace between text fragments from different calls to',
    'add_text or new_paragraph calls. If we have extra whitespace,',
    'it will be consolidated into a single space.',
    '</p>',
    '<p>',
    'With new_paragraph we can start another paragraph.  With smart_ws=False',
    'the whitespace between text  fragments will be preserved.So we can have',
    'no whitespae or multiple spaces between text fragments if we want to. ',
    'We can at any time switch on smart whitespace handling by ommitting',
    'the smart_ws=False argument, or by explicitly setting smart_ws=True.',
    '</p>',
    '<p>',
    '<strong>',
    '(As this example does not have a heading the generated',
    'markdown file will not have a heading. If markdownlint is used on the',
    'generated markdown file it will report an error for the missing heading.)',
    '</strong>',
    '</p>',
    ]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e04_paragraphs_smart_ws_md(capsys):
    """Test the paragraphs_smart_ws_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # MD041: First line in file should be a top level heading
    expected_error = ['MD041']
    check_markdown_func(paragraphs_smart_ws_example, expected_txt, expected_error)
    check_capsys_silent(capsys)


def test_e04_paragraphs_smart_ws_html(capsys):
    """Test the paragraphs_smart_ws_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(paragraphs_smart_ws_example, expected_txt)
    check_capsys_silent(capsys)


def test_e04_paragraphs_smart_ws_docx(capsys):
    """Test the paragraphs_smart_ws_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(paragraphs_smart_ws_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e04_paragraphs_smart_ws_odt(capsys):
    """Test the paragraphs_smart_ws_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(paragraphs_smart_ws_example, expected_txt)
    check_capsys_silent(capsys)
