#! /usr/local/bin/python3
"""Test factory integration for LaTeX formatter."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from mformat.document_class import DocumentClass
from mformat.factory import OptArgs, create_mf, filter_args_mf
from mformat.mformat_latex import MultiFormatLatex
from mformat.paper_size import PaperSize
from .check_capsys import check_capsys
from .test_helpers import FileExistsCallbackCounter


@pytest.mark.parametrize('format_name', ['LaTeX', 'latex', 'LATEX'])
def test_create_mf_latex_returns_formatter(
        capsys: pytest.CaptureFixture[str], format_name: str) -> None:
    """Test create_mf creates MultiFormatLatex case-insensitively."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.tex')
        with create_mf(format_name, file_name) as mfd:
            assert isinstance(mfd, MultiFormatLatex)
            assert mfd.file_name == file_name
    check_capsys(capsys)


def test_create_mf_latex_optional_args(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test create_mf passes optional LaTeX args to constructor."""
    replacements = [{}, {}, {'\\textbf': '\\Strong'}]
    args: OptArgs = {
        'document_class': DocumentClass.BOOK,
        'paper_size': PaperSize.LETTER,
        'title': 'My title',
        'latex_preamble': '\\usepackage{xcolor}\n',
        'latex_heading_levels': {2: '\\myheading'},
        'latex_replacements': replacements,
    }
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        with create_mf('LaTeX', file_name, args=args) as mfd:
            assert isinstance(mfd, MultiFormatLatex)
            assert mfd.file_name.endswith('.tex')
            assert mfd.document_class == DocumentClass.BOOK
            assert mfd.paper_size == PaperSize.LETTER
            assert mfd.title == 'My title'
            assert mfd.latex_preamble == '\\usepackage{xcolor}\n'
            assert mfd.heading_levels[2] == 'myheading'
            assert mfd.latex_replacements == replacements
    check_capsys(capsys)


def test_create_mf_latex_invalid_paper_size_and_preamble(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test constructor validation is propagated through create_mf."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.tex')
        with pytest.raises(ValueError) as exc:
            _ = create_mf('LaTeX', file_name, args={
                'paper_size': PaperSize.A4,
                'latex_preamble': '\\documentclass[a4paper]{report}\n',
            })
        assert exc.value.args[0] == (
            'paper_size cannot be used if the latex_preamble string '
            'contains the substring "\\documentclass"')
    check_capsys(capsys)


def test_filter_args_mf_for_latex(capsys: pytest.CaptureFixture[str]) -> None:
    """Test filter_args_mf keeps LaTeX args and ignores others."""
    callback = FileExistsCallbackCounter()
    args: OptArgs = {
        'file_exists_callback': callback,
        'document_class': DocumentClass.REPORT,
        'paper_size': PaperSize.A4,
        'title': 'My title',
        'latex_preamble': '\\usepackage{xcolor}\n',
        'latex_heading_levels': {3: 'custom'},
        'latex_replacements': [{}, {}, {}],
        'line_length': 42,
        'css_file': 'ignored.css',
    }
    filtered = filter_args_mf(args=args, format_name='LaTeX')
    assert filtered == {
        'file_exists_callback': callback,
        'document_class': DocumentClass.REPORT,
        'paper_size': PaperSize.A4,
        'title': 'My title',
        'latex_preamble': '\\usepackage{xcolor}\n',
        'latex_heading_levels': {3: 'custom'},
        'latex_replacements': [{}, {}, {}],
    }
    check_capsys(capsys)


def test_create_mf_latex_file_exists_callback(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test file_exists_callback is passed through create_mf for LaTeX."""
    callback = FileExistsCallbackCounter()
    with TemporaryDirectory() as tmp_dir:
        file_name = Path(tmp_dir) / 'test.tex'
        file_name.write_text('old content', encoding='utf-8')
        with create_mf('LaTeX', file_name,
                       args={'file_exists_callback': callback}) as mfd:
            assert isinstance(mfd, MultiFormatLatex)
            mfd.new_heading(level=1, text='New heading')
        assert file_name.read_text(encoding='utf-8').find('old content') < 0
        assert file_name.read_text(encoding='utf-8').find('New heading') >= 0
    assert callback.called == 1
    assert callback.last_file_name.endswith('.tex')
    check_capsys(capsys)
