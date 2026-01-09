#! /usr/local/bin/python3
"""Base class for all multi file format classes."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from types import TracebackType
from enum import IntEnum, auto
from typing import NamedTuple, Callable, Optional, TypedDict
import sys
import os


class FormatterDescriptor(NamedTuple):
    """Descriptor for a formatter."""

    name: str
    mandatory_args: list[str]
    optional_args: list[str]


class MultiFormatState(IntEnum):
    """Enum for the state of the multi file format."""

    EMPTY = auto()
    HEADING = auto()
    PARAGRAPH = auto()
    PARAGRAPH_END = auto()
    BULLET_LIST = auto()
    BULLET_LIST_ITEM = auto()
    NUMBERED_LIST = auto()
    NUMBERED_LIST_ITEM = auto()
    TABLE = auto()
    CODE_BLOCK = auto()
    CLOSED = auto()


class PointListType(IntEnum):
    """Enum for the type of point list."""

    BULLET = auto()
    NUMBERED = auto()


class PointStackItem(TypedDict):
    """Item in the point list stack."""

    point_list_type: PointListType
    number_at_level: int


class TableInformation:  # pylint: disable=too-few-public-methods
    """Information about a table."""

    def __init__(self) -> None:
        """Initialize the TableInformation class."""
        self.number_of_columns: int = 0
        self.number_of_rows: int = 0
        self.column_widths: list[int] = []


class MultiFormat:  # pylint: disable=too-many-instance-attributes
    """Base class for all multi file format classes."""

    def __init__(self, file_name: str,
                 url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the MultiFormat class.

        Args:
            file_name: The name of the file to write to.
            url_as_text: Format URLs as text not clickable URLs.
            file_exists_callback: A callback function to call if the file
                                  already exists. Return to allow the file to
                                  be overwritten. Raise an exception to
                                  prevent the file from being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
        """
        self.file_exists_callback: Optional[Callable[[str], None]] = \
            file_exists_callback
        self.file_name: str = \
            self.file_name_with_extension(file_name,
                                          self.file_name_extension())
        self.state: MultiFormatState = MultiFormatState.EMPTY
        self.url_as_text: bool = url_as_text
        self._file_exists_check()
        self.point_list_stack: list[PointStackItem] = []
        self.heading_level: Optional[int] = None
        # Is whitespace needed at beginning of next text to be added?
        self.ws_needed_at_append: bool = False
        self.table: Optional[TableInformation] = None

    def __enter__(self) -> 'MultiFormat':
        """Enter the context manager."""
        self._file_exists_check()
        self.open()
        return self

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        """Exit the context manager.

        Args:
            exc_type: The type of the exception.
            exc_value: The value of the exception.
            traceback: The traceback of the exception.
        Returns:
            True if the exception was handled, False otherwise.
        """
        self.close()
        return exc_type is None

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter.

        Must be overridden by subclasses.
        """
        err = cls._must_be_overridden('get_arg_desciption')
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return FormatterDescriptor(name='', mandatory_args=[],
                                   optional_args=['file_exists_callback'])

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter.

        Must be overridden by subclasses.
        """
        err = cls._must_be_overridden('file_name_extension')
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return ''

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use MultiFormat as a context manager instead, using a with statement.
        """
        err = self._must_be_overridden('open')
        raise NotImplementedError(err)

    def close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use MultiFormat as a context manager instead, using a with statement.
        """
        if self.state != MultiFormatState.EMPTY:
            self._end_state()
            self._write_file_suffix()
        self._close()
        self.state = MultiFormatState.CLOSED

    def start_heading(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                      level: int, text: str, smart_ws: bool = True,
                      bold: bool = False, italic: bool = False) -> None:
        """Start a new heading.

        Args:
            level: The level of the heading.
            text: The text to write in the heading.
            smart_ws: If True, leading and trailing whitespace are collapsed
                      and a single space is inserted between texts (from
                      start_heading or add_text).
            bold: If True, the text is bold.
                  Recommended to leave False for headings as it will be
                  formatted as a heading.
            italic: If True, the text is italic.
                    Recommended to leave False for headings as it will be
                    formatted as a heading.
        """
        if self.state != MultiFormatState.PARAGRAPH_END:
            self._end_state()
        self._start_heading(level)
        self.state = MultiFormatState.HEADING
        self.heading_level = level
        self.ws_needed_at_append = False
        self._write_text(self._to_write(text, smart_ws, False),
                         self.state, bold, italic)

    def start_paragraph(self, text: str, smart_ws: bool = True,
                        bold: bool = False, italic: bool = False) -> None:
        """Start a new paragraph.

        Args:
            text: The text to write in the paragraph.
            smart_ws: If True, leading and trailing whitespace are collapsed
                      and a single space is inserted between texts (from
                      start_paragraph or add_text).
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        if self.state != MultiFormatState.PARAGRAPH_END:
            self._end_state()
        self._start_paragraph()
        self.state = MultiFormatState.PARAGRAPH
        self._write_text(self._to_write(text, smart_ws, False),
                         self.state, bold, italic)

    def start_bullet_item(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                          text: str, level: Optional[int] = None,
                          smart_ws: bool = True, bold: bool = False,
                          italic: bool = False) -> None:
        """Start a new bullet list item and a new bullet list if needed.

        If level is not provided, the item is added to the current bullet list.
        If level is not provided and there is no current bullet list, a new
        bullet list is started.
        If level is provided and it is one greater than the current level, a
        new bullet list is started.
        If level is provided and it is less than the current level, one or
        several lists are ended to get to the level specified.
        If level is provided and it is equal to the current level, the item is
        added to the current bullet list item.
        If level is provided and it is more than one greater than the current
        level, an error is raised.
        If level is provided and and the list at that level is not a bullet
        list, the list at that level is ended and a new bullet list is started.
        Args:
            text: The text to write in the bullet list item.
            level: The level of the bullet list item.
            smart_ws: If True, leading and trailing whitespace are collapsed
                      and a single space is inserted between texts (from
                      start_bullet_item or add_text).
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        assert level is None or level > 0
        self._start_list_item_impl(
            text=text, level=level, smart_ws=smart_ws,
            bold=bold, italic=italic,
            point_list_type=PointListType.BULLET)

    def start_numbered_point_item(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                  text: str, level: Optional[int] = None,
                                  smart_ws: bool = True, bold: bool = False,
                                  italic: bool = False) -> None:
        """Start a new numbered point list item and a new list if needed.

        If level is not provided, the item is added to the current numbered
        point list
        If level is not provided and there is no current numbered point list,
        a new numbered point list is started.
        If level is provided and it is one greater than the current level, a
        new numbered point list is started.
        If level is provided and it is less than the current level, one or
        several lists are ended to get to the level specified.
        If level is provided and it is equal to the current level, the item is
        added to the current numbered point list item.
        If level is provided and it is more than one greater than the current
        level, an error is raised.
        If level is provided and and the list at that level is not a numbered
        point list, the list at that level is ended and a new numbered point
        list is started.
        Args:
            text: The text to write in the numbered point list item.
            level: The level of the numbered point list item.
            smart_ws: If True, leading and trailing whitespace are collapsed
                      and a single space is inserted between texts (from
                      start_numbered_point_item or add_text).
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        assert level is None or level > 0
        self._start_list_item_impl(
            text=text, level=level, smart_ws=smart_ws,
            bold=bold, italic=italic,
            point_list_type=PointListType.NUMBERED)

    def add_text(self, text: str, smart_ws: bool = True,
                 bold: bool = False, italic: bool = False) -> None:
        """Add text to the current item (paragraph, bullet list item, etc.).

        Args:
            text: The text to add to the current item.
            smart_ws: If True, leading and trailing whitespace are collapsed
                      and a single space is inserted between texts (from
                      start_paragraph, start_bullet, ... or add_text).
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        if self.state not in (MultiFormatState.HEADING,
                              MultiFormatState.PARAGRAPH,
                              MultiFormatState.BULLET_LIST_ITEM,
                              MultiFormatState.NUMBERED_LIST_ITEM):
            err = f'Cannot add text to state {self.state.name}'
            raise RuntimeError(err)
        self._write_text(self._to_write(text, smart_ws, True),
                         self.state, bold, italic)

    def add_url(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                url: str, text: Optional[str] = None,
                smart_ws: bool = True,
                bold: bool = False, italic: bool = False) -> None:
        """Add a URL to the current item (paragraph, bullet list item, etc.).

        Args:
            url: The URL to add to the current item.
            text: The text to add to the current item.
            smart_ws: If True, leading and trailing whitespace are collapsed
                      and a single space is inserted between texts (from
                      add_url or add_text).
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        if self.state not in (MultiFormatState.HEADING,
                              MultiFormatState.PARAGRAPH,
                              MultiFormatState.BULLET_LIST_ITEM,
                              MultiFormatState.NUMBERED_LIST_ITEM):
            err = f'Cannot add URL to state {self.state.name}'
            raise RuntimeError(err)
        if self.url_as_text:
            text_to_write = ''
            if text:
                assert text is not None
                text_to_write = self._to_write(text, smart_ws, True) + ' '
            text_to_write += url.strip()
            self._write_text(text_to_write, self.state, bold, italic)
            return
        # Write spacing before URL if needed
        if smart_ws and self.ws_needed_at_append:
            self._write_text(' ', self.state, False, False)
        # Process URL text and update ws_needed_at_append
        processed_text = text.strip() if text and smart_ws else text
        self.ws_needed_at_append = \
            not processed_text[-1].isspace() if processed_text else True
        self._write_url(url,
                        self._encode_text(processed_text) if processed_text
                        else None,
                        self.state, bold, italic)

    def start_table(self, first_row: list[str],
                    bold: bool = False, italic: bool = False) -> None:
        """Start a new table.

        Args:
            first_row: The first row of the table.
            bold: If True, the text in each cell in first row is bold.
            italic: If True, the text in each cell in first row is italic.
        """
        if self.state != MultiFormatState.PARAGRAPH_END:
            self._end_state()
        if not self.table:
            self.table = TableInformation()
        self.table.number_of_rows = 0
        self.table.number_of_columns = len(first_row)
        self._update_table_column_widths(row=first_row)
        self.state = MultiFormatState.TABLE
        self._start_table(num_columns=self.table.number_of_columns)
        encoded_first_row = self._encode_table_row(first_row)
        self._write_table_first_row(first_row=encoded_first_row,
                                    bold=bold,
                                    italic=italic)
        self.table.number_of_rows += 1

    def add_table_row(self, row: list[str],
                      bold: bool = False, italic: bool = False) -> None:
        """Add a row to the table.

        Args:
            row: The row to add to the table.
            bold: If True, the text in each cell in row is bold.
            italic: If True, the text in each cell in row is italic.
        """
        if self.state != MultiFormatState.TABLE:
            errmsg = f'Cannot add table row to state {self.state.name}'
            raise RuntimeError(errmsg)
        assert self.table is not None
        if len(row) != self.table.number_of_columns:
            errmsg = f'Row has {len(row)} columns, but table has '
            errmsg += f'{self.table.number_of_columns} columns'
            raise RuntimeError(errmsg)
        self._update_table_column_widths(row=row)
        self._write_table_row(row=self._encode_table_row(row),
                              bold=bold, italic=italic,
                              row_number=self.table.number_of_rows)
        self.table.number_of_rows += 1

    def write_complete_table(self, table: list[list[str]],
                             bold_first_row: bool = False,
                             italic_first_row: bool = False) -> None:
        """Add a complete table.

        Result is same as calling start_table followed by add_table_row
        for each row. Args:
            table: The complete table to add.
            bold_first_row: If True, the text in each cell in first
                            row is bold.
            italic_first_row: If True, the text in each cell in first
                              row is italic.
        """
        assert table is not None and isinstance(table, list)
        if len(table) == 0:
            errmsg = 'Table must have at least one row.'
            raise RuntimeError(errmsg)
        num_cols = len(table[0])
        if num_cols == 0:
            errmsg = 'First row of table must have at least one column.'
            raise RuntimeError(errmsg)
        self.table = TableInformation()
        for row_number, row in enumerate(table):
            if len(row) != num_cols:
                errmsg = f'Row {row_number} has {len(row)} columns, but '
                errmsg += f'first row has {num_cols} columns.\n'
                errmsg += 'All rows must have the same number of columns!'
                raise RuntimeError(errmsg)
            self._update_table_column_widths(row=row)
        self.start_table(first_row=table[0], bold=bold_first_row,
                         italic=italic_first_row)
        for row in table[1:]:
            self.add_table_row(row=row, bold=False, italic=False)

    def write_code_block(self, text: str,
                         programming_language: Optional[str] = None) -> None:
        """Add a code block.

        Write a text block verbatim into the document. Trying to keep all
        aspects of the text block, including whitespace, line breaks, etc.
        The text block is ended with a line break.
        Depending on the actual document format, the text block may be
        formatted as a code block or as a verbatim text block.
        Args:
            text: The text to add to the code block.
            programming_language: The programming language of the code block.
                                  Depending on the actual document format,
                                  this may be ignored or used to syntax
                                  highlight the code block.
        """
        if self.state != MultiFormatState.PARAGRAPH_END:
            self._end_state()
        self.state = MultiFormatState.CODE_BLOCK
        self._start_code_block(programming_language=programming_language)
        self._write_code_block(text=self._encode_text(text),
                               programming_language=programming_language)
        self._end_code_block(programming_language=programming_language)
        self.state = MultiFormatState.PARAGRAPH_END

    def _start_list_item_impl(  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
            self, text: str, level: Optional[int],
            smart_ws: bool, bold: bool, italic: bool,
            point_list_type: PointListType) -> None:
        """Start a list item of any type.

        Handle the full state machine for list items with a clear,
        linear flow:
        1. Calculate the effective target level
        2. Validate the level
        3. Exit any non-list state
        4. Adjust to the target level and type
        5. Start the new item
        6. Write the text

        Args:
            text: The text to write in the list item.
            level: The level of the list item (None = current or 1).
            smart_ws: If True, leading and trailing whitespace are collapsed.
            bold: If True, the text is bold.
            italic: If True, the text is italic.
            point_list_type: The type of point list (bullet or numbered).
        """
        target_level = level if level else (len(self.point_list_stack) or 1)
        self._validate_list_level(target_level, point_list_type)
        if not self._is_in_list_state():
            self._end_state()
        self._adjust_to_list_level(target_level, point_list_type)
        self._start_item_in_list(point_list_type)
        self.ws_needed_at_append = False
        self._write_text(self._to_write(text, smart_ws, False),
                         self.state, bold, italic)

    def _validate_list_level(
            self, target_level: int,
            point_list_type: PointListType) -> None:
        """Validate that the target level is reachable.

        Args:
            target_level: The level to validate.
            point_list_type: The type of list (for error message).
        Raises:
            RuntimeError: If the target level skips a level.
        """
        if target_level > len(self.point_list_stack) + 1:
            type_name = self._get_point_list_type_name(point_list_type)
            raise RuntimeError(
                f'start_{type_name}_item called with level={target_level}, '
                f'but level {target_level-1} does not exist.')

    def _adjust_to_list_level(
            self, target_level: int,
            point_list_type: PointListType) -> None:
        """Adjust the list stack to the target level with the right type.

        This method handles three operations in sequence:
        1. Decrease depth: End lists until at or below target level
        2. Switch type: End list at target level if type doesn't match
        3. Increase depth: Start new lists until at target level

        Args:
            target_level: The level to reach.
            point_list_type: The type of list needed at target level.
        """
        # Step 1: Decrease depth if needed
        while len(self.point_list_stack) > target_level:
            self._end_list_state()
        # Step 2: Switch type at target level if needed
        if len(self.point_list_stack) == target_level:
            if self.point_list_stack[-1]['point_list_type'] != point_list_type:
                self._end_list_state()
        # Step 3: Increase depth if needed
        while len(self.point_list_stack) < target_level:
            self._end_item_before_nesting()
            self._push_and_start_list(point_list_type)

    def _end_item_before_nesting(self) -> None:
        """End the current item before starting a nested list.

        Transitions from item state to list state. Does nothing if not
        currently in an item state or if no list exists.
        """
        if not self.point_list_stack or not self._is_in_item_state():
            return
        current_type = self.point_list_stack[-1]['point_list_type']
        list_state, _ = self._get_list_states(current_type)
        self._dispatch_end_item(len(self.point_list_stack), current_type)
        self.state = list_state

    def _push_and_start_list(self, point_list_type: PointListType) -> None:
        """Push a new list onto the stack and start it.

        Args:
            point_list_type: The type of list to start.
        """
        stack_item = PointStackItem(
            point_list_type=point_list_type,
            number_at_level=0)
        self.point_list_stack.append(stack_item)
        list_state, _ = self._get_list_states(point_list_type)
        self.state = list_state
        self._dispatch_start_list(len(self.point_list_stack), point_list_type)

    def _start_item_in_list(self, point_list_type: PointListType) -> None:
        """Start a new item in the current list.

        Ends the current item if in item state, then starts a new one.

        Args:
            point_list_type: The type of list item to start.
        """
        _, item_state = self._get_list_states(point_list_type)
        lev = len(self.point_list_stack)
        if self.state == item_state:
            self._dispatch_end_item(lev, point_list_type)
        self.point_list_stack[-1]['number_at_level'] += 1
        self._dispatch_start_item(lev, point_list_type)
        self.state = item_state

    def _full_number_of_list_item(self, num: int) -> str:
        """Get the full number of the current item."""
        full_number = ''
        assert isinstance(num, int)
        assert self.point_list_stack
        assert self.point_list_stack[-1]['number_at_level'] == num
        for stack_item in self.point_list_stack:
            full_number += f'{stack_item["number_at_level"]}.'
        return full_number

    def _get_list_states(
            self,
            point_list_type: PointListType
    ) -> tuple[MultiFormatState, MultiFormatState]:
        """Get the list and item states for a point list type.

        Args:
            point_list_type: The type of point list.
        Returns:
            A tuple of (list_state, item_state).
        """
        if point_list_type == PointListType.BULLET:
            return (MultiFormatState.BULLET_LIST,
                    MultiFormatState.BULLET_LIST_ITEM)
        return (MultiFormatState.NUMBERED_LIST,
                MultiFormatState.NUMBERED_LIST_ITEM)

    def _get_point_list_type_name(
            self, point_list_type: PointListType) -> str:
        """Get the name of a point list type for error messages."""
        if point_list_type == PointListType.BULLET:
            return 'bullet'
        return 'numbered'

    def _is_in_list_state(self) -> bool:
        """Check if currently in any list state (list or item)."""
        return self.state in (MultiFormatState.BULLET_LIST,
                              MultiFormatState.BULLET_LIST_ITEM,
                              MultiFormatState.NUMBERED_LIST,
                              MultiFormatState.NUMBERED_LIST_ITEM)

    def _is_in_item_state(self) -> bool:
        """Check if currently in any list item state."""
        return self.state in (MultiFormatState.BULLET_LIST_ITEM,
                              MultiFormatState.NUMBERED_LIST_ITEM)

    def _dispatch_start_list(
            self, level: int, point_list_type: PointListType) -> None:
        """Call the appropriate _start_*_list method."""
        if point_list_type == PointListType.BULLET:
            self._start_bullet_list(level=level)
        else:
            self._start_numbered_list(level=level)

    def _dispatch_end_list(
            self, level: int, point_list_type: PointListType) -> None:
        """Call the appropriate _end_*_list method."""
        if point_list_type == PointListType.BULLET:
            self._end_bullet_list(level=level)
        else:
            self._end_numbered_list(level=level)

    def _dispatch_start_item(
            self, level: int, point_list_type: PointListType) -> None:
        """Call the appropriate _start_*_item method."""
        if point_list_type == PointListType.BULLET:
            self._start_bullet_item(level=level)
        else:
            num = self.point_list_stack[-1]['number_at_level']
            full_number = self._full_number_of_list_item(num=num)
            self._start_numbered_item(level=level, num=num,
                                      full_number=full_number)

    def _dispatch_end_item(
            self, level: int, point_list_type: PointListType) -> None:
        """Call the appropriate _end_*_item method."""
        if point_list_type == PointListType.BULLET:
            self._end_bullet_item(level=level)
        else:
            num = self.point_list_stack[-1]['number_at_level']
            self._end_numbered_item(level=level, num=num)

    def _close(self) -> None:
        """Close the file.

        Must be overridden by subclasses.
        """
        err = self._must_be_overridden('_close')
        raise NotImplementedError(err)

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""
        err = self._must_be_overridden('_write_file_prefix')
        raise NotImplementedError(err)

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""
        err = self._must_be_overridden('_write_file_suffix')
        raise NotImplementedError(err)

    def _end_state(self) -> None:
        """End the current state."""
        if self.state == MultiFormatState.EMPTY:
            self._write_file_prefix()
            self.state = MultiFormatState.PARAGRAPH_END
        elif self.state == MultiFormatState.PARAGRAPH:
            self._end_paragraph()
            self.state = MultiFormatState.PARAGRAPH_END
        elif self.state == MultiFormatState.HEADING:
            assert self.heading_level is not None
            self._end_heading(level=self.heading_level)
            self.state = MultiFormatState.PARAGRAPH_END
            self.heading_level = None
        elif self.state == MultiFormatState.TABLE:
            assert self.table is not None
            self._end_table(num_columns=self.table.number_of_columns,
                            num_rows=self.table.number_of_rows)
            self.table = None
            self.state = MultiFormatState.PARAGRAPH_END
        elif self.state in (MultiFormatState.BULLET_LIST_ITEM,
                            MultiFormatState.BULLET_LIST,
                            MultiFormatState.NUMBERED_LIST_ITEM,
                            MultiFormatState.NUMBERED_LIST):
            while self.point_list_stack:
                self._end_list_state()
            self.state = MultiFormatState.PARAGRAPH_END

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        err = self._must_be_overridden('_start_paragraph')
        raise NotImplementedError(err)

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        err = self._must_be_overridden('_end_paragraph')
        raise NotImplementedError(err)

    def _start_heading(self, level: int) -> None:
        """Start a heading."""
        assert isinstance(level, int)
        err = self._must_be_overridden('_start_heading')
        raise NotImplementedError(err)

    def _end_heading(self, level: int) -> None:
        """End a heading."""
        assert isinstance(level, int)
        err = self._must_be_overridden('_end_heading')
        raise NotImplementedError(err)

    def _write_text(self, text: str, state: MultiFormatState,
                    bold: bool, italic: bool) -> None:
        """Write text into current item (paragraph, bullet list item...)."""
        assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        assert isinstance(bold, bool)
        assert isinstance(italic, bool)
        err = self._must_be_overridden('_write_text')
        raise NotImplementedError(err)

    def _write_url(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                   url: str, text: Optional[str],
                   state: MultiFormatState,
                   bold: bool, italic: bool) -> None:
        """Write a URL into current item (paragraph, bullet list item...)."""
        assert isinstance(url, str)
        if text is not None:
            assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        assert isinstance(bold, bool)
        assert isinstance(italic, bool)
        err = self._must_be_overridden('_write_url')
        raise NotImplementedError(err)

    @staticmethod
    def file_name_with_extension(file_name: str, extension: str) -> str:
        """Get the file name with the extension."""
        if not extension.startswith('.'):
            extension = f'.{extension}'
        if file_name.endswith(extension):
            return file_name
        return f'{file_name}{extension}'

    @classmethod
    def _must_be_overridden(cls, func_name: str) -> str:
        """Error message if the function is not overridden by a subclass."""
        return f'{func_name} must be overridden by a ' + \
            f'subclass {cls.__name__}'

    def _file_exists_check(self) -> None:
        """Check if the file exists and handle it accordingly."""
        if os.path.exists(self.file_name):
            if self.file_exists_callback is not None:
                self.file_exists_callback(self.file_name)
            else:
                msg = 'Cowardly refusing to overwrite existing file '
                msg += f'{self.file_name}.\n\n'
                msg += '(Use a different file name or provide a '
                msg += 'file_exists_callback \n'
                msg += ' function to allow the file to be overwritten.)\n'
                print(msg, file=sys.stderr)
                raise FileExistsError(msg)

    def _to_write_optional(self, text: Optional[str],
                           smart_ws: bool,
                           in_add: bool) -> Optional[str]:
        """Get the text to write."""
        if text is None:
            return None
        if not smart_ws:
            self.ws_needed_at_append = \
               bool(text) and not text[-1].isspace()
            return self._encode_text(text)
        ret = text.strip()
        if self.ws_needed_at_append and in_add:
            ret = ' ' + ret
        # As ret was stripped, no whitespace at end of text. Whitespace is
        # needed at beginning of next text to be added.
        # However, if ret is empty, whitespace is not needed.
        self.ws_needed_at_append = bool(ret)
        return self._encode_text(ret)

    def _to_write(self, text: str, smart_ws: bool, in_add: bool) -> str:
        """Get the text to write."""
        ret = self._to_write_optional(text, smart_ws, in_add)
        assert ret is not None  # ret can only be None if text is None
        return ret

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list."""
        assert isinstance(level, int)
        err = self._must_be_overridden('_start_bullet_list')
        raise NotImplementedError(err)

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list."""
        assert isinstance(level, int)
        err = self._must_be_overridden('_end_bullet_list')
        raise NotImplementedError(err)

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item."""
        assert isinstance(level, int)
        err = self._must_be_overridden('_start_bullet_item')
        raise NotImplementedError(err)

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item."""
        assert isinstance(level, int)
        err = self._must_be_overridden('_end_bullet_item')
        raise NotImplementedError(err)

    def _end_numbered_item(self, level: int, num: int) -> None:
        """End a numbered item."""
        assert isinstance(level, int)
        assert isinstance(num, int)
        err = self._must_be_overridden('_end_numbered_item')
        raise NotImplementedError(err)

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list."""
        assert isinstance(level, int)
        err = self._must_be_overridden('_end_numbered_list')
        raise NotImplementedError(err)

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list."""
        assert isinstance(level, int)
        err = self._must_be_overridden('_start_numbered_list')
        raise NotImplementedError(err)

    def _start_numbered_item(self, level: int, num: int,
                             full_number: str) -> None:
        """Start a numbered item.

        Args:
            level: The level of the item.
            num: The number of the item at this level.
            full_number: The full number of the item including all levels.
        """
        assert isinstance(level, int)
        assert isinstance(num, int)
        assert isinstance(full_number, str)
        err = self._must_be_overridden('_start_numbered_item')
        raise NotImplementedError(err)

    def _update_table_column_widths(self, row: list[str]) -> None:
        """Update the column widths of the table."""
        assert self.table is not None
        while len(self.table.column_widths) < len(row):
            self.table.column_widths.append(0)
        self.table.column_widths = \
            [max(len(cell), width) for cell, width in
             zip(row, self.table.column_widths)]

    def _start_table(self, num_columns: int) -> None:
        """Start a table."""
        assert isinstance(num_columns, int)
        err = self._must_be_overridden('_start_table')
        raise NotImplementedError(err)

    def _end_table(self, num_columns: int, num_rows: int) -> None:
        """End a table."""
        assert isinstance(num_columns, int)
        assert isinstance(num_rows, int)
        err = self._must_be_overridden('_end_table')
        raise NotImplementedError(err)

    def _write_table_first_row(self, first_row: list[str],
                               bold: bool, italic: bool) -> None:
        """Write the first row of the table."""
        assert isinstance(first_row, list)
        assert isinstance(bold, bool)
        assert isinstance(italic, bool)
        err = self._must_be_overridden('_write_table_first_row')
        raise NotImplementedError(err)

    def _write_table_row(self, row: list[str], bold: bool, italic: bool,
                         row_number: int) -> None:
        """Write a row of the table."""
        assert isinstance(row, list)
        assert isinstance(bold, bool)
        assert isinstance(italic, bool)
        assert isinstance(row_number, int)
        err = self._must_be_overridden('_write_table_row')
        raise NotImplementedError(err)

    def _state_from_point_list(self) -> None:
        """Set the state from the point list stack."""
        if not self.point_list_stack:
            self.state = MultiFormatState.PARAGRAPH_END
            return
        point_list_type = self.point_list_stack[-1]['point_list_type']
        if point_list_type == PointListType.BULLET:
            self.state = MultiFormatState.BULLET_LIST
            return
        if point_list_type == PointListType.NUMBERED:
            self.state = MultiFormatState.NUMBERED_LIST
            return
        err = 'Unknown point list type ' + \
            f'{self.point_list_stack[-1]["point_list_type"]}'
        raise RuntimeError(err)

    def _end_list_state(self) -> None:
        """End a list state."""
        assert self.point_list_stack
        point_list_type = self.point_list_stack[-1]['point_list_type']
        list_state, item_state = self._get_list_states(point_list_type)
        lev = len(self.point_list_stack)
        if self.state == item_state:
            self._dispatch_end_item(level=lev, point_list_type=point_list_type)
            self.state = list_state
        if self.state == list_state:
            self._dispatch_end_list(level=lev, point_list_type=point_list_type)
            self.point_list_stack.pop()
            self._state_from_point_list()

    def _start_code_block(self, programming_language: Optional[str]) -> None:
        """Start a code block."""
        if programming_language is not None:
            assert isinstance(programming_language, str)
        err = self._must_be_overridden('_start_code_block')
        raise NotImplementedError(err)

    def _end_code_block(self, programming_language: Optional[str]) -> None:
        """End a code block."""
        if programming_language is not None:
            assert isinstance(programming_language, str)
        err = self._must_be_overridden('_end_code_block')
        raise NotImplementedError(err)

    def _write_code_block(self, text: str,
                          programming_language: Optional[str]) -> None:
        """Write a code block."""
        assert isinstance(text, str)
        if programming_language is not None:
            assert isinstance(programming_language, str)
        err = self._must_be_overridden('_write_code_block')
        raise NotImplementedError(err)

    def _encode_text(self, text: str) -> str:
        """Encode text (escape special characters).

        Derived classes must implement this method.
        Whenever special characters need to be encoded, this method
        should be defined in the derived class. The base class always
        calls this method with the text to encode.
        Notice that the derived class implementation have access to
        the self.state variable, in case the encoding depends on the
        current state.

        Args:
            text: The text to encode.
        Returns:
            The encoded text.
        """
        assert isinstance(text, str)
        err = self._must_be_overridden('_encode_text')
        raise NotImplementedError(err)
        return text  # pylint: disable=unreachable

    def _encode_table_row(self, row: list[str]) -> list[str]:
        """Encode a table row."""
        assert isinstance(row, list)
        return [self._encode_text(cell) for cell in row]
