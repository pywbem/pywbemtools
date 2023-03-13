
"""
Tests of errors that are common across a wide group of pywbemcli groups and
commands.

This includes:

1. Tests of connection timeout on bad server with all commands. Note that the
command options in these tests are just sufficient to pass command parsing
since all tests should fail with connection error.

2. Test of the --namespace option with namespace that is not in the target
   wbem server.
"""


from __future__ import absolute_import, print_function

import os
import pytest

from .cli_test_extensions import CLITestsBase

# pylint: disable=use-dict-literal

SCRIPT_DIR = os.path.dirname(__file__)
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
SIMPLE_MOCK_FILE_PATH = os.path.join(SCRIPT_DIR, SIMPLE_MOCK_FILE)

OK = True
RUN = True
FAIL = False
SKIP = False

TEST_CASES_CONNECTION_FAIL = [
    # desc - Description of test
    # group - String, defining test group to be executed.
    # cmd - string/required arguments defining the command string
    # condition - If True, the test is executed,  Otherwise it is skipped.

    ['class', 'enumerate', OK],
    ['class', 'get CIM_BLAH', OK],
    ['class', 'delete CIM_BLAH', OK],
    ['class', 'associators CIM_BLAH', OK],
    ['class', 'references CIM_BLAH', OK],
    ['class', 'invokemethod CIM_BLAH methodx', OK],
    ['class', 'find CIM_*', OK],

    ['instance', 'enumerate CIM_Blah', OK],
    ['instance', 'get CIM_BLAH.x=3', OK],
    ['instance', 'create CIM_blah -p x=3', OK],
    ['instance', 'modify CIM_blah.x=3 -p x=4', OK],
    ['instance', 'delete CIM_BLAH.x=3', OK],
    ['instance', 'associators CIM_BLAH.x=3', OK],
    ['instance', 'references CIM_BLAH.x=4', OK],
    ['instance', 'invokemethod CIM_BLAH.x=4 methodx', OK],
    ['instance', 'query select', FAIL],

    ['instance', 'count CIM_*', OK],

    ['connection', 'test', OK],
    # The other connection commands do not connect to a server

    ['qualifier', 'get qualblah', OK],
    ['qualifier', 'enumerate', OK],


    ['server', 'brand', OK],
    ['server', 'info', OK],

    ['profile', 'list', OK],
    ['profile', 'centralinsts', OK],
]


class TestConnectionFail(CLITestsBase):
    """
    Test of the return for a connection error.
    """
    @pytest.mark.parametrize(
        "grp, cmd, condition", TEST_CASES_CONNECTION_FAIL)
    def test_execute_pywbemcli(self, grp, cmd, condition):
        """
        Execute pybemcli with the defined input and test output.
        This tests builds the inputs dictionary nad exp_response dictionary
        from the cmd line inputs.
        """
        desc = "Verify {} args {} fails with connection error".format(grp, cmd)

        # Build inputs dictionary for the test with bad svr name and cmd/args
        inputs = {'general': ['--server', 'http://blahblah', '--timeout', '1'],
                  'args': cmd.split(' ')}

        # Build expected response dictionary that tests for ConnectionError
        exp_response = {'stderr': ['ConnectionError'],
                        'rc': 1,
                        'test': 'innows'}
        mock = None
        self.command_test(desc, grp, inputs, exp_response,
                          mock, condition)


TEST_CASES_NAMESPACE_ERR = [
    # desc - Description of test
    # group - String, defining test group to be executed.
    # cmd - string/required arguments defining the command string
    # condition - If True, the test is executed,  Otherwise it is skipped.

    ['class', 'enumerate --namespace blah', OK],
    ['class', 'get CIM_Foo --namespace blah', OK],
    ['class', 'delete CIM_Foo --namespace blah', OK],
    ['class', 'associators CIM_Foo --namespace blah', OK],
    ['class', 'references CIM_Foo --namespace blah', OK],
    ['class', 'invokemethod CIM_Foo methodx --namespace blah', OK],
    ['class', 'find CIM_* --namespace blah', OK],

    ['instance', 'enumerate CIM_Foo --namespace blah', OK],
    ['instance', 'get CIM_Foo.x=3 --namespace blah', OK],
    ['instance', 'create CIM_Foo -p x=3 --namespace blah', OK],
    ['instance', 'modify CIM_Foo.x=3 -p x=4 --namespace blah', OK],
    ['instance', 'delete CIM_Foo.x=3 --namespace blah', OK],
    ['instance', 'associators CIM_Foo.x=3 --namespace blah', OK],
    ['instance', 'references CIM_Foo.x=4 --namespace blah', OK],
    ['instance', 'invokemethod CIM_Foo.x=4 methodx --namespace blah', OK],
    # pywbem issue # 2313 - Fails with QueryLanguage, not namespace error
    # ['instance', 'query select --namespace blah', OK],

    ['instance', 'count CIM_* --namespace blah', OK],

    ['qualifier', 'get qualblah --namespace blah', OK],
    ['qualifier', 'enumerate --namespace blah', OK],
]


class TestNamespaceError(CLITestsBase):
    """
    Test of the return for a connection error.
    """
    @pytest.mark.parametrize(
        "grp, cmd, condition", TEST_CASES_NAMESPACE_ERR)
    def test_execute_pywbemcli(self, grp, cmd, condition):
        """
        Execute pybemcli with the defined input and test output.
        This tests builds the inputs dictionary nad exp_response dictionary
        from the cmd line inputs.
        """
        desc = "Verify {} args {} fails with namespace error".format(grp, cmd)

        # Build inputs dictionary for the test with bad svr name and cmd/args
        inputs = {'args': cmd.split(' ')}

        # Build expected response dictionary that tests for ConnectionError
        exp_response = {'stderr': ['CIMError', 'CIM_ERR_INVALID_NAMESPACE'],
                        'rc': 1,
                        'test': 'innows'}
        mock = SIMPLE_MOCK_FILE_PATH
        self.command_test(desc, grp, inputs, exp_response,
                          mock, condition)
