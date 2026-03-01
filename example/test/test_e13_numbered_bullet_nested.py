#! /usr/local/bin/python3
"""Test the e13_numbered_bullet_nested example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
from test_e01_paragraph import (
    EXPECTED_HTML_PRE, EXPECTED_HTML_POST, EXPECTED_ODT_PRE)
from example_checkers import (
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
from e13_numbered_bullet_nested import example_nest_numbers_bullets  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# Nesting points example\n\n'
    '1. First item\n\n',
    '2. Second item **with some bold text**\n\n'
    '  - First bullet\n\n',
    '  - *Second bullet is italic* **with some bold** and some non-bold and\n'
    '    non-italic text\n\n'
    '    2.2.1. First item in third level\n\n'
    '    2.2.2. Second item in third level\n\n'
    '3. Third item on first level. By specifying a lower level we end '
    'some nested\n'
    '   lists.\n',
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Nesting points example',
    '</h1>', '<ol>', '<li>',
    'First item',
    '</li>', '<li>',
    'Second item',
    '<strong>',
    'with some bold text',
    '</strong>', '</li>', '<ul>', '<li>',
    'First bullet',
    '</li>', '<li>', '<em>',
    'Second bullet is italic',
    '</em>', '<strong>',
    'with some bold',
    '</strong>', 'and some non-bold and non-italic text',
    '</li>', '<ol>', '<li>',
    'First item in third level',
    '</li>', '<li>',
    'Second item in third level',
    '</li>', '</ol>', '<li>',
    'Third item on first level. By specifying a lower level we end some',
    'nested lists.',
    '</li>', '</ol>'
]
EXPECTED_DOCX_HTML_BODY_TEXT = [
    '<h1>',
    'Nesting points example',
    '</h1>',
    '<ol>', '<li>',
    'First item',
    '</li>', '<li>',
    'Second item',
    '<strong>',
    'with some bold text',
    '</strong>',
    '<ul>', '<li>',
    'First bullet',
    '</li>', '<li>',
    '<em>',
    'Second bullet is italic',
    '</em>', '<strong>',
    'with some bold',
    '</strong>', 'and some non-bold and non-italic text',
    '<ol>', '<li>',
    'First item in third level',
    '</li>', '<li>',
    'Second item in third level',
    '</li>', '</ol>', '</li>', '</ul>', '</li>', '<li>',
    'Third item on first level.',
    'By specifying a lower level we end some nested lists.',
    '</li>', '</ol>',
]
EXPECTED_ODT_HTML_BODY_TEXT = [
    '<h1>',
    'Nesting points example',
    '</h1>', '<ol>', '<li>',
    'First item',
    '</li>', '<li>',
    'Second item',
    '<strong>',
    'with some bold text',
    '</strong>',
    #    '</li>',  ODT nested lists start in outer list item.
    '<ul>', '<li>',
    'First bullet',
    '</li>', '<li>', '<em>',
    'Second bullet is italic',
    '</em>', '<strong>',
    'with some bold',
    '</strong>', 'and some non-bold and non-italic text',
    #    '</li>',  ODT nested lists start in outer list item.
    '<ol>', '<li>',
    'First item in third level',
    '</li>', '<li>',
    'Second item in third level',
    '</li>', '</ol>', '<li>',
    ('Third item on first level. By specifying a lower level we end '
     'some nested lists.'),
    '</li>', '</ol>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_ODT_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_e13_numbered_bullet_nested_md(capsys):
    """Test the example_nest_numbers_bullets function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # pymarkdown incorreclty think that unordered list is intended as
    # top level not nested inside ordered list causing error MD007
    # and that numbering is wrong MD029.
    expected_error = ['MD007', 'MD029']
    check_markdown_func(example_nest_numbers_bullets, expected_txt,
                        expected_error=expected_error)
    check_capsys_silent(capsys)


def test_e13_numbered_bullet_nested_html(capsys):
    """Test the example_nest_numbers_bullets function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(example_nest_numbers_bullets, expected_txt)
    check_capsys_silent(capsys)


def test_e13_numbered_bullet_nested_docx(capsys):
    """Test the example_nest_numbers_bullets function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(
        example_nest_numbers_bullets,
        expected_txt,
        expected_warnings)
    check_capsys_silent(capsys)


def test_e13_numbered_bullet_nested_odt(capsys):
    """Test the example_nest_numbers_bullets function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(example_nest_numbers_bullets, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'Nesting points example\n'
        '**********************\n'
        '\n'
    ),
    (
        '1. First item\n'
        '2. Second item with some bold text\n'
        '  - First bullet\n'
        '  - Second bullet is italic with some bold and some non-bold and '
        'non-italic\n'
        '    text\n'
        '    2.2.1. First item in third level\n'
        '    2.2.2. Second item in third level\n'
        '3. Third item on first level. By specifying a lower level we end '
        'some nested\n'
        '   lists.\n'
    ),
]


def test_e13_numbered_bullet_nested_txt(capsys):
    """Test the example_nest_numbers_bullets function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(example_nest_numbers_bullets, expected_txt)
    check_capsys_silent(capsys)


def test_e13_numbered_bullet_nested_rst(capsys):
    """Test example_nest_numbers_bullets with the reST format."""
    expected_txt = [
        'Nesting points example',
        '2. Second item **with some bold text**',
        '   * *Second bullet is italic* **with some bold**',
        '3. Third item on first level.',
    ]
    expected_error: list[str] = []
    check_rst_func(example_nest_numbers_bullets, expected_txt,
                   expected_error)
    check_capsys_silent(capsys)
