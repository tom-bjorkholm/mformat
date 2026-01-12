#! /usr/local/bin/python3
"""Extension of the MultiFormat class for DOCX files."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Optional, Callable, Union
from odfdo import Document, Paragraph, Header, Table, Row, Cell, \
    Link, List, ListItem, Style
from mformat.mformat import FormatterDescriptor, MultiFormat
from mformat.mformat_state import MultiFormatState, Formatting


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
        """
        self.doc: Document = Document('text')
        self.doc.set_language(lang)
        self.current_paragraph: Optional[Paragraph] = None
        self.odt_table: Optional[Table] = None
        self.odt_tablenumber: int = 1
        self.odt_list: list[List] = []
        self.odt_listitem: Optional[ListItem] = None
        bold_style = Style(name='bold', family='text')
        bold_style.set_attribute('fo:font-weight', 'bold')
        self.doc.insert_style(bold_style)
        italic_style = Style(name='italic', family='text')
        italic_style.set_attribute('fo:font-style', 'italic')
        self.doc.insert_style(italic_style)
        bold_italic_style = Style(name='bold-italic', family='text')
        bold_italic_style.set_attribute('fo:font-weight', 'bold')
        bold_italic_style.set_attribute('fo:font-style', 'italic')
        self.doc.insert_style(bold_italic_style)
        code_style = Style(name='code', family='text')
        code_style.set_attribute('fo:font-family', 'monospace')
        self.doc.insert_style(code_style)
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback)

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

    @staticmethod
    def _apply_formatting(paragraph: Union[Paragraph, ListItem],
                          formatting: Formatting, text: str) -> None:
        """Apply formatting to a paragraph or list item."""
        assert paragraph is not None
        assert isinstance(paragraph, (Paragraph, ListItem))
        style = MultiFormatOdt._style_name_from_formatting(formatting)
        if style:
            total_length = len(paragraph.text)
            text_length = len(text)
            paragraph.set_span(style=style, offset=total_length - text_length,
                               length=text_length)

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
            self.current_paragraph.text += text
            self._apply_formatting(self.current_paragraph, formatting, text)
        elif self.state == MultiFormatState.BULLET_LIST_ITEM:
            assert self.odt_listitem is not None
            self.odt_listitem.text += text
            self._apply_formatting(self.odt_listitem, formatting, text)
        elif self.state == MultiFormatState.NUMBERED_LIST_ITEM:
            assert self.odt_listitem is not None
            self.odt_listitem.text += text
            self._apply_formatting(self.odt_listitem, formatting, text)
        else:
            raise RuntimeError(f'Unexpected state: {self.state.name}')

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   formatting: Formatting) -> None:
        """Write a URL into current item (paragraph, bullet list item, etc.).

        Args:
            url: The URL to write into the current item.
            text: The text to display for the URL.
            state: The state of the current item.
            formatting: The formatting of the text.
        """  # pylint: disable=too-many-arguments,too-many-positional-arguments
        if self.current_paragraph is None:
            raise RuntimeError('No current paragraph to write URL into')
        if not text:
            text = url
        lnk = Link(url=url, text=text)
        if isinstance(self.current_paragraph, ListItem):
            return  # TODO: Figure out how to add formatting to list items
        assert isinstance(self.current_paragraph, Paragraph)
        style = self._style_name_from_formatting(formatting)
        if style:
            lnk.style = style
        self.current_paragraph.append(lnk)

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list.

        Args:
            level: The level of the bullet list (1-9).
        """
        assert isinstance(level, int)
        self.odt_list.append(List(style='bullet'))
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
        self.doc.body.append(self.odt_list[-1])
        self.odt_list.pop()

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item.

        Args:
            level: The level of the bullet item (1-9).
        """
        assert isinstance(level, int)
        self.odt_listitem = ListItem()
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
        self.odt_list.append(List(style='number'))
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
        self.odt_listitem = ListItem()
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
        self._write_table_row(first_row, formatting, 1)

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
            style = self._style_name_from_formatting(formatting)
            if style:
                cell.style = style
            table_row.append(cell)
        self.odt_table.append(table_row)

    @staticmethod
    def _style_name_from_formatting(formatting: Formatting) -> str:
        """Get the style name from the formatting."""
        assert isinstance(formatting, Formatting)
        style = ''
        if formatting.bold:
            style = 'bold'
            if formatting.italic:
                style += '-italic'
        elif formatting.italic:
            style = 'italic'
        return style

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
            para = Paragraph()
            para.text = line
            para.set_span(style='code', offset=0, length=len(line))
            self.doc.body.append(para)

    def _encode_text(self, text: str) -> str:
        """Encode text (escape special characters)."""
        # No encoding needed for DOCX
        return text
