#!/usr/bin/env python

from setuptools import setup

config = {
    'description': 'My Project',
    'author': 'Peter Suggitt',
    'url': '',
    'download_url': '',
    'author_email': 'me@suggs.org.uk',
    'version': '0.0.1',
    'packages': ['skeleton'],
    'scripts': [],
    'name': 'skeleton',
    'install_requires': [
        'nose'
    ]
}

setup(**config)

