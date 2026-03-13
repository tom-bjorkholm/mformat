#! /usr/local/bin/python3
"""Test the mformat_pdf module core functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import NamedTuple
import pytest
from mformat_ext.mformat_pdf import MultiFormatPdf
from mformat.mformat import FormatterDescriptor
from mformat.paper_size import PaperSize


class PdfInspection(NamedTuple):
    """Selected PDF details extracted through a subprocess."""

    page_text: str
    metadata_title: str
    toc: list[list[int | str]]
    link_uri: str | None
    page_width: float
    page_height: float


def _assert_toc(value: object) -> list[list[int | str]]:
    """Validate and return a PDF table-of-contents structure."""
    if not isinstance(value, list):
        raise AssertionError('Expected TOC list')
    toc: list[list[int | str]] = []
    for entry in value:
        if not isinstance(entry, list):
            raise AssertionError('Expected TOC entry list')
        validated_entry: list[int | str] = []
        for item in entry:
            if not isinstance(item, (int, str)):
                raise AssertionError('Expected TOC item to be int or str')
            validated_entry.append(item)
        toc.append(validated_entry)
    return toc


def _inspect_pdf(file_name: str) -> PdfInspection:
    """Inspect one PDF file through a subprocess using PyMuPDF."""
    script = """
import json
import sys
import fitz
with fitz.open(sys.argv[1]) as pdf_document:
    page = pdf_document[0]
    links = page.get_links()
    payload = {
        'page_text': page.get_text(),
        'metadata_title': pdf_document.metadata.get('title', ''),
        'toc': pdf_document.get_toc(),
        'link_uri': links[0].get('uri') if links else None,
        'page_width': page.rect.width,
        'page_height': page.rect.height,
    }
print(json.dumps(payload))
"""
    result = subprocess.run(
        [sys.executable, '-W', 'ignore::DeprecationWarning', '-c',
         script, file_name],
        check=True,
        capture_output=True,
        text=True,
    )
    payload: object = json.loads(result.stdout)
    if not isinstance(payload, dict):
        raise AssertionError('Expected JSON object from PDF inspection')
    page_text = payload.get('page_text')
    metadata_title = payload.get('metadata_title')
    toc_value = payload.get('toc')
    link_uri = payload.get('link_uri')
    page_width = payload.get('page_width')
    page_height = payload.get('page_height')
    if not isinstance(page_text, str):
        raise AssertionError('Expected page_text string')
    if not isinstance(metadata_title, str):
        raise AssertionError('Expected metadata_title string')
    if link_uri is not None and not isinstance(link_uri, str):
        raise AssertionError('Expected link_uri string or None')
    if not isinstance(page_width, float):
        raise AssertionError('Expected page_width float')
    if not isinstance(page_height, float):
        raise AssertionError('Expected page_height float')
    return PdfInspection(
        page_text=page_text,
        metadata_title=metadata_title,
        toc=_assert_toc(toc_value),
        link_uri=link_uri,
        page_width=page_width,
        page_height=page_height,
    )


def test_file_name_extension(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file_name_extension method."""
    assert MultiFormatPdf.file_name_extension() == '.pdf'
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_get_arg_desciption(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_arg_desciption method."""
    assert MultiFormatPdf.get_arg_desciption() == \
        FormatterDescriptor(name='pdf', mandatory_args=[],
                            optional_args=['paper_size', 'title'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_pdf_contains_core_structures() -> None:
    """Test visible PDF content for core structures."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.pdf')
        with MultiFormatPdf(file_name=file_name) as formatter:
            formatter.new_paragraph(text='Hello')
            formatter.add_text(text=' bold', bold=True)
            formatter.new_bullet_item(text='Bullet one')
            formatter.new_numbered_point_item(text='Number one', level=1)
            formatter.new_numbered_point_item(text='Nested number', level=2)
            formatter.new_table(first_row=['A', 'B'], bold=True)
            formatter.add_table_row(row=['1', '2'])
            formatter.write_code_block(text='x = 1\ny = 2')
            formatter.new_block_quote(text='Quoted text')
        inspection = _inspect_pdf(file_name)
        assert 'Hello bold' in inspection.page_text
        assert '• Bullet one' in inspection.page_text
        assert '1. Number one' in inspection.page_text
        assert '1.1. Nested number' in inspection.page_text
        assert 'A' in inspection.page_text
        assert 'B' in inspection.page_text
        assert '1' in inspection.page_text
        assert '2' in inspection.page_text
        assert 'x = 1' in inspection.page_text
        assert 'y = 2' in inspection.page_text
        assert 'Quoted text' in inspection.page_text


def test_metadata_outline_link_and_paper_size() -> None:
    """Test PDF metadata, outline entries, links and paper size."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.pdf')
        with MultiFormatPdf(file_name=file_name, title='My Title',
                            paper_size=PaperSize.A5) as formatter:
            formatter.new_heading(level=1, text='Heading One')
            formatter.new_paragraph(text='Read ')
            formatter.add_url(url='http://example.com', text='Example')
            formatter.new_heading(level=3, text='Heading Three')
        inspection = _inspect_pdf(file_name)
        assert inspection.metadata_title == 'My Title'
        assert inspection.toc == [[1, 'Heading One', 1],
                                  [2, 'Heading Three', 1],
                                  [3, 'Heading Three', 1]]
        assert inspection.link_uri == 'http://example.com'
        assert abs(inspection.page_width - 419.5276) < 0.01
        assert abs(inspection.page_height - 595.2756) < 0.01
