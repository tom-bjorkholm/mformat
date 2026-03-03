#! /usr/local/bin/python3
"""Test factory integration for reStructuredText formatter."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from mformat.factory import OptArgs, create_mf, filter_args_mf
from mformat.mformat_rst import MultiFormatRst
from mformat.plain_text_table import TableAlignment
from .check_capsys import check_capsys
from .test_helpers import FileExistsCallbackCounter


@pytest.mark.parametrize('format_name', ['reST', 'REST'])
def test_create_mf_rst_returns_rst_formatter(
        capsys: pytest.capturefixture[str], format_name: str) -> None:
    """Test create_mf creates MultiFormatRst (case-insensitive)."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.rst')
        with create_mf(format_name, file_name) as mfd:
            assert isinstance(mfd, MultiFormatRst)
            assert mfd.file_name == file_name
    check_capsys(capsys)


def test_create_mf_rst_optional_args(
        capsys: pytest.capturefixture[str]) -> None:
    """Test create_mf passes optional reST args to constructor."""
    expected: OptArgs = {
        'line_length': 42,
        'table_max_line_length': 26,
        'table_alignment': TableAlignment.RIGHT,
    }
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        with create_mf('reST', file_name, args=expected) as mfd:
            assert isinstance(mfd, MultiFormatRst)
            assert mfd.file_name.endswith('.rst')
            assert {
                'line_length': mfd.line_length,
                'table_max_line_length': mfd.table_max_line_length,
                'table_alignment': mfd.table_alignment,
            } == expected
    check_capsys(capsys)


def test_create_mf_rst_invalid_line_length(
        capsys: pytest.capturefixture[str]) -> None:
    """Test constructor validation is propagated through create_mf."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.rst')
        with pytest.raises(ValueError) as exc:
            _ = create_mf('reST', file_name, args={'line_length': 10})
        assert exc.value.args[0] == \
            'Line length must be greater than 10, got 10'
    check_capsys(capsys)


def test_filter_args_mf_for_rst(capsys: pytest.capturefixture[str]) -> None:
    """Test filter_args_mf keeps reST args and ignores others."""
    args: OptArgs = {
        'line_length': 42,
        'table_max_line_length': 26,
        'table_alignment': TableAlignment.LEFT,
        'title': 'not used by rest',
    }
    assert filter_args_mf(args=args, format_name='reST') == {
        'line_length': 42,
        'table_max_line_length': 26,
        'table_alignment': TableAlignment.LEFT,
    }
    check_capsys(capsys)


def test_create_mf_rst_file_exists_callback(
        capsys: pytest.capturefixture[str]) -> None:
    """Test file_exists_callback is passed through create_mf for reST."""
    callback = FileExistsCallbackCounter()
    with TemporaryDirectory() as tmp_dir:
        file_name = Path(tmp_dir) / 'test.rst'
        file_name.write_text('old content', encoding='utf-8')
        with create_mf('reST', file_name,
                       args={'file_exists_callback': callback}) as mfd:
            assert isinstance(mfd, MultiFormatRst)
            mfd.new_heading(level=1, text='New heading')
        assert file_name.read_text(encoding='utf-8').startswith('New heading')
    assert (callback.called, callback.last_file_name.endswith('.rst')) == \
        (1, True)
    check_capsys(capsys)
