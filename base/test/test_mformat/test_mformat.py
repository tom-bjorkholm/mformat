#! /usr/local/bin/python3
"""Test the mformat module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

import pytest
from mformat.mformat import MultiFormat


@pytest.mark.parametrize('file_name, extension, res',
                         [('test', 'txt', 'test.txt'),
                          ('test.txt', 'txt', 'test.txt'),
                          ('test.txt', 'html', 'test.txt.html'),
                          ('test', 'md', 'test.md'),
                          ('test.txt', 'docx', 'test.txt.docx'),
                          ('test.txt', 'pdf', 'test.txt.pdf'),
                          ('test.txt', 'csv', 'test.txt.csv'),
                          ('test.txt', 'json', 'test.txt.json')])
def test_file_name_with_extension(file_name, extension, res):
    """Test the file_name_with_extension method."""
    assert MultiFormat.file_name_with_extension(file_name, extension) == res
