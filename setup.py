#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='mini_vss',
    version='0.0.1',
    author='Atominick',
    packages=find_packages(),

    install_requires = [
        'semantic_version',
        'pycryptodome',
        'requests',
    ],
    entry_points = {
        'console_scripts': ['mini_vss=mini_vss.command_line:main'],
    }
)