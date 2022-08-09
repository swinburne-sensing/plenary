#!/usr/bin/env python3

import os
import re

from setuptools import setup, find_packages


_RE_URL_DEPENDENCY = re.compile(r'^[^:\s]+://[^#]+#egg=(.+)$')


# Read properties from __init__.py
with open(os.path.join(os.path.dirname(__file__), 'plenary', '__init__.py')) as file_init:
    content_init = file_init.read()

    version = re.search("__version__ = '([^']+)'", content_init).group(1)

    author = re.search("__author__ = '([^']+)'", content_init).group(1)

    maintainer = re.search("__maintainer__ = '([^']+)'", content_init).group(1)
    maintainer_email = re.search("__email__ = '([^']+)'", content_init).group(1)


setup(
    name='plenary',
    version=version,
    description='A library of convenient utility methods and classes',
    long_description=open('README.md').read(),
    author=author,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='GPLv3',
    platforms='any',
    install_requires=[]
)
