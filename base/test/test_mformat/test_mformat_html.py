#! /usr/local/bin/python3
"""Test the mformat_html module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
import pytest
from check_capsys import check_capsys
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat import FormatterDescriptor, NewOrAppend
from mformat.factory import create as create_mf


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
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.html'
        args = {'lang': lang}
        if title is not None:
            args['title'] = title
        if css_file is not None:
            args['css_file'] = css_file
        mfd = create_mf('html', file_name=fname, args=args)
        assert isinstance(mfd, MultiFormatHtml)
        mfd.open()
        mfd._write_file_prefix()  # pylint: disable=protected-access
        mfd._close()  # pylint: disable=protected-access
        with open(fname, 'rt', encoding='utf-8') as file:
            txt = file.read()
            assert txt == expected
    check_capsys(capsys)


def test_write_file_suffix(capsys):
    """Test the write_file_suffix method."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.html'
        mfd = create_mf('html', file_name=fname)
        assert isinstance(mfd, MultiFormatHtml)
        mfd.open()
        mfd._write_file_suffix()  # pylint: disable=protected-access
        mfd._close()  # pylint: disable=protected-access
        with open(fname, 'rt', encoding='utf-8') as file:
            txt = file.read()
            assert txt == SFTOT
    check_capsys(capsys)


def test_start_paragraph(capsys):
    """Test the start_paragraph method."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.html'
        mfd = create_mf('html', file_name=fname)
        assert isinstance(mfd, MultiFormatHtml)
        mfd.open()
        mfd._start_paragraph()  # pylint: disable=protected-access
        mfd._close()  # pylint: disable=protected-access
        with open(fname, 'rt', encoding='utf-8') as file:
            txt = file.read()
            assert txt == '<p>\n'
    check_capsys(capsys)


def test_end_paragraph(capsys):
    """Test the end_paragraph method."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.html'
        mfd = create_mf('html', file_name=fname)
        assert isinstance(mfd, MultiFormatHtml)
        mfd.open()
        mfd._end_paragraph()  # pylint: disable=protected-access
        mfd._close()  # pylint: disable=protected-access
        with open(fname, 'rt', encoding='utf-8') as file:
            txt = file.read()
            assert txt == '</p>\n'
    check_capsys(capsys)


@pytest.mark.parametrize('text, expected',
                         [('Hello, world!', 'Hello, world!'),
                          ('Something else', 'Something else')])
def test_write_in_paragraph(capsys, text, expected):
    """Test the write_in_paragraph method."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.html'
        mfd = create_mf('html', file_name=fname)
        assert isinstance(mfd, MultiFormatHtml)
        mfd.open()
        mfd._write_in_paragraph(text)  # pylint: disable=protected-access
        mfd._close()  # pylint: disable=protected-access
        with open(fname, 'rt', encoding='utf-8') as file:
            txt = file.read()
            assert txt == expected
    check_capsys(capsys)


EN_NT_NC_T1 = PF_EN_NT_NC + '<p>\nHello, world!</p>\n<p>\nBye!</p>\n' + SFTOT
SV_TS_C1_T2 = PF_SV_TS_C1 + '<p>\nSomething else</p>\n<p>\nYeah!</p>\n' + \
    SFTOT


@pytest.mark.parametrize('lang, title, css_file, texts, expected',
                         [('en', None, None,
                           ['Hello, world!', 'Bye!'], EN_NT_NC_T1),
                          ('sv', 'Something', 'style1.css',
                           ['Something else', 'Yeah!'], SV_TS_C1_T2)])
def test_write_paragraph(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                         lang, title, css_file, texts, expected):
    """Test the write_paragraph method."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.html'
        args = {'lang': lang}
        if title is not None:
            args['title'] = title
        if css_file is not None:
            args['css_file'] = css_file
        with create_mf('html', file_name=fname, args=args) as mfd:
            assert isinstance(mfd, MultiFormatHtml)
            for text in texts:
                mfd.write_paragraph(text, how=NewOrAppend.NEW)
        with open(fname, 'rt', encoding='utf-8') as file:
            txt = file.read()
            assert txt == expected
    check_capsys(capsys)
