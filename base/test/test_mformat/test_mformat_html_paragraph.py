#! /usr/local/bin/python3
"""Test the mformat_html module paragraph functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Any
import pytest
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat_state import Formatting, MultiFormatState
from .check_capsys import check_capsys
from .test_helpers import check_run_with_context_manager, run_protected_method
from .test_mformat_html_core import (EN_NT_NC_T1, PF_EN_NT_NC, SFTOT,
                                     SV_TS_C1_T2, args_for_file_prefix)


def test_start_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the _start_paragraph method."""
    txt = run_protected_method('html', '.html', '_start_paragraph')
    assert txt == '<p>\n'
    check_capsys(capsys)


def test_end_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the end_paragraph method."""
    txt = run_protected_method('html', '.html', '_end_paragraph')
    assert txt == '</p>\n'
    check_capsys(capsys)


@pytest.mark.parametrize('lang, title, css_file, texts, expected',
                         [('en', None, None,
                           ['Hello, world!', 'Bye!'], EN_NT_NC_T1),
                          ('sv', 'Something', 'style1.css',
                           ['Something else', 'Yeah!'], SV_TS_C1_T2)])
def test_new_paragraph2(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                        lang: str, title: str | None,
                        css_file: str | None, texts: list[str],
                        expected: str) -> None:
    """Test the new_paragraph method."""
    args = args_for_file_prefix(lang, title, css_file)

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        for text in texts:
            mfd.new_paragraph(text)

    check_run_with_context_manager('html', '.html', test_action, args=args,
                                   expected_text=expected, capsys=capsys)


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('Bold text', True, False,
                           '<strong>Bold text</strong>'),
                          ('Italic text', False, True,
                           '<em>Italic text</em>'),
                          ('Both styles', True, True,
                           '<em><strong>Both styles</strong></em>')])
def test_new_paragraph_formatting(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                                  text: str, bold: bool, italic: bool,
                                  expected: str) -> None:
    """Test the new_paragraph method with bold and italic."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_paragraph(text, bold=bold, italic=italic)

    exp = PF_EN_NT_NC + '<p>\n' + expected + '</p>\n' + SFTOT
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=exp, capsys=capsys)


@pytest.mark.parametrize('url, text, bold, italic, expected',
                         [('http://example.com', None, False, False,
                           '<a href="http://example.com">'
                           'http://example.com</a>'),
                          ('http://test.org', 'link text', False, False,
                           '<a href="http://test.org">'
                           'link text</a>'),
                          ('http://test.org', 'link', True, False,
                           '<strong><a href="http://test.org">'
                           'link</a></strong>'),
                          ('http://test.org', 'link', False, True,
                           '<em><a href="http://test.org">'
                           'link</a></em>'),
                          ('http://test.org', 'link', True, True,
                           '<em><strong><a href="http://test.org">'
                           'link</a></strong></em>')])
def test_write_url(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                   url: str, text: str | None, bold: bool, italic: bool,
                   expected: str) -> None:
    """Test the _write_url method."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd._write_url(url=url,  # pylint: disable=protected-access
                       text=text,
                       formatting=Formatting(bold=bold, italic=italic),
                       state=MultiFormatState.PARAGRAPH)

    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


@pytest.mark.parametrize('url, text, expected',
                         [('http://example.com', None,
                           PF_EN_NT_NC +
                           '<p>\n<a href="http://example.com">'
                           'http://example.com</a></p>\n' + SFTOT),
                          ('http://test.org', 'link text',
                           PF_EN_NT_NC +
                           '<p>\n<a href="http://test.org">'
                           'link text</a></p>\n' + SFTOT)])
def test_add_url(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 url: str, text: str | None, expected: str) -> None:
    """Test the add_url method."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_paragraph('')
        mfd.add_url(url=url, text=text)

    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


@pytest.mark.parametrize('url, text, expected',
                         [('http://example.com', None,
                           PF_EN_NT_NC +
                           '<p>\nhttp://example.com</p>\n' + SFTOT),
                          ('http://test.org', 'See here',
                           PF_EN_NT_NC +
                           '<p>\nSee here http://test.org</p>\n' +
                           SFTOT)])
def test_add_url_as_text(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         url: str, text: str | None, expected: str) -> None:
    """Test the add_url method with url_as_text=True."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_paragraph('')
        mfd.add_url(url=url, text=text)

    check_run_with_context_manager('html', '.html', test_action,
                                   url_as_text=True, expected_text=expected,
                                   capsys=capsys)


@pytest.mark.parametrize('text,code,expected',
                         [('text', 'code',
                           PF_EN_NT_NC + '<p>\n' +
                           'text <code>code</code></p>\n' + SFTOT),
                          ('Here is the code: ',
                           ' print("Hello")',
                           PF_EN_NT_NC + '<p>\n' +
                           'Here is the code: ' +
                           '<code>print(&quot;Hello&quot;)</code></p>\n' +
                           SFTOT)])
def test_add_code_in_text(capsys: pytest.CaptureFixture[str],
                          text: str, code: str, expected: str) -> None:
    """Test the add_code_in_text method."""
    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_paragraph(text=text)
        mfd.add_code_in_text(text=code)

    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)
