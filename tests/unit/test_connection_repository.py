# -*- coding: utf-8 -*-
# (C) Copyright 2020 IBM Corp.
# (C) Copyright 2020 Inova Development Inc.
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
Unit test of connection repository class. Tests the capability to create and
modify good repositories and to catch load errors for repositories that have
errors in the data.
"""

from __future__ import absolute_import, print_function

import os
from mock import patch
import pytest

from tests.unit.pytest_extensions import simplified_test_function

from pywbemtools.pywbemcli._connection_repository import ConnectionRepository, \
    ConnectionsFileError, ConnectionsFileWriteError
from pywbemtools.pywbemcli._pywbem_server import PywbemServer

SCRIPT_DIR = os.path.dirname(__file__)
CONNECTION_REPO_TEST_FILE_PATH = os.path.join(SCRIPT_DIR,
                                              'tst_connection_repository.yaml')

TST_YAML_GOOD = u"""connection_definitions:
    tst1:
        name: tst1
        server: http://blah
        user: fred
        password: fred
        default-namespace: root/cimv2
        timeout: 30
        use_pull: null
        pull_max_cnt: null
        verify: true
        certfile: null
        keyfile: null
        ca-certs: null
        mock-server: []
    tst2:
        name: tst2
        server: http://blah
        user: null
        password: null
        default-namespace: root/cimv2
        timeout: 30
        use_pull: true
        pull_max_cnt: 98
        verify: true
        certfile: null
        keyfile: null
        ca-certs: null
        mock-server: []
default_connection_name: null
"""

YAML_NO_DEFAULT = u"""connection_definitions:
    tst1:
        name: tst1
        server: http://blah
        user: fred
        password: fred
        default-namespace: root/cimv2
        timeout: 30
        use_pull: null
        pull_max_cnt: null
        verify: true
        certfile: null
        keyfile: null
        ca-certs: null
        mock-server: []
"""

YAML_NO_DEFS = u"""tst1:
        name: tst1
        server: http://blah
        user: fred
        password: fred
        default-namespace: root/cimv2
        timeout: 30
        use_pull: null
        pull_max_cnt: null
        verify: true
        certfile: null
        keyfile: null
        ca-certs: null
        mock-server: []
default_connection_name: null
"""

YAML_BAD_NAME = u"""connection_definitions:
    tst1:
        name: tst1
        server: http://blah
        user: fred
        password: fred
        default-namespace: root/cimv2
        timeoutx: 30
        use_pull: null
        pull_max_cnt: null
        verify: true
        certfile: null
        keyfile: null
        ca-certs: null
        mock-server: []
default_connection_name: null
"""

INVALIDYAMLFILE = u"""connection_definitions:;
    tst1:
        name: tst1
default_connection_name: null
"""

INVALID_ITEM_VALUE = u"""connection_definitions:;
    tst1:
        name: tst1
        mock-server: ['blah']
default_connection_name: null
"""

INVALID_ITEM_VALUE_TYPE = u"""connection_definitions:;
    tst1:
        name: tst1
        mock-server: 'blah'
default_connection_name: null
"""

INVALID_TIMEOUT_VALUE = u"""connection_definitions:;
    tst1:
        name: tst1
        server: http://blah
        timeout: -100
default_connection_name: null
"""

OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet


@pytest.fixture()
def remove_file_before_after():
    """
    Remove the connections file at beginning and end of test.
    """
    if os.path.isfile(CONNECTION_REPO_TEST_FILE_PATH):
        os.remove(CONNECTION_REPO_TEST_FILE_PATH)
    # The yield causes the remainder of this fixture to be executed at the
    # end of the test.
    yield
    if os.path.isfile(CONNECTION_REPO_TEST_FILE_PATH):
        os.remove(CONNECTION_REPO_TEST_FILE_PATH)


# Testcases for create ConnectionRepository

#       Each list item is a testcase tuple with these items:
#       * desc: Short testcase description.
#       * kwargs: Keyword arguments for the test function:
#           * file: test file path. File to test built into this file path
#           * svrs: Zero or more instances of PywbemServer class
#           * default: value to set as default server
#           * exp_rtn: Expected return value of _format_instances_as_rows().
#             * keys: keys expected in file
#             * default: Value for default server to test to test
#       * exp_exc_types: Expected exception type(s), or None.
#       * exp_rtn: Expected warning type(s), or None.
#       * condition: Boolean condition for testcase to run, 'pdb' for debugger

TESTCASES_CREATE_CONNECTION_REPOSITORY = [
    (
        "Verify Creation of good repo with one server",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1")],
            default=None,
            exp_rtn=dict(
                keys=['tst1'],
                default=None
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify Creation of good repo with 2 servers, no default",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1"),
                  PywbemServer('http://blah2', name="tst2")],
            default=None,
            exp_rtn=dict(
                keys=['tst1', 'tst2'],
                default=None
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify Creation of good repo with multiple servers and default",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1"),
                  PywbemServer('http://blah2', name="tst2")],
            default='tst1',
            exp_rtn=dict(
                keys=['tst1', 'tst2'],
                default='tst1'
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify Creation of good repo with multiple servers and 1st as default",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1"),
                  PywbemServer('http://blah2', name="tst2")],
            default='tst1',
            exp_rtn=dict(
                keys=['tst1', 'tst2'],
                default='tst1'
            ),
        ),
        None, None, OK,
    ),

    (
        "Verify Creation of good repo with multiple servers and 2nd as default",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1"),
                  PywbemServer('http://blah2', name="tst2")],
            default='tst2',
            exp_rtn=dict(
                keys=['tst1', 'tst2'],
                default='tst2'
            ),
        ),
        None, None, OK,
    ),

    (
        "Verify Creation of good repo with one server but set-default fails",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1")],
            default='tst2',
            exp_rtn=dict(
                keys=['tst1'],
                default='tst2'
            ),
        ),
        ValueError, None, OK,
    ),

    (
        "Verify Creation of good repo with multiple servers and set-default in"
        "error. The error is fixed. Note we cannot test the fix because of "
        "exception.",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1"),
                  PywbemServer('http://blah2', name="tst2")],
            default='tst3',
            exp_rtn=dict(
                keys=['tst1', 'tst2'],
                default=None
            ),
        ),
        ValueError, None, OK,
    ),
]


@pytest.mark.usefixtures("remove_file_before_after")
@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CREATE_CONNECTION_REPOSITORY)
@simplified_test_function
def test_create_connection_repository(testcase, file, svrs, default, exp_rtn):

    """
    Test the creation, loading and save of the connection repository with
    good data and errors
    """
    repo = ConnectionRepository(file)
    for svr in svrs:
        repo.add(svr)

    repo.default_connection_name = default
    repo_default = repo.default_connection_name

    assert testcase.exp_exc_types is None

    assert repo_default == exp_rtn['default']

    # Test what is in file by opening second connection to load file
    repo_2 = ConnectionRepository(file)
    assert sorted(repo_2.keys()) == sorted(exp_rtn['keys'])
    assert sorted(repo_2.keys()) == sorted(repo.keys())
    assert repo.default_connection_name == repo_2.default_connection_name

    assert repo_2.default_connection_name == exp_rtn['default']

    # validate basic values in __str__ and __repr__
    assert file in str(repo_2)
    assert file in repr(repo_2)
    for key in repo_2.keys():
        assert "{}:".format(key) in repr(repo_2)

    rtn_keys = []
    rtn_svrs = []
    for name, svr in repo.items():
        rtn_keys.append(name)
        rtn_svrs.append(svr)

    assert len(rtn_keys) == len(exp_rtn['keys'])
    assert len(repo) == len(rtn_keys)
    assert len(repo) == len(rtn_svrs)


# Testcases for create ConnectionRepository
#       Each list item is a testcase tuple with these items:
#       * desc: Short testcase description.
#       * kwargs: Keyword arguments for the test function:
#           * file: test file path. File to test built into this file path
#           * yaml: YAML to insert into test file
#           * exp_rtn: Expected return value of _format_instances_as_rows().
#             * keys: keys expected in file
#             * default: Value for default server to test to test
#       * exp_exc_types: Expected exception type(s), or None.
#       * exp_rtn: Expected warning type(s), or None.
#       * condition: Boolean condition for testcase to run, 'pdb' for debugger

TESTCASES_CONNECTION_REPOSITORY_ERRORS = [
    (
        "Verify Creation of good repo with one server",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=TST_YAML_GOOD,
            exp_rtn=dict(
                keys=['tst1', 'tst2'],
                default=None
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify load fails when no default section",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_NO_DEFAULT,
            exp_rtn=dict(),
        ),
        ConnectionsFileError, None, OK,
    ),
    (
        "Verify load fails when no connection section",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_NO_DEFS,
            exp_rtn=dict(),
        ),
        ConnectionsFileError, None, OK,
    ),
    (
        "Verify load fails when file empty",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=u'',
            exp_rtn=dict(),
        ),
        ConnectionsFileError, None, OK,
    ),

    (
        "Verify load fails when unknown element in file.",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_BAD_NAME,
            exp_rtn=dict(),
        ),
        ConnectionsFileError, None, OK,
    ),
    (
        "Verify load fails YAML syntax invalid",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=INVALIDYAMLFILE,
            exp_rtn=dict(),
        ),
        ConnectionsFileError, None, OK,
    ),

    (
        "Verify load fails invalid type on key value",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=INVALID_ITEM_VALUE,
            exp_rtn=dict(),
        ),
        ConnectionsFileError, None, OK,
    ),

    (
        "Verify load fails invalid type on key value",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=INVALID_ITEM_VALUE_TYPE,
            exp_rtn=dict(),
        ),
        ConnectionsFileError, None, OK,
    ),

    (
        "Verify load fails invalid value of timeout (negative integer)",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=INVALID_TIMEOUT_VALUE,
            exp_rtn=dict(),
        ),
        ConnectionsFileError, None, OK,
    ),
]


@pytest.mark.usefixtures("remove_file_before_after")
@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CONNECTION_REPOSITORY_ERRORS)
@simplified_test_function
def test_connection_repository_errors(testcase, file, yaml, exp_rtn):
    """
    Test the loading of a YAML file that has errors to confirm the
    exceptions generated.
    """
    # Write the YAML text to the file
    repo_file = open(file, "wt")
    repo_file.write(yaml)
    repo_file.close()

    repo = ConnectionRepository(file)
    # attempt to use file
    repo_keys = repo.keys()

    assert testcase.exp_exc_types is None

    # Confirm file was written if noexceptions
    assert sorted(repo_keys) == sorted(exp_rtn['keys'])
    assert repo.default_connection_name == exp_rtn['default']


# Testcases for add to ConnectionRepository
#       Each list item is a testcase tuple with these items:
#       * desc: Short testcase description.
#       * kwargs: Keyword arguments for the test function:
#           * file: test file path. File to test built into this file path
#           * yaml: YAML to insert into test file
#           * svrs: Servers to add to the repository
#           * default: Default to set
#           * exp_rtn: Expected return value of _format_instances_as_rows().
#             * keys: keys expected in file
#             * default: Value for default server to test to test
#       * exp_exc_types: Expected exception type(s), or None.
#       * exp_rtn: Expected warning type(s), or None.
#       * condition: Boolean condition for testcase to run, 'pdb' for debugger

TESTCASES_CONNECTION_REPOSITORY_ADD = [
    (
        "Verify add with existing name replaces the existing name",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=TST_YAML_GOOD,
            svrs=[PywbemServer('http://args', name="tst1")],
            default=None,
            exp_rtn=dict(
                keys=['tst1', 'tst2'],
                default=None
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify add with new name adds the new name",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=TST_YAML_GOOD,
            svrs=[PywbemServer('http://args', name="tst3")],
            default=None,
            exp_rtn=dict(
                keys=['tst1', 'tst2', 'tst3'],
                default=None
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify load fails when file completly empty but exists. Add fails",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_BAD_NAME,
            svrs=[PywbemServer('http://blah', name="tst1")],
            default=None,
            exp_rtn=dict(
                keys=['tst1', 'tst2'],
                default=None),
        ),
        ConnectionsFileError, None, OK,
    ),
    (
        "Add to non-existent server file works",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=None,
            svrs=[PywbemServer('http://blah', name="tst1")],
            default=None,
            exp_rtn=dict(
                keys=['tst1'],
                default=None),
        ),
        None, None, OK,
    ),
]


@pytest.mark.usefixtures("remove_file_before_after")
@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CONNECTION_REPOSITORY_ADD)
@simplified_test_function
def test_connection_repository_add(testcase, file, yaml, svrs, default,
                                   exp_rtn):
    """
    Test the loading of a YAML file that has errors to confirm the
    exceptions generated.
    """
    # Write the YAML text to the file
    if yaml:
        repo_file = open(file, "wt")
        repo_file.write(yaml)
        repo_file.close()

    repo = ConnectionRepository(file)
    for svr in svrs:
        repo.add(svr)
    repo.default_connection_name = default

    assert testcase.exp_exc_types is None

    # Confirm file was written if noexceptions
    assert sorted(repo.keys()) == sorted(exp_rtn['keys'])
    assert repo.default_connection_name == exp_rtn['default']
    for svr in svrs:
        assert repo[svr.name].server == svr.server

# Testcases ConnectionRepository write method
#       Each list item is a testcase tuple with these items:
#       * desc: Short testcase description.
#       * kwargs: Keyword arguments for the test function:
#           * file: test file path. File to test built into this file path
#           * svrs: Servers to add to the repository
#           * default: Default to set
#       * exp_exc_types: Expected exception type(s), or None.
#       * exp_rtn: Expected warning type(s), or None.
#       * condition: Boolean condition for testcase to run, 'pdb' for debugger


TESTCASES_CONNECTION_REPOSITORY_WRITE = [
    (
        "Verify connection file write fail with mock",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://args', name="tst1")],
            failure="openfile"
        ),
        ConnectionsFileWriteError, None, OK,
    ),
    (
        "Verify connection file rename failure",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://args', name="tst1")],
            failure="rename"
        ),
        ConnectionsFileWriteError, None, OK,
    ),
]


@pytest.mark.usefixtures("remove_file_before_after")
@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CONNECTION_REPOSITORY_WRITE)
@simplified_test_function
def test_connection_repository_write_error(testcase, file, svrs, failure):
    """
    Test the loading of a YAML file that has errors to confirm the
    exceptions generated.
    """
    @patch('pywbemtools.pywbemcli.ConnectionRepository._open_file')
    def mock_fail_open_file(connections_file, mock_write):
        mock_write.side_effect = IOError("foo")
        repo = ConnectionRepository(connections_file)
        for svr in svrs:
            repo.add(svr)

    @patch('os.rename')
    def mock_fail_rename_file(connections_file, mock_rename):
        mock_rename.side_effect = OSError("foo")
        repo = ConnectionRepository(connections_file)
        for svr in svrs:
            repo.add(svr)

    if failure == 'openfile':
        mock_fail_open_file(file)  # pylint: disable=no-value-for-parameter
    elif failure == 'rename':
        mock_fail_rename_file(file)  # pylint: disable=no-value-for-parameter
    else:
        assert False, "Invalid failure attribute in test"

    assert testcase.exp_exc_types is None
