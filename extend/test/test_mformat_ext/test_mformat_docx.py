#! /usr/local/bin/python3
"""Test the mformat_docx module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from tempfile import TemporaryFile
import pytest
from mformat_ext.mformat_docx import MultiFormatDocx


def test_exit_with_exception(capsys):    # pylint: disable=duplicate-code
    """Test that exception propagates from __exit__."""
    with TemporaryFile('w+b') as file:  # pylint: disable=duplicate-code
        with pytest.raises(RuntimeError) as exc:
            with MultiFormatDocx(file) as _:  # pylint: disable=duplicate-code
                raise RuntimeError('test exception')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
    assert exc.value.args[0] == 'test exception'
