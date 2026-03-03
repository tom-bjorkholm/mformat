#! /usr/local/bin/python3
"""Test factory integration for TXT formatter."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from mformat.factory import OptArgs, create_mf, filter_args_mf
from mformat.mformat_txt import MultiFormatTxt
from mformat.plain_text_table import TableAlignment
from .check_capsys import check_capsys
from .test_helpers import FileExistsCallbackCounter


def test_create_mf_txt_returns_txt_formatter(capsys):
    """Test create_mf creates MultiFormatTxt."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.txt')
        with create_mf('txt', file_name) as mfd:
            assert isinstance(mfd, MultiFormatTxt)
            assert mfd.file_name == file_name
    check_capsys(capsys)


def test_create_mf_txt_is_case_insensitive(capsys):
    """Test create_mf accepts TXT format in upper case."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.txt')
        with create_mf('TXT', file_name) as mfd:
            assert isinstance(mfd, MultiFormatTxt)
    check_capsys(capsys)


def test_create_mf_txt_optional_args(capsys):
    """Test create_mf passes optional TXT args to constructor."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        args: OptArgs = {
            'line_length': 42,
            'table_max_line_length': 26,
            'table_alignment': TableAlignment.LEFT,
        }
        with create_mf('txt', file_name, args=args) as mfd:
            assert isinstance(mfd, MultiFormatTxt)
            assert mfd.file_name.endswith('.txt')
            assert mfd.line_length == 42
            assert mfd.table_max_line_length == 26
            assert mfd.table_alignment == TableAlignment.LEFT
    check_capsys(capsys)


def test_create_mf_txt_invalid_line_length(capsys):
    """Test constructor validation is propagated through create_mf."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.txt')
        with pytest.raises(ValueError) as exc:
            _ = create_mf('txt', file_name, args={'line_length': 10})
        assert exc.value.args[0] == 'Line length must be greater than 10, '\
            'got 10'
    check_capsys(capsys)


def test_filter_args_mf_for_txt(capsys):
    """Test filter_args_mf keeps TXT args and ignores others."""
    args: OptArgs = {
        'line_length': 42,
        'table_max_line_length': 26,
        'table_alignment': TableAlignment.RIGHT,
        'title': 'not used by txt',
    }
    assert filter_args_mf(args=args, format_name='txt') == {
        'line_length': 42,
        'table_max_line_length': 26,
        'table_alignment': TableAlignment.RIGHT,
    }
    check_capsys(capsys)


def test_create_mf_txt_file_exists_callback(capsys):
    """Test file_exists_callback is passed through create_mf for TXT."""
    callback = FileExistsCallbackCounter()
    with TemporaryDirectory() as tmp_dir:
        file_name = Path(tmp_dir) / 'test.txt'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write('old content')
        with create_mf('txt', file_name,
                       args={'file_exists_callback': callback}) as mfd:
            assert isinstance(mfd, MultiFormatTxt)
            mfd.new_heading(level=1, text='New heading')
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            assert 'old content' not in content
            assert 'New heading' in content
    assert callback.called == 1
    assert callback.last_file_name.endswith('test.txt')
    check_capsys(capsys)
