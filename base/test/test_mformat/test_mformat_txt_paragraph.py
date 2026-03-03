#! /usr/local/bin/python3
"""Test the mformat_txt module paragraph functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import pytest
from mformat.factory import OptArgs
from .test_helpers import check_run_with_context_manager


@pytest.mark.parametrize(
    'text, expected',
    [
        ('Simple text', 'Simple text\n'),
        ('a b c d e f g h i', 'a b c d e f\ng h i\n'),
    ]
)
def test_new_paragraph(capsys, text, expected):
    """Test creating a new paragraph in TXT output."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_paragraph(text=text)

    args: OptArgs = {'line_length': 11} if text.startswith('a b c') else None
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   args=args,
                                   capsys=capsys)


def test_paragraph_add_text_smart_ws(capsys):
    """Test smart whitespace handling when adding paragraph text."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_paragraph(text='  start  ', smart_ws=True)
        mfd.add_text(text='  next  ')
        mfd.add_text(text=' end')

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text='start next end\n',
                                   capsys=capsys)


def test_paragraph_add_text_no_smart_ws(capsys):
    """Test paragraph text with smart_ws disabled."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_paragraph(text='start', smart_ws=False)
        mfd.add_text(text='  next', smart_ws=False)

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text='start  next\n',
                                   capsys=capsys)


@pytest.mark.parametrize(
    'url, text, expected',
    [
        ('http://example.com', 'this link',
         'See this link http://example.com\n'),
        ('http://example.com', None,
         'See http://example.com\n'),
    ]
)
def test_add_url(capsys, url, text, expected):
    """Test adding URLs in paragraph text."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_paragraph(text='See')
        mfd.add_url(url=url, text=text)

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_add_url_url_as_text(capsys):
    """Test adding URL with url_as_text enabled."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_paragraph(text='See')
        mfd.add_url(url='http://example.com', text='this link')

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text='See this link '
                                                 'http://example.com\n',
                                   url_as_text=True,
                                   capsys=capsys)


def test_add_code_in_text_wraps_atomically(capsys):
    """Test code-in-text wrapping keeps code token atomic."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_paragraph(text='Use')
        mfd.add_code_in_text(text='averylongtoken')

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text='Use\n averylongtoken\n',
                                   args={'line_length': 11},
                                   capsys=capsys)


def test_block_quote_text_wrapping(capsys):
    """Test block quote formatting in TXT output."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_block_quote(text='a b c d e f g h i')

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text='> a b c d e\n> f g h i\n',
                                   args={'line_length': 11},
                                   capsys=capsys)
