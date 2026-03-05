#! /usr/local/bin/python3
"""Test the factory module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import pytest
from mformat_ext.mformat_docx import MultiFormatDocx
from mformat_ext.mformat_odt import MultiFormatOdt
from mformat.factory import (MultiFormatFactory, OptArgs, create_mf,
                             filter_args_mf, list_registered_mf, register_mf,
                             usage_mf)
from mformat.mformat import FormatterDescriptor, MultiFormat
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat_md import MultiFormatMd
from mformat.mformat_txt import MultiFormatTxt
from .check_capsys import check_capsys
from .test_helpers import (check_character_encoding_bytes,
                           check_invalid_character_encoding_factory,
                           create_paragraph_file_bytes_factory)


class MultiFormat2T(MultiFormat):
    """Test class for the factory module."""

    def __init__(self, file_name: str, url_as_text: bool = False,
                 arg1: str = '', arg2: str = '') -> None:
        """Initialize the MultiFormat2 class."""
        super().__init__(file_name=file_name, url_as_text=url_as_text)
        self.arg1: str = arg1
        self.arg2: str = arg2

    @classmethod
    def file_name_extension(cls) -> str:
        """Test the file_name_extension method."""
        return '.test'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Test the get_arg_desciption method."""
        return FormatterDescriptor(name='mf2t', mandatory_args=[],
                                   optional_args=['arg1', 'arg2'])


def test_factory_obj_reg_ok(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the factory object registration with an OK class."""
    factory = MultiFormatFactory()
    for i in ['md', 'html', 'docx']:
        assert i in factory.i_get_registered_formats()
        assert i in factory._registry  # pylint: disable=protected-access
        assert i in factory._usage  # pylint: disable=protected-access
    assert 'mf2t' not in factory.i_get_registered_formats()
    assert 'mf2t' not in factory._registry  # pylint: disable=protected-access
    assert 'mf2t' not in factory._usage  # pylint: disable=protected-access
    factory.i_register(MultiFormat2T)
    assert 'mf2t' in factory.i_get_registered_formats()
    assert 'mf2t' in factory._registry  # pylint: disable=protected-access
    assert 'mf2t' in factory._usage  # pylint: disable=protected-access
    # pylint: disable=protected-access
    assert factory._usage['mf2t'] == \
        FormatterDescriptor(name='mf2t', mandatory_args=[],
                            optional_args=['arg1', 'arg2'])
    assert factory._registry['mf2t'] == MultiFormat2T  # pylint: disable=protected-access # noqa: E501
    assert factory.i_get_usage('mf2t') == \
        FormatterDescriptor(name='mf2t', mandatory_args=[],
                            optional_args=['arg1', 'arg2'])
    check_capsys(capsys)


def test_factory_obj_reg_nok(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the factory object registration with a not OK class."""
    factory = MultiFormatFactory()
    with pytest.raises(ValueError) as exc:
        factory.i_register(int)  # type: ignore[arg-type]
    assert exc.value.args[0] == 'int must be a subclass of MultiFormat'
    check_capsys(capsys)


@pytest.mark.parametrize('args, arg1, arg2',
                         [({'arg1': 'value1', 'arg2': 'value2'},
                           'value1', 'value2'),
                          ({'arg1': 'value1'}, 'value1', ''),
                          ({'arg2': 'value2'}, '', 'value2'),
                          ({}, '', ''), (None, '', '')])
def test_factory_obj_create_ok(capsys: pytest.CaptureFixture[str],
                               args: OptArgs, arg1: str,
                               arg2: str) -> None:
    """Test the factory object create method with an OK class."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormat2T)
    mf = factory.i_create('mf2t', 'test.test', url_as_text=True, args=args)
    assert isinstance(mf, MultiFormat2T)
    assert mf.arg1 == arg1
    assert mf.arg2 == arg2
    check_capsys(capsys)


def test_factory_obj_create_nok(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the factory object create method with a not OK class."""
    factory = MultiFormatFactory()
    with pytest.raises(KeyError) as exc:
        factory.i_create('something', 'test.test', url_as_text=True,
                         args=None)
    assert exc.value.args[0] == \
        'Format "something" is not registered. Available formats: ' + \
        'docx, html, md, odt, reST, rtf, txt'
    check_capsys(capsys)


def test_factory_obj_get_regs(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the factory object get_registered_formats method."""
    factory = MultiFormatFactory()
    assert sorted(factory.i_get_registered_formats()) == \
        ['docx', 'html', 'md', 'odt', 'reST', 'rtf', 'txt']
    check_capsys(capsys)


def test_factory_obj_get_usage(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the factory object get_usage method."""
    factory = MultiFormatFactory()
    assert factory.i_get_usage('md') == \
        FormatterDescriptor(name='md', mandatory_args=[],
                            optional_args=['character_encoding'])
    check_capsys(capsys)


def test_factory_obj_get_usage_nok(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the factory object get_usage method with a not OK class."""
    factory = MultiFormatFactory()
    with pytest.raises(KeyError) as exc:
        factory.i_get_usage('something')
    assert exc.value.args[0] == \
        'Format "something" is not registered. Available formats: ' + \
        'docx, html, md, odt, reST, rtf, txt'
    check_capsys(capsys)


@pytest.mark.parametrize('usage_func',
                         [MultiFormatFactory.get_usage, usage_mf])
@pytest.mark.parametrize('list_func',
                         [MultiFormatFactory.get_registered_formats,
                          list_registered_mf])
@pytest.mark.parametrize('create_func',
                         [MultiFormatFactory.create, create_mf])
@pytest.mark.parametrize('reg_func',
                         [MultiFormatFactory.register, register_mf])
def test_factory_reg_ok(  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                        capsys: pytest.CaptureFixture[str],
                        monkeypatch: pytest.MonkeyPatch,
                        reg_func: Any, create_func: Any,
                        list_func: Any, usage_func: Any) -> None:
    """Test the factory register method with an OK class."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    reg_func(MultiFormat2T)
    assert 'mf2t' in list_func()
    assert MultiFormatFactory.get_usage('mf2t') == \
        FormatterDescriptor(name='mf2t', mandatory_args=[],
                            optional_args=['arg1', 'arg2'])
    mf2to1 = create_func('mf2t', 'test.test',
                         url_as_text=True,
                         args={'arg1': 'value1',
                               'arg2': 'value2'})
    assert mf2to1.arg1 == 'value1'
    assert mf2to1.arg2 == 'value2'
    mf2to2 = create_func('mf2t', 'test.test', url_as_text=True,
                         args={'arg1': 'value1'})
    assert mf2to2.arg1 == 'value1'
    assert mf2to2.arg2 == ''
    mf2to3 = create_func('mf2t', 'test.test', url_as_text=True,
                         args={'arg2': 'value2'})
    assert mf2to3.arg1 == ''
    assert mf2to3.arg2 == 'value2'
    mf2to4 = create_func('mf2t', 'test.test', url_as_text=True)
    assert mf2to4.arg1 == ''
    assert mf2to4.arg2 == ''
    assert sorted(list_func()) == ['docx', 'html', 'md', 'mf2t',
                                   'odt', 'reST', 'rtf', 'txt']
    assert usage_func('mf2t') == \
        FormatterDescriptor(name='mf2t', mandatory_args=[],
                            optional_args=['arg1', 'arg2'])
    assert usage_func('md') == \
        FormatterDescriptor(name='md', mandatory_args=[],
                            optional_args=['character_encoding'])
    assert usage_func('html') == \
        FormatterDescriptor(name='html', mandatory_args=[],
                            optional_args=['title', 'css_file', 'lang',
                                           'character_encoding'])
    assert usage_func('docx') == \
        FormatterDescriptor(name='docx', mandatory_args=[],
                            optional_args=[])
    check_capsys(capsys)


@pytest.mark.parametrize('format_name',
                         ['html', 'md', 'docx', 'odt'])
def test_list_registered_mf(capsys: pytest.CaptureFixture[str],
                            format_name: str) -> None:
    """Test the list_registered_mf function."""
    assert format_name in list_registered_mf()
    check_capsys(capsys)


def test_create_ok(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the shortcut create function with an OK class."""
    mfh = create_mf('html', 'test.html', url_as_text=True,
                    args={'title': 'Test title', 'css_file': 'test.css'})
    assert isinstance(mfh, MultiFormatHtml)
    assert mfh.title == 'Test title'
    assert mfh.css_file == 'test.css'
    assert type(mfh).__name__ == 'MultiFormatHtml'
    check_capsys(capsys)


def test_create_nok(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the shortcut create function with a not OK class."""
    with pytest.raises(KeyError) as exc:
        create_mf('something', 'test.html', url_as_text=True,
                  args={'title': 'Test title', 'css_file': 'test.css'})
    assert 'Format "something" is not registered.' in exc.value.args[0]
    check_capsys(capsys)


class FileExistsCB:  # pylint: disable=too-few-public-methods
    """Callback function to ask user what to do if the file exists."""

    def __init__(self, ask_user: bool = True, overwrite: bool = False) -> None:
        """Initialize the FileExistsCB class."""
        self.file_name: str = ''
        self.num_calls: int = 0
        self.ask_user: bool = ask_user
        self.overwrite: bool = overwrite

    def __call__(self, file_name: str) -> None:
        """Ask user what to do if the file exists.

        Return if OK to overwrite the file.
        Raise an exception to prevent the file from being overwritten.
        Args:
            file_name: The name of the file that already exists.
        """
        self.file_name = file_name
        self.num_calls += 1
        if self.ask_user:
            question = f'File {file_name} already exists. Overwrite? (y/n)'
            answer = input(question)
            if answer.lower() == 'y':
                self.overwrite = True
            else:
                self.overwrite = False
        if not self.overwrite:
            raise FileExistsError(f'File {file_name} already exists.')


def _build_file_name(tmp_dir: str, fmt: str,
                     as_path: bool) -> str | Path:
    """Build test file name as str or Path."""
    file_name: Path = Path(tmp_dir) / f'test.{fmt}'
    if as_path:
        return file_name
    return str(file_name)


@pytest.mark.parametrize('fmt, expected_cls',
                         [('html', MultiFormatHtml),
                          ('md', MultiFormatMd),
                          ('docx', MultiFormatDocx),
                          ('odt', MultiFormatOdt),
                          ('txt', MultiFormatTxt)])
@pytest.mark.parametrize('as_path', [False, True])
def test_create_mf_file_name_type_matrix(
        capsys: pytest.CaptureFixture[str], fmt: str, expected_cls: type,
        as_path: bool) -> None:
    """Test create_mf supports str and Path file names."""
    with TemporaryDirectory() as tmp_dir:
        file_name = _build_file_name(tmp_dir, fmt, as_path)
        with create_mf(format_name=fmt, file_name=file_name) as mf:
            assert isinstance(mf, expected_cls)
            assert str(Path(mf.file_name)) == str(Path(file_name))
            mf.new_heading(1, 'Test heading')
        assert Path(file_name).exists()
    check_capsys(capsys)


@pytest.mark.parametrize('format_name, file_extension',
                         [('html', '.html'),
                          ('md', '.md'),
                          ('txt', '.txt')])
@pytest.mark.parametrize('character_encoding, expected_text_bytes',
                         [('utf-8', b'Caf\xc3\xa9'),
                          ('iso-8859-1', b'Caf\xe9')])
def test_create_mf_character_encoding_writes_bytes(
        capsys: pytest.CaptureFixture[str], format_name: str,
        file_extension: str, character_encoding: str,
        expected_text_bytes: bytes) -> None:
    """Test create_mf writes bytes in the selected character encoding."""
    raw_content = create_paragraph_file_bytes_factory(
        format_name=format_name, file_extension=file_extension,
        character_encoding=character_encoding)
    check_character_encoding_bytes(
        raw_content=raw_content, character_encoding=character_encoding,
        expected_text_bytes=expected_text_bytes,
        expected_html_meta=format_name == 'html')
    check_capsys(capsys)


@pytest.mark.parametrize('format_name, file_extension',
                         [('html', '.html'),
                          ('md', '.md'),
                          ('txt', '.txt')])
def test_create_mf_invalid_character_encoding(
        capsys: pytest.CaptureFixture[str],
        format_name: str,
        file_extension: str) -> None:
    """Test create_mf propagates invalid encoding from Python open."""
    check_invalid_character_encoding_factory(
        format_name=format_name, file_extension=file_extension)
    check_capsys(capsys)


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt', 'txt'])
@pytest.mark.parametrize('as_path', [False, True])
@pytest.mark.parametrize('allow_overwrite', [False, True])
def test_create_mf_file_exists_callback_matrix(
        capsys: pytest.CaptureFixture[str],
        fmt: str,
        as_path: bool,
        allow_overwrite: bool) -> None:
    """Test file_exists_callback for str and Path file names."""
    file_exists_cb = FileExistsCB(ask_user=False, overwrite=allow_overwrite)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_name = _build_file_name(tmp_dir, fmt, as_path)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        if allow_overwrite:
            with create_mf(format_name=fmt, file_name=file_name,
                           args=args) as mf:
                mf.new_heading(1, 'Test heading')
            assert file_exists_cb.num_calls == 1
            assert str(file_exists_cb.file_name) == str(file_name)
            if fmt in ['html', 'md', 'txt']:
                with open(file_name, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                assert 'Original content' not in text_content
                assert 'Test heading' in text_content
            else:
                with open(file_name, 'rb') as f:
                    raw_content = f.read()
                assert b'Original content' not in raw_content
        else:
            with pytest.raises(FileExistsError) as exc:
                with create_mf(format_name=fmt, file_name=file_name,
                               args=args) as mf:
                    mf.new_heading(1, 'Test heading')
            assert exc.value.args[0] == f'File {file_name} already exists.'
            assert file_exists_cb.num_calls == 1
            assert str(file_exists_cb.file_name) == str(file_name)
    check_capsys(capsys)


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt', 'txt'])
def test_create_file_exists_y(capsys: pytest.CaptureFixture[str],
                              fmt: str) -> None:
    """Test the create function with file exists and overwrite OK."""
    file_exists_cb = FileExistsCB(ask_user=False, overwrite=True)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / f'test.{fmt}')
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        with create_mf(format_name=fmt, file_name=file_name,
                       args=args) as mf:
            mf.new_heading(1, 'Test heading')
        if fmt in ['html', 'md', 'txt']:
            with open(file_name, 'r', encoding='utf-8') as f:
                text_content = f.read()
                assert 'Original content' not in text_content
                assert 'Test heading' in text_content
        else:
            with open(file_name, 'rb') as f:
                raw_content = f.read()
                assert b'Original content' not in raw_content
    assert file_exists_cb.num_calls == 1
    check_capsys(capsys)


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt', 'txt'])
def test_create_file_exists_y2(
        capsys: pytest.CaptureFixture[str], fmt: str) -> None:
    """Test the create function with file exists and overwrite OK."""
    file_exists_cb = FileExistsCB(ask_user=False, overwrite=True)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_with_ext = f'test.{fmt}'
        file_name = Path(tmp_dir) / file_with_ext
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        with create_mf(format_name=fmt, file_name=file_name,
                       args=args) as mf:
            mf.new_heading(1, 'Test heading')
        if fmt in ['html', 'md', 'txt']:
            with open(file_name, 'r', encoding='utf-8') as f:
                text_content = f.read()
                assert 'Original content' not in text_content
                assert 'Test heading' in text_content
        else:
            with open(file_name, 'rb') as f:
                raw_content = f.read()
                assert b'Original content' not in raw_content
    assert file_exists_cb.num_calls == 1
    check_capsys(capsys)


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt'])
def test_create_file_exists_ay(capsys: pytest.CaptureFixture[str],
                               monkeypatch: pytest.MonkeyPatch,
                               fmt: str) -> None:
    """Test the create function with file exists and overwrite OK."""
    file_exists_cb = FileExistsCB(ask_user=True, overwrite=False)
    mock_input = StringIO('y\ny\n')
    monkeypatch.setattr(sys, 'stdin', mock_input)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / f'test.{fmt}')
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        with create_mf(format_name=fmt, file_name=file_name,
                       args=args) as mf:
            mf.new_heading(1, 'Test heading')
        if fmt in ['html', 'md']:
            with open(file_name, 'r', encoding='utf-8') as f:
                text_content = f.read()
                assert 'Original content' not in text_content
                assert 'Test heading' in text_content
        else:
            with open(file_name, 'rb') as f:
                raw_content = f.read()
                assert b'Original content' not in raw_content
    assert file_exists_cb.num_calls == 1
    assert file_exists_cb.file_name == file_name
    outmsg = [f'File {file_name} already exists. Overwrite? (y/n)']
    check_capsys(capsys, out_msgs=outmsg)


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt'])
def test_create_file_exists_n(
        capsys: pytest.CaptureFixture[str], fmt: str) -> None:
    """Test the create function with file exists and no overwrite."""
    file_exists_cb = FileExistsCB(ask_user=False, overwrite=False)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / f'test.{fmt}')
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        with pytest.raises(FileExistsError) as exc:
            with create_mf(format_name=fmt, file_name=file_name,
                           args=args) as mf:
                mf.new_heading(1, 'Test heading')
        assert exc.value.args[0] == f'File {file_name} already exists.'
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Original content' in content
    assert file_exists_cb.num_calls == 1
    check_capsys(capsys)


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt'])
def test_create_file_exists_an(capsys: pytest.CaptureFixture[str],
                               monkeypatch: pytest.MonkeyPatch,
                               fmt: str) -> None:
    """Test the create function with file exists and no overwrite."""
    file_exists_cb = FileExistsCB(ask_user=True, overwrite=False)
    mock_input = StringIO('n\n')
    monkeypatch.setattr(sys, 'stdin', mock_input)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / f'test.{fmt}')
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        with pytest.raises(FileExistsError) as exc:
            with create_mf(format_name=fmt, file_name=file_name,
                           args=args) as mf:
                mf.new_heading(1, 'Test heading')
        assert exc.value.args[0] == f'File {file_name} already exists.'
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Original content' in content
    assert file_exists_cb.num_calls == 1
    assert file_exists_cb.file_name == file_name
    outmsg = [f'File {file_name} already exists. Overwrite? (y/n)']
    check_capsys(capsys, out_msgs=outmsg)


class MultiFormatCase1(MultiFormat):
    """Test class for the factory module."""

    def __init__(self, file_name: str, lang: str,
                 url_as_text: bool = False) -> None:
        """Initialize the MultiFormatCase1 class."""
        super().__init__(file_name=file_name, url_as_text=url_as_text)
        self.lang: str = lang

    @classmethod
    def file_name_extension(cls) -> str:
        """Test the file_name_extension method."""
        return '.case1'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Test the get_arg_desciption method."""
        return FormatterDescriptor(name='Case1', mandatory_args=['lang'],
                                   optional_args=[])


class MultiFormatCase1Upper(MultiFormat):
    """Test class for the factory module."""

    def __init__(self, file_name: str, url_as_text: bool = False) -> None:
        """Initialize the MultiFormatCase1Upper class."""
        super().__init__(file_name=file_name, url_as_text=url_as_text)

    @classmethod
    def file_name_extension(cls) -> str:
        """Test the file_name_extension method."""
        return '.CaSe1'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Test the get_arg_desciption method."""
        return FormatterDescriptor(name='CaSE1', mandatory_args=[],
                                   optional_args=[])


def test_factory_reg_ident1(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the factory register method with identical names."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormatCase1)
    with pytest.raises(KeyError) as exc:
        factory.i_register(MultiFormatCase1)
    assert exc.value.args[0] == 'Format "Case1" is already registered.'
    check_capsys(capsys)


def test_factory_reg_ident2(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the factory register method with case different names."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormatCase1)
    with pytest.raises(KeyError) as exc:
        factory.i_register(MultiFormatCase1Upper)
    assert exc.value.args[0] == 'Cannot register format "CaSE1" as ' + \
        '"Case1" is already registered.'
    check_capsys(capsys)


def test_factory_reg_ident3(capsys: pytest.CaptureFixture[str],
                            monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the register function with identical names."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    register_mf(MultiFormatCase1)
    with pytest.raises(KeyError) as exc:
        register_mf(MultiFormatCase1)
    assert exc.value.args[0] == 'Format "Case1" is already registered.'
    check_capsys(capsys)


def test_factory_reg_ident4(capsys: pytest.CaptureFixture[str],
                            monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the register function with case different names."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    register_mf(MultiFormatCase1)
    with pytest.raises(KeyError) as exc:
        register_mf(MultiFormatCase1Upper)
    assert exc.value.args[0] == 'Cannot register format "CaSE1" as ' + \
        '"Case1" is already registered.'
    check_capsys(capsys)


def wrap_i_get_reg_formats(lower: bool, upper: bool) -> list[str]:
    """Wrap the i_get_reg_formats method."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormatCase1)
    return factory.i_get_registered_formats(lower=lower, upper=upper)


def wrap_get_reg_formats(lower: bool, upper: bool) -> list[str]:
    """Wrap the get_reg_formats method."""
    MultiFormatFactory.register(MultiFormatCase1)
    return MultiFormatFactory.get_registered_formats(lower=lower, upper=upper)


def wrap_list_reg_mf(lower: bool, upper: bool) -> list[str]:
    """Wrap the list_registered_mf method."""
    MultiFormatFactory.register(MultiFormatCase1)
    return list_registered_mf(lower=lower, upper=upper)


@pytest.mark.parametrize('wrap_func',
                         [wrap_i_get_reg_formats,
                          wrap_get_reg_formats,
                          wrap_list_reg_mf])
@pytest.mark.parametrize('lower, upper, expected',
                         [(False, False,
                           ['Case1', 'docx', 'html', 'md', 'odt',
                            'reST', 'rtf', 'txt']),
                          (False, True,
                           ['Case1', 'CASE1',
                            'docx', 'DOCX',
                            'html', 'HTML',
                            'md', 'MD',
                            'odt', 'ODT',
                            'reST', 'REST',
                            'rtf', 'RTF',
                            'txt', 'TXT']),
                          (True, False,
                           ['Case1', 'case1',
                            'docx', 'html', 'md', 'odt', 'reST',
                            'rest', 'rtf', 'txt']),
                          (True, True,
                           ['Case1', 'case1', 'CASE1',
                            'docx', 'DOCX', 'html', 'HTML',
                            'md', 'MD', 'odt', 'ODT',
                            'reST', 'rest', 'REST',
                            'rtf', 'RTF',
                            'txt', 'TXT'])])
def test_factory_reg_ident5(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                            monkeypatch: pytest.MonkeyPatch,
                            wrap_func: Any, lower: bool,
                            upper: bool, expected: list[str]) -> None:
    """Test the factory register method with identical names."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    assert wrap_func(lower=lower, upper=upper) == expected
    check_capsys(capsys)


def wrap_i_get_usage(format_name: str) -> FormatterDescriptor:
    """Wrap the i_get_usage method."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormatCase1)
    return factory.i_get_usage(format_name)


def wrap_get_usage(format_name: str) -> FormatterDescriptor:
    """Wrap the get_usage method."""
    MultiFormatFactory.register(MultiFormatCase1)
    return MultiFormatFactory.get_usage(format_name)


def wrap_usage_mf(format_name: str) -> FormatterDescriptor:
    """Wrap the usage_mf function."""
    register_mf(MultiFormatCase1)
    return usage_mf(format_name)


@pytest.mark.parametrize('wrap_func',
                         [wrap_i_get_usage, wrap_get_usage, wrap_usage_mf])
@pytest.mark.parametrize('format_name, usage',
                         [('Case1',
                           FormatterDescriptor(name='Case1',
                                               mandatory_args=['lang'],
                                               optional_args=[])),
                          ('case1',
                           FormatterDescriptor(name='Case1',
                                               mandatory_args=['lang'],
                                               optional_args=[])),
                          ('CASE1',
                           FormatterDescriptor(name='Case1',
                                               mandatory_args=['lang'],
                                               optional_args=[])),
                          ('docx',
                           FormatterDescriptor(name='docx',
                                               mandatory_args=[],
                                               optional_args=[])),
                          ('html',
                           FormatterDescriptor(
                               name='html',
                               mandatory_args=[],
                               optional_args=[
                                   'title', 'css_file',
                                   'lang',
                                   'character_encoding'])),
                          ('Docx',
                           FormatterDescriptor(name='docx',
                                               mandatory_args=[],
                                               optional_args=[])),
                          ('HTML',
                           FormatterDescriptor(
                               name='html',
                               mandatory_args=[],
                               optional_args=[
                                   'title', 'css_file',
                                   'lang',
                                   'character_encoding']))])
def test_get_usage_wrap(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                        monkeypatch: pytest.MonkeyPatch,
                        wrap_func: Any, format_name: str,
                        usage: FormatterDescriptor) -> None:
    """Test the get_usage functions with lower and upper case names."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    assert wrap_func(format_name) == usage
    check_capsys(capsys)


def wrap_filter_args(args: OptArgs, format_name: str) -> OptArgs:
    """Wrap the filter_args function."""
    MultiFormatFactory.register(MultiFormatCase1)
    return MultiFormatFactory.filter_args(args=args, format_name=format_name)


def wrap_i_filter_args(args: OptArgs, format_name: str) -> OptArgs:
    """Wrap the i_filter_args function."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormatCase1)
    return factory.i_filter_args(args=args, format_name=format_name)


def wrap_filter_args_mf(args: OptArgs, format_name: str) -> OptArgs:
    """Wrap the filter_args_mf function."""
    register_mf(MultiFormatCase1)
    return filter_args_mf(args=args, format_name=format_name)


def dummy_file_exists_cb(file_name: str) -> None:
    """Handle existing file in dummy way."""


OPTARG_EMPTY: OptArgs = {}
OPTARG_FILE_EXISTS_CALLBACK: OptArgs = {
    'file_exists_callback': dummy_file_exists_cb}
OPTARG_TITLE: OptArgs = {'title': 'Test Title'}
OPTARG_CSS_FILE: OptArgs = {'css_file': 'test.css'}
OPTARG_LANG: OptArgs = {'lang': 'en'}
OPTARG_LANG_EXISTS: OptArgs = {'file_exists_callback': dummy_file_exists_cb,
                               'lang': 'en'}
OPTARG_TITLE_CSS_FILE_LANG: OptArgs = {'title': 'Test Title',
                                       'css_file': 'test.css',
                                       'lang': 'en'}
OPTARG_ODT: OptArgs = {'lang': 'en',
                       'file_exists_callback': dummy_file_exists_cb}
OPTARG_ALL: OptArgs = {'file_exists_callback': dummy_file_exists_cb,
                       'title': 'Test Title',
                       'css_file': 'test.css',
                       'lang': 'en'}


@pytest.mark.parametrize('wrap_func',
                         [wrap_filter_args,
                          wrap_i_filter_args,
                          wrap_filter_args_mf])
@pytest.mark.parametrize('args, format_name, expected',
                         [(OPTARG_EMPTY, 'caSE1', OPTARG_EMPTY),
                          (OPTARG_EMPTY, 'case1', OPTARG_EMPTY),
                          (OPTARG_EMPTY, 'CASE1', OPTARG_EMPTY),
                          (OPTARG_EMPTY, 'Case1', OPTARG_EMPTY),
                          (OPTARG_EMPTY, 'md', OPTARG_EMPTY),
                          (OPTARG_EMPTY, 'MD', OPTARG_EMPTY),
                          (OPTARG_EMPTY, 'mD', OPTARG_EMPTY),
                          (OPTARG_EMPTY, 'Md', OPTARG_EMPTY),
                          (OPTARG_FILE_EXISTS_CALLBACK, 'case1',
                           OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_FILE_EXISTS_CALLBACK, 'CASE1',
                           OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_FILE_EXISTS_CALLBACK, 'caSE1',
                           OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_FILE_EXISTS_CALLBACK, 'Case1',
                           OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_FILE_EXISTS_CALLBACK, 'md',
                           OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_FILE_EXISTS_CALLBACK, 'MD',
                           OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_FILE_EXISTS_CALLBACK, 'Md',
                           OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_FILE_EXISTS_CALLBACK, 'mD',
                           OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_ALL, 'case1', OPTARG_LANG_EXISTS),
                          (OPTARG_ALL, 'CASE1', OPTARG_LANG_EXISTS),
                          (OPTARG_ALL, 'CAsE1', OPTARG_LANG_EXISTS),
                          (OPTARG_ALL, 'Case1', OPTARG_LANG_EXISTS),
                          (OPTARG_ALL, 'md', OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_ALL, 'MD', OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_ALL, 'mD', OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_ALL, 'Md', OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_ALL, 'html', OPTARG_ALL),
                          (OPTARG_ALL, 'HTML', OPTARG_ALL),
                          (OPTARG_ALL, 'HtmL', OPTARG_ALL),
                          (OPTARG_ALL, 'Html', OPTARG_ALL),
                          (OPTARG_TITLE, 'html', OPTARG_TITLE),
                          (OPTARG_TITLE, 'MD', OPTARG_EMPTY),
                          (OPTARG_TITLE, 'Docx', OPTARG_EMPTY),
                          (OPTARG_TITLE, 'ODT', OPTARG_EMPTY),
                          (OPTARG_CSS_FILE, 'Html', OPTARG_CSS_FILE),
                          (OPTARG_CSS_FILE, 'md', OPTARG_EMPTY),
                          (OPTARG_CSS_FILE, 'DOCX', OPTARG_EMPTY),
                          (OPTARG_CSS_FILE, 'Odt', OPTARG_EMPTY),
                          (OPTARG_LANG, 'html', OPTARG_LANG),
                          (OPTARG_LANG, 'MD', OPTARG_EMPTY),
                          (OPTARG_LANG, 'Docx', OPTARG_EMPTY),
                          (OPTARG_LANG, 'ODT', OPTARG_LANG),
                          (OPTARG_TITLE_CSS_FILE_LANG, 'html',
                           OPTARG_TITLE_CSS_FILE_LANG),
                          (OPTARG_TITLE_CSS_FILE_LANG, 'MD', OPTARG_EMPTY),
                          (OPTARG_TITLE_CSS_FILE_LANG, 'Docx', OPTARG_EMPTY),
                          (OPTARG_TITLE_CSS_FILE_LANG, 'ODT', OPTARG_LANG),
                          (OPTARG_TITLE_CSS_FILE_LANG, 'Html',
                           OPTARG_TITLE_CSS_FILE_LANG),
                          (OPTARG_ALL, 'DOCX', OPTARG_FILE_EXISTS_CALLBACK),
                          (OPTARG_ALL, 'Odt', OPTARG_ODT),
                          (None, 'html', None),
                          (None, 'MD', None),
                          (None, 'Docx', None),
                          (None, 'ODT', None),
                          (None, 'Html', None),
                          (None, 'md', None),
                          (None, 'case1', None),
                          (None, 'odt', None)])
def test_filter_args_wrap(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                          monkeypatch: pytest.MonkeyPatch,
                          wrap_func: Any, args: OptArgs,
                          format_name: str, expected: OptArgs) -> None:
    """Test the filter_args functions with lower and upper case names."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    assert wrap_func(args=args, format_name=format_name) == expected
    check_capsys(capsys)


@pytest.mark.parametrize('wrap_func',
                         [wrap_filter_args,
                          wrap_i_filter_args,
                          wrap_filter_args_mf])
@pytest.mark.parametrize('format_name, expected',
                         [('case1', OPTARG_EMPTY),
                          ('md', {'character_encoding': 'iso-8859-1'}),
                          ('MD', {'character_encoding': 'iso-8859-1'}),
                          ('txt', {'character_encoding': 'iso-8859-1'}),
                          ('TXT', {'character_encoding': 'iso-8859-1'}),
                          ('html', {'character_encoding': 'iso-8859-1'}),
                          ('HTML', {'character_encoding': 'iso-8859-1'}),
                          ('docx', OPTARG_EMPTY),
                          ('odt', OPTARG_EMPTY)])
def test_filter_args_wrap_character_encoding(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch,
        wrap_func: Any, format_name: str, expected: OptArgs) -> None:
    """Test filter_args keeps character_encoding only for text formats."""
    args: OptArgs = {'character_encoding': 'iso-8859-1'}
    monkeypatch.setattr('mformat.factory._the_factory', None)
    assert wrap_func(args=args, format_name=format_name) == expected
    check_capsys(capsys)


@pytest.mark.parametrize('wrap_func',
                         [wrap_filter_args,
                          wrap_i_filter_args,
                          wrap_filter_args_mf])
@pytest.mark.parametrize('args, format_name',
                         [(OPTARG_EMPTY, 'MDS'),
                          (OPTARG_EMPTY, 'docxx'),
                          (OPTARG_EMPTY, 'oodt'),
                          (OPTARG_EMPTY, 'invalid'),
                          (None, 'hmtlx')])
def test_filter_args_wrap_nok(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                              monkeypatch: pytest.MonkeyPatch,
                              wrap_func: Any, args: OptArgs,
                              format_name: str) -> None:
    """Test the filter_args functions with invalid format name."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    with pytest.raises(KeyError) as exc:
        wrap_func(args=args, format_name=format_name)
    assert f'Format "{format_name}" is not registered.' in exc.value.args[0]
    check_capsys(capsys)


def wrap_i_create(format_name: str, file_name: str,
                  url_as_text: bool, args: OptArgs) -> MultiFormat:
    """Wrap the i_create method."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormatCase1)
    return factory.i_create(format_name=format_name, file_name=file_name,
                            url_as_text=url_as_text, args=args)


def wrap_create(format_name: str, file_name: str, url_as_text: bool,
                args: OptArgs) -> MultiFormat:
    """Wrap the create method."""
    MultiFormatFactory.register(MultiFormatCase1)
    return MultiFormatFactory.create(format_name=format_name,
                                     file_name=file_name,
                                     url_as_text=url_as_text,
                                     args=args)


def wrap_create_mf(format_name: str, file_name: str, url_as_text: bool,
                   args: OptArgs) -> MultiFormat:
    """Wrap the create_mf function."""
    register_mf(MultiFormatCase1)
    return create_mf(format_name=format_name, file_name=file_name,
                     url_as_text=url_as_text, args=args)


@pytest.mark.parametrize('wrap_func',
                         [wrap_i_create, wrap_create, wrap_create_mf])
@pytest.mark.parametrize('url_as_text', [True, False])
@pytest.mark.parametrize('file_name', ['tmp_a', 'tmp_b'])
@pytest.mark.parametrize('format_name,args, expected_cls',
                         [('Case1', OPTARG_LANG, MultiFormatCase1),
                          ('case1', OPTARG_LANG, MultiFormatCase1),
                          ('CASE1', OPTARG_LANG, MultiFormatCase1),
                          ('md', OPTARG_EMPTY, MultiFormatMd),
                          ('MD', OPTARG_EMPTY, MultiFormatMd),
                          ('mD', OPTARG_EMPTY, MultiFormatMd),
                          ('Md', OPTARG_EMPTY, MultiFormatMd),
                          ('html', OPTARG_ALL, MultiFormatHtml),
                          ('HTML', OPTARG_ALL, MultiFormatHtml),
                          ('HtmL', OPTARG_ALL, MultiFormatHtml),
                          ('Html', OPTARG_ALL, MultiFormatHtml),
                          ('docx', OPTARG_FILE_EXISTS_CALLBACK,
                           MultiFormatDocx),
                          ('DOCX', OPTARG_FILE_EXISTS_CALLBACK,
                           MultiFormatDocx)])
def test_create_wrap(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                     monkeypatch: pytest.MonkeyPatch,
                     wrap_func: Any, url_as_text: bool,
                     file_name: str, format_name: str,
                     args: OptArgs, expected_cls: type[MultiFormat]) -> None:
    """Test the create functions with lower and upper case names."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    result = wrap_func(format_name=format_name, file_name=file_name,
                       url_as_text=url_as_text, args=args)
    assert isinstance(result, expected_cls)
    assert str(result.file_name).startswith(str(file_name))
    assert result.url_as_text == url_as_text
    check_capsys(capsys)


@pytest.mark.parametrize('wrap_func',
                         [wrap_i_create, wrap_create, wrap_create_mf])
@pytest.mark.parametrize('format_name, expected_cls',
                         [('html', MultiFormatHtml),
                          ('md', MultiFormatMd),
                          ('txt', MultiFormatTxt)])
def test_create_wrap_character_encoding(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
        wrap_func: Any, format_name: str,
        expected_cls: type[MultiFormat]) -> None:
    """Test create wrappers propagate character_encoding argument."""
    args: OptArgs = {'character_encoding': 'iso-8859-1'}
    monkeypatch.setattr('mformat.factory._the_factory', None)
    result = wrap_func(format_name=format_name, file_name='tmp_a',
                       url_as_text=False, args=args)
    assert isinstance(result, expected_cls)
    result_any: Any = result
    assert result_any.character_encoding == 'iso-8859-1'
    check_capsys(capsys)


@pytest.mark.parametrize('wrap_func',
                         [wrap_i_create, wrap_create, wrap_create_mf])
@pytest.mark.parametrize('format_name', ['invalid', 'INVALID', 'Invalid',
                                         'invalid', 'hmtlx'])
def test_create_wrap_nok(capsys: pytest.CaptureFixture[str],
                         monkeypatch: pytest.MonkeyPatch,
                         wrap_func: Any, format_name: str) -> None:
    """Test the create functions with invalid format name."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    with pytest.raises(KeyError) as exc:
        wrap_func(format_name=format_name, file_name='tmp_a',
                  url_as_text=False, args=None)
    assert f'Format "{format_name}" is not registered.' in exc.value.args[0]
    check_capsys(capsys)
