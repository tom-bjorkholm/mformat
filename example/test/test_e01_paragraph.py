#! /usr/local/bin/python3
"""Test the e01_paragraph example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest  # pylint: disable=unused-import
from example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_docx_func, check_odt_func)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e01_paragraph import paragraph_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501


EXPECTED_MD_TEXT = [
    'With new_paragraph we can start a paragraph. ',
    'With add_text we can add text to\n'
    'the paragraph. We can also add text to the ',
    'paragraph in multiple calls using\n'
    'add_text. (As this example does not have a ',
    'heading the generated markdown file\n'
    'will not have a heading. If markdownlint is used ',
    'on the generated markdown file\n'
    'it will report an error for the missing heading.)'
]
EXPECTED_HTML_PRE = [
    '<!DOCTYPE html>',
    '<html lang="en">',
    '<head>',
    '<meta charset="utf-8">',
    '<title>HTML file</title>',
    '</head>',
    '<body>'
]
EXPECTED_HTML_POST = [
    '</body>',
    '</html>'
]
EXPECTED_HTML_BODY_TEXT = [
    '<p>',
    'With new_paragraph we can start a paragraph.',
    'With add_text we can add text to the paragraph.',
    'We can also add text to the paragraph in multiple',
    'calls using add_text. (As this example does not',
    'have a heading the generated markdown file will',
    'not have a heading. If markdownlint is used on',
    'the generated markdown file it will report an error',
    'for the missing heading.)',
    '</p>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_PRE = [
    '<!DOCTYPE html PUBLIC ',
    '<html xmlns="http://www.w3.org/1999/xhtml">',
    '<head>',
    '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>',
    '<title></title>',
    '</head>',
    '<body>'
]
EXPECTED_ODT_BODY_TEXT = EXPECTED_HTML_BODY_TEXT
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e01_paragraph_md(capsys):
    """Test the paragraph_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # MD041: First line in file should be a top level heading
    expected_error = ['MD041']
    check_markdown_func(paragraph_example, expected_txt, expected_error)
    check_capsys_silent(capsys)


def test_e01_paragraph_html(capsys):
    """Test the paragraph_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(paragraph_example, expected_txt)
    check_capsys_silent(capsys)


def test_e01_paragraph_docx(capsys):
    """Test the paragraph_example function with the docx format."""
    expected_txt = EXPECTED_HTML_BODY_TEXT
    expected_warnings = []
    check_docx_func(paragraph_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e01_paragraph_odt(capsys):
    """Test the paragraph_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(paragraph_example, expected_txt)
    check_capsys_silent(capsys)
