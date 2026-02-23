#! /usr/local/bin/python3
"""Plain text format class."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from copy import deepcopy
from typing import Optional, Callable
from mformat.mformat_textbased import MultiFormatTextBased
from mformat.mformat_state import MultiFormatState, Formatting
from mformat.mformat import FormatterDescriptor
from mformat.plain_text_table import get_plain_text_table, \
    get_rst_like_spec, TableAlignment
from mformat.underline_text import underline_text, UnderlineSpec


_UNDERLINE_SPEC: list[UnderlineSpec] = [
    UnderlineSpec(pattern='*', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='=', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='-', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='"', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='\'"', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='\'', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern=None, empty_lines_between=1, empty_lines_after=1),
]


class MultiFormatTxt(MultiFormatTextBased):
    """Plain text format class."""

    MAX_LINE_LENGTH = 80

    def __init__(self, file_name: str, url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]] = None,
                 line_length: int = 79):
        """Initialize the MultiFormatTxt class.

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
        assert line_length and isinstance(line_length, int)
        if line_length <= 10:
            raise ValueError('Line length must be greater than 10, '
                             f'got {line_length}')
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback)
        self.txt_heading: str = ''
        self.txt_table: list[list[str]] = []
        self.line_length = line_length

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.txt'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='txt', mandatory_args=[],
                                   optional_args=['line_length'])

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        self._empty_line_before()
        self._reset_line_state()

    def _start_block_quote(self) -> None:
        """Start a block quote."""
        assert self.file is not None
        self._empty_line_before()
        self._reset_line_state(continuation_indent='> ')
        self.file.write('> ')
        self._current_column = 2

    def _end_block_quote(self) -> None:
        """End a block quote."""
        self._write_line_break()
        self._reset_line_state()

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        self._write_line_break()

    def _start_heading(self, level: int) -> None:
        """Start a heading."""
        self.txt_heading = ''

    def _end_heading(self, level: int) -> None:
        """End a heading."""
        assert self.file is not None
        self._empty_line_before()
        assert level > 0
        uspec = _UNDERLINE_SPEC[-1]
        if level <= len(_UNDERLINE_SPEC):
            uspec = _UNDERLINE_SPEC[level-1]
        lines = underline_text(text=self.txt_heading,
                               underline_spec=uspec,
                               max_line_length=self.line_length)
        for line in lines:
            self.file.write(line + '\n')

    def _write_text(self,  # pylint: disable=unused-argument,too-many-arguments,too-many-positional-arguments # noqa: E501
                    text: str, state: MultiFormatState,
                    formatting: Formatting) -> None:
        """Write text into current item (paragraph, bullet list item, etc.).

        Args:
            text: The text to write into the current item.
            state: The state of the current item.
            formatting: The formatting of the text.
        """
        assert self.file is not None
        if state == MultiFormatState.HEADING:
            self.txt_heading += text
            return
        self._wrap_and_write(text, self.line_length)

    def _write_url(self,  # pylint: disable=unused-argument,too-many-arguments,too-many-positional-arguments # noqa: E501
                   url: str, text: Optional[str],
                   state: MultiFormatState,
                   formatting: Formatting) -> None:
        """Write a URL into current item (paragraph, bullet list item...)."""
        assert self.file is not None
        formatted_url = f'{text} {url}' if text else url
        if state == MultiFormatState.HEADING:
            self.txt_heading += formatted_url
            return
        self._wrap_and_write(formatted_url, self.line_length)

    def _write_code_in_text(self, text: str,
                            state: MultiFormatState) -> None:
        """Write code into current item (paragraph, bullet list item...)."""
        assert self.file is not None
        assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        if state == MultiFormatState.HEADING:
            self.txt_heading += text
            return
        self._wrap_and_write_atomic(text, self.line_length)

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list."""
        _ = level  # pylint: disable=unused-variable

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list."""
        _ = level  # pylint: disable=unused-variable

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item."""
        self._start_bullet_item_common(level=level,
                                       empty_line_before=False,
                                       marker='- ')

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list."""
        _ = level  # pylint: disable=unused-variable

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list."""
        _ = level  # pylint: disable=unused-variable

    def _start_numbered_item(self, level: int, num: int,
                             full_number: str) -> None:
        """Start a numbered list item."""
        self._start_numbered_item_common(level=level, num=num,
                                         full_number=full_number,
                                         empty_line_before=False)

    def _start_code_block(self, programming_language: Optional[str]) -> None:
        """Start a code block."""
        assert self.file is not None
        self._empty_line_before()
        prl = programming_language + ' ' if programming_language else ''
        self.file.write(f'----- Start of {prl}code block -----\n')

    def _end_code_block(self, programming_language: Optional[str]) -> None:
        """End a code block."""
        assert self.file is not None
        prl = programming_language + ' ' if programming_language else ''
        self.file.write(f'\n------ End of {prl}code block ------\n')

    def _write_code_block(self, text: str,
                          programming_language: Optional[str]) -> None:
        """Write a code block."""
        _ = programming_language  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write(text)

    def _start_table(self, num_columns: int) -> None:
        """Start a table."""
        assert self.file is not None
        assert isinstance(num_columns, int)
        self._empty_line_before()
        self.txt_table = []

    def _end_table(self, num_columns: int, num_rows: int) -> None:
        """End a table."""
        assert self.file is not None
        assert isinstance(num_columns, int)
        assert isinstance(num_rows, int)
        alignment = TableAlignment.CENTER_BUT_DIGITS_RIGHT
        lines = get_plain_text_table(data=self.txt_table,
                                     border_spec=get_rst_like_spec(),
                                     alignment=alignment,
                                     max_line_length=self.line_length)
        for line in lines:
            self.file.write(line + '\n')
        self.txt_table = []

    def _write_table_first_row(self, first_row: list[str],
                               formatting: Formatting) -> None:
        """Write the first row of a table."""
        assert self.file is not None
        assert self.table is not None
        self.txt_table.append(deepcopy(first_row))

    def _write_table_row(self, row: list[str],
                         formatting: Formatting, row_number: int) -> None:
        """Write a row of a table."""
        assert self.table is not None
        if len(row) != self.table.number_of_columns:
            msg = f'Row {row_number} has {len(row)} columns, but '
            msg += f'table has {self.table.number_of_columns} columns.'
            raise ValueError(msg)
        # Make a copy of the row to avoid modifying the original row.
        self.txt_table.append(deepcopy(row))

    def _encode_text(self, text: str) -> str:
        """No encoding for plain text."""
        return text
