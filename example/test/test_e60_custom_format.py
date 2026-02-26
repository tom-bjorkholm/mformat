#! /usr/local/bin/python3
"""Test the e60_custom_format example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest  # pylint: disable=unused-import
from test_e01_paragraph import EXPECTED_HTML_PRE, \
    EXPECTED_HTML_POST, EXPECTED_ODT_PRE
from example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_txt_func,
    check_docx_func, check_odt_func, odt_version_of_html,
    check_text_in_order)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e60_custom_format import custom_format_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '# Custom Format Example\n\n'
     'This example demonstrates how to create and use a custom '
     'format in the mformat',
     'framework. The same code can be used to write to different '
     'formats, just by',
     'changing the format name.\n\n'
     '## Features\n\n'
     '- Easy to extend the framework\n\n'
     '- Supports most standard document elements\n\n'
     '- Format-agnostic API\n\n'
     '1. First step: Create a format class\n\n'
     '2. Second step: Implement required methods\n\n'
     '3. Third step: Register the format\n\n'
]
EXPECTED_HTML_BODY_TEXT = [
   '<h1>',
   'Custom Format Example',
   '</h1>',
   '<p>',
   'This example demonstrates how to create and use a',
   'custom format in the mformat framework.',
   'The same code can be used to write to different formats,',
   'just by changing the format name.',
   '</p>',
   '<h2>',
   'Features',
   '</h2>',
   '<ul>',
   '<li>',
   'Easy to extend the framework',
   '</li>',
   '<li>',
   'Supports most standard document elements',
   '</li>',
   '<li>',
   'Format-agnostic API'
]

EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_60_custom_format_md(capsys):
    """Test the custom_format_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(custom_format_example, expected_txt, expected_error=[])
    check_capsys_silent(capsys)


def test_60_custom_format_html(capsys):
    """Test the custom_format_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(custom_format_example, expected_txt)
    check_capsys_silent(capsys)


def test_60_custom_format_docx(capsys):
    """Test the custom_format_example function with the docx format."""
    expected_txt = EXPECTED_HTML_BODY_TEXT
    expected_warnings = []
    check_docx_func(custom_format_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_60_custom_format_odt(capsys):
    """Test the custom_format_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(custom_format_example, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TREE_TEXT = [
    '> Custom Format Example',
    'This example demonstrates how to create and use a custom',
    'format in the mformat framework.',
    'The same code can be used to write to different formats,',
    'just by changing the format name.',
    '  >> Features'
]


def test_60_custom_format_tree(capsys):
    """Test the custom_format_example function with the tree format."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / 'custom_format.tree')
        custom_format_example('tree', file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            check_text_in_order(text, EXPECTED_TREE_TEXT)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'Custom Format Example\n'
        '*********************\n'
        '\n'
    ),
    (
        'This example demonstrates how to create and use a custom format in '
        'the mformat\n'
        'framework. The same code can be used to write to different formats, '
        'just by\n'
        'changing the format name.\n'
        '\n'
    ),
    (
        'Features\n'
        '========\n'
        '\n'
    ),
    (
        '- Easy to extend the framework\n'
        '- Supports most standard document elements\n'
        '- Format-agnostic API\n'
        '1. First step: Create a format class\n'
        '2. Second step: Implement required methods\n'
        '3. Third step: Register the format\n'
        '\n'
    ),
    (
        '+-----------+-------------------+\n'
        '|  Element  |       Method      |\n'
        '+-----------+-------------------+\n'
        '| Paragraph |  new_paragraph()  |\n'
        '+-----------+-------------------+\n'
        '|  Heading  |   new_heading()   |\n'
        '+-----------+-------------------+\n'
        '|    List   | new_bullet_item() |\n'
        '+-----------+-------------------+\n'
        '\n'
    ),
    (
        '----- Start of python code block -----\n'
        'def example():\n'
        '    print("Hello, World!")\n'
        '------ End of python code block ------\n'
        '\n'
    ),
    (
        'This text is bold and this is italic.\n'
        '\n'
    ),
    (
        'Visit our website https://example.com\n'
    ),
]


def test_60_custom_format_txt(capsys):
    """Test the custom_format_example function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(custom_format_example, expected_txt)
    check_capsys_silent(capsys)
