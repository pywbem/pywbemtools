# Copyright 2021 IBM Corp. All Rights Reserved.
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
Utilities for end2end testing.
"""

from __future__ import absolute_import, print_function

import os
from subprocess import call, check_call
try:
    from subprocess import DEVNULL  # Python 3
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

import pytest

# Server nickname or server group nickname in WBEM server definition file
TEST_SERVER_IMAGE = os.getenv('TEST_SERVER_IMAGE', None)


@pytest.fixture(
    params=[TEST_SERVER_IMAGE],
    scope='module'
)
def server_url(request):
    """
    Fixture that starts a WBEM server in a Docker image and returns its URL.

    The TCP ports used on the host side are 15988 and 15989 so that they do
    not conflict with a WBEM server the user may have set up manually, which
    typically would use the standard ports 5988 and 5989.
    """
    image = request.param
    if image is None:
        raise ValueError("TEST_SERVER_IMAGE variable not specified")

    # The container name and ports are chosen to minimize the potential of
    # conflicts. They are fixed so multiple instances of the test cannot run
    # in parallel on the same system.
    container = 'pywbemtools_test_server'
    host_port_http = '15988'
    host_port_https = '15989'

    call(['docker', 'rm', container, '--force'],
         stdout=DEVNULL, stderr=DEVNULL)

    check_call(['docker', 'create',
                '--name', container,
                '--publish', '{}:5988'.format(host_port_http),
                '--publish', '{}:5989'.format(host_port_https),
                image],
               stdout=DEVNULL)

    check_call(['docker', 'start', container], stdout=DEVNULL)

    yield 'https://localhost:15989'

    check_call(['docker', 'rm', container, '--force'], stdout=DEVNULL)
