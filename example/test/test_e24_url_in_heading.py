#! /usr/local/bin/python3
"""Test the e23_url_in_numbered_list example."""

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
    check_docx_func, check_odt_func, check_rtf_func, check_latex_func,
    docx_version_of_html, odt_version_of_html)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e24_url_in_heading import example_url_in_heading  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# URL in heading example\n\n',
    '# A heading with a URL: '
    '[This URL link to the examples.]'
    '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example)\n\n',
    '## A heading with a bold URL: ',
    ('**[This bold URL link to the example source code.]'
     '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src)**'
     '\n\n'),
    '## A heading with an italic URL: ',
    ('*[This italic URL link to the examples result.]'
     '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/result)*'
     '\n\n'),
    '## And with an italic and bold URL: ',
    ('***[This italic and bold URL link to the examples.]'
     '(https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src)***'
     '\n\n'),
    ('The add_url function can be used to add a URL to a heading, as well '
     'as to'),
    'paragraphs, bullet lists, and numbered point lists.\n']
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'URL in heading example',
    '</h1>',
    '<h1>',
    'A heading with a URL:',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example">',
    'This URL link to the examples.',
    '</a>',
    '</h1>',
    '<h2>',
    'A heading with a bold URL:',
    '<strong>',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/src">',
    'This bold URL link to the example source code.',
    '</a>',
    '</strong>',
    '</h2>',
    '<h2>',
    'A heading with an italic URL:',
    '<em>',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/result">',
    'This italic URL link to the examples result.',
    '</a>', '</em>', '</h2>',
    '<h2>',
    'And with an italic and bold URL:',
    '<em>', '<strong>',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/src">',
    'This italic and bold URL link to the examples.',
    '</a>', '</strong>', '</em>', '</h2>', '<p>',
    'The add_url function can be used to add a URL to a heading,',
    'as well as to',
    'paragraphs, bullet lists, and numbered point lists.',
    '</p>'
]
EXPECTED_DOCX_HTML_TEXT = [
    '<h1>',
    'URL in heading example',
    '</h1>',
    '<h1>',
    'A heading with a URL:',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example">',
    'This URL link to the examples.',
    '</a>',
    '</h1>',
    '<h2>',
    'A heading with a bold URL:',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/src">',
    'This bold URL link to the example source code.',
    '</a>',
    '</h2>',
    '<h2>',
    'A heading with an italic URL:',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/result">',
    'This italic URL link to the examples result.',
    '</a>',
    '</h2>',
    '<h2>',
    'And with an italic and bold URL:',
    '<a href="https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
    'example/src">',
    'This italic and bold URL link to the examples.',
    '</a>',
    '</h2>', '<p>',
    'The add_url function can be used to add a URL to a heading,',
    'as well as to paragraphs, bullet lists, and numbered point lists.',
    '</p>'
]
EXPECTED_ODT_HTML_TEXT = EXPECTED_DOCX_HTML_TEXT
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_ODT_HTML_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_LATEX_TEXT = [
    '\\documentclass[a4paper]{report}',
    '\\chapter{URL in heading example}',
    ('\\chapter{A heading with a URL: \\penalty0\\href{https://'
     'bitbucket.org/tom-bjorkholm/mformat/src/master/example}{This URL '
     'link to the examples.}\\penalty0}'),
    ('\\section{A heading with a bold URL: \\textbf{\\penalty0\\href'
     '{https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
     'example/src}{This bold URL link to the example source '
     'code.}\\penalty0}}'),
    ('\\section{A heading with an italic URL: \\textit{\\penalty0\\href'
     '{https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
     'example/result}{This italic URL link to the examples '
     'result.}\\penalty0}}'),
    ('And with an italic and bold URL: \\textit{\\textbf{\\penalty0\\href'
     '{https://bitbucket.org/tom-bjorkholm/mformat/src/master/'
     'example/src}{This italic and bold URL link to the '
     'examples.}\\penalty0}}}'),
    ('The add\\_url function can be used to add a URL to a heading, '
     'as well as'),
    '\\end{document}',
]


def test_e24_url_in_headings_md(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_url_in_heading function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # MD025: Multiple top level headings in the same document
    expected_error = ['MD025']
    check_markdown_func(example_url_in_heading, expected_txt,
                        expected_error=expected_error)
    check_capsys_silent(capsys)


def test_e24_url_in_headings_html(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_url_in_heading function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(example_url_in_heading, expected_txt)
    check_capsys_silent(capsys)


def test_e24_url_in_headings_docx(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_url_in_heading function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_DOCX_HTML_TEXT)
    expected_warnings: list[str] = []
    check_docx_func(example_url_in_heading, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e24_url_in_headings_odt(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_url_in_heading function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(example_url_in_heading, expected_txt)
    check_capsys_silent(capsys)


def test_e24_url_in_headings_rtf(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_url_in_heading function with the rtf format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_rtf_func(example_url_in_heading, expected_txt)
    check_capsys_silent(capsys)


def test_e24_url_in_headings_latex(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_url_in_heading function with the latex format."""
    expected_txt = EXPECTED_LATEX_TEXT
    check_latex_func(example_url_in_heading, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'URL in heading example\n'
        '**********************\n'
        '\n'
    ),
    (
        'A heading with a URL: This URL link to the examples.\n'
        '****************************************************\n'
        '\n'
    ),
    (
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example\n'
        '**************************************************************\n'
        '\n'
    ),
    (
        'A heading with a bold URL: This bold URL link to the example source '
        'code.\n'
        '===================================================================='
        '=====\n'
        '\n'
    ),
    (
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src\n'
        '==================================================================\n'
        '\n'
    ),
    (
        'A heading with an italic URL: This italic URL link to the examples '
        'result.\n'
        '===================================================================='
        '======\n'
        '\n'
    ),
    (
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/'
        'result\n'
        '===================================================================='
        '=\n'
        '\n'
    ),
    (
        'And with an italic and bold URL: This italic and bold URL link to '
        'the examples.\n'
        '===================================================================='
        '===========\n'
        '\n'
    ),
    (
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src\n'
        '==================================================================\n'
        '\n'
    ),
    (
        'The add_url function can be used to add a URL to a heading, as well '
        'as to\n'
        'paragraphs, bullet lists, and numbered point lists.\n'
    ),
]


def test_e24_url_in_headings_txt(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the example_url_in_heading function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(example_url_in_heading, expected_txt)
    check_capsys_silent(capsys)


def test_e24_url_in_heading_rst(capsys: pytest.CaptureFixture[str]) -> None:
    """Test example_url_in_heading with the reST format."""
    expected_txt = [
        'URL in heading example',
        'A heading with a URL: `This URL link to the examples.',
        'A heading with a bold URL: **`This bold URL link',
        'The add_url function can be used to add a URL to a heading',
    ]
    expected_error: list[str] = []
    check_rst_func(example_url_in_heading, expected_txt, expected_error)
    check_capsys_silent(capsys)
