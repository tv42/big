#!/usr/bin/python
from setuptools import setup, find_packages
import os
import sys


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    f = open(path)
    return f.read()

install_requires = []
pyversion = sys.version_info[:2]
if pyversion < (2, 7) or (3, 0) <= pyversion <= (3, 1):
    install_requires.append('argparse')

setup(
    name="big",
    version="0.0.1",
    packages=find_packages(),

    author="Tommi Virtanen",
    author_email="tv@eagain.net",
    description="Large file storage with Git",
    long_description=read('README.rst'),
    license="MIT",
    keywords="git media",
    url="https://github.com/tv42/big",

    install_requires=[
        'setuptools',
        'gevent >=0.13.6',
        'Paramiko >=1.7.7.1',
        ] + install_requires,

    tests_require=[
        'pytest >=2.1.3',
        'cram >=0.5',
        ],

    entry_points={

        'console_scripts': [
            'big = big.cli:main',
            ],

        'big.cli': [
            'add = big.add:make',
            'get = big.get:make',
            'put = big.put:make',
            'fix-missing-links = big.fix_missing_links:make',
            ],

        },

    )
