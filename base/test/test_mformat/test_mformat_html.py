#! /usr/local/bin/python3
"""Test the mformat_html module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from test_helpers import run_with_context_manager, run_protected_method
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat import FormatterDescriptor, MultiFormatState


def test_file_name_extension(capsys):
    """Test the file_name_extension method."""
    assert MultiFormatHtml.file_name_extension() == '.html'
    check_capsys(capsys)


def test_get_arg_desciption(capsys):
    """Test the get_arg_desciption method."""
    assert MultiFormatHtml.get_arg_desciption() == \
        FormatterDescriptor(name='html', mandatory_args=[],
                            optional_args=['title', 'css_file', 'lang'])
    check_capsys(capsys)


PFDT = '<!DOCTYPE html encoding="utf-8">\n<html lang="'
PTAL = '">\n<head>\n<title>'
PFAT = '</title>\n'
PFCSS = '<link rel="stylesheet" href="'
PFCSSE = '">\n'
PFLS = '</head>\n<body>\n'

SFTOT = '</body>\n</html>\n'

PF_EN_NT_NC = PFDT + 'en' + PTAL + 'HTML file' + PFAT + PFLS
PF_SV_TS_C1 = PFDT + 'sv' + PTAL + 'Something' + PFAT + PFCSS + \
    'style1.css' + PFCSSE + PFLS


@pytest.mark.parametrize('lang, title, css_file, expected',
                         [('en', None, None, PF_EN_NT_NC),
                          ('sv', 'Something', 'style1.css', PF_SV_TS_C1)])
def test_write_file_prefix(capsys, lang, title, css_file, expected):
    """Test the write_file_prefix method."""
    args = {'lang': lang}
    if title is not None:
        args['title'] = title
    if css_file is not None:
        args['css_file'] = css_file
    txt = run_protected_method('html', '.html', '_write_file_prefix',
                               args=args)
    assert txt == expected
    check_capsys(capsys)


def test_write_file_suffix(capsys):
    """Test the write_file_suffix method."""
    txt = run_protected_method('html', '.html', '_write_file_suffix')
    assert txt == SFTOT
    check_capsys(capsys)


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


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('Hello, world!', False, False, 'Hello, world!'),
                          ('Something else', False, False,
                           'Something else'),
                          ('Bold text', True, False,
                           '<strong>Bold text</strong>'),
                          ('Italic text', False, True,
                           '<em>Italic text</em>'),
                          ('Both', True, True,
                           '<em><strong>Both</strong></em>')])
def test_write_text(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                    text, bold, italic, expected):
    """Test the _write_text method."""
    txt = run_protected_method('html', '.html', '_write_text',
                               (text, MultiFormatState.PARAGRAPH,
                                bold, italic))
    assert txt == expected
    check_capsys(capsys)


EN_NT_NC_T1 = PF_EN_NT_NC + '<p>\nHello, world!</p>\n<p>\nBye!</p>\n' + SFTOT
SV_TS_C1_T2 = PF_SV_TS_C1 + '<p>\nSomething else</p>\n<p>\nYeah!</p>\n' + \
    SFTOT
EN_NT_NC_BOLD = PF_EN_NT_NC + '<p>\n<strong>Bold text</strong></p>\n' + SFTOT
EN_NT_NC_ITALIC = PF_EN_NT_NC + '<p>\n<em>Italic text</em></p>\n' + SFTOT
EN_NT_NC_BOTH = PF_EN_NT_NC + \
    '<p>\n<em><strong>Both styles</strong></em></p>\n' + SFTOT


@pytest.mark.parametrize('lang, title, css_file, texts, expected',
                         [('en', None, None,
                           ['Hello, world!', 'Bye!'], EN_NT_NC_T1),
                          ('sv', 'Something', 'style1.css',
                           ['Something else', 'Yeah!'], SV_TS_C1_T2)])
def test_start_paragraph2(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                          lang, title, css_file, texts, expected):
    """Test the start_paragraph method."""
    args = {'lang': lang}
    if title is not None:
        args['title'] = title
    if css_file is not None:
        args['css_file'] = css_file

    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        for text in texts:
            mfd.start_paragraph(text)

    txt = run_with_context_manager('html', '.html', test_action, args=args)
    assert txt == expected
    check_capsys(capsys)


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

    txt = run_with_context_manager('html', '.html', test_action)
    assert txt == PF_EN_NT_NC + '<p>\n' + expected + '</p>\n' + SFTOT
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, bold, italic, expected',
                         [('http://example.com', None, False, False,
                           ' <a href="http://example.com">'
                           'http://example.com</a>'),
                          ('http://test.org', 'link text', False, False,
                           ' <a href="http://test.org">'
                           'link text</a>'),
                          ('http://test.org', 'link', True, False,
                           '<strong> <a href="http://test.org">'
                           'link</a></strong>'),
                          ('http://test.org', 'link', False, True,
                           '<em> <a href="http://test.org">'
                           'link</a></em>'),
                          ('http://test.org', 'link', True, True,
                           '<em><strong> <a href="http://test.org">'
                           'link</a></strong></em>')])
def test_write_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                   url, text, bold, italic, expected):
    """Test the _write_url method."""
    txt = run_protected_method('html', '.html', '_write_url',
                               (url, text, MultiFormatState.PARAGRAPH,
                                bold, italic))
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, expected',
                         [('http://example.com', None,
                           PF_EN_NT_NC +
                           '<p>\n <a href="http://example.com">'
                           'http://example.com</a></p>\n' + SFTOT),
                          ('http://test.org', 'link text',
                           PF_EN_NT_NC +
                           '<p>\n <a href="http://test.org">'
                           'link text</a></p>\n' + SFTOT)])
def test_add_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 url, text, expected):
    """Test the add_url method."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph('')
        mfd.add_url(url=url, text=text)

    txt = run_with_context_manager('html', '.html', test_action)
    assert txt == expected
    check_capsys(capsys)


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

    txt = run_with_context_manager('html', '.html', test_action,
                                   url_as_text=True)
    assert txt == expected
    check_capsys(capsys)
