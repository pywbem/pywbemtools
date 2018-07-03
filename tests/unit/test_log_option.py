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

OK = False
RUN = True
FAIL = False

MOCK_TEST_CASES = [
    # desc - Description of test
    # args - List of arguments or string of arguments. For this test,
    #        list includes subcommand unless there is only one argument
    # exp_response - Dictionary of expected responses,
    # mock - None or name of files (mof or .py),
    # condition - If True, the test is executed,  Otherwise it is skipped.

    ['verify pywbemcl --help command. Just test for log help',
     {'subcmd': None,
      'args': ['--help']},
     {'stdout': ['-l, --log COMP=DEST:DETAIL,...',
                 '(COMP: [api|http|all], Default:',
                 'DETAIL:[all|paths|summary], Default: all)'],
      'test': 'in'},
     None, OK],

    ['verify pywbemcl -o all=stderr class get blah. class get that fails',
     {'global': ['-l', 'all=stderr'],
      'subcmd': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['-pywbem.api', 'PYWBEMCLIConnection(url',
                 "GetClass(ClassName=\'blah\'",
                 '-Exception:'],
      'test': 'in',
      'rc': 1},
     None, OK],

    ['verify log of class get blah. class get that fails',
     {'global': ['-l', 'all=stderr'],
      'subcmd': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['-pywbem.api', 'PYWBEMCLIConnection(url',
                 "GetClass(ClassName=\'blah\'",
                 '-Exception:'],
      'test': 'in',
      'rc': 1},
     None, OK],

    ['Verify log of class subcommand get localonly. Tests whole response',
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

    ['Verify Log of class subcommand get localonly. Tests whole response.'
     'Cannot test stderr and stdout in same test.',
     {'global': ['-l', 'all=stderr:summary'],
      'subcmd': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--localonly']},
     {'stderr': ['-pywbem.api.',
                 'PYWBEMCLIFakedConnection(url',
                 '-Request:',
                 "GetClass(ClassName='CIM_Foo_sub2', IncludeClassOrigin=False",
                 '-Return:',
                 'GetClass(CIMClass CIM_Foo_sub2'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify log of class subcommand get localonly. Tests whole response.'
     'Cannot test stderr and stdout in same test.',
     {'global': ['-l', 'api=stderr:summary'],
      'subcmd': 'class',
      'args': ['get', 'CIM_Foo_sub2', '--localonly']},
     {'stderr': ['-pywbem.api.',
                 'PYWBEMCLIFakedConnection(url',
                 '-Request:',
                 "GetClass(ClassName='CIM_Foo_sub2', IncludeClassOrigin=False",
                 '-Return:',
                 'GetClass(CIMClass CIM_Foo_sub2'],
      'test': 'in'},
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
     {'stderr': ["Error: Logger configuration error. inputhttpx=stderr."],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, RUN],

]


class TestLogOption(CLITestsBase):
    """
    Test use of the global log option. This was be tested in the
    test_global_opts.py file because it requires execution of a subcommand
    to actually use the log and create logs.
    """

    @pytest.mark.parametrize(
        "desc, args, exp_response, mock, condition",
        MOCK_TEST_CASES)
    def test_class(self, desc, args, exp_response, mock, condition):
        """
        Common test method for those subcommands and options in the
        class subcmd that can be tested.  This includes:

          * Subcommands like help that do not require access to a server

          * Subcommands that can be tested with a single execution of a
            pywbemcli command.
        """
        env = None
        subcmd = ""  # Do not supply a subcommand with these requests
        if args['subcmd']:
            subcmd = args['subcmd']

        self.mock_subcmd_test(desc, subcmd, args, env, exp_response,
                              mock, condition)
