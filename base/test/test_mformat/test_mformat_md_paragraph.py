#! /usr/local/bin/python3
"""Test the mformat_md module paragraph functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
import pytest
from check_capsys import check_capsys
from test_helpers import (
    run_protected_method,
    check_run_with_context_manager,
)
from mformat.mformat_state import MultiFormatState, Formatting
from mformat.factory import create_mf


@pytest.mark.parametrize('text, expected',
                         [('test', 'test\n'),
                          ('test\ntest', 'test\ntest\n')])
def test_start_paragraph(capsys, text, expected):
    """Test the start_paragraph method."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.md'
        with create_mf('md', file_name=fname) as mfd:
            assert type(mfd).__name__ == 'MultiFormatMd'
            assert mfd.state == MultiFormatState.EMPTY
            mfd.start_paragraph(text=text)
            assert mfd.state == MultiFormatState.PARAGRAPH
        with open(fname, 'rt', encoding='utf-8') as file:
            assert file.read() == expected
        check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('bold text', True, False, '**bold text**\n'),
                          ('italic text', False, True, '*italic text*\n'),
                          ('both', True, True, '***both***\n')])
def test_start_paragraph_formatting(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                                    text, bold, italic, expected):
    """Test the start_paragraph method with bold and italic."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        assert mfd.state == MultiFormatState.EMPTY
        mfd.start_paragraph(text=text, bold=bold, italic=italic)
        assert mfd.state == MultiFormatState.PARAGRAPH

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


@pytest.mark.parametrize('bold', [True, False])
@pytest.mark.parametrize('italic', [True, False])
@pytest.mark.parametrize('text, expected',
                         [('', '\n'),
                          (' ', '\n'),
                          ('   ', '\n')])
def test_start_paragraph_space(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                               text, bold, italic, expected):
    """Test the start_paragraph method with bold and italic."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        assert mfd.state == MultiFormatState.EMPTY
        mfd.start_paragraph(text=text, bold=bold, italic=italic,
                            smart_ws=False)
        assert mfd.state == MultiFormatState.PARAGRAPH

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


@pytest.mark.parametrize('url, text, bold, italic, expected',
                         [('http://example.com', None, False, False,
                           '[http://example.com](http://example.com)'),
                          ('http://test.org', 'link text', False, False,
                           '[link text](http://test.org)'),
                          ('http://test.org', 'link', True, False,
                           '**[link](http://test.org)**'),
                          ('http://test.org', 'link', False, True,
                           '*[link](http://test.org)*'),
                          ('http://test.org', 'link', True, True,
                           '***[link](http://test.org)***')])
def test_write_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                   url, text, bold, italic, expected):
    """Test the _write_url method."""
    txt = run_protected_method('md', '.md', '_write_url',
                               (url, text, MultiFormatState.PARAGRAPH,
                                Formatting(bold=bold, italic=italic)))
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, expected',
                         [('http://example.com', None,
                           '[http://example.com](http://example.com)\n'),
                          ('http://test.org', 'link text',
                           '[link text](http://test.org)\n')])
def test_add_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 url, text, expected):
    """Test the add_url method."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_paragraph('')
        mfd.add_url(url=url, text=text)

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


@pytest.mark.parametrize('url, text, expected',
                         [('http://example.com', None,
                           'http://example.com\n'),
                          ('http://test.org', 'See here',
                           'See here http://test.org\n')])
def test_add_url_as_text(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         url, text, expected):
    """Test the add_url method with url_as_text=True."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_paragraph('')
        mfd.add_url(url=url, text=text)

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   url_as_text=True,
                                   capsys=capsys)
