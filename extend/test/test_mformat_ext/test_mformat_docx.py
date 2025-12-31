#! /usr/local/bin/python3
"""Test the mformat_docx module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
import os
import pytest
from mformat_ext.mformat_docx import MultiFormatDocx
from mformat.mformat import FormatterDescriptor
from mformat.factory import create_mf


def test_file_name_extension(capsys):
    """Test the file_name_extension method."""
    assert MultiFormatDocx.file_name_extension() == '.docx'
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_get_arg_desciption(capsys):
    """Test the get_arg_desciption method."""
    assert MultiFormatDocx.get_arg_desciption() == \
        FormatterDescriptor(name='docx', mandatory_args=[],
                            optional_args=[])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


@pytest.mark.parametrize('fname', ['test.docx', 'other.docx'])
def test_create_ok(capsys, fname):
    """Test the shortcut create function with an OK class."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/' + fname
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_create_nok(capsys):
    """Test the shortcut create function with a not OK class."""
    with pytest.raises(TypeError) as exc:
        args = {'output': 'test.docx'}
        with create_mf('docx', file_name='test.docx', args=args) as _:
            pass
    assert "MultiFormatDocx.__init__() got an unexpected " + \
        "keyword argument 'output'" in exc.value.args[0]
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
