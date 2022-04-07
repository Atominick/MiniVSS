#!/usr/bin/env python3

from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='mini_vss',
    version='0.0.5',
    author='Atominick',
    author_email='atominick@ukr.net',
    url='https://github.com/Atominick/MiniVSS',
    description='Version Sharing System',

    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires = [
        'semantic_version',
        'pycryptodome',
        'requests',
    ],
    entry_points = {
        'console_scripts': ['mini_vss=mini_vss.command_line:main'],
    },
    classifiers=[
        'Topic :: Communications :: File Sharing',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
    ],
)