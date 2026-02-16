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
from e05_heading import heading_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '# This is a heading, at level 1\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'This is a heading, at level 1',
    '</h1>',
    ]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_e05_heading_md(capsys):
    """Test the heading_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(heading_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e05_heading_html(capsys):
    """Test the heading_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(heading_example, expected_txt)
    check_capsys_silent(capsys)


def test_e05_heading_docx(capsys):
    """Test the heading_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(heading_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e05_heading_odt(capsys):
    """Test the heading_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(heading_example, expected_txt)
    check_capsys_silent(capsys)
