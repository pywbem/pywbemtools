# (C) Copyright 2023 IBM Corp.
# (C) Copyright 2023 Inova Development Inc.
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
Unit tests for the tab-completer functions implemented in pywbemcli that are
executed when the user does <TAB> and the shell or repl calls back to pywbemcli
with a partial entity (argument or option value) to get possible completion.

These unit tests just test the completer functions themselves in isolation but
not in a command line environment.
"""

from __future__ import absolute_import, print_function

import os
import io
import packaging.version
import pytest
import click

from pywbemtools.pywbemcli._cmd_help import help_arg_subject_shell_completer
from pywbemtools.pywbemcli.pywbemcli import connection_name_completer
from pywbemtools.pywbemcli._warnings import TabCompletionError
# pylint: disable=relative-beyond-top-level
from ..pytest_extensions import simplified_test_function
# pylint: enable=relative-beyond-top-level

# pylint: disable=use-dict-literal

# Click version as a tuple. Used to control tab-completion features
CLICK_VERSION = packaging.version.parse(click.__version__).release
# boolean True if click version 8 or greater.
CLICK_V_8 = CLICK_VERSION[0] >= 8


TEST_CONNECTION_YAML = """connection_definitions:
    testconn:
        name: testconn
        server: http://blah
        user: fred
        password: fred
        default-namespace: root/cimv2
        timeout: 30
        use-pull: null
        pull-max-cnt: 1000
        verify: true
        certfile: cert1.pem
        keyfile: null
        ca-certs: null
        mock-server: []
    tmp1:
        name: tmp1
        server: null
        user: null
        password: null
        default-namespace: root/cimv2
        timeout: 30
        use-pull: null
        pull-max-cnt: 1000
        verify: true
        certfile: null
        keyfile: null
        ca-certs: null
        mock-server:
        - temp_mock_model.mof
default_connection_name: null
"""

SCRIPT_DIR = os.path.dirname(__file__)
CONNECTION_REPO_TEST_FILE_PATH = os.path.join(SCRIPT_DIR,
                                              'tst_tabcompletion.yaml')


@pytest.fixture(scope='function', autouse=True)
def remove_connections_file():
    """Remove the test connection file before and after each test"""

    if os.path.isfile(CONNECTION_REPO_TEST_FILE_PATH):
        os.remove(CONNECTION_REPO_TEST_FILE_PATH)
    yield
    if os.path.isfile(CONNECTION_REPO_TEST_FILE_PATH):
        os.remove(CONNECTION_REPO_TEST_FILE_PATH)


OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet
SKIP = False  # mark tests that are to be skipped.


TESTCASES_CONNECTION_NAME_COMPLETE = [
    # Testcases for pywbemcli.connection_name_complete()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * ctx: Value of connection file or None
    #   * yaml: string containing yaml to put into file
    #   * file_exists: boolean defining whether test expects file to exist
    #   * incomplete; the incomplete value for the connection name
    #   * ext_rtn; list of connection names to be returned
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify with connections file, valid incomplete completes name',
     dict(ctx=CONNECTION_REPO_TEST_FILE_PATH,
          yaml=TEST_CONNECTION_YAML,
          file=CONNECTION_REPO_TEST_FILE_PATH,
          file_exists=True,
          incomplete="testco",
          exp_rtn=["testconn"]),
     None, None, OK),

    ('Verify with connections file, invalid incomplete returns empty list',
     dict(ctx=CONNECTION_REPO_TEST_FILE_PATH,
          yaml=TEST_CONNECTION_YAML,
          file=CONNECTION_REPO_TEST_FILE_PATH,
          file_exists=True,
          incomplete="mock",
          exp_rtn=[]),
     None, None, OK),

    ('Verify with connections file, complete is complete returns name',
     dict(ctx=CONNECTION_REPO_TEST_FILE_PATH,
          yaml=TEST_CONNECTION_YAML,
          file=CONNECTION_REPO_TEST_FILE_PATH,
          file_exists=True,
          incomplete="testconn",
          exp_rtn=["testconn"]),
     None, None, OK),

    ('Verify with connections file, single char incomplete returns name',
     dict(ctx=CONNECTION_REPO_TEST_FILE_PATH,
          yaml=TEST_CONNECTION_YAML,
          file=CONNECTION_REPO_TEST_FILE_PATH,
          file_exists=True,
          incomplete="t",
          exp_rtn=["testconn", 'tmp1']),
     None, None, OK),

    ('Verify with connections file, empty incomplete incomplete returns name',
     dict(ctx=CONNECTION_REPO_TEST_FILE_PATH,
          yaml=TEST_CONNECTION_YAML,
          file=CONNECTION_REPO_TEST_FILE_PATH,
          file_exists=True,
          incomplete="",
          exp_rtn=["testconn", 'tmp1']),
     None, None, OK),

    ('Verify with connections file, incomplete too big fails',
     dict(ctx=CONNECTION_REPO_TEST_FILE_PATH,
          yaml=TEST_CONNECTION_YAML,
          file=CONNECTION_REPO_TEST_FILE_PATH,
          file_exists=True,
          incomplete="testconnextra",
          exp_rtn=[]),
     None, None, OK),

    ('Verify with invalid connections file, warning',
     dict(ctx="CONNECTION_REPO_TEST_FILE_PATH",
          yaml=TEST_CONNECTION_YAML,
          file=CONNECTION_REPO_TEST_FILE_PATH,
          file_exists=False,
          incomplete="",
          exp_rtn=[]),
     None, TabCompletionError, CLICK_V_8),

    # Needs click version as condition to avoid unwanted exception because
    # of the exception expected.
    ('Verify with  invalid connections file, generates warning',
     dict(ctx="CONNECTION_REPO_TEST_FILE_PATH",
          yaml=TEST_CONNECTION_YAML,
          file=None,
          file_exists=False,
          incomplete="",
          exp_rtn=[]),
     None, TabCompletionError, CLICK_V_8),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CONNECTION_NAME_COMPLETE)
@simplified_test_function
def test_connection_name_complete(testcase, ctx, yaml, file, file_exists,
                                  incomplete, exp_rtn):
    """
    Test function for connection_name_complete() function
    """
    # Ignore the test for Click  version 7
    if not CLICK_V_8:
        return

    # Create a fake click context object that contains param "connections_file"
    class ClickContextMock(object):  # pylint: disable=too-few-public-methods
        """ Create a mock click context object containing param attribute """
        def __init__(self):
            self.params = {"connections_file": None}

    # Setup to emulate the params in click ctx
    context = ClickContextMock()
    context.params = {"connections_file": ctx}

    # Conditionally create connections file by writing YAML text to the file
    if file_exists:
        if yaml:
            with io.open(file, "w", encoding='utf-8') as repo_file:
                repo_file.write(yaml)

    param = None  # The method being tested ignores param

    rtn_items = connection_name_completer(context, param, incomplete)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    act_rtn_values = [item.value for item in rtn_items]
    assert act_rtn_values == exp_rtn


TESTCASES_HELP_ARG_SUBJECT_SHELL_COMPLETE = [
    # Testcases for _cmd_help.help_arg_subject_shell_complete()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * incomplete = string representing the incomplete subject name
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify correct completion with last character missing',
     dict(incomplete="act",
          exp_rtn=["activate"]),
     None, None, OK),

    ('Verify correct completion with complete input',
     dict(incomplete="activate",
          exp_rtn=["activate"]),
     None, None, OK),

    ('Verify correct whe incomplete is empty.',
     dict(incomplete="",
          exp_rtn=["repl", "activate", "instancename", "tab-completion"]),
     None, None, OK),

    ('Verify empty rtn when invalid incomplete input, i.e. no match',
     dict(incomplete="blah", exp_rtn=[]),
     None, None, OK),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_HELP_ARG_SUBJECT_SHELL_COMPLETE)
@simplified_test_function
def test_help_arg_subject_shell_complete(testcase, incomplete, exp_rtn):
    """
    Test function for help_arg_subject_shell_complete() function. Note that
    the parameters ctx and param are not used by the function being tested
    """
    # Ignore the test for Click  version lt 8
    if CLICK_VERSION[0] < 8:
        return

    # The code to be tested
    # ctx and param not used by the complete function.
    ctx = None
    param = None
    # Note: Must return a list of click CompletionItem object.
    rtn_items = help_arg_subject_shell_completer(ctx, param, incomplete)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    act_rtn_values = [item.value for item in rtn_items]
    assert act_rtn_values == exp_rtn
