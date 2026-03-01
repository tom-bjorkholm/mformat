#! /usr/local/bin/python3
"""Test the e07_bullet_list example."""

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
from e07_bullet_list import bullet_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# Bullet list example\n\n'
    '- This is the first bullet point item.\n\n'
    '- This is the second bullet point item. '
    'We can add text to the bullet point\n'
    '  items with add_text(), just as we can add text to paragraphs.\n\n'
    '- This is the third bullet point item.\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Bullet list example',
    '</h1>',
    '<ul>',
    '<li>',
    'This is the first bullet point item.',
    '</li>',
    '<li>',
    ('This is the second bullet point item. We can add text to the bullet '
     'point'),
    'items with add_text(), just as we can add text to paragraphs.',
    '</li>',
    '<li>',
    'This is the third bullet point item.',
    '</li>',
    '</ul>']
EXPECTED_HTML_TEXT = EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_e07_bullet_list_md(capsys):
    """Test the bullet_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(bullet_example, expected_txt,
                        expected_error=[])
    check_capsys_silent(capsys)


def test_e07_bullet_list_html(capsys):
    """Test the bullet_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(bullet_example, expected_txt)
    check_capsys_silent(capsys)


def test_e07_bullet_list_docx(capsys):
    """Test the bullet_example function with the docx format."""
    expected_txt = docx_version_of_html(EXPECTED_HTML_BODY_TEXT)
    expected_warnings = []
    check_docx_func(bullet_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_e07_bullet_list_odt(capsys):
    """Test the bullet_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(bullet_example, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'Bullet list example\n'
        '*******************\n'
        '\n'
    ),
    (
        '- This is the first bullet point item.\n'
        '- This is the second bullet point item. We can add text to the '
        'bullet point\n'
        '  items with add_text(), just as we can add text to paragraphs.\n'
        '- This is the third bullet point item.\n'
    ),
]


def test_e07_bullet_list_txt(capsys):
    """Test the bullet_example function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(bullet_example, expected_txt)
    check_capsys_silent(capsys)


def test_e07_bullet_list_rst(capsys):
    """Test the bullet_example function with the reST format."""
    expected_txt = [
        'Bullet list example',
        '* This is the first bullet point item.',
        '* This is the third bullet point item.',
    ]
    expected_error: list[str] = []
    check_rst_func(bullet_example, expected_txt, expected_error)
    check_capsys_silent(capsys)
