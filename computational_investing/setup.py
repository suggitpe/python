#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Computational Investments, Part 1 (coursera)',
    'author': 'Peter Suggitt',
    'url': '',
    'download_url': '',
    'author_email': 'me@suggs.org.uk',
    'version': '0.0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'Computational Investments'
}

setup(**config)
