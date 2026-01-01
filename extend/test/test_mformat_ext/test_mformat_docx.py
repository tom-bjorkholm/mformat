#! /usr/local/bin/python3
"""Test the mformat_docx module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
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
            mfd.start_bullet_item(text='Item 1', level=1)
            mfd.start_bullet_item(text='Item 1.1', level=2)
            mfd.start_bullet_item(text='Item 1.2', level=2)
            mfd.start_bullet_item(text='Item 2', level=1)
            mfd.start_bullet_item(text='Item 2.1', level=2)
        assert os.path.exists(fpath)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''
