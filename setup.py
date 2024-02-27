#!/usr/bin/python -u

"""
Copyright (C) 2017 Jacksgong(jacksgong.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from setuptools import setup, find_packages

# Get the long description from the README file
# noinspection PyArgumentList
setup(
    name="OkCat",
    version="1.4.0",
    packages=find_packages(exclude=['demo-conf', 'arts']),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['PyYAML>=3.12'],

    # metadata for upload to PyPI
    author="Jacksgong",
    author_email="igzhenjie@gmail.com",
    description="An powerful log processor",
    long_description='More detail please move to https://github.com/Jacksgong/okcat',
    license="Apache2",
    keywords="okcat log 'log processor' 'log filter'",
    url="https://github.com/Jacksgong/okcat",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'okcat=okcat:main'
        ]
    }
)
