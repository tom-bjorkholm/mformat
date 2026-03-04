#! /usr/local/bin/python3
"""Test the file already exists functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
from pathlib import Path
import pytest
from mformat.factory import OptArgsDict, create_mf


class FileExistsCallback:  # pylint: disable=too-few-public-methods
    """Callback function to handle file already exists."""

    def __init__(self, allow_overwrite: bool):
        """Initialize the FileExistsCallback class."""
        self.count: int = 0
        self.allow_overwrite: bool = allow_overwrite

    def __call__(self, file_name: str) -> None:
        """Call the FileExistsCallback function."""
        self.count += 1
        if self.allow_overwrite:
            return
        raise FileExistsError(f'File {file_name} already exists')


@pytest.mark.parametrize('format_name, file_name', [('docx', 'test.docx'),
                                                    ('html', 'test.html'),
                                                    ('md', 'test.md')])
def test_file_exists_overwrite(format_name: str, file_name: str) -> None:
    """Test the file already exists functionality."""
    with TemporaryDirectory() as temp_dir:
        full_file_name = str(Path(temp_dir) / file_name)
        with open(full_file_name, 'w', encoding='utf-8') as f:
            f.write('Test')
        file_exists_callback = FileExistsCallback(allow_overwrite=True)
        args: OptArgsDict = {'file_exists_callback': file_exists_callback}
        with create_mf(format_name=format_name,
                       file_name=full_file_name,
                       args=args) as _:
            pass
        assert file_exists_callback.count == 1


@pytest.mark.parametrize('format_name, file_name', [('docx', 'test.docx'),
                                                    ('html', 'test.html'),
                                                    ('md', 'test.md')])
def test_file_exists_no_overwrite(format_name: str, file_name: str) -> None:
    """Test the file already exists functionality not allowing overwrite."""
    with TemporaryDirectory() as temp_dir:
        full_file_name = str(Path(temp_dir) / file_name)
        with open(full_file_name, 'w', encoding='utf-8') as f:
            f.write('Test')
        file_exists_callback = FileExistsCallback(allow_overwrite=False)
        args: OptArgsDict = {'file_exists_callback': file_exists_callback}
        with pytest.raises(FileExistsError) as exc:
            with create_mf(format_name=format_name,
                           file_name=full_file_name,
                           args=args) as _:
                pass
        assert exc.value.args[0] == f'File {full_file_name} already exists'
        assert file_exists_callback.count == 1


@pytest.mark.parametrize('format_name, file_name', [('docx', 'test.docx'),
                                                    ('html', 'test.html'),
                                                    ('md', 'test.md')])
def test_file_exists_no_callback(format_name: str, file_name: str) -> None:
    """Test the file already exists functionality without a callback."""
    with TemporaryDirectory() as temp_dir:
        full_file_name = str(Path(temp_dir) / file_name)
        with open(full_file_name, 'w', encoding='utf-8') as f:
            f.write('Test')
        with pytest.raises(FileExistsError) as exc:
            with create_mf(format_name=format_name,
                           file_name=full_file_name) as _:
                pass
        assert 'Cowardly refusing to overwrite existing file' in \
            exc.value.args[0]


@pytest.mark.parametrize('format_name, file_name', [('docx', 'test.docx'),
                                                    ('html', 'test.html'),
                                                    ('md', 'test.md')])
def test_file_does_not_exist(format_name: str, file_name: str) -> None:
    """Test the file exists functionality when the file does not exist."""
    with TemporaryDirectory() as temp_dir:
        full_file_name = str(Path(temp_dir) / file_name)
        file_exists_callback = FileExistsCallback(allow_overwrite=False)
        args: OptArgsDict = {'file_exists_callback': file_exists_callback}
        with create_mf(format_name=format_name,
                       file_name=full_file_name,
                       args=args) as _:
            pass
        assert file_exists_callback.count == 0
