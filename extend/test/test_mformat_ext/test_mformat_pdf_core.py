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
from unittest.mock import Mock, call
import pytest
from reportlab.platypus import (  # type: ignore[import-untyped]
    Paragraph, Preformatted)
from mformat_ext.mformat_pdf import (MultiFormatPdf, _PendingTextBlock,
                                     _PdfDocumentTemplate,
                                     _PdfHeadingParagraph)
from mformat.mformat import FormatterDescriptor, TableInformation
from mformat.mformat_state import Formatting, MultiFormatState
from mformat.paper_size import PaperSize


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
    font: str


class PdfInspection(NamedTuple):
    """Selected first-page PDF details extracted in a subprocess."""

    page_text: str
    metadata_title: str
    toc: list[list[int | str]]
    link_uri: str | None
    page_width: float
    page_height: float
    lines: list[PdfLine]
    spans: list[PdfSpan]


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
        font = item.get('font')
        if not isinstance(text, str):
            raise AssertionError('Expected span text string')
        if not isinstance(x0, float):
            raise AssertionError('Expected span x0 float')
        if not isinstance(y0, float):
            raise AssertionError('Expected span y0 float')
        if not isinstance(color, int):
            raise AssertionError('Expected span color int')
        if not isinstance(font, str):
            raise AssertionError('Expected span font string')
        spans.append(PdfSpan(text=text, x0=x0, y0=y0, color=color,
                             font=font))
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


def _assert_has_error_message(exception: BaseException) -> None:
    """Assert that one exception carries a non-empty message."""
    assert str(exception) != ''


def _heading_paragraph(formatter: MultiFormatPdf,
                       level: int,
                       text: str,
                       plain_text: str | None = None) -> _PdfHeadingParagraph:
    """Create one heading flowable for direct outline tests."""
    actual_plain_text = text if plain_text is None else plain_text
    return _PdfHeadingParagraph(text=text, style=formatter.pdf_styles.body,
                                heading_level=level,
                                plain_text=actual_plain_text)


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
                    'font': str(span.get('font', '')),
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


def test_init_rejects_non_string_title(tmp_path: Path) -> None:
    """Test that title validation rejects non-string values."""
    with pytest.raises(ValueError) as exc:
        _ = MultiFormatPdf(file_name=tmp_path / 'test.pdf',
                           title=1)  # type: ignore[arg-type]
    _assert_has_error_message(exc.value)


@pytest.mark.parametrize(
    'paper_size, expected_width, expected_height',
    [
        (PaperSize.A3, 841.8897637795277, 1190.5511811023623),
        (PaperSize.A4, 595.2755905511812, 841.8897637795277),
        (PaperSize.A5, 419.52755905511816, 595.2755905511812),
        (PaperSize.LEGAL, 612.0, 1008.0),
        (PaperSize.LETTER, 612.0, 792.0),
    ],
)
def test_paper_size_sets_expected_page_size(
        tmp_path: Path,
        paper_size: PaperSize,
        expected_width: float,
        expected_height: float) -> None:
    """Test that each supported paper size maps to the expected page size."""
    formatter = MultiFormatPdf(file_name=tmp_path / f'{paper_size.name}.pdf',
                               paper_size=paper_size)
    assert formatter.page_size == pytest.approx(
        (expected_width, expected_height))


def test_pending_text_block_accumulates_markup_and_plain_text(
        tmp_path: Path) -> None:
    """Test that pending blocks keep markup and plain text in sync."""
    formatter = MultiFormatPdf(file_name=tmp_path / 'test.pdf')
    block = _PendingTextBlock(style=formatter.pdf_styles.body,
                              bullet_text='*',
                              heading_level=2)
    assert block.markup_text() == '&#160;'
    assert block.plain_text() == ''
    block.append_fragment(markup='<b>Hello</b>', plain_text='Hello')
    block.append_fragment(markup=' &amp; bye', plain_text=' & bye')
    assert block.markup_text() == '<b>Hello</b> &amp; bye'
    assert block.plain_text() == 'Hello & bye'


def test_escape_helpers_and_formatting() -> None:
    """Test escaping and formatting helper methods."""
    # pylint: disable=protected-access
    assert MultiFormatPdf._escape_text('A < B & C\nline 2') == \
        'A &lt; B &amp; C<br/>line 2'
    assert MultiFormatPdf._escape_attribute('"quote" & <tag>') == \
        '&quot;quote&quot; &amp; &lt;tag&gt;'
    assert MultiFormatPdf._apply_formatting(
        'x',
        Formatting(bold=True, italic=True),
    ) == '<i><b>x</b></i>'


def test_heading_style_clamps_to_supported_levels(tmp_path: Path) -> None:
    """Test that visible heading styles clamp to the supported range."""
    # pylint: disable=protected-access
    formatter = MultiFormatPdf(file_name=tmp_path / 'test.pdf')
    assert formatter._heading_style(0) is formatter.pdf_styles.headings[1]
    assert formatter._heading_style(7) is formatter.pdf_styles.headings[6]


def test_require_current_block_raises_when_missing(tmp_path: Path) -> None:
    """Test that missing current blocks raise a runtime error."""
    # pylint: disable=protected-access
    formatter = MultiFormatPdf(file_name=tmp_path / 'test.pdf')
    with pytest.raises(RuntimeError) as exc:
        formatter._require_current_block('writing text')
    _assert_has_error_message(exc.value)


def test_append_current_block_handles_empty_paragraph_and_heading(
        tmp_path: Path) -> None:
    """Test empty pending blocks become valid paragraph flowables."""
    # pylint: disable=protected-access
    formatter = MultiFormatPdf(file_name=tmp_path / 'test.pdf')
    formatter._start_paragraph()
    formatter._append_current_block()
    assert formatter.current_block is None
    assert len(formatter.story) == 1
    paragraph = formatter.story[0]
    assert isinstance(paragraph, Paragraph)
    assert paragraph.text == '&#160;'
    formatter._start_heading(level=9)
    formatter._append_current_block()
    assert formatter.current_block is None
    assert len(formatter.story) == 2
    heading = formatter.story[1]
    assert isinstance(heading, _PdfHeadingParagraph)
    assert heading.text == '&#160;'
    assert heading.heading_level == 9
    assert heading.plain_text == ''
    assert heading.style is formatter.pdf_styles.headings[6]


def test_append_current_block_is_noop_when_missing(tmp_path: Path) -> None:
    """Test appending without a current block leaves the story unchanged."""
    # pylint: disable=protected-access
    formatter = MultiFormatPdf(file_name=tmp_path / 'test.pdf')
    formatter._append_current_block()
    assert formatter.current_block is None
    assert not formatter.story


def test_table_column_widths_respect_weights_and_minimums(
        tmp_path: Path) -> None:
    """Test table column widths use proportional weights and minimum one."""
    # pylint: disable=protected-access
    formatter = MultiFormatPdf(file_name=tmp_path / 'test.pdf')
    formatter.table = TableInformation()
    assert formatter._table_column_widths() == []
    formatter.table.column_widths = [0, 2, 4]
    widths = formatter._table_column_widths()
    available_width = formatter.page_size[0] - (2 * 54.0)
    assert sum(widths) == pytest.approx(available_width)
    assert widths[1] == pytest.approx(widths[0] * 2)
    assert widths[2] == pytest.approx(widths[0] * 4)


def test_write_code_block_appends_preformatted_flowable(
        tmp_path: Path) -> None:
    """Test that code blocks become Preformatted flowables."""
    formatter = MultiFormatPdf(file_name=tmp_path / 'test.pdf')
    formatter.write_code_block(text='x = 1\ny = 2')
    assert formatter.state == MultiFormatState.PARAGRAPH_END
    assert len(formatter.story) == 1
    code_block = formatter.story[0]
    assert isinstance(code_block, Preformatted)
    assert code_block.style.fontName == 'Courier'


def test_document_template_registers_outline_root_and_missing_levels(
        tmp_path: Path) -> None:
    """Test direct outline registration for skipped heading levels."""
    formatter = MultiFormatPdf(file_name=tmp_path / 'style.pdf')
    template = _PdfDocumentTemplate(
        file_name=str(tmp_path / 'outline.pdf'),
        title='Meta title',
        outline_root_title='Root title',
        pagesize=formatter.page_size,
    )
    canvas = Mock()
    setattr(template, 'canv', canvas)
    template.afterFlowable(_heading_paragraph(formatter, 1, 'Heading one'))
    template.afterFlowable(_heading_paragraph(formatter, 4, 'Heading four'))
    assert canvas.bookmarkPage.call_args_list == [
        call('heading-0'),
        call('heading-1'),
        call('heading-2'),
        call('heading-3'),
        call('heading-4'),
    ]
    assert canvas.addOutlineEntry.call_args_list == [
        call('Root title', 'heading-0', level=0),
        call('Heading one', 'heading-1', level=1),
        call('Heading four', 'heading-2', level=2),
        call('Heading four', 'heading-3', level=3),
        call('Heading four', 'heading-4', level=4),
    ]


def test_document_template_ignores_non_headings_and_blank_titles(
        tmp_path: Path) -> None:
    """Test direct outline registration ignores non-visible titles."""
    formatter = MultiFormatPdf(file_name=tmp_path / 'style.pdf')
    template = _PdfDocumentTemplate(
        file_name=str(tmp_path / 'outline.pdf'),
        title='Meta title',
        outline_root_title='Root title',
        pagesize=formatter.page_size,
    )
    canvas = Mock()
    setattr(template, 'canv', canvas)
    template.afterFlowable(
        Paragraph('Not a heading', formatter.pdf_styles.body))
    template.afterFlowable(
        _heading_paragraph(formatter, 2, 'Ignored', plain_text='   '))
    canvas.bookmarkPage.assert_not_called()
    canvas.addOutlineEntry.assert_not_called()


def test_empty_context_manager_does_not_create_pdf_file(
        tmp_path: Path) -> None:
    """Test that empty documents do not create a PDF file on close."""
    file_name = tmp_path / 'empty.pdf'
    formatter = MultiFormatPdf(file_name=file_name)
    with formatter:
        pass
    assert formatter.state == MultiFormatState.CLOSED
    assert not file_name.exists()


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


def test_inline_formatting_and_code_use_expected_fonts() -> None:
    """Test visible inline formatting and code fonts in the generated PDF."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.pdf')
        with MultiFormatPdf(file_name=file_name) as formatter:
            formatter.new_paragraph(text='Before')
            formatter.add_text(text=' both', bold=True, italic=True)
            formatter.add_text(text=' code')
            formatter.add_code_in_text('X()')
            formatter.write_code_block(text='x = 1\ny = 2')
        inspection = _inspect_pdf(file_name)
        formatted_span = _span_by_text(inspection.spans, ' both')
        inline_code_span = _span_by_text(inspection.spans, ' X()')
        code_block_span = _span_by_text(inspection.spans, 'x = 1')
        assert formatted_span.font == 'Helvetica-BoldOblique'
        assert inline_code_span.font == 'Courier'
        assert code_block_span.font == 'Courier'


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


def test_blank_title_uses_default_outline_root_and_missing_levels() -> None:
    """Test fallback outline title and gap-filling outline levels."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.pdf')
        with MultiFormatPdf(file_name=file_name, title='   ') as formatter:
            formatter.new_heading(level=2, text='Heading Two')
            formatter.new_heading(level=4, text='Heading Four')
        inspection = _inspect_pdf(file_name)
        assert inspection.toc == [[1, 'Document', 1],
                                  [2, 'Heading Two', 1],
                                  [3, 'Heading Two', 1],
                                  [4, 'Heading Four', 1],
                                  [5, 'Heading Four', 1]]


def test_url_as_text_writes_visible_text_without_link() -> None:
    """Test that url_as_text writes plain text without a clickable link."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.pdf')
        with MultiFormatPdf(file_name=file_name,
                            url_as_text=True) as formatter:
            formatter.new_paragraph(text='Read')
            formatter.add_url(url='http://example.com', text='Example')
        inspection = _inspect_pdf(file_name)
        assert 'Read Example http://example.com' in inspection.page_text
        assert inspection.link_uri is None


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
