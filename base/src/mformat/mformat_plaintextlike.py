#! /usr/local/bin/python3
"""Base class for plain-text-like format classes."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import re
from typing import Optional, Callable
from mformat.mformat_textbased import MultiFormatTextBased
from mformat.mformat import PathLike


class MultiFormatPlainTextLike(MultiFormatTextBased):
    """Base class for plain-text-like format classes.

    Provides common functionality for formats that use plain text
    with line wrapping, indentation, and simple text markers
    (e.g. Markdown, plain text, reStructuredText), as opposed to
    tag-based formats (e.g. HTML, LaTeX).
    """

    def __init__(self, file_name: PathLike, url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]] = None,
                 character_encoding: str = 'utf-8'):
        """Initialize the MultiFormatPlainTextLike class.

        Args:
            file_name: The name of the file to write to.
            url_as_text: Format URLs as text not clickable URLs.
            file_exists_callback: A callback function to call if the
                file already exists. Return to allow the file to be
                overwritten. Raise an exception to prevent the file
                from being overwritten.
                (May for instance save existing file as backup.)
                (Default is to raise an exception.)
            character_encoding: The character encoding to use.
                                Default is 'utf-8'. Keep it as default unless
                                you have a good specific reason to change it.
        """
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback,
                         character_encoding=character_encoding)
        self._current_column = 0
        self._continuation_indent = ''
        self._pending_whitespace = ''

    # =================================================================
    # Line wrapping
    # =================================================================

    def _reset_line_state(self, continuation_indent: str = '') -> None:
        """Reset line tracking state for new wrappable content.

        Call this when starting a new paragraph or list item.

        Args:
            continuation_indent: Indent string for wrapped
                                 continuation lines.
        """
        self._current_column = 0
        self._continuation_indent = continuation_indent
        self._pending_whitespace = ''

    def _write_line_break(self) -> None:
        """Write a line break, discarding any pending whitespace.

        Call this when ending a paragraph or list item.
        Pending whitespace is discarded to avoid trailing spaces.
        """
        assert self.file is not None
        self._pending_whitespace = ''
        self.file.write('\n')
        self._current_column = 0

    def _wrap_and_write(self, text: str, max_line_length: int) -> None:
        """Wrap text to fit within max line length and write to file.

        Wraps text at word boundaries to keep lines within the
        specified maximum length. Handles whitespace at wrap points
        by collapsing multiple spaces/newlines into the line break.

        Args:
            text: The text to write (may be wrapped).
            max_line_length: Maximum characters per line.
        """
        assert self.file is not None
        if not text:
            return
        tokens = re.findall(r'\S+|\s+', text)
        indent_len = len(self._continuation_indent)
        for token in tokens:
            if token.isspace():
                self._pending_whitespace = token
            else:
                self._write_word_with_wrapping(token, max_line_length,
                                               indent_len)

    def _write_word_with_wrapping(self, word: str, max_line_length: int,
                                  indent_len: int) -> None:
        """Write a word, wrapping to new line if needed.

        Args:
            word: The word to write (non-whitespace token).
            max_line_length: Maximum characters per line.
            indent_len: Length of continuation indent.
        """
        assert self.file is not None
        ws_len = len(self._pending_whitespace)
        word_len = len(word)
        total_len = ws_len + word_len
        if self._current_column + total_len <= max_line_length:
            self._write_pending_whitespace()
            self.file.write(word)
            self._current_column += word_len
        elif self._current_column <= indent_len:
            self._write_pending_whitespace()
            self.file.write(word)
            self._current_column += word_len
        else:
            self._pending_whitespace = ''
            self.file.write('\n' + self._continuation_indent)
            self.file.write(word)
            self._current_column = indent_len + word_len

    def _write_pending_whitespace(self) -> None:
        """Write any pending whitespace and clear it."""
        assert self.file is not None
        if self._pending_whitespace:
            self.file.write(self._pending_whitespace)
            self._current_column += len(
                self._pending_whitespace)
            self._pending_whitespace = ''

    def _wrap_and_write_atomic(self, text: str, max_line_length: int) -> None:
        """Write text as atomic unit, wrapping before if needed.

        Use for URLs or other content that should not be broken
        across lines.

        Args:
            text: The text to write (will not be broken).
            max_line_length: Maximum characters per line.
        """
        assert self.file is not None
        text_len = len(text)
        ws_len = len(self._pending_whitespace)
        total_len = ws_len + text_len
        indent_len = len(self._continuation_indent)
        if self._current_column + total_len <= max_line_length:
            self._write_pending_whitespace()
            self.file.write(text)
            self._current_column += text_len
        elif self._current_column > indent_len:
            self._pending_whitespace = ''
            self.file.write('\n' + self._continuation_indent)
            self.file.write(text)
            self._current_column = indent_len + text_len
        else:
            self._write_pending_whitespace()
            self.file.write(text)
            self._current_column += text_len

    # =================================================================
    # Structural helpers
    # =================================================================

    def _empty_line_before(self) -> None:
        """Make sure there is an empty line before next item."""
        assert self.file is not None
        preceeding = self._get_last_chars_written(num_chars=2)
        if preceeding in ('\n\n', ''):
            pass
        elif preceeding[-1] == '\n':
            self.file.write('\n')
        else:
            self.file.write('\n\n')

    def _indent2(self, level: int) -> str:
        """Get the indentation for a level."""
        return 2 * (level - 1) * ' '

    # =================================================================
    # Paragraph and block quote
    # =================================================================

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        self._empty_line_before()
        self._reset_line_state()

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        self._write_line_break()

    def _start_block_quote(self) -> None:
        """Start a block quote."""
        assert self.file is not None
        self._empty_line_before()
        self.file.write('> ')
        self._reset_line_state(continuation_indent='> ')
        self._current_column = 2

    def _end_block_quote(self) -> None:
        """End a block quote."""
        self._write_line_break()
        self._reset_line_state()

    # =================================================================
    # Bullet and numbered list items
    # =================================================================

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list (no-op for plain-text-like formats)."""
        assert isinstance(level, int)

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list (no-op for plain-text-like formats)."""
        assert isinstance(level, int)

    def _start_bullet_item_common(
            self, level: int,
            empty_line_before: bool = True,
            marker: str = '- ') -> None:
        """Start a bullet item."""
        assert self.file is not None
        assert isinstance(level, int)
        if empty_line_before:
            self._empty_line_before()
        indent = self._indent2(level)
        self.file.write(indent + marker)
        self._reset_line_state(
            continuation_indent=indent + '  ')
        self._current_column = len(indent) + len(marker)

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item."""
        _ = level  # pylint: disable=unused-variable
        self._write_line_break()

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list (no-op for plain-text-like)."""
        assert isinstance(level, int)

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list (no-op for plain-text-like)."""
        assert isinstance(level, int)

    def _start_numbered_item_common(
            self, level: int, num: int,
            full_number: str,
            empty_line_before: bool) -> None:
        """Start a numbered item."""
        assert self.file is not None
        assert isinstance(level, int)
        assert isinstance(num, int)
        if empty_line_before:
            self._empty_line_before()
        indent = self._indent2(level)
        marker = full_number + ' '
        self.file.write(indent + marker)
        self._reset_line_state(
            continuation_indent=indent + ' ' * len(marker))
        self._current_column = len(indent) + len(marker)

    def _end_numbered_item(self, level: int, num: int) -> None:
        """End a numbered list item."""
        _ = level  # pylint: disable=unused-variable
        _ = num  # pylint: disable=unused-variable
        self._write_line_break()
