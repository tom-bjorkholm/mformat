#! /usr/local/bin/python3
"""Test the mformat_docx module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from mformat_ext.mformat_docx import MultiFormatDocx
from mformat.mformat import FormatterDescriptor
from mformat.factory import create_mf

# Add base test helpers to path for shared test utilities
_base_test_path = (
    Path(__file__).parent.parent.parent.parent /
    'base' / 'test' / 'test_mformat'
)
sys.path.insert(0, str(_base_test_path))
# pylint: disable=wrong-import-order,wrong-import-position,import-error
from test_helpers import action_complex_nested_bullet_structure  # noqa: E402


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


def test_add_url(capsys):
    """Test the add_url method creates a docx file."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_paragraph('Check this link:')
            mfd.add_url(url='http://example.com', text='Example')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_add_url_as_text(capsys):
    """Test the add_url method with url_as_text=True."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath,
                       url_as_text=True) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_paragraph('Check this:')
            mfd.add_url(url='http://example.com', text='Here')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


@pytest.mark.parametrize('level', [1, 2, 3, 4, 5, 6])
def test_heading_creation(capsys, level):
    """Test creating headings at different levels."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=level, text=f'Heading Level {level}')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_heading_with_text(capsys):
    """Test heading with additional text."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=1, text='Main Title')
            mfd.add_text(text=' - Extended')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_heading_with_url(capsys):
    """Test heading with URL."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=2, text='Check ')
            mfd.add_url(url='http://example.com', text='this link')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_heading_then_paragraph(capsys):
    """Test heading followed by paragraph."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=1, text='Title')
            mfd.start_paragraph('Some text')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_multiple_headings(capsys):
    """Test multiple headings."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=1, text='Main')
            mfd.start_heading(level=2, text='Sub')
            mfd.start_heading(level=3, text='Subsub')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_heading_paragraph_heading(capsys):
    """Test heading, paragraph, then another heading."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=1, text='First Heading')
            mfd.start_paragraph('Some content here.')
            mfd.start_heading(level=2, text='Second Heading')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


@pytest.mark.parametrize('bold, italic',
                         [(True, False),
                          (False, True),
                          (True, True)])
def test_heading_formatting(capsys, bold, italic):
    """Test heading with bold and italic formatting."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=1, text='Formatted Title',
                              bold=bold, italic=italic)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_single_bullet_item(capsys):
    """Test a single bullet item."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='First item')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_multiple_bullet_items(capsys):
    """Test multiple bullet items."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='First item')
            mfd.start_bullet_item(text='Second item')
            mfd.start_bullet_item(text='Third item')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_bullet_item_with_add_text(capsys):
    """Test bullet item with additional text."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='First item')
            mfd.add_text(text=' with more text')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_bullet_item_with_url(capsys):
    """Test bullet item with URL."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='Check ')
            mfd.add_url(url='http://example.com', text='this link')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_nested_bullet_items_level2(capsys):
    """Test nested bullet items at level 2."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='Level 1', level=1)
            mfd.start_bullet_item(text='Level 2', level=2)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_nested_bullet_items_level3(capsys):
    """Test nested bullet items at level 3."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='Level 1', level=1)
            mfd.start_bullet_item(text='Level 2', level=2)
            mfd.start_bullet_item(text='Level 3', level=3)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_bullet_list_back_to_level1(capsys):
    """Test bullet list returning to level 1."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='Level 1 first', level=1)
            mfd.start_bullet_item(text='Level 2', level=2)
            mfd.start_bullet_item(text='Level 1 second', level=1)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_bullet_list_formatting(capsys):
    """Test bullet list with bold and italic."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='Bold item', bold=True)
            mfd.start_bullet_item(text='Italic item', italic=True)
            mfd.start_bullet_item(text='Both', bold=True, italic=True)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_paragraph_then_bullet_list(capsys):
    """Test paragraph followed by bullet list."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_paragraph(text='Intro paragraph')
            mfd.start_bullet_item(text='First item')
            mfd.start_bullet_item(text='Second item')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_bullet_list_then_paragraph(capsys):
    """Test bullet list followed by paragraph."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='First item')
            mfd.start_bullet_item(text='Second item')
            mfd.start_paragraph(text='Concluding paragraph')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_heading_then_bullet_list(capsys):
    """Test heading followed by bullet list."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=1, text='Main Title')
            mfd.start_bullet_item(text='First item')
            mfd.start_bullet_item(text='Second item')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_complex_nested_structure(capsys):
    """Test complex nested bullet structure."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            action_complex_nested_bullet_structure(mfd)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


# Tests for numbered point lists


def test_single_numbered_item(capsys):
    """Test a single numbered point item."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_numbered_point_item(text='First item')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_multiple_numbered_items(capsys):
    """Test multiple numbered point items."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_numbered_point_item(text='First item')
            mfd.start_numbered_point_item(text='Second item')
            mfd.start_numbered_point_item(text='Third item')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_numbered_item_with_add_text(capsys):
    """Test numbered point item with additional text."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_numbered_point_item(text='First item')
            mfd.add_text(text=' with more text')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_numbered_item_with_url(capsys):
    """Test numbered point item with URL."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_numbered_point_item(text='Check ')
            mfd.add_url(url='http://example.com', text='this link')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_nested_numbered_items_level2(capsys):
    """Test nested numbered point items at level 2."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_numbered_point_item(text='Level 1', level=1)
            mfd.start_numbered_point_item(text='Level 2', level=2)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_nested_numbered_items_level3(capsys):
    """Test nested numbered point items at level 3."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_numbered_point_item(text='Level 1', level=1)
            mfd.start_numbered_point_item(text='Level 2', level=2)
            mfd.start_numbered_point_item(text='Level 3', level=3)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_numbered_list_back_to_level1(capsys):
    """Test numbered point list returning to level 1."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_numbered_point_item(text='Level 1 first', level=1)
            mfd.start_numbered_point_item(text='Level 2', level=2)
            mfd.start_numbered_point_item(text='Level 1 second', level=1)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_numbered_list_formatting(capsys):
    """Test numbered point list with bold and italic."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_numbered_point_item(text='Bold item', bold=True)
            mfd.start_numbered_point_item(text='Italic item', italic=True)
            mfd.start_numbered_point_item(text='Both', bold=True, italic=True)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_paragraph_then_numbered_list(capsys):
    """Test paragraph followed by numbered point list."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_paragraph(text='Intro paragraph')
            mfd.start_numbered_point_item(text='First item')
            mfd.start_numbered_point_item(text='Second item')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_numbered_list_then_paragraph(capsys):
    """Test numbered point list followed by paragraph."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_numbered_point_item(text='First item')
            mfd.start_numbered_point_item(text='Second item')
            mfd.start_paragraph(text='Concluding paragraph')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_heading_then_numbered_list(capsys):
    """Test heading followed by numbered point list."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=1, text='Main Title')
            mfd.start_numbered_point_item(text='First item')
            mfd.start_numbered_point_item(text='Second item')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_mixed_bullet_and_numbered_lists(capsys):
    """Test switching between bullet and numbered point lists."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='Bullet 1', level=1)
            mfd.start_bullet_item(text='Bullet 2', level=1)
            mfd.start_numbered_point_item(text='Numbered 1', level=1)
            mfd.start_numbered_point_item(text='Numbered 2', level=1)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_nested_mixed_lists(capsys):
    """Test nested mixed bullet and numbered point lists."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_bullet_item(text='Bullet 1', level=1)
            mfd.start_numbered_point_item(text='Numbered 1.1', level=2)
            mfd.start_numbered_point_item(text='Numbered 1.2', level=2)
            mfd.start_bullet_item(text='Bullet 2', level=1)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


# Tests for code blocks


def test_simple_code_block(capsys):
    """Test a simple code block."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.write_code_block(text='print("Hello, World!")')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_code_block_with_language(capsys):
    """Test a code block with programming language."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.write_code_block(text='print("Hello")',
                                 programming_language='python')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_code_block_multiline(capsys):
    """Test a multiline code block."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            code = 'def hello():\n    print("Hello")\n    return True'
            mfd.write_code_block(text=code, programming_language='python')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_code_block_with_special_chars(capsys):
    """Test a code block with special characters."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            code = 'x = "test <>&"\ny = \'another\''
            mfd.write_code_block(text=code)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_paragraph_then_code_block(capsys):
    """Test paragraph followed by code block."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_paragraph(text='Here is some code:')
            mfd.write_code_block(text='x = 42', programming_language='python')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_code_block_then_paragraph(capsys):
    """Test code block followed by paragraph."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.write_code_block(text='x = 42')
            mfd.start_paragraph(text='That was the code.')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_heading_then_code_block(capsys):
    """Test heading followed by code block."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=2, text='Code Example')
            mfd.write_code_block(text='example()',
                                 programming_language='python')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_multiple_code_blocks(capsys):
    """Test multiple code blocks."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.write_code_block(text='x = 1', programming_language='python')
            mfd.write_code_block(text='y = 2', programming_language='python')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


# Tests for tables


def test_simple_table(capsys):
    """Test a simple table."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_table(first_row=['Col1', 'Col2'])
            mfd.add_table_row(row=['A', 'B'])
            mfd.add_table_row(row=['C', 'D'])
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_table_with_bold_header(capsys):
    """Test a table with bold header."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_table(first_row=['Name', 'Age'], bold=True)
            mfd.add_table_row(row=['Alice', '30'])
            mfd.add_table_row(row=['Bob', '25'])
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_table_with_italic_header(capsys):
    """Test a table with italic header."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_table(first_row=['Name', 'Age'], italic=True)
            mfd.add_table_row(row=['Alice', '30'])
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_write_complete_table(capsys):
    """Test write_complete_table method."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            table_data = [
                ['Header1', 'Header2'],
                ['Row1Col1', 'Row1Col2'],
                ['Row2Col1', 'Row2Col2']
            ]
            mfd.write_complete_table(table=table_data)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_write_complete_table_with_bold_header(capsys):
    """Test write_complete_table with bold first row."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            table_data = [
                ['Name', 'Value'],
                ['Alpha', '1'],
                ['Beta', '2']
            ]
            mfd.write_complete_table(table=table_data, bold_first_row=True)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_paragraph_then_table(capsys):
    """Test paragraph followed by table."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_paragraph(text='Here is a table:')
            mfd.start_table(first_row=['A', 'B'])
            mfd.add_table_row(row=['1', '2'])
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_table_then_paragraph(capsys):
    """Test table followed by paragraph."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_table(first_row=['X', 'Y'])
            mfd.add_table_row(row=['1', '2'])
            mfd.start_paragraph(text='That was the table.')
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_heading_then_table(capsys):
    """Test heading followed by table."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_heading(level=2, text='Data Table')
            mfd.start_table(first_row=['Col1', 'Col2'])
            mfd.add_table_row(row=['A', 'B'])
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_table_with_three_columns(capsys):
    """Test a table with three columns."""
    with TemporaryDirectory() as tmp_dir:
        fpath = tmp_dir + '/test.docx'
        with create_mf('docx', file_name=fpath) as mfd:
            assert type(mfd).__name__ == 'MultiFormatDocx'
            mfd.start_table(first_row=['Name', 'Age', 'City'])
            mfd.add_table_row(row=['Alice', '30', 'NYC'])
            mfd.add_table_row(row=['Bob', '25', 'LA'])
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
