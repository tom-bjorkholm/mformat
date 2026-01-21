#! /usr/local/bin/python3
"""Extension of the MultiFormat class for DOCX files."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Optional, Callable, NamedTuple
from odfdo import Document, Paragraph, Header, Table, Row, Cell, \
    Link, List, ListItem, Style, Span
from mformat.mformat import FormatterDescriptor, MultiFormat
from mformat.mformat_state import MultiFormatState, Formatting


class OdtStyles(NamedTuple):
    """Styles for ODT files."""

    text_styles: dict[str, Style]
    font_styles: dict[str, Style]
    paragraph_styles: dict[str, Style]
    bold: Style
    italic: Style
    bold_italic: Style
    code: Style


class MultiFormatOdt(MultiFormat):
    """Extension of the MultiFormat class for ODT files."""

    def __init__(self, file_name: str, url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]] = None,
                 lang: str = 'en-UK'):
        """Initialize the MultiFormatOdt class.

        Args:
            file_name: The name of the file to write to.
            url_as_text: Format URLs as text not clickable URLs.
            file_exists_callback: A callback function to call if the file
                                  already exists. Return to allow the file to
                                  be overwritten. Raise an exception to prevent
                                  the file from being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
            lang: The language of the document.
        """
        self.doc: Document = Document('text')
        self.doc.set_language(lang)
        self.current_paragraph: Optional[Paragraph] = None
        self.odt_table: Optional[Table] = None
        self.odt_tablenumber: int = 1
        self.odt_list: list[List] = []
        self.odt_listitem: Optional[ListItem] = None
        self.odt_styles: OdtStyles = self._create_odt_styles()
        self._insert_odt_styles()
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback)

    def _insert_odt_styles(self) -> None:
        """Insert the ODT styles into the document."""
        for style in self.odt_styles.text_styles.values():
            self.doc.insert_style(style)
        for style in self.odt_styles.font_styles.values():
            self.doc.insert_style(style)
        for style in self.odt_styles.paragraph_styles.values():
            self.doc.insert_style(style)

    def _create_odt_styles(self) -> OdtStyles:
        """Create the ODT styles needed for documents."""
        text_styles: dict[str, Style] = {}
        font_styles: dict[str, Style] = {}
        paragraph_styles: dict[str, Style] = {}
        bold_style = Style(name='bold', family='text',
                           display_name='bold', area='text',
                           bold=True, italic=False)
        text_styles['bold'] = bold_style
        italic_style = Style(name='italic', family='text',
                             display_name='italic', area='text',
                             italic=True, bold=False)
        text_styles['italic'] = italic_style
        bold_italic_style = Style(name='bold-italic', family='text',
                                  display_name='bold-italic', area='text',
                                  bold=True, italic=True)
        text_styles['bold-italic'] = bold_italic_style
        code_style = Style(name='code', family='font-face',
                           display_name='code',
                           font_family='monospace', font_name='courier new',
                           bold=False, italic=False)
        font_styles['code'] = code_style
        return OdtStyles(text_styles=text_styles, font_styles=font_styles,
                         paragraph_styles=paragraph_styles, bold=bold_style,
                         italic=italic_style, bold_italic=bold_italic_style,
                         code=code_style)

    @staticmethod
    def _style_name_from_formatting(formatting: Formatting) -> str:
        """Get the style name from the formatting."""
        assert isinstance(formatting, Formatting)
        style_name = ''
        if formatting.bold:
            style_name = 'bold'
            if formatting.italic:
                style_name += '-italic'
        elif formatting.italic:
            style_name = 'italic'
        return style_name

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.odt'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='odt', mandatory_args=[],
                                   optional_args=['lang'])

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        # No need to open the file - it is created when the document is saved

    def _close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        if self.state == MultiFormatState.EMPTY:
            return
        self.doc.save(self.file_name, pretty=True)

    def _write_file_prefix(self) -> None:
        """Write the file prefix.

        For ODT files, this is a no-op since the document
        structure is handled by odfdo.
        """

    def _write_file_suffix(self) -> None:
        """Write the file suffix.

        For ODT files, this is a no-op since the document
        structure is handled by odfdo.
        """

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        self.current_paragraph = Paragraph()

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        if self.current_paragraph is not None:
            self.doc.body.append(self.current_paragraph)
        self.current_paragraph = None

    def _start_heading(self, level: int) -> None:
        """Start a heading.

        Args:
            level: The level of the heading (1-9).
        """
        self.current_paragraph = Header(level=level)

    def _end_heading(self, level: int) -> None:
        """End a heading.

        Args:
            level: The level of the heading (1-9).
        """
        if self.current_paragraph is not None:
            self.doc.body.append(self.current_paragraph)
        self.current_paragraph = None

    def _formatted_write(self, paragraph: Paragraph,
                         formatting: Formatting, text: str) -> None:
        """Apply formatting to a paragraph or list item.

        In ODF/XML, paragraph.text holds text before any child elements,
        and each element's tail holds text after that element. To maintain
        correct text order when mixing formatted and unformatted text, we:
        - Use Span elements for formatted text (appended as children)
        - For unformatted text: add to paragraph.text if no children exist,
          otherwise add to the tail of the last child element.
        """
        assert paragraph is not None
        assert isinstance(paragraph, Paragraph)
        style = self._style_name_from_formatting(formatting)
        if style:
            # Formatted text: create a span with the style and append it
            span = Span(text=text, style=style)
            paragraph.append(span)
        else:
            # Unformatted text: add to correct position
            if len(paragraph.children) == 0:
                # No children yet, add to paragraph.text
                if paragraph.text:
                    paragraph.text += text
                else:
                    paragraph.text = text
            else:
                # Has children, add to the tail of the last child
                last_child = paragraph.children[-1]
                if last_child.tail:
                    last_child.tail += text
                else:
                    last_child.tail = text

    def _write_text(self, text: str, state: MultiFormatState,
                    formatting: Formatting) -> None:
        """Write text into current item (paragraph, bullet list item, etc.).

        Args:
            text: The text to write into the current item.
            state: The state of the current item.
            formatting: The formatting of the text.
        """
        if self.state in (MultiFormatState.PARAGRAPH,
                          MultiFormatState.HEADING):
            assert self.current_paragraph is not None
            self._formatted_write(self.current_paragraph, formatting, text)
        elif self.state in (MultiFormatState.BULLET_LIST_ITEM,
                            MultiFormatState.NUMBERED_LIST_ITEM):
            assert self.odt_listitem is not None
            assert isinstance(self.odt_listitem.children[-1], Paragraph)
            self._formatted_write(self.odt_listitem.children[-1],
                                  formatting, text)
        else:
            raise RuntimeError(f'Unexpected state: {self.state.name} for '
                               f'writing text: {text}')

    def _impl_write_url(self, paragraph: Paragraph,
                        url: str, text: Optional[str],
                        formatting: Formatting) -> None:
        """Implement the writing of a URL into a paragraph or list item."""
        assert paragraph is not None
        assert isinstance(paragraph, Paragraph)
        assert isinstance(formatting, Formatting)
        if not text:
            text = url
        lnk = Link(url=url, text=text)
        style = self._style_name_from_formatting(formatting)
        if style:
            lnk.style = style
        paragraph.append(lnk)

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   formatting: Formatting) -> None:
        """Write a URL into current item (paragraph, bullet list item, etc.).

        Args:
            url: The URL to write into the current item.
            text: The text to display for the URL.
            state: The state of the current item.
            formatting: The formatting of the text.
        """
        assert state == self.state
        if self.state in (MultiFormatState.PARAGRAPH,
                          MultiFormatState.HEADING):
            assert self.current_paragraph is not None
            self._impl_write_url(self.current_paragraph, url, text, formatting)
        elif self.state in (MultiFormatState.BULLET_LIST_ITEM,
                            MultiFormatState.NUMBERED_LIST_ITEM):
            assert self.odt_listitem is not None
            assert isinstance(self.odt_listitem.children[-1], Paragraph)
            self._impl_write_url(self.odt_listitem.children[-1],
                                 url, text, formatting)
        else:
            raise RuntimeError(f'Unexpected state: {self.state.name} for '
                               f'writing url: {url} text: {text}')

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list.

        Args:
            level: The level of the bullet list (1-9).
        """
        assert isinstance(level, int)
        self.odt_list.append(List(style='bullet-list'))
        self.current_paragraph = None

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list.

        Args:
            level: The level of the bullet list (1-9).
        """
        assert isinstance(level, int)
        if not self.odt_list or len(self.odt_list) != level:
            print(f'len(odt_list) = {len(self.odt_list)} for bullet list '
                  f'level = {level} state: {self.state.name}')
        assert self.odt_list and len(self.odt_list) == level
        if len(self.odt_list) > 1:
            self.odt_list[-2].append(self.odt_list[-1])
        else:
            self.doc.body.append(self.odt_list[-1])
        self.odt_list.pop()

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item.

        Args:
            level: The level of the bullet item (1-9).
        """
        assert isinstance(level, int)
        self.odt_listitem = ListItem()
        self.odt_listitem.text_content = Paragraph(text_or_element=Paragraph())
        assert self.odt_listitem is not None
        self.current_paragraph = None

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item.

        Args:
            level: The level of the bullet item (1-9).
        """
        assert isinstance(level, int)
        assert self.odt_listitem is not None
        self.odt_list[-1].append(self.odt_listitem)
        self.odt_listitem = None
        self.current_paragraph = None

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list.

        Args:
            level: The level of the numbered list (1-9).
        """
        assert isinstance(level, int)
        self.odt_list.append(List(style='numbered-list'))
        self.current_paragraph = None

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list.

        Args:
            level: The level of the numbered list (1-9).
        """
        assert isinstance(level, int)
        if not self.odt_list or len(self.odt_list) != level:
            print(f'len(odt_list) = {len(self.odt_list)} for numbered list '
                  f'level = {level} state: {self.state.name}')
        assert self.odt_list and len(self.odt_list) == level
        if len(self.odt_list) > 1:
            self.odt_list[-2].append(self.odt_list[-1])
        else:
            self.doc.body.append(self.odt_list[-1])
        self.odt_list.pop()

    def _start_numbered_item(self, level: int, num: int,
                             full_number: str) -> None:
        """Start a numbered item.

        Args:
            level: The level of the numbered item (1-9).
            num: The number of the item.
            full_number: The full number of the item including all levels.
        """
        assert isinstance(level, int)
        assert isinstance(num, int)
        assert isinstance(full_number, str)
        self.odt_listitem = ListItem(text_or_element=Paragraph())
        self.current_paragraph = None

    def _end_numbered_item(self, level: int, num: int) -> None:
        """End a numbered item.

        Args:
            level: The level of the numbered item (1-9).
            num: The number of the item.
        """
        assert isinstance(level, int)
        assert isinstance(num, int)
        assert self.odt_listitem is not None
        if not self.odt_list or len(self.odt_list) != level:
            print(f'len(odt_list) = {len(self.odt_list)} for numbered item '
                  f'level = {level} {num} state: {self.state.name}')
        assert self.odt_list and len(self.odt_list) == level
        self.odt_list[-1].append(self.odt_listitem)
        self.odt_listitem = None
        self.current_paragraph = None

    def _start_table(self, num_columns: int) -> None:
        """Start a table.

        Args:
            num_columns: The number of columns in the table.
        """
        assert isinstance(num_columns, int)
        assert num_columns > 0
        self.odt_table = Table(name=f'Table{self.odt_tablenumber}',
                               width=num_columns)
        self.odt_tablenumber += 1

    def _end_table(self, num_columns: int, num_rows: int) -> None:
        """End a table.

        Args:
            num_columns: The number of columns in the table.
            num_rows: The number of rows in the table.
        """
        assert isinstance(num_columns, int)
        assert isinstance(num_rows, int)
        assert self.odt_table is not None
        self.doc.body.append(self.odt_table)
        self.odt_table = None

    def _write_table_first_row(self, first_row: list[str],
                               formatting: Formatting) -> None:
        """Write the first row of a table.

        Args:
            first_row: The first row of the table.
            formatting: The formatting of the text in each cell.
        """
        assert isinstance(first_row, list)
        assert isinstance(formatting, Formatting)
        assert self.odt_table is not None
        self._write_table_row(first_row, formatting, 0)
        self.odt_table.delete_row(0)

    def _write_table_row(self, row: list[str], formatting: Formatting,
                         row_number: int) -> None:
        """Write a row of a table.

        Args:
            row: The row to add to the table.
            formatting: The formatting of the text in each cell.
            row_number: The row number (0-based).
        """
        assert isinstance(row, list)
        assert isinstance(formatting, Formatting)
        assert isinstance(row_number, int)
        assert self.odt_table is not None
        table_row = Row()
        for cell_text in row:
            cell = Cell(value=cell_text, cell_style='string')
            cell.style = self._style_name_from_formatting(formatting)
            table_row.append(cell)
        self.odt_table.append(table_row)

    def _start_code_block(self, programming_language: Optional[str]) -> None:
        """Start a code block.

        Args:
            programming_language: The programming language of the code block.
        """
        assert programming_language is None or \
            isinstance(programming_language, str)
        # No-op. Everything is done in _write_code_block.

    def _end_code_block(self, programming_language: Optional[str]) -> None:
        """End a code block.

        Args:
            programming_language: The programming language of the code block.
        """
        assert programming_language is None or \
            isinstance(programming_language, str)
        # No-op. Everyhing is done in _write_code_block.

    def _write_code_block(self, text: str,
                          programming_language: Optional[str]) -> None:
        """Write a code block.

        Args:
            text: The text to add to the code block.
            programming_language: The programming language of the code block.
        """
        assert isinstance(text, str)
        assert programming_language is None or \
            isinstance(programming_language, str)
        for line in text.split('\n'):
            para = Paragraph(text_or_element=line, style='code')
            self.doc.body.append(para)

    def _encode_text(self, text: str) -> str:
        """Encode text (escape special characters)."""
        # No encoding needed for DOCX
        return text
