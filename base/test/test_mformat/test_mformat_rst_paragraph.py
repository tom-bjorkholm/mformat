#! /usr/local/bin/python3
"""Test the mformat_rst module paragraph functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import pytest
from rst_test_helpers import check_rst_output


@pytest.mark.parametrize(
    'method_calls, expected, args',
    [
        ([('new_paragraph', {'text': 'Simple text'})],
         'Simple text\n', None),
        ([('new_paragraph', {'text': 'a b c d e f g h i'})],
         'a b c d e f\ng h i\n',
         {'line_length': 11}),
    ]
)
def test_new_paragraph(capsys, method_calls, expected, args):
    """Test creating a new paragraph in reST output."""
    check_rst_output(
        capsys=capsys,
        method_calls=method_calls,
        expected_text=expected,
        args=args)


@pytest.mark.parametrize(
    'text, bold, italic, expected',
    [
        ('bold text', True, False, '**bold text**\n'),
        ('italic text', False, True, '*italic text*\n'),
        ('both', True, True, '***both***\n'),
    ]
)
def test_new_paragraph_formatting(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                  text, bold, italic, expected):
    """Test creating paragraph with bold and italic formatting."""
    check_rst_output(
        capsys=capsys,
        method_calls=[('new_paragraph',
                       {'text': text, 'bold': bold, 'italic': italic})],
        expected_text=expected)


def test_paragraph_add_text_smart_ws(capsys):
    """Test smart whitespace handling when adding paragraph text."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_paragraph', {'text': '  start  ', 'smart_ws': True}),
            ('add_text', {'text': '  next  '}),
            ('add_text', {'text': ' end'}),
        ],
        expected_text='start next end\n')


def test_paragraph_add_text_no_smart_ws(capsys):
    """Test paragraph text with smart_ws disabled."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_paragraph', {'text': 'start', 'smart_ws': False}),
            ('add_text', {'text': '  next', 'smart_ws': False}),
        ],
        expected_text='start  next\n')


@pytest.mark.parametrize(
    'url, text, expected',
    [
        ('http://example.com', 'this link',
         'See `this link <http://example.com>`_\n'),
        ('http://example.com', None,
         'See `http://example.com <http://example.com>`_\n'),
    ]
)
def test_add_url(capsys, url, text, expected):
    """Test adding URLs in paragraph text."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_paragraph', {'text': 'See'}),
            ('add_url', {'url': url, 'text': text}),
        ],
        expected_text=expected)


def test_add_url_url_as_text(capsys):
    """Test adding URL with url_as_text enabled."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_paragraph', {'text': 'See'}),
            ('add_url', {'url': 'http://example.com', 'text': 'this link'}),
        ],
        expected_text='See this link http://example.com\n',
        url_as_text=True)


@pytest.mark.parametrize(
    'bold, italic, expected',
    [
        (True, False, 'Check **`x <http://a>`_**\n'),
        (False, True, 'Check *`x <http://a>`_*\n'),
        (True, True, 'Check ***`x <http://a>`_***\n'),
    ]
)
def test_add_url_formatting(capsys, bold, italic, expected):
    """Test adding URL with bold and italic formatting."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_paragraph', {'text': 'Check'}),
            ('add_url',
             {'url': 'http://a', 'text': 'x', 'bold': bold,
              'italic': italic}),
        ],
        expected_text=expected)


def test_add_code_in_text_wraps_atomically(capsys):
    """Test code-in-text wrapping keeps code token atomic."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_paragraph', {'text': 'Use'}),
            ('add_code_in_text', {'text': 'averylongtoken'}),
        ],
        expected_text='Use\n ``averylongtoken``\n',
        args={'line_length': 11})


def test_block_quote_text_wrapping(capsys):
    """Test block quote formatting in reST output."""
    check_rst_output(
        capsys=capsys,
        method_calls=[('new_block_quote', {'text': 'a b c d e f g h i'})],
        expected_text='  a b c d e\n  f g h i\n',
        args={'line_length': 11})
