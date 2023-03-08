# Copyright 2020 IBM Corp. All Rights Reserved.
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
Tests the 'namespace' command group.
"""

from __future__ import absolute_import, print_function

import pytest

from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE

# pylint: disable=use-dict-literal

# The mock files used for testing
TEST_INTEROP_MOCK_FILE = 'simple_interop_mock_script.py'
TEST_USER_MOCK_FILE = 'simple_mock_model.mof'

#
# The following list defines the help for each command in terms of particular
# parts of lines that are to be tested.
#
NAMESPACE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] namespace COMMAND [ARGS] '
    '[COMMAND-OPTIONS]',
    'Command group for CIM namespaces.',
    CMD_OPTION_HELP_HELP_LINE,
    'list     List the namespaces of the server.',
    'create   Create a namespace on the server.',
    'delete   Delete a namespace from the server.',
    'interop  Get the Interop namespace of the server.',
]

NAMESPACE_LIST_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] namespace list '
    '[COMMAND-OPTIONS]',
    'List the namespaces of the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

NAMESPACE_CREATE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] namespace create NAMESPACE '
    '[COMMAND-OPTIONS]',
    'Create a namespace on the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

NAMESPACE_DELETE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] namespace delete NAMESPACE '
    '[COMMAND-OPTIONS]',
    'Delete a namespace from the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

NAMESPACE_INTEROP_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] namespace interop '
    '[COMMAND-OPTIONS]',
    'Get the Interop namespace of the server.',
    CMD_OPTION_HELP_HELP_LINE,
]


TEST_CASES = [

    # List of testcases.
    # Each testcase is a tuple with the following items:
    # * desc: Description of testcase.
    # * inputs: String, or tuple/list of strings, or dict of 'env', 'args',
    #     'general', and 'stdin'. See the 'inputs' parameter of
    #     CLITestsBase.command_test() in cli_test_extensions.py for detailed
    #     documentation.
    # * exp_response: Dictionary of expected responses (stdout, stderr, rc) and
    #     test definition (test: <testname>). See the 'exp_response' parameter
    #     of CLITestsBase.command_test() in cli_test_extensions.py for
    #     detailed documentation.
    # * mock: None, name of file (.mof or .py), or list thereof.
    # * condition: If True the test is executed, if 'pdb' the test breaks in the
    #     the debugger, if 'verbose' print verbose messages, if False the test
    #     is skipped.

    #
    # No command, but options of the command group
    #
    (
        "Verify lines in output of command 'namespace --help'",
        ['--help'],
        dict(
            rc=0,
            stdout=NAMESPACE_HELP_LINES,
            test='innows'
        ),
        None, True
    ),
    (
        "Verify order of commands in output of 'namespace --help'",
        ['--help'],
        dict(
            rc=0,
            stdout=r'Commands:'
                   '.*\n  list'
                   '.*\n  create'
                   '.*\n  delete'
                   '.*\n  interop',
            test='regex'
        ),
        None, True
    ),
    (
        "Verify lines in output of command 'namespace -h'",
        ['-h'],
        dict(
            rc=0,
            stdout=NAMESPACE_HELP_LINES,
            test='innows'
        ),
        None, True
    ),

    #
    # 'list' command and its options
    #
    (
        "Verify lines in output of command 'namespace list --help'",
        ['list', '--help'],
        dict(
            rc=0,
            stdout=NAMESPACE_LIST_HELP_LINES,
            test='innows'
        ),
        None, True
    ),
    (
        "Verify lines in output of command 'namespace list -h'",
        ['list', '-h'],
        dict(
            rc=0,
            stdout=NAMESPACE_LIST_HELP_LINES,
            test='innows'
        ),
        None, True
    ),
    (
        "Verify that command 'namespace list' shows the expected namespaces",
        ['list'],
        dict(
            rc=0,
            stdout=[
                'root/cimv2',
                'interop',
            ],
            test='innows'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace list' fails when there is no "
        "Interop namespace",
        ['list'],
        dict(
            rc=1,
            stderr=['ModelError.*Interop namespace does not exist'],
            test='regex'
        ),
        TEST_USER_MOCK_FILE, True
    ),

    #
    # 'create' command and its options
    #
    (
        "Verify lines in output of command 'namespace create --help'",
        ['create', '--help'],
        dict(
            rc=0,
            stdout=NAMESPACE_CREATE_HELP_LINES,
            test='innows'
        ),
        None, True
    ),
    (
        "Verify lines in output of command 'namespace create -h'",
        ['create', '-h'],
        dict(
            rc=0,
            stdout=NAMESPACE_CREATE_HELP_LINES,
            test='innows'
        ),
        None, True
    ),
    (
        "Verify that command 'namespace create foo' succeeds",
        ['create', 'foo'],
        dict(
            rc=0,
            stdout=['Created namespace foo'],
            test='innows'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace create foo' creates the namespace "
        "(using interactive mode)",
        dict(stdin=[
            'namespace create foo',
            'namespace list'
        ]),
        dict(
            rc=0,
            stdout=[
                'Created namespace foo',
                'root/cimv2',
                'interop',
                'foo',
            ],
            test='innows'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace create root/cimv2' fails because it "
        "already exists",
        ['create', 'root/cimv2'],
        dict(
            rc=1,
            stderr=['CIMError.*CIM_ERR_ALREADY_EXISTS.*already exists'],
            test='regex'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace create interop' fails when there is no "
        "Interop namespace",
        ['create', 'interop'],
        dict(
            rc=1,
            stderr=['ModelError.*Interop namespace does not exist'],
            test='regex'
        ),
        TEST_USER_MOCK_FILE, True
    ),

    #
    # 'delete' command and its options
    #
    (
        "Verify lines in output of command 'namespace delete --help'",
        ['delete', '--help'],
        dict(
            rc=0,
            stdout=NAMESPACE_DELETE_HELP_LINES,
            test='innows'
        ),
        None, True
    ),
    (
        "Verify lines in output of command 'namespace delete -h'",
        ['delete', '-h'],
        dict(
            rc=0,
            stdout=NAMESPACE_DELETE_HELP_LINES,
            test='innows'
        ),
        None, True
    ),
    (
        "Verify that command 'namespace delete foo' fails because foo does not "
        "exist",
        ['delete', 'foo'],
        dict(
            rc=1,
            stderr=['CIMError.*CIM_ERR_INVALID_NAMESPACE.*Namespace does not '
                    'exist'],
            test='regex'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace delete root/cimv2' fails because it "
        "is not empty",
        ['delete', 'root/cimv2'],
        dict(
            rc=1,
            stderr=['Cannot delete namespace .* because it has .* qualifier '
                    'types and .* top-level classes'],
            test='regex'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace delete foo' succeeds when empty "
        "namespace foo exists (using interactive mode)",
        dict(stdin=[
            'namespace create foo',
            'namespace delete foo',
            'namespace list'
        ]),
        dict(
            rc=0,
            stdout=[
                'Created namespace foo',
                'Deleted namespace foo',
                'root/cimv2',
                'interop',
            ],
            test='innows'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace delete' succeeds for non-empty "
        "namespace with --include-objects",
        dict(stdin=[
            'namespace delete root/cimv2 --include-objects',
            'namespace list'
        ]),
        dict(
            rc=0,
            stdout=[
                # Only a subset of output lines is verified
                'Deleted instance root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                'Deleted class CIM_Foo',
                'Deleted qualifier type Description',
                'Deleted namespace root/cimv2',
                'interop',
            ],
            test='innows'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace delete' succeeds for non-empty "
        "namespace with --include-objects and --dry-run",
        dict(stdin=[
            'namespace delete root/cimv2 --include-objects --dry-run',
            'namespace list',
            'class get CIM_Foo',
            'instance count CIM_Foo',
        ]),
        dict(
            rc=0,
            stdout=[
                # Only a subset of output lines is verified
                'Dry run: Deleted instance root/cimv2:CIM_Foo.InstanceID='
                '"CIM_Foo1"',
                'Dry run: Deleted class CIM_Foo',
                'Dry run: Deleted qualifier type Description',
                'Dry run: Deleted namespace root/cimv2',
                'interop',
                'class CIM_Foo {',
                'root/cimv2 CIM_Foo 5',
            ],
            test='innows'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace delete' fails when deleting the "
        "Interop namespace",
        ['delete', 'interop'],
        dict(
            rc=1,
            stderr=['Cannot delete namespace .* because it is the Interop '
                    'namespace'],
            test='regex'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),

    #
    # 'interop' command and its options
    #
    (
        "Verify lines in output of command 'namespace interop --help'",
        ['interop', '--help'],
        dict(
            rc=0,
            stdout=NAMESPACE_INTEROP_HELP_LINES,
            test='innows'
        ),
        None, True
    ),
    (
        "Verify lines in output of command 'namespace interop -h'",
        ['interop', '-h'],
        dict(
            rc=0,
            stdout=NAMESPACE_INTEROP_HELP_LINES,
            test='innows'
        ),
        None, True
    ),
    (
        "Verify that command 'namespace interop' shows the expected namespace",
        ['interop'],
        dict(
            rc=0,
            stdout=[
                'interop',
            ],
            test='innows'
        ),
        TEST_INTEROP_MOCK_FILE, True
    ),
    (
        "Verify that command 'namespace interop' fails when there is no "
        "Interop namespace",
        ['interop'],
        dict(
            rc=1,
            stderr=['ModelError.*Interop namespace does not exist'],
            test='regex'
        ),
        TEST_USER_MOCK_FILE, True
    ),
]


class TestSubcmdClass(CLITestsBase):
    # pylint: disable=too-few-public-methods
    """
    Test all of the 'namespace' command variations.
    """

    command_group = 'namespace'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_namespace(self, desc, inputs, exp_response, mock, condition):
        """
        Run the test for a single testcase.
        """
        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition)
