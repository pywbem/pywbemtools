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
Test the connection command group and its subcommands. This test depends on
a pywbemcliservers.json file in the test directory.  It assumes that the
test directory is the same as the current working directory where pywbemcli
was called.
"""

import os
import pytest

from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE, \
    CMD_OPTION_VERIFY_HELP_LINE

SCRIPT_DIR = os.path.dirname(__file__)

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
CONFIRM_FILE_PATH = os.path.join(TEST_DIR_REL, MOCK_CONFIRMY_FILE)

CONNECTION_HELP_LINES = [
    'Usage: pywbemcli connection [COMMAND-OPTIONS] COMMAND [ARGS]...',
    'Command group for WBEM connection definitions.',
    CMD_OPTION_HELP_HELP_LINE,
    'add     Add a new WBEM connection definition from specified options.',
    'delete  Delete a WBEM connection definition.',
    'export  Export the current connection.',
    'list    List the WBEM connection definitions.',
    'save    Save the current connection to a new WBEM connection definition.',
    'select  Select a WBEM connection definition as current or default.',
    'show    Show connection info of a WBEM connection definition.',
    'test    Test the current connection with a predefined WBEM request.',
]

CONNECTION_ADD_HELP_LINES = [
    'Usage: pywbemcli connection add [COMMAND-OPTIONS] NAME',
    'Add a new WBEM connection definition from specified options.',
    '-s, --server URL Use the WBEM server at the specified URL',
    '-u, --user TEXT User name for the WBEM server.',
    '-p, --password TEXT Password for the WBEM server.',
    '-t, --timeout INT Timeout in seconds for operations with the WBEM server.',
    '-N, --no-verify Do not verify the X.509 server certificate',
    '--ca-certs FILE Path name of a file or directory containing ',
    '-c, --certfile FILE Path name of a PEM file containing a X.509 client',
    '-k, --keyfile FILE Path name of a PEM file containing a X.509 private',
    '-U, --use-pull [yes|no|either] Determines whether pull operations are',
    '-m, --mock-server FILE Use a mock WBEM server',
    '--pull-max-cnt INT Maximum number of instances to be returned',
    '-d, --default-namespace NAMESPACE Default namespace',
    '-l, --log COMP=DEST:DETAIL,... Enable logging of the WBEM operations',
    CMD_OPTION_VERIFY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CONNECTION_DELETE_HELP_LINES = [
    'Usage: pywbemcli connection delete [COMMAND-OPTIONS] NAME',
    'Delete a WBEM connection definition.',
    CMD_OPTION_VERIFY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CONNECTION_EXPORT_HELP_LINES = [
    'Usage: pywbemcli connection export [COMMAND-OPTIONS]',
    'Export the current connection.',
    CMD_OPTION_HELP_HELP_LINE,
]

CONNECTION_LIST_HELP_LINES = [
    'Usage: pywbemcli connection list [COMMAND-OPTIONS]',
    'List the WBEM connection definitions.',
    CMD_OPTION_HELP_HELP_LINE
]

CONNECTION_SAVE_HELP_LINES = [
    'Usage: pywbemcli connection save [COMMAND-OPTIONS] NAME',
    'Save the current connection to a new WBEM connection definition.',
    CMD_OPTION_VERIFY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE
]

CONNECTION_SELECT_HELP_LINES = [
    'Usage: pywbemcli connection select [COMMAND-OPTIONS] NAME',
    'Select a WBEM connection definition as current or default.',
    '-d, --default  If set, the connection is set to be the default ',

    CMD_OPTION_HELP_HELP_LINE
]

CONNECTION_SHOW_HELP_LINES = [
    'Usage: pywbemcli connection show [COMMAND-OPTIONS] NAME',
    'Show connection info of a WBEM connection definition.',
    CMD_OPTION_HELP_HELP_LINE
]

CONNECTION_TEST_HELP_LINES = [
    'Usage: pywbemcli connection test [COMMAND-OPTIONS]',
    'Test the current connection with a predefined WBEM request.',
    CMD_OPTION_HELP_HELP_LINE,
]

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

    ['Verify connection command --help response',
     '--help',
     {'stdout': CONNECTION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand -h response',
     '-h',
     {'stdout': CONNECTION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand add --help response',
     ['add', '--help'],
     {'stdout': CONNECTION_ADD_HELP_LINES,
      'test': 'inows'},
     None, OK],

    ['Verify connection subcommand add -h response',
     ['add', '-h'],
     {'stdout': CONNECTION_ADD_HELP_LINES,
      'test': 'inows'},
     None, OK],

    ['Verify connection subcommand delete --help response',
     ['delete', '--help'],
     {'stdout': CONNECTION_DELETE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand delete -h response',
     ['delete', '-h'],
     {'stdout': CONNECTION_DELETE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand export --help response',
     ['export', '--help'],
     {'stdout': CONNECTION_EXPORT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand export -h response',
     ['export', '-h'],
     {'stdout': CONNECTION_EXPORT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand list --help response',
     ['list', '--help'],
     {'stdout': CONNECTION_LIST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand list -h response',
     ['list', '-h'],
     {'stdout': CONNECTION_LIST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand save --help response',
     ['save', '--help'],
     {'stdout': CONNECTION_SAVE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand save -h response',
     ['save', '-h'],
     {'stdout': CONNECTION_SAVE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand select  --help response',
     ['select', '--help'],
     {'stdout': CONNECTION_SELECT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand select  -h response',
     ['select', '-h'],
     {'stdout': CONNECTION_SELECT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand show --help response',
     ['show', '--help'],
     {'stdout': CONNECTION_SHOW_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand show -h response',
     ['show', '-h'],
     {'stdout': CONNECTION_SHOW_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand test --help response',
     ['test', '--help'],
     {'stdout': CONNECTION_TEST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand test -h response',
     ['test', '-h'],
     {'stdout': CONNECTION_TEST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    # ['Verify connection subcommand new. test with show and delete  ',
    # # {'stdin': ['connection new test1 http://blah', 'connection show test1',
    #            # 'connection delete test1']},
    # # {'stdout': ["name: test1", "  WBEM Server uri: http://blah",
    #  # "  default-namespace: root/cimv2", "  user: None", "  password: None",
    #  # "  timeout: None", "  Noverify: False", "  certfile: None",
    #  # "  keyfile: None", "  use-pull: None", "  mock-server:",
    #  # "  log: None"],
    #  # 'test': 'in'},
    # # None, OK],

    ['Verify connection subcommand list empty repository.',
     {'global': ['-o', 'simple'],
      'args': ['list']},
     {'stdout': [
         "WBEM server connections:", ""],
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand delete, empty repo fails.',
     ['delete', 'blah'],
     {'stderr': 'Connection name "blah" does not exist',
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server and --server together fail.',
     ['add', 'fred', '--mock-server', 'test1.mof', '--server', 'http://blah'],
     {'stderr': ['Add failed',
                 '"--server" and "--mock-server" are mutuallly exclusive'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    #
    # The following tests are a sequence. Each depends on the previous
    # and what was in the repository when each test is executed.
    #
    ['Verify connection subcommand add with simple arguments only.',
     ['add', 'test1', '-s', 'http://blah'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand show',
     ['show', 'test1'],
     {'stdout': [
         "name: test1", "  server: http://blah",
         "  default-namespace: root/cimv2", "  user: None", "  password: None",
         "  timeout: 30", "  no-verify: False", "  certfile: None",
         "  keyfile: None", "  use-pull: None", "  mock-server:",
         "  log: None"],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand add with complex options',
     ['add', 'test2', '-s', 'http://blahblah', '-u', 'fred', '-p',
      'argh', '-t', '18', '-N', '-l', 'api=file,all'],
     {'stdout': "",
      'test': 'regex',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand show  ',
     ['show', 'test1'],
     {'stdout': [
         "name: test1", "  server: http://blah",
         "  default-namespace: root/cimv2", "  user: None", "  password: None",
         "  timeout: 30", "  no-verify: False", "  certfile: None",
         "  keyfile: None", "  use-pull: None", "  mock-server:",
         "  log: None"],
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand show  ',
     ['show', 'test2'],
     {'stdout': [
         "name: test2", "  server: http://blahblah",
         "  default-namespace: root/cimv2", "  user: fred", "  password: argh",
         "  timeout: 18", "  no-verify: True", "  certfile: None",
         "  keyfile: None", "  use-pull: None", "  mock-server:",
         "  log: api=file,all"],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand list with 2 servers defined',
     {'global': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections:',
                 'name    server namespace user timeout no-verify    log',
                 "test1   http://blah      root/cimv2         30  False",
                 "test2   http://blahblah  root/cimv2   fred  18  True "
                 "api=file,all"],
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand select test2',
     ['select', 'test2', '--default'],
     {'stdout': ['test2', 'default'],
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand show test2 includes "current"',
     ['show', 'test2'],
     {'stdout': ['test2', 'http://blahblah', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand select test2 shows it is current',
     ['select', 'test2'],
     {'stdout': ['test2', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand select test3 fails',
     ['select', 'test9'],
     {'stderr': ['Connection name "test9" does not exist'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify connection subcommand list with 2 servers defined, not sel after '
     ' next pywbemcli call',
     {'global': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections:',
                 '(#: default, *: current)',
                 'name    server namespace user timeout no-verify    log',
                 'test1   http://blah      root/cimv2        30  False',
                 '*#test2   http://blahblah  root/cimv2   fred 18  True '
                 'api=file,all'],
      'test': 'insnows'},
     None, OK],

    ['Verify connection subcommand delete test1',
     ['delete', 'test1'],
     {'stdout': ['Deleted', 'test1'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand test',
     ['test'],
     {'stdout': "Connection successful",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify connection subcommand delete test2',
     ['delete', 'test2'],
     {'stdout': ['Deleted', 'test2', 'connection'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    ['Verify connection subcommand list empty repository.',
     {'global': ['-o', 'simple'],
      'args': ['list']},
     {'stdout': [
         "WBEM server connections:", ""],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},

     None, OK],

    #
    #   The following is a new sequence but depends on the repo being empty
    #   It creates, shows and deletes a single server definition.
    #
    ['Verify connection subcommand add with all arguments.',
     ['add', 'addallargs',
      '--server', 'http://blah',
      '--default-namespace', 'root/blah',
      '--user', 'john',
      '--password', 'pw',
      '--timeout', '30',
      '--no-verify',
      '--certfile', 'mycertfile.pem',
      '--keyfile', 'mykeyfile.pem', ],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand with duplicate name fails.',
     ['add', 'addallargs',
      '--server', 'http://blah',
      '--default-namespace', 'root/blah',
      '--user', 'john',
      '--password', 'pw',
      '--timeout', '30',
      '--no-verify',
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
         'name: addallargs',
         '  server: http://blah',
         '  default-namespace: root/blah',
         '  user: john',
         '  password: pw',
         '  certfile: mycertfile.pem',
         '  keyfile: mykeyfile.pem',
         '  use-pull: None',
         '  pull-max-cnt: 1000',
         '  mock-server: ',
         '  log: None'],
      'test': 'in'},
     None, OK],

    ['Verify connection subcommand delete addallargs',
     ['delete', 'addallargs'],
     {'stdout': "Deleted",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
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
                 'PYWBEMCLI_NO_VERIFY=True$',
                 'PYWBEMCLI_CERTFILE=certfile.txt$',
                 'PYWBEMCLI_KEYFILE=keyfile.txt$',
                 # account for windows and non_windows platforms
                 '^(export|set) '],
      'test': 'regex',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    #
    #  Test command line parameter errors
    #
    ['Verify connection subcommand select with name not in repo',
     ['show', 'Blah'],
     {'stderr': ['Connection name "Blah" does not exist'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand select with no name empty repo',
     ['show', 'Blah'],
     {'stderr': ['Connection name "Blah" does not exist'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify connection subcommand add with bad arg fails',
     ['add', 'addallargs', '-s', 'http://blah',
      '--timeout', 'fred', ],
     {'stderr': ['Usage: pywbemcli connection add [COMMAND-OPTIONS]',
                 'Error: Invalid value for "-t" / "--timeout": '
                 'fred is not a valid integer'],
      'rc': 2,
      'test': 'in',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection subcommand add no server option fails, no --server',
     ['add', 'blah'],
     {'stderr': ['Add failed',
                 'missing server definition',
                 '"--server" or "--mock-server" required'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify connection subcommand fails, no NAME argument.',
     ['add',
      '--server', 'http://strangename',
      '--default-namespace', 'root/blah',
      '--user', 'john',
      '--password', 'pw',
      '--timeout', '30',
      '--no-verify',
      '--certfile', 'mycertfile.pem',
      '--keyfile', 'mykeyfile.pem', ],
     {'stderr': ['Usage: pywbemcli connection add [COMMAND-OPTIONS] NAME',
                 'Missing argument "NAME".'],
      'rc': 2,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection subcommand select, empty repo fails',
     ['select'],
     {'stderr': ["Connection repository", "empty"],
      'rc': 1,
      'test': 'regex',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection subcommand delete, empty repo fails',
     ['delete'],
     {'stderr': ["Connection repository", "empty"],
      'rc': 1,
      'test': 'regex',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    #
    #  Verify create and save mock connection sequence. Starts with empty
    #  server adds a mock server, shows it, tests if valid, and deletes
    #  the connection
    #

    ['Verify mock connection exists.',
     ['add', 'mocktest', '--mock-server', MOCK_FILE_PATH],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand shows mock file ',
     ['show', 'mocktest'],
     {'stdout': [
         "name: mocktest",
         "  default-namespace: root/cimv2",
         "  user: None", "  password: None",
         "  timeout: 30",
         "  no-verify: False", "  certfile: None",
         "  keyfile: None", "  use-pull: None",
         r"  mock-server:", r"simple_mock_model.mof",
         "  log: None"],
      'test': 'regex'},
     None, OK],

    ['Verify connection subcommand test against existing mock def',
     {'args': ['test'],
      'global': ['--name', 'mocktest']},
     {'stdout': "Connection successful",
      'test': 'lines'},
     None, OK],

    ['Verify connection subcommand select mocktest with prompt',
     ['select'],
     {'stdout': "",
      'test': 'in',
      'file': {'before': 'exists', 'after': 'exists'}},
     MOCK_PROMPT0_FILE, OK],

    ['Verify connection subcommand delete with prompt that selects 0',
     ['delete', ],
     {'stdout': ['Select a connection or Ctrl_C to abort',
                 '0: mocktest',
                 'Input integer between 0 and 0 or Ctrl-C to exit selection:'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     MOCK_PROMPT0_FILE, OK],

    ['Verify Add mock server to empty connections file.',
     ['add', 'mocktest', '--mock-server', MOCK_FILE_PATH],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand delete with prompt that selects y for '
     'verify',
     ['delete', 'mocktest', '--verify'],
     {'stdout': ['name: mocktest', 'Execute delete'],
      'test': 'regex',
      'file': {'before': 'exists', 'after': 'none'}},
     MOCK_CONFIRMY_FILE, OK],

    #
    #  Verify Create from mock with cmd line params, save, show, delete works
    #  The following is a sequence of tests that must be run in order
    #  The following test is artifical in that the first create actually
    #  uses the mock but not to really create a server
    #
    ['Verify save server with cmd line params to empty connections file. Using '
     '--verify',
     {'args': ['save', '--verify', 'svrtest2'],
      'global': ['--server', 'http://blah',
                 '--timeout', '45',
                 '--use-pull', 'no',
                 '--default-namespace', 'root/blah',
                 '--user', 'john',
                 '--password', 'pw',
                 '--no-verify',
                 '--certfile', 'mycertfile.pem',
                 '--keyfile', 'mykeyfile.pem']},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'exists'}},
     MOCK_CONFIRMY_FILE, OK],

    ['Verify save mock server with cmd line params to empty connections file.',
     {'args': ['save', 'mocktest2'],
      'global': ['--mock-server', MOCK_FILE_PATH,
                 '--timeout', '45',
                 '--use-pull', 'no',
                 '--default-namespace', 'root/blah',
                 '--user', 'john',
                 '--password', 'pw',
                 '--no-verify',
                 '--certfile', 'mycertfile.pem',
                 '--keyfile', 'mykeyfile.pem']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand shows mock file ',
     ['show', 'mocktest2'],
     {'stdout': [
         "name: mocktest2",
         "  default-namespace: root/blah", "  user: john", "  password: pw",
         "  timeout: 45", "  no-verify: True", "  certfile: mycertfile.pem",
         "  keyfile: mykeyfile.pem", "  use-pull: False",
         r"  mock-server:", "simple_mock_model.mof",
         "  log: None"],
      'test': 'regex',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand shows svrtest2 ',
     ['show', 'svrtest2'],
     {'stdout': [
         "name: svrtest2",
         "  server: http://blah",
         "  default-namespace: root/blah", "  user: john", "  password: pw",
         "  timeout: 45", "  no-verify: True", "  certfile: mycertfile.pem",
         "  keyfile: mykeyfile.pem", "  use-pull: False",
         "  log: None"],
      'test': 'in',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand delete works',
     ['delete', 'mocktest2'],
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection subcommand delete works and file empty',
     ['delete', 'svrtest2'],
     {'stderr': "",
      'rc': 0,
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    #
    #  Test select variations
    #

    ['Verify connection show with just current server defined by --server',
     {'args': ['show'],
      'global': ['--server', 'http://blah']},
     {'stdout': ['name', 'not-saved'],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection list with current server from general options',
     {'args': ['list'],
      'global': ['--server', 'http://blah']},
     {'stdout': """
WBEM server connections: (#: default, *: current)
+------------+-------------+-------------+-----------+-------------+
| name       | server      | namespace   |   timeout | no-verify   |
|------------+-------------+-------------+-----------+-------------|
| *not-saved | http://blah | root/cimv2  |        30 | False       |
+------------+-------------+-------------+-----------+-------------+
""",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    #
    #  Sequence to test
    #

    ['Verify mock connection exists.',
     ['add', 'svrtest', '--server', 'http://blah'],
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],


    ['Verify connection list with current server from general options',
     {'args': ['list'],
      'global': ['--server', 'http://blah']},
     {'stdout':
      ['WBEM server connections: (#: default, *: current)',
       '+------------+-------------+-------------+-----------+-------------+',
       '| name       | server      | namespace   |   timeout | no-verify   |',
       '|------------+-------------+-------------+-----------+-------------|',
       '| *not-saved | http://blah | root/cimv2  |        30 | False       |',
       '| svrtest    | http://blah | root/cimv2  |        30 | False       |',
       '+------------+-------------+-------------+-----------+-------------+'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection select of svrtest',
     {'args': ['select', 'svrtest', '--default'],
      'global': ['--server', 'http://blah']},
     {'stdout': '"svrtest" default and current',
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection select of mocktest',
     {'args': ['list'],
      'global': ['--server', 'http://blah']},
     {'stdout':
      ['WBEM server connections: (#: default, *: current)',
       '+------------+-------------+-------------+-----------+-------------+',
       '| name       | server      | namespace   |   timeout | no-verify   |',
       '|------------+-------------+-------------+-----------+-------------|',
       '| *not-saved | http://blah | root/cimv2  |        30 | False       |',
       '| #svrtest   | http://blah | root/cimv2  |        30 | False       |',
       '+------------+-------------+-------------+-----------+-------------+'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],


    ['Verify connection delete svrtest',
     {'args': ['delete', 'svrtest'],
      'global': []},
     {'stdout': "Deleted default connection",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

]


class TestSubcmdClass(CLITestsBase):
    """
    Test all of the class command variations.
    """
    subcmd = 'connection'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_connection(self, desc, inputs, exp_response, mock, condition,
                        repo_file_path):
        """
        Common test method for those subcommands and options in the
        class subcmd that can be tested.  Note the
        fixture remove_connection_file which is session, autouse so should
        hide any existing connection file at beginning of this test and
        restore it after the test.
        """
        # Where is this file to be located for tests.
        pywbemserversfile = repo_file_path

        def test_file(file_test):
            """
            Local function to execute tests on existence of connections file.
            """
            if file_test == 'exists':
                assert os.path.isfile(pywbemserversfile) and \
                    os.path.getsize(pywbemserversfile) > 0, \
                    "Fail. File  %s should exist" % pywbemserversfile
            elif file_test == 'none':
                if os.path.isfile(pywbemserversfile):
                    print('FILE THAT SHOULD NOT EXIST')
                    with open(pywbemserversfile, 'r') as fin:
                        print(fin.read())

                assert not os.path.isfile(pywbemserversfile), \
                    "Fail. File %s should not exist" % pywbemserversfile

            else:
                assert False, 'File test option name %s invalid' % file_test

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
