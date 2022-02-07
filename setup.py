#!/usr/bin/env python

# (C) Copyright 2017 IBM Corp.
# (C) Copyright 2017 Inova Development Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Setup script for pywbemtools project.
"""

import os
import io
import re
import setuptools


def get_version(version_file):
    """
    Execute the specified version file and return the value of the __version__
    global variable that is set in the version file.

    Note: Make sure the version file does not depend on any packages in the
    requirements list of this package (otherwise it cannot be executed in
    a fresh Python environment).
    """
    with io.open(version_file, 'r', encoding='utf-8') as fp:
        version_source = fp.read()
    _globals = {}
    exec(version_source, _globals)  # pylint: disable=exec-used
    return _globals['__version__']


def get_requirements(requirements_file):
    """
    Parse the specified requirements file and return a list of its non-empty,
    non-comment lines. The returned lines are without any trailing newline
    characters.
    """
    with io.open(requirements_file, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    reqs = []
    for line in lines:
        line = line.strip('\n')
        if not line.startswith('#') and line != '':
            reqs.append(line)
    return reqs


def read_file(a_file):
    """
    Read the specified file and return its content as one string.
    """
    with io.open(a_file, 'r', encoding='utf-8') as fp:
        content = fp.read()
    return content


# pylint: disable=invalid-name
requirements = get_requirements('requirements.txt')
install_requires = [req for req in requirements
                    if req and not re.match(r'[^:]+://', req)]
dependency_links = [req for req in requirements
                    if req and re.match(r'[^:]+://', req)]
package_version = get_version(os.path.join('pywbemtools', '_version.py'))

# Docs on setup():
# * https://docs.python.org/2.7/distutils/apiref.html?
#   highlight=setup#distutils.core.setup
# * https://setuptools.readthedocs.io/en/latest/setuptools.html#
#   new-and-changed-setup-keywords
setuptools.setup(
    name='pywbemtools',
    version=package_version,
    packages=[
        'pywbemtools',
    ],
    entry_points={
        'console_scripts': [
            'pywbemcli = pywbemtools.pywbemcli.pywbemcli:cli',
            'pywbemlistener = pywbemtools.pywbemlistener.pywbemlistener:cli',
        ],
    },
    include_package_data=True,  # as specified in MANIFEST.in
    install_requires=install_requires,
    dependency_links=dependency_links,

    description='Python client tools to work with WBEM Servers using the '
    'PyWBEM API.',
    long_description=read_file('README_PYPI.rst'),
    long_description_content_type='text/x-rst',
    license='Apache License, Version 2.0',
    author='Karl Schopmeyer, Andreas Maier',
    author_email='k.schopmeyer@swbell.net, maiera@de.ibm.com',
    maintainer='Karl Schopmeyer, Andreas Maier',
    maintainer_email='k.schopmeyer@swbell.net, maiera@de.ibm.com',
    url='https://github.com/pywbem/pywbemtools',
    project_urls={
        'Bug Tracker': 'https://github.com/pywbem/pywbemtools/issues',
        'Documentation': 'https://pywbemtools.readthedocs.io/en/latest/',
        'Source Code': 'https://github.com/pywbem/pywbemtools',
    },

    options={'bdist_wheel': {'universal': True}},
    zip_safe=True,  # This package can safely be installed from a zip file
    platforms='any',

    # Keep these Python versions in sync with pywbemtools/__init__.py
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
