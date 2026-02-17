#! /usr/local/bin/python3
"""Test the e06_headings example."""

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
from e06_headings import headings_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '# This is the first heading, it is at level 1\n\n',
    '## This is the second heading, it is at level 2\n\n',
    '### This is the third heading, it is at level 3\n\n',
    'We can add text to headings with add_text(), just as we can add text to',
    'paragraphs. New headings can be added at any level. The argument',
    'smart_ws is',
    'used to control how whitespace is handled in headings just as',
    'in paragraphs.\n\n',
    'new_heading() also obeys the arguments bold and italic,',
    'just as in paragraphs.',
    'However, they make less sense for headings.',
    'Explicitly setting bold or italic on',
    'a heading may not produce the expected readability, as the heading has',
    'formatting from the heading definition that is specific',
    'to the output format.\n\n',
    '## The fourth heading is again at level 2\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'This is the first heading, it is at level 1',
    '</h1>',
    '<h2>',
    'This is the second heading, it is at level 2',
    '</h2>',
    '<h3>', 
    'This is the third heading, it is at level 3',
    '</h3>',
    '<p>',
    'We can add text to headings with add_text(), just as we can add text',
    'to paragraphs. New headings can be added at any level. The argument',
    'smart_ws is used to control how whitespace is handled in headings',
    'just as in paragraphs.',
    '</p>',
    '<p>',
    'new_heading() also obeys the arguments bold and italic, just as in',
    'paragraphs. However, they make less sense for headings. Explicitly',
    'setting bold or italic on a heading may not produce the expected',
    'readability, as the heading has formatting from the heading definition',
    'that is specific to the output format.',
    '</p>',
    '<h2>',
    'The fourth heading is again at level 2',
    '</h2>'
    ]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e06_headings_md(capsys):
    """Test the headings_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(headings_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e06_headings_html(capsys):
    """Test the headings_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(headings_example, expected_txt)
    check_capsys_silent(capsys)


def test_e06_headings_docx(capsys):
    """Test the headings_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(headings_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e06_headings_odt(capsys):
    """Test the headings_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(headings_example, expected_txt)
    check_capsys_silent(capsys)
