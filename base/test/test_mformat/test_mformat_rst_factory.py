#! /usr/local/bin/python3
"""Test factory integration for reStructuredText formatter."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#
# pylint: disable=duplicate-code

from tempfile import TemporaryDirectory
from pathlib import Path
import pytest
from check_capsys import check_capsys
from mformat.factory import create_mf, filter_args_mf
from mformat.mformat_rst import MultiFormatRst
from mformat.plain_text_table import TableAlignment


class FileExistsCallbackCounter:  # pylint: disable=too-few-public-methods
    """Count callback calls for existing file checks."""

    def __init__(self):
        """Initialize callback counter."""
        self.called = 0
        self.last_file_name = ''

    def __call__(self, file_name: str):
        """Record callback invocation."""
        self.called += 1
        self.last_file_name = file_name


def test_create_mf_rst_returns_rst_formatter(capsys):
    """Test create_mf creates MultiFormatRst."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.rst')
        with create_mf('reST', file_name) as mfd:
            assert isinstance(mfd, MultiFormatRst)
            assert mfd.file_name == file_name
    check_capsys(capsys)


def test_create_mf_rst_is_case_insensitive(capsys):
    """Test create_mf accepts REST format in upper case."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.rst')
        with create_mf('REST', file_name) as mfd:
            assert isinstance(mfd, MultiFormatRst)
    check_capsys(capsys)


def test_create_mf_rst_optional_args(capsys):
    """Test create_mf passes optional reST args to constructor."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test')
        args = {
            'line_length': 42,
            'table_max_line_length': 26,
            'table_alignment': TableAlignment.RIGHT,
        }
        with create_mf('reST', file_name, args=args) as mfd:
            assert isinstance(mfd, MultiFormatRst)
            assert mfd.file_name.endswith('.rst')
            assert mfd.line_length == 42
            assert mfd.table_max_line_length == 26
            assert mfd.table_alignment == TableAlignment.RIGHT
    check_capsys(capsys)


def test_create_mf_rst_invalid_line_length(capsys):
    """Test constructor validation is propagated through create_mf."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.rst')
        with pytest.raises(ValueError) as exc:
            _ = create_mf('reST', file_name, args={'line_length': 10})
        assert exc.value.args[0] == \
            'Line length must be greater than 10, got 10'
    check_capsys(capsys)


def test_filter_args_mf_for_rst(capsys):
    """Test filter_args_mf keeps reST args and ignores others."""
    args = {
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


def test_create_mf_rst_file_exists_callback(capsys):
    """Test file_exists_callback is passed through create_mf for reST."""
    callback = FileExistsCallbackCounter()
    with TemporaryDirectory() as tmp_dir:
        file_name = Path(tmp_dir) / 'test.rst'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write('old content')
        with create_mf('reST', file_name,
                       args={'file_exists_callback': callback}) as mfd:
            assert isinstance(mfd, MultiFormatRst)
            mfd.new_heading(level=1, text='New heading')
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            assert 'old content' not in content
            assert 'New heading' in content
    assert callback.called == 1
    assert callback.last_file_name.endswith('test.rst')
    check_capsys(capsys)
