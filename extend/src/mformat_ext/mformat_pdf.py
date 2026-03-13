#! /usr/local/bin/python3
"""Extension of the MultiFormat class for PDF files."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from html import escape
from typing import Optional, Callable, NamedTuple
from reportlab.lib import colors  # type: ignore[import-untyped]
from reportlab.lib.pagesizes import (  # type: ignore[import-untyped]
    A3, A4, A5, LEGAL, LETTER)
from reportlab.lib.styles import (  # type: ignore[import-untyped]
    ParagraphStyle, getSampleStyleSheet)
from reportlab.pdfbase import pdfmetrics  # type: ignore[import-untyped]
from reportlab.platypus import (  # type: ignore[import-untyped]
    Paragraph, Preformatted, SimpleDocTemplate, Table, TableStyle)
from mformat.mformat import FormatterDescriptor, MultiFormat, PathLike
from mformat.mformat_state import MultiFormatState, Formatting
from mformat.paper_size import PaperSize

_PDF_PAPER_SIZE: dict[PaperSize, tuple[float, float]] = {
    PaperSize.A3: A3,
    PaperSize.A4: A4,
    PaperSize.A5: A5,
    PaperSize.LEGAL: LEGAL,
    PaperSize.LETTER: LETTER,
}
"""Paper size mapping for PDF documents."""

_PAGE_MARGIN = 54.0
_BULLET_TEXT = '\u2022'
_DEFAULT_OUTLINE_ROOT_TITLE = 'Document'
_LIST_LEVEL_INDENT = 18.0
_LIST_MARKER_GAP = 8.0
_MAX_HEADING_STYLE_LEVEL = 6
_TABLE_VERTICAL_SPACE = 6.0
_URL_COLOR = '#1a5fb4'

# Some information sources for PDF generation with reportlab:
# https://pypi.org/project/reportlab/
# https://docs.reportlab.com/reportlab/userguide/ch1_intro/
# https://docs.reportlab.com/reportlab/userguide/ch4_pdffeatures/
# https://docs.reportlab.com/reportlab/userguide/ch6_paragraphs/
# https://docs.reportlab.com/reportlab/userguide/ch7_tables/
# https://docs.reportlab.com/reportlab/userguide/ch9_other_useful_flowables/


class PdfStyles(NamedTuple):
    """Styles used for PDF output."""

    body: ParagraphStyle
    block_quote: ParagraphStyle
    code_block: ParagraphStyle
    table_cell: ParagraphStyle
    list_base: ParagraphStyle
    headings: dict[int, ParagraphStyle]


class _PendingTextBlock:  # pylint: disable=too-few-public-methods
    """State for one text-like block being accumulated."""

    def __init__(self, style: ParagraphStyle,
                 bullet_text: Optional[str] = None,
                 heading_level: Optional[int] = None) -> None:
        """Initialize one pending text block."""
        self.style = style
        self.bullet_text = bullet_text
        self.heading_level = heading_level
        self.fragments: list[str] = []
        self.plain_text_parts: list[str] = []

    def append_fragment(self, markup: str, plain_text: str) -> None:
        """Append one markup fragment and its plain-text counterpart."""
        self.fragments.append(markup)
        self.plain_text_parts.append(plain_text)

    def markup_text(self) -> str:
        """Return accumulated markup text for the block."""
        if self.fragments:
            return ''.join(self.fragments)
        return '&#160;'

    def plain_text(self) -> str:
        """Return accumulated plain text for the block."""
        return ''.join(self.plain_text_parts)


class _PdfHeadingParagraph(Paragraph):  # type: ignore[misc]
    """Paragraph carrying outline metadata for one heading."""

    def __init__(self, text: str, style: ParagraphStyle,
                 heading_level: int, plain_text: str) -> None:
        """Initialize one outline-aware heading paragraph."""
        super().__init__(text=text, style=style)
        self.heading_level = heading_level
        self.plain_text = plain_text


class _PdfDocumentTemplate(SimpleDocTemplate):  # type: ignore[misc]
    """Simple document template that registers outline entries."""

    def __init__(self, file_name: str, title: Optional[str],
                 outline_root_title: str,
                 pagesize: tuple[float, float]) -> None:
        """Initialize one PDF document template."""
        kwargs: dict[str, object] = {
            'pagesize': pagesize,
            'leftMargin': _PAGE_MARGIN,
            'rightMargin': _PAGE_MARGIN,
            'topMargin': _PAGE_MARGIN,
            'bottomMargin': _PAGE_MARGIN,
        }
        if title is not None:
            kwargs['title'] = title
        super().__init__(file_name, **kwargs)
        self.outline_root_title = outline_root_title
        self._bookmark_counter = 0
        self._last_outline_level = -1
        self._outline_root_created = False

    def _next_bookmark_key(self) -> str:
        """Return a unique bookmark key."""
        key = f'heading-{self._bookmark_counter}'
        self._bookmark_counter += 1
        return key

    def afterFlowable(self, flowable: object) -> None:
        """Register a bookmark and outline entry after rendering heading."""
        if not isinstance(flowable, _PdfHeadingParagraph):
            return
        title = flowable.plain_text.strip()
        if not title:
            return
        if not self._outline_root_created:
            bookmark_key = self._next_bookmark_key()
            self.canv.bookmarkPage(bookmark_key)
            self.canv.addOutlineEntry(self.outline_root_title, bookmark_key,
                                      level=0)
            self._outline_root_created = True
            self._last_outline_level = 0
        target_level = max(flowable.heading_level, 1)
        outline_levels = [target_level]
        if target_level > self._last_outline_level + 1:
            outline_levels = list(range(self._last_outline_level + 1,
                                        target_level + 1))
        for outline_level in outline_levels:
            bookmark_key = self._next_bookmark_key()
            self.canv.bookmarkPage(bookmark_key)
            self.canv.addOutlineEntry(title, bookmark_key,
                                      level=outline_level)
        self._last_outline_level = target_level


class MultiFormatPdf(MultiFormat):
    """Extension of the MultiFormat class for PDF output files."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, file_name: PathLike, url_as_text: bool = False,
                 paper_size: PaperSize = PaperSize.A4,
                 title: Optional[str] = None,
                 file_exists_callback: Optional[Callable[[str], None]] = None):
        """Initialize the MultiFormatPdf class.

        Args:
            file_name: The name of the file to write to.
            url_as_text: Format URLs as text not clickable URLs.
            paper_size: Paper size for the document.
                        (Default is A4 paper size.)
            title: PDF document metadata title.
                   This is not rendered as visible document content.
            file_exists_callback: A callback function to call if the file
                                  already exists. Return to allow the file to
                                  be overwritten. Raise an exception to
                                  prevent the file from being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
        """
        if title is not None and not isinstance(title, str):
            raise ValueError('title must be a string')
        self.paper_size = paper_size
        self.title = title
        self.page_size = _PDF_PAPER_SIZE[paper_size]
        self.story: list[object] = []
        self.pdf_styles = self._create_pdf_styles()
        self.current_block: Optional[_PendingTextBlock] = None
        self.current_table_rows: list[list[Paragraph]] = []
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.pdf'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='pdf', mandatory_args=[],
                                   optional_args=['paper_size', 'title'])

    @staticmethod
    def _escape_text(text: str) -> str:
        """Escape plain text for ReportLab paragraph markup."""
        return escape(text, quote=False).replace('\n', '<br/>')

    @staticmethod
    def _escape_attribute(text: str) -> str:
        """Escape text for use in ReportLab markup attributes."""
        return escape(text, quote=True)

    @staticmethod
    def _apply_formatting(markup: str, formatting: Formatting) -> str:
        """Wrap markup in bold and italic tags."""
        if formatting.bold:
            markup = f'<b>{markup}</b>'
        if formatting.italic:
            markup = f'<i>{markup}</i>'
        return markup

    def _create_pdf_styles(self) -> PdfStyles:
        """Create paragraph styles used by the PDF backend."""
        sample_styles = getSampleStyleSheet()
        body_style = ParagraphStyle(
            'pdf-body',
            parent=sample_styles['BodyText'], spaceBefore=0, spaceAfter=10)
        block_quote_style = ParagraphStyle(
            'pdf-block-quote',
            parent=body_style, leftIndent=18, rightIndent=18,
            borderPadding=6, backColor=colors.HexColor('#e8e8e8'),
            spaceBefore=6, spaceAfter=6)
        code_block_style = ParagraphStyle(
            'pdf-code-block',
            parent=body_style, fontName='Courier', fontSize=8.5, leading=10,
            leftIndent=18, rightIndent=18, borderPadding=6,
            backColor=colors.HexColor('#f0f0f0'), spaceBefore=6, spaceAfter=6)
        table_cell_style = ParagraphStyle(
            'pdf-table-cell', parent=body_style, spaceBefore=0, spaceAfter=0)
        list_base_style = ParagraphStyle(
            'pdf-list-base', parent=body_style, spaceBefore=1, spaceAfter=1)
        headings: dict[int, ParagraphStyle] = {}
        heading_sizes = {
            1: 18,
            2: 16,
            3: 14,
            4: 12,
            5: 11,
            6: 10,
        }
        for level, size in heading_sizes.items():
            headings[level] = ParagraphStyle(
                f'pdf-heading-{level}', parent=body_style,
                fontName='Helvetica-Bold', fontSize=size, leading=size + 4,
                spaceBefore=14 if level == 1 else 10,
                spaceAfter=6)
        return PdfStyles(body=body_style,
                         block_quote=block_quote_style,
                         code_block=code_block_style,
                         table_cell=table_cell_style,
                         list_base=list_base_style,
                         headings=headings)

    def _heading_style(self, level: int) -> ParagraphStyle:
        """Return a visible heading style for a heading level."""
        bounded_level = max(1, min(level, _MAX_HEADING_STYLE_LEVEL))
        return self.pdf_styles.headings[bounded_level]

    def _list_style(self, level: int, marker_text: str) -> ParagraphStyle:
        """Return a paragraph style for one list item."""
        bounded_level = max(1, level)
        base_indent = _LIST_LEVEL_INDENT * (bounded_level - 1)
        marker_width = pdfmetrics.stringWidth(
            marker_text,
            self.pdf_styles.list_base.fontName,
            self.pdf_styles.list_base.fontSize,
        )
        return ParagraphStyle(
            f'pdf-list-{bounded_level}-{marker_text}',
            parent=self.pdf_styles.list_base,
            bulletFontName=self.pdf_styles.list_base.fontName,
            bulletFontSize=self.pdf_styles.list_base.fontSize,
            bulletIndent=base_indent,
            leftIndent=base_indent + marker_width + _LIST_MARKER_GAP,
            firstLineIndent=0,
        )

    def _require_current_block(self, operation: str) -> _PendingTextBlock:
        """Return current pending block or raise a helpful error."""
        if self.current_block is None:
            raise RuntimeError(f'No current block for {operation}')
        return self.current_block

    def _append_current_block(self) -> None:
        """Finalize the current block and append it to the story."""
        if self.current_block is None:
            return
        block = self.current_block
        if block.heading_level is not None:
            self.story.append(
                _PdfHeadingParagraph(
                    text=block.markup_text(),
                    style=block.style,
                    heading_level=block.heading_level,
                    plain_text=block.plain_text(),
                ))
        else:
            self.story.append(
                Paragraph(block.markup_text(), block.style,
                          bulletText=block.bullet_text))
        self.current_block = None

    def _table_cell_paragraph(self, text: str,
                              formatting: Formatting) -> Paragraph:
        """Create one table-cell paragraph."""
        markup = self._escape_text(text)
        markup = self._apply_formatting(markup, formatting)
        return Paragraph(markup, self.pdf_styles.table_cell)

    def _table_column_widths(self) -> list[float]:
        """Calculate proportional column widths for the current table."""
        assert self.table is not None
        if not self.table.column_widths:
            return []
        weights = [max(width, 1) for width in self.table.column_widths]
        available_width = self.page_size[0] - (2 * _PAGE_MARGIN)
        total_weight = sum(weights)
        return [available_width * weight / total_weight
                for weight in weights]

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """

    def _close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        if self.state == MultiFormatState.EMPTY:
            return
        pdf_document = _PdfDocumentTemplate(
            file_name=self.file_name,
            title=self.title,
            outline_root_title=(
                self.title.strip()
                if self.title is not None and self.title.strip()
                else _DEFAULT_OUTLINE_ROOT_TITLE
            ),
            pagesize=self.page_size,
        )
        pdf_document.build(self.story)

    def _write_file_prefix(self) -> None:
        """Write the file prefix.

        For PDF files, this is a no-op since the document structure is
        handled by ReportLab.
        """

    def _write_file_suffix(self) -> None:
        """Write the file suffix.

        For PDF files, this is a no-op since the document structure is
        handled by ReportLab.
        """

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        self.current_block = _PendingTextBlock(style=self.pdf_styles.body)

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        self._append_current_block()

    def _start_block_quote(self) -> None:
        """Start a block quote."""
        self.current_block = _PendingTextBlock(
            style=self.pdf_styles.block_quote)

    def _end_block_quote(self) -> None:
        """End a block quote."""
        self._append_current_block()

    def _start_heading(self, level: int) -> None:
        """Start a heading."""
        self.current_block = _PendingTextBlock(
            style=self._heading_style(level),
            heading_level=level,
        )

    def _end_heading(self, level: int) -> None:
        """End a heading."""
        _ = level
        self._append_current_block()

    def _write_text(self, text: str, state: MultiFormatState,
                    formatting: Formatting) -> None:
        """Write text into current item (paragraph, list item, etc.)."""
        _ = state
        block = self._require_current_block('writing text')
        markup = self._apply_formatting(self._escape_text(text),
                                        formatting)
        block.append_fragment(markup=markup, plain_text=text)

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   formatting: Formatting) -> None:
        """Write a URL into current item (paragraph, list item, etc.)."""
        _ = state
        block = self._require_current_block('writing URL')
        display_text = url if text is None else text
        markup = (f'<font color="{_URL_COLOR}"><u><a '
                  f'href="{self._escape_attribute(url)}">'
                  f'{self._escape_text(display_text)}</a></u></font>')
        markup = self._apply_formatting(markup, formatting)
        block.append_fragment(markup=markup, plain_text=display_text)

    def _write_code_in_text(self, text: str,
                            state: MultiFormatState) -> None:
        """Write code into current item (paragraph, list item, etc.)."""
        _ = state
        block = self._require_current_block('writing inline code')
        markup = f'<font face="Courier">{self._escape_text(text)}</font>'
        block.append_fragment(markup=markup, plain_text=text)

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list."""
        _ = level

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list."""
        _ = level

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item."""
        self.current_block = _PendingTextBlock(
            style=self._list_style(level, _BULLET_TEXT),
            bullet_text=_BULLET_TEXT)

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item."""
        _ = level
        self._append_current_block()

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list."""
        _ = level

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list."""
        _ = level

    def _start_numbered_item(self, level: int, num: int,
                             full_number: str) -> None:
        """Start a numbered item."""
        _ = num
        self.current_block = _PendingTextBlock(
            style=self._list_style(level, full_number),
            bullet_text=full_number)

    def _end_numbered_item(self, level: int, num: int) -> None:
        """End a numbered item."""
        _ = level
        _ = num
        self._append_current_block()

    def _start_table(self, num_columns: int) -> None:
        """Start a table."""
        _ = num_columns
        self.current_table_rows = []

    def _end_table(self, num_columns: int, num_rows: int) -> None:
        """End a table."""
        _ = num_columns
        _ = num_rows
        pdf_table = Table(self.current_table_rows,
                          colWidths=self._table_column_widths(), repeatRows=1)
        pdf_table.spaceBefore = _TABLE_VERTICAL_SPACE
        pdf_table.spaceAfter = _TABLE_VERTICAL_SPACE
        pdf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        self.story.append(pdf_table)
        self.current_table_rows = []

    def _write_table_first_row(self, first_row: list[str],
                               formatting: Formatting) -> None:
        """Write the first row of the table."""
        self.current_table_rows.append([
            self._table_cell_paragraph(text=cell, formatting=formatting)
            for cell in first_row
        ])

    def _write_table_row(self, row: list[str], formatting: Formatting,
                         row_number: int) -> None:
        """Write a row of the table."""
        _ = row_number
        self.current_table_rows.append([
            self._table_cell_paragraph(text=cell, formatting=formatting)
            for cell in row
        ])

    def _start_code_block(self, programming_language: Optional[str]) -> None:
        """Start a code block."""
        _ = programming_language

    def _end_code_block(self, programming_language: Optional[str]) -> None:
        """End a code block."""
        _ = programming_language

    def _write_code_block(self, text: str,
                          programming_language: Optional[str]) -> None:
        """Write a code block."""
        _ = programming_language
        self.story.append(Preformatted(text, self.pdf_styles.code_block))

    def _encode_text(self, text: str) -> str:
        """Return text unchanged for object-based PDF output."""
        return text
