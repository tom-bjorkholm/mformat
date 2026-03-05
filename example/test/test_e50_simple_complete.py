#! /usr/local/bin/python3
"""Test the e50_simple_complete example."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest
from .test_e01_paragraph import (
    EXPECTED_HTML_PRE, EXPECTED_HTML_POST, EXPECTED_ODT_PRE)
from .example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_txt_func, check_rst_func,
    check_docx_func, check_odt_func, docx_version_of_html)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e50_simple_complete import multi_format_example  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501

EXPECTED_MD_TEXT = [
    '# Main heading of example',
    'With new_paragraph we can start a paragraph.',
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
EXPECTED_TXT_TEXT = [
    (
        'Main heading of example\n'
        '***********************\n'
        '\n'
    ),
    (
        'With new_paragraph we can start a paragraph. With add_text we can '
        'add text to\n'
        'the paragraph.\n'
        '\n'
    ),
    (
        'Sub heading of example where add_text adds text to the sub heading\n'
        '==================================================================\n'
        '\n'
    ),
    (
        'Whenever we start a new item type the previous item type is '
        'automatically\n'
        'closed. Add text does not automatically close the previous item '
        'type, instead\n'
        'it just adds text to that item. There is never a need to close an '
        'item type.\n'
        '\n'
    ),
    (
        'Heading with URL to the example file\n'
        '====================================\n'
        '\n'
    ),
    (
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src/'
        'e50_simple_complete.py\n'
        '==================================================================='
        '======================\n'
        '\n'
    ),
    (
        'As you can see, we can add URLs to both headings and paragraphs. It '
        'is also\n'
        'possible to add URLs to text, for instance the URL to the example '
        'file is added\n'
        'here. The same example file\n'
        'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src/'
        'e50_simple_complete.py\n'
        '\n'
    ),
    (
        'URLs can (depending on the format) be formatted as clickable URLs '
        'or as text.\n'
        'To force URLs to be formatted as text, set url_as_text=True.\n'
        '\n'
    ),
    (
        'You may have noticed that we have not worried about about the '
        'whitespace\n'
        'between text. This is because we use a smart whitespace handling.If '
        'we disable\n'
        'smart whitespace handling,we need to handle whitespace manually, '
        'which can be\n'
        'cumbersome as shown here.\n'
        '\n'
    ),
    (
        'Bullet lists and numbered lists\n'
        '===============================\n'
        '\n'
    ),
    (
        '- Item 1\n'
        '- Item 2\n'
        '  - Item 2.1\n'
        '  - Item 2.2\n'
        '- Item 3\n'
        '1. Item 1\n'
        '2. Item 2 with some more text. Naturally more text can be added in '
        'the same\n'
        '   item using add_text.\n'
        '3. Item 3\n'
        '  3.1. Item 3.1\n'
        '    - Item 3.1.1\n'
        '    - Item 3.1.1\n'
        '4. Item 4\n'
        '\n'
    ),
    (
        'A simple table\n'
        '==============\n'
        '\n'
    ),
    (
        '+-----------+-------------------+--------------+\n'
        '| Full Name | Street and Number | City or Town |\n'
        '+-----------+-------------------+--------------+\n'
        '|  John Doe |    123 Main St    |   Anytown    |\n'
        '+-----------+-------------------+--------------+\n'
        '|  Jane Doe |    456 Main St    |   Anytown    |\n'
        '+-----------+-------------------+--------------+\n'
        '|  Jim Doe  |    789 Main St    | The Village  |\n'
        '+-----------+-------------------+--------------+\n'
        '\n'
    ),
    (
        'Another table\n'
        '-------------\n'
        '\n'
    ),
    (
        '+----------+-----+--------+\n'
        '|   Name   | Age | Gender |\n'
        '+----------+-----+--------+\n'
        '| John Doe |  30 |  Male  |\n'
        '+----------+-----+--------+\n'
        '| Jane Doe |  25 | Female |\n'
        '+----------+-----+--------+\n'
        '| Jim Doe  |  35 |  Male  |\n'
        '+----------+-----+--------+\n'
        '\n'
    ),
    (
        'Finally code blocks\n'
        '===================\n'
        '\n'
    ),
    (
        'Code blocks are written with write_code_block.\n'
        '\n'
    ),
    (
        '----- Start of python code block -----\n'
        'def my_function(x: int) -> int:\n'
        '    return x + 1\n'
        '\n'
    ),
    (
        'print(my_function(1))\n'
        '------ End of python code block ------\n'
    ),
]
EXPECTED_RST_TEXT = [
    (
        'Main heading of example\n'
        '=======================\n'
    ),
    (
        'Sub heading of example where add_text adds text to the sub heading\n'
        '------------------------------------------------------------------\n'
    ),
    (
        'Heading with URL to `the example file <https://bitbucket.org/'
        'tom-bjorkholm/mformat/src/master/example/src/'
        'e50_simple_complete.py>`_'
    ),
    '* Item 1',
    '* Item 2',
    '   * Item 2.1',
    '1. Item 1',
    '3. Item 3',
    '   1. Item 3.1',
    '      * Item 3.1.1',
    '4. Item 4',
    '| Full Name | Street and Number | City or Town |',
    '| Jim Doe   | 789 Main St       | The Village  |',
    '.. code:: python',
    'def my_function(x: int) -> int:',
    'print(my_function(1))'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'Main heading of example',
    '</h1>',
    'With new_paragraph we can start a paragraph.',
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
    '</ul>',
]
EXPECTED_DOCX_HTML_BODY_TEXT = [
    '<h1>',
    'Main heading of example',
    '</h1>',
    'With new_paragraph we can start a paragraph.',
    'With add_text we can add text to',
    'the paragraph.',
    '<h2>',
    'Sub heading of example',
    '</h2>',
    'There is never a need to close an item type.',
    'the example file</a>',
    '<ul>',
    'Item 1</li>',
    '<li>', 'Item 2',
    '<ul>', '<li>', 'Item 2.1</li>',
    '</ul>',
    '</ul>',
    '<ol>',
    '<li>', 'Item 1</li>',
    '</ol>',
]
EXPECTED_HTML_TEXT = (
    EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST)
EXPECTED_ODT_BODY_TEXT = [
    '<h1 class="P-">',
    'Main heading of example',
    '</h1>',
    'With new_paragraph we can start a paragraph.',
    'With add_text we can add text to',
    'the paragraph.',
    '<h2 class="P-">',
    'Sub heading of example',
    '</h2>',
    'There is never a need to close an item type.',
    'the example file</a>',
    '<ul',
    '<li>', '<p>', 'Item 1', '</p>', '</li>',
    '<li>', '<p>', 'Item 2',
    '<li>', '<p>', 'Item 2.1', '</p>', '</li>',
    '</ul>',
    '<ol',
    '<li>', '<p>', 'Item 1', '</p>', '</li>',
    '</ol>'
]
EXPECTED_ODT_TEXT = (
    EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST)


def test_e50_simple_complete_md(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the multi_format_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    # MD046: Deeply nested lists (4+ spaces) trigger false positive for
    # indented code blocks. Real code blocks in output use fenced style.
    expected_error = ['MD029', 'MD046']
    check_markdown_func(multi_format_example, expected_txt, expected_error)
    check_capsys_silent(capsys)


def test_e50_simple_complete_txt(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the multi_format_example function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(multi_format_example, expected_txt)
    check_capsys_silent(capsys)


def test_e50_simple_complete_rst(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the multi_format_example function with the reST format."""
    expected_txt = EXPECTED_RST_TEXT
    expected_error: list[str] = []
    check_rst_func(multi_format_example, expected_txt, expected_error)
    check_capsys_silent(capsys)


def test_e50_simple_complete_html(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the multi_format_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(multi_format_example, expected_txt)
    check_capsys_silent(capsys)


def test_e50_simple_complete_docx(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the multi_format_example function with the docx format."""
    expected_txt = docx_version_of_html(
        EXPECTED_DOCX_HTML_BODY_TEXT)
    expected_warnings: list[str] = []
    check_docx_func(multi_format_example, expected_txt,
                    expected_warnings)
    check_capsys_silent(capsys)


def test_e50_simple_complete_odt(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the multi_format_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(multi_format_example, expected_txt)
    check_capsys_silent(capsys)
