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
Tests the server command group
"""
import os
import pytest
from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE

TEST_DIR = os.path.dirname(__file__)


# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
INVOKE_METHOD_MOCK_FILE = 'simple_mock_invokemethod.py'
MOCK_SERVER_MODEL = os.path.join('testmock', 'wbemserver_mock.py')

#
# The following list define the help for each command in terms of particular
# parts of lines that are to be tested.
# For each test, try to include:
# 1. The usage line and in particular the argument component
# 2. The first line of the command comment (i.e. the summary sentence)
# 3. The last line CMD_OPTION_HELP_HELP_LINE
# 4. Each option including at least the long and short names
SERVER_HELP_LINES = [
    'Usage: pywbemcli server [COMMAND-OPTIONS]',
    'Command group for WBEM servers.',
    CMD_OPTION_HELP_HELP_LINE,
    'brand             Get the brand of the server.',
    'centralinsts      List central instances of mgmt profiles on the server.',
    'info              Get information about the server.',
    'interop           Get the Interop namespace of the server.',
    'namespaces        List the namespaces of the server.',
    'profiles          List management profiles advertized by the server.',
]

SERVER_BRAND_HELP_LINES = [
    'Usage: pywbemcli server brand [COMMAND-OPTIONS]',
    'Get the brand of the server.',
    CMD_OPTION_HELP_HELP_LINE,
]


SERVER_CENTRAL_INSTS_HELP_LINES = [
    'Usage: pywbemcli server centralinsts [COMMAND-OPTIONS]',
    'List central instances of mgmt profiles on the server.',
    '-o, --organization ORG-NAME Filter by the defined organization',
    '-p, --profile PROFILE-NAME Filter by the profile name',
    '--cc, --central-class CLASSNAME Optional. Required only if profiles',
    '--sc, --scoping-class CLASSNAME Optional. Required only if profiles',
    '--sp, --scoping-path CLASSLIST Optional. Required only if profiles',
    '--rd, --reference-direction [snia|dmtf] Navigation direction',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_INFO_HELP_LINES = [
    'Usage: pywbemcli server info [COMMAND-OPTIONS]',
    'Get information about the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_INTEROP_HELP_LINES = [
    'Usage: pywbemcli server interop [COMMAND-OPTIONS]',
    'Get the Interop namespace of the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_NAMESPACES_HELP_LINES = [
    'Usage: pywbemcli server namespaces [COMMAND-OPTIONS]',
    'List the namespaces of the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_PROFILES_HELP_LINES = [
    'Usage: pywbemcli server profiles [COMMAND-OPTIONS]',
    'List management profiles advertized by the server.',
    CMD_OPTION_HELP_HELP_LINE,
]


OK = True  # mark tests OK when they execute correctly
RUN = True  # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet

# pylint: enable=line-too-long
TEST_CASES = [
    # desc - Description of test
    # inputs - String, or list of args or dict of 'env', 'args', 'general',
    #          and 'stdin'. See See CLITestsBase.command_test()  for
    #          detailed documentation
    # exp_response - Dictionary of expected responses,
    # mock - None or name of files (mof or .py),
    # condition - If True the test is executed, if 'pdb' the test breaks in
    #             the debugger, otherwise the test is skipped.

    ['Verify server command --help response',
     '--help',
     {'stdout': SERVER_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command -h response',
     '-h',
     {'stdout': SERVER_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command brand  --help response',
     ['brand', '--help'],
     {'stdout': SERVER_BRAND_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command brand  -h response',
     ['brand', '-h'],
     {'stdout': SERVER_BRAND_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command get-centralinsts  --help response',
     ['centralinsts', '--help'],
     {'stdout': SERVER_CENTRAL_INSTS_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command centralinsts  -h response',
     ['centralinsts', '-h'],
     {'stdout': SERVER_CENTRAL_INSTS_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command info --help response',
     ['info', '--help'],
     {'stdout': SERVER_INFO_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command info -h response',
     ['info', '-h'],
     {'stdout': SERVER_INFO_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command interop --help response',
     ['interop', '--help'],
     {'stdout': SERVER_INTEROP_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command interop -h response',
     ['interop', '-h'],
     {'stdout': SERVER_INTEROP_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command namespaces --help response',
     ['namespaces', '--help'],
     {'stdout': SERVER_NAMESPACES_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command namespaces -h response',
     ['namespaces', '-h'],
     {'stdout': SERVER_NAMESPACES_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command profiles --help response',
     ['profiles', '--help'],
     {'stdout': SERVER_PROFILES_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify server command profiles -h response',
     ['profiles', '-h'],
     {'stdout': SERVER_PROFILES_HELP_LINES,
      'test': 'innows'},
     None, OK],

    #
    #   Verify the individual commands returning data
    #
    ['Verify server command interop',
     {'args': ['interop'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Server Interop Namespace:',
                 'Namespace Name',
                 '----------------',
                 'interop'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server command namespaces',
     {'args': ['namespaces'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Server Namespaces:',
                 'Namespace Name',
                 '----------------',
                 'interop'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    # TODO: Remove this test once removal of --sort option is agreed.
    ['Verify server command namespaces with sort option',
     {'args': ['namespaces', '-s'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Server Namespaces:',
                 'Namespace Name',
                 '----------------',
                 'interop'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, FAIL],

    ['Verify server command brand',
     {'args': ['brand'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Server brand:',
                 'WBEM server brand',
                 '-------------------',
                 'OpenPegasus'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server command profiles',
     {'args': ['profiles'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Component             1.4.0',
                 'DMTF            Indications           1.1.0',
                 'DMTF            Profile Registration  1.0.0',
                 'SNIA            Array                 1.4.0',
                 'SNIA            SMI-S                 1.2.0',
                 'SNIA            Server                1.1.0',
                 'SNIA            Server                1.2.0',
                 'SNIA            Software              1.4.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server command profiles, filtered by org',
     {'args': ['profiles', '-o', 'DMTF'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Component             1.4.0',
                 'DMTF            Indications           1.1.0',
                 'DMTF            Profile Registration  1.0.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server command profiles, filtered by org, long',
     {'args': ['profiles', '--organization', 'DMTF'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Component             1.4.0',
                 'DMTF            Indications           1.1.0',
                 'DMTF            Profile Registration  1.0.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server command profiles, filtered by name',
     {'args': ['profiles', '-p', 'Profile Registration'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Profile Registration  1.0.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server command profiles, filtered by org, long',
     {'args': ['profiles', '--profile', 'Profile Registration'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Profile Registration  1.0.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server command centralinsts based on wbem server mock.',
     {'args': ['centralinsts', '-o', 'SNIA',
               '-p', 'Server'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised Central Instances:',
                 'Profile',
                 'Central Instance paths',
                 'SNIA:Server:1.1.0',
                 'SNIA:Server:1.2.0',
                 'interop:MCK_StorageComputerSystem'],
      'rc': 0,
      'test': 'innows'},
     MOCK_SERVER_MODEL, OK],


    ['Verify server command info with mock server',
     {'args': ['info'],
      'general': ['-d', 'interop', '-o', 'simple']},
     {'stdout':
      ['Server General Information',
       'Brand        Version    Interop Namespace    Namespaces',
       '-----------  ---------  -------------------  ------------',
       'OpenPegasus  2.15.0     interop              interop'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    #
    # Error tests
    #
    # TODO add error tests.
    # At this point we do not have any error tests
]


class TestSubcmdServer(CLITestsBase):
    """
    Execute the testcases for server command variations.
    """
    command_group = 'server'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_class(self, desc, inputs, exp_response, mock, condition):
        """
        Common test method for those commands and options in the
        class subcmd that can be tested.  This includes:

          * Subcommands like help that do not require access to a server

          * Subcommands that can be tested with a single execution of a
            pywbemcli command.
        """
        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition)
