#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = '0.2.8'

long_description = ''
with open('README.txt', 'rt') as f:
    long_description = f.read()

setup(
    name='tornadoblueprint',
    version=VERSION,
    description='',
    long_description=long_description,
    classifiers=[],
    keywords='Tornado,Blueprint',
    author='gatsby',
    author_email='dreamcatchwang1991@gmail.com',
    url='https://github.com/keepalive555/tornadoblueprint',
    license='MIT',
    packages=['tornadoblueprint'],
    include_package_data=True,
    zip_safe=True,
    install_requires=['tornado>=2.4'],
)
