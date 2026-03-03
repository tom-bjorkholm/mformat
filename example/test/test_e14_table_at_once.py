#! /usr/local/bin/python3
"""Test the e14_table_at_once example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
from .test_e01_paragraph import (
    EXPECTED_HTML_PRE, EXPECTED_HTML_POST, EXPECTED_ODT_PRE)
from .example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_txt_func,
    check_rst_func,
    check_docx_func, check_odt_func, docx_version_of_html, odt_version_of_html)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e14_table_at_once import example_table_at_once  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# Table in one call example\n\n'
    '| Name | Age | City        |\n'
    '|------|-----|-------------|\n'
    '| John | 25  | New York    |\n'
    '| Jane | 30  | Los Angeles |\n'
    '| Jim  | 35  | Chicago     |\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Table in one call example',
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
    '</table>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_e14_table_at_once_md(capsys):
    """Test the example_table_at_once function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(example_table_at_once, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e14_table_at_once_html(capsys):
    """Test the example_table_at_once function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(example_table_at_once, expected_txt)
    check_capsys_silent(capsys)


def test_e14_table_at_once_docx(capsys):
    """Test the example_table_at_once function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(example_table_at_once, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e14_table_at_once_odt(capsys):
    """Test the example_table_at_once function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(example_table_at_once, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'Table in one call example\n'
        '*************************\n'
        '\n'
    ),
    (
        '+------+-----+-------------+\n'
        '| Name | Age |     City    |\n'
        '+------+-----+-------------+\n'
        '| John |  25 |   New York  |\n'
        '+------+-----+-------------+\n'
        '| Jane |  30 | Los Angeles |\n'
        '+------+-----+-------------+\n'
        '| Jim  |  35 |   Chicago   |\n'
        '+------+-----+-------------+\n'
    ),
]


def test_e14_table_at_once_txt(capsys):
    """Test the example_table_at_once function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(example_table_at_once, expected_txt)
    check_capsys_silent(capsys)


def test_e14_table_at_once_rst(capsys):
    """Test the example_table_at_once function with the reST format."""
    expected_txt = [
        'Table in one call example',
        '| Name | Age | City        |',
        '| Jim  | 35  | Chicago     |',
    ]
    expected_error: list[str] = []
    check_rst_func(example_table_at_once, expected_txt, expected_error)
    check_capsys_silent(capsys)
