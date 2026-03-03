#! /usr/local/bin/python3
"""Test the e12_numbered_bold example."""

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
from e12_numbered_bold import numbered_bold_example  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# Numbered list with bold text example\n\n',
    '1. This is the first numbered point item. This is not bold or italic. '
    '**However,\n'
    '   this bold text is added to it.** *And this italic text is added '
    'to it.*\n\n',
    '2. **This is the bold numbered point item.** This non-bold text is '
    'added to it.\n\n',
    '3. *This is the italic numbered point item.* This non-italic text '
    'is added to\n'
    '   it.\n\n',
    '4. ***This is the bold and italic item.*** This non-bold and '
    'non-italic text is\n'
    '   added to it.\n\n',
    '  4.1. This is in item in a nested numbered point list. '
    '**Bold text added to\n'
    '       it.** *And italic text added to it.*\n\n',
    '  4.2. ***Second nested numbered point item.*** '
    'This non-bold and non-italic\n'
    '       text is added to it. **And bold** *and italic text added to '
    'it.*\n\n',
    '5. The final item is back at level 1. '
    'This is the final numbered point item.\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Numbered list with bold text example',
    '</h1>', '<ol>', '<li>',
    ('This is the first numbered point item. This is not bold or '
     'italic.'),
    '<strong>',
    'However, this bold text is added to it.',
    '</strong>', '<em>',
    'And this italic text is added to it.'
    '</em>', '</li>', '<li>', '<strong>',
    'This is the bold numbered point item.',
    '</strong>',
    'This non-bold text is added to it.',
    '</li>', '<li>', '<em>',
    'This is the italic numbered point item.',
    '</em>',
    'This non-italic text is added to it.',
    '</li>', '<li>', '<em>', '<strong>',
    'This is the bold and italic item.',
    '</strong>', '</em>',
    'This non-bold and non-italic text is added to it.',
    '</li>', '<ol>', '<li>',
    'This is in item in a nested numbered point list.',
    '<strong>',
    'Bold text added to it.',
    '</strong>', '<em>',
    'And italic text added to it.',
    '</em>', '</li>', '<li>', '<em>', '<strong>',
    'Second nested numbered point item.',
    '</strong>', '</em>',
    'This non-bold and non-italic text is added to it.',
    '<strong>',
    'And bold',
    '</strong>', '<em>',
    'and italic text added to it.',
    '</em>', '</li>', '</ol>', '<li>',
    ('The final item is back at level 1. This is the final numbered '
     'point item.'),
    '</li>', '</ol>'
]
EXPECTED_DOCX_HTML_BODY_TEXT = [
    '<h1>',
    'Numbered list with bold text example',
    '</h1>',
    '<ol>', '<li>',
    ('This is the first numbered point item. This is not bold or '
     'italic.'),
    '<strong>',
    'However, this bold text is added to it.',
    '</strong>', '<em>',
    'And this italic text is added to it.',
    '</em>', '</li>', '<li>',
    '<strong>',
    'This is the bold numbered point item.',
    '</strong>',
    'This non-bold text is added to it.',
    '</li>', '<li>',
    '<em>',
    'This is the italic numbered point item.',
    '</em>',
    'This non-italic text is added to it.',
    '</li>', '<li>',
    '<em>', '<strong>',
    'This is the bold and italic item.',
    '</strong>', '</em>',
    'This non-bold and non-italic text is added to it.',
    '<ol>', '<li>',
    'This is in item in a nested numbered point list.',
    '<strong>',
    'Bold text added to it.',
    '</strong>', '<em>',
    'And italic text added to it.',
    '</em>', '</li>', '<li>',
    '<strong>',
    '<em>',
    'Second nested numbered point item.',
    '</em>', '</strong>',
    'This non-bold and non-italic text is added to it.',
    '<strong>',
    'And bold',
    '</strong>', '<em>',
    'and italic text added to it.',
    '</em>', '</li>', '</ol>', '</li>', '<li>',
    ('The final item is back at level 1. This is the final numbered '
     'point item.'),
    '</li>', '</ol>'
]
EXPECTED_ODT_HTML_BODY_TEXT = [
    '<h1>',
    'Numbered list with bold text example',
    '</h1>', '<ol>', '<li>',
    ('This is the first numbered point item. This is not bold or '
     'italic.'),
    '<strong>',
    'However, this bold text is added to it.',
    '</strong>', '<em>',
    'And this italic text is added to it.',
    '</em>', '</li>', '<li>', '<strong>',
    'This is the bold numbered point item.',
    '</strong>',
    'This non-bold text is added to it.',
    '</li>', '<li>', '<em>',
    'This is the italic numbered point item.',
    '</em>',
    'This non-italic text is added to it.',
    '</li>', '<li>', '<em>', '<strong>',
    'This is the bold and italic item.',
    '</strong>', '</em>',
    'This non-bold and non-italic text is added to it.',
    #    '</li>',  ODT nested lists start in outer list item.
    '<ol>', '<li>',
    'This is in item in a nested numbered point list.',
    '<strong>',
    'Bold text added to it.',
    '</strong>', '<em>',
    'And italic text added to it.',
    '</em>', '</li>', '<li>', '<em>', '<strong>',
    'Second nested numbered point item.',
    '</strong>', '</em>',
    'This non-bold and non-italic text is added to it.',
    '<strong>',
    'And bold',
    '</strong>', '<em>',
    'and italic text added to it.',
    '</em>', '</li>', '</ol>', '<li>',
    ('The final item is back at level 1. This is the final numbered '
     'point item.'),
    '</li>', '</ol>'
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_ODT_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_e12_numbered_bold_md(capsys):
    """Test the numbered_bold_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # pymarkdown incorreclty think that numbering is wrong MD029.
    expected_error = ['MD029']
    check_markdown_func(numbered_bold_example, expected_txt,
                        expected_error=expected_error)
    check_capsys_silent(capsys)


def test_e12_numbered_bold_html(capsys):
    """Test the numbered_bold_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(numbered_bold_example, expected_txt)
    check_capsys_silent(capsys)


def test_e12_numbered_bold_docx(capsys):
    """Test the numbered_bold_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(numbered_bold_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e12_numbered_bold_odt(capsys):
    """Test the numbered_bold_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(numbered_bold_example, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'Numbered list with bold text example\n'
        '************************************\n'
        '\n'
    ),
    (
        '1. This is the first numbered point item. This is not bold or '
        'italic. However,\n'
        '   this bold text is added to it. And this italic text is added to '
        'it.\n'
        '2. This is the bold numbered point item. This non-bold text is '
        'added to it.\n'
        '3. This is the italic numbered point item. This non-italic text is '
        'added to it.\n'
        '4. This is the bold and italic item. This non-bold and non-italic '
        'text is added\n'
        '   to it.\n'
        '  4.1. This is in item in a nested numbered point list. Bold text '
        'added to it.\n'
        '       And italic text added to it.\n'
        '  4.2. Second nested numbered point item. This non-bold and '
        'non-italic text is\n'
        '       added to it. And bold and italic text added to it.\n'
        '5. The final item is back at level 1. This is the final numbered '
        'point item.\n'
    ),
]


def test_e12_numbered_bold_txt(capsys):
    """Test the numbered_bold_example function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(numbered_bold_example, expected_txt)
    check_capsys_silent(capsys)


def test_e12_numbered_bold_rst(capsys):
    """Test the numbered_bold_example function with the reST format."""
    expected_txt = [
        'Numbered list with bold text example',
        '**However, this bold text is added',
        '   2. ***Second nested numbered point item.***',
        '5. The final item is back at level 1.',
    ]
    expected_error: list[str] = []
    check_rst_func(numbered_bold_example, expected_txt, expected_error)
    check_capsys_silent(capsys)
