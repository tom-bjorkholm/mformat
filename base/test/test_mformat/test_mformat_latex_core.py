#! /usr/local/bin/python3
"""Test core functionality of the LaTeX formatter."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import pytest
from mformat import mformat_latex as mformat_latex_module
from mformat.document_class import DocumentClass
from mformat.mformat import FormatterDescriptor
from mformat.mformat_latex import MultiFormatLatex
from mformat.mformat_state import Formatting, MultiFormatState
from mformat.paper_size import PaperSize
from .check_capsys import check_capsys
from .test_helpers import (check_formatter_character_encoding,
                           check_invalid_character_encoding_constructor,
                           check_run_with_context_manager,
                           run_with_context_manager)


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


@pytest.mark.parametrize(
    'kwargs, expected_message',
    [
        ({'latex_preamble': None},
         'latex_preamble must be a string'),
        ({'latex_heading_levels': []},
         'latex_heading_levels must be a dictionary'),
        ({'latex_heading_levels': {'1': 'section'}},
         'latex_heading_levels must contain only int keys'),
        ({'latex_heading_levels': {1: 2}},
         'latex_heading_levels must contain only str values'),
        ({'latex_replacements': {}},
         'latex_replacements must be a list'),
        ({'latex_replacements': [{}, {}]},
         'latex_replacements must contain 3 dictionaries'),
        ({'latex_replacements': [{'ok': 'value'}, {}, {1: 'bad'}]},
         'latex_replacements dictionaries must contain only str keys and '
         'str values'),
        ({'title': 7},
         'title must be a string'),
    ])
def test_constructor_validation_errors(
        capsys: pytest.CaptureFixture[str],
        kwargs: dict[str, Any],
        expected_message: str) -> None:
    """Test constructor validation for malformed optional arguments."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        with pytest.raises(ValueError) as exc:
            _ = MultiFormatLatex(file_name=file_name, **kwargs)
    assert exc.value.args[0] == expected_message
    check_capsys(capsys)


def test_constructor_raises_when_default_heading_levels_are_missing(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test constructor rejects document classes without heading mapping."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        # pylint: disable=protected-access
        monkeypatch.delitem(
            mformat_latex_module._DEF_LATEX_HEADING_LEVELS,
            DocumentClass.REPORT)
        with pytest.raises(ValueError) as exc:
            _ = MultiFormatLatex(file_name=file_name)
    assert exc.value.args[0] == (
        'document_class REPORT has no default heading levels')
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
        '\\usepackage{xurl}\n'
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
        '\\usepackage{xurl}\n'
        '\\begin{document}\n\n'
        '\\myheading{Mapped}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected,
        args={'latex_heading_levels': {2: '\\myheading'}},
        capsys=capsys)


def test_normalize_latex_command_rejects_empty_commands(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test empty LaTeX command names are rejected."""
    with pytest.raises(ValueError) as exc:
        # pylint: disable=protected-access
        _ = MultiFormatLatex._normalize_latex_command(' \\ ')
    assert exc.value.args[0] == 'LaTeX command name cannot be empty'
    check_capsys(capsys)


@pytest.mark.parametrize(
    'level, expected',
    [
        (1, 'subsection'),
        (4, 'subsection'),
    ])
def test_heading_command_fallbacks(
        capsys: pytest.CaptureFixture[str],
        level: int,
        expected: str) -> None:
    """Test heading command lookup for shallow and intermediate fallbacks."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatLatex(file_name=file_name)
        mfd.heading_levels = {3: 'subsection', 5: 'paragraph'}
        # pylint: disable=protected-access
        assert mfd._heading_command(level) == expected
    check_capsys(capsys)


def test_heading_command_raises_when_no_levels_are_configured(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading lookup fails clearly when no levels are configured."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatLatex(file_name=file_name)
        mfd.heading_levels = {}
        with pytest.raises(RuntimeError) as exc:
            # pylint: disable=protected-access
            mfd._heading_command(level=2)
    assert exc.value.args[0] == 'No heading levels are configured'
    check_capsys(capsys)


def test_use_booktabs_tables_returns_true_for_existing_package(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test existing booktabs package forces booktabs table output."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatLatex(file_name=file_name)
        # pylint: disable=protected-access
        assert mfd._use_booktabs_tables(
            has_docclass=True,
            has_begin_document=True,
            has_booktabs_package=True)
    check_capsys(capsys)


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


@pytest.mark.parametrize('before', ['Alpha\n', 'Alpha'])
def test_ensure_blank_line_before_adds_needed_spacing(
        capsys: pytest.CaptureFixture[str], before: str) -> None:
    """Test blank-line insertion after partial or non-newline endings."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatLatex(file_name=file_name)
        mfd.open()
        assert mfd.file is not None
        mfd.file.write(before)
        mfd._ensure_blank_line_before()  # pylint: disable=protected-access
        mfd._close()  # pylint: disable=protected-access
        assert Path(mfd.file_name).read_text(encoding='utf-8') == 'Alpha\n\n'
    check_capsys(capsys)


@pytest.mark.parametrize('before', ['', '\n\n'])
def test_ensure_blank_line_before_is_noop_for_blank_or_empty_state(
        capsys: pytest.CaptureFixture[str], before: str) -> None:
    """Test blank-line helper leaves empty or already blank-separated text."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatLatex(file_name=file_name)
        mfd.open()
        assert mfd.file is not None
        mfd.file.write(before)
        mfd._ensure_blank_line_before()  # pylint: disable=protected-access
        mfd._close()  # pylint: disable=protected-access
        assert Path(mfd.file_name).read_text(encoding='utf-8') == before
    check_capsys(capsys)


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
        '\\usepackage{xurl}\n'
        '\\begin{document}\n\n'
        'See \\penalty0'
        '\\href{http://example.com?a=1\\&b=2}{Link}'
        '\\penalty0\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_add_url_without_text_uses_url_command(
        capsys: pytest.CaptureFixture[str]) -> None:
    r"""Test URL emission without link text uses \url with break hints."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='See')
        mfd.add_url(url='http://example.com/a?x=1&y=2')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\usepackage{xurl}\n'
        '\\begin{document}\n\n'
        'See \\penalty0\\url{http://example.com/a?x=1\\&y=2}\\penalty0\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_add_url_as_text_adds_needed_space(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test url_as_text mode keeps readable spacing before raw URL text."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='Prefix:')
        mfd.add_url(url='https://example.com')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        'Prefix: https://example.com\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, url_as_text=True, capsys=capsys)


def test_dash_conversion_in_prose(capsys: pytest.CaptureFixture[str]) -> None:
    """Test conversion from space-dash-space to em dash in prose."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='A - B')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\usepackage{xurl}\n'
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
        '\\usepackage{xurl}\n'
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
        '\\usepackage{xurl}\n'
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
        '\\usepackage{xurl}\n'
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
        '\\usepackage{xurl}\n'
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
        '\\usepackage{xurl}\n'
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
        '\\usepackage{xurl}\n'
        '\\begin{document}\n\n'
        '\\begin{verbatim}\n'
        'A - B\n'
        '\\end{verbatim}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected, capsys=capsys)


def test_docclass_preamble_injects_required_packages(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test docclass-only preambles gain the needed package lines."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_paragraph(text='x')

    expected = (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{xurl}\n'
        '\\usepackage{booktabs}\n'
        '\\begin{document}\n\n'
        'x\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected,
        args={'latex_preamble': '\\documentclass[a4paper]{report}'},
        capsys=capsys)


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
        '\\usepackage{xurl}\n'
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
        '\\usepackage{xurl}\n'
        '\\begin{document}\n\n'
        '\\Strong{AND}\n\n'
        '\\end{document}\n')
    check_run_with_context_manager(
        format_name='LaTeX', file_extension='.tex', test_action=test_action,
        expected_text=expected,
        args={'latex_replacements': replacements},
        capsys=capsys)


def test_write_table_row_reports_row_number(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test _write_table_row reports row number in error messages."""

    def test_action(mfd: Any) -> None:
        assert isinstance(mfd, MultiFormatLatex)
        mfd.new_table(first_row=['Name', 'Age', 'City'])
        mismatched_row = ['Alice', '30']
        formatting = Formatting(bold=False, italic=False)
        mfd._write_table_row(  # pylint: disable=protected-access
            row=mismatched_row,
            formatting=formatting,
            row_number=2)

    with pytest.raises(ValueError) as exc:
        _ = run_with_context_manager('LaTeX', '.tex', test_action)
    assert exc.value.args[0] == 'Row 2 has 2 columns, but table has 3 columns.'
    check_capsys(capsys)


def test_write_file_suffix_skips_duplicate_end_document(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test suffix writer stays silent when preamble already ends the file."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatLatex(
            file_name=file_name,
            latex_preamble='\\documentclass{report}\n\\end{document}\n')
        mfd.open()
        mfd._write_file_suffix()  # pylint: disable=protected-access
        mfd._close()  # pylint: disable=protected-access
        assert Path(mfd.file_name).read_text(encoding='utf-8') == ''
    check_capsys(capsys)


def test_encode_text_returns_empty_string_unchanged(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test empty strings are returned unchanged during LaTeX encoding."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        mfd = MultiFormatLatex(file_name=file_name)
        # pylint: disable=protected-access
        assert mfd._encode_text('') == ''
        mfd.state = MultiFormatState.CODE_BLOCK
        assert mfd._encode_text('') == ''
    check_capsys(capsys)


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
