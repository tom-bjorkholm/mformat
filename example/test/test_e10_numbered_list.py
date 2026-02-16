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
from e10_numbered_list import numbered_list_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '# Numbered list example\n\n'
    '1. This is the first numbered item. We can add text '
    'to the numbered items with\n'
    '   add_text(), just as we can add text to paragraphs.\n\n'
    '2. This is the second numbered item.\n\n'
    '3. This is the third numbered item.\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Numbered list example',
    '</h1>',
    '<ol>', '<li>',
    'This is the first numbered item.',
    'We can add text to the numbered items with add_text(),',
    'just as we can add text to paragraphs.',
    '</li>','<li>',
    'This is the second numbered item.',
    '</li>','<li>',
    'This is the third numbered item.',
    '</li>',
    '</ol>'
]
EXPECTED_DOCX_HTML_BODY_TEXT = [
    '<h1>',
    'Numbered list example',
    '</h1>',
    '<p>',  # Check if docx can make this real numbered list.
    'This is the first numbered item.',
    'We can add text to the numbered items with add_text(),',
    'just as we can add text to paragraphs.',
    '</p>','<p>',  # Check if docx can make this real numbered list.
    'This is the second numbered item.',
    '</p>','<p>',  # Check if docx can make this real numbered list.
    'This is the third numbered item.',
    '</p>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e10_numbered_list_md(capsys):
    """Test the numbered_list_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(numbered_list_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e10_numbered_list_html(capsys):
    """Test the numbered_list_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(numbered_list_example, expected_txt)
    check_capsys_silent(capsys)


def test_e10_numbered_list_docx(capsys):
    """Test the numbered_list_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(numbered_list_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e10_numbered_list_odt(capsys):
    """Test the numbered_list_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(numbered_list_example, expected_txt)
    check_capsys_silent(capsys)
