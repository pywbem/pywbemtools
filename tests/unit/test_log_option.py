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
Tests the class subcommand
"""
import os
import pytest
from .cli_test_extensions import CLITestsBase

TEST_DIR = os.path.dirname(__file__)

SIMPLE_MOCK_FILE = 'simple_mock_model.mof'

OK = True
RUN = True
FAIL = False

TEST_CASES = [
    # desc - Description of test
    # inputs - String, or list of args or dict of 'env', 'args', 'globals',
    #          and 'stdin'. See See CLITestsBase.subcmd_test()  for
    #          detailed documentation. This test processor includes an
    #          additional key, `subcmd`
    # exp_response - Dictionary of expected responses,
    # mock - None or name of files (mof or .py),
    # condition - If True, the test is executed,  Otherwise it is skipped.

    ['Verify log of class get blah. class get that fails',
     {'global': ['-l', 'all=stderr'],
      'subcmd': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['-pywbem.api',
                 'PYWBEMCLIFakedConnection',
                 r'GetClass\(ClassName=', r'blah',
                 '-Exception:'],
      'test': 'regex',
      'rc': 1},
     SIMPLE_MOCK_FILE, OK],

    ['Verify log of class subcommand get localonly. Test stdpit',
     {'global': ['-l', 'all=stderr:summary'],
      'subcmd': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--localonly']},
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '};', '', ],
      'stderr': ["blahblah"],
      'test': 'patterns'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify Log of class subcommand get localonly. test stderr'
     'Cannot test stderr and stdout in same test.',
     {'global': ['-l', 'all=stderr:summary'],
      'subcmd': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--localonly']},
     {'stderr': [r'-pywbem.api.',
                 r'PYWBEMCLIFakedConnection',
                 r'-Request:',
                 r'-Return:',
                 r'GetClass\(CIMClass ', r'CIM_Foo_sub2'],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify log of class subcommand get localonly. Test stderr'
     'Cannot test stderr and stdout in same test.',
     {'global': ['-l', 'api=stderr:summary'],
      'subcmd': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--localonly']},
     {'stderr': [r'-pywbem.api.',
                 r'PYWBEMCLIFakedConnection',
                 r'-Request:',
                 r'-Return:',
                 r'GetClass\(CIMClass ', r'CIM_Foo_sub2'],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify log http class subcommand get localonly. Should be no log because '
     'mock does not use http'
     'Cannot test stderr and stdout in same test.',
     {'global': ['-l', 'http=stderr:summary'],
      'subcmd': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--localonly']},
     {'stderr': [],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify log with error in definition. Cannot test stderr and stdout in '
     'same test.',
     {'global': ['-l', 'httpx=stderr'],
      'subcmd': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--localonly']},
     {'stderr': ["Error: Logger configuration error. input: "],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify log with error in definition. invalid type',
     {'global': ['-l', 'allx=stderr'],
      'subcmd': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--localonly']},
     {'stderr': ["Error: Logger configuration error. input: allx=stderr. "
                 "Exception: Invalid simple logger name:"],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify invalid log parameter fails (no value) '
     'same test.',
     {'global': ['-l'],
      'subcmd': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--localonly']},
     {'stderr': ["Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]"],
      'rc': 2,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

]


class TestLogOption(CLITestsBase):
    """
    Test use of the global log option. This was be tested in the
    test_global_opts.py file because it requires execution of a subcommand
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
        subcmd = inputs['subcmd'] if inputs['subcmd'] else ''

        self.subcmd_test(desc, subcmd, inputs, exp_response,
                         mock, condition)
