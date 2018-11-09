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
Test the connection command group and it subcommands
"""

import os
import pytest
from .cli_test_extensions import CLITestsBase

from pywbemcli._connection_repository import CONNECTIONS_FILE

TEST_DIR = os.path.dirname(__file__)


# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
INVOKE_METHOD_MOCK_FILE = 'simple_mock_invokemethod.py'

CONN_HELP = """Usage: pywbemcli connection [COMMAND-OPTIONS] COMMAND [ARGS]...

  Command group to manage WBEM connections.

  These command allow viewing and setting persistent connection definitions.
  The connections are normally defined in the file pywbemcliconnections.json
  in the current directory.

  In addition to the command-specific options shown in this help text, the
  general options (see 'pywbemcli --help') can also be specified before the
  command. These are NOT retained after the command is executed.

Options:
  -h, --help  Show this message and exit.

Commands:
  delete  Delete connection information.
  export  Export the current connection information.
  list    List the entries in the connection file.
  new     Create a new named WBEM connection.
  save    Save current connection into repository.
  select  Select a connection from defined connections.
  show    Show current or NAME connection information.
  test    Execute a predefined wbem request.
"""

CONN_SHOW_HELP = """Usage: pywbemcli connection show [COMMAND-OPTIONS] NAME

  Show current or NAME connection information.

  This subcommand displays  all the variables that make up the current WBEM
  connection if the optional NAME argument is NOT provided

  If the optional NAME argument is provided, the information on the
  connection with that name is displayed if that name is in the persistent
  repository.

Options:
  -h, --help  Show this message and exit.
"""

CONN_DEL_HELP = """Usage: pywbemcli connection delete [COMMAND-OPTIONS] NAME

  Delete connection information.

  Delete connection information from the persistent store for the connection
  defined by NAME.

  If NAME not supplied, a select list presents the list of connection
  definitions for selection.

  Example:   connection delete blah

Options:
  -h, --help  Show this message and exit.
"""

CONN_SAVE_HELP = """Usage: pywbemcli connection save [COMMAND-OPTIONS] NAME

  Save current connection into repository.

  Saves the current wbem connection information into the repository of
  connections. If the name does not already exist in the connection
  information, the provided name is used.

Options:
  -h, --help  Show this message and exit.
"""

CONN_NEW_HELP = """Usage: pywbemcli connection new [COMMAND-OPTIONS] NAME uri

  Create a new named WBEM connection.

  This subcommand creates and saves a new named connection from the required
  input arguments (NAME and URI) and the options defined below.

  The new connection that can be referenced by the name argument in the
  future.  This connection object is capable of managing all of the
  properties defined for WBEMConnections.

  The NAME and URI arguments MUST exist. They define the server uri and the
  unique name under which this server connection information will be stored.

  It does NOT automatically set pywbemcli to use that connection. Use
  `connection select` to set a particular stored connection definition as
  the current connection.

  This is the alternative means of defining a new WBEM server to be
  accessed. A server can also be defined by supplying the parameters on the
  command line and using the `connection set` command to put it into the
  connection repository.

Options:
  -d, --default_namespace TEXT    Default Namespace to use in the target
                                  WBEMServer if no namespace is defined in the
                                  subcommand (Default: root/cimv2).
  -u, --user TEXT                 User name for the WBEM Server connection.
  -p, --password TEXT             Password for the WBEM Server. Will be
                                  requested as part  of initialization if user
                                  name exists and it is not  provided by this
                                  option.
  -t, --timeout INTEGER RANGE     Operation timeout for the WBEM Server in
                                  seconds. Default: 30
  -n, --noverify                  If set, client does not verify server
                                  certificate.
  -c, --certfile TEXT             Server certfile. Ignored if noverify flag
                                  set.
  -k, --keyfile TEXT              Client private key file.
  -l, --log COMP=DEST:DETAIL,...  Enable logging of CIM Operations and set a
                                  component to destination, and detail level
                                  (COMP: [api|http|all], Default: all) DEST:
                                  [file|stderr], Default: file)
                                  DETAIL:[all|paths|summary], Default: all)
  -m, --mock-server FILENAME      If this option is defined, a mock WBEM
                                  server is constructed as the target WBEM
                                  server and the option value defines a MOF or
                                  Python file to be used to populate the mock
                                  repository. This option may be used multiple
                                  times where each use defines a single file
                                  or file_path.See the pywbemcli documentation
                                  for more information.
  --ca_certs TEXT                 File or directory containing certificates
                                  that will be matched against a certificate
                                  received from the WBEM server. Set the --no-
                                  verify-cert option to bypass client
                                  verification of the WBEM server certificate.
                                  Default: Searches for matching certificates
                                  in the following system directories:
                                  /etc/pki/ca-trust/extracted/openssl/ca-
                                  bundle.trust.crt
                                  /etc/ssl/certs
                                  /etc/ssl/certificates
  -h, --help                      Show this message and exit.
"""


OK = False  # mark tests OK when they execute correctly
RUN = True  # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet

# pylint: enable=line-too-long
TEST_CASES = [
    # desc - Description of test
    # inputs - String, or list of args or dict of 'env', 'args', 'globals',
    #          and 'stdin'. See See CLITestsBase.subcmd_test()  for
    #          detailed documentation
    # exp_response - Dictionary of expected responses,
    #                This test adds a new dict entry to exp_response: "file"
    #                that allows the test to determine if the json output file
    #                exists and to remove it.
    # mock - None or name of files (mof or .py),
    # condition - If True, the test is executed,  Otherwise it is skipped.


    ['Verify connection subcommand help response',
     '--help',
     {'stdout': CONN_HELP,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand show  --help response',
     ['show', '--help'],
     {'stdout': CONN_SHOW_HELP,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand delete  --help response',
     ['delete', '--help'],
     {'stdout': CONN_DEL_HELP,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand save  --help response',
     ['save', '--help'],
     {'stdout': CONN_SAVE_HELP,
      'test': 'lines',
      'file': {'before': 'none', 'after': 'none'}},
     None, RUN],

    # TODO: help not done for select, new, export, list, test

    # ['Verify connection subcommand new. test with show and delete  ',
    # # {'stdin': ['connection new test1 http://blah', 'connection show test1',
    #            # 'connection delete test1']},
    # # {'stdout': ["Name: test1", "  WBEMServer uri: http://blah",
    #  # "  Default_namespace: root/cimv2", "  User: None", "  Password: None",
    #  # "  Timeout: None", "  Noverify: False", "  Certfile: None",
    #  # "  Keyfile: None", "  use_pull_ops: None", "  mock: []",
    #  # "  log: None"],
    #  # 'test': 'in'},
    # # None, RUN],

    ['Verify connection subcommand list empty repository.',
     ['list'],
     {'stdout': [
         "WBEMServer Connections:",
         "name    server uri    namespace    user    password    "
         "timeout    noverify    certfile    keyfile    log",
         "------  ------------  -----------  ------  ----------  ---------  "
         "----------  ----------  ---------  -----"],
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand delete, empty repo fails.',
     ['delete', 'blah'],
     {'stderr': "Error: blah not a defined connection name",
      'rc': 1,
      'test': 'lines'},
     None, OK],

    # The following 3 tests are a sequence. Each depends on the previous.
    ['Verify connection subcommand new with simple arguments only.',
     ['new', 'test1', 'http://blah'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, RUN],

    ['Verify connection subcommand show  ',
     ['show', 'test1'],
     {'stdout': [
         "Name: test1", "  WBEMServer uri: http://blah",
         "  Default_namespace: root/cimv2", "  User: None", "  Password: None",
         "  Timeout: None", "  Noverify: False", "  Certfile: None",
         "  Keyfile: None", "  use_pull_ops: None", "  mock: []",
         "  log: None"],
      'test': 'in'},
     None, RUN],

    ['Verify connection subcommand new with complex options.',
     ['new', 'test2', 'http://blahblah', '-u', 'fred', '-p', 'argh', '-t',
      '18', '-n', '-l', 'api=file,all'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, RUN],

    ['Verify connection subcommand show  ',
     ['show', 'test1'],
     {'stdout': [
         "Name: test1", "  WBEMServer uri: http://blah",
         "  Default_namespace: root/cimv2", "  User: None", "  Password: None",
         "  Timeout: None", "  Noverify: False", "  Certfile: None",
         "  Keyfile: None", "  use_pull_ops: None", "  mock: []",
         "  log: None"],
      'test': 'in'},
     None, RUN],

    ['Verify connection subcommand show  ',
     ['show', 'test2'],
     {'stdout': [
         "Name: test2", "  WBEMServer uri: http://blahblah",
         "  Default_namespace: root/cimv2", "  User: fred", "  Password: argh",
         "  Timeout: 18", "  Noverify: True", "  Certfile: None",
         "  Keyfile: None", "  use_pull_ops: None", "  mock: []",
         "  log: api=file,all"],
      'test': 'in'},
     None, RUN],

    ['Verify connection subcommand list  ',
     ['list'],
     {'stdout': ["test1   http://blah      root/cimv2"
                 "                                  False",
                 "test2   http://blahblah  root/cimv2   fred    argh"
                 "               18  True"],
      'test': 'in'},
     None, RUN],

    ['Verify connection subcommand delete ',
     ['delete', 'test1'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, RUN],

    ['Verify connection subcommand delete ',
     ['delete', 'test2'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'None'}},
     None, RUN],

    # TODO additional tests
]


class TestSubcmdClass(CLITestsBase):
    """
    Test all of the class subcommand variations.
    """
    subcmd = 'connection'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_connection(self, desc, inputs, exp_response, mock, condition):
        """
        Common test method for those subcommands and options in the
        class subcmd that can be tested.

        """
        # Where is this file to be located for tests.
        pywbemserversfile = CONNECTIONS_FILE

        def test_file(file_test):
            """Local function to execute tests on servers file."""
            if file_test == 'exists':
                assert os.path.isfile(pywbemserversfile) and \
                    os.path.getsize(pywbemserversfile) > 0, \
                    "Fail. File  %s should exist" % pywbemserversfile
            elif file_test == 'none':
                assert not os.path.isfile(pywbemserversfile), \
                    "Fail. File %s should exist" % pywbemserversfile

        if 'file' in exp_response:
            if 'before' in exp_response['file']:
                test_file(exp_response['file']['before'])

        self.subcmd_test(desc, self.subcmd, inputs, exp_response,
                         mock, condition, verbose=False)

        if 'file' in exp_response:
            if 'after' in exp_response['file']:
                test_file(exp_response['file']['after'])
