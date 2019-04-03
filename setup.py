#!/usr/bin/env python3
# This file is placed into public domain. See UNLICENSE.setup.txt


from setuptools import setup


setup(
    name            = 'parx',
    version         = '1.0.0alpha',
    description     = 'Simple parser for user-defined grammars',
    author          = 'Alexander Korzun',
    author_email    = 'korzun.sas@mail.ru',
    license         = 'MIT',
    packages        = ['parx'],
    tests_require   = ['pytest'],
    setup_requires  = ['pytest-runner'],
)
