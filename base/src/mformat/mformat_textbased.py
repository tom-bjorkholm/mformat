#! /usr/local/bin/python3
"""Base class for all text based format classes."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import io
import re
from typing import TextIO, Optional, Callable
from mformat.mformat import MultiFormat


def split_whitespace(text: str) -> tuple[str, str, str]:
    """Split a string into leading, stripped, and trailing whitespace."""
    if not text:
        return '', '', ''
    stripped = text.strip()
    if not stripped:
        return text, '', ''
    if stripped == text:
        return '', stripped, ''
    leading = text[:len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()):]
    return leading, stripped, trailing


class MultiFormatTextBased(MultiFormat):
    """Base class for all text based format classes."""

    def __init__(self, file_name: str, url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]] = None):
        """Initialize the TextBasedFormat class.

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
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback)
        self.file: Optional[TextIO] = None
        # Line wrapping state
        self._current_column = 0
        self._continuation_indent = ''
        self._pending_whitespace = ''

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        self.file = open(self.file_name,  # pylint: disable=consider-using-with
                         mode='w+t', encoding='utf-8')

    def _close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        if self.file is None:
            return
        self.file.close()
        self.file = None

    def _get_last_chars_written(self, num_chars: int) -> str:
        """Get the last characters written to the file.

        Keep the file pointer at the same position, i.e. at the end of the
        file, so that we can continue writing after the last characters.
        Returns the last characters written to the file.
        """
        assert self.file is not None
        assert num_chars > 0
        cur_pos = self.file.tell()
        number_of_chars = min(num_chars, cur_pos)
        self.file.seek(cur_pos - number_of_chars, io.SEEK_SET)
        last_chars = self.file.read(number_of_chars)
        self.file.seek(cur_pos, io.SEEK_SET)
        return last_chars

    def _reset_line_state(self, continuation_indent: str = '') -> None:
        """Reset line tracking state for new wrappable content.

        Call this when starting a new paragraph or list item.

        Args:
            continuation_indent: Indent string for wrapped continuation lines.
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

        Wraps text at word boundaries to keep lines within the specified
        maximum length. Handles whitespace at wrap points by collapsing
        multiple spaces/newlines into the line break.

        Args:
            text: The text to write (may be wrapped).
            max_line_length: Maximum characters per line.
        """
        assert self.file is not None
        if not text:
            return

        # Split into tokens: sequences of whitespace or non-whitespace
        tokens = re.findall(r'\S+|\s+', text)
        indent_len = len(self._continuation_indent)

        for token in tokens:
            if token.isspace():
                # Hold whitespace as pending until we see the next word
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
            # Both whitespace and word fit on current line
            self._write_pending_whitespace()
            self.file.write(word)
            self._current_column += word_len
        elif self._current_column <= indent_len:
            # At start of line - word is too long but can't wrap further
            self._write_pending_whitespace()
            self.file.write(word)
            self._current_column += word_len
        else:
            # Need to wrap before this word
            # Discard pending whitespace (replaced by line break)
            self._pending_whitespace = ''
            self.file.write('\n' + self._continuation_indent)
            self.file.write(word)
            self._current_column = indent_len + word_len

    def _write_pending_whitespace(self) -> None:
        """Write any pending whitespace and clear it."""
        assert self.file is not None
        if self._pending_whitespace:
            self.file.write(self._pending_whitespace)
            self._current_column += len(self._pending_whitespace)
            self._pending_whitespace = ''

    def _wrap_and_write_atomic(self, text: str, max_line_length: int) -> None:
        """Write text as atomic unit (no breaking), wrapping before if needed.

        Use for URLs or other content that should not be broken across lines.

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
            # Both pending whitespace and text fit
            self._write_pending_whitespace()
            self.file.write(text)
            self._current_column += text_len
        elif self._current_column > indent_len:
            # Need to wrap before text - discard pending whitespace
            self._pending_whitespace = ''
            self.file.write('\n' + self._continuation_indent)
            self.file.write(text)
            self._current_column = indent_len + text_len
        else:
            # At start of line, text is long but can't wrap further
            self._write_pending_whitespace()
            self.file.write(text)
            self._current_column += text_len
