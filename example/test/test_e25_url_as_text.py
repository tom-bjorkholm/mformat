#! /usr/local/bin/python3
"""Test the e20_url_in_paragraph example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest  # pylint: disable=unused-import
from test_e01_paragraph import EXPECTED_HTML_PRE, EXPECTED_HTML_POST, EXPECTED_ODT_PRE
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
from e25_url_as_text import example_url_as_text  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# URL in paragraph example\n\n'
    'This is a paragraph with a URL: '
    'The examples are here.',
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example\n\n',
    'The URL was added as a link using add_url(text, url)\n\n',
    'By not specifying the text, the URL is shows as text:\n'
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example\n\n',
    'A paragraph can of course have multiple URLs. '
    'The source code of the examples',
    'are here. '
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src '
    'and\n'
    'The produced output files are here.',
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/result'
    '\n\n',
    'The URLs are shown as text instead of clickable links.',
    'This might be useful when',
    'you want to copy the URLs to the clipboard and paste them into another',
    'application. This is done by passing the url_as_text argument to the create_mf',
    'factory function.'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'URL in paragraph example',
    '</h1>',
    '<p>',
    'This is a paragraph with a URL: The examples are here.',
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example',
    '</p>',
    '<p>',
    'The URL was added as a link using add_url(text, url)',
    '</p>',
    '<p>',
    'By not specifying the text, the URL is shows as text:',
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example',
    '</p>',
    '<p>',
    'A paragraph can of course have multiple URLs.',
    'The source code of the examples are here.',
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src',
    'and The produced output files are here.',
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/result',
    '</p>',
    '<p>',
    'The URLs are shown as text instead of clickable links.',
    'This might be useful when you want to copy the URLs to the clipboard',
    'and paste them into another application.',
    'This is done by passing the url_as_text argument to the create_mf',
    'factory function.',
    '</p>'
]
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST


def test_e25_url_as_text_md(capsys):
    """Test the example_url_as_text function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    expected_error = ['MD034']  # Bare URL used
    check_markdown_func(example_url_as_text, expected_txt,
                        expected_error=expected_error)
    check_capsys_silent(capsys)


def test_e25_url_as_text_html(capsys):
    """Test the example_url_as_text function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(example_url_as_text, expected_txt)
    check_capsys_silent(capsys)


def test_e25_url_as_text_docx(capsys):
    """Test the example_url_as_text function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(example_url_as_text, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e25_url_as_text_odt(capsys):
    """Test the example_url_as_text function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(example_url_as_text, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'URL in paragraph example\n'
        '************************\n'
        '\n'
    ),
    (
        'This is a paragraph with a URL: The examples are here.\n'
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example\n'
        '\n'
    ),
    (
        'The URL was added as a link using add_url(text, url)\n'
        '\n'
    ),
    (
        'By not specifying the text, the URL is shows as text:\n'
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example\n'
        '\n'
    ),
    (
        'A paragraph can of course have multiple URLs. The source code of '
        'the examples\n'
        'are here. https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
        'example/src\n'
        'and The produced output files are here.\n'
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/'
        'result\n'
        '\n'
    ),
    (
        'The URLs are shown as text instead of clickable links. This might '
        'be useful\n'
        'when you want to copy the URLs to the clipboard and paste them into '
        'another\n'
        'application. This is done by passing the url_as_text argument to '
        'the create_mf\n'
        'factory function.\n'
    ),
]


def test_e25_url_as_text_txt(capsys):
    """Test the example_url_as_text function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(example_url_as_text, expected_txt)
    check_capsys_silent(capsys)


def test_e25_url_as_text_rst(capsys):
    """Test example_url_as_text with the reST format."""
    expected_txt = [
        'URL in paragraph example',
        'This is a paragraph with a URL: The examples are here.',
        'The URLs are shown as text instead of clickable links.',
        'factory function.',
    ]
    expected_error: list[str] = []
    check_rst_func(example_url_as_text, expected_txt, expected_error)
    check_capsys_silent(capsys)
