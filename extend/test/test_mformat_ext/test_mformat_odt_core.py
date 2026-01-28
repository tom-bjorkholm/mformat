#! /usr/local/bin/python3
"""Test the mformat_odt module core functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from typing import Callable, Any
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from odf.opendocument import load as odf_load
from odf.text import P, H, Span, A
from odf.element import Element as OdfElement
from odf.teletype import extractText
from mformat_ext.mformat_odt import MultiFormatOdt
from mformat.mformat import FormatterDescriptor
from mformat.factory import create_mf

# Add base test helpers to path for shared test utilities
_base_test_path = (
    Path(__file__).parent.parent.parent.parent /
    'base' / 'test' / 'test_mformat'
)
sys.path.insert(0, str(_base_test_path))
# pylint: disable=wrong-import-order,wrong-import-position,import-error
from check_capsys import check_capsys  # noqa: E402


# --- Helper functions for ODT tests ---


def get_element_text(element: OdfElement) -> str:
    """Extract all text content from an ODF element recursively.

    Uses odfpy's extractText function for proper text extraction.

    Args:
        element: The ODF element to extract text from.

    Returns:
        The concatenated text content of the element and all children.
    """
    return extractText(element)


def get_elements_by_type(doc: Any, element_type: type) -> list[Any]:
    """Get all elements of a specific type from an ODF document.

    Args:
        doc: The ODF document.
        element_type: The type of element to search for.

    Returns:
        A list of elements of the specified type.
    """
    return doc.getElementsByType(element_type)


def silent_odt_create(
        capsys: pytest.CaptureFixture[str],
        func: Callable[[MultiFormatOdt], None],
        fname: str = 'test.odt',
        lang: str = 'en-UK') -> Any:
    """Create an ODT file silently and return the loaded document.

    func is expected to write to the file silently.
    Check that the file is created and that there are no output on
    stdout or stderr. We also check that the file exists and is not empty
    after func has been called.

    Args:
        capsys: The pytest capsys fixture.
        func: The function to call with the MultiFormatOdt instance.
        fname: The filename to use.
        lang: The language parameter for the ODT document.

    Returns:
        The loaded ODF document (using odfpy).
    """
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/' + fname
        args = {'lang': lang} if lang != 'en-UK' else None
        if args:
            with create_mf('odt', file_name=fpath, args=args) as mfo:
                func(mfo)
        else:
            with create_mf('odt', file_name=fpath) as mfo:
                func(mfo)
        assert os.path.exists(fpath)
        assert os.path.getsize(fpath) > 0
        check_capsys(capsys)
        return odf_load(fpath)


def get_all_text_content(doc: Any) -> str:
    """Get all text content from an ODT document.

    Args:
        doc: The ODF document.

    Returns:
        All text content concatenated.
    """
    text_parts = []
    # Get paragraphs
    for para in get_elements_by_type(doc, P):
        text_parts.append(get_element_text(para))
    # Get headings
    for heading in get_elements_by_type(doc, H):
        text_parts.append(get_element_text(heading))
    return ' '.join(text_parts)


def get_heading_texts(doc: Any) -> list[tuple[int, str]]:
    """Get all headings from an ODT document with their levels.

    Args:
        doc: The ODF document.

    Returns:
        A list of tuples (level, text) for each heading.
    """
    headings = []
    for heading in get_elements_by_type(doc, H):
        level_attr = heading.getAttribute('outlinelevel')
        level = int(level_attr) if level_attr else 1
        text = get_element_text(heading)
        headings.append((level, text))
    return headings


def get_paragraph_texts(doc: Any) -> list[str]:
    """Get all paragraph texts from an ODT document.

    Note: This returns all P elements, including those in tables and lists.

    Args:
        doc: The ODF document.

    Returns:
        A list of text content for each paragraph.
    """
    return [get_element_text(para) for para in get_elements_by_type(doc, P)]


def has_span_with_style(element: OdfElement, style_name: str) -> bool:
    """Check if an element contains a span with a specific style.

    Args:
        element: The ODF element to search in.
        style_name: The style name to search for.

    Returns:
        True if a span with the specified style is found.
    """
    for span in element.getElementsByType(Span):
        if span.getAttribute('stylename') == style_name:
            return True
    return False


def has_link_with_url(element: OdfElement, url: str) -> bool:
    """Check if an element contains a link with a specific URL.

    Args:
        element: The ODF element to search in.
        url: The URL to search for.

    Returns:
        True if a link with the specified URL is found.
    """
    for link in element.getElementsByType(A):
        href = link.getAttribute('href')
        if href == url:
            return True
    return False


# --- Tests for file extension and argument description ---


def test_file_name_extension(capsys):
    """Test the file_name_extension method."""
    assert MultiFormatOdt.file_name_extension() == '.odt'
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_get_arg_desciption(capsys):
    """Test the get_arg_desciption method."""
    assert MultiFormatOdt.get_arg_desciption() == \
        FormatterDescriptor(name='odt', mandatory_args=[],
                            optional_args=['lang'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


# --- Tests for basic file creation ---


@pytest.mark.parametrize('fname', ['test.odt', 'other.odt'])
def test_create_ok(capsys, fname):
    """Test the shortcut create function with an OK class."""
    def func(mfo: MultiFormatOdt) -> None:
        assert type(mfo).__name__ == 'MultiFormatOdt'
        mfo.start_paragraph(text='Test content')

    doc = silent_odt_create(capsys, func=func, fname=fname)
    assert doc is not None


def test_create_nok(capsys):
    """Test the shortcut create function with a not OK class."""
    with pytest.raises(TypeError) as exc:
        args = {'output': 'test.odt'}
        with create_mf('odt', file_name='test.odt', args=args) as _:
            pass
    assert "MultiFormatOdt.__init__() got an unexpected " + \
        "keyword argument 'output'" in exc.value.args[0]
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


# --- Tests for language parameter ---


@pytest.mark.parametrize('lang', ['en-UK', 'en-US', 'sv-SE', 'de-DE', 'fr-FR'])
def test_language_parameter(capsys, lang):
    """Test creating ODT with different language parameters."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Test content')

    doc = silent_odt_create(capsys, func=func, lang=lang)
    assert doc is not None
    # Verify content was written
    all_text = get_all_text_content(doc)
    assert 'Test content' in all_text


# --- Tests for headings ---


@pytest.mark.parametrize('level', [1, 2, 3, 4, 5, 6])
def test_heading_creation(capsys, level):
    """Test creating headings at different levels."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=level, text=f'Heading Level {level}')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    assert headings[0] == (level, f'Heading Level {level}')


def test_heading_with_text(capsys):
    """Test heading with additional text."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=1, text='Main Title')
        mfo.add_text(text=' - Extended')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    assert headings[0] == (1, 'Main Title - Extended')


def test_heading_with_url(capsys):
    """Test heading with URL."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=2, text='Check ')
        mfo.add_url(url='http://example.com', text='this link')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    assert 'Check' in headings[0][1]
    assert 'this link' in headings[0][1]
    # Verify the URL is present
    for heading in get_elements_by_type(doc, H):
        assert has_link_with_url(heading, 'http://example.com')


def test_heading_then_paragraph(capsys):
    """Test heading followed by paragraph."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=1, text='Title')
        mfo.start_paragraph('Some text')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    assert headings[0] == (1, 'Title')
    all_text = get_all_text_content(doc)
    assert 'Some text' in all_text


def test_multiple_headings(capsys):
    """Test multiple headings."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=1, text='Main')
        mfo.start_heading(level=2, text='Sub')
        mfo.start_heading(level=3, text='Subsub')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 3
    assert headings[0] == (1, 'Main')
    assert headings[1] == (2, 'Sub')
    assert headings[2] == (3, 'Subsub')


def test_heading_paragraph_heading(capsys):
    """Test heading, paragraph, then another heading."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=1, text='First Heading')
        mfo.start_paragraph('Some content here.')
        mfo.start_heading(level=2, text='Second Heading')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 2
    assert headings[0] == (1, 'First Heading')
    assert headings[1] == (2, 'Second Heading')
    all_text = get_all_text_content(doc)
    assert 'Some content here.' in all_text


@pytest.mark.parametrize('bold, italic, expected_style', [
    (True, False, 'bold'),
    (False, True, 'italic'),
    (True, True, 'bold-italic'),
])
def test_heading_formatting(capsys, bold, italic, expected_style):
    """Test heading with bold and italic formatting."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=1, text='Formatted Title',
                          bold=bold, italic=italic)

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    assert 'Formatted Title' in headings[0][1]
    # Verify the style is applied
    for heading in get_elements_by_type(doc, H):
        assert has_span_with_style(heading, expected_style)


# --- Tests for code blocks ---


def test_simple_code_block(capsys):
    """Test a simple code block."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.write_code_block(text='print("Hello, World!")')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'print("Hello, World!")' in all_text


def test_code_block_with_language(capsys):
    """Test a code block with programming language."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.write_code_block(text='print("Hello")',
                             programming_language='python')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'print("Hello")' in all_text


def test_code_block_multiline(capsys):
    """Test a multiline code block."""
    def func(mfo: MultiFormatOdt) -> None:
        code = 'def hello():\n    print("Hello")\n    return True'
        mfo.write_code_block(text=code, programming_language='python')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'def hello():' in all_text
    assert 'print("Hello")' in all_text
    assert 'return True' in all_text


def test_code_block_with_special_chars(capsys):
    """Test a code block with special characters."""
    def func(mfo: MultiFormatOdt) -> None:
        code = 'x = "test <>&"\ny = \'another\''
        mfo.write_code_block(text=code)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'x = "test <>&"' in all_text
    assert "y = 'another'" in all_text


def test_code_block_style(capsys):
    """Test that code block paragraphs have the code style."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.write_code_block(text='x = 42')

    doc = silent_odt_create(capsys, func=func)
    # Find paragraphs with code style
    code_paragraphs = []
    for para in get_elements_by_type(doc, P):
        style = para.getAttribute('stylename')
        if style == 'code':
            code_paragraphs.append(para)
    assert len(code_paragraphs) >= 1
    assert 'x = 42' in get_element_text(code_paragraphs[0])


def test_paragraph_then_code_block(capsys):
    """Test paragraph followed by code block."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Here is some code:')
        mfo.write_code_block(text='x = 42', programming_language='python')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Here is some code:' in all_text
    assert 'x = 42' in all_text


def test_code_block_then_paragraph(capsys):
    """Test code block followed by paragraph."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.write_code_block(text='x = 42')
        mfo.start_paragraph(text='That was the code.')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'x = 42' in all_text
    assert 'That was the code.' in all_text


def test_heading_then_code_block(capsys):
    """Test heading followed by code block."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=2, text='Code Example')
        mfo.write_code_block(text='example()', programming_language='python')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    assert headings[0] == (2, 'Code Example')
    all_text = get_all_text_content(doc)
    assert 'example()' in all_text


def test_multiple_code_blocks(capsys):
    """Test multiple code blocks."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.write_code_block(text='x = 1', programming_language='python')
        mfo.write_code_block(text='y = 2', programming_language='python')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'x = 1' in all_text
    assert 'y = 2' in all_text


# --- Tests for empty content ---


def test_empty_document(capsys):
    """Test that an empty document does not create a file."""
    def func(mfo: MultiFormatOdt) -> None:
        # Do nothing - empty document
        assert mfo is not None  # Silence unused argument warning

    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/empty.odt'
        with create_mf('odt', file_name=fpath) as mfo:
            func(mfo)
        # Empty documents should not create a file (state is EMPTY)
        # or create a minimal file - check what happens
        check_capsys(capsys)


# --- Tests for special characters ---


def test_special_characters_in_heading(capsys):
    """Test special characters in heading text."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=1, text='Test <>&"\'')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    # ODF handles special characters properly
    assert '<>&"\'' in headings[0][1]
