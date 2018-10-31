#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
from .professional_review import __program__, __version__
from setuptools import setup
README = open('README.txt').read()

# allow setup.py to be run from any path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
setup(
    name=__program__,
    version=__version__,
    license='MIT',
    description='Python script to scrap data',
    long_description=README,
    url='https://github.com/ManojDatt/professional_review',
    download_url='https://github.com/fopina/pyspeedtest/tarball/v%s' %
    __version__,
    author='Manoj Datt',
    author_email='manojdatt1it@gmail.com',
    py_modules=['professional_review'],
    entry_points={
        'console_scripts': ['professional_review=professional_review:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords=['professional_review']
)
