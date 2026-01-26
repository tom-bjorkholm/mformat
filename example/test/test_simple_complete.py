#! /usr/local/bin/python3
"""Test the simple_complete module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
# import pytest
# Add example/src to path for shared test utilities
_example_test_path = (
    Path(__file__).parent.parent / 'src'
)
sys.path.insert(0, str(_example_test_path))
from e50_simple_complete import multi_format_example  # pylint: disable=wrong-import-position,import-error # noqa: E402,E501


def test_mfe_md():
    """Test the multi_format_example function with the md format."""
    with TemporaryDirectory() as tmp_dir:
        file_name =  tmp_dir + '/test.md'
        multi_format_example(format_name="md", file_name=file_name)
        with open(file_name, "rt", encoding="utf-8") as file:
            content = file.read()
        bold_ita = ' ***There is never a need to close an item type.***'
        assert bold_ita in content
    assert True
