#! /usr/local/bin/python3
"""Test the e10_numbered_list example."""

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
    check_docx_func, check_odt_func, docx_version_of_html, odt_version_of_html)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e10_numbered_list import numbered_list_example  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501


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
    '</li>', '<li>',
    'This is the second numbered item.',
    '</li>', '<li>',
    'This is the third numbered item.',
    '</li>',
    '</ol>'
]
EXPECTED_DOCX_HTML_BODY_TEXT = [
    '<h1>',
    'Numbered list example',
    '</h1>',
    '<ol>', '<li>',
    'This is the first numbered item.',
    'We can add text to the numbered items with add_text(),',
    'just as we can add text to paragraphs.',
    '</li>', '<li>',
    'This is the second numbered item.',
    '</li>', '<li>',
    'This is the third numbered item.',
    '</li>',
    '</ol>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_e10_numbered_list_md(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the numbered_list_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(numbered_list_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e10_numbered_list_html(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the numbered_list_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(numbered_list_example, expected_txt)
    check_capsys_silent(capsys)


def test_e10_numbered_list_docx(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the numbered_list_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_BODY_TEXT)
    expected_warnings: list[str] = []
    check_docx_func(numbered_list_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e10_numbered_list_odt(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the numbered_list_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(numbered_list_example, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'Numbered list example\n'
        '*********************\n'
        '\n'
    ),
    (
        '1. This is the first numbered item. We can add text to the numbered '
        'items with\n'
        '   add_text(), just as we can add text to paragraphs.\n'
        '2. This is the second numbered item.\n'
        '3. This is the third numbered item.\n'
    ),
]


def test_e10_numbered_list_txt(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the numbered_list_example function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(numbered_list_example, expected_txt)
    check_capsys_silent(capsys)


def test_e10_numbered_list_rst(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the numbered_list_example function with the reST format."""
    expected_txt = [
        'Numbered list example',
        '1. This is the first numbered item.',
        '3. This is the third numbered item.',
    ]
    expected_error: list[str] = []
    check_rst_func(numbered_list_example, expected_txt, expected_error)
    check_capsys_silent(capsys)
