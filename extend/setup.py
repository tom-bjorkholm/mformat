#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='mformat_ext',
  version='0.0.1',
  description='Extension of the MultiFormat class for DOCX files',
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['mformat_ext'],
  package_dir={'mformat_ext': 'src/mformat_ext'},
  package_data={'mformat_ext': ['src/py.typed']},
  install_requires=[  # pylint: disable=duplicate-code
    'mformat >= 0.0.1',
    'python-docx >= 1.2.0',
    'pypi-simple >= 1.8.0',
    'packaging >= 25.0',
    'argcomplete >= 3.6.3',
    'requests >= 2.32.3',
    'types-requests >= 2.32.4.20250913',
    'pip >= 25.3',
    'setuptools >= 80.9.0',
    'build >= 1.3.0',
    'wheel>=0.45.1'
  ]
)
