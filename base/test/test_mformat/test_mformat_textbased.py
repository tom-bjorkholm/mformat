#! /usr/local/bin/python3
"""Test the mformat_textbased module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from mformat.mformat_state import MultiFormatState
from mformat.mformat_textbased import MultiFormatTextBased
from .check_capsys import check_capsys
from .test_helpers import check_invalid_character_encoding_constructor


class MultiFormatTextBased2(MultiFormatTextBased):
    """Test class for the mformat_textbased module."""

    def __enter__(self) -> 'MultiFormatTextBased2':
        """Enter the context manager."""
        super().__enter__()
        return self

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


@pytest.mark.parametrize('num', [1, 2, 3, 4, 5, 6, 7, 8])
@pytest.mark.parametrize('laststr',
                         ['ÅÄÖßåäö', 'å\nÄ\nÖ\nÅ\nß\nä\nö\n',
                          'øæÆØ😀👍\n😀👍\n'])
@pytest.mark.parametrize('last_times', [1, 2, 4])
@pytest.mark.parametrize('bytes_before', [0, 20, 100])
def test_get_last_chars_written2(capsys, num, laststr,
                                 last_times, bytes_before):
    """Test the get_last_chars_written method."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / 'test.test')
        with MultiFormatTextBased2(file_name=file_name) as mf:
            assert mf.file is not None
            mf.file.write('a' * bytes_before)
            for _ in range(last_times):
                mf.file.write(laststr)
            last = mf._get_last_chars_written(num)  # pylint: disable=protected-access # noqa: E501
            assert last == laststr[-num:]
    check_capsys(capsys)


@pytest.mark.parametrize('character_encoding, expected_bytes',
                         [('utf-8', b'Caf\xc3\xa9'),
                          ('iso-8859-1', b'Caf\xe9')])
def test_open_writes_selected_character_encoding(
        capsys, character_encoding, expected_bytes):
    """Test that open uses the selected character encoding."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / 'test.test')
        with MultiFormatTextBased2(
                file_name=file_name,
                character_encoding=character_encoding) as mf:
            assert mf.file is not None
            assert mf.character_encoding == character_encoding
            mf.file.write('Café')
            mf.state = MultiFormatState.PARAGRAPH
        with open(file_name, 'rb') as file:
            assert file.read() == expected_bytes
    check_capsys(capsys)


def test_open_with_invalid_character_encoding(capsys):
    """Test invalid encoding is propagated from Python open."""
    check_invalid_character_encoding_constructor(
        formatter_class=MultiFormatTextBased2, file_extension='.test')
    check_capsys(capsys)
