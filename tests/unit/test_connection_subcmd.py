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
Test the connection command group and its subcommands.. This test depends on
a pywbemcliservers.json file in the test directory.  It assumes that the
test directory is the same as the current working directory where pywbemcli
was called.
"""

# TODO: clean up the connection repository file before and after the
#       tests

import os
import pytest
from .cli_test_extensions import CLITestsBase

from pywbemcli._connection_repository import DEFAULT_CONNECTIONS_FILE

SCRIPT_DIR = os.path.dirname(__file__)
TEST_DIR = os.getcwd()
REPO_FILE_PATH = os.path.join(TEST_DIR, DEFAULT_CONNECTIONS_FILE)
# if there is a config file, save to this name during tests
SAVE_FILE = DEFAULT_CONNECTIONS_FILE + '.testsave'
SAVE_FILE_PATH = os.path.join(SCRIPT_DIR, SAVE_FILE)

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
  add     Create a new named WBEM connection.
  delete  Delete connection information.
  export  Export the current connection information.
  list    List the entries in the connection file.
  save    Save current connection to repository.
  select  Select a connection from defined connections.
  show    Show current or NAME connection information.
  test    Execute a predefined wbem request.
"""

CONN_SHOW_HELP = """Usage: pywbemcli connection show [COMMAND-OPTIONS] NAME

  Show current or NAME connection information.

  This subcommand displays  all the variables that make up the current WBEM
  connection if the optional NAME argument is NOT provided. If NAME not
  supplied, a list of connections from the connections definition file is
  presented with a prompt for the user to select a NAME.

  The information on the     connection named is displayed if that name is
  in the persistent repository.

Options:
  -h, --help  Show this message and exit.
"""

CONN_DEL_HELP = """Usage: pywbemcli connection delete [COMMAND-OPTIONS] NAME

  Delete connection information.

  Delete connection information from the persistent store for the connection
  defined by NAME. The NAME argument is optional.

  If NAME not supplied, a select list presents the list of connection
  definitions for selection.

  Example:   connection delete blah

Options:
  -V, --verify  If set, The change is displayed and verification requested
                before the change is executed
  -h, --help    Show this message and exit.
"""

CONN_SAVE_HELP = """Usage: pywbemcli connection save [COMMAND-OPTIONS]

  Save current connection to repository.

  Saves the current connection to the connections file if it does not
  already exist in that file.

  This is useful when you have defined a connection on the command line and
  want to set it into the connections file.

Options:
  -V, --verify  If set, The change is displayed and verification requested
                before the change is executed
  -h, --help    Show this message and exit.
"""

CONN_ADD_HELP = """Usage: pywbemcli connection add [COMMAND-OPTIONS] NAME uri

  Create a new named WBEM connection.

  This subcommand creates and saves a named connection from the input
  arguments (NAME and URI) and options in the connections file.

  The new connection can be referenced by the name argument in the future.
  This connection object is capable of managing all of the properties
  defined for WBEMConnections.

  The NAME and URI arguments MUST exist. They define the server uri and the
  unique name under which this server connection information will be stored.
  All other properties are optional.

  Adding a connection does not the new connection as the current connection.
  Use `connection select` to set a particular stored connection definition
  as the current connection.

  A new connection can also be defined by supplying the parameters on the
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
  -V, --verify                    If set, The change is displayed and
                                  verification requested before the change is
                                  executed
  -h, --help                      Show this message and exit.
"""

CONN_LIST_HELP = """Usage: pywbemcli connection list [COMMAND-OPTIONS]

  List the entries in the connection file.

  This subcommand displays all entries in the connection file as a table
  using the command line output_format to define the table format.

  An "*" after the name indicates the currently selected connection.

Options:
  -h, --help  Show this message and exit.
"""

CONN_TEST_HELP = """Usage: pywbemcli connection test [COMMAND-OPTIONS]

  Execute a predefined wbem request.

  This executes a predefined request against the currente WBEM server to
  confirm that the connection exists and is working.

  It executes getclass on CIM_ManagedElement as the test.

Options:
  -h, --help  Show this message and exit.
"""

CONN_EXPORT_HELP = """Usage: pywbemcli connection export [COMMAND-OPTIONS]

  Export  the current connection information.

  Creates an export statement for each connection variable and outputs the
  statement to the conole.

Options:
  -h, --help  Show this message and exit.
"""

CONN_SELECT_HELP = """Usage: pywbemcli connection select [COMMAND-OPTIONS] NAME

  Select a connection from defined connections.

  Selects a connection from the persistently stored set of named connections
  if NAME exists in the store. The NAME argument is optional.  If NAME not
  supplied, a list of connections from the connections definition file is
  presented with a prompt for the user to select a NAME.

  Select state is not persistent.

  Examples:

     connection select <name>    # select the defined <name>

     connection select           # presents select list to pick connection

Options:
  -h, --help  Show this message and exit.
"""


@pytest.fixture(scope='session', autouse=True)
def set_connections_file(request):
    """
    Fixture to hide any existing repo at the beginning and restore it
    at the end of the session.  This assumes that the connection repository
    is in the root directory of pywbemcli which is logical since that file
    is defined by the call to pywbemcli in tests.
    """
    if os.path.isfile(REPO_FILE_PATH):
        os.rename(REPO_FILE_PATH, SAVE_FILE_PATH)

    def teardown():
        """
        Remove any created repository file and restore saved file. This
        should occur as session end.
        """
        if os.path.isfile(REPO_FILE_PATH):
            os.remove(REPO_FILE_PATH)
        if os.path.isfile(SAVE_FILE_PATH):
            os.rename(SAVE_FILE_PATH, REPO_FILE_PATH)

    request.addfinalizer(teardown)


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
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand add  --help response',
     ['add', '--help'],
     {'stdout': CONN_ADD_HELP,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand list  --help response',
     ['list', '--help'],
     {'stdout': CONN_LIST_HELP,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand test  --help response',
     ['test', '--help'],
     {'stdout': CONN_TEST_HELP,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand export  --help response',
     ['export', '--help'],
     {'stdout': CONN_EXPORT_HELP,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand select  --help response',
     ['select', '--help'],
     {'stdout': CONN_SELECT_HELP,
      'test': 'lines'},
     None, OK],

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

    #
    # The following tests are a sequence. Each depends on the previous
    # and what was in the repository.
    #
    ['Verify connection subcommand add with simple arguments only.',
     ['add', 'test1', 'http://blah'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand show  ',
     ['show', 'test1'],
     {'stdout': [
         "Name: test1", "  WBEMServer uri: http://blah",
         "  Default_namespace: root/cimv2", "  User: None", "  Password: None",
         "  Timeout: None", "  Noverify: False", "  Certfile: None",
         "  Keyfile: None", "  use_pull_ops: None", "  mock: []",
         "  log: None"],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand add with complex options.',
     ['add', 'test2', 'http://blahblah', '-u', 'fred', '-p', 'argh', '-t',
      '18', '-n', '-l', 'api=file,all'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand show  ',
     ['show', 'test1'],
     {'stdout': [
         "Name: test1", "  WBEMServer uri: http://blah",
         "  Default_namespace: root/cimv2", "  User: None", "  Password: None",
         "  Timeout: None", "  Noverify: False", "  Certfile: None",
         "  Keyfile: None", "  use_pull_ops: None", "  mock: []",
         "  log: None"],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand show  ',
     ['show', 'test2'],
     {'stdout': [
         "Name: test2", "  WBEMServer uri: http://blahblah",
         "  Default_namespace: root/cimv2", "  User: fred", "  Password: argh",
         "  Timeout: 18", "  Noverify: True", "  Certfile: None",
         "  Keyfile: None", "  use_pull_ops: None", "  mock: []",
         "  log: api=file,all"],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand list  with 2 servers defined',
     ['list'],
     {'stdout': ["test1   http://blah      root/cimv2                       "
                 "           False",
                 "test2   http://blahblah  root/cimv2   fred    argh        "
                 "       18  True                               api=file,all"],
      'test': 'in'},
     None, OK],


    ['Verify connection subcommand select test2',
     ['select', 'test2'],
     {'stdout': [""],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand list  with 2 servers defined, not sel after '
     ' next pywbemcli call',
     ['list'],
     {'stdout': ["test1   http://blah      root/cimv2                       "
                 "           False",
                 "test2   http://blahblah  root/cimv2   fred    argh        "
                 "       18  True                               api=file,all"],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand delete ',
     ['delete', 'test1'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'None'}},
     None, OK],

    ['Verify connection subcommand delete ',
     ['delete', 'test2'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'None'}},
     None, OK],

    ['Verify connection subcommand list empty repository.',
     ['list'],
     {'stdout': [
         "WBEMServer Connections:",
         "name    server uri    namespace    user    password    "
         "timeout    noverify    certfile    keyfile    log",
         "------  ------------  -----------  ------  ----------  ---------  "
         "----------  ----------  ---------  -----"],
      'test': 'lines',
      'file': {'before': 'None', 'after': 'None'}},

     None, OK],

    #
    #   The following is a new sequence but depends on the repo being empty
    #
    ['Verify connection subcommand add with add all arguments.',
     ['add', 'addallargs', 'http://blah',
      '--default_namespace', 'root/blah',
      '--user', 'john',
      '--password', 'pw',
      '--timeout', '30',
      '--noverify',
      '--certfile', 'mycertfile.pem',
      '--keyfile', 'mykeyfile.pem', ],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],


    ['Verify connection subcommand show with all params',
     ['show', 'addallargs'],
     {'stdout': [
         "Name: addallargs",
         "  WBEMServer uri: http://blah",
         "  Default_namespace: root/blah",
         "  User: john",
         "  Password: pw",
         "  Certfile: mycertfile.pem",
         "  Keyfile: mykeyfile.pem",
         "  use_pull_ops: None",
         "  mock: []",
         "  log: None"],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand delete ',
     ['delete', 'addallargs'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'None'}},
     None, OK],

    #
    #  Test command line parameter errors
    #
    ['Verify connection subcommand select with name not in repo',
     ['show', 'Blah'],
     {'stderr': ["Error: Name Blah not in servers repository"],
      'rc': 1,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand select with no name empty repo repo',
     ['show', 'Blah'],
     {'stderr': ["Error: Name Blah not in servers repository"],
      'rc': 1,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand add no uri',
     ['add', 'blah'],
     {'stderr': ['Usage: pywbemcli connection add [COMMAND-OPTIONS] NAME uri',
                 'Try "pywbemcli connection add -h" for help.',
                 '',
                 'Error: Missing argument "uri".'],
      'rc': 2,
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand add with bad arg.',
     ['add', 'addallargs', 'http://blah',
      '--timeout', 'fred', ],
     {'stderr': ['Usage: pywbemcli connection add [COMMAND-OPTIONS] NAME uri',
                 'Error: Invalid value for "-t" / "--timeout": '
                 'fred is not a valid integer'],
      'rc': 2,
      'test': 'in',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

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
        class subcmd that can be tested.  Note the
        fixture remove_connection_file which is session, autouse so should
        hide any existing connection file at beginning of this test and
        restore it after the test.
        """
        # Where is this file to be located for tests.
        pywbemserversfile = REPO_FILE_PATH

        def test_file(file_test):
            """Local function to execute tests on servers file."""
            if file_test == 'exists':
                assert os.path.isfile(pywbemserversfile) and \
                    os.path.getsize(pywbemserversfile) > 0, \
                    "Fail. File  %s should exist" % pywbemserversfile
            elif file_test == 'none':
                assert not os.path.isfile(pywbemserversfile), \
                    "Fail. File %s should exist" % pywbemserversfile

        if not condition:
            pytest.skip("Condition for test case not met")

        if condition == 'pdb':
            import pdb
            pdb.set_trace()

        if 'file' in exp_response:
            if 'before' in exp_response['file']:
                test_file(exp_response['file']['before'])

        self.subcmd_test(desc, self.subcmd, inputs, exp_response,
                         mock, condition, verbose=False)

        if 'file' in exp_response:
            if 'after' in exp_response['file']:
                test_file(exp_response['file']['after'])
