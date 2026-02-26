#! /usr/local/bin/python3
"""Test the mformat_textbased module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
from pathlib import Path
import pytest
from check_capsys import check_capsys
from mformat.mformat_textbased import MultiFormatTextBased
from mformat.mformat_state import MultiFormatState


class MultiFormatTextBased2(MultiFormatTextBased):
    """Test class for the mformat_textbased module."""

    @classmethod
    def file_name_extension(cls) -> str:
        """Test the file_name_extension method."""
        return '.test'

    def _end_paragraph(self) -> None:
        """Mock the end_paragraph method."""

    def _write_file_suffix(self) -> None:
        """Mock the write_file_suffix method."""


@pytest.mark.parametrize('fname', ['a.test', 'b.test', 'c.test'])
def test_open_close_context_manager(capsys, fname):
    """Test the open and close methods."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / fname)
        with MultiFormatTextBased2(file_name=file_name) as mf:
            mf.state = MultiFormatState.PARAGRAPH
            assert mf.file_name == file_name
            assert mf.file is not None
            assert mf.file.name == file_name
            assert mf.file.closed is False
        assert mf.file is None
        assert Path(file_name).exists()
    check_capsys(capsys)


@pytest.mark.parametrize('fname', ['a.test', 'b.test', 'c.test'])
def test_open_close_manual(capsys, fname):
    """Test the open and close methods."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / fname)
        mf = MultiFormatTextBased2(file_name=file_name)
        mf.open()
        mf.state = MultiFormatState.PARAGRAPH
        assert mf.file is not None
        assert mf.file.name == file_name
        assert mf.file.closed is False
        mf.close()
        assert mf.file is None
        assert Path(file_name).exists()
    check_capsys(capsys)


@pytest.mark.parametrize('fname', ['a.test', 'b.test', 'c.test'])
def test_close_only(capsys, fname):
    """Test only the close method when the file is not open."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / fname)
        mf = MultiFormatTextBased2(file_name=file_name)
        mf.state = MultiFormatState.PARAGRAPH
        assert mf.file is None
        assert not Path(file_name).exists()
        mf.close()
        assert mf.file is None
        assert not Path(file_name).exists()
    check_capsys(capsys)


@pytest.mark.parametrize('wr1,wr2,wr1end,num',
                         [('Hello ', 'world!', 'lo ', 3),
                          ('Hi', ' Earth!', 'Hi', 5),
                          ('What a', ' beautiful day!', 'at a', 4)])
def test_get_last_chars_written(capsys, wr1, wr2, wr1end, num):
    """Test the get_last_chars_written method."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / 'test.test')
        with MultiFormatTextBased2(file_name=file_name) as mf:
            assert mf.file is not None
            mf.file.write(wr1)
            # pylint: disable=protected-access
            assert mf._get_last_chars_written(num) == wr1end
            mf.file.write(wr2)
        with open(file=file_name, mode='rt', encoding='utf-8') as file:
            content = file.read()
            assert content == wr1 + wr2
    check_capsys(capsys)
