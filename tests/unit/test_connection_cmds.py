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
Test the connection command group and its commands. This test manipulates
a connections file in the test directory.  It assumes that the
test directory is the same as the current working directory where pywbemcli
was called.  If there is a connections file at the start of the test it is
renamed for the test and restored at the end of the test.
"""

import os
import pytest

from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE

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
    'delete  Delete a WBEM connection definition.',
    'export  Export the current connection.',
    'list    List the WBEM connection definitions.',
    'save    Save the current connection to a new WBEM connection definition.',
    'select  Select a WBEM connection definition as current or default.',
    'show    Show a WBEM connection definition or the current connection.',
    'test    Test the current connection with a predefined WBEM request.',
]

CONNECTION_DELETE_HELP_LINES = [
    'Usage: pywbemcli connection delete [COMMAND-OPTIONS] NAME',
    'Delete a WBEM connection definition.',
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
    'Show a WBEM connection definition or the current connection.',
    '--show-password  If set, show existing password in results.',
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
    # inputs - String, or list of args or dict of 'env', 'args', 'general',
    #          and 'stdin'. See See CLITestsBase.command_test()  for
    #          detailed documentation
    # exp_response - Dictionary of expected responses (stdout, stderr, rc) and
    #                test definition (test: <testname>).
    #                See CLITestsBase.command_test() for detailed documentation.
    # mock - None or name of files (mof or .py),
    # condition - If True the test is executed, if 'pdb' the test breaks in
    #             the debugger, otherwise the test is skipped.

    ['Verify connection command --help response',
     '--help',
     {'stdout': CONNECTION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command -h response',
     '-h',
     {'stdout': CONNECTION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command delete --help response',
     ['delete', '--help'],
     {'stdout': CONNECTION_DELETE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command delete -h response',
     ['delete', '-h'],
     {'stdout': CONNECTION_DELETE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command export --help response',
     ['export', '--help'],
     {'stdout': CONNECTION_EXPORT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command export -h response',
     ['export', '-h'],
     {'stdout': CONNECTION_EXPORT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command list --help response',
     ['list', '--help'],
     {'stdout': CONNECTION_LIST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command list -h response',
     ['list', '-h'],
     {'stdout': CONNECTION_LIST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command save --help response',
     ['save', '--help'],
     {'stdout': CONNECTION_SAVE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command save -h response',
     ['save', '-h'],
     {'stdout': CONNECTION_SAVE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command select  --help response',
     ['select', '--help'],
     {'stdout': CONNECTION_SELECT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command select  -h response',
     ['select', '-h'],
     {'stdout': CONNECTION_SELECT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command show --help response',
     ['show', '--help'],
     {'stdout': CONNECTION_SHOW_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command show -h response',
     ['show', '-h'],
     {'stdout': CONNECTION_SHOW_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command test --help response',
     ['test', '--help'],
     {'stdout': CONNECTION_TEST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command test -h response',
     ['test', '-h'],
     {'stdout': CONNECTION_TEST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command list empty repository.',
     {'general': ['-o', 'simple'],
      'args': ['list']},
     {'stdout': [
         "WBEM server connections:", ""],
      'test': 'innows'},
     None, OK],

    ['Verify connection command delete, empty repo fails.',
     ['delete', 'blah'],
     {'stderr': ["Connection repository", "empty"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server and --server together fail.',
     {'general': ['--mock-server', MOCK_FILE_PATH, '--server', 'http://blah'],
      'args': ['list']},
     {'stderr': ['Conflicting server definitions:',
                 'server:', 'http://blah',
                 'mock-server:', MOCK_FILE_PATH],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    #
    # The following tests are a sequence. Each depends on the previous
    # and what was in the repository when each test is executed.
    #
    ['Verify connection command save creates file.',
     {'general': ['--server', 'http://blah'],
      'args': ['save', 'test1']},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show of just created test1',
     ['show', 'test1'],
     {'stdout': [
         "name: test1", "  server: http://blah",
         "default-namespace: root/cimv2", "  user: None",
         "password: None",
         "timeout: 30",
         "verify: True",
         "certfile: None",
         "keyfile: None", "  mock-server:"],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command save with complex general options short',
     {'general': ['--server', 'http://blahblah', '-u', 'fred', '-p',
                  'argh', '-t', '18', '--no-verify', '-l', 'api=file,all'],
      'args': ['save', 'test2']},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show named connnection test1',
     ['show', 'test1'],
     {'stdout': [
         "name: test1", "  server: http://blah",
         "default-namespace: root/cimv2", "user: None", "password: None",
         "timeout: 30",
         "verify: True",
         "certfile: None",
         "keyfile: None", "mock-server:"],
      'test': 'innows'},
     None, OK],

    ['Verify connection command show  test2 with --show-password',
     ['show', 'test2', '--show-password'],
     {'stdout': ['name: test2',
                 'server: http://blahblah',
                 'default-namespace: root/cimv2',
                 'user: fred',
                 'password: argh',
                 'timeout: 18',
                 'verify: False',
                 'certfile: None',
                 'keyfile: None',
                 'mock-server:'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command show  test2, masked password',
     ['show', 'test2'],
     {'stdout': ['name: test2',
                 'server: http://blahblah',
                 'default-namespace: root/cimv2',
                 'user: fred',
                 'password: ****',
                 'timeout: 18',
                 'verify: False',
                 'certfile: None',
                 'keyfile: None',
                 'mock-server:'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command list with 2 servers defined',
     {'general': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections:',
                 'name server namespace user timeout verify',
                 "test1 http://blah root/cimv2 30  True",
                 "test2 http://blahblah  root/cimv2 fred 18  False"],
      'test': 'innows'},
     None, OK],

    ['Verify connection command select test2',
     ['select', 'test2', '--default'],
     {'stdout': ['test2', 'default'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command show test2 includes "current"',
     ['show', 'test2'],
     {'stdout': ['test2', 'http://blahblah', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command select test2 shows it is current',
     ['select', 'test2'],
     {'stdout': ['test2', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command select test3 fails',
     ['select', 'test9'],
     {'stderr': ['Connection name "test9" does not exist'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify connection command list with 2 servers defined, not sel after '
     ' next pywbemcli call',
     {'general': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections:',
                 '(#: default, *: current)',
                 'name    server namespace user timeout verify log',
                 'test1   http://blah      root/cimv2        30  True',
                 '*#test2   http://blahblah  root/cimv2   fred 18  False'
                 'api=file,all'],
      'test': 'insnows'},
     None, OK],

    ['Verify connection command delete test1',
     ['delete', 'test1'],
     {'stdout': ['Deleted', 'test1'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command test',
     ['test'],
     {'stdout': "Connection successful",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify connection command delete test2',
     ['delete', 'test2'],
     {'stdout': ['Deleted', 'test2', 'connection'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    ['Verify connection command list empty repository.',
     {'general': ['-o', 'simple'],
      'args': ['list']},
     {'stdout': [
         "WBEM server connections:", ""],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},

     None, OK],

    #
    # The following tests are a new sequence and depends on empty repo.
    # It creates, shows and deletes a single server definition.
    #
    ['Verify connection command add with all arguments.',
     {'general': ['--server', 'http://blahblah',
                  '--default-namespace', 'root/blahblah',
                  '--user', 'john',
                  '--password', 'pw',
                  '--timeout', '30',
                  '--no-verify',
                  '--certfile', 'mycertfile.pem',
                  '--keyfile', 'mykeyfile.pem', ],
      'args': ['save', 'addallargs']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show addallargs initial version',
     ['show', 'addallargs'],
     {'stdout': [
         'name: addallargs',
         '  server: http://blahblah',
         '  default-namespace: root/blahblah',
         '  user: john',
         '  password: ******',
         '  certfile: mycertfile.pem',
         '  keyfile: mykeyfile.pem',
         '  mock-server: '],
      'test': 'in'},
     None, OK],

    ['Verify connection command with that overwrites existing name works.',
     {'general': ['--server', 'http://blah',
                  '--default-namespace', 'root/blah',
                  '--user', 'john',
                  '--password', 'pw',
                  '--timeout', '30',
                  '--no-verify',
                  '--certfile', 'mycertfile.pem',
                  '--keyfile', 'mykeyfile.pem', ],
      'args': ['save', 'addallargs']},
     {'stderr': '',
      'rc': 0,
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show of name addallargs, overwrite changed',
     ['show', 'addallargs', '--show-password'],
     {'stdout': [
         'name: addallargs',
         '  server: http://blah',
         '  default-namespace: root/blah',
         '  user: john',
         '  password: pw',
         '  certfile: mycertfile.pem',
         '  keyfile: mykeyfile.pem',
         '  mock-server: '],
      'test': 'in'},
     None, OK],

    ['Verify connection command delete addallargs',
     ['delete', 'addallargs'],
     {'stdout': "Deleted",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    # uses regex because windows generates set and linux export in statements
    # No file verification required. Does not use file
    ['Verify connection command export current connection',
     {'args': ['export'],
      'general': ['-s', 'http://blah', '-u', 'fred', '-p', 'arghh',
                  '--no-verify',
                  '-c', 'certfile.txt', '-k', 'keyfile.txt', '-t', '12']},
     {'stdout': ['PYWBEMCLI_SERVER=http://blah$',
                 'PYWBEMCLI_DEFAULT_NAMESPACE=root/cimv2$',
                 'PYWBEMCLI_USER=fred$',
                 'PYWBEMCLI_PASSWORD=arghh$',
                 'PYWBEMCLI_TIMEOUT=12$',
                 #   TODO 'PYWBEMCLI_NO_VERIFY=True$',
                 'PYWBEMCLI_CERTFILE=certfile.txt$',
                 'PYWBEMCLI_KEYFILE=keyfile.txt$',
                 # account for windows and non_windows platforms
                 '^(export|set) '],
      'test': 'regex',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command export no current conection',
     {'args': ['export'],
      'general': []},
     {'stderr': ['No server currently defined as current'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    #
    #  Test command line parameter errors, select, show, and delete with
    #  no repository
    #
    ['Verify connection command show with name not in empty repo',
     ['show', 'Blah'],
     {'stderr': ['Name "Blah" not current and no connections file'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command show with no name empty repo',
     ['show'],
     {'stderr': ['No current connection and no connections file'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify connection command select, empty repo fails',
     ['select'],
     {'stderr': ["Connection repository", "empty"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command select blah, empty repo fails',
     ['select', 'blah'],
     {'stderr': ["Connection repository", "empty"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command delete, empty repo fails',
     ['delete'],
     {'stderr': ["Connection repository", "empty"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],


    ['Verify connection command delete, empty repo fails',
     ['delete', 'blah'],
     {'stderr': ["Connection repository", "empty"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    #  The following is a sequence that starts with an empty repo
    #  Verify create and save mock connection sequence. Starts with empty
    #  server adds a mock server, shows it, tests if valid, and deletes
    #  the connection
    #

    ['Verify mock connection exists.',
     {'general': ['--mock-server', MOCK_FILE_PATH],
      'args': ['save', 'mocktest']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command shows mock file ',
     ['show', 'mocktest'],
     {'stdout': [
         "name: mocktest",
         "default-namespace: root/cimv2",
         "user: None",
         "password: None",
         "timeout: 30",
         "verify: True",
         "certfile: None",
         "keyfile: None",
         "mock-server:", r"simple_mock_model.mof"],
      'test': 'innows'},
     None, OK],

    ['Verify connection command test against existing mock def',
     {'args': ['test'],
      'general': ['--name', 'mocktest']},
     {'stdout': "Connection successful",
      'test': 'linnows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command select mocktest with prompt',
     ['select'],
     {'stdout': "",
      'test': 'in',
      'file': {'before': 'exists', 'after': 'exists'}},
     MOCK_PROMPT0_FILE, OK],


    ['Verify connection command show with prompt',
     ['show', '?'],
     {'stdout': ['name: mocktest'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     MOCK_PROMPT0_FILE, OK],

    ['Verify connection command delete with prompt that selects 0',
     ['delete', ],
     {'stdout': ['Select a connection or Ctrl_C to abort',
                 '0: mocktest',
                 'Input integer between 0 and 0 or Ctrl-C to exit selection:'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     MOCK_PROMPT0_FILE, OK],

    ['Verify Add mock server to empty connections file.',
     {'general': ['--mock-server', MOCK_FILE_PATH],
      'args': ['save', 'mocktest']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command delete'
     'verify',
     ['delete', 'mocktest'],
     {'stdout': ['name: mocktest', 'Execute delete'],
      'test': 'onnows',
      'file': {'before': 'exists', 'after': 'none'}},
     MOCK_CONFIRMY_FILE, OK],

    #
    #  Verify Create from mock with cmd line params, save, show, delete works
    #  The following is a sequence of tests that must be run in order
    #  The following test is artifical in that the first create actually
    #  uses the mock but not to really create a server
    #
    ['Verify save server with cmd line params to empty connections file.',
     {'args': ['save', 'svrtest2'],
      'general': ['--server', 'http://blah',
                  '--timeout', '45',
                  '--use-pull', 'no',
                  '--default-namespace', 'root/blah',
                  '--user', 'john',
                  '--password', 'pw',
                  '--verify',
                  '--certfile', 'mycertfile.pem',
                  '--keyfile', 'mykeyfile.pem']},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'exists'}},
     MOCK_CONFIRMY_FILE, OK],

    ['Verify save mock server with cmd line params to empty connections file.',
     {'args': ['save', 'mocktest2'],
      'general': ['--mock-server', MOCK_FILE_PATH,
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

    ['Verify connection command shows mock file ',
     ['show', 'mocktest2'],
     {'stdout': [
         "name: mocktest2",
         "default-namespace: root/blah",
         "user: john",
         "password: **",
         "timeout: 45",
         "verify: False",
         "certfile: mycertfile.pem",
         "keyfile: mykeyfile.pem",
         "mock-server:", "simple_mock_model.mof"],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command shows svrtest2 ',
     ['show', 'svrtest2'],
     {'stdout': [
         "name: svrtest2",
         "server: http://blah",
         "default-namespace: root/blah", "user: john",
         "password: **",
         "timeout: 45",
         "verify: True",
         "certfile: mycertfile.pem",
         "keyfile: mykeyfile.pem"],
      'test': 'in',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command delete works',
     ['delete', 'mocktest2'],
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command delete works and file empty',
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
      'general': ['--server', 'http://blah']},
     {'stdout': ['name', 'not-saved'],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection list with current server from general options, plain',
     {'args': ['list'],
      'general': ['--server', 'http://blah', '--output-format', 'plain']},
     {'stdout': ['WBEM server connections: (#: default, *: current)',
                 '*not-saved http://blah root/cimv2  30 True'],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    #
    #  Sequence to test
    #

    ['Verify Create new connection names svrtest works.',
     {'general': ['--server', 'http://blah'],
      'args': ['save', 'svrtest']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection list with current server from general options, grid',
     {'args': ['list'],
      'general': ['--server', 'http://blah']},
     {'stdout': """
WBEM server connections: (#: default, *: current)
+------------+-------------+-------------+-----------+----------+
| name       | server      | namespace   |   timeout | verify   |
|------------+-------------+-------------+-----------+----------|
| *not-saved | http://blah | root/cimv2  |        30 | True     |
| svrtest    | http://blah | root/cimv2  |        30 | True     |
+------------+-------------+-------------+-----------+----------+
""",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection select of svrtest',
     {'args': ['select', 'svrtest', '--default'],
      'general': ['--server', 'http://blah']},
     {'stdout': '"svrtest" default and current',
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection select of svrtest as default',
     {'args': ['show'],
      'general': []},
     {'stdout': ['svrtest'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify current connection set with general opts overrides default',
     {'args': ['show'],
      'general': ['--server', 'https://blahblahblah']},
     {'stdout': ['not-saved', 'https://blahblahblah'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection delete svrtest',
     {'args': ['delete', 'svrtest'],
      'general': []},
     {'stdout': "Deleted default connection",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    #
    #   Test creating a server and saving it from stdin all in single
    #   interactive sequence
    #
    ['Verify Create new connection in interactive mode and delete.',
     {'general': [],
      'stdin': ['--server http://blah --user fred --password fred '
                '--certfile cert1.pem --keyfile keys1.pem',
                'connection save fred',
                'connection show',
                'connection delete fred']},
     {'stdout': ['name', 'not-saved',
                 'server', 'http://blah',
                 'default-namespace', 'root/cimv2',
                 'user',
                 'fred',
                 'password',
                 'timeout', '30',
                 'verify', 'True',
                 'certfile', 'cert1.pem',
                 'keyfile', 'keys1.pem',
                 'Deleted', 'connection', '"fred"'],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    #
    # The following is a sequence to assure that the interactive creation
    # of a server actually puts the server in the repository
    #
    ['Verify Create new connection in interactive mode and delete.',
     {'general': [],
      'stdin': ['--server http://blah --user fred --password fred '
                '--certfile cert1.pem --keyfile keys1.pem',
                'connection save fred',
                'connection show']},
     {'stdout': ['name', 'not-saved',
                 'server', 'http://blah',
                 'default-namespace', 'root/cimv2',
                 'user',
                 'fred',
                 'password',
                 'timeout', '30',
                 'verify', 'True',
                 'certfile', 'cert1.pem',
                 'keyfile', 'keys1.pem'],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection delete fred',
     {'args': ['delete', 'fred'],
      'general': []},
     {'stdout': 'Deleted connection "fred"',
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    #
    #   The following is a sequence. Confirm fix to issue #396
    #
    ['Create mock server defintion.',
     {'args': ['save', 'mocktest3'],
      'general': ['--mock-server', MOCK_FILE_PATH]},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify sequence select, list, create new and save, list works.',
     {'general': [],
      'stdin': ['connection select mocktest3',
                'connection list',
                '--server http://blah --user fred --password fred '
                '--certfile cert1.pem connection save testconn',
                'connection connection list',
                'connection select testconn',
                'connection delete testconn',
                'connection delete mocktest3']},
     {'stdout': ['Deleted connection "mocktest3"'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'None'}},
     None, OK],

]


class TestSubcmdClass(CLITestsBase):
    """
    Test all of the class command variations.
    """
    command_group = 'connection'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_connection(self, desc, inputs, exp_response, mock, condition,
                        repo_file_path):
        """
        Common test method for those commands and options in the
        connection command group that can be tested.  Note the
        fixture remove_connection_file which is session, autouse so should
        hide any existing connection file at beginning of this test and
        restore it after the test.
        """
        # Where is this file to be located for tests.
        pywbemserversfile = repo_file_path

        def test_file_existence(file_test):
            """
            Local function to execute tests on existence of connections file.
            """
            if file_test == 'exists':
                assert os.path.isfile(pywbemserversfile) and \
                    os.path.getsize(pywbemserversfile) > 0, \
                    "Fail. File  %s should exist" % pywbemserversfile
            elif file_test.lower() == 'none':
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
            import pdb  # pylint: disable=import-outside-toplevel
            pdb.set_trace()

        if 'file' in exp_response:
            if 'before' in exp_response['file']:
                test_file_existence(exp_response['file']['before'])

        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition, verbose=False)

        if 'file' in exp_response:
            if 'after' in exp_response['file']:
                test_file_existence(exp_response['file']['after'])
