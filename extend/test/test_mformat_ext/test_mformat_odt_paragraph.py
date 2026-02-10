#! /usr/local/bin/python3
"""Test the mformat_odt module paragraph functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import pytest
from odf.text import P, A
from mformat_ext.mformat_odt import MultiFormatOdt
from test_mformat_odt_core import (
    silent_odt_create, get_elements_by_type, get_element_text,
    get_paragraph_texts, get_all_text_content, has_span_with_style,
    has_link_with_url
)


# --- Tests for basic paragraphs ---


def test_simple_paragraph(capsys):
    """Test a simple paragraph."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Hello, World!')

    doc = silent_odt_create(capsys, func=func)
    paragraphs = get_paragraph_texts(doc)
    assert 'Hello, World!' in paragraphs


def test_multiple_paragraphs(capsys):
    """Test multiple paragraphs."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='First paragraph')
        mfo.start_paragraph(text='Second paragraph')
        mfo.start_paragraph(text='Third paragraph')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'First paragraph' in all_text
    assert 'Second paragraph' in all_text
    assert 'Third paragraph' in all_text


def test_paragraph_with_add_text(capsys):
    """Test paragraph with additional text added."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Start')
        mfo.add_text(text=' middle')
        mfo.add_text(text=' end')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Start middle end' in all_text


def test_paragraph_with_empty_start_text(capsys):
    """Test starting paragraph with empty string then adding text."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='')
        mfo.add_text(text='Added later')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Added later' in all_text


# --- Tests for paragraph formatting ---


def test_paragraph_bold(capsys):
    """Test paragraph with bold text."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Bold text', bold=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Bold text' in all_text
    # Verify bold style is applied
    for para in get_elements_by_type(doc, P):
        if 'Bold text' in get_element_text(para):
            assert has_span_with_style(para, 'bold')


def test_paragraph_italic(capsys):
    """Test paragraph with italic text."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Italic text', italic=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Italic text' in all_text
    # Verify italic style is applied
    for para in get_elements_by_type(doc, P):
        if 'Italic text' in get_element_text(para):
            assert has_span_with_style(para, 'italic')


def test_paragraph_bold_italic(capsys):
    """Test paragraph with bold and italic text."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Bold italic', bold=True, italic=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Bold italic' in all_text
    # Verify bold-italic style is applied
    for para in get_elements_by_type(doc, P):
        if 'Bold italic' in get_element_text(para):
            assert has_span_with_style(para, 'bold-italic')


def test_mixed_formatting_in_paragraph(capsys):
    """Test paragraph with mixed formatting."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Normal ')
        mfo.add_text(text='bold', bold=True)
        mfo.add_text(text=' normal ')
        mfo.add_text(text='italic', italic=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Normal' in all_text
    assert 'bold' in all_text
    assert 'italic' in all_text


# --- Tests for URLs in paragraphs ---


def test_paragraph_with_url(capsys):
    """Test paragraph with URL."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Check this link: ')
        mfo.add_url(url='http://example.com', text='Example')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Check this link:' in all_text
    assert 'Example' in all_text
    # Verify URL is present
    for para in get_elements_by_type(doc, P):
        if 'Example' in get_element_text(para):
            assert has_link_with_url(para, 'http://example.com')


def test_url_without_text(capsys):
    """Test URL without display text (URL becomes the text)."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Link: ')
        mfo.add_url(url='http://example.com')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Link:' in all_text
    assert 'http://example.com' in all_text


def test_url_with_bold(capsys):
    """Test URL with bold formatting."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='See ')
        mfo.add_url(url='http://example.com', text='link', bold=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'See' in all_text
    assert 'link' in all_text
    # Verify URL is present
    for para in get_elements_by_type(doc, P):
        if 'link' in get_element_text(para):
            assert has_link_with_url(para, 'http://example.com')


def test_url_with_italic(capsys):
    """Test URL with italic formatting."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='See ')
        mfo.add_url(url='http://example.com', text='link', italic=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'See' in all_text
    assert 'link' in all_text


def test_multiple_urls_in_paragraph(capsys):
    """Test multiple URLs in one paragraph."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Visit ')
        mfo.add_url(url='http://example1.com', text='site1')
        mfo.add_text(text=' or ')
        mfo.add_url(url='http://example2.com', text='site2')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Visit' in all_text
    assert 'site1' in all_text
    assert 'site2' in all_text
    # Verify both URLs are present
    url_found_1 = False
    url_found_2 = False
    for para in get_elements_by_type(doc, P):
        for link in para.getElementsByType(A):
            href = link.getAttribute('href')
            if href == 'http://example1.com':
                url_found_1 = True
            elif href == 'http://example2.com':
                url_found_2 = True
    assert url_found_1
    assert url_found_2


# --- Tests for special characters in paragraphs ---


def test_special_characters_in_paragraph(capsys):
    """Test special characters in paragraph text."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Special chars: <>&"\'')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert '<>&"\'' in all_text


def test_unicode_in_paragraph(capsys):
    """Test unicode characters in paragraph text."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Unicode: åäö éèê 日本語')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'åäö' in all_text
    assert 'éèê' in all_text
    assert '日本語' in all_text


# --- Tests for paragraph transitions ---


def test_paragraph_after_paragraph(capsys):
    """Test paragraph immediately after paragraph."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='First')
        mfo.start_paragraph(text='Second')

    doc = silent_odt_create(capsys, func=func)
    paragraphs = get_paragraph_texts(doc)
    assert 'First' in paragraphs
    assert 'Second' in paragraphs


@pytest.mark.parametrize('first_format, second_format', [
    ({'bold': True}, {'italic': True}),
    ({'italic': True}, {'bold': True}),
    ({}, {'bold': True, 'italic': True}),
])
def test_paragraph_format_transitions(capsys, first_format, second_format):
    """Test paragraphs with different formatting transitions."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='First', **first_format)
        mfo.start_paragraph(text='Second', **second_format)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'First' in all_text
    assert 'Second' in all_text


@pytest.mark.parametrize('text,code,expected',
                         [('text', 'code', 'text code'),
                          ('Here is the code: ',
                           ' print("Hello")',
                           'Here is the code: print("Hello")')])
def test_add_code_in_text(capsys, text, code, expected):
    """Test the add_code_in_text method."""
    def test_action(mfo):
        assert isinstance(mfo, MultiFormatOdt)
        mfo.start_paragraph(text=text)
        mfo.add_code_in_text(text=code)

    doc = silent_odt_create(capsys, func=test_action)
    all_text = get_all_text_content(doc)
    assert text in all_text
    assert expected in all_text
