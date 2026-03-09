#! /usr/local/bin/python3
"""MultiFormat class for LaTeX output format."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from copy import deepcopy
from typing import Optional, Callable
from mformat.document_class import DocumentClass, DocumentClassInput
from mformat.paper_size import PaperSize, PaperSizeInput
from mformat.mformat_textbased import MultiFormatTextBased, split_whitespace
from mformat.mformat_state import MultiFormatState, Formatting
from mformat.mformat import PathLike, FormatterDescriptor

_DEF_LATEX_HEADING_LEVELS: dict[DocumentClass, dict[int, str]] = {
    DocumentClass.ARTICLE: {
        1: 'section',
        2: 'subsection',
        3: 'subsubsection',
        4: 'paragraph',
        5: 'subparagraph',
    },
    DocumentClass.BOOK: {
        1: 'part',
        2: 'chapter',
        3: 'section',
        4: 'subsection',
        5: 'subsubsection',
        6: 'paragraph',
        7: 'subparagraph',
    },
    DocumentClass.REPORT: {
        1: 'chapter',
        2: 'section',
        3: 'subsection',
        4: 'subsubsection',
        5: 'paragraph',
        6: 'subparagraph',
    },
    DocumentClass.LETTER: {
        1: 'section',
        2: 'subsection',
        3: 'subsubsection',
        4: 'paragraph',
        5: 'subparagraph',
    },
}

_LATEX_ESCAPE_MAP: dict[str, str] = {
    '\\': '\\textbackslash{}',
    '{': '\\{',
    '}': '\\}',
    '$': '\\$',
    '&': '\\&',
    '%': '\\%',
    '#': '\\#',
    '_': '\\_',
    '^': '\\textasciicircum{}',
    '~': '\\textasciitilde{}',
}


class MultiFormatLatex(MultiFormatTextBased):
    """MultiFormat class for LaTeX output format."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 file_name: PathLike, url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]] = None,
                 character_encoding: str = 'utf-8',
                 document_class: Optional[DocumentClassInput] = None,
                 paper_size: Optional[PaperSizeInput] = None,
                 title: Optional[str] = None,
                 latex_preamble: str = '',
                 latex_heading_levels: Optional[dict[int, str]] = None,
                 latex_replacements: Optional[list[dict[str, str]]] = None):
        r"""Initialize the MultiFormatLatex class.

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
            document_class: The document class to use. If None, the default
                            document class REPORT will be used.
                            The document class is written into the
                            documentclass command in the preamble in the
                            LaTeX output file, but it is also used to set
                            the default heading levels for the output file.
            paper_size: The paper size to use. If None, the default
                        paper size A4 will be used.
                        The paper size is written into the
                        paper size command in the preamble in the
                        LaTeX output file. Note that paper_size cannot
                        be used if the latex_preamble string contains the
                        substring "\\documentclass".
            latex_preamble: This string is written into the preamble of the
                            LaTeX output file. If the string does not contain
                            the substring "\\documentclass" it will be
                            written to the output file directly after the
                            "\\documentclass" command. If the string
                            contains the
                            string "\\documentclass", the string is inserted
                            first in the output file, and paper size is
                            taken from the latex_preamble string (in this
                            case it is an error to also supply paper_size).
                            If the string does not contain the substring
                            "\\begin{document}", the string is inserted
                            before the "\\begin{document}" command.
                            If the string contains the substring
                            "\\begin{document}", this class generates no
                            "\\begin{document}" command (and thus the
                            latex_preamble string can contain also text
                            after the "\\begin{document}" command).
            latex_heading_levels: A dictionary of heading levels and their
                                  corresponding LaTeX commands. This will
                                  override the heading levels for the
                                  document class. Note that this need not
                                  map all heading levels, and the default
                                  heading levels for the document class will
                                  be used for the heading levels not mapped.
            latex_replacements: A list of dictionaries of LaTeX replacements.
                                The list must contain 3 dictionaries.
                                The replacements in latex_replacements[0]
                                will be done on the text to be written,
                                before the standard encoding is applied.
                                This means that latex_replacements[0]
                                is usable for replacing text content,
                                but not for inserting LaTeX commands.
                                The replacements in latex_replacements[1]
                                will be done on the text to be written,
                                after the standard encoding is applied.
                                This means that latex_replacements[2]
                                is usable for inserting LaTeX commands.
                                The replacements in latex_replacements[2]
                                will be done after the latex commands
                                have been added to the text. This means
                                that latex_replacements[2] is usable for
                                replacing LaTeX commands.
                                (Default is None.)
        """
        if not isinstance(latex_preamble, str):
            raise ValueError('latex_preamble must be a string')
        self.latex_preamble: str = latex_preamble
        self.document_class: DocumentClass = \
            DocumentClass.from_str(document_class) \
            if document_class is not None else DocumentClass.REPORT
        if self.document_class not in _DEF_LATEX_HEADING_LEVELS:
            raise ValueError(f'document_class {self.document_class} has no '
                             'default heading levels')
        self.heading_levels: dict[int, str] = \
            deepcopy(_DEF_LATEX_HEADING_LEVELS[self.document_class])
        self.paper_size: PaperSize = PaperSize.from_str(paper_size) \
            if paper_size is not None else PaperSize.A4
        if paper_size is not None and \
                self._preamble_has_documentclass():
            errmsg = 'paper_size cannot be used if the latex_preamble string '
            errmsg += 'contains the substring "\\documentclass"'
            raise ValueError(errmsg)
        if latex_heading_levels is not None:
            if not isinstance(latex_heading_levels, dict):
                raise ValueError('latex_heading_levels must be a dictionary')
            if not all(isinstance(k, int)
                       for k in latex_heading_levels.keys()):
                errmsg = 'latex_heading_levels must contain only int keys'
                raise ValueError(errmsg)
            if not all(isinstance(v, str)
                       for v in latex_heading_levels.values()):
                errmsg = 'latex_heading_levels must contain only str values'
                raise ValueError(errmsg)
            self.heading_levels.update({
                level: self._normalize_latex_command(command)
                for level, command in latex_heading_levels.items()
            })
        self.latex_replacements: list[dict[str, str]] = [{}, {}, {}]
        if latex_replacements is not None:
            if not isinstance(latex_replacements, list):
                raise ValueError('latex_replacements must be a list')
            if len(latex_replacements) != 3 or \
                    not all(isinstance(d, dict) for d in latex_replacements):
                raise ValueError('latex_replacements must contain 3 '
                                 'dictionaries')
            if not all(isinstance(key, str) and isinstance(value, str)
                       for mapping in latex_replacements
                       for key, value in mapping.items()):
                errmsg = 'latex_replacements dictionaries must contain only '
                errmsg += 'str keys and str values'
                raise ValueError(errmsg)
            self.latex_replacements = latex_replacements
        if title is not None and not isinstance(title, str):
            raise ValueError('title must be a string')
        self.title: Optional[str] = title
        self._latex_table_rows: list[list[str]] = []
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback,
                         character_encoding=character_encoding)

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='LaTeX', mandatory_args=[],
                                   optional_args=['character_encoding',
                                                  'title',
                                                  'document_class',
                                                  'paper_size',
                                                  'latex_preamble',
                                                  'latex_heading_levels',
                                                  'latex_replacements'])

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.tex'

    @staticmethod
    def _normalize_latex_command(command: str) -> str:
        """Normalize a command name by stripping whitespace and backslash."""
        normalized = command.strip()
        if normalized.startswith('\\'):
            normalized = normalized[1:]
        if not normalized:
            raise ValueError('LaTeX command name cannot be empty')
        return normalized

    def _heading_command(self, level: int) -> str:
        """Get a heading command for a level using deepest-known fallback."""
        if level in self.heading_levels:
            return self.heading_levels[level]
        sorted_levels = sorted(self.heading_levels.keys())
        if not sorted_levels:
            raise RuntimeError('No heading levels are configured')
        if level <= sorted_levels[0]:
            return self.heading_levels[sorted_levels[0]]
        if level >= sorted_levels[-1]:
            return self.heading_levels[sorted_levels[-1]]
        lower_levels = [heading_level for heading_level in sorted_levels
                        if heading_level <= level]
        assert lower_levels
        return self.heading_levels[lower_levels[-1]]

    def _apply_latex_replacements(self, text: str, stage: int) -> str:
        """Apply configured replacement stage to text."""
        result = text
        for key, value in self.latex_replacements[stage].items():
            result = result.replace(key, value)
        return result

    def _preamble_has_documentclass(self) -> bool:
        """Check if preamble contains a document class command."""
        return '\\documentclass' in self.latex_preamble

    def _preamble_has_begin_document(self) -> bool:
        """Check if preamble contains begin document command."""
        return '\\begin{document}' in self.latex_preamble

    def _preamble_has_end_document(self) -> bool:
        """Check if preamble contains end document command."""
        return '\\end{document}' in self.latex_preamble

    def _preamble_has_url_package(self) -> bool:
        """Check if preamble contains URL-capable package."""
        return ('\\usepackage{hyperref}' in self.latex_preamble or
                '\\usepackage{url}' in self.latex_preamble)

    def _write_with_stage_three_replacements(self, text: str) -> None:
        """Write text after applying stage-three replacements."""
        assert self.file is not None
        self.file.write(self._apply_latex_replacements(text, stage=2))

    def _ensure_blank_line_before(self) -> None:
        """Ensure there is an empty line before the next item."""
        assert self.file is not None
        preceeding = self._get_last_chars_written(num_chars=2)
        if preceeding in ('', '\n\n'):
            return
        if preceeding.endswith('\n'):
            self.file.write('\n')
            return
        self.file.write('\n\n')

    @staticmethod
    def _ensure_ending_newline(text: str) -> str:
        """Return text ending with a newline."""
        if text.endswith('\n'):
            return text
        return text + '\n'

    @staticmethod
    def _escape_latex_text(text: str) -> str:
        """Escape LaTeX special characters in plain text content."""
        return ''.join(_LATEX_ESCAPE_MAP.get(character, character)
                       for character in text)

    @staticmethod
    def _tabular_spec(num_columns: int) -> str:
        """Build a simple tabular specification for given number of columns."""
        return '|' + '|'.join(['l'] * num_columns) + '|'

    @staticmethod
    def _format_text(text: str, formatting: Formatting) -> str:
        """Apply bold and italic formatting wrappers to text."""
        if formatting.bold:
            text = f'\\textbf{{{text}}}'
        if formatting.italic:
            text = f'\\textit{{{text}}}'
        return text

    def _write_file_prefix(self) -> None:
        """Write the LaTeX file prefix and preamble."""
        assert self.file is not None
        has_docclass = self._preamble_has_documentclass()
        has_begin_document = self._preamble_has_begin_document()
        has_url_package = self._preamble_has_url_package()
        if not has_docclass:
            paper = self.paper_size.lower() + 'paper'
            docclass = self.document_class.lower()
            self.file.write(f'\\documentclass[{paper}]{{{docclass}}}\n')
        if not self.url_as_text and \
                not has_url_package and \
                not has_docclass:
            self.file.write('\\usepackage{hyperref}\n')
        if self.latex_preamble:
            self.file.write(self._ensure_ending_newline(self.latex_preamble))
        if not self.url_as_text and \
                not has_url_package and \
                has_docclass and \
                not has_begin_document:
            self.file.write('\\usepackage{hyperref}\n')
        encoded_title = self._encode_text(self.title) \
            if self.title is not None else None
        if encoded_title is not None:
            self._write_with_stage_three_replacements(
                f'\\title{{{encoded_title}}}\n')
        if not has_begin_document:
            self.file.write('\\begin{document}\n')
        if encoded_title is not None:
            self.file.write('\\maketitle\n')

    def _write_file_suffix(self) -> None:
        """Write LaTeX document ending unless provided in preamble."""
        assert self.file is not None
        if self._preamble_has_end_document():
            return
        self.file.write('\n\\end{document}\n')

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        self._ensure_blank_line_before()

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        assert self.file is not None
        self.file.write('\n')

    def _start_block_quote(self) -> None:
        """Start a block quote."""
        assert self.file is not None
        self._ensure_blank_line_before()
        self.file.write('\\begin{quote}\n')

    def _end_block_quote(self) -> None:
        """End a block quote."""
        assert self.file is not None
        self.file.write('\n\\end{quote}\n')

    def _start_heading(self, level: int) -> None:
        """Start a heading."""
        self._ensure_blank_line_before()
        command = self._heading_command(level)
        self._write_with_stage_three_replacements(f'\\{command}{{')

    def _end_heading(self, level: int) -> None:
        """End a heading."""
        _ = level  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('}\n')

    def _write_text(self, text: str, state: MultiFormatState,
                    formatting: Formatting) -> None:
        """Write text into current item (paragraph, bullet list item...)."""
        _ = state  # pylint: disable=unused-variable
        formatted = self._format_text(text=text, formatting=formatting)
        self._write_with_stage_three_replacements(formatted)

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   formatting: Formatting) -> None:
        """Write a URL into current item (paragraph, bullet list item...)."""
        _ = state  # pylint: disable=unused-variable
        safe_url = self._escape_latex_text(url)
        if text:
            url_text = f'\\href{{{safe_url}}}{{{text}}}'
        else:
            url_text = f'\\url{{{safe_url}}}'
        self._write_with_stage_three_replacements(
            self._format_text(text=url_text, formatting=formatting))

    def _write_code_in_text(self, text: str,
                            state: MultiFormatState) -> None:
        """Write code into current item (paragraph, bullet list item...)."""
        _ = state  # pylint: disable=unused-variable
        leading, stripped, trailing = split_whitespace(text)
        code_text = f'{leading}\\texttt{{{stripped}}}{trailing}'
        self._write_with_stage_three_replacements(code_text)

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list."""
        _ = level  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\\begin{itemize}\n')

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list."""
        _ = level  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\\end{itemize}\n')

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item."""
        _ = level  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\\item ')

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item."""
        _ = level  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\n')

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list."""
        _ = level  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\\begin{enumerate}\n')

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list."""
        _ = level  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\\end{enumerate}\n')

    def _start_numbered_item(self, level: int, num: int,
                             full_number: str) -> None:
        """Start a numbered item."""
        _ = level  # pylint: disable=unused-variable
        _ = num  # pylint: disable=unused-variable
        _ = full_number  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\\item ')

    def _end_numbered_item(self, level: int, num: int) -> None:
        """End a numbered item."""
        _ = level  # pylint: disable=unused-variable
        _ = num  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\n')

    def _start_table(self, num_columns: int) -> None:
        """Start a table."""
        _ = num_columns  # pylint: disable=unused-variable
        self._ensure_blank_line_before()
        self._latex_table_rows = []

    def _end_table(self, num_columns: int, num_rows: int) -> None:
        """End a table."""
        _ = num_rows  # pylint: disable=unused-variable
        assert self.file is not None
        column_spec = self._tabular_spec(num_columns)
        self.file.write(f'\\begin{{tabular}}{{{column_spec}}}\n')
        self.file.write('\\hline\n')
        for row in self._latex_table_rows:
            self.file.write(' & '.join(row))
            self.file.write(' \\\\\n')
            self.file.write('\\hline\n')
        self.file.write('\\end{tabular}\n')
        self._latex_table_rows = []

    def _write_table_first_row(self, first_row: list[str],
                               formatting: Formatting) -> None:
        """Write the first row of the table."""
        row = [self._apply_latex_replacements(
            self._format_text(text=cell, formatting=formatting),
            stage=2) for cell in first_row]
        self._latex_table_rows.append(row)

    def _write_table_row(self, row: list[str],
                         formatting: Formatting, row_number: int) -> None:
        """Write a row of the table."""
        assert self.table is not None
        if len(row) != self.table.number_of_columns:
            errmsg = f'Row {row_number} has {len(row)} columns, but '
            errmsg += f'table has {self.table.number_of_columns} columns.'
            raise ValueError(errmsg)
        local_row = [self._apply_latex_replacements(
            self._format_text(text=cell, formatting=formatting),
            stage=2) for cell in row]
        self._latex_table_rows.append(local_row)

    def _start_code_block(self, programming_language: Optional[str]) -> None:
        """Start a code block.

        The programming_language argument is accepted but ignored.
        """
        _ = programming_language  # pylint: disable=unused-variable
        assert self.file is not None
        self._ensure_blank_line_before()
        self.file.write('\\begin{verbatim}\n')

    def _end_code_block(self, programming_language: Optional[str]) -> None:
        """End a code block.

        The programming_language argument is accepted but ignored.
        """
        _ = programming_language  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write('\n\\end{verbatim}\n')

    def _write_code_block(self, text: str,
                          programming_language: Optional[str]) -> None:
        """Write a code block.

        The programming_language argument is accepted but ignored.
        """
        _ = programming_language  # pylint: disable=unused-variable
        assert self.file is not None
        self.file.write(text)

    def _encode_text(self, text: str) -> str:
        """Encode text (escape special characters)."""
        if not text:
            return text
        if self.state == MultiFormatState.CODE_BLOCK:
            return text
        result = deepcopy(text)
        result = self._apply_latex_replacements(result, stage=0)
        result = self._escape_latex_text(result)
        result = self._apply_latex_replacements(result, stage=1)
        return result
