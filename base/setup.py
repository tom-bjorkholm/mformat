#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='mformat',
  version='0.7.1',
  description='Uniform way to write simple text to different file formats',
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['mformat'],
  package_dir={'mformat': 'src/mformat'},
  package_data={'mformat': ['py.typed']},
  install_requires=[]
)
