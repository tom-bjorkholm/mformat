#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='mformat_ext',
  version='0.7',
  description=('Uniform way to write simple text extended with DOCX '
               'and ODT files'),
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['mformat_ext'],
  package_dir={'mformat_ext': 'src/mformat_ext'},
  package_data={'mformat_ext': ['py.typed']},
  install_requires=[
    'mformat >= 0.7',
    'python-docx >= 1.2.0',
    'odfdo >= 3.22.10',
    'PyRTF3 >= 0.47.5',
    'reportlab >= 5.0.0',
    'types-reportlab >= 4.5.1.20260521',
  ]
)
