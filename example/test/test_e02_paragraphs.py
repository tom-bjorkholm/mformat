#! /usr/local/bin/python3
"""Test the e02_paragraphs example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest  # pylint: disable=unused-import
from test_e01_paragraph import EXPECTED_HTML_PRE, EXPECTED_HTML_POST, EXPECTED_ODT_PRE
from example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_txt_func,
    check_docx_func, check_odt_func)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e02_paragraphs import paragraphs_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    'With new_paragraph we can start a paragraph. '
    'With add_text we can add text to\n'
    'the paragraph. As described in the example file e01_paragraph.py.\n\n'
    'With new_paragraph we can start a second paragraph. '
    'With add_text we can add\n'
    'text to the second paragraph just as we did with the first paragraph.'
    '\n\n'
    '(As this example does not have a heading the generated markdown file '
    'will not\n'
    'have a heading. If markdownlint is used on the generated markdown '
    'file it will\n'
    'report an error for the missing heading.)'
]
EXPECTED_HTML_BODY_TEXT = [
    '<p>',
    'With new_paragraph we can start a paragraph.',
    'With add_text we can add text to the paragraph.',
    'As described in the example file e01_paragraph.py.',
    '</p>',
    '<p>',
    'With new_paragraph we can start a second paragraph.',
    'With add_text we can add text to the second paragraph',
    'just as we did with the first paragraph.',
    '</p>', 
    '<p>',
    '(As this example does not have a heading the generated markdown',
    'file will not have a heading. If markdownlint is used on the',
    'generated markdown file it will report an error for the missing',
    'heading.)',
    '</p>',
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = EXPECTED_HTML_BODY_TEXT
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e02_paragraphs_md(capsys):
    """Test the paragraphs_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # MD041: First line in file should be a top level heading
    expected_error = ['MD041']
    check_markdown_func(paragraphs_example, expected_txt, expected_error)
    check_capsys_silent(capsys)


def test_e02_paragraphs_html(capsys):
    """Test the paragraphs_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(paragraphs_example, expected_txt)
    check_capsys_silent(capsys)


def test_e02_paragraphs_docx(capsys):
    """Test the paragraphs_example function with the docx format."""
    expected_txt = EXPECTED_HTML_BODY_TEXT
    expected_warnings = []
    check_docx_func(paragraphs_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e02_paragraphs_odt(capsys):
    """Test the paragraphs_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(paragraphs_example, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'With new_paragraph we can start a paragraph. With add_text we can '
        'add text to\n'
        'the paragraph. As described in the example file e01_paragraph.py.\n'
        '\n'
    ),
    (
        'With new_paragraph we can start a second paragraph. With add_text '
        'we can add\n'
        'text to the second paragraph just as we did with the first '
        'paragraph.\n'
        '\n'
    ),
    (
        '(As this example does not have a heading the generated markdown '
        'file will not\n'
        'have a heading. If markdownlint is used on the generated markdown '
        'file it will\n'
        'report an error for the missing heading.)\n'
    ),
]


def test_e02_paragraphs_txt(capsys):
    """Test the paragraphs_example function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(paragraphs_example, expected_txt)
    check_capsys_silent(capsys)
