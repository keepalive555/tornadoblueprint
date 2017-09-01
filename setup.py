#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.1.1'

long_description = ''
with open('README.md') as f:
    long_description = f.read()

setup(
    name='',
    version=VERSION,
    description='',
    long_description=long_description,
    classifiers=[],
    classifiers=['Tornado', 'Blueprint'],
    author='gatsby',
    author_email='dreamcatchwang1991@gmail.com',
    url='https://github.com/keepalive555/tornadoblueprint',
    license='MIT',
    packages=['tornadoblueprint'],
    include_package_data=True,
    zip_safe=True,
    install_requires=['tornado'],
)
