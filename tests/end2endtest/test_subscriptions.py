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
Test subscription command group commands. Generally this test creates
indication filters, listener destinations, and subscriptions, displays them
and removes them from the server.
"""

from __future__ import absolute_import, print_function

import re

# pylint: disable=unused-import
from .utils import server_url  # noqa: F401
# pylint: enable=unused-import
from ..unit.utils import execute_command


def test_subscriptions(server_url):
    # pylint: disable=redefined-outer-name
    """
    The test.  This function is called because server_url is a pytest
    fixture.
    """
    # Get Interop Namespace
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'namespace', 'interop'])
    assert rc == 0
    assert stderr == ''
    interop = stdout.strip('\n')
    assert interop == 'root/interop'

    # Determine if Indication profile exists
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'profile', 'list'])
    assert rc == 0
    assert stderr == ''
    profile_lines = stdout.strip('\n').split('\n')[3:]
    profiles = []
    for line in profile_lines:
        m = re.match(r'^(.+?) {2,}(.+?) {2,}(.+)$', line)
        assert m, "Cannot parse 'profile list' output line: {!r}".format(line)
        profiles.append(m.groups())
    # validate versions of indication profile
    assert ('SNIA', 'Indication', '1.2.0') in profiles

    # Determine if required classes are in interop
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'class', 'get',
         'CIM_ListenerDestinationCIMXML', '-n', interop])
    assert rc == 0
    assert stderr == ''

    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'class', 'get',
         'CIM_IndicationFilter', '-n', interop])
    assert rc == 0
    assert stderr == ''
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'class', 'get',
         'CIM_IndicationSubscription', '-n', interop])
    assert rc == 0
    assert stderr == ''

    # Create a destination
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'subscription', 'add-destination',
         'odest1', '-l', 'http://localhost:5000'])
    assert rc == 0
    assert stderr == ''
    good_response = stdout.strip('\n')
    assert good_response == 'Added owned destination: ' \
        'Name=pywbemdestination:defaultpywbemcliSubMgr:odest1'

    # Create a filter
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'subscription', 'add-filter',
         'ofilter1', '--query', 'Select * from CIM_AlertIndication'])
    assert rc == 0
    assert stderr == ''
    good_response = stdout.strip('\n')
    assert good_response == 'Added owned filter: Name=pywbemfilter:' \
        'defaultpywbemcliSubMgr:ofilter1'

    # Test filter creation that returns CIMError since we cannot test
    # this with mock. Server should return exception because of bad filter
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'subscription', 'add-filter',
         'ofilter2', '--query', 'blah'])
    assert rc == 1
    err_response = stderr.strip('\n')
    assert re.search("CIM_ERR_INVALID_PARAMETER", err_response)

    # Create a subscription
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'subscription', 'add-subscription',
         'odest1', 'ofilter1', '--owned'])
    assert rc == 0
    assert stderr == ''
    good_response = stdout.strip('\n')
    assert re.search("Added owned subscription:", good_response)
    assert re.search('pywbemdestination:defaultpywbemcliSubMgr:odest1',
                     good_response)

    # General list command
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', '-o', 'simple',
         'subscription', 'list'])
    assert rc == 0
    assert stderr == ''
    good_response = stdout.strip('\n')
    pattern = r"TOTAL INSTANCES +3 +0 +3"
    assert re.search(pattern, good_response)

    # Remove the subscription
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'subscription', 'remove-subscription',
         'odest1', 'ofilter1'])
    assert rc == 0
    assert stderr == ''
    good_response = stdout.strip('\n')
    assert good_response == \
        'Removed 1 subscription(s) for destination-id: odest1, filter-id: ' \
        'ofilter1.'

    # Remove the filter
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'subscription', 'remove-filter',
         'ofilter1'])
    assert rc == 0
    assert stderr == ''
    good_response = stdout.strip('\n')
    assert good_response == \
        'Removed owned indication filter: identity=ofilter1, ' \
        'Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1.'

    # Remove the destination
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', 'subscription', 'remove-destination',
         'odest1'])
    assert rc == 0
    assert stderr == ''
    good_response = stdout.strip('\n')
    assert good_response == \
        'Removed owned indication destination: identity=odest1, ' \
        'Name=pywbemdestination:defaultpywbemcliSubMgr:odest1.'
