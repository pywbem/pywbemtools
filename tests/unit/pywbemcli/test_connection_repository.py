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

import sys
import os
import io
from contextlib import contextmanager
from mock import patch
import pytest

import pywbemtools.pywbemcli._connection_repository
from pywbemtools.pywbemcli._connection_repository import ConnectionRepository, \
    ConnectionsFileLoadError, ConnectionsFileWriteError
from pywbemtools._utils import B08_DEFAULT_CONNECTIONS_FILE, \
    DEFAULT_CONNECTIONS_FILE
from pywbemtools.pywbemcli._pywbem_server import PywbemServer

from ..pytest_extensions import simplified_test_function

# pylint: disable=use-dict-literal

# Click (as of 7.1.2) raises UnsupportedOperation in click.echo() when
# the pytest capsys fixture is used. That happens only on Windows.
# See Click issue https://github.com/pallets/click/issues/1590. This
# run condition skips the testcases on Windows.
CLICK_ISSUE_1590 = sys.platform == 'win32'

SCRIPT_DIR = os.path.dirname(__file__)
CONNECTION_REPO_TEST_FILE_PATH = os.path.join(SCRIPT_DIR,
                                              'tst_connection_repository.yaml')

YAML_GOOD_TWO_DEFS = u"""connection_definitions:
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

YAML_GOOD_NO_DEF = u"""connection_definitions: {}
default_connection_name: null
"""

YAML_MISSING_DEFAULT = u"""connection_definitions:
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

YAML_MISSING_CONNDEFS = u"""tst1:
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

YAML_INVALID_ATTR_NAME = u"""connection_definitions:
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

YAML_INVALID_SYNTAX = u"""connection_definitions:
    *+&%:
default_connection_name: null
"""

YAML_INVALID_MOCKSERVER_TYPE = u"""connection_definitions:
    tst1:
        name: tst1
        mock-server: 42
default_connection_name: null
"""

YAML_INVALID_TIMEOUT_VALUE = u"""connection_definitions:
    tst1:
        name: tst1
        server: http://blah
        timeout: -100
default_connection_name: null
"""

YAML_SERVER_AND_MOCKSERVER = u"""connection_definitions:
    tst1:
        name: tst1
        server: http://blah
        mock-server: 'blah'
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
    file = CONNECTION_REPO_TEST_FILE_PATH
    if os.path.isfile(file):
        os.remove(file)
    file = CONNECTION_REPO_TEST_FILE_PATH + '.bak'
    if os.path.isfile(file):
        os.remove(file)
    file = CONNECTION_REPO_TEST_FILE_PATH + '.tmp'
    if os.path.isfile(file):
        os.remove(file)
    # The yield causes the remainder of this fixture to be executed at the
    # end of the test.
    yield
    file = CONNECTION_REPO_TEST_FILE_PATH
    if os.path.isfile(file):
        os.remove(file)
    file = CONNECTION_REPO_TEST_FILE_PATH + '.bak'
    if os.path.isfile(file):
        os.remove(file)
    file = CONNECTION_REPO_TEST_FILE_PATH + '.tmp'
    if os.path.isfile(file):
        os.remove(file)


# The real functions before they get patched
REAL_OS_RENAME = os.rename
REAL_OS_RENAME_STR = 'os.rename'
# pylint: disable=protected-access
REAL_OPEN_TEXT_FILE = \
    pywbemtools.pywbemcli._connection_repository.open_text_file
REAL_OPEN_TEXT_FILE_STR = \
    'pywbemtools.pywbemcli._connection_repository.open_text_file'


def rename_to_bak_fails(file1, file2):
    """
    Patch function replacing os.rename() that raises OSError when the target
    file ends with '.bak'.
    """
    if file2.endswith('.bak'):
        raise OSError("Mocked failure: Cannot rename {} to {}".
                      format(file1, file2))
    REAL_OS_RENAME(file1, file2)


def rename_from_tmp_fails(file1, file2):
    """
    Patch function replacing os.rename() that raises OSError when the source
    file ends with '.tmp'.
    """
    if file1.endswith('.tmp'):
        raise OSError("Mocked failure: Cannot rename {} to {}".
                      format(file1, file2))
    REAL_OS_RENAME(file1, file2)


def rename_fails(file1, file2):
    """
    Patch function replacing os.rename() that raises OSError.
    """
    raise OSError("Mocked failure: Cannot rename {} to {}".
                  format(file1, file2))


@contextmanager
def open_text_file_write_fails(filename, file_mode):
    """
    Patch function replacing open_text_file() that raises
    OSError when the file is opened in write mode.
    """
    if 'w' in file_mode:
        raise OSError("Mocked failure: Cannot open {} in mode {}".
                      format(filename, file_mode))
    # Delegate the context manager yield to REAL_OPEN_TEXT_FILE()
    return REAL_OPEN_TEXT_FILE(filename, file_mode)


@contextmanager
def open_text_file_read_fails(filename, file_mode):
    """
    Patch function replacing open_text_file() that raises
    OSError when the file is opened in read mode.
    """
    if 'r' in file_mode:
        raise OSError("Mocked failure: Cannot open {} in mode {}".
                      format(filename, file_mode))
    # Delegate the context manager yield to REAL_OPEN_TEXT_FILE()
    return REAL_OPEN_TEXT_FILE(filename, file_mode)


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
        "Verify creation of good repo with no conn def, no default",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[],
            default=None,
            exp_rtn=dict(
                keys=[],
                default=None
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify creation of good repo with 1 conn def, no default",
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
        "Verify creation of good repo with 1 conn def and 1st as default",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1")],
            default='tst1',
            exp_rtn=dict(
                keys=['tst1'],
                default='tst1'
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify creation of good repo with 2 conn defs, no default",
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
        "Verify creation of good repo with 2 conn defs and 1st as default",
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
        "Verify creation of good repo with 2 conn defs and 2nd as default",
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
        "Verify creation of good repo with no conn def, but setting "
        "non-existing as default (fails)",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[],
            default='non_existing',
            exp_rtn=None
        ),
        KeyError, None, OK,
    ),
    (
        "Verify creation of good repo with 1 conn def, but setting "
        "non-existing as default (fails)",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1")],
            default='non_existing',
            exp_rtn=None
        ),
        KeyError, None, OK,
    ),
    (
        "Verify creation of good repo with 2 conn defs, but setting "
        "non-existing as default (fails).",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://blah', name="tst1"),
                  PywbemServer('http://blah2', name="tst2")],
            default='non_existing',
            exp_rtn=None
        ),
        KeyError, None, OK,
    ),
]


@pytest.mark.usefixtures("remove_file_before_after")
@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CREATE_CONNECTION_REPOSITORY)
@simplified_test_function
def test_create_connection_repository(testcase, file, svrs, default, exp_rtn):
    """
    Test the creation, adding and setting a default for the connection
    repository, with good data and errors.
    """

    # The code to be tested
    repo = ConnectionRepository(file)
    for svr in svrs:
        repo.add(svr)
    repo.default_connection_name = default

    # Since we want to test the creation, addition and default setting, any
    # expected exceptions must have already been raised, thus if we get to
    # here, no exception was expected. Verify that.
    assert testcase.exp_exc_types is None

    # Test what is in file by opening second connection to load same file
    repo_2 = ConnectionRepository(file)
    assert sorted(repo_2.keys()) == sorted(exp_rtn['keys'])
    assert repo_2.default_connection_name == exp_rtn['default']

    # validate the file name
    conn_file = repo.connections_file
    assert conn_file == file

    # validate the default connection
    repo_default = repo.default_connection_name
    assert repo_default == exp_rtn['default']

    # validate basic values in __str__()
    str_repo = str(repo)
    assert file in str_repo

    # validate basic values in __repr__()
    repr_repo = repr(repo)
    assert repr(file) in repr_repo
    for key in exp_rtn['keys']:
        assert "{!r}:".format(key) in repr_repo

    # validate __len__()
    len_repo = len(repo)
    assert len_repo == len(exp_rtn['keys'])

    # validate __contains__()
    for key in exp_rtn['keys']:
        assert key in repo

    # validate __iter__()
    rtn_keys = []
    for name in repo:
        rtn_keys.append(name)
    assert sorted(rtn_keys) == sorted(exp_rtn['keys'])

    # validate iterkeys()
    rtn_keys = []
    for name in repo.iterkeys():
        rtn_keys.append(name)
    assert sorted(rtn_keys) == sorted(exp_rtn['keys'])

    # validate iteritems()
    rtn_keys = []
    for name, _ in repo.iteritems():
        rtn_keys.append(name)
    assert sorted(rtn_keys) == sorted(exp_rtn['keys'])

    # validate keys()
    rtn_keys = []
    for name in repo.keys():
        rtn_keys.append(name)
    assert sorted(rtn_keys) == sorted(exp_rtn['keys'])

    # validate items()
    rtn_keys = []
    for name, _ in repo.items():
        rtn_keys.append(name)
    assert sorted(rtn_keys) == sorted(exp_rtn['keys'])


# Testcases for connection file load errors
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

TESTCASES_CONNECTION_FILE_LOAD_ERROR = [
    (
        "Verify good file with 2 conn defs and no default set",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_GOOD_TWO_DEFS,
            exp_rtn=dict(
                keys=['tst1', 'tst2'],
                default=None
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify load fails when file misses top-level property for default",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_MISSING_DEFAULT,
            exp_rtn=None,
        ),
        ConnectionsFileLoadError, None, OK,
    ),
    (
        "Verify load fails when file misses top-level property for conn defs",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_MISSING_CONNDEFS,
            exp_rtn=None,
        ),
        ConnectionsFileLoadError, None, OK,
    ),
    (
        "Verify load fails when file is completely empty",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=u'',
            exp_rtn=None,
        ),
        ConnectionsFileLoadError, None, OK,
    ),
    (
        "Verify load fails when a conn def attribute has unknown name",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_INVALID_ATTR_NAME,
            exp_rtn=None,
        ),
        ConnectionsFileLoadError, None, OK,
    ),
    (
        "Verify load fails when YAML syntax is invalid",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_INVALID_SYNTAX,
            exp_rtn=None,
        ),
        ConnectionsFileLoadError, None, OK,
    ),
    (
        "Verify load fails when conn def mock-server attr has invalid type",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_INVALID_MOCKSERVER_TYPE,
            exp_rtn=None,
        ),
        ConnectionsFileLoadError, None, OK,
    ),
    (
        "Verify load fails when conn def timeout attr has invalid value",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_INVALID_TIMEOUT_VALUE,
            exp_rtn=None,
        ),
        ConnectionsFileLoadError, None, OK,
    ),
    (
        "Verify load fails when conn def has both server and mock-server",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_SERVER_AND_MOCKSERVER,
            exp_rtn=None,
        ),
        ConnectionsFileLoadError, None, OK,
    ),
]


@pytest.mark.usefixtures("remove_file_before_after")
@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CONNECTION_FILE_LOAD_ERROR)
@simplified_test_function
def test_connection_file_load_error(testcase, file, yaml, exp_rtn):
    """
    Test the loading of a YAML file that has errors to confirm the
    exceptions generated.
    """
    # Write the YAML text to the file
    with io.open(file, "w", encoding='utf-8') as repo_file:
        repo_file.write(yaml)

    # This does not load the file yet, so it succeeds even for a bad file
    repo = ConnectionRepository(file)

    # This loads the file and will raise any exceptions during loading
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
            yaml=YAML_GOOD_TWO_DEFS,
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
            yaml=YAML_GOOD_TWO_DEFS,
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
        "Verify add works to file that has 0 connections",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml=YAML_GOOD_NO_DEF,
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
        "Verify add works to completely empty file that exists",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            yaml="",
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
        "Verify add works to non-existent file",
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
        with io.open(file, "w", encoding='utf-8') as repo_file:
            repo_file.write(yaml)

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


# Testcases for delete from ConnectionRepository
#       Each list item is a testcase tuple with these items:
#       * desc: Short testcase description.
#       * kwargs: Keyword arguments for the test function:
#           * file: test file path. File to test built into this file path
#           * svrs: Servers to add to the repository
#           * default: Default to set
#           * del_svr: Name of server to be deleted
#           * exp_rtn: Expected return value of _format_instances_as_rows().
#             * keys: keys expected in file
#             * default: Value for default server to test to test
#       * exp_exc_types: Expected exception type(s), or None.
#       * exp_rtn: Expected warning type(s), or None.
#       * condition: Boolean condition for testcase to run, 'pdb' for debugger

TESTCASES_CONNECTION_REPOSITORY_DELETE = [
    (
        "Verify deletion of existing conn in repo with 1 conn and no default",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://args', name="tst1")],
            default=None,
            del_svr='tst1',
            exp_rtn=dict(
                keys=[],
                default=None
            ),
        ),
        None, None, OK,
    ),
    (
        "Verify deletion of existing conn in repo with 1 conn and default set",
        dict(
            file=CONNECTION_REPO_TEST_FILE_PATH,
            svrs=[PywbemServer('http://args', name="tst1")],
            default='tst1',
            del_svr='tst1',
            exp_rtn=dict(
                keys=[],
                default=None
            ),
        ),
        None, None, OK,
    ),
]


@pytest.mark.usefixtures("remove_file_before_after")
@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CONNECTION_REPOSITORY_DELETE)
@simplified_test_function
def test_connection_repository_delete(
        testcase, file, svrs, default, del_svr, exp_rtn):
    """
    Test the deletion of conn defs from the connection repository.
    """

    repo = ConnectionRepository(file)
    for svr in svrs:
        repo.add(svr)
    repo.default_connection_name = default

    # The code to be tested
    repo.delete(del_svr)

    assert testcase.exp_exc_types is None

    # Validate repo after successful deletion
    assert sorted(repo.keys()) == sorted(exp_rtn['keys'])
    assert repo.default_connection_name == exp_rtn['default']


# Testcases connection file load errors (mocked)
#       Each list item is a testcase tuple with these items:
#       * desc: Short testcase description.
#       * kwargs: Keyword arguments for the test function:
#           * orig_func_str: String with pkg.name of original function
#           * patch_func: Patch function replacing original function
#       * exp_exc_types: Expected exception type(s), or None.
#       * exp_rtn: Expected warning type(s), or None.
#       * condition: Boolean condition for testcase to run, 'pdb' for debugger

TESTCASES_CONNECTION_FILE_LOAD_ERROR_M = [
    (
        "Verify connection file open for writing fails",
        dict(
            orig_func_str=REAL_OPEN_TEXT_FILE_STR,
            patch_func=open_text_file_read_fails,
        ),
        ConnectionsFileLoadError, None, OK,
    ),
]


@pytest.mark.usefixtures("remove_file_before_after")
@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CONNECTION_FILE_LOAD_ERROR_M)
@simplified_test_function
def test_connection_file_load_error_m(
        testcase, orig_func_str, patch_func):
    """
    Test the loading of a connections file with patched functions injecting
    errors.
    """

    # Create the connections file
    repo = ConnectionRepository(CONNECTION_REPO_TEST_FILE_PATH)
    repo.add(PywbemServer('http://args', name="tst1"))

    # The second repo has not loaded the file yet
    repo2 = ConnectionRepository(CONNECTION_REPO_TEST_FILE_PATH)

    with patch(orig_func_str, patch_func):

        # The code to be tested.
        # This triggers the loading of the file.
        repo2.keys()

    assert testcase.exp_exc_types is None


# Testcases connection file write errors (mocked)
#       Each list item is a testcase tuple with these items:
#       * desc: Short testcase description.
#       * kwargs: Keyword arguments for the test function:
#           * orig_func_str: String with pkg.name of original function
#           * patch_func: Patch function replacing original function
#       * exp_exc_types: Expected exception type(s), or None.
#       * exp_rtn: Expected warning type(s), or None.
#       * condition: Boolean condition for testcase to run, 'pdb' for debugger

TESTCASES_CONNECTION_FILE_WRITE_ERROR = [
    (
        "Verify connection file open for writing fails",
        dict(
            create_file=False,
            orig_func_str=REAL_OPEN_TEXT_FILE_STR,
            patch_func=open_text_file_write_fails,
        ),
        ConnectionsFileWriteError, None, OK,
    ),
    (
        "Verify connection file rename to .bak fails",
        dict(
            create_file=True,
            orig_func_str=REAL_OS_RENAME_STR,
            patch_func=rename_to_bak_fails,
        ),
        ConnectionsFileWriteError, None, OK,
    ),
    (
        "Verify connection file rename from .tmp fails",
        dict(
            create_file=False,
            orig_func_str=REAL_OS_RENAME_STR,
            patch_func=rename_from_tmp_fails,
        ),
        ConnectionsFileWriteError, None, OK,
    ),
]


@pytest.mark.usefixtures("remove_file_before_after")
@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CONNECTION_FILE_WRITE_ERROR)
@simplified_test_function
def test_connection_file_write_error(
        testcase, create_file, orig_func_str, patch_func):
    """
    Test the writing of a connections file with patched functions injecting
    errors.
    """

    # Create a repo, but do not load or create the file yet, so it still does
    # not exist at this point.
    repo = ConnectionRepository(CONNECTION_REPO_TEST_FILE_PATH)
    svr1 = PywbemServer('http://args', name="tst1")
    svr2 = PywbemServer('http://args', name="tst2")

    if create_file:
        repo.add(svr1)

    with patch(orig_func_str, patch_func):

        # The code to be tested.
        # This triggers the file to be written.
        repo.add(svr2)

    assert testcase.exp_exc_types is None


# Testcases for connection file migration
#       Each list item is a testcase tuple with these items:
#       * desc: Short testcase description.
#       * failure: Type of failure to set up for.
#       * exp_exc_type: Expected exception type, or None.

TESTCASES_CONNECTION_FILE_MIGRATION = [
    (
        "Verify successful migration of old file",
        "none",
        None,
    ),
    (
        "Verify migration of old file that fails during rename (mocked)",
        "rename",
        ConnectionsFileLoadError,
    ),
]


@pytest.mark.parametrize(
    "desc, failure, exp_exc_type",
    TESTCASES_CONNECTION_FILE_MIGRATION)
def test_connection_file_migration(desc, failure, exp_exc_type, capsys):
    # pylint: disable=unused-argument
    """
    Test the migration of an old connections file.
    """

    # A possibly existing user-owned default connections file has already been
    # by fixture set_connections_file, so in theory, we can be sure it does not
    # exist. In case other testcases leave the file as garbage, we still make
    # sure it does not exist.
    if os.path.isfile(DEFAULT_CONNECTIONS_FILE):
        os.remove(DEFAULT_CONNECTIONS_FILE)

    # Create the old default connections file.
    repo_old = ConnectionRepository(B08_DEFAULT_CONNECTIONS_FILE)
    repo_old.add(PywbemServer('http://args', name="tst1"))
    assert os.path.isfile(B08_DEFAULT_CONNECTIONS_FILE)

    # Create a repo that uses the new default connections file, but do not
    # load or create the file yet, so it still does not exist at this point.
    repo = ConnectionRepository(DEFAULT_CONNECTIONS_FILE)
    assert not os.path.isfile(DEFAULT_CONNECTIONS_FILE)

    try:

        if failure == 'none':
            if CLICK_ISSUE_1590:
                pytest.skip("Condition for test case not met")

            # The code to be tested.
            # This triggers a load of the file which performs the migration.
            # We expect a successful migration.
            repo.keys()

            captured = capsys.readouterr()
            assert "Migrated old connections file" in captured.out

        else:
            assert failure == 'rename'
            with patch(REAL_OS_RENAME_STR, rename_fails):
                with pytest.raises(exp_exc_type):

                    # The code to be tested.
                    # This triggers a load which performs the migration.
                    # We expect an exception.
                    repo.keys()

    finally:

        # verify that the patching has been undone
        assert id(os.rename) == id(REAL_OS_RENAME)

        # Cleanup the old default connections file and its backup and temps.
        file = B08_DEFAULT_CONNECTIONS_FILE
        if os.path.isfile(file):
            os.remove(file)
        file = B08_DEFAULT_CONNECTIONS_FILE + '.bak'
        if os.path.isfile(file):
            os.remove(file)
        file = B08_DEFAULT_CONNECTIONS_FILE + '.tmp'
        if os.path.isfile(file):
            os.remove(file)
        assert not os.path.isfile(B08_DEFAULT_CONNECTIONS_FILE)

        # A successful migration leaves a default connections file. Clean it up.
        if os.path.isfile(DEFAULT_CONNECTIONS_FILE):
            os.remove(DEFAULT_CONNECTIONS_FILE)
