#! /usr/local/bin/python3
"""Test the e22_url_in_bullet_list example."""

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
from e22_url_in_bullet_list import example_url_in_bullet_list  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# URL in bullet list example\n\n',
    '- This is a bullet list with a URL:\n',
    '  [This URL link to the examples.]'
    '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src)\n',
    '- Another bullet point with a bold URL:\n',
    ('  **[This bold URL link to the example source code.]'
     '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src)**'
     '\n'),
    '- A bullet point with an italic URL:\n',
    ('  *[This italic URL link to the examples result.]'
     '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/result)*'
     '\n'),
    '- Last point with an italic and bold URL:\n',
    ('  ***[This italic and bold URL link to the examples.]'
     '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src)***'
     '\n'),
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'URL in bullet list example',
    '</h1>',
    '<ul>',
    '<li>',
    'This is a bullet list with a URL:',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/src">',
    'This URL link to the examples.',
    '</a>',
    '</li>',
    '<li>',
    'Another bullet point with a bold URL:',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/src">',
    'This bold URL link to the example source code.',
    '</a>',
    '</li>',
    '<li>',
    'A bullet point with an italic URL:',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/result">',
    'This italic URL link to the examples result.',
    '</a>',
    '</li>',
    '<li>',
    'Last point with an italic and bold URL:',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/src">',
    'This italic and bold URL link to the examples.',
    '</a>',
    '</li>',
    '</ul>',
]
EXPECTED_DOCX_HTML_TEXT = EXPECTED_HTML_BODY_TEXT
EXPECTED_ODT_HTML_TEXT = EXPECTED_HTML_BODY_TEXT
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_ODT_HTML_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_e22_url_in_bullet_list_md(capsys):
    """Test the example_url_in_bullet_list function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(example_url_in_bullet_list, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e22_url_in_bullet_list_html(capsys):
    """Test the example_url_in_bullet_list function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(example_url_in_bullet_list, expected_txt)
    check_capsys_silent(capsys)


def test_e22_url_in_bullet_list_docx(capsys):
    """Test the example_url_in_bullet_list function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_TEXT)
    expected_warnings = []
    check_docx_func(
        example_url_in_bullet_list,
        expected_txt,
        expected_warnings)
    check_capsys_silent(capsys)


def test_e22_url_in_bullet_list_odt(capsys):
    """Test the example_url_in_bullet_list function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(example_url_in_bullet_list, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'URL in bullet list example\n'
        '**************************\n'
        '\n'
    ),
    (
        '- This is a bullet list with a URL: This URL link to the examples.\n'
        '  https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/'
        'src\n'
        '- Another bullet point with a bold URL: This bold URL link to the '
        'example\n'
        '  source code.\n'
        '  https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/'
        'src\n'
        '- A bullet point with an italic URL: This italic URL link to the '
        'examples\n'
        '  result. https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
        'example/result\n'
        '- Last point with an italic and bold URL: This italic and bold URL '
        'link to the\n'
        '  examples. https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
        'example/src\n'
    ),
]


def test_e22_url_in_bullet_list_txt(capsys):
    """Test the example_url_in_bullet_list function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(example_url_in_bullet_list, expected_txt)
    check_capsys_silent(capsys)


def test_e22_url_in_bullet_list_rst(capsys):
    """Test example_url_in_bullet_list with the reST format."""
    expected_txt = [
        'URL in bullet list example',
        '* This is a bullet list with a URL:',
        '**`This bold URL link to the example source code.',
        '***`This italic and bold URL link to the examples.',
    ]
    expected_error: list[str] = []
    check_rst_func(example_url_in_bullet_list, expected_txt, expected_error)
    check_capsys_silent(capsys)
