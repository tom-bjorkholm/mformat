#! /usr/local/bin/python3
"""Test the mformat_docx module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from tempfile import TemporaryFile
import pytest
from mformat_ext.mformat_docx import MultiFormatDocx


def test_exit_with_exception(capsys):
    """Test that exception propagates from __exit__."""
    with TemporaryFile('w+b') as file:
        with pytest.raises(RuntimeError) as exc:
            with MultiFormatDocx(file) as _:
                raise RuntimeError('test exception')
        assert exc.value.args[0] == 'test exception'
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''
