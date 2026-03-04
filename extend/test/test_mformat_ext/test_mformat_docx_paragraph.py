#! /usr/local/bin/python3
"""Test the mformat_docx module paragraph functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from mformat_ext.mformat_docx import MultiFormatDocx
from .test_mformat_docx_core import silent_docx_create


def test_add_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the add_url method creates a docx file with URL content."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_paragraph('Check this link:')
        mfd.add_url(url='http://example.com', text='Example')

    html = silent_docx_create(capsys, func=func)
    assert 'Check this link:' in html
    assert '<a href="http://example.com">Example</a>' in html


def test_add_url_as_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the add_url method with url_as_text=True."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_paragraph('Check this:')
        mfd.add_url(url='http://example.com', text='Here')

    html = silent_docx_create(capsys, func=func)
    assert 'Check this:' in html
    assert '<a href="http://example.com">Here</a>' in html


@pytest.mark.parametrize(
    'text,code,expected',
    [('text', 'code', 'text code'),
     ('Here is the code:', 'print("Hello")', 'print(&quot;Hello&quot;)')])
def test_add_code_in_text(capsys: pytest.CaptureFixture[str], text: str,
                          code: str, expected: str) -> None:
    """Test the add_code_in_text method."""

    def test_action(mfd: MultiFormatDocx) -> None:
        mfd.new_paragraph(text=text)
        mfd.add_code_in_text(text=code)

    html = silent_docx_create(capsys, func=test_action)
    assert text in html
    assert expected in html
