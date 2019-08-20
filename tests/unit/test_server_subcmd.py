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


# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
INVOKE_METHOD_MOCK_FILE = 'simple_mock_invokemethod.py'
MOCK_SERVER_MODEL = os.path.join('utils', 'wbemserver_mock.py')

SERVER_HELP = """
Usage: pywbemcli server [COMMAND-OPTIONS] COMMAND [ARGS]...

  Command Group for WBEM server operations.

  The server command-group defines commands to inspect and manage core
  components of the server including namespaces, the interop namespace,
  profiles, and access to profile central instances.

  In addition to the command-specific options shown in this help text, the
  general options (see 'pywbemcli --help') can also be specified before the
  command. These are NOT retained after the command is executed.

Options:
  -h, --help  Show this message and exit.

Commands:
  brand             Display information on the WBEM server.
  connection        Display connection info used by this server.
  get-centralinsts  Display central instances in the WBEM server.
  info              Display general information on the server.
  interop           Display the server interop namespace name.
  namespaces        Display the namespaces in the WBEM server.
  profiles          Display registered profiles from the WBEM server.
"""

SVR_BRAND_HELP = """
Usage: pywbemcli server brand [COMMAND-OPTIONS]

  Display information on the WBEM server.

  Display brand information on the current server if it is available. This
  is typically the definition of the server implementor.

Options:
  -h, --help  Show this message and exit.
"""

SVR_GETCENTRALINSTS_HELP = """
Usage: pywbemcli server get-centralinsts [COMMAND-OPTIONS]

  Display central instances in the WBEM server.

  Displays central instances for management profiles registered in the
  server. Displays management profiles that adher to to the central class
  methodology with none of the extra parameters (ex. scoping_class)

  However, profiles that only use the scoping methodology require extra
  information that is dependent on the profile itself. These profiles will
  only be accessed when the correct values of central_class, scoping_class,
  and scoping path for the particular profile is provided.

  This display may be filtered by the optional organization and profile name
  options that define the organization for each profile (ex. SNIA) and the
  name of the profile. This will display only the profiles that are
  registered for the defined organization and/or name.

  Profiles are display as a table showing the organization, name, and
  version for each profile.

Options:
  -o, --organization <org name>   Filter by the defined organization. (ex. -o
                                  DMTF
  -p, --profile <profile name>    Filter by the profile name. (ex. -p Array
  -c, --central-class <classname>
                                  Optional. Required only if profiles supports
                                  only scopig methodology
  -s, --scoping-class <classname>
                                  Optional. Required only if profiles supports
                                  only scopig methodology
  -S, --scoping-path <pathname>   Optional. Required only if profiles supports
                                  only scopig methodology. Multiples allowed
  -r, --reference-direction [snia|dmtf]
                                  Navigation direction for association.
                                  [default: dmtf]
  -h, --help                      Show this message and exit.
  """

SVR_CONNECT_HELP = """
Usage: pywbemcli  server connection [COMMAND-OPTIONS]

  Display connection info used by this server.

  Displays the connection information for the WBEM connection attached to
  this server.  This includes uri, default namespace, etc.

  This is equivalent to the connection show subcommand.

Options:
  -h, --help  Show this message and exit.
"""

SVR_INFO_HELP = """
Usage: pywbemcli server info [COMMAND-OPTIONS]

  Display general information on the server.

  Displays general information on the current server includeing brand,
  namespaces, etc.

Options:
  -h, --help  Show this message and exit.
"""

SVR_INTEROP_HELP = """
Usage: pywbemcli server interop [COMMAND-OPTIONS]

  Display the server interop namespace name.

  Displays the name of the interop namespace defined for the WBEM server.

Options:
  -h, --help  Show this message and exit.
"""

SVR_NAMESPACES_HELP = """
Usage: pywbemcli server namespaces [COMMAND-OPTIONS]

  Display the namespaces in the WBEM server.

Options:
  -s, --sort  Sort into alphabetical order by classname.
  -h, --help  Show this message and exit.
"""

SVR_PROFILES_HELP = """
Usage: pywbemcli server profiles [COMMAND-OPTIONS]

  Display registered profiles from the WBEM server.

  Displays the WBEM management profiles that have been registered for this
  server.  Within the DMTF and SNIA these are the definition of management
  functionality supported by the WBEM server.

  This display may be filtered by the optional organization and profile
  options that define the organization for each profile (ex. SNIA) and the
  name of the profile. This will display only the profiles that are
  registered for the defined organization and/or profile name.

  Profiles are displayed as a table showing the organization, name, and
  version for each profile.

Options:
  -o, --organization <org name>  Filter by the defined organization. (ex. -o
                                 DMTF
  -p, --profile <profile name>   Filter by the profile name. (ex. -p Array
  -h, --help                     Show this message and exit.
"""

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
     {'stdout': SERVER_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify server subcommand brand  --help response',
     ['brand', '--help'],
     {'stdout': SVR_BRAND_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify class subcommand profiles  --help response',
     ['get-centralinsts', '--help'],
     {'stdout': SVR_GETCENTRALINSTS_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify server subcommand connection --help response',
     ['connection', '--help'],
     {'stdout': SVR_CONNECT_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify server subcommand info --help response',
     ['info', '--help'],
     {'stdout': SVR_INFO_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify server subcommand interop --help response',
     ['interop', '--help'],
     {'stdout': SVR_INTEROP_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify class subcommand namespaces --help response',
     ['namespaces', '--help'],
     {'stdout': SVR_NAMESPACES_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify class subcommand profiles  --help response',
     ['profiles', '--help'],
     {'stdout': SVR_PROFILES_HELP,
      'test': 'linesnows'},
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
