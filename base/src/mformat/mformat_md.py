#! /usr/local/bin/python3
"""Markdown format class."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Optional, Callable
from mformat.mformat_textbased import MultiFormatTextBased
from mformat.mformat import FormatterDescriptor, MultiFormatState


class MultiFormatMd(MultiFormatTextBased):
    """Markdown format class."""

    def __init__(self, file_name: str, url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]] = None):
        """Initialize the MdFormat class.

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

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.md'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='md', mandatory_args=[],
                                   optional_args=[])

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        assert self.file is not None
        self.file.write('\n')

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        assert self.file is not None
        self.file.write('\n')

    def _start_heading(self, level: int) -> None:
        """Start a heading."""
        assert self.file is not None
        self.file.write(f'{"#" * level} ')

    def _end_heading(self, level: int) -> None:
        """End a heading."""
        assert self.file is not None
        self.file.write('\n')

    def _write_text(self,  # pylint: disable=unused-argument,too-many-arguments,too-many-positional-arguments # noqa: E501
                    text: str, state: MultiFormatState,
                    bold: bool, italic: bool) -> None:
        """Write text into current item (paragraph, bullet list item, etc.).

        Args:
            text: The text to write into the current item.
            state: The state of the current item.
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        assert self.file is not None
        if bold:
            text = f'**{text}**'
        if italic:
            text = f'*{text}*'
        self.file.write(text)

    def _write_url(self,  # pylint: disable=unused-argument,too-many-arguments,too-many-positional-arguments # noqa: E501
                   url: str, text: Optional[str],
                   state: MultiFormatState,
                   bold: bool, italic: bool) -> None:
        """Write a URL into current item (paragraph, bullet list item...)."""
        assert self.file is not None
        if not text:
            text = url
        text = f'[{text}]({url})'
        if bold:
            text = f'**{text}**'
        if italic:
            text = f'*{text}*'
        self.file.write(text)

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list."""
        assert self.file is not None
        assert isinstance(level, int)

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list."""
        assert self.file is not None
        assert isinstance(level, int)

    def _indent(self, level: int) -> str:
        """Get the indentation for a level."""
        assert self.file is not None
        assert isinstance(level, int)
        return 2*(level-1)*' '

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item."""
        assert self.file is not None
        assert isinstance(level, int)
        self.file.write(self._indent(level) + '- ')

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item."""
        assert self.file is not None
        assert isinstance(level, int)
        self.file.write('\n')

    def _start_numeric_list(self, level: int) -> None:
        """Start a numeric list."""
        assert self.file is not None
        assert isinstance(level, int)

    def _end_numeric_list(self, level: int) -> None:
        """End a numeric list."""
        assert self.file is not None
        assert isinstance(level, int)

    def _start_numeric_item(self, level: int, num: int) -> None:
        """Start a numeric item."""
        assert self.file is not None
        assert isinstance(level, int)
        assert isinstance(num, int)
        self.file.write(self._indent(level) + f'{num}. ')

    def _end_numeric_item(self, level: int, num: int) -> None:
        """End a numeric item."""
        assert self.file is not None
        assert isinstance(level, int)
        assert isinstance(num, int)
        self.file.write('\n')
