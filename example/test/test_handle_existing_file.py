#! /usr/local/bin/python3
"""Test the handle existing file example module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
# Add example/src to path for shared test utilities
# pylint: disable=duplicate-code
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e40_handle_existing_file import existing_file_example  # pylint: disable=wrong-import-position,wrong-import-order # noqa: E402,E501


@pytest.mark.parametrize('format_name, extension',
                         [('md', 'md'),
                          ('txt', 'txt')])
def test_existing_file_example1(capsys: pytest.CaptureFixture[str],
                                format_name: str, extension: str) -> None:
    """Test the existing file example."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / f'test.{extension}')
        existing_file_example(format_name=format_name, file_name=file_name)
        with open(file_name, "rt", encoding="utf-8") as file:
            content = file.read()
        assert 'Existing File Example' in content
    out, err = capsys.readouterr()
    assert '' == out
    assert '' == err


@pytest.mark.parametrize('env_var, txt_out',
                         [('overwrite', 'Overwriting file'),
                          ('backup', 'Backed up file')])
@pytest.mark.parametrize('format_name',
                         ['md', 'txt'])
def test_existing_file_example2(capsys: pytest.CaptureFixture[str],
                                monkeypatch: pytest.MonkeyPatch, env_var: str,
                                txt_out: str, format_name: str) -> None:
    """Test the existing file example."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / f'test.{format_name}')
        monkeypatch.setenv('MFORMAT_FILE_EXISTS', env_var)
        with open(file=file_name, mode='wt', encoding='utf-8') as file:
            file.write('Some old content.')
        existing_file_example(format_name=format_name, file_name=file_name)
        with open(file_name, "rt", encoding="utf-8") as file:
            content = file.read()
        assert 'Existing File Example' in content
    out, err = capsys.readouterr()
    assert txt_out in err
    assert file_name in err
    assert '' == out


@pytest.mark.parametrize('format_name',
                         ['md', 'txt'])
def test_existing_file_example3(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch,
        format_name: str) -> None:
    """Test the existing file example."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / f'test.{format_name}')
        monkeypatch.delenv('MFORMAT_FILE_EXISTS', raising=False)
        with open(file=file_name, mode='wt', encoding='utf-8') as file:
            file.write('Some old content.')
        with pytest.raises(FileExistsError):
            existing_file_example(format_name=format_name, file_name=file_name)
    out, err = capsys.readouterr()
    assert '' == out
    assert f'File {file_name} already exists' in err
    assert f'Not overwriting file {file_name}' in err
