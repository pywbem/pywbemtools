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
Utilities for end2end testing. Includes both fixtures and non-fixture common
functions.
"""

from __future__ import absolute_import, print_function

import os
import re

from subprocess import call, check_call
try:
    from subprocess import DEVNULL  # Python 3
except ImportError:
    DEVNULL = open(os.devnull, 'wb')  # pylint: disable=consider-using-with

import pytest

from ..unit.utils import execute_command

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

    Yields the url of the WBEM server started including port number with
    scheme == HTTPS. Stops the container on return from the yield so
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

    host_uri = 'https://localhost:{}'.format(host_port_https)

    # Flag to use an existing running container for the test.  This is
    # a debug mechanism in that the WBEM Server must be already running in
    # an existing container before the test and the container is not stoppe
    # at the end of the test.  This allows debugging the test in the container
    # and setting the flags to capture server information from the container
    # when the test is over
    # TODO: Change following to False before commit
    use_running_container = False

    if use_running_container:
        yield host_uri

    else:
        # Remove, create and start a new container before yield to the test
        call(['docker', 'rm', container, '--force'],
             stdout=DEVNULL, stderr=DEVNULL)

        check_call(['docker', 'create',
                    '--name', container,
                    '--publish', '{}:5988'.format(host_port_http),
                    '--publish', '{}:5989'.format(host_port_https),
                    '--net', 'bridge',
                    image],
                   stdout=DEVNULL)

        check_call(['docker', 'start', container], stdout=DEVNULL)

        yield host_uri

        check_call(['docker', 'rm', container, '--force'], stdout=DEVNULL)


def exec_pywbemcli_cmd(request_params, expected_rc=0, ignore_stderr=False):
    """
    Execute a pywbemcli request with the list of parameters provided in
    request_params and assert if rc != 0. When ignore_stderr is set, the test
    ignores values in the stderr returned.

    If expected_rc == 0
        Returns stdout if rc = 0 or asserts if rc != 0
    if expected_rc != 0
        Returns stderr if expected_rc == rc or asserts if expected_rc != rc

    There is a case in the code where a non-zero stderr is returned when
    rc == 0. the ingore_stderr parameter allows bypassing this.
    """
    # print("debug: exec_pywbemcli_cmd {}".format(" ".join(request_params)))
    rc, stdout, stderr = execute_command('pywbemcli', request_params)
    # print("debug: rc={}, stderr={}".format(rc, stderr))

    if expected_rc == 0:
        assert rc == 0, "pywbemcli failed: params={}, rc={}, stderr={}" \
                        .format(request_params, rc, stderr)
        if not ignore_stderr:
            assert stderr == '', "pywbemcli stderr={}, rc={}".format(stderr, rc)
        return stdout

    # expected rc not 0
    assert rc == expected_rc, "pywbemcli failed: params={} failed rc={}, " \
                              "stderr={} " \
                              .format(request_params, rc, stderr)
    return stderr


def validate_namespace_exists(server_url, namespace, namespace_full_name):
    # pylint: disable=redefined-outer-name
    """
    Validate that the namespace defined by namespace  ex. interop exists.  The
    parameter namespace_full_name is the full namespace name (ex root/interop)

    Returns the namespace if successful
    """
    # Get Interop Namespace
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'namespace', namespace])
    namespace = stdout.strip('\n')
    assert namespace == namespace_full_name
    return namespace


def validate_indication_profile(server_url, expected_profile):
    # pylint: disable=redefined-outer-name
    """
    Validate that the expected profile defined by the tuple expected_profile
    exists.
    """
    # Determine if Indication profile exists
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'profile', 'list'])

    profile_lines = stdout.strip('\n').split('\n')[3:]
    profiles = []
    for line in profile_lines:
        m = re.match(r'^(.+?) {2,}(.+?) {2,}(.+)$', line)
        assert m, "Cannot parse 'profile list' output line: {!r}".format(line)
        profiles.append(m.groups())

    # validate versions of indication profile
    assert expected_profile in profiles, "Expected profile {0} not found in " \
        "{1}".format(expected_profile, profiles)


def validate_required_classes(server_url, required_classes_dict):
    # pylint: disable=redefined-outer-name
    """
    Test that the classed defined in the namespaces in the input dictionary
    actually exist.
    """
    for namespace, classnames in required_classes_dict.items():
        for classname in classnames:
            exec_pywbemcli_cmd(
                ['-s', server_url, '--no-verify', 'class', 'get',
                 classname, '-n', namespace])


def create_indication_subscription(server_url, listener_scheme, listener_host,
                                   listener_port, dest_id, filter_id,
                                   query, source_namespaces):
    # pylint: disable=redefined-outer-name
    """
    Create the 3 instances required for a complete  indication subscription
    in the WBEM server defined by server_url

    The bind_address must include both the host name/IP and scheme.

    Source namespaces which is a parameter for the filter is optional
    """
    # Create a destination
    listener_url = "{}://{}:{}".format(listener_scheme, listener_host,
                                       listener_port)

    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'subscription', 'add-destination',
         dest_id, '-l', listener_url])

    good_response = stdout.strip('\n')
    assert good_response == 'Added owned destination: ' \
        'Name=pywbemdestination:defaultpywbemcliSubMgr:{}'.format(dest_id)

    # Create a filter
    cmd = ['-s', server_url, '--no-verify', 'subscription', 'add-filter',
           filter_id,
           '--query', query,
           '--source-namespaces', source_namespaces]

    stdout = exec_pywbemcli_cmd(cmd)

    good_response = stdout.strip('\n')
    assert good_response == 'Added owned filter: Name=pywbemfilter:' \
        'defaultpywbemcliSubMgr:{}'.format(filter_id)

    # Test filter creation that returns CIMError since we cannot test
    # this with mock. Server should return exception because of bad filter
    stderr = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'subscription', 'add-filter',
         'ofilter2', '--query', 'blah', '--source-namespaces', 'root/cimv2'],
        expected_rc=1, )

    err_response = stderr.strip('\n')
    assert re.search("CIM_ERR_INVALID_PARAMETER", err_response)

    # Create a subscription
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'subscription', 'add-subscription',
         'odest1', 'ofilter1', '--owned'])
    good_response = stdout.strip('\n')
    assert re.search("Added owned subscription:", good_response)
    assert re.search(
        'pywbemdestination:defaultpywbemcliSubMgr:{}'.format(dest_id),
        good_response)


def remove_subscription(server_url, dest_id, filter_id):
    # pylint: disable=redefined-outer-name
    """
    Remove an existing indication defined by dest_id and filter_id from the
    WBEM server defined by server_url
    """
    # pylint: disable=redefined-outer-name
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'subscription', 'remove-subscription',
         dest_id, filter_id])
    good_response = stdout.strip('\n')
    assert good_response == \
        'Removed 1 subscription(s) for destination-id: {}, filter-id: ' \
        '{}.'.format(dest_id, filter_id)

    # Remove the filter
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'subscription', 'remove-filter',
         filter_id])
    good_response = stdout.strip('\n')
    assert good_response == \
        'Removed owned indication filter: identity={0}, ' \
        'Name=pywbemfilter:defaultpywbemcliSubMgr:{0}.'.format(filter_id)

    # Remove the destination
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', 'subscription', 'remove-destination',
         dest_id])

    good_response = stdout.strip('\n')
    assert good_response == \
        'Removed owned indication destination: identity={0}, ' \
        'Name=pywbemdestination:defaultpywbemcliSubMgr:{0}.'.format(dest_id)
