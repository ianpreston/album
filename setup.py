#!/usr/bin/env python
from distutils.core import setup

setup(
    name='album',
    version='0.0.1',
    description='Markdown-based Literate Programming environment',
    author='Ian Preston',
    author_email='ian@ian-preston.com',
    url='https://github.com/ianpreston/album',
    install_requires=['click==2.5', 'mistune==0.3.1'],
    packages=['album'],
    package_dir={'album': 'build/album'},
    scripts=['build/album.py'],
)
