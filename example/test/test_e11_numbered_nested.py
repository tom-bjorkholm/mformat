#! /usr/local/bin/python3
"""Test the e11_numbered_nested example."""

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
from e11_numbered_nested import numbered_nested_example  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# Nested numbered list example\n\n'
    '1. This is the first numbered item. If we do not specify the level, '
    'it is at the\n'
    '   same level as the previous item - and when there is no '
    'previous item, it is\n'
    '   at level 1.\n\n'
    '2. This is the second numbered item.\n\n',
    ('  2.1. This is the third numbered item. This is the first item at '
     'level 2.\n\n'),
    '  2.2. Another item at level 2.\n\n'
    '    2.2.1. And an item at level 3.\n\n'
    '3. The final item is back at level 1.\n']
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Nested numbered list example',
    '</h1>', '<ol>', '<li>',
    'This is the first numbered item.',
    'If we do not specify the level, it is at the same level as the',
    'previous item - and when there is no previous item, it is at level 1.',
    '</li>', '<li>',
    'This is the second numbered item.',
    '</li>', '<ol>', '<li>',
    'This is the third numbered item. This is the first item at level 2.',
    '</li>', '<li>',
    'Another item at level 2.',
    '</li>', '<ol>', '<li>',
    'And an item at level 3.',
    '</li>', '</ol>', '</ol>', '<li>',
    'The final item is back at level 1.',
    '</li>', '</ol>'
]
EXPECTED_DOCX_HTML_BODY_TEXT = [
    '<h1>',
    'Nested numbered list example',
    '</h1>',
    '<ol>', '<li>',
    'This is the first numbered item.',
    'If we do not specify the level, it is at the same level as the',
    'previous item - and when there is no previous item, it is at level 1.',
    '</li>', '<li>',
    'This is the second numbered item.',
    '<ol>', '<li>',
    'This is the third numbered item. This is the first item at level 2.',
    '</li>', '<li>',
    'Another item at level 2.',
    '<ol>', '<li>',
    'And an item at level 3.',
    '</li>', '</ol>', '</ol>', '</li>', '<li>',
    'The final item is back at level 1.',
    '</li>', '</ol>'
]
EXPECTED_ODT_HTML_BODY_TEXT = [
    '<h1>',
    'Nested numbered list example',
    '</h1>', '<ol>', '<li>',
    'This is the first numbered item.',
    'If we do not specify the level, it is at the same level as the',
    'previous item - and when there is no previous item, it is at level 1.',
    '</li>', '<li>',
    'This is the second numbered item.',
    #    '</li>',  ODT nested lists start in outer list item.
    '<ol>', '<li>',
    'This is the third numbered item. This is the first item at level 2.',
    '</li>', '<li>',
    'Another item at level 2.',
    #    '</li>',  ODT nested lists start in outer list item.
    '<ol>', '<li>',
    'And an item at level 3.',
    '</li>', '</ol>', '</ol>', '<li>',
    'The final item is back at level 1.',
    '</li>', '</ol>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_ODT_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_e11_numbered_nested_list_md(capsys):
    """Test the numbered_nested_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # pymarkdown list incorreclty sees 4 space indented nested list items
    # as indented code blocks causing errors MD046 and MD029.
    expected_error = ['MD046', 'MD029']
    check_markdown_func(numbered_nested_example, expected_txt,
                        expected_error=expected_error)
    check_capsys_silent(capsys)


def test_e11_numbered_nested_list_html(capsys):
    """Test the numbered_nested_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(numbered_nested_example, expected_txt)
    check_capsys_silent(capsys)


def test_e11_numbered_nested_list_docx(capsys):
    """Test the numbered_nested_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(numbered_nested_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e11_numbered_nested_list_odt(capsys):
    """Test the numbered_nested_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(numbered_nested_example, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'Nested numbered list example\n'
        '****************************\n'
        '\n'
    ),
    (
        '1. This is the first numbered item. If we do not specify the level, '
        'it is at\n'
        '   the same level as the previous item - and when there is no '
        'previous item, it\n'
        '   is at level 1.\n'
        '2. This is the second numbered item.\n'
        '  2.1. This is the third numbered item. This is the first item at '
        'level 2.\n'
        '  2.2. Another item at level 2.\n'
        '    2.2.1. And an item at level 3.\n'
        '3. The final item is back at level 1.\n'
    ),
]


def test_e11_numbered_nested_list_txt(capsys):
    """Test the numbered_nested_example function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(numbered_nested_example, expected_txt)
    check_capsys_silent(capsys)


def test_e11_numbered_nested_rst(capsys):
    """Test the numbered_nested_example function with the reST format."""
    expected_txt = [
        'Nested numbered list example',
        '2. This is the second numbered item.\n'
        '\n'
        '   1. This is the third numbered item. This is the first item at '
        'level 2.',
        '      1. And an item at level 3.\n'
        '\n'
        '3. The final item is back at level 1.',
    ]
    expected_error: list[str] = []
    check_rst_func(numbered_nested_example, expected_txt, expected_error)
    check_capsys_silent(capsys)
