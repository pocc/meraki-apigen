#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2018 Ross Jacobs All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Setup file."""
from setuptools import setup
from merakygen import __version__, __description__, __project_url__
from codecs import open

with open('README.md', encoding='utf-8') as file:
    readme = file.read()

setup(
    name='Meraki API Code Generator',
    version=__version__,
    description=__description__,
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Ross Jacobs',
    author_email='rossbjacobs@gmail.com',
    url=__project_url__,
    download_url='https://github.com/pocc/merakygen/releases',
    license='Apache 2.0',
    packages=['merakygen'],
    python_requires='>=3.5',
    provides=['merakygen'],
    install_requires=[
        'requests',
        'yapf',
        'pylint',
        'docopt',
        'inflection'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Ruby',
        'Programming Language :: Other Scripting Engines',  # Powershell
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: Utilities',
    ],
    entry_points={'console_scripts': ['merakygen = merakygen:merakygen:main']},
)
