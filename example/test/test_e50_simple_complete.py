#! /usr/local/bin/python3
"""Test the e50_simple_complete example."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest  # pylint: disable=unused-import
from example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_docx_func)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e50_simple_complete import multi_format_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# Main heading of example',
    'With start_paragraph we can start a paragraph.',
    'With add_text we can add text to',
    'the paragraph.',
    '## Sub heading of example',
    '***There is never a need to close an item type.***',
    '[the example file](',
    '- Item 1',
    '- Item 2',
    '  - Item 2.1',
    '1. Item 1',
    '  3.1. Item 3.1',
    '4. Item 4'
]


EXPECTED_DOCX_TEXT = [
    '<h1>',
    'Main heading of example',
    '</h1>',
    'With start_paragraph we can start a paragraph.',
    'With add_text we can add text to',
    'the paragraph.',
    '<h2>',
    'Sub heading of example',
    '</h2>',
    'There is never a need to close an item type.',
    'the example file</a>',
    '<ul>',
    'Item 1</li>',
    'Item 2</li>',
    'Item 2.1</li>',
    '</ul>'
]

EXPECTED_HTML_TEXT = [
    '<!DOCTYPE html>',
    '<html lang="en">',
    '<head>',
    '<meta charset="utf-8">',
    '<title>HTML file</title>',
    '</head>',
    '<body>'] + EXPECTED_DOCX_TEXT + [
    '<ol>',
    'Item 1</li>',
    '</ol>',
    '</body>',
    '</html>']


def test_mfe_md(capsys):
    """Test the multi_format_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # MD046: Deeply nested lists (4+ spaces) trigger false positive for
    # indented code blocks. Real code blocks in output use fenced style.
    expected_error = ['MD029', 'MD046']
    check_markdown_func(multi_format_example, expected_txt, expected_error)
    check_capsys_silent(capsys)


def test_mfe_html(capsys):
    """Test the multi_format_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(multi_format_example, expected_txt)
    check_capsys_silent(capsys)


def test_mfe_docx(capsys):
    """Test the multi_format_example function with the docx format."""
    expected_txt = EXPECTED_DOCX_TEXT
    expected_warnings = []
    check_docx_func(multi_format_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)
