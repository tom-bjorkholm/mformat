#! /usr/local/bin/python3
"""reStructuredText formatter implementation.

The formatter writes reStructuredText with line wrapping and indentation.
Headings use underline styles by heading level.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#
# pylint: disable=duplicate-code

from copy import deepcopy
from typing import Optional, Callable
from mformat.mformat_plaintextlike import MultiFormatPlainTextLike
from mformat.mformat_textbased import split_whitespace
from mformat.mformat_state import MultiFormatState, Formatting
from mformat.mformat import FormatterDescriptor, PathLike
from mformat.plain_text_table import get_plain_text_table, \
    get_rst_like_spec, TableAlignment, TableAlignmentSpec
from mformat.underline_text import underline_text, UnderlineSpec


_UNDERLINE_SPEC: list[UnderlineSpec] = [
    UnderlineSpec(pattern='=', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='-', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='~', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='^', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='"', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern="'", empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern='`', empty_lines_between=1, empty_lines_after=1),
    UnderlineSpec(pattern=':', empty_lines_between=1, empty_lines_after=1),
]


class MultiFormatRst(MultiFormatPlainTextLike):
    """reStructuredText formatter.

    Text is wrapped at word boundaries. Bold and italic formatting
    are rendered using reStructuredText inline markup. Tables are
    rendered as reStructuredText grid tables.
    """

    def __init__(self,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                 file_name: PathLike, url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]] = None,
                 character_encoding: str = 'utf-8',
                 line_length: int = 79,
                 table_max_line_length: Optional[int] = None,
                 table_alignment: TableAlignmentSpec = TableAlignment.LEFT):
        """Initialize the MultiFormatRst class.

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
            character_encoding: The character encoding to use.
                                Default is 'utf-8'. Keep it as default unless
                                you have a good specific reason to change it.
            line_length: The maximum length of a line.
                         Must be an integer greater than 10.
            table_max_line_length: The maximum length of a line when writing
                                   a table. If None, line_length is used.
                                   Must be at least 10 when provided.
            table_alignment: The alignment of cell values in tables.
                             Can be one alignment for all columns or
                             a list of per-column alignments.
        """
        assert line_length and isinstance(line_length, int)
        if line_length <= 10:
            raise ValueError('Line length must be greater than 10, '
                             f'got {line_length}')
        assert table_max_line_length is None or \
            isinstance(table_max_line_length, int)
        if table_max_line_length is not None and table_max_line_length < 10:
            raise ValueError('Table max line length must be at least 10, '
                             f'got {table_max_line_length}')
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback,
                         character_encoding=character_encoding)
        self.heading_text: str = ''
        self.table_rows: list[list[str]] = []
        self.line_length: int = line_length
        self.table_max_line_length: int = \
            line_length if table_max_line_length is None \
            else table_max_line_length
        self.table_alignment: TableAlignmentSpec = table_alignment

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.rst'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='reST', mandatory_args=[],
                                   optional_args=['line_length',
                                                  'table_max_line_length',
                                                  'table_alignment',
                                                  'character_encoding'])

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""

    def _start_heading(self, level: int) -> None:
        """Start a heading."""
        _ = level  # pylint: disable=unused-variable
        self.heading_text = ''

    def _end_heading(self, level: int) -> None:
        """End a heading."""
        assert self.file is not None
        self._empty_line_before()
        assert level > 0
        uspec = _UNDERLINE_SPEC[-1]
        if level <= len(_UNDERLINE_SPEC):
            uspec = _UNDERLINE_SPEC[level-1]
        heading_line_length = max(self.line_length, len(self.heading_text))
        lines = underline_text(text=self.heading_text,
                               underline_spec=uspec,
                               max_line_length=heading_line_length)
        for line in lines:
            self.file.write(line + '\n')

    @staticmethod
    def _format_text(text: str, formatting: Formatting) -> str:
        """Format text with bold and italic markup."""
        pre, stripped, post = split_whitespace(text)
        if not stripped:
            return text
        if formatting.bold:
            stripped = f'**{stripped}**'
        if formatting.italic:
            stripped = f'*{stripped}*'
        return pre + stripped + post

    def _write_text(self,  # pylint: disable=unused-argument,too-many-arguments,too-many-positional-arguments # noqa: E501
                    text: str, state: MultiFormatState,
                    formatting: Formatting) -> None:
        """Write text into current item (paragraph, bullet list item...)."""
        assert self.file is not None
        formatted_text = self._format_text(text, formatting)
        if state == MultiFormatState.HEADING:
            self.heading_text += formatted_text
            return
        self._wrap_and_write(formatted_text, self.line_length)

    def _write_url(self,  # pylint: disable=unused-argument,too-many-arguments,too-many-positional-arguments # noqa: E501
                   url: str, text: Optional[str],
                   state: MultiFormatState,
                   formatting: Formatting) -> None:
        """Write a URL into current item (paragraph, bullet list item...)."""
        assert self.file is not None
        label = text if text else url
        rst_url = f'`{label} <{url}>`_'
        formatted_url = self._format_text(rst_url, formatting)
        if state == MultiFormatState.HEADING:
            self.heading_text += formatted_url
            return
        self._wrap_and_write_atomic(formatted_url, self.line_length)

    def _write_code_in_text(self, text: str, state: MultiFormatState) -> None:
        """Write code into current item (paragraph, bullet list item...)."""
        assert self.file is not None
        assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        pre, stripped, post = split_whitespace(text)
        formatted_text = pre + f'``{stripped}``' + post
        if state == MultiFormatState.HEADING:
            self.heading_text += formatted_text
            return
        self._wrap_and_write_atomic(formatted_text, self.line_length)

    def _start_block_quote(self) -> None:
        """Start a block quote."""
        assert self.file is not None
        self._empty_line_before()
        self.file.write('  ')
        self._reset_line_state(continuation_indent='  ')
        self._current_column = 2

    def _end_block_quote(self) -> None:
        """End a block quote."""
        self._write_line_break()
        self._reset_line_state()

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list."""
        assert self.file is not None
        assert isinstance(level, int)
        if level == 1:
            self._empty_line_before()
            return
        self.file.write('\n')

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list."""
        assert self.file is not None
        assert isinstance(level, int)
        if level > 1:
            self._empty_line_before()

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item."""
        self._start_bullet_item_common(level=level, empty_line_before=False,
                                       marker='* ')

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list."""
        assert self.file is not None
        assert isinstance(level, int)
        if level == 1:
            self._empty_line_before()
            return
        self.file.write('\n')

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list."""
        assert self.file is not None
        assert isinstance(level, int)
        if level > 1:
            self._empty_line_before()

    def _start_numbered_item(self,  # pylint: disable=unused-argument
                             level: int, num: int,
                             full_number: str) -> None:
        """Start a numbered list item."""
        self._start_numbered_item_common(level=level, num=num,
                                         full_number=f'{num}.',
                                         empty_line_before=False)

    def _indent_for_level(self, level: int) -> str:
        """Get list indentation for reStructuredText output."""
        return 3 * (level - 1) * ' '

    def _start_code_block(self, programming_language: Optional[str]) -> None:
        """Start a code block."""
        assert self.file is not None
        self._empty_line_before()
        if programming_language is None:
            self.file.write('::\n\n')
            return
        self.file.write(f'.. code:: {programming_language}\n\n')

    def _end_code_block(self, programming_language: Optional[str]) -> None:
        """End a code block."""
        _ = programming_language  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\n')

    def _write_code_block(self, text: str,
                          programming_language: Optional[str]) -> None:
        """Write a code block."""
        _ = programming_language  # pylint: disable=unused-variable
        assert self.file is not None
        if not text:
            self.file.write('    \n')
            return
        for line in text.splitlines(keepends=True):
            self.file.write(f'    {line}')
        if not text.endswith('\n'):
            self.file.write('\n')

    def _start_table(self, num_columns: int) -> None:
        """Start a table."""
        assert self.file is not None
        assert isinstance(num_columns, int)
        self._empty_line_before()
        self.table_rows = []

    def _end_table(self, num_columns: int, num_rows: int) -> None:
        """End a table."""
        assert self.file is not None
        assert isinstance(num_columns, int)
        assert isinstance(num_rows, int)
        lines = get_plain_text_table(
            data=self.table_rows,
            border_spec=get_rst_like_spec(),
            alignment=self.table_alignment,
            max_line_length=self.table_max_line_length)
        for line in lines:
            self.file.write(line + '\n')
        self.table_rows = []

    def _write_table_first_row(self, first_row: list[str],
                               formatting: Formatting) -> None:
        """Write the first row of a table."""
        assert self.file is not None
        assert self.table is not None
        _ = formatting  # pylint: disable=unused-variable
        self.table_rows.append(deepcopy(first_row))

    def _write_table_row(self, row: list[str],
                         formatting: Formatting, row_number: int) -> None:
        """Write a row of a table."""
        assert self.table is not None
        _ = formatting  # pylint: disable=unused-variable
        if len(row) != self.table.number_of_columns:
            msg = f'Row {row_number} has {len(row)} columns, but '
            msg += f'table has {self.table.number_of_columns} columns.'
            raise ValueError(msg)
        self.table_rows.append(deepcopy(row))

    def _encode_text(self, text: str) -> str:
        """Encode text for reStructuredText output."""
        if not text:
            return text
        if self.state == MultiFormatState.CODE_BLOCK:
            return text
        result = text.replace('\\', '\\\\')
        result = result.replace('`', '\\`')
        result = result.replace('*', '\\*')
        result = result.replace('|', '\\|')
        return result
