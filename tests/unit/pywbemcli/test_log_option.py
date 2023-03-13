# Copyright 2018 IBM Corp. All Rights Reserved.
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
Tests the general log option. This tests the --log general option value
for valid and invalid strings.
"""

from __future__ import absolute_import, print_function

import os
import pytest

from .cli_test_extensions import CLITestsBase

# pylint: disable=use-dict-literal

TEST_DIR = os.path.dirname(__file__)

SIMPLE_MOCK_MODEL_FILE = 'simple_mock_model.mof'
SIMPLE_MOCK_FILE_PATH = os.path.join(TEST_DIR, SIMPLE_MOCK_MODEL_FILE)

OK = True
RUN = True
FAIL = False

TEST_CASES = [

    # List of testcases.
    # Each testcase is a list with the following items:
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

    ['Verify log of class get blah. class get that fails',
     {'general': ['-l', 'all=stderr'],
      'cmdgrp': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['-pywbem.api',
                 'FakedWBEMConnection',
                 r'GetClass\(ClassName=', r'blah',
                 '-Exception:'],
      'test': 'regex',
      'rc': 1},
     SIMPLE_MOCK_MODEL_FILE, OK],

    ['Verify log of class  get command get local-only. Test stdoit',
     {'general': ['-l', 'all=stderr:summary'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--local-only']},
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '};', '', ],
      'stderr': ["blahblah"],
      'test': 'patterns'},
     SIMPLE_MOCK_MODEL_FILE, OK],

    ['Verify Log of class get command local-only. test stderr'
     'Cannot test stderr and stdout in same test.',
     {'general': ['-l', 'all=stderr:summary'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--local-only']},
     {'stderr': [r'-pywbem.api.',
                 r'FakedWBEMConnection',
                 r'-Request:',
                 r'-Return:',
                 r'GetClass\(CIMClass ', r'CIM_Foo_sub2'],
      'test': 'regex'},
     SIMPLE_MOCK_MODEL_FILE, OK],

    ['Verify log of class get command local-only. Test stderr'
     'Cannot test stderr and stdout in same test.',
     {'general': ['-l', 'api=stderr:summary'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--local-only']},
     {'stderr': [r'-pywbem.api.',
                 r'FakedWBEMConnection',
                 r'-Request:',
                 r'-Return:',
                 r'GetClass\(CIMClass ', r'CIM_Foo_sub2'],
      'test': 'regex'},
     SIMPLE_MOCK_MODEL_FILE, OK],

    ['Verify log http class get command local-only. Should be no log '
     'because mock does not use http'
     'Cannot test stderr and stdout in same test.',
     {'general': ['-l', 'http=stderr:summary'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--local-only']},
     {'stderr': [],
      'test': 'in'},
     SIMPLE_MOCK_MODEL_FILE, OK],

    ['Verify log with error in definition. Cannot test stderr and stdout in '
     'same test.',
     {'general': ['-l', 'httpx=stderr'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--local-only']},
     {'stderr': ["Error: Logger configuration error. input: "],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_MODEL_FILE, OK],

    ['Verify log with error in definition. invalid type',
     {'general': ['-l', 'allx=stderr'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--local-only']},
     {'stderr': ["Error: Logger configuration error. input: allx=stderr. "
                 "Exception: Invalid simple logger name:"],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_MODEL_FILE, OK],

    ['Verify invalid log parameter fails (no value) same test.',
     {'general': ['-l'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--local-only']},
     {'stderr': ["Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]"],
      'rc': 2,
      'test': 'in'},
     SIMPLE_MOCK_MODEL_FILE, OK],

    ['Verify log all=off. Cannot really test effect.',
     {'general': ['-l', 'all=off'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--local-only']},
     {'stderr': [""],
      'test': 'innows'},
     SIMPLE_MOCK_MODEL_FILE, OK],

    ['Verify  --log general option and in interactive cmd that change log. '
     'Turns on log in one command and off in the next command',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '--log', 'all=off'],
      'stdin': ['--log all=stderr:summary instance enumerate CIM_Foo',
                'instance enumerate CIM_Foo'],
      'cmdgrp': None},
     {'stderr': ["OpenEnumerateInstances(ClassName", "CIM_Foo",
                 'OpenEnumerateInstances(pull_inst_result_tuple'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify  --log general option in interactive cmd that change log. '
     'Changes log for the interactive command',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '-v', '--log',
                  'api=stderr:summary'],
      'stdin': ['--log all=stderr:summary instance enumerate CIM_Foo -s',
                'instance enumerate CIM_Foo --summary'],
      'cmdgrp': None},
     {'stdout': ["Log configured to all=stderr:summary",
                 "Log configured to api=stderr:summary"],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify  with --log general option in interactive cmds that change log. '
     'Turns on log in one command and off in the next command',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '--log', 'all=off'],
      'stdin': ['--log all=stderr:summary instance enumerate CIM_Foo -s',
                'instance enumerate CIM_Foo -s'],
      'cmdgrp': None},
     {'stderr': ["OpenEnumerateInstances(ClassName=", "CIM_Foo",
                 'OpenEnumerateInstances(pull_inst_result_tuple'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify  no --log general option and in interactive cmds that change log. '
     'Turns on log in one command and off in the next command',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '-v',
                  '--log', 'all=off'],
      'stdin': ['--log all=stderr:summary instance enumerate CIM_Foo -s',
                'instance enumerate CIM_Foo -s'],
      'cmdgrp': None},
     # Use verbose mode to display log change msg
     {'stdout': ["Log configured to all=stderr:summary",
                 "Log configured to all=off"],
      'rc': 0,
      'test': 'innows'},
     None, OK],
]


class TestLogOption(CLITestsBase):
    """
    Test use of the general log option. This was be tested in the
    test_general_opts.py file because it requires execution of a command
    to actually use the log and create logs.
    """

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition", TEST_CASES)
    def test_log_option(self, desc, inputs, exp_response, mock, condition):
        """
        Common test method for those subcommands and options in the
        class subcmd that can be tested.  This includes:

          * Subcommands like help that do not require access to a server

          * Subcommands that can be tested with a single execution of a
            pywbemcli command.
        """
        cmd_grp = inputs['cmdgrp'] if inputs['cmdgrp'] else ''

        self.command_test(desc, cmd_grp, inputs, exp_response,
                          mock, condition)
