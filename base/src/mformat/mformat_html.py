#! /usr/local/bin/python3
"""HTML format class."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from typing import Optional
from mformat.mformat_textbased import MultiFormatTextBased
from mformat.mformat import FormatterDescriptor


class MultiFormatHtml(MultiFormatTextBased):
    """HTML format class."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: str, url_as_text: bool = False,
                 title: str = 'HTML file', css_file: Optional[str] = None,
                 lang: str = 'en'):
        """Initialize the HtmlFormat class."""
        super().__init__(file_name=file_name, url_as_text=url_as_text)
        self.title: str = title
        self.css_file: Optional[str] = css_file
        self.lang: str = lang

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.html'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='html', mandatory_args=[],
                                   optional_args=['title', 'css_file',
                                                  'lang'])

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""
        assert self.file is not None
        self.file.write('<!DOCTYPE html encoding="utf-8">\n')
        self.file.write(f'<html lang="{self.lang}">\n')
        self.file.write('<head>\n')
        self.file.write(f'<title>{self.title}</title>\n')
        if self.css_file is not None:
            self.file.write('<link rel="stylesheet" ' +
                            f'href="{self.css_file}">\n')
        self.file.write('</head>\n')
        self.file.write('<body>\n')

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""
        assert self.file is not None
        self.file.write('</body>\n')
        self.file.write('</html>\n')

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        assert self.file is not None
        self.file.write('<p>\n')

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        assert self.file is not None
        self.file.write('</p>\n')

    def _write_in_paragraph(self, text: str) -> None:
        """Write text into current paragraph."""
        assert self.file is not None
        self.file.write(text)
