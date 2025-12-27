#! /usr/local/bin/python3
"""Test the mformat_docx module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
import pytest
from mformat_ext.mformat_docx import MultiFormatDocx


def test_exit_with_exception(capsys):  # pylint: disable=duplicate-code
    """Test that exception propagates from __exit__."""
    with TemporaryDirectory() as temp_dir:  # pylint: disable=duplicate-code  # noqa: E501
        file_name = temp_dir + '/test.docx'
        with pytest.raises(RuntimeError) as exc:  # pylint: disable=duplicate-code # noqa: E501
            with MultiFormatDocx(file_name=file_name) as _:  # pylint: disable=duplicate-code # noqa: E501
                raise RuntimeError('test exception')
        assert exc.value.args[0] == 'test exception'
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''
