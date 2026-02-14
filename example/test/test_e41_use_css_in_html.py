#! /usr/local/bin/python3
"""Test the e50_simple_complete example."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest  # pylint: disable=unused-import
from test_e01_paragraph import EXPECTED_HTML_POST, EXPECTED_ODT_PRE
from example_checkers import (
    check_markdown_func, check_capsys_silent, check_html_func,
    check_docx_func, check_odt_func, odt_version_of_html)
# Add example/src to path
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e41_use_css_in_html import use_css_in_html_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501



EXPECTED_MD_TEXT = [
    '# CSS und Sprache in HTML\n\n'
    'Dieses Beispiel zeigt, wie Sie eine CSS-Datei und die Dokumentensprache '
    '(lang)\n'
    'mit mformat setzen. Übergeben Sie OptArgs mit "css_file" und '
    '"lang" an\n'
    'create_mf, wenn das Format HTML ist.\n\n'
    'Die CSS-Datei liegt unter example/css/ und wird per relativem Pfad '
    'eingebunden\n'
    '(für lokale Anzeige). Die Ausgabe ist auf Deutsch; '
    'lang="de" steht im erzeugten\n'
    '\\<html>-Tag.\n'
]
EXPECTED_HTML_BODY_TEXT = [
    '<h1>',
    'CSS und Sprache in HTML',
    '</h1>',
    '<p>',
    'Dieses Beispiel zeigt, wie Sie eine CSS-Datei und die',
    'Dokumentensprache (lang) mit mformat setzen. Übergeben',
    'Sie OptArgs mit &quot;css_file&quot; und &quot;lang&quot;',
    'an create_mf, wenn das Format HTML ist.',
    '</p>',
    '<p>',
    'Die CSS-Datei liegt unter example/css/ und wird per relativem',
    'Pfad eingebunden (für lokale Anzeige). Die Ausgabe ist auf',
    'Deutsch; lang=&quot;de&quot; steht im erzeugten &lt;html&gt;-Tag.',
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
EXPECTED_HTML_TEXT = THIS_EXPECTED_HTML_PRE + EXPECTED_HTML_BODY_TEXT + EXPECTED_HTML_POST
EXPECTED_ODT_BODY_TEXT = odt_version_of_html(EXPECTED_HTML_BODY_TEXT)
EXPECTED_ODT_BODY_TEXT2 = [
    '<h1',
    'CSS und Sprache in HTML',
    '</h1>',
    '<p',
    'Dieses Beispiel zeigt, wie Sie eine CSS-Datei und die',
    'Dokumentensprache (lang) mit mformat setzen. Übergeben',
    'Sie OptArgs mit "css_file" und "lang"',
    'an create_mf, wenn das Format HTML ist.',
    '</p>',
    '<p',
    'Die CSS-Datei liegt unter example/css/ und wird per relativem',
    'Pfad eingebunden (für lokale Anzeige). Die Ausgabe ist auf',
    'Deutsch; lang="de" steht im erzeugten &lt;html&gt;-Tag.',
    '</p>'
]
EXPECTED_ODT_TEXT = EXPECTED_ODT_PRE + EXPECTED_ODT_BODY_TEXT + EXPECTED_HTML_POST



def test_41_use_css_in_html_md(capsys):
    """Test the use_css_in_html_example function with the md format."""
    expected_txt = EXPECTED_MD_TEXT
    check_markdown_func(use_css_in_html_example, expected_txt, expected_error=[])
    check_capsys_silent(capsys)


def test_41_use_css_in_html_html(capsys):
    """Test the use_css_in_html_example function with the html format."""
    expected_txt = EXPECTED_HTML_TEXT
    check_html_func(use_css_in_html_example, expected_txt)
    check_capsys_silent(capsys)


def test_41_use_css_in_html_docx(capsys):
    """Test the use_css_in_html_example function with the docx format."""
    expected_txt = EXPECTED_HTML_BODY_TEXT
    expected_warnings = []
    check_docx_func(use_css_in_html_example, expected_txt, expected_warnings)
    check_capsys_silent(capsys)


def test_41_use_css_in_html_odt(capsys):
    """Test the use_css_in_html_example function with the odt format."""
    expected_txt = EXPECTED_ODT_TEXT
    check_odt_func(use_css_in_html_example, expected_txt)
    check_capsys_silent(capsys)


def test_odt_body_text():
    """Test the odt body text."""
    assert EXPECTED_ODT_BODY_TEXT == EXPECTED_ODT_BODY_TEXT2
