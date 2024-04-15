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
Basic server tests.
"""

from __future__ import absolute_import, print_function

import re

# pylint: disable=unused-import
from .utils import server_url, exec_pywbemcli_cmd  # noqa: F401
# pylint: enable=unused-import


def test_server_is_pegasus(server_url):  # noqa: F811
    # pylint: disable=redefined-outer-name
    """
    Test that this WBEM server is OpenPegasus and that it provides the
    expected Interop namespace, and the namespaces and profiles we want to test
    against.

    This container-packaged version of OpenPegasus is provided by the
    OpenPegasus project on GitHub (https://github.com/OpenPegasus/OpenPegasus).
    It includes OpenPegasus 2.14.2, the CIM Schema version 2.41.0, and a number
    of providers including a namespace provider.
    """

    # Check the server brand
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'server', 'brand'])
    brand = stdout.strip('\n')
    assert brand == 'OpenPegasus'

    # Check the expected Interop namespace
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'namespace', 'interop'])
    interop = stdout.strip('\n')
    assert interop == 'root/interop'

    # Check the namespaces our tests will use
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'namespace', 'list'])
    namespaces = stdout.strip('\n').split('\n')[2:]
    assert 'root/interop' in namespaces
    assert 'test/TestProvider' in namespaces

    # Check the profiles our tests will use
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'profile', 'list'])
    profile_lines = stdout.strip('\n').split('\n')[3:]
    profiles = []
    for line in profile_lines:
        m = re.match(r'^(.+?) {2,}(.+?) {2,}(.+)$', line)
        assert m, "Cannot parse 'profile list' output line: {!r}".format(line)
        profiles.append(m.groups())
    assert ('SNIA', 'Array', '1.1.0') in profiles
    assert ('SNIA', 'Indication', '1.2.0') in profiles
    assert ('SNIA', 'Profile Registration', '1.0.0') in profiles
    assert ('SNIA', 'SMI-S', '1.2.0') in profiles
