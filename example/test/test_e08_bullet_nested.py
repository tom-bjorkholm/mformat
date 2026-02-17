#! /usr/local/bin/python3
"""Test the e08_bullet_nested example."""

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
from e08_bullet_nested import bullets_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '# Nested bullet list example\n\n'
    '- This is the first bullet point item at level 1.\n\n'
    '  - This is the second bullet point item. This time at level 2.\n\n'
    '  - Another point item without specifying level. This means '
    'that it is at the\n'
    '    same level as the previous item.\n\n',
    '    - This is a bullet point item at level 3.\n\n'
    '- This is final bullet point item. This time at level 1\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Nested bullet list example',
    '</h1>',
    '<ul>',
    '<li>',
    'This is the first bullet point item at level 1.',
    '</li>',
    '<ul>',
    '<li>',
    'This is the second bullet point item. This time at level 2.',
    '</li>',
    '<li>',
    'Another point item without specifying level.',
    'This means that it is at the same level as the previous item.',
    '</li>',
    '<ul>',
    '<li>',
    'This is a bullet point item at level 3.',
    '</li>',
    '</ul>',
    '</ul>',
    '<li>',
    'This is final bullet point item. This time at level 1',
    '</li>',
    '</ul>'
]
EXPECTED_DOCX_HTML_BODY_TEXT = [
    '<h1>',
    'Nested bullet list example',
    '</h1>',
    '<ul>',
    '<li>',
    'This is the first bullet point item at level 1.',
    '</li>',
#    '<ul>',  # Check is docx can make this real nested list.
    '<li>',
    'This is the second bullet point item. This time at level 2.',
    '</li>',
    '<li>',
    'Another point item without specifying level.',
    'This means that it is at the same level as the previous item.',
    '</li>',
#    '<ul>',
    '<li>',
    'This is a bullet point item at level 3.',
    '</li>',
#    '</ul>',
#    '</ul>',
    '<li>',
    'This is final bullet point item. This time at level 1',
    '</li>',
    '</ul>'
]
EXPECTED_HTML_ODT_BODY_TEXT = [
    '<h1>',
    'Nested bullet list example',
    '</h1>',
    '<ul>',
    '<li>',
    'This is the first bullet point item at level 1.',
#    '</li>',  # ODT nested lists are in list item.
    '<ul>',
    '<li>',
    'This is the second bullet point item. This time at level 2.',
    '</li>',
    '<li>',
    'Another point item without specifying level.',
    'This means that it is at the same level as the previous item.',
#    '</li>',  # ODT nested lists are in list item.
    '<ul>',
    '<li>',
    'This is a bullet point item at level 3.',
    '</li>',
    '</ul>',
    '</ul>',
    '<li>',
    'This is final bullet point item. This time at level 1',
    '</li>',
    '</ul>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_ODT_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e08_bullet_nested_md(capsys):
    """Test the bullets_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(bullets_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e08_bullet_nested_html(capsys):
    """Test the bullets_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(bullets_example, expected_txt)
    check_capsys_silent(capsys)


def test_e08_bullet_nested_docx(capsys):
    """Test the bullets_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(bullets_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e08_bullet_nested_odt(capsys):
    """Test the bullets_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(bullets_example, expected_txt)
    check_capsys_silent(capsys)
