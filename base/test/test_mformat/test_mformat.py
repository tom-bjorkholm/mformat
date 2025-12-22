#! /usr/local/bin/python3
"""Test the mformat module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from tempfile import TemporaryFile
import pytest
from mformat.mformat import MultiFormat


def test_exit_with_exception(capsys):  # pylint: disable=duplicate-code
    """Test that exception propagates from __exit__."""
    with TemporaryFile('w+t') as file:  # pylint: disable=duplicate-code
        with pytest.raises(RuntimeError) as exc:
            with MultiFormat(file) as _:  # pylint: disable=duplicate-code
                raise RuntimeError('test exception')
        assert exc.value.args[0] == 'test exception'
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''
