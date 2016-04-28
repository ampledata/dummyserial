#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the Dummy Serial Python Module.

Source:: https://github.com/ampledata/dummyserial
"""


__title__ = 'dummyserial'
__version__ = '0.0.1'
__author__ = 'Greg Albrecht <gba@orionlabs.io>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


import os
import setuptools
import sys


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit()


publish()


setuptools.setup(
    name='dummyserial',
    version=__version__,
    description='Dummy Serial Implementation.',
    author='Greg Albrecht',
    author_email='gba@orionlabs.io',
    packages=['aprs'],
    package_data={'': ['LICENSE']},
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/ampledata/dummyserial',
    setup_requires=['coverage >= 3.7.1', 'nose >= 1.3.7'],
    package_dir={'dummyserial': 'dummyserial'},
    zip_safe=False,
    include_package_data=True
)
