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
from .utils import server_url, validate_namespace_exists, \
    validate_indication_profile, validate_required_classes, \
    create_indication_subscription, remove_subscription, \
    exec_pywbemcli_cmd  # noqa: F401
# pylint: enable=unused-import


def test_subscriptions(server_url):  # noqa: F811
    # pylint: disable=redefined-outer-name
    """
    The test.  This function is called because server_url is a pytest
    fixture.
    """
    interop = validate_namespace_exists(server_url, 'interop', 'root/interop')

    validate_indication_profile(server_url, ('SNIA', 'Indication', '1.2.0'))

    required_classes = {interop: ['CIM_ListenerDestinationCIMXML',
                                  'CIM_IndicationFilter',
                                  'CIM_IndicationSubscription', ], }

    validate_required_classes(server_url, required_classes)

    filter_id = 'ofilter1'
    dest_id = 'odest1'

    create_indication_subscription(server_url, 'http', 'localhost', '5000',
                                   dest_id, filter_id,
                                   'Select * from CIM_AlertIndication',
                                   'root/cimv2')

    # General list command
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', '-o', 'simple',
         'subscription', 'list'])

    good_response = stdout.strip('\n')
    pattern = r"TOTAL INSTANCES +3 +0 +3"
    assert re.search(pattern, good_response)

    # Remove the subscription

    remove_subscription(server_url, dest_id, filter_id)
