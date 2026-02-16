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
from e17_table_row_by_row_bold import example_table_row_by_row_bold  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '# Table row by row with bold & italic example\n\n'
    '| **City** | **Country** | **Size** |\n'
    '|----------|-------------|----------|\n'
    '| Mariehamn | Finland     | Small    |\n'
    '| *Copenhagen* | *Denmark*   | *Large*  |\n'
    '| ***Tokyo***  | ***Japan*** | ***Huge*** |\n\n'
    '| *Capital* | *Country* | *Continent* |\n'
    '|-----------|-----------|-------------|\n'
    '| Oslo      | Norway    | Europe      |\n'
    '| Tokyo     | Japan     | Asia        |\n'
    '| **Berlin** | **Germany** | **Europe**  |\n'
    '| Kairo      | Egypt       | Africa      |\n'
    '| ***Brussels*** | ***Belgium*** | ***Europe*** |\n\n'
    'Note: As the rows are added and written one by one'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Table row by row with bold &amp; italic example',
    '</h1>',
    '<table',
    '<tr>',
    '<td>', '<strong>', 'City', '</strong>', '</td>',
    '<td>', '<strong>', 'Country', '</strong>', '</td>',
    '<td>', '<strong>', 'Size', '</strong>', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Mariehamn', '</td>',
    '<td>', 'Finland', '</td>',
    '<td>', 'Small', '</td>',
    '</tr>',
    '<tr>',
    '<td>', '<em>', 'Copenhagen', '</em>', '</td>',
    '<td>', '<em>', 'Denmark', '</em>', '</td>',
    '<td>', '<em>', 'Large', '</em>', '</td>',
    '</tr>',
    '<tr>',
    '<td>', '<em>', '<strong>', 'Tokyo', '</strong>', '</em>', '</td>',
    '<td>', '<em>', '<strong>', 'Japan', '</strong>', '</em>', '</td>',
    '<td>', '<em>', '<strong>', 'Huge', '</strong>', '</em>', '</td>',
    '</tr>',
    '<tr>',
    '<td>', '<em>', 'Capital', '</em>', '</td>',
    '<td>', '<em>', 'Country', '</em>', '</td>',
    '<td>', '<em>', 'Continent', '</em>', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Oslo', '</td>',
    '<td>', 'Norway', '</td>',
    '<td>', 'Europe', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Tokyo', '</td>',
    '<td>', 'Japan', '</td>',
    '<td>', 'Asia', '</td>',
    '</tr>',
    '<tr>',
    '<td>', '<strong>', 'Berlin', '</strong>', '</td>',
    '<td>', '<strong>', 'Germany', '</strong>', '</td>',
    '<td>', '<strong>', 'Europe', '</strong>', '</td>',
    '</tr>',
    '<tr>',
    '<td>', '<em>', '<strong>', 'Brussels', '</strong>', '</em>', '</td>',
    '<td>', '<em>', '<strong>', 'Belgium', '</strong>', '</em>', '</td>',
    '<td>', '<em>', '<strong>', 'Europe', '</strong>', '</em>', '</td>',
    '</tr>',
    '</table>',
    '<p>',
    'Note: As the rows are added and written one by one,'
    ]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_e17_table_row_by_row_bold_md(capsys):
    """Test the example_table_row_by_row_bold function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(example_table_row_by_row_bold, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e17_table_row_by_row_bold_html(capsys):
    """Test the example_table_row_by_row_bold function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(example_table_row_by_row_bold, expected_txt)
    check_capsys_silent(capsys)


def test_e17_table_row_by_row_bold_docx(capsys):
    """Test the example_table_row_by_row_bold function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(example_table_row_by_row_bold, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e17_table_row_by_row_bold_odt(capsys):
    """Test the example_table_row_by_row_bold function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(example_table_row_by_row_bold, expected_txt)
    check_capsys_silent(capsys)
