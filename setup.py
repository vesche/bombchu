#!/usr/bin/env python

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bombchu',
    py_modules=['bombchu'],
    version='0.1.3',
    description='Simple data manipulation tool with a bang.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Unlicense',
    url='https://github.com/vesche/bombchu',
    author='Austin Jackson',
    author_email='vesche@protonmail.com',
    install_requires=['click', 'nothoney'],
    entry_points={
        'console_scripts': [
            'bombchu = bombchu:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Public Domain',
        'Programming Language :: Python :: 3'
    ]
)
