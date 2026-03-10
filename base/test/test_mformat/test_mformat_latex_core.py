#! /usr/local/bin/python3
"""Test core functionality of the LaTeX formatter."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import pytest
from mformat.document_class import DocumentClass
from mformat.mformat import FormatterDescriptor
from mformat.mformat_latex import MultiFormatLatex
from mformat.paper_size import PaperSize
from .check_capsys import check_capsys
from .test_helpers import (check_formatter_character_encoding,
                           check_invalid_character_encoding_constructor,
                           check_run_with_context_manager)


def test_file_name_extension(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file_name_extension method."""
    assert MultiFormatLatex.file_name_extension() == '.tex'
    check_capsys(capsys)


def test_get_arg_desciption(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_arg_desciption method."""
    assert MultiFormatLatex.get_arg_desciption() == FormatterDescriptor(
        name='LaTeX', mandatory_args=[],
        optional_args=['character_encoding', 'title', 'document_class',
                       'paper_size', 'latex_preamble',
                       'latex_heading_levels', 'latex_replacements'])
    check_capsys(capsys)


def test_constructor_defaults(capsys: pytest.CaptureFixture[str]) -> None:
    """Test constructor defaults."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatLatex(file_name=file_name)
        assert mfd.file_name == file_name + '.tex'
        assert mfd.document_class == DocumentClass.REPORT
        assert mfd.paper_size == PaperSize.A4
        assert mfd.title is None
        assert mfd.heading_levels[1] == 'chapter'
        assert mfd.heading_levels[6] == 'subparagraph'
    check_capsys(capsys)


def test_constructor_paper_size_with_documentclass_in_preamble(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test that paper_size is rejected with preamble documentclass."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        with pytest.raises(ValueError) as exc:
            _ = MultiFormatLatex(
                file_name=file_name,
                paper_size='A4',
                latex_preamble='\\documentclass[a4paper]{report}\n')
    assert exc.value.args[0] == (
        'paper_size cannot be used if the latex_preamble string contains '
        'the substring "\\documentclass"')
    check_capsys(capsys)


def test_heading_fallback_deepest(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading fallback to deepest known command."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_heading(level=9, text='Deep')

    expected = (
        '\\documentclass[a4paper]{article}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        '\\subparagraph{Deep}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, args={'document_class': DocumentClass.ARTICLE},
        capsys=capsys)


def test_custom_heading_mapping(capsys: pytest.CaptureFixture[str]) -> None:
    """Test custom heading command mapping."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_heading(level=2, text='Mapped')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        '\\myheading{Mapped}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected,
        args={'latex_heading_levels': {2: '\\myheading'}},
        capsys=capsys)


def test_title_with_begin_document_in_preamble(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test title handling when preamble already has begin document."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='x')

    preamble = '\\documentclass[a4paper]{report}\n\\begin{document}\n'
    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\begin{document}\n'
        '\\title{My Title}\n'
        '\\maketitle\n\n'
        'x\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected,
        args={'title': 'My Title', 'latex_preamble': preamble},
        capsys=capsys)


def test_add_url_escapes_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test URL emission and escaping in href argument."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='See')
        mfd.add_url(url='http://example.com?a=1&b=2', text='Link')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        'See \\href{http://example.com?a=1\\&b=2}{Link}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_dash_conversion_in_prose(capsys: pytest.CaptureFixture[str]) -> None:
    """Test conversion from space-dash-space to em dash in prose."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='A - B')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        'A --- B\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_dash_not_converted_in_code_in_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test that code in text keeps dashes unchanged."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='Code:')
        mfd.add_code_in_text(text='A - B')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        'Code: \\texttt{A - B}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_code_in_text_escapes_underscores_in_heading(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test that code in heading escapes LaTeX special characters."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_heading(level=1, text='Code')
        mfd.add_code_in_text(text='add_code_in_text()')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        '\\chapter{Code \\texttt{add\\_code\\_in\\_text()}}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_angle_brackets_are_escaped_in_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test that angle brackets are escaped in plain text."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='Tag <html>')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        'Tag \\textless{}html\\textgreater{}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_replacements_apply_in_code_in_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test replacement stages are applied for inline code."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='Code:')
        mfd.add_code_in_text(text='x')

    replacements = [{'x': '&'}, {'\\&': 'AND'}, {}]
    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        'Code: \\texttt{AND}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected,
        args={'latex_replacements': replacements},
        capsys=capsys)


def test_replacements_apply_in_code_block_without_escaping(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test replacement stages in code blocks without text escaping."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.write_code_block(text='x & y')

    replacements = [{'x': '<'}, {'<': 'LT'}, {}]
    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        '\\begin{verbatim}\n'
        'LT & y\n'
        '\\end{verbatim}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected,
        args={'latex_replacements': replacements},
        capsys=capsys)


def test_write_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test LaTeX code block output."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.write_code_block(text='A - B')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        '\\begin{verbatim}\n'
        'A - B\n'
        '\\end{verbatim}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_write_table(capsys: pytest.CaptureFixture[str]) -> None:
    """Test simple LaTeX table output."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_table(first_row=['H1', 'H2'])
        mfd.add_table_row(row=['a', 'b'])

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        '\\noindent\n'
        '\\begin{tabular}{ll}\n'
        '\\toprule\n'
        'H1 & H2 \\\\\n'
        '\\midrule\n'
        'a & b \\\\\n'
        '\\bottomrule\n'
        '\\end{tabular}\n'
        '\\par\\medskip\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_write_table_fallback_without_booktabs_package(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test fallback table style when booktabs cannot be injected."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_table(first_row=['H1', 'H2'])
        mfd.add_table_row(row=['a', 'b'])

    preamble = '\\documentclass[a4paper]{report}\n\\begin{document}\n'
    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\begin{document}\n\n'
        '\\noindent\n'
        '\\begin{tabular}{|l|l|}\n'
        '\\hline\n'
        'H1 & H2 \\\\\n'
        '\\hline\n'
        'a & b \\\\\n'
        '\\hline\n'
        '\\end{tabular}\n'
        '\\par\\medskip\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, args={'latex_preamble': preamble},
        capsys=capsys)


def test_replacement_pipeline(capsys: pytest.CaptureFixture[str]) -> None:
    """Test replacement stages around escaping and LaTeX commands."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='x', bold=True)

    replacements = [{'x': '&'}, {'\\&': 'AND'}, {'\\textbf': '\\Strong'}]
    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        '\\Strong{AND}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected,
        args={'latex_replacements': replacements},
        capsys=capsys)


@pytest.mark.parametrize('character_encoding, expected_text_bytes',
                         [('utf-8', b'Caf\xc3\xa9'),
                          ('iso-8859-1', b'Caf\xe9')])
def test_character_encoding(capsys: pytest.CaptureFixture[str],
                            character_encoding: str,
                            expected_text_bytes: bytes) -> None:
    """Test selected encoding output for LaTeX formatter."""
    check_formatter_character_encoding(
        formatter_class=MultiFormatLatex,
        file_extension='.tex',
        character_encoding=character_encoding,
        expected_text_bytes=expected_text_bytes)
    check_capsys(capsys)


def test_invalid_character_encoding(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test invalid encoding is propagated from Python open."""
    check_invalid_character_encoding_constructor(
        formatter_class=MultiFormatLatex,
        file_extension='.tex')
    check_capsys(capsys)
