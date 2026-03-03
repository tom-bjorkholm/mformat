#! /usr/local/bin/python3
"""Test the e42_filter_args_for_format example."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest
from .test_e01_paragraph import EXPECTED_HTML_POST, EXPECTED_ODT_PRE
from .example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_txt_func,
    check_rst_func,
    check_docx_func, check_odt_func, odt_version_of_html)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e42_filter_args_for_format import filter_args_for_format_example  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501


EXPECTED_MD_TEXT = [
    '# CSS in HTML gefiltert für andere Formate\n\n'
    'Dieses Beispiel zeigt, wie Sie eine CSS-Datei für HTML gefiltert ',
    'haben, so dass\nsie nicht für andere Formate verfügbar ist.\n\n'
    'Die CSS-Datei liegt unter example/css/ und wird per relativem ',
    'Pfad eingebunden\n'
    '(für lokale Anzeige). Die Ausgabe ist auf Deutsch; in HTML ',
    'wird lang="de" im\n'
    'erzeugten \\<html>-Tag gesetzt. ',
    'Für ODT wird sprache auch als "de" gesetzt. Für\n'
    'andere Formate wird die Sprache ignoriert.\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'CSS in HTML gefiltert für andere Formate',
    '</h1>',
    '<p>',
    'Dieses Beispiel zeigt, wie Sie eine CSS-Datei für HTML gefiltert',
    'haben, so dass',
    'sie nicht für andere Formate verfügbar ist.',
    '</p>',
    '<p>',
    'Die CSS-Datei liegt unter example/css/ und wird per relativem',
    'Pfad eingebunden',
    '(für lokale Anzeige).',
    'Die Ausgabe ist auf Deutsch; in HTML',
    'wird', 'lang=&quot;de&quot;', 'im',
    'erzeugten &lt;html&gt;-Tag gesetzt.',
    'Für ODT wird sprache auch als &quot;de&quot; gesetzt. Für',
    'andere Formate wird die Sprache ignoriert.',
    '</p>'
]
THIS_EXPECTED_HTML_PRE = [
    '<!DOCTYPE html>',
    '<html lang="de">',
    '<head>',
    '<meta charset="utf-8">',
    '<title>HTML file</title>',
    '<link rel="stylesheet" href="../css/e41_styles.css">',
    '</head>',
    '<body>',
]
EXPECTED_HTML_TEXT = THIS_EXPECTED_HTML_PRE + \
    EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + \
    EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST


def test_42_filter_args_for_format_md(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the filter_args_for_format_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(
        filter_args_for_format_example,
        expected_txt,
        expected_error=[])
    check_capsys_silent(capsys)


def test_42_filter_args_for_format_html(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test filter_args_for_format_example with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(filter_args_for_format_example, expected_txt)
    check_capsys_silent(capsys)


def test_42_filter_args_for_format_docx(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test filter_args_for_format_example with the docx format."""
    expected_txt = EXPECTED_HTML_BODY_TEXT
    expected_warnings: list[str] = []
    check_docx_func(
        filter_args_for_format_example,
        expected_txt,
        expected_warnings)
    check_capsys_silent(capsys)


def test_42_filter_args_for_format_odt(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the filter_args_for_format_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(filter_args_for_format_example, expected_txt)
    check_capsys_silent(capsys)


EXPECTED_TXT_TEXT = [
    (
        'CSS in HTML gefiltert für andere Formate\n'
        '****************************************\n'
        '\n'
    ),
    (
        'Dieses Beispiel zeigt, wie Sie eine CSS-Datei für HTML gefiltert '
        'haben, so dass\n'
        'sie nicht für andere Formate verfügbar ist.\n'
        '\n'
    ),
    (
        'Die CSS-Datei liegt unter example/css/ und wird per relativem Pfad '
        'eingebunden\n'
        '(für lokale Anzeige). Die Ausgabe ist auf Deutsch; in HTML wird '
        'lang="de" im\n'
        'erzeugten <html>-Tag gesetzt. Für ODT wird sprache auch als "de" '
        'gesetzt. Für\n'
        'andere Formate wird die Sprache ignoriert.\n'
    ),
]


def test_42_filter_args_for_format_txt(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test the filter_args_for_format_example function with the txt format."""
    expected_txt = EXPECTED_TXT_TEXT
    check_txt_func(filter_args_for_format_example, expected_txt)
    check_capsys_silent(capsys)


def test_42_filter_args_for_format_rst(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test filter_args_for_format_example with the reST format."""
    expected_txt = [
        'CSS in HTML gefiltert für andere Formate',
        'so dass',
        'Für ODT wird sprache auch als "de" gesetzt.',
        'andere Formate wird die Sprache ignoriert.',
    ]
    expected_error: list[str] = []
    check_rst_func(filter_args_for_format_example, expected_txt,
                   expected_error)
    check_capsys_silent(capsys)
