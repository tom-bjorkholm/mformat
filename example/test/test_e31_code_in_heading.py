#! /usr/local/bin/python3
"""Test the e31_code_in_heading example."""

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
from e31_code_in_heading import code_in_heading_example  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# Code in heading example `add_code_in_text()`\n\n'
    '- Bullet items can also contain code: `example()`\n\n'
    '1. Numbered items can also contain code: `example()`\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Code in heading example', '<code>', 'add_code_in_text()',
    '</code>', '</h1>',
    '<ul>',
    '<li>', 'Bullet items can also contain code:', '<code>', 'example()',
    '</code>', '</li>', '</ul>',
    '<ol>',
    '<li>', 'Numbered items can also contain code:', '<code>', 'example()',
    '</code>', '</li>', '</ol>',
]
EXPECTED_DOCX_HTML_BODY_TEXT = [
    '<h1>',
    'Code in heading example', '<code>', 'add_code_in_text()',
    '</code>', '</h1>',
    '<ul>',
    '<li>', 'Bullet items can also contain code:', '<code>', 'example()',
    '</code>', '</li>', '</ul>',
    # '<ol>', '<li>',  Check if docx can make this real numbered list.
    'Numbered items can also contain code:', '<code>', 'example()',
    '</code>',
    # '</li>', '</ol>',
]

EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT +\
    EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + \
    EXPECTED_HTML_POST


def test_e31_code_in_heading_md(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the code_in_heading_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(code_in_heading_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e31_code_in_heading_html(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the code_in_heading_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(code_in_heading_example, expected_txt)
    check_capsys_silent(capsys)


def test_e31_code_in_heading_docx(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the code_in_heading_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_BODY_TEXT)
    expected_warnings: list[str] = []
    check_docx_func(code_in_heading_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e31_code_in_heading_odt(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the code_in_heading_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(code_in_heading_example, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'Code in heading example add_code_in_text()\n'
        '******************************************\n'
        '\n'
    ),
    (
        '- Bullet items can also contain code: example()\n'
        '1. Numbered items can also contain code: example()\n'
    ),
]


def test_e31_code_in_heading_txt(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the code_in_heading_example function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(code_in_heading_example, expected_txt)
    check_capsys_silent(capsys)


def test_e31_code_in_heading_rst(capsys: pytest.CaptureFixture[str]) -> None:
    """Test code_in_heading_example with the reST format."""
    expected_txt = [
        'Code in heading example ``add_code_in_text()``',
        '* Bullet items can also contain code: ``example()``',
        '1. Numbered items can also contain code: ``example()``',
    ]
    expected_error: list[str] = []
    check_rst_func(code_in_heading_example, expected_txt, expected_error)
    check_capsys_silent(capsys)
