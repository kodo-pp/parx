#!/usr/bin/env python3
# (c) 2019 Alexander Korzun
# This file is licensed under the MIT license. See LICENSE file


from setuptools import setup


setup(
    name            = 'parx',
    version         = '1.0.0alpha',
    description     = 'A simple parser for user-defined grammars',
    author          = 'Alexander Korzun',
    author_email    = 'korzun.sas@mail.ru',
    license         = 'MIT',
    packages        = ['parx'],
    tests_require   = ['pytest'],
    setup_requires  = ['pytest-runner'],
)
