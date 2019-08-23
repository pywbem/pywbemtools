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
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE

TEST_DIR = os.path.dirname(__file__)


# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
INVOKE_METHOD_MOCK_FILE = 'simple_mock_invokemethod.py'
MOCK_SERVER_MODEL = os.path.join('utils', 'wbemserver_mock.py')

#
# The following list define the help for each command in terms of particular
# parts of lines that are to be tested.
# For each test, try to include:
# 1. The usage line and in particular the argument component
# 2. The first line of the command comment (i.e. the summary sentence)
# 3. The last line CMD_OPTION_HELP_HELP_LINE
# 4. Each option including at least the long and short names
SERVER_HELP_LINE = [
    'Usage: pywbemcli server [COMMAND-OPTIONS]',
    'Command group for WBEM servers.',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_BRAND_HELP_LINE = [
    'Usage: pywbemcli server brand [COMMAND-OPTIONS]',
    'Display the brand of the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_CONNECTION_HELP_LINE = [
    'Usage: pywbemcli server connection [COMMAND-OPTIONS]',
    'Display connection info used by this server.',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_GETCENTRALINSTS_HELP_LINE = [
    'Usage: pywbemcli server get-centralinsts [COMMAND-OPTIONS]',
    'Get central instances of mgmt profiles on the server.',
    '-o, --organization <org name>   Filter by the defined organization',
    '-p, --profile <profile name>    Filter by the profile name',
    '-c, --central-class <classname>',
    '-s, --scoping-class <classname>',
    '-S, --scoping-path <pathname>   Optional. Required only if profiles',
    '-r, --reference-direction [snia|dmtf]',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_INFO_HELP_LINE = [
    'Usage: pywbemcli server info [COMMAND-OPTIONS]',
    'Display information about the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_INTEROP_HELP_LINE = [
    'Usage: pywbemcli server interop [COMMAND-OPTIONS]',
    'Display the Interop namespace of the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_NAMESPACES_HELP_LINE = [
    'Usage: pywbemcli server namespaces [COMMAND-OPTIONS]',
    'Display the namespaces of the server.',
    CMD_OPTION_HELP_HELP_LINE,
]

SERVER_PROFILES_HELP_LINE = [
    'Usage: pywbemcli server profiles [COMMAND-OPTIONS]',
    'Display management profiles advertized by the server.',
    CMD_OPTION_HELP_HELP_LINE,
]


OK = True  # mark tests OK when they execute correctly
RUN = True  # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet

# pylint: enable=line-too-long
TEST_CASES = [
    # desc - Description of test
    # inputs - String, or list of args or dict of 'env', 'args', 'globals',
    #          and 'stdin'. See See CLITestsBase.subcmd_test()  for
    #          detailed documentation
    # exp_response - Dictionary of expected responses,
    # mock - None or name of files (mof or .py),
    # condition - If True, the test is executed,  Otherwise it is skipped.

    ['Verify server subcommand help response',
     '--help',
     {'stdout': SERVER_HELP_LINE,
      'test': 'innows'},
     None, OK],

    ['Verify server subcommand brand  --help response',
     ['brand', '--help'],
     {'stdout': SERVER_BRAND_HELP_LINE,
      'test': 'innows'},
     None, OK],

    ['Verify server subcommand connection --help response',
     ['connection', '--help'],
     {'stdout': SERVER_CONNECTION_HELP_LINE,
      'test': 'innows'},
     None, OK],

    ['Verify server subcommand get-centralinsts  --help response',
     ['get-centralinsts', '--help'],
     {'stdout': SERVER_GETCENTRALINSTS_HELP_LINE,
      'test': 'innows'},
     None, OK],

    ['Verify server subcommand info --help response',
     ['info', '--help'],
     {'stdout': SERVER_INFO_HELP_LINE,
      'test': 'innows'},
     None, OK],

    ['Verify server subcommand interop --help response',
     ['interop', '--help'],
     {'stdout': SERVER_INTEROP_HELP_LINE,
      'test': 'innows'},
     None, OK],

    ['Verify class subcommand namespaces --help response',
     ['namespaces', '--help'],
     {'stdout': SERVER_NAMESPACES_HELP_LINE,
      'test': 'innows'},
     None, OK],

    ['Verify class subcommand profiles  --help response',
     ['profiles', '--help'],
     {'stdout': SERVER_PROFILES_HELP_LINE,
      'test': 'innows'},
     None, OK],

    #
    #   Verify the individual subcommands returning data
    #
    ['Verify server subcommand interop',
     {'args': ['interop'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Server Interop Namespace:',
                 'Namespace Name',
                 '----------------',
                 'interop'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server subcommand namespaces',
     {'args': ['namespaces'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Server Namespaces:',
                 'Namespace Name',
                 '----------------',
                 'interop'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server subcommand namespaces with sort option',
     {'args': ['namespaces', '-s'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Server Namespaces:',
                 'Namespace Name',
                 '----------------',
                 'interop'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server subcommand brand',
     {'args': ['brand'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Server brand:',
                 'WBEM server brand',
                 '-------------------',
                 'OpenPegasus'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server subcommand profiles',
     {'args': ['profiles'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Component             1.4.0',
                 'DMTF            Indications           1.1.0',
                 'DMTF            Profile Registration  1.0.0',
                 'SNIA            Array                 1.4.0',
                 'SNIA            SMI-S                 1.2.0',
                 'SNIA            Server                1.2.0',
                 'SNIA            Server                1.1.0',
                 'SNIA            Software              1.4.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server subcommand profiles, filtered by org',
     {'args': ['profiles', '-o', 'DMTF'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Component             1.4.0',
                 'DMTF            Indications           1.1.0',
                 'DMTF            Profile Registration  1.0.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server subcommand profiles, filtered by org, long',
     {'args': ['profiles', '--organization', 'DMTF'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Component             1.4.0',
                 'DMTF            Indications           1.1.0',
                 'DMTF            Profile Registration  1.0.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server subcommand profiles, filtered by name',
     {'args': ['profiles', '-p', 'Profile Registration'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Profile Registration  1.0.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server subcommand profiles, filtered by org, long',
     {'args': ['profiles', '--profile', 'Profile Registration'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised management profiles:',
                 'Organization    Registered Name       Version',
                 '--------------  --------------------  ---------',
                 'DMTF            Profile Registration  1.0.0'],
      'rc': 0,
      'test': 'lines'},
     MOCK_SERVER_MODEL, OK],

    ['Verify server subcommand connection with mock server',
     ['connection'],
     {'stdout': ["", 'url: http://FakedUrl', 'creds: None', '.x509: None',
                 'default_namespace: root/cimv2', 'timeout: None sec.',
                 'ca_certs: None'],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify server subcommand get-centralinsts, ',
     {'args': ['get-centralinsts', '-o', 'SNIA',
               '-p', 'Server'],
      'global': ['-d', 'interop', '-o', 'simple']},
     {'stdout': ['Advertised Central Instances:',
                 r'Profile +Central Instances',
                 'SNIA:Server:1.1.0',
                 'SNIA:Server:1.2.0',
                 'interop:XXX_StorageComputerSystem'],
      'rc': 0,
      'test': 'regex'},
     MOCK_SERVER_MODEL, OK],


    ['Verify server subcommand info with mock server',
     {'args': ['info'],
      'global': ['-d', 'interop', '-o', 'simple']},
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
    Execute the testcases for server subcommand variations.
    """
    subcmd = 'server'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_class(self, desc, inputs, exp_response, mock, condition):
        """
        Common test method for those subcommands and options in the
        class subcmd that can be tested.  This includes:

          * Subcommands like help that do not require access to a server

          * Subcommands that can be tested with a single execution of a
            pywbemcli command.
        """
        self.subcmd_test(desc, self.subcmd, inputs, exp_response,
                         mock, condition)
