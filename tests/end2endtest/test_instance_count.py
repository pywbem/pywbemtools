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


def create_table(stdout):
    """
    Convert the returned table to a list of lists, one item for each
    component in an inner list and one list for each row in the outer list
    """
    table_lines = stdout.strip('\n').split('\n')[3:]
    table = []
    for line in table_lines:
        # match 3 groups of characters separated by spaces
        m = re.match(r'^(\S+) *(\S+) *(.+?)$', line)
        assert m, "Cannot parse output line: {!r}".format(line)
        table.append(m.groups())
    return table


def test_instance_count(server_url):  # noqa: F811
    # pylint: disable=redefined-outer-name
    """
    Test instance count command against OpenPegasus server.
    """

    # Check the instance count operation that will return a success and
    # valid data
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--no-verify', '-o', 'simple', 'instance', 'count',
         '-n', 'root/cimv2'])

    table_lines = create_table(stdout)
    # Why this not in rslt assert ('Namespace', 'Class', 'count') in table_lines
    assert ('root/cimv2', 'PG_ComputerSystem', '1') in table_lines
    assert ('root/cimv2', 'PG_OperatingSystem', '1') in table_lines

    # Test instance count against OpenPegasus with option that produces
    # CIMError from the server but from which pywbemcli should simply
    # produce a line in a report.
    stdout = exec_pywbemcli_cmd(
        ['-s', server_url, '--verbose', '--no-verify', '-o', 'simple',
         'instance', 'count', '-n', 'test/TestProvider',
         '--ignore-class', 'TST_FaultyInstance,TST_FaultyInstanceSub'],
        ignore_stderr=True)

    table_lines = create_table(stdout)
    assert ('test/TestProvider', 'TEST_Family', 'CIMError CIM_ERR_NOT_FOUND') \
        in table_lines

# FUTURE: Add test that causes Error exception ex. count against PG_Internal
# namespace. Issue is that the probably breaks test environment since the
# apparently OpenPegasus fails. The only way this could work is to be the last
# test against the container assuming that the container is restarted for each
#  testsagainst a particular environment or having the container automatically
# restart.
