#! /usr/local/bin/python3
"""Test the mformat_html module paragraph functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from test_helpers import check_run_with_context_manager, run_protected_method
from test_mformat_html_core import (
    PF_EN_NT_NC, SFTOT,
    EN_NT_NC_T1, SV_TS_C1_T2,
    args_for_file_prefix,
)
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat import MultiFormatState


def test_start_paragraph(capsys):
    """Test the start_paragraph method."""
    txt = run_protected_method('html', '.html', '_start_paragraph')
    assert txt == '<p>\n'
    check_capsys(capsys)


def test_end_paragraph(capsys):
    """Test the end_paragraph method."""
    txt = run_protected_method('html', '.html', '_end_paragraph')
    assert txt == '</p>\n'
    check_capsys(capsys)


@pytest.mark.parametrize('lang, title, css_file, texts, expected',
                         [('en', None, None,
                           ['Hello, world!', 'Bye!'], EN_NT_NC_T1),
                          ('sv', 'Something', 'style1.css',
                           ['Something else', 'Yeah!'], SV_TS_C1_T2)])
def test_start_paragraph2(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                          lang, title, css_file, texts, expected):
    """Test the start_paragraph method."""
    args = args_for_file_prefix(lang, title, css_file)

    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        for text in texts:
            mfd.start_paragraph(text)

    check_run_with_context_manager('html', '.html', test_action, args=args,
                                   expected_text=expected, capsys=capsys)


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('Bold text', True, False,
                           '<strong>Bold text</strong>'),
                          ('Italic text', False, True,
                           '<em>Italic text</em>'),
                          ('Both styles', True, True,
                           '<em><strong>Both styles</strong></em>')])
def test_start_paragraph_formatting(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                                    text, bold, italic, expected):
    """Test the start_paragraph method with bold and italic."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph(text, bold=bold, italic=italic)

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
def test_write_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                   url, text, bold, italic, expected):
    """Test the _write_url method."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd._write_url(url=url,  # pylint: disable=protected-access
                       text=text, bold=bold, italic=italic,
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
def test_add_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 url, text, expected):
    """Test the add_url method."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph('')
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
def test_add_url_as_text(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         url, text, expected):
    """Test the add_url method with url_as_text=True."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph('')
        mfd.add_url(url=url, text=text)

    check_run_with_context_manager('html', '.html', test_action,
                                   url_as_text=True, expected_text=expected,
                                   capsys=capsys)
