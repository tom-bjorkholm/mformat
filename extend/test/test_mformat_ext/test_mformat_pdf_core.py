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
    """Selected first-page PDF details extracted in a subprocess."""

    page_text: str
    metadata_title: str
    toc: list[list[int | str]]
    link_uri: str | None
    page_width: float
    page_height: float
    lines: list['PdfLine']
    spans: list['PdfSpan']


class PdfLine(NamedTuple):
    """One extracted text line from the first page."""

    text: str
    x0: float
    y0: float


class PdfSpan(NamedTuple):
    """One extracted text span from the first page."""

    text: str
    x0: float
    y0: float
    color: int


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


def _assert_lines(value: object) -> list[PdfLine]:
    """Validate and return extracted PDF text lines."""
    if not isinstance(value, list):
        raise AssertionError('Expected lines list')
    lines: list[PdfLine] = []
    for item in value:
        if not isinstance(item, dict):
            raise AssertionError('Expected line entry dict')
        text = item.get('text')
        x0 = item.get('x0')
        y0 = item.get('y0')
        if not isinstance(text, str):
            raise AssertionError('Expected line text string')
        if not isinstance(x0, float):
            raise AssertionError('Expected line x0 float')
        if not isinstance(y0, float):
            raise AssertionError('Expected line y0 float')
        lines.append(PdfLine(text=text, x0=x0, y0=y0))
    return lines


def _assert_spans(value: object) -> list[PdfSpan]:
    """Validate and return extracted PDF text spans."""
    if not isinstance(value, list):
        raise AssertionError('Expected spans list')
    spans: list[PdfSpan] = []
    for item in value:
        if not isinstance(item, dict):
            raise AssertionError('Expected span entry dict')
        text = item.get('text')
        x0 = item.get('x0')
        y0 = item.get('y0')
        color = item.get('color')
        if not isinstance(text, str):
            raise AssertionError('Expected span text string')
        if not isinstance(x0, float):
            raise AssertionError('Expected span x0 float')
        if not isinstance(y0, float):
            raise AssertionError('Expected span y0 float')
        if not isinstance(color, int):
            raise AssertionError('Expected span color int')
        spans.append(PdfSpan(text=text, x0=x0, y0=y0, color=color))
    return spans


def _line_starting_with(lines: list[PdfLine], prefix: str) -> PdfLine:
    """Return the first extracted line starting with one prefix."""
    for line in lines:
        if line.text.startswith(prefix):
            return line
    raise AssertionError(f'No line starts with {prefix!r}')


def _span_by_text(spans: list[PdfSpan], text: str) -> PdfSpan:
    """Return the first extracted span with one exact text value."""
    for span in spans:
        if span.text == text:
            return span
    raise AssertionError(f'No span matches {text!r}')


def _spans_by_text(spans: list[PdfSpan], text: str) -> list[PdfSpan]:
    """Return all extracted spans with one exact text value."""
    return [span for span in spans if span.text == text]


def _inspect_pdf(file_name: str) -> PdfInspection:
    """Inspect one PDF file in a subprocess using the PyMuPDF API.

    The subprocess keeps current PyMuPDF import-time SWIG deprecation
    warnings out of the main pytest process while still exercising the
    actual PDF reader used by these tests.
    """
    script = """
import json
import sys
# Import inside the subprocess: current PyMuPDF builds in this venv still
# emit SWIG-layer DeprecationWarnings at import time.
import pymupdf
with pymupdf.open(sys.argv[1]) as pdf_document:
    page = pdf_document[0]
    links = page.get_links()
    text_dict = page.get_text('dict')
    lines = []
    spans = []
    for block in text_dict['blocks']:
        for line in block.get('lines', []):
            line_spans = line.get('spans', [])
            if not line_spans:
                continue
            lines.append({
                'text': ''.join(span['text'] for span in line_spans),
                'x0': float(line['bbox'][0]),
                'y0': float(line['bbox'][1]),
            })
            for span in line_spans:
                spans.append({
                    'text': span['text'],
                    'x0': float(span['bbox'][0]),
                    'y0': float(span['bbox'][1]),
                    'color': int(span.get('color', 0)),
                })
    payload = {
        'page_text': page.get_text(),
        'metadata_title': pdf_document.metadata.get('title', ''),
        'toc': pdf_document.get_toc(),
        'link_uri': links[0].get('uri') if links else None,
        'page_width': page.rect.width,
        'page_height': page.rect.height,
        'lines': lines,
        'spans': spans,
    }
print(json.dumps(payload))
"""
    result = subprocess.run(
        [sys.executable, '-c', script, file_name],
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
    lines = payload.get('lines')
    spans = payload.get('spans')
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
        lines=_assert_lines(lines),
        spans=_assert_spans(spans),
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
        assert '•' in inspection.page_text
        assert 'Bullet one' in inspection.page_text
        assert '1.' in inspection.page_text
        assert 'Number one' in inspection.page_text
        assert '1.1.' in inspection.page_text
        assert 'Nested number' in inspection.page_text
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
        assert inspection.toc == [[1, 'My Title', 1],
                                  [2, 'Heading One', 1],
                                  [3, 'Heading Three', 1],
                                  [4, 'Heading Three', 1]]
        assert inspection.link_uri == 'http://example.com'
        assert abs(inspection.page_width - 419.5276) < 0.01
        assert abs(inspection.page_height - 595.2756) < 0.01


def test_list_indentation_and_wrapping() -> None:
    """Test list-marker nesting and wrapped-line indentation."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.pdf')
        with MultiFormatPdf(file_name=file_name) as formatter:
            formatter.new_bullet_item(
                text='Top bullet item. ' + ('BulletWrap ' * 18))
            formatter.new_bullet_item(level=2, text='Nested bullet item.')
            formatter.new_numbered_point_item(
                text='Top numbered item. ' + ('NumberWrap ' * 18),
                level=1,
            )
            formatter.new_numbered_point_item(
                text='Nested numbered item.',
                level=2,
            )
        inspection = _inspect_pdf(file_name)
    bullet_markers = _spans_by_text(inspection.spans, '•')
    assert len(bullet_markers) == 2
    top_bullet_marker = min(bullet_markers, key=lambda span: span.y0)
    nested_bullet_marker = max(bullet_markers, key=lambda span: span.y0)
    top_bullet_line = _line_starting_with(inspection.lines, 'Top bullet item.')
    bullet_wrap_line = _line_starting_with(inspection.lines, 'BulletWrap')
    nested_bullet_text = _span_by_text(inspection.spans, 'Nested bullet item.')
    top_number_marker = _span_by_text(inspection.spans, '1.')
    nested_number_marker = _span_by_text(inspection.spans, '1.1.')
    top_number_line = _line_starting_with(
        inspection.lines,
        'Top numbered item.',
    )
    number_wrap_line = _line_starting_with(inspection.lines, 'NumberWrap')
    nested_number_text = _span_by_text(
        inspection.spans,
        'Nested numbered item.',
    )
    assert nested_bullet_marker.x0 > top_bullet_marker.x0
    assert nested_bullet_text.x0 > top_bullet_line.x0
    assert abs(bullet_wrap_line.x0 - top_bullet_line.x0) < 0.01
    assert nested_number_marker.x0 > top_number_marker.x0
    assert nested_number_text.x0 > top_number_line.x0
    assert abs(number_wrap_line.x0 - top_number_line.x0) < 0.01


def test_table_spacing_and_url_color() -> None:
    """Test visible table spacing and URL text color."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.pdf')
        with MultiFormatPdf(file_name=file_name) as formatter:
            formatter.new_table(first_row=['Top table'], bold=True)
            formatter.add_table_row(row=['First table bottom'])
            formatter.new_table(first_row=['Second table'], bold=True)
            formatter.add_table_row(row=['Second table bottom'])
            formatter.new_paragraph(text='Visible link: ')
            formatter.add_url(url='http://example.com', text='Link text')
        inspection = _inspect_pdf(file_name)
    first_bottom = _span_by_text(inspection.spans, 'First table bottom')
    second_top = _span_by_text(inspection.spans, 'Second table')
    link_text = _span_by_text(inspection.spans, 'Link text')
    assert second_top.y0 - first_bottom.y0 > 18.0
    assert link_text.color == 1728436
