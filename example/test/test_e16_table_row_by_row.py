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
from e16_table_row_by_row import example_table_row_by_row  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '# Table row by row example\n\n'

    '| Name | Age | City |\n'
    '|------|-----|------|\n'
    '| John | 25  | New York |\n'
    '| Jane | 30  | Los Angeles |\n'
    '| Jim  | 35  | Chicago     |\n\n'
    'Note: As the rows are added and written one by one'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Table row by row example',
    '</h1>',
    '<table',
    '<tr>',
    '<td>', 'Name', '</td>',
    '<td>', 'Age', '</td>',
    '<td>', 'City', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'John', '</td>',
    '<td>', '25', '</td>',
    '<td>', 'New York', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Jane', '</td>',
    '<td>', '30', '</td>',
    '<td>', 'Los Angeles', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Jim', '</td>',
    '<td>', '35', '</td>',
    '<td>', 'Chicago', '</td>',
    '</tr>',
    '</table>',
    '<p>',
    'Note: As the rows are added and written one by one,'
    ]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e16_table_row_by_row_md(capsys):
    """Test the example_table_row_by_row function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(example_table_row_by_row, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e16_table_row_by_row_html(capsys):
    """Test the example_table_row_by_row function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(example_table_row_by_row, expected_txt)
    check_capsys_silent(capsys)


def test_e16_table_row_by_row_docx(capsys):
    """Test the example_table_row_by_row function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(example_table_row_by_row, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e16_table_row_by_row_odt(capsys):
    """Test the example_table_row_by_row function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(example_table_row_by_row, expected_txt)
    check_capsys_silent(capsys)
