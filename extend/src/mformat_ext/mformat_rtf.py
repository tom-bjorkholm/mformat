#! /usr/local/bin/python3
"""Extension of the MultiFormat class for Rich Text Format files."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from typing import Optional, Callable
from PyRTF.Elements import (  # type: ignore[import-untyped]
    Document,
    ParagraphStyle,
    TextStyle,
)
from PyRTF.PropertySets import (  # type: ignore[import-untyped]
    ParagraphPropertySet,
    StandardPaper,
    TabPropertySet,
    TextPropertySet,
)
from PyRTF.document.base import RawCode  # type: ignore[import-untyped]
from PyRTF.document.section import Section  # type: ignore[import-untyped]
from PyRTF.document.paragraph import (  # type: ignore[import-untyped]
    Paragraph,
    Table,
    Cell,
)
from PyRTF.document.character import Text  # type: ignore[import-untyped]
from mformat_ext.rtf_codec import (
    encode_rtf_field_instruction,
    encode_rtf_text,
)
from mformat.paper_size import PaperSize
from mformat.mformat import FormatterDescriptor, MultiFormat, PathLike
from mformat.mformat_state import MultiFormatState, Formatting

_MAX_HEADING_LEVEL = 6
_LIST_INDENT_TWIPS = 360
_MIN_COLUMN_WIDTH_TWIPS = 800
_NUMBER_CHAR_WIDTH_TWIPS = 120
_NUMBER_MARKER_PADDING_TWIPS = 120

#
# As some help to future maintainers, here are some URLs
# that may be useful:
# https://pypi.org/project/PyRTF3/
# https://github.com/xoviat/pyrtf
# https://www.biblioscape.com/rtf15_spec.htm
# Old and slightly outdated, but still useful:
# https://www.web2py.com/examples/static/sphinx/gluon/gluon.contrib.pyrtf.html
# https://github.com/grangier/pyrtf/blob/master/examples/examples.py
#


class MultiFormatRtf(MultiFormat):
    """Extension of the MultiFormat class for Rich Text Format files."""

    def __init__(self, file_name: PathLike, url_as_text: bool = False,
                 paper_size: PaperSize = PaperSize.A4,
                 file_exists_callback: Optional[Callable[[str], None]] = None):
        """Initialize the MultiFormatRtf class.

        Args:
            file_name: The name of the file to write to.
            url_as_text: Format URLs as text not clickable URLs.
            paper_size: Paper size for the document.
            file_exists_callback: A callback function to call if the file
                                  already exists. Return to allow the file to
                                  be overwritten. Raise an exception to prevent
                                  the file from being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
        """
        self.doc: Document = Document()
        self.section: Section = Section(
            paper=self._pyrtf_paper_size(paper_size=paper_size))
        self.doc.Sections.append(self.section)
        self.current_paragraph: Optional[Paragraph] = None
        self.current_table: Optional[Table] = None
        self.styles: dict[str, ParagraphStyle] = {}
        self.heading_styles: dict[int, ParagraphStyle] = {}
        self.list_styles: dict[tuple[bool, int], ParagraphStyle] = {}
        self._create_styles()
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.rtf'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='rtf', mandatory_args=[],
                                   optional_args=['paper_size'])

    @staticmethod
    def _pyrtf_paper_size(paper_size: PaperSize) -> object:
        """Map a PaperSize value to a PyRTF StandardPaper value."""
        return getattr(StandardPaper, paper_size.name)

    def _create_styles(self) -> None:
        """Create all paragraph styles used for RTF output."""
        fonts = self.doc.StyleSheet.Fonts
        paragraph_styles = self.doc.StyleSheet.ParagraphStyles
        self.styles['normal'] = paragraph_styles.Normal
        block_quote_style = ParagraphStyle(
            'Block Quote',
            TextStyle(TextPropertySet(font=fonts.Arial, size=22)),
            ParagraphPropertySet(space_before=60, space_after=60,
                                 left_indent=720, right_indent=720))
        paragraph_styles.append(block_quote_style)
        self.styles['block_quote'] = block_quote_style
        code_block_style = ParagraphStyle(
            'Code Block',
            TextStyle(TextPropertySet(font=fonts.CourierNew, size=20)),
            ParagraphPropertySet(space_before=60, space_after=60,
                                 left_indent=720, right_indent=720))
        paragraph_styles.append(code_block_style)
        self.styles['code_block'] = code_block_style
        heading_sizes = {1: 36, 2: 30, 3: 26, 4: 24, 5: 22, 6: 22}
        for level, size in heading_sizes.items():
            style = ParagraphStyle(
                f'Heading RTF {level}',
                TextStyle(TextPropertySet(font=fonts.Arial, size=size,
                                          bold=True)),
                ParagraphPropertySet(space_before=180, space_after=60))
            paragraph_styles.append(style)
            self.heading_styles[level] = style

    def _create_list_style(self, level: int,
                           bullet: bool) -> ParagraphStyle:
        """Create one list paragraph style for a given nesting level."""
        style_name = f'RTF {"Bullet" if bullet else "Numbered"} {level}'
        fonts = self.doc.StyleSheet.Fonts
        indent = _LIST_INDENT_TWIPS * max(level, 1)
        style = ParagraphStyle(
            style_name,
            TextStyle(TextPropertySet(font=fonts.Arial, size=22)),
            ParagraphPropertySet(space_before=20, space_after=20,
                                 tabs=[TabPropertySet(width=indent)],
                                 first_line_indent=-_LIST_INDENT_TWIPS,
                                 left_indent=indent))
        self.doc.StyleSheet.ParagraphStyles.append(style)
        return style

    def _get_heading_style(self, level: int) -> ParagraphStyle:
        """Get the heading style for a heading level."""
        bounded_level = max(1, min(level, _MAX_HEADING_LEVEL))
        return self.heading_styles[bounded_level]

    def _get_list_style(self, level: int, bullet: bool) -> ParagraphStyle:
        """Get a list style for level and type, creating it if needed."""
        key = (bullet, level)
        if key not in self.list_styles:
            self.list_styles[key] = self._create_list_style(level=level,
                                                            bullet=bullet)
        return self.list_styles[key]

    @staticmethod
    def _estimated_marker_width(full_number: str) -> int:
        """Estimate marker width in twips for one numbered-item marker."""
        return (len(full_number) * _NUMBER_CHAR_WIDTH_TWIPS) + \
            _NUMBER_MARKER_PADDING_TWIPS

    @staticmethod
    def _numbered_item_properties(level: int,
                                  full_number: str) -> ParagraphPropertySet:
        """Build paragraph properties for one numbered list item."""
        base_indent = _LIST_INDENT_TWIPS * max(level, 1)
        marker_width = MultiFormatRtf._estimated_marker_width(full_number)
        text_indent = max(base_indent, marker_width)
        return ParagraphPropertySet(
            tabs=[TabPropertySet(width=text_indent)],
            first_line_indent=-marker_width,
            left_indent=text_indent)

    def _start_new_paragraph(self,
                             style: Optional[ParagraphStyle] = None) -> None:
        """Create and append a new paragraph to the document."""
        paragraph_style = self.styles['normal'] if style is None else style
        paragraph = Paragraph(paragraph_style)
        self.section.append(paragraph)
        self.current_paragraph = paragraph

    def _require_current_paragraph(self, operation: str) -> Paragraph:
        """Get current paragraph or raise if no paragraph is active."""
        if self.current_paragraph is None:
            raise RuntimeError(f'No current paragraph for {operation}')
        return self.current_paragraph

    def _require_current_table(self, operation: str) -> Table:
        """Get current table or raise if no table is active."""
        if self.current_table is None:
            raise RuntimeError(f'No current table for {operation}')
        return self.current_table

    def _text_properties(self, formatting: Formatting,
                         code: bool = False) -> Optional[TextPropertySet]:
        """Build text property overrides for one text run."""
        if not formatting.bold and not formatting.italic and not code:
            return None
        text_props = TextPropertySet()
        if formatting.bold:
            text_props.bold = True
        if formatting.italic:
            text_props.italic = True
        if code:
            text_props.font = self.doc.StyleSheet.Fonts.CourierNew
        return text_props

    def _append_text(self, text: str, formatting: Formatting,
                     code: bool = False) -> None:
        """Append text to the current paragraph."""
        paragraph = self._require_current_paragraph('writing text')
        text_props = self._text_properties(formatting=formatting, code=code)
        if text_props is None:
            paragraph.append(text)
            return
        paragraph.append(Text(text, text_props))

    @staticmethod
    def _build_hyperlink_style_prefix(formatting: Formatting) -> str:
        """Build RTF style prefix to render links in blue with underline."""
        parts = [r'\ul\cf2']
        if formatting.bold:
            parts.append(r'\b')
        if formatting.italic:
            parts.append(r'\i')
        return ''.join(parts)

    def _build_hyperlink_field(self, url: str, text: str,
                               formatting: Formatting) -> str:
        """Build RTF field code for a hyperlink."""
        encoded_url = encode_rtf_field_instruction(url)
        style_prefix = self._build_hyperlink_style_prefix(formatting)
        return ('{\\field{\\*\\fldinst HYPERLINK "' + encoded_url + '"}'
                '{\\fldrslt {' + style_prefix + ' ' + text + '}}}')

    @staticmethod
    def _table_column_widths(num_columns: int) -> tuple[int, ...]:
        """Calculate equal fallback table column widths in twips."""
        if num_columns <= 0:
            raise RuntimeError('Table must have at least one column')
        width = _MIN_COLUMN_WIDTH_TWIPS
        return tuple(width for _ in range(num_columns))

    @staticmethod
    def _table_target_width(section: Section, num_columns: int) -> int:
        """Get target total table width in twips from page settings."""
        available = getattr(section, 'Width', 0)
        if not isinstance(available, int) or available <= 0:
            return _MIN_COLUMN_WIDTH_TWIPS * num_columns
        minimum = _MIN_COLUMN_WIDTH_TWIPS * num_columns
        return max(minimum, available)

    @staticmethod
    def _balance_column_widths(widths: list[int], target_total: int) -> None:
        """Adjust column widths so they fit the target total width."""
        if not widths:
            return
        current_total = sum(widths)
        if current_total < target_total:
            widths[-1] += target_total - current_total
            return
        overflow = current_total - target_total
        if overflow <= 0:
            return
        indices = sorted(range(len(widths)),
                         key=lambda idx: widths[idx], reverse=True)
        for index in indices:
            if overflow <= 0:
                break
            reducible = widths[index] - _MIN_COLUMN_WIDTH_TWIPS
            if reducible <= 0:
                continue
            reduce_by = min(reducible, overflow)
            widths[index] -= reduce_by
            overflow -= reduce_by

    @classmethod
    def _scaled_widths_from_char_widths(
            cls, char_widths: list[int], target_total: int) -> tuple[int, ...]:
        """Scale character-based widths into RTF twip column widths."""
        if not char_widths:
            return tuple()
        weighted_widths = [max(1, width + 2) for width in char_widths]
        weighted_total = sum(weighted_widths)
        widths = [max(_MIN_COLUMN_WIDTH_TWIPS,
                      (target_total * width) // weighted_total)
                  for width in weighted_widths]
        cls._balance_column_widths(widths=widths, target_total=target_total)
        return tuple(widths)

    def _dynamic_column_widths(self, num_columns: int) -> tuple[int, ...]:
        """Calculate dynamic column widths from table text lengths."""
        if self.table is None or len(self.table.column_widths) != num_columns:
            return self._table_column_widths(num_columns)
        target_total = self._table_target_width(section=self.section,
                                                num_columns=num_columns)
        widths = self._scaled_widths_from_char_widths(
            char_widths=self.table.column_widths,
            target_total=target_total)
        if widths:
            return widths
        return self._table_column_widths(num_columns)

    def _write_table_row_impl(self, row: list[str],
                              formatting: Formatting) -> None:
        """Write one table row into the current RTF table."""
        table = self._require_current_table('writing table row')
        table.SetColumnWidths(*self._dynamic_column_widths(len(row)))
        cells: list[Cell] = []
        for cell_text in row:
            paragraph = Paragraph(self.styles['normal'])
            text_props = self._text_properties(formatting=formatting)
            if text_props is None:
                paragraph.append(cell_text)
            else:
                paragraph.append(Text(cell_text, text_props))
            cells.append(Cell(paragraph))
        table.AddRow(*cells)

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
        self.doc.write(self.file_name)

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        self._start_new_paragraph()

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        self.current_paragraph = None

    def _start_block_quote(self) -> None:
        """Start a block quote paragraph."""
        self._start_new_paragraph(style=self.styles['block_quote'])

    def _end_block_quote(self) -> None:
        """End a block quote paragraph."""
        self.current_paragraph = None

    def _start_heading(self, level: int) -> None:
        """Start a heading paragraph.

        Args:
            level: The level of the heading (1-9).
        """
        self._start_new_paragraph(style=self._get_heading_style(level))

    def _end_heading(self, level: int) -> None:
        """End a heading paragraph.

        Args:
            level: The level of the heading (1-9).
        """
        _ = level
        self.current_paragraph = None

    def _write_text(self, text: str, state: MultiFormatState,
                    formatting: Formatting) -> None:
        """Write text into current item (paragraph, list item, etc.)."""
        _ = state
        self._append_text(text=text, formatting=formatting)

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   formatting: Formatting) -> None:
        """Write a URL into current item (paragraph, list item, etc.)."""
        _ = state
        paragraph = self._require_current_paragraph('writing url')
        display_text = text if text is not None else self._encode_text(url)
        paragraph.append(
            RawCode(self._build_hyperlink_field(url=url,
                                                text=display_text,
                                                formatting=formatting)))

    def _write_code_in_text(self, text: str,
                            state: MultiFormatState) -> None:
        """Write inline code into current item."""
        _ = state
        self._append_text(text=text, formatting=Formatting(False, False),
                          code=True)

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list.

        Args:
            level: The level of the bullet list.
        """
        _ = level

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list.

        Args:
            level: The level of the bullet list.
        """
        _ = level

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item.

        Args:
            level: The level of the bullet item.
        """
        style = self._get_list_style(level=level, bullet=True)
        self._start_new_paragraph(style=style)
        self._append_text(text=self._encode_text('•'),
                          formatting=Formatting(False, False))
        paragraph = self._require_current_paragraph('starting bullet item')
        paragraph.append(RawCode(r'\tab '))

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item.

        Args:
            level: The level of the bullet item.
        """
        _ = level
        self.current_paragraph = None

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list.

        Args:
            level: The level of the numbered list.
        """
        _ = level

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list.

        Args:
            level: The level of the numbered list.
        """
        _ = level

    def _start_numbered_item(self, level: int, num: int,
                             full_number: str) -> None:
        """Start a numbered item.

        Args:
            level: The level of the numbered item.
            num: The number at this level.
            full_number: The full number including parent levels.
        """
        _ = num
        style = self._get_list_style(level=level, bullet=False)
        self._start_new_paragraph(style=style)
        paragraph = self._require_current_paragraph('starting numbered item')
        paragraph.Properties = self._numbered_item_properties(
            level=level, full_number=full_number)
        self._append_text(text=self._encode_text(full_number),
                          formatting=Formatting(False, False))
        paragraph.append(RawCode(r'\tab '))

    def _end_numbered_item(self, level: int, num: int) -> None:
        """End a numbered item.

        Args:
            level: The level of the numbered item.
            num: The number at this level.
        """
        _ = level
        _ = num
        self.current_paragraph = None

    def _start_table(self, num_columns: int) -> None:
        """Start a table.

        Args:
            num_columns: The number of columns in the table.
        """
        self.section.append(Paragraph(self.styles['normal'], ''))
        self.current_table = Table(*self._dynamic_column_widths(num_columns))
        self.section.append(self.current_table)

    def _end_table(self, num_columns: int, num_rows: int) -> None:
        """End a table.

        Args:
            num_columns: The number of columns in the table.
            num_rows: The number of rows in the table.
        """
        _ = num_columns
        _ = num_rows
        self.current_table = None
        self.section.append(Paragraph(self.styles['normal'], ''))

    def _write_table_first_row(self, first_row: list[str],
                               formatting: Formatting) -> None:
        """Write the first row of a table.

        Args:
            first_row: The first row values.
            formatting: Formatting for the row.
        """
        self._write_table_row_impl(row=first_row, formatting=formatting)

    def _write_table_row(self, row: list[str], formatting: Formatting,
                         row_number: int) -> None:
        """Write a row of a table.

        Args:
            row: The row values.
            formatting: Formatting for the row.
            row_number: Row number in table.
        """
        _ = row_number
        self._write_table_row_impl(row=row, formatting=formatting)

    def _start_code_block(self, programming_language: Optional[str]) -> None:
        """Start a code block.

        Args:
            programming_language: The language of the code block.
        """
        _ = programming_language
        self._start_new_paragraph(style=self.styles['code_block'])

    def _end_code_block(self, programming_language: Optional[str]) -> None:
        """End a code block.

        Args:
            programming_language: The language of the code block.
        """
        _ = programming_language
        self.current_paragraph = None

    def _write_code_block(self, text: str,
                          programming_language: Optional[str]) -> None:
        """Write a code block.

        Args:
            text: The code text to write.
            programming_language: The language of the code block.
        """
        _ = programming_language
        paragraph = self._require_current_paragraph('writing code block')
        for index, line in enumerate(text.split('\n')):
            if index > 0:
                paragraph.append(RawCode(r'\line '))
            self._append_text(text=line, formatting=Formatting(False, False),
                              code=True)

    def _encode_text(self, text: str) -> str:
        """Encode text (escape special characters)."""
        return encode_rtf_text(text)
