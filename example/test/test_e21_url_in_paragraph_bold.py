#! /usr/local/bin/python3
"""Test the e21_url_in_paragraph_bold example."""

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
from e21_url_in_paragraph_bold import example_url_in_paragraph_bold  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501

_BB = 'https://bitbucket.org/tom-bjorkholm/mformat/src/master'
EXPECTED_MD_TEXT = [
    '# URL in paragraph with bold & italic example\n\n'
    'This is a paragraph with a URL:\n'
    '*[This italic URL link to the examples]'
    '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example)*\n'
    'and\n'
    '**[this bold URL link to the example source code.]'
    '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src)**'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'URL in paragraph with bold &amp; italic example', '</h1>',
    '<p>',
    'This is a paragraph with a URL: ',
    '<em>',
    f'<a href="{_BB}/example">',
    'This italic URL link to the examples',
    '</a>', '</em>',
    'and',
    '<strong>',
    f'<a href="{_BB}/example/src">',
    ('this bold URL link to the example source '
     'code.'),
    '</a>', '</strong>', '</p>',
]
EXPECTED_DOCX_HTML_TEXT = [
    '<h1>',
    'URL in paragraph with bold &amp; italic example',
    '</h1>',
    '<p>',
    'This is a paragraph with a URL: ',
    f'<a href="{_BB}/example">',
    '<em>',
    'This italic URL link to the examples',
    '</em>',
    '</a>',
    'and',
    f'<a href="{_BB}/example/src">',
    '<strong>',
    ('this bold URL link to the example source '
     'code.'),
    '</strong>',
    '</a>',
    '</p>',
]
EXPECTED_ODT_HTML_TEXT = [
    '<h1>',
    'URL in paragraph with bold &amp; italic example',
    '</h1>',
    '<p>',
    'This is a paragraph with a URL: ',
    f'<a href="{_BB}/example">',
    'This italic URL link to the examples',
    '</a>',
    'and',
    f'<a href="{_BB}/example/src">',
    ('this bold URL link to the example source '
     'code.'),
    '</a>',
    '</p>',
]
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_ODT_HTML_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_e21_url_in_paragraph_bold_md(capsys):
    """Test the example_url_in_paragraph_bold function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(example_url_in_paragraph_bold, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e21_url_in_paragraph_bold_html(capsys):
    """Test the example_url_in_paragraph_bold function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(example_url_in_paragraph_bold, expected_txt)
    check_capsys_silent(capsys)


def test_e21_url_in_paragraph_bold_docx(capsys):
    """Test the example_url_in_paragraph_bold function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_TEXT)
    expected_warnings = []
    check_docx_func(
        example_url_in_paragraph_bold,
        expected_txt,
        expected_warnings)
    check_capsys_silent(capsys)


def test_e21_url_in_paragraph_bold_odt(capsys):
    """Test the example_url_in_paragraph_bold function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(example_url_in_paragraph_bold, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'URL in paragraph with bold & italic example\n'
        '*******************************************\n'
        '\n'
    ),
    (
        'This is a paragraph with a URL: This italic URL link to the '
        'examples\n'
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example and '
        'this bold\n'
        'URL link to the example source code.\n'
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src\n'
    ),
]


def test_e21_url_in_paragraph_bold_txt(capsys):
    """Test the example_url_in_paragraph_bold function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(example_url_in_paragraph_bold, expected_txt)
    check_capsys_silent(capsys)


def test_e21_url_in_paragraph_bold_rst(capsys):
    """Test example_url_in_paragraph_bold with the reST format."""
    expected_txt = [
        'URL in paragraph with bold & italic example',
        '*`This italic URL link to the examples <https://bitbucket.org',
        '**`this bold URL link to the example source code.',
    ]
    expected_error: list[str] = []
    check_rst_func(example_url_in_paragraph_bold, expected_txt,
                   expected_error)
    check_capsys_silent(capsys)
