#! /usr/local/bin/python3
"""Test the factory module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
from io import StringIO
import sys
import pytest
from check_capsys import check_capsys
from mformat.factory import MultiFormatFactory
from mformat.factory import create_mf, register_mf, \
    list_registered_mf, usage_mf, OptArgs
from mformat.mformat import MultiFormat, FormatterDescriptor


class MultiFormat2T(MultiFormat):
    """Test class for the factory module."""

    def __init__(self, file_name: str, url_as_text: bool = False,
                 arg1: str = '', arg2: str = ''):
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


def test_factory_obj_reg_ok(capsys):
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


def test_factory_obj_reg_nok(capsys):
    """Test the factory object registration with a not OK class."""
    factory = MultiFormatFactory()
    with pytest.raises(ValueError) as exc:
        factory.i_register(int)
    assert exc.value.args[0] == 'int must be a subclass of MultiFormat'
    check_capsys(capsys)


@pytest.mark.parametrize('args, arg1, arg2',
                         [({'arg1': 'value1', 'arg2': 'value2'},
                           'value1', 'value2'),
                          ({'arg1': 'value1'}, 'value1', ''),
                          ({'arg2': 'value2'}, '', 'value2'),
                          ({}, '', ''), (None, '', '')])
def test_factory_obj_create_ok(capsys, args, arg1, arg2):
    """Test the factory object create method with an OK class."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormat2T)
    mf = factory.i_create('mf2t', 'test.test', url_as_text=True, args=args)
    assert mf.arg1 == arg1
    assert mf.arg2 == arg2
    check_capsys(capsys)


def test_factory_obj_create_nok(capsys):
    """Test the factory object create method with a not OK class."""
    factory = MultiFormatFactory()
    with pytest.raises(KeyError) as exc:
        factory.i_create('something', 'test.test', url_as_text=True,
                         args={'arg1': 'value1'})
    assert exc.value.args[0] == \
        'Format "something" is not registered. Available formats: ' + \
        'docx, html, md, odt'
    check_capsys(capsys)


def test_factory_obj_get_regs(capsys):
    """Test the factory object get_registered_formats method."""
    factory = MultiFormatFactory()
    assert sorted(factory.i_get_registered_formats()) == \
        ['docx', 'html', 'md', 'odt']
    check_capsys(capsys)


def test_factory_obj_get_usage(capsys):
    """Test the factory object get_usage method."""
    factory = MultiFormatFactory()
    assert factory.i_get_usage('md') == \
        FormatterDescriptor(name='md', mandatory_args=[],
                            optional_args=[])
    check_capsys(capsys)


def test_factory_obj_get_usage_nok(capsys):
    """Test the factory object get_usage method with a not OK class."""
    factory = MultiFormatFactory()
    with pytest.raises(KeyError) as exc:
        factory.i_get_usage('something')
    assert exc.value.args[0] == \
        'Format "something" is not registered. Available formats: ' + \
        'docx, html, md, odt'
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
                        capsys, monkeypatch,
                        reg_func, create_func, list_func, usage_func):
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
    assert sorted(list_func()) == ['docx', 'html', 'md', 'mf2t', 'odt']
    assert usage_func('mf2t') == \
        FormatterDescriptor(name='mf2t', mandatory_args=[],
                            optional_args=['arg1', 'arg2'])
    assert usage_func('md') == \
        FormatterDescriptor(name='md', mandatory_args=[],
                            optional_args=[])
    assert usage_func('html') == \
        FormatterDescriptor(name='html', mandatory_args=[],
                            optional_args=['title', 'css_file', 'lang'])
    assert usage_func('docx') == \
        FormatterDescriptor(name='docx', mandatory_args=[],
                            optional_args=[])
    check_capsys(capsys)


@pytest.mark.parametrize('format_name',
                         ['html', 'md', 'docx', 'odt'])
def test_list_registered_mf(capsys, format_name):
    """Test the list_registered_mf function."""
    assert format_name in list_registered_mf()
    check_capsys(capsys)


def test_create_ok(capsys):
    """Test the shortcut create function with an OK class."""
    mfh = create_mf('html', 'test.html', url_as_text=True,
                    args={'title': 'Test title', 'css_file': 'test.css'})
    assert mfh.title == 'Test title'
    assert mfh.css_file == 'test.css'
    assert type(mfh).__name__ == 'MultiFormatHtml'
    check_capsys(capsys)


def test_create_nok(capsys):
    """Test the shortcut create function with a not OK class."""
    with pytest.raises(KeyError) as exc:
        create_mf('something', 'test.html', url_as_text=True,
                  args={'title': 'Test title', 'css_file': 'test.css'})
    assert 'Format "something" is not registered.' in exc.value.args[0]
    check_capsys(capsys)


class FileExistsCB:  # pylint: disable=too-few-public-methods
    """Callback function to ask user what to do if the file exists."""

    def __init__(self, ask_user: bool = True, overwrite: bool = False):
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


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt'])
def test_create_file_exists_y(capsys, fmt):
    """Test the create function with file exists and overwrite OK."""
    file_exists_cb = FileExistsCB(ask_user=False, overwrite=True)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_name = tmp_dir + '/test.' + fmt
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        with create_mf(format_name=fmt, file_name=file_name,
                       args=args) as mf:
            mf.start_heading(1, 'Test heading')
        if fmt in ['html', 'md']:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'Original content' not in content
                assert 'Test heading' in content
        else:
            with open(file_name, 'rb') as f:
                content = f.read()
                assert b'Original content' not in content
    assert file_exists_cb.num_calls == 1
    check_capsys(capsys)


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt'])
def test_create_file_exists_ay(capsys, monkeypatch, fmt):
    """Test the create function with file exists and overwrite OK."""
    file_exists_cb = FileExistsCB(ask_user=True, overwrite=False)
    mock_input = StringIO('y\ny\n')
    monkeypatch.setattr(sys, 'stdin', mock_input)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_name = tmp_dir + '/test.' + fmt
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        with create_mf(format_name=fmt, file_name=file_name,
                       args=args) as mf:
            mf.start_heading(1, 'Test heading')
        if fmt in ['html', 'md']:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'Original content' not in content
                assert 'Test heading' in content
        else:
            with open(file_name, 'rb') as f:
                content = f.read()
                assert b'Original content' not in content
    assert file_exists_cb.num_calls == 1
    assert file_exists_cb.file_name == file_name
    outmsg = [f'File {file_name} already exists. Overwrite? (y/n)']
    check_capsys(capsys, out_msgs=outmsg)


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt'])
def test_create_file_exists_n(capsys, fmt):
    """Test the create function with file exists and no overwrite."""
    file_exists_cb = FileExistsCB(ask_user=False, overwrite=False)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_name = tmp_dir + '/test.' + fmt
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        with pytest.raises(FileExistsError) as exc:
            with create_mf(format_name=fmt, file_name=file_name,
                           args=args) as mf:
                mf.start_heading(1, 'Test heading')
        assert exc.value.args[0] == f'File {file_name} already exists.'
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Original content' in content
    assert file_exists_cb.num_calls == 1
    check_capsys(capsys)


@pytest.mark.parametrize('fmt', ['html', 'md', 'docx', 'odt'])
def test_create_file_exists_an(capsys, monkeypatch, fmt):
    """Test the create function with file exists and no overwrite."""
    file_exists_cb = FileExistsCB(ask_user=True, overwrite=False)
    mock_input = StringIO('n\n')
    monkeypatch.setattr(sys, 'stdin', mock_input)
    args: OptArgs = {'file_exists_callback': file_exists_cb}
    with TemporaryDirectory() as tmp_dir:
        file_name = tmp_dir + '/test.' + fmt
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('Original content')
        with pytest.raises(FileExistsError) as exc:
            with create_mf(format_name=fmt, file_name=file_name,
                           args=args) as mf:
                mf.start_heading(1, 'Test heading')
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

    def __init__(self, file_name: str, url_as_text: bool = False):
        """Initialize the MultiFormatCase1 class."""
        super().__init__(file_name=file_name, url_as_text=url_as_text)

    @classmethod
    def file_name_extension(cls) -> str:
        """Test the file_name_extension method."""
        return '.case1'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Test the get_arg_desciption method."""
        return FormatterDescriptor(name='Case1', mandatory_args=[],
                                   optional_args=[])


class MultiFormatCase1Upper(MultiFormat):
    """Test class for the factory module."""

    def __init__(self, file_name: str, url_as_text: bool = False):
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


def test_factory_reg_ident1(capsys):
    """Test the factory register method with identical names."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormatCase1)
    with pytest.raises(KeyError) as exc:
        factory.i_register(MultiFormatCase1)
    assert exc.value.args[0] == 'Format "Case1" is already registered.'
    check_capsys(capsys)


def test_factory_reg_ident2(capsys):
    """Test the factory register method with case different names."""
    factory = MultiFormatFactory()
    factory.i_register(MultiFormatCase1)
    with pytest.raises(KeyError) as exc:
        factory.i_register(MultiFormatCase1Upper)
    assert exc.value.args[0] == 'Cannot register format "CaSE1" as ' + \
        '"Case1" is already registered.'
    check_capsys(capsys)


def test_factory_reg_ident3(capsys, monkeypatch):
    """Test the register function with identical names."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    register_mf(MultiFormatCase1)
    with pytest.raises(KeyError) as exc:
        register_mf(MultiFormatCase1)
    assert exc.value.args[0] == 'Format "Case1" is already registered.'
    check_capsys(capsys)


def test_factory_reg_ident4(capsys, monkeypatch):
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
                           ['Case1', 'docx', 'html', 'md', 'odt']),
                          (False, True,
                           ['Case1', 'CASE1',
                            'docx', 'DOCX',
                            'html', 'HTML',
                            'md', 'MD',
                            'odt', 'ODT']),
                          (True, False,
                           ['Case1', 'case1',
                            'docx', 'html', 'md', 'odt']),
                          (True, True,
                           ['Case1', 'case1', 'CASE1',
                            'docx', 'DOCX', 'html', 'HTML',
                            'md', 'MD', 'odt', 'ODT'])])
def test_factory_reg_ident5(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                            monkeypatch, wrap_func, lower, upper, expected):
    """Test the factory register method with identical names."""
    # Reset factory to get a new instance
    monkeypatch.setattr('mformat.factory._the_factory', None)
    assert wrap_func(lower=lower, upper=upper) == expected
    check_capsys(capsys)


# TODO: Add tests for the get_usage functions with lower and upper case names.
# TODO: Add tests for the create functions with lower and upper case names.
# TODO: Add tests for the filter args functions with lower and upper case names.
