#! /usr/local/bin/python3
"""Test the e15_table_at_once_bold example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest
from .test_e01_paragraph import (
    EXPECTED_HTML_PRE, EXPECTED_HTML_POST, EXPECTED_ODT_PRE)
from .example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_txt_func,
    check_rst_func,
    check_docx_func, check_odt_func, check_rtf_func, check_latex_func,
    docx_version_of_html, odt_version_of_html)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e15_table_at_once_bold import example_table_at_once_bold  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# Table in one call with bold first row example\n\n'
    'This is a table with bold text in first row.\n\n'
    '| **Name** | **Age** | **City**    |\n'
    '|----------|---------|-------------|\n'
    '| Janet    | 25      | New York    |\n'
    '| Jacob    | 30      | Los Angeles |\n'
    '| Jill     | 35      | Chicago     |\n\n'
    'Now a table with italics and bold in the first row.\n\n'
    '| ***Name*** | ***Age*** | ***City***  |\n'
    '|------------|-----------|-------------|\n'
    '| Janet      | 25        | New York    |\n'
    '| Jacob      | 30        | Los Angeles |\n'
    '| Jill       | 35        | Chicago     |\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Table in one call with bold first row example',
    '</h1>',
    '<p>',
    'This is a table with bold text in first row.',
    '</p>',
    '<table',
    '<tr>',
    '<td>', '<strong>', 'Name', '</strong>', '</td>',
    '<td>', '<strong>', 'Age', '</strong>', '</td>',
    '<td>', '<strong>', 'City', '</strong>', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Janet', '</td>',
    '<td>', '25', '</td>',
    '<td>', 'New York', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Jacob', '</td>',
    '<td>', '30', '</td>',
    '<td>', 'Los Angeles', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Jill', '</td>',
    '<td>', '35', '</td>',
    '<td>', 'Chicago', '</td>',
    '</tr>',
    '</table>',
    '<p>',
    'Now a table with italics and bold in the first row.',
    '</p>',
    '<table',
    '<tr>',
    '<td>', '<em>', '<strong>', 'Name', '</strong>', '</em>', '</td>',
    '<td>', '<em>', '<strong>', 'Age', '</strong>', '</em>', '</td>',
    '<td>', '<em>', '<strong>', 'City', '</strong>', '</em>', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Janet', '</td>',
    '<td>', '25', '</td>',
    '<td>', 'New York', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Jacob', '</td>',
    '<td>', '30', '</td>',
    '<td>', 'Los Angeles', '</td>',
    '</tr>',
    '<tr>',
    '<td>', 'Jill', '</td>',
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
EXPECTED_LATEX_TEXT = [
    '\\documentclass[a4paper]{report}',
    '\\chapter{Table in one call with bold first row example}',
    'This is a table with bold text in first row.',
    '\\textbf{Name} & \\textbf{Age} & \\textbf{City} \\\\',
    'Now a table with italics and bold in the first row.',
    ('\\textit{\\textbf{Name}} & \\textit{\\textbf{Age}} & '
     '\\textit{\\textbf{City}} \\\\'),
    '\\end{document}',
]


def test_e15_table_at_once_bold_md(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_table_at_once_bold function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(example_table_at_once_bold, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e15_table_at_once_bold_html(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_table_at_once_bold function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(example_table_at_once_bold, expected_txt)
    check_capsys_silent(capsys)


def test_e15_table_at_once_bold_docx(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_table_at_once_bold function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings: list[str] = []
    check_docx_func(
        example_table_at_once_bold,
        expected_txt,
        expected_warnings)
    check_capsys_silent(capsys)


def test_e15_table_at_once_bold_odt(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_table_at_once_bold function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(example_table_at_once_bold, expected_txt)
    check_capsys_silent(capsys)


def test_e15_table_at_once_bold_rtf(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_table_at_once_bold function with the rtf format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_rtf_func(example_table_at_once_bold, expected_txt)
    check_capsys_silent(capsys)


def test_e15_table_at_once_bold_latex(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_table_at_once_bold function with the latex format."""
    expected_txt = EXPECTED_LATEX_TEXT
    check_latex_func(example_table_at_once_bold, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'Table in one call with bold first row example\n'
        '*********************************************\n'
        '\n'
    ),
    (
        'This is a table with bold text in first row.\n'
        '\n'
    ),
    (
        '+-------+-----+-------------+\n'
        '|  Name | Age |     City    |\n'
        '+-------+-----+-------------+\n'
        '| Janet |  25 |   New York  |\n'
        '+-------+-----+-------------+\n'
        '| Jacob |  30 | Los Angeles |\n'
        '+-------+-----+-------------+\n'
        '|  Jill |  35 |   Chicago   |\n'
        '+-------+-----+-------------+\n'
        '\n'
    ),
    (
        'Now a table with italics and bold in the first row.\n'
        '\n'
    ),
    (
        '+-------+-----+-------------+\n'
        '|  Name | Age |     City    |\n'
        '+-------+-----+-------------+\n'
        '| Janet |  25 |   New York  |\n'
        '+-------+-----+-------------+\n'
        '| Jacob |  30 | Los Angeles |\n'
        '+-------+-----+-------------+\n'
        '|  Jill |  35 |   Chicago   |\n'
        '+-------+-----+-------------+\n'
    ),
]


def test_e15_table_at_once_bold_txt(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_table_at_once_bold function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(example_table_at_once_bold, expected_txt)
    check_capsys_silent(capsys)


def test_e15_table_at_once_bold_rst(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test example_table_at_once_bold with the reST format."""
    expected_txt = [
        'Table in one call with bold first row example',
        'This is a table with bold text in first row.',
        'Now a table with italics and bold in the first row.',
        '| Jill  | 35  | Chicago     |',
    ]
    expected_error: list[str] = []
    check_rst_func(example_table_at_once_bold, expected_txt, expected_error)
    check_capsys_silent(capsys)
