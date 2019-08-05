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

import os
import pytest
from pywbemtools.pywbemcli._connection_repository \
    import DEFAULT_CONNECTIONS_FILE

from .cli_test_extensions import CLITestsBase

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
MOCK_PROMPT0_FILE = "mock_prompt_0.py"
MOCK_CONFIRMY_FILE = "mock_confirm_y.py"

TEST_DIR = os.path.dirname(__file__)

# Get the relative path to the current directory.  This presumes that the
# test was run from the pywbemtools directory
TEST_DIR_REL = os.path.relpath(TEST_DIR)
MOCK_FILE_PATH = os.path.join(TEST_DIR_REL, SIMPLE_MOCK_FILE)

CONN_HELP = """
Usage: pywbemcli connection [COMMAND-OPTIONS] COMMAND [ARGS]...

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
  test    Execute a predefined WBEM request.
"""

CONN_SHOW_HELP = """
Usage: pywbemcli connection show [COMMAND-OPTIONS] NAME

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

CONN_DEL_HELP = """
Usage: pywbemcli connection delete [COMMAND-OPTIONS] NAME

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

CONN_SAVE_HELP = """
Usage: pywbemcli connection save [COMMAND-OPTIONS]

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

CONN_ADD_HELP = """
Usage: pywbemcli connection add [COMMAND-OPTIONS]

  Create a new named WBEM connection.

  This subcommand creates and saves a named connection from the input
  options in the connections file.

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
  command line and using the `connection save` command to put it into the
  connection repository.

Options:
  -s, --server SERVER             Required hostname or IP address with scheme
                                  of the WBEMServer in format:
                                  [{scheme}://]{host}[:{port}]
                                  * Scheme: must
                                  be "https" or "http" [Default: "https"]
                                  *
                                  Host: defines short/fully qualified DNS
                                  hostname, literal IPV4 address (dotted), or
                                  literal IPV6 address
                                  * Port: (optional)
                                  defines WBEM server port to be used
                                  [Defaults: 5988(HTTP) and 5989(HTTPS)].
  -n, --name NAME                 Required name for the connection(optional,
                                  see --server).  This is the name for this
                                  defined WBEM server in the connection file
                                  [required]
  -d, --default-namespace NAMESPACE
                                  Default namespace to use in the target
                                  WBEMServer if no namespace is defined in the
                                  subcommand (Default: root/cimv2).
  -u, --user TEXT                 User name for the WBEM Server connection.
  -p, --password TEXT             Password for the WBEM Server. Will be
                                  requested as part  of initialization if user
                                  name exists and it is not  provided by this
                                  option.
  -t, --timeout INTEGER RANGE     Operation timeout for the WBEM Server in
                                  seconds. Default: 30
  -N, --noverify                  If set, client does not verify server
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

CONN_LIST_HELP = """
Usage: pywbemcli connection list [COMMAND-OPTIONS]

  List the entries in the connection file.

  This subcommand displays all entries in the connection file as a table
  using the command line output_format to define the table format with
  default of simple format.

  An "*" after the name indicates the currently selected connection.

Options:
  -h, --help  Show this message and exit.
"""

CONN_TEST_HELP = """
Usage: pywbemcli connection test [COMMAND-OPTIONS]

  Execute a predefined WBEM request.

  This executes a predefined request against the current WBEM server to
  confirm that the connection exists and is working.

  It executes EnumerateClassNames on the default namespace as the test.

Options:
  -h, --help  Show this message and exit.
"""

CONN_EXPORT_HELP = """
Usage: pywbemcli connection export [COMMAND-OPTIONS]

  Export  the current connection information.

  Creates an export statement for each connection variable and outputs the
  statement to the conole.

Options:
  -h, --help  Show this message and exit.
"""

CONN_SELECT_HELP = """
Usage: pywbemcli connection select [COMMAND-OPTIONS] NAME

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


OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet


TEST_CASES = [
    # desc - Description of test
    # inputs - String, or list of args or dict of 'env', 'args', 'globals',
    #          and 'stdin'. See See CLITestsBase.subcmd_test()  for
    #          detailed documentation
    # exp_response - Dictionary of expected responses (stdout, stderr, rc) and
    #                test definition (test: <testname>).
    #                See CLITestsBase.subcmd_test() for detailed documentation.
    # mock - None or name of files (mof or .py),
    # condition - If True, the test is executed,  Otherwise it is skipped.

    ['Verify connection subcommand help response',
     '--help',
     {'stdout': CONN_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand show --help response',
     ['show', '--help'],
     {'stdout': CONN_SHOW_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand delete --help response',
     ['delete', '--help'],
     {'stdout': CONN_DEL_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand save --help response',
     ['save', '--help'],
     {'stdout': CONN_SAVE_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand add --help response',
     ['add', '--help'],
     {'stdout': CONN_ADD_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand list --help response',
     ['list', '--help'],
     {'stdout': CONN_LIST_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand test --help response',
     ['test', '--help'],
     {'stdout': CONN_TEST_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand export --help response',
     ['export', '--help'],
     {'stdout': CONN_EXPORT_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand select  --help response',
     ['select', '--help'],
     {'stdout': CONN_SELECT_HELP,
      'test': 'linesnows'},
     None, OK],

    # ['Verify connection subcommand new. test with show and delete  ',
    # # {'stdin': ['connection new test1 http://blah', 'connection show test1',
    #            # 'connection delete test1']},
    # # {'stdout': ["Name: test1", "  WBEMServer uri: http://blah",
    #  # "  Default_namespace: root/cimv2", "  User: None", "  Password: None",
    #  # "  Timeout: None", "  Noverify: False", "  Certfile: None",
    #  # "  Keyfile: None", "  use-pull-ops: None", "  mock: ",
    #  # "  log: None"],
    #  # 'test': 'in'},
    # # None, OK],

    ['Verify connection subcommand list empty repository.',
     {'global': ['-o', 'simple'],
      'args': ['list']},
     {'stdout': [
         "WBEMServer Connections:", ""],
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
     ['add', '--name', 'test1', '-s', 'http://blah'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand show  ',
     ['show', 'test1'],
     {'stdout': [
         "Name: test1", "  WBEMServer uri: http://blah",
         "  Default-namespace: root/cimv2", "  User: None", "  Password: None",
         "  Timeout: None", "  Noverify: False", "  Certfile: None",
         "  Keyfile: None", "  use-pull-ops: None", "  mock: ",
         "  log: None"],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand add with complex options and verify',
     ['add', '--name', 'test2', '-s', 'http://blahblah', '-u', 'fred', '-p',
      'argh', '-t', '18', '-N', '-l', 'api=file,all', '--verify'],
     {'stdout': "Execute add connection",
      'test': ['test2', 'Execute add connection'],
      'file': {'before': 'exists', 'after': 'exists'}},
     MOCK_CONFIRMY_FILE, OK],

    ['Verify connection subcommand show  ',
     ['show', 'test1'],
     {'stdout': [
         "Name: test1", "  WBEMServer uri: http://blah",
         "  Default-namespace: root/cimv2", "  User: None", "  Password: None",
         "  Timeout: None", "  Noverify: False", "  Certfile: None",
         "  Keyfile: None", "  use-pull-ops: None", "  mock: ",
         "  log: None"],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand show  ',
     ['show', 'test2'],
     {'stdout': [
         "Name: test2", "  WBEMServer uri: http://blahblah",
         "  Default-namespace: root/cimv2", "  User: fred", "  Password: argh",
         "  Timeout: 18", "  Noverify: True", "  Certfile: None",
         "  Keyfile: None", "  use-pull-ops: None", "  mock: ",
         "  log: api=file,all"],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand list  with 2 servers defined',
     {'global': ['--output-format', 'simple'],
      'args': ['list']},
     {'stdout': ['WBEMServerConnections:',
                 'name    server uri namespace user timeout noverify    log',
                 '---------------------------------------------------------'
                 '------------',
                 "test1   http://blah      root/cimv2   False",
                 "test2   http://blahblah  root/cimv2   fred  18  True "
                 "api=file,all"],
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand select test2',
     ['select', 'test2'],
     {'stdout': "",
      'test': 'regex'},
     None, OK],

    ['Verify connection subcommand select test2',
     ['select', 'test9'],
     {'stderr': ['Connection name "test9" does not exist'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify connection subcommand list  with 2 servers defined, not sel after '
     ' next pywbemcli call',
     {'global': ['--output-format', 'simple'],
      'args': ['list']},
     {'stdout': ['WBEMServerConnections:',
                 'name    server uri namespace user timeout noverify    log',
                 '---------------------------------------------------------'
                 '------------',
                 'test1   http://blah      root/cimv2  False',
                 'test2   http://blahblah  root/cimv2   fred 18  True '
                 'api=file,all'],
      'test': 'linesnows'},
     None, OK],

    ['Verify connection subcommand delete test1',
     ['delete', 'test1'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'None'}},
     None, OK],

    ['Verify connection subcommand test',
     ['test'],
     {'stdout': "Connection successful",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify connection subcommand delete test2',
     ['delete', 'test2'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'None'}},
     None, OK],

    ['Verify connection subcommand list empty repository.',
     {'global': ['-o', 'simple'],
      'args': ['list']},
     {'stdout': [
         "WBEMServer Connections:", ""],
      'test': 'linesnows',
      'file': {'before': 'None', 'after': 'None'}},

     None, OK],

    #
    #   The following is a new sequence but depends on the repo being empty
    #   It creates, shows and deletes a single server definition.
    #
    ['Verify connection subcommand add with all arguments.',
     ['add', '--name', 'addallargs',
      '--server', 'http://blah',
      '--default-namespace', 'root/blah',
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

    ['Verify connection subcommand with duplicate name fails.',
     ['add', '--name', 'addallargs',
      '--server', 'http://blah',
      '--default_namespace', 'root/blah',
      '--user', 'john',
      '--password', 'pw',
      '--timeout', '30',
      '--noverify',
      '--certfile', 'mycertfile.pem',
      '--keyfile', 'mykeyfile.pem', ],
     {'stderr': 'Connection name "addallargs" already defined',
      'rc': 1,
      'test': 'in',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand show with all params',
     ['show', 'addallargs'],
     {'stdout': [
         'Name: addallargs',
         '  WBEMServer uri: http://blah',
         '  Default-namespace: root/blah',
         '  User: john',
         '  Password: pw',
         '  Certfile: mycertfile.pem',
         '  Keyfile: mykeyfile.pem',
         '  use-pull-ops: None',
         '  pull-max-cnt: 1000',
         '  mock: ',
         '  log: None'],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand delete addallargs',
     ['delete', 'addallargs'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'None'}},
     None, OK],

    # uses regex because windows generates set and linux export in statements
    # No file verification required. Does not use file
    ['Verify connection subcommand export',
     {'args': ['export'],
      'global': ['-s', 'http://blah', '-u', 'fred', '-p', 'arghh', '-N',
                 '-c', 'certfile.txt', '-k', 'keyfile.txt', '-t', '12']},
     {'stdout': ['PYWBEMCLI_SERVER=http://blah$',
                 'PYWBEMCLI_DEFAULT_NAMESPACE=root/cimv2$',
                 'PYWBEMCLI_USER=fred$',
                 'PYWBEMCLI_PASSWORD=argh',
                 'PYWBEMCLI_TIMEOUT=12$',
                 'PYWBEMCLI_NOVERIFY=True$',
                 'PYWBEMCLI_CERTFILE=certfile.txt$',
                 'PYWBEMCLI_KEYFILE=keyfile.txt$',
                 # account for windows and non_windows platforms
                 '^(export|set) '],
      'test': 'regex',
      'file': {'before': 'None', 'after': 'None'}},
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

    ['Verify connection subcommand add with bad arg fails',
     ['add', '--name', 'addallargs', '-s', 'http://blah',
      '--timeout', 'fred', ],
     {'stderr': ['Usage: pywbemcli connection add [COMMAND-OPTIONS]',
                 'Error: Invalid value for "-t" / "--timeout": '
                 'fred is not a valid integer'],
      'rc': 2,
      'test': 'in',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection subcommand add no server option fails, no --server',
     ['add', '--name', 'blah'],
     {'stderr': ['Error:',
                 'Add failed',
                 'Missing server definition',
                 '"--server" or "--mock-server" required'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify connection subcommand fails, no --name.',
     ['add',
      '--server', 'http://strangename',
      '--default-namespace', 'root/blah',
      '--user', 'john',
      '--password', 'pw',
      '--timeout', '30',
      '--noverify',
      '--certfile', 'mycertfile.pem',
      '--keyfile', 'mykeyfile.pem', ],
     {'stderr': ['Usage: pywbemcli connection add [COMMAND-OPTIONS]',
                 'Try "pywbemcli connection add -h" for help.',
                 '',
                 'Error: Missing option "-n" / "--name".'],
      'rc': 2,
      'test': 'lines',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection subcommand select, empty repo fails',
     ['select'],
     {'stderr': ["Connection repository", "empty"],
      'rc': 1,
      'test': 'regex',
      'file': {'before': 'none', 'after': 'None'}},
     None, OK],

    ['Verify connection subcommand delete, empty repo fails',
     ['delete'],
     {'stderr': ["Connection repository", "empty"],
      'rc': 1,
      'test': 'regex',
      'file': {'before': 'none', 'after': 'None'}},
     None, OK],

    #
    #  Verify create and save mock connection sequence. Starts with empty
    #  server adds a mock server, shows it, tests if valid, and deletes
    #  the connection
    #

    ['Verify mock connection exists.',
     ['add', '--name', 'mocktest', '--mock-server', MOCK_FILE_PATH],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand shows mock file ',
     ['show', 'mocktest'],
     {'stdout': [
         "Name: mocktest",
         "  Default-namespace: root/cimv2",
         "  User: None", "  Password: None",
         "  Timeout: None",
         "  Noverify: False", "  Certfile: None",
         "  Keyfile: None", "  use-pull-ops: None",
         r"  mock: tests", r"simple_mock_model.mof",
         "  log: None"],
      'test': 'regex'},
     None, OK],

    ['Verify connection subcommand test against existing mock def',
     {'args': ['test'],
      'global': ['--name', 'mocktest']},
     {'stdout': "Connection successful",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify connection subcommand select mocktest with prompt ',
     ['select'],
     {'stdout': "",
      'test': 'in',
      'file': {'before': 'exists', 'after': 'exists'}},
     MOCK_PROMPT0_FILE, OK],

    ['Verify connection subcommand delete with prompt that selects 0',
     ['delete', ],
     {'stdout': ['Select a connection or CTRL_C to abort.',
                 '0: mocktest',
                 'Input integer between 0 and 0 or Ctrl-C to exit selection:'],
      'test': 'linesnows',
      'file': {'before': 'exists', 'after': 'None'}},
     MOCK_PROMPT0_FILE, OK],

    ['Verify Add mock server to empty connections file.',
     ['add', '--name', 'mocktest', '--mock-server', MOCK_FILE_PATH],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand delete with prompt that selects y for '
     'verify',
     ['delete', 'mocktest', '--verify'],
     {'stdout': ['Name: mocktest', 'Execute delete'],
      'test': 'regex',
      'file': {'before': 'exists', 'after': 'None'}},
     MOCK_CONFIRMY_FILE, OK],

    #
    #  Verify Create from mock with cmd line params, save, show, delete works
    #
    ['Verify save server with cmd line params to empty connections file. Use '
     '--verify',
     {'args': ['save', '--verify'],
      'global': ['--name', 'svrtest2',
                 '--server', 'http://blah',
                 '--timeout', '45',
                 '--use-pull-ops', 'no',
                 '--default-namespace', 'root/blah',
                 '--user', 'john',
                 '--password', 'pw',
                 '--noverify',
                 '--certfile', 'mycertfile.pem',
                 '--keyfile', 'mykeyfile.pem']},
     {'stdout': "",
      'test': 'in',
      'file': {'before': 'none', 'after': 'exists'}},
     MOCK_CONFIRMY_FILE, OK],

    ['Verify save mock server with cmd line params to empty connections file.',
     {'args': ['save'],
      'global': ['--name', 'mocktest2',
                 '--mock-server', MOCK_FILE_PATH,
                 '--timeout', '45',
                 '--use-pull-ops', 'no',
                 '--default-namespace', 'root/blah',
                 '--user', 'john',
                 '--password', 'pw',
                 '--noverify',
                 '--certfile', 'mycertfile.pem',
                 '--keyfile', 'mykeyfile.pem']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand shows mock file ',
     ['show', 'mocktest2'],
     {'stdout': [
         "Name: mocktest2",
         "  Default-namespace: root/blah", "  User: john", "  Password: pw",
         "  Timeout: 45", "  Noverify: True", "  Certfile: mycertfile.pem",
         "  Keyfile: mykeyfile.pem", "  use-pull-ops: False",
         r"  mock: tests", "simple_mock_model.mof",
         "  log: None"],
      'test': 'regex',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand shows svrtest2 ',
     ['show', 'svrtest2'],
     {'stdout': [
         "Name: svrtest2",
         "  WBEMServer uri: http://blah",
         "  Default-namespace: root/blah", "  User: john", "  Password: pw",
         "  Timeout: 45", "  Noverify: True", "  Certfile: mycertfile.pem",
         "  Keyfile: mykeyfile.pem", "  use-pull-ops: False",
         "  mock:",
         "  log: None"],
      'test': 'in',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand delete works'
     'verify',
     ['delete', 'mocktest2'],
     {'stdout': "",
      'test': 'regex',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand delete works',
     ['delete', 'svrtest2'],
     {'stdout': "",
      'test': 'regex',
      'file': {'before': 'exists', 'after': 'none'}},
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
                         mock, condition)

        if 'file' in exp_response:
            if 'after' in exp_response['file']:
                test_file(exp_response['file']['after'])
