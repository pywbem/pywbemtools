# Copyright 2023 IBM Corp. All Rights Reserved.
# Copyright 2023 Inova Development All Rights Reserved.
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
Test subscription command group commands. This test creates indication filters,
listener destinations, and subscriptions, requests indications from an
Open Pegasus server, confirms the correct number of indications sent and, and
removes the subscription from the server.  If fails if the requested number
of indications not received.  The test may be repeated by calling
execute_indication_test(...) multiple times.

"""


import socket
import os
import time

# pylint: disable=unused-import
from .utils import server_url, validate_namespace_exists, \
    validate_indication_profile, validate_required_classes, \
    create_indication_subscription, remove_subscription, \
    exec_pywbemcli_cmd   # noqa: F401
# pylint: enable=unused-import

from ..unit.utils import execute_command


def exec_pywbemlistener_cmd(request_params, expected_rc=0, ignore_stderr=False,
                            verbose=False):
    """
    Execute a pywbemlistener request with the list of parameters provided in
    request_params and assert if rc != 0. When ignore_stderr is set, the test
    ignores values in the stderr returned.

    If expected_rc == 0
        Returns stdout if rc = 0 or asserts if rc != 0
    if expected_rc != 0
        Returns stderr if expected_rc == rc or asserts if expected_rc != rc

    Allows code where a non-zero stderr is returned when
    rc == 0. the ingore_stderr parameter allows bypassing this.
    """
    if verbose:
        print(f"Exec_listener_cmd {request_params}")
    rc, stdout, stderr = execute_command('pywbemlistener', request_params)
    if verbose:
        print(f"Listener startup result rc={rc}, stderr={stderr}")

    if expected_rc == 0:
        assert rc == 0, f"pywbemlistener failed: params={request_params}, " \
            f"{rc=}, {stderr=}"
        if not ignore_stderr:
            assert stderr == '', \
                f"pywbemlistener stderr={stderr}, rc={rc}"
        return stdout

    # expected rc not 0
    assert rc == expected_rc, f"pywbemlistener failed: " \
                              f"params={request_params} failed {rc=}, " \
                              f"{stderr=} "
    return stderr


def execute_indication_test(
        svr_url, ind_dest_scheme, ind_dest_addr,
        listener_scheme, listener_bind_addr, listener_port,
        indication_send_count, verbose):  # noqa: F811
    # pylint: disable=redefined-outer-name
    """
    Execute the indication test with the parameters provided. The test includes
    creating the subscription, creating the listener, requesting a defined
    number of indications from the WBEM server, waiting for the indications to
    be received, and removing the subscription.

    The verbose flag adds a number of console outputs as the test proceeds.
    """
    if verbose:
        print(f"Test for {ind_dest_scheme=}, "
              f"{ind_dest_addr=}, "
              f"{listener_scheme=}, "
              f"{listener_bind_addr=}, "
              f"{listener_port=}")
    filter_id = 'ofilter1'
    dest_id = 'odest1'
    test_result = None

    source_namespaces = 'test/TestProvider'
    query = 'SELECT * from Test_IndicationProviderClass'

    if verbose:
        print(f"Create subscription. svr_url={svr_url} "
              f"ind_dest_scheme={ind_dest_scheme}, "
              f"ind_dest_addr={ind_dest_addr}, listener_port={listener_port}, "
              f"destid={dest_id}, filterid={filter_id}, "
              f"query={query}, source_namespaces={source_namespaces}")

    create_indication_subscription(
        svr_url, ind_dest_scheme, ind_dest_addr,
        listener_port, dest_id, filter_id, query, source_namespaces)

    # Create listener that writes to a file
    listener_name = 'lis1-end2endtest'
    if verbose:
        print(f"Create listener named {listener_name}")

    # Define file name,remove existing, create empty indication count file
    # line count from this file is number of indications received.
    indication_count_file = "end2endindication_output.txt"
    if os.path.isfile(indication_count_file):
        os.remove(indication_count_file)
    with open(indication_count_file, 'w', encoding='UTF-8'):
        pass

    if verbose:
        print(f"Create listener name={listener_name} port={listener_port} "
              f"scheme={listener_scheme} indi-file={indication_count_file}")

    exec_pywbemlistener_cmd(['start', listener_name,
                             '--port', str(listener_port),
                             '--scheme', listener_scheme,
                             '--bind-addr', listener_bind_addr,
                             '--indi-file', indication_count_file],
                            verbose=verbose)

    exec_pywbemlistener_cmd(['list'], verbose=verbose)

    if verbose:
        print(f"Debug Send invoke method for {indication_send_count} instances")
    result = exec_pywbemcli_cmd(
        ['-s', svr_url, '--no-verify', '--log', 'all', 'class',
         'invokemethod',
         'Test_IndicationProviderClass',
         'SendTestIndicationsCount',
         '--namespace',
         source_namespaces,
         '--parameter',
         f'indicationSendCount={indication_send_count}'])

    if verbose:
        print(f"Debug: invoke method result {result}")

    test_result = wait_for_indications(indication_send_count,
                                       indication_count_file,
                                       verbose)

    # Close listener
    if verbose:
        print('Debug Close listener')
    exec_pywbemlistener_cmd(['stop', listener_name], verbose=verbose)

    # Remove subscriptions
    if verbose:
        print("Remove subscription")
    remove_subscription(svr_url, dest_id, filter_id)

    if test_result:
        assert False, test_result


def wait_for_indications(indication_send_count, indication_count_file,
                         verbose):
    """
    Wait and count indications received. Exactly the required number of
    indications must be returned and counted in a time period determined
    by the indication_send_count.

    Returns None if successful or fail message if indication
    """
    # Wait for indications to be received with timeout.
    # This counts the number of loops with nothing received and with
    # less than requested received. This accounts for possibility of too many
    # indications sent by waiting for at least 2 seconds extended by number
    # if indications expected
    max_loop_count = int(2 + (indication_send_count / 50))

    rcvd_indication_count = 0
    loop_counter = 0  # Set to zero each time indications received.

    test_result = None
    while loop_counter <= max_loop_count:
        loop_counter += 1
        time.sleep(1)

        # Count indications received in file by counting lines
        with open(indication_count_file, encoding='UTF-8') as fp:
            rcvd_lines = len(fp.readlines())
            if verbose:
                print(f"rcvd {rcvd_lines} indications, loop {loop_counter}")

        # Restart loop counter when any indications received
        if rcvd_indication_count < rcvd_lines:
            rcvd_indication_count = rcvd_lines
            if verbose:
                print(f"Rcvd {rcvd_indication_count} indications  "
                      f"loop_counter {loop_counter}")
            loop_counter = 0

        if rcvd_lines == indication_send_count:
            if verbose:
                print(f"Received expected number of indications {rcvd_lines}")
            break
        # If requested number of indications received, break loop
        if rcvd_lines > indication_send_count:
            test_result = f"Received too many indications rcvd={rcvd_lines}, " \
                          f"expected={indication_send_count}"
            break

    else:
        test_result = f"Waited too long for indications. " \
                      f"Rcvd {rcvd_indication_count} " \
                      f"indications, expected {indication_send_count}."
        if verbose:
            print(
                f"Loop counter {loop_counter} max_loop_count {max_loop_count}")
    return test_result or None


def test_indications(server_url):  # noqa: F811
    # pylint: disable=redefined-outer-name
    """
    The indication test.  This function is called because server_url is a pytest
    fixture.
    """

    verbose = False

    # Get a real IP address for the machine to insert into the
    # indication_destination_host variable. This must be an address available
    # to both the test machine/vm/etc. and the container in which OpenPegasus
    # is running so OpenPegasus can route indications to the listener.
    # cannot be localhost, etc.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    indication_dest_host = sock.getsockname()[0]
    sock.close()

    if verbose:
        print(f"Indication_dest_host {indication_dest_host}")

    interop = validate_namespace_exists(server_url, 'interop', 'root/interop')

    validate_indication_profile(server_url, ('SNIA', 'Indication', '1.2.0'))

    required_classes = {interop: ['CIM_ListenerDestinationCIMXML',
                                  'CIM_IndicationFilter',
                                  'CIM_IndicationSubscription', ], }

    validate_required_classes(server_url, required_classes)

    # Two network addresses are associated with the listener:
    # 1. The destination url for indications that is part of the Destination
    #    instance of the subscription.  This must be a real public destination
    #    URL for indications created by the server. In this code that is the
    #    ind_dest_scheme, ind_dest_addr and listener_port.
    # 2. The bind address for the indication listener that defines the
    #    the network interfaces on which the listener will accept indications
    #    This is the listener_scheme either a specific public IP address or a
    #    wildcard address and the listener port.

    # Subscription destination URL parameters
    ind_dest_scheme = 'http'
    ind_dest_addr = indication_dest_host

    # TODO: Extend to include both http and https listener ports.
    # listener bind url parameters
    listener_scheme = 'http'
    # tests parameters for bind to IP and wildcard bind.
    listener_bind_addr_ip = indication_dest_host
    listener_bind_addr_wc = "0.0.0.0"

    # listener and indication_dest port are the same
    listener_port = 5000

    # Sending only a single indication because we have issues with losing
    # indications. They get stuck in the WBEM Server See pywbem issue.
    indication_send_count = 1

    # Execute the test.  If successful, will return. If fail, the
    # test asserts. Test1, with bind IP, test2 wildcard bind
    execute_indication_test(server_url, ind_dest_scheme, ind_dest_addr,
                            listener_scheme, listener_bind_addr_wc,
                            listener_port, indication_send_count, verbose)

    execute_indication_test(server_url, ind_dest_scheme, ind_dest_addr,
                            listener_scheme, listener_bind_addr_ip,
                            listener_port, indication_send_count, verbose)
