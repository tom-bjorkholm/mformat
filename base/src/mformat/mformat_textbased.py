#! /usr/local/bin/python3
"""Base class for all text based format classes."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import io
from typing import TextIO, Optional, Callable
from mformat.mformat import MultiFormat, PathLike


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

    def __init__(self, file_name: PathLike, url_as_text: bool = False,
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

    def _get_last_chars_written_impl(self, num_chars: int, end_pos: int,
                                     rec_count: int) -> str:
        """Get the last characters written to the file.

        This is an implementation detail of the _get_last_chars_written method.
        Keep the file pointer at the same position, i.e. at the end of the
        file, so that we can continue writing after the last characters.
        Returns the last characters written to the file.
        As utf-8 encode characters may be 1-6 bytes long, we need to read
        more than num_chars characters to get the last characters.
        (On Microsoft Windows the newline character is 2 bytes long CR/LF.)
        If we start reading bytes that are in the middle of a character,
        the utf-8 decoder will raise and exception. If we read 6 bytes for
        every character we are guaranteed to get the last characters.
        If the reading happens to be in the middle of a character it will
        be a character before the characters we are looking for. If
        decoding fails we will try again with a larger number of bytes,
        to try to find a place in the file where some preceeding character
        starts.
        Args:
            num_chars: The number of characters to get.
            end_pos: The position at end of file to start reading from.
            rec_count: The number of recursive calls.
        Returns:
            The last characters written to the file.
        """
        assert self.file is not None
        assert num_chars > 0
        if rec_count > 8:
            # Limit 8 is bigger than longest utf-8 encoded character (6 bytes)
            return ''
        number_of_bytes = min(num_chars * 6 + rec_count, end_pos)
        self.file.seek(end_pos - number_of_bytes, io.SEEK_SET)
        try:
            last_chars = self.file.read(number_of_bytes)
        except UnicodeDecodeError:
            return self._get_last_chars_written_impl(num_chars, end_pos,
                                                     rec_count + 1)
        self.file.seek(end_pos, io.SEEK_SET)
        return last_chars[-num_chars:]

    def _get_last_chars_written(self, num_chars: int) -> str:
        """Get the last characters written to the file.

        Keep the file pointer at the same position, i.e. at the end of the
        file, so that we can continue writing after the last characters.
        Returns the last characters written to the file.
        """
        assert self.file is not None
        assert num_chars > 0
        cur_pos = self.file.tell()
        last_chars = self._get_last_chars_written_impl(num_chars, cur_pos, 0)
        self.file.seek(cur_pos, io.SEEK_SET)
        return last_chars
