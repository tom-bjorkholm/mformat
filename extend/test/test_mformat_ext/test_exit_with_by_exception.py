#! /usr/local/bin/python3
"""Test that exception propagates from __exit__."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
import os
import pytest
from mformat_ext.mformat_docx import MultiFormatDocx
from mformat.mformat_md import MultiFormatMd
from mformat.mformat_html import MultiFormatHtml


@pytest.mark.skip
@pytest.mark.parametrize('cls, fname, file_created',
                         [(MultiFormatDocx, 'test.docx', True),
                          (MultiFormatMd, 'test.md', True),
                          (MultiFormatHtml, 'test.html', True)])
def test_exit_with_exception(capsys, cls, fname, file_created):
    """Test that exception propagates from __exit__."""
    with TemporaryDirectory() as temp_dir:
        file_name = temp_dir + '/' + fname
        with pytest.raises(RuntimeError) as exc:
            with cls(file_name=file_name) as _:
                raise RuntimeError('test exception')
        assert exc.value.args[0] == 'test exception'
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''
        assert os.path.exists(file_name) == file_created
