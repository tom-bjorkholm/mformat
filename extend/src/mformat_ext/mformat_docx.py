#! /usr/local/bin/python3
"""Extension of the MultiFormat class for DOCX files."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Optional, Callable
from docx import Document
from docx.document import Document as DocumentObject
from docx.text.paragraph import Paragraph
from docx.shared import Inches
from mformat.mformat import FormatterDescriptor, MultiFormat, \
    MultiFormatState


class MultiFormatDocx(MultiFormat):
    """Extension of the MultiFormat class for DOCX files."""

    def __init__(self, file_name: str, url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]] = None):
        """Initialize the MultiFormatDocx class.

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
        self.doc: DocumentObject = Document()
        self.current_paragraph: Optional[Paragraph] = None
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.docx'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='docx', mandatory_args=[],
                                   optional_args=[])

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        self.doc.save(self.file_name)

    def _close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        if self.state == MultiFormatState.EMPTY:
            return
        self.doc.save(self.file_name)

    def _write_file_prefix(self) -> None:
        """Write the file prefix.

        For DOCX files, this is a no-op since the document
        structure is handled by python-docx.
        """

    def _write_file_suffix(self) -> None:
        """Write the file suffix.

        For DOCX files, this is a no-op since the document
        structure is handled by python-docx.
        """

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        self.current_paragraph = self.doc.add_paragraph()

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        self.current_paragraph = None

    def _start_heading(self, level: int) -> None:
        """Start a heading.

        Args:
            level: The level of the heading (1-9).
        """
        self.current_paragraph = self.doc.add_heading(level=level)

    def _end_heading(self, level: int) -> None:
        """End a heading.

        Args:
            level: The level of the heading (1-9).
        """
        self.current_paragraph = None

    def _write_text(self, text: str, state: MultiFormatState,
                    bold: bool, italic: bool) -> None:
        """Write text into current item (paragraph, bullet list item, etc.).

        Args:
            text: The text to write into the current item.
            state: The state of the current item.
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        if self.current_paragraph is None:
            raise RuntimeError('No current paragraph to write text into')
        run = self.current_paragraph.add_run(text)
        if bold:
            run.bold = True
        if italic:
            run.italic = True

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   bold: bool, italic: bool) -> None:
        """Write a URL into current item (paragraph, bullet list item, etc.).

        Args:
            url: The URL to write into the current item.
            text: The text to display for the URL.
            state: The state of the current item.
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """  # pylint: disable=too-many-arguments,too-many-positional-arguments
        if self.current_paragraph is None:
            raise RuntimeError('No current paragraph to write URL into')
        if not text:
            text = url
        # Note: python-docx doesn't have direct hyperlink
        # support, so we add it as styled text
        run = self.current_paragraph.add_run(text)
        if bold:
            run.bold = True
        if italic:
            run.italic = True
        run.font.color.rgb = None  # Use default color
        # Note: For proper hyperlinks in docx, we would need to manipulate
        # the underlying XML. For now, we just format the text.

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list.

        Args:
            level: The level of the bullet list (1-9).
        """
        assert isinstance(level, int)
        # In python-docx, lists are created by setting paragraph styles
        # No explicit list start/end is needed

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list.

        Args:
            level: The level of the bullet list (1-9).
        """
        assert isinstance(level, int)
        # In python-docx, lists are created by setting paragraph styles
        # No explicit list start/end is needed

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item.

        Args:
            level: The level of the bullet item (1-9).
        """
        assert isinstance(level, int)
        self.current_paragraph = self.doc.add_paragraph(style='List Bullet')
        # Set the indentation level for nested lists
        if level > 1:
            self.current_paragraph.paragraph_format.left_indent = \
                Inches(0.5 * (level - 1))

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item.

        Args:
            level: The level of the bullet item (1-9).
        """
        assert isinstance(level, int)
        self.current_paragraph = None

    def _start_numeric_list(self, level: int) -> None:
        """Start a numeric list.

        Args:
            level: The level of the numeric list (1-9).
        """
        assert isinstance(level, int)
        # In python-docx, lists are created by setting paragraph styles
        # No explicit list start/end is needed

    def _end_numeric_list(self, level: int) -> None:
        """End a numeric list.

        Args:
            level: The level of the numeric list (1-9).
        """
        assert isinstance(level, int)
        # In python-docx, lists are created by setting paragraph styles
        # No explicit list start/end is needed

    def _start_numeric_item(self, level: int, num: int) -> None:
        """Start a numeric item.

        Args:
            level: The level of the numeric item (1-9).
            num: The number of the item.
        """
        assert isinstance(level, int)
        assert isinstance(num, int)
        self.current_paragraph = self.doc.add_paragraph(
            style='List Number')
        # Set the indentation level for nested lists
        if level > 1:
            self.current_paragraph.paragraph_format.left_indent = \
                Inches(0.5 * (level - 1))

    def _end_numeric_item(self, level: int, num: int) -> None:
        """End a numeric item.

        Args:
            level: The level of the numeric item (1-9).
            num: The number of the item.
        """
        assert isinstance(level, int)
        assert isinstance(num, int)
        self.current_paragraph = None

    def _start_table(self, num_columns: int) -> None:
        """Start a table.

        Args:
            num_columns: The number of columns in the table.
        """
        assert isinstance(num_columns, int)
        # In python-docx, we need to know the number of rows in advance
        # We'll handle this by creating a table with 1 row initially
        # and adding rows as needed
        # Note: This is a placeholder - actual table creation happens
        # in _write_table_first_row

    def _end_table(self, num_columns: int, num_rows: int) -> None:
        """End a table.

        Args:
            num_columns: The number of columns in the table.
            num_rows: The number of rows in the table.
        """
        assert isinstance(num_columns, int)
        assert isinstance(num_rows, int)
        # No action needed - table is already complete

    def _write_table_first_row(self, first_row: list[str],
                               bold: bool, italic: bool) -> None:
        """Write the first row of a table.

        Args:
            first_row: The first row of the table.
            bold: If True, the text in each cell is bold.
            italic: If True, the text in each cell is italic.
        """
        assert isinstance(first_row, list)
        assert isinstance(bold, bool)
        assert isinstance(italic, bool)
        # Create the table with the first row
        table = self.doc.add_table(rows=1, cols=len(first_row))
        table.style = 'Table Grid'
        # Fill in the first row
        for idx, cell_text in enumerate(first_row):
            cell = table.rows[0].cells[idx]
            para = cell.paragraphs[0]
            run = para.add_run(cell_text)
            if bold:
                run.bold = True
            if italic:
                run.italic = True

    def _write_table_row(self, row: list[str], bold: bool, italic: bool,
                         row_number: int) -> None:
        """Write a row of a table.

        Args:
            row: The row to add to the table.
            bold: If True, the text in each cell is bold.
            italic: If True, the text in each cell is italic.
            row_number: The row number (0-based).
        """
        assert isinstance(row, list)
        assert isinstance(bold, bool)
        assert isinstance(italic, bool)
        assert isinstance(row_number, int)
        # Get the last table in the document
        table = self.doc.tables[-1]
        # Add a new row
        new_row = table.add_row()  # type: ignore[no-untyped-call]
        # Fill in the row
        for idx, cell_text in enumerate(row):
            cell = new_row.cells[idx]
            para = cell.paragraphs[0]
            run = para.add_run(cell_text)
            if bold:
                run.bold = True
            if italic:
                run.italic = True

    def _start_code_block(self, programming_language: Optional[str]) -> None:
        """Start a code block.

        Args:
            programming_language: The programming language of the code block.
        """
        assert programming_language is None or \
            isinstance(programming_language, str)
        # Create a paragraph with a code/verbatim style
        # python-docx doesn't have a built-in code style,
        # so we'll use 'No Spacing' style and monospace font
        self.current_paragraph = self.doc.add_paragraph()
        self.current_paragraph.style = 'No Spacing'

    def _end_code_block(self, programming_language: Optional[str]) -> None:
        """End a code block.

        Args:
            programming_language: The programming language of the code block.
        """
        assert programming_language is None or \
            isinstance(programming_language, str)
        self.current_paragraph = None

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
        if self.current_paragraph is None:
            raise RuntimeError('No current paragraph to write code into')
        run = self.current_paragraph.add_run(text)
        # Set monospace font
        run.font.name = 'Courier New'
