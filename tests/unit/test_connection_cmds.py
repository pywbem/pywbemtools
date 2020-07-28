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

from __future__ import absolute_import, print_function

import os
import pytest

from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE

SCRIPT_DIR = os.path.dirname(__file__)

# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
ONE_CLASS_MOCK_FILE = 'one_class_mock.mof'
INVOKE_METHOD_MOCK_FILE = 'simple_mock_invokemethod.py'
MOCK_PROMPT_0_FILE = "mock_prompt_0.py"

TEST_DIR = os.path.dirname(__file__)

# Get the relative path to the current directory.  This presumes that the
# test was run from the pywbemtools directory
TEST_DIR_REL = os.path.relpath(TEST_DIR)
MOCK_FILE_PATH = os.path.join(TEST_DIR_REL, SIMPLE_MOCK_FILE)

CONNECTION_HELP_LINES = [
    # pylint: disable=line-too-long
    'Usage: pywbemcli [GENERAL-OPTIONS] connection COMMAND [ARGS] [COMMAND-OPTIONS]',  # noqa: E501
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
    'Usage: pywbemcli [GENERAL-OPTIONS] connection delete NAME '
    '[COMMAND-OPTIONS]',
    'Delete a WBEM connection definition.',
    CMD_OPTION_HELP_HELP_LINE,
]

CONNECTION_EXPORT_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] connection export [COMMAND-OPTIONS]',
    'Export the current connection.',
    CMD_OPTION_HELP_HELP_LINE,
]

CONNECTION_LIST_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] connection list [COMMAND-OPTIONS]',
    'List the WBEM connection definitions.',
    '-f, --full  If set, display the full table. Otherwise display  a brief',
    CMD_OPTION_HELP_HELP_LINE,
]

CONNECTION_SAVE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] connection save NAME [COMMAND-OPTIONS]',
    'Save the current connection to a new WBEM connection definition.',
    CMD_OPTION_HELP_HELP_LINE,
]

CONNECTION_SELECT_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] connection select NAME '
    '[COMMAND-OPTIONS]',
    'Select a WBEM connection definition as current or default.',
    '-d, --default  If set, the connection is set to be the default ',
    CMD_OPTION_HELP_HELP_LINE,
]

CONNECTION_SHOW_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] connection show NAME [COMMAND-OPTIONS]',
    'Show a WBEM connection definition or the current connection.',
    '--show-password  If set, show existing password in results.',
    CMD_OPTION_HELP_HELP_LINE,
]

CONNECTION_TEST_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] connection test [COMMAND-OPTIONS]',
    'Test the current connection with a predefined WBEM request.',
    CMD_OPTION_HELP_HELP_LINE,
]

OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet

# Note: Some test cases are sequences, where each test case depends on the
# previous test case and what was in the repository when each test is executed.
# The sequences always start and end with an empty repository, and are marked
# with "Begin of sequence" and "End of sequence".


TEST_CASES = [

    # List of testcases.
    # Each testcase is a list with the following items:
    # * desc: Description of testcase.
    # * inputs: String, or tuple/list of strings, or dict of 'env', 'args',
    #     'general', and 'stdin'. See the 'inputs' parameter of
    #     CLITestsBase.command_test() in cli_test_extensions.py for detailed
    #     documentation.
    # * exp_response: Dictionary of expected responses (stdout, stderr, rc) and
    #     test definition (test: <testname>). See the 'exp_response' parameter
    #     of CLITestsBase.command_test() in cli_test_extensions.py for
    #     detailed documentation.
    # * mock: None, name of file (.mof or .py), or list thereof.
    # * condition: If True the test is executed, if 'pdb' the test breaks in the
    #     the debugger, if 'verbose' print verbose messages, if False the test
    #     is skipped.

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
     {'general': [],
      'args': ['test', '-h']},
     {'stdout': CONNECTION_TEST_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command list empty repository.',
     {'general': ['-o', 'simple'],
      'args': ['list']},
     {'stdout': [
         "WBEM server connections(brief):", ""],
      'test': 'innows'},
     None, OK],

    ['Verify connection command delete, empty repo fails.',
     {'general': [],
      'args': ['delete', 'blah']},
     {'stderr': ["Connection repository", "does not exist"],
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
    # This sequence creates a simple server named test1 and tests the
    # display, etc. of that persisted server name
    #

    # Begin of sequence - repository is empty.

    ['Verify connection command save creates file.',
     {'general': ['--server', 'http://blah'],
      'args': ['save', 'test1']},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show of just created test1',
     {'general': [],
      'args': ['show', 'test1']},
     {'stdout': """Connection status:
name               value  (state)
-----------------  ----------------
name               test1
server             http://blah
default-namespace  root/cimv2
user
password
timeout            30
use-pull
verify             True
certfile
keyfile
mock-server
ca-certs
""",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show of just created test1 as table',
     {'general': ['--output-format', 'plain'],
      'args': ['show', 'test1']},
     {'stdout': """Connection status:
name               value  (state)
name               test1
server             http://blah
default-namespace  root/cimv2
user
password
timeout            30
use-pull
verify             True
certfile
keyfile
mock-server
ca-certs
""",
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
     {'general': [],
      'args': ['show', 'test1']},
     {'stdout': """Connection status:
name               value  (state)
-----------------  ----------------
name               test1
server             http://blah
default-namespace  root/cimv2
user
password
timeout            30
use-pull
verify             True
certfile
keyfile
mock-server
ca-certs
""",
      'test': 'innows'},
     None, OK],

    ['Verify connection command show test2 with --show-password',
     {'general': [],
      'args': ['show', 'test2', '--show-password']},
     {'stdout': """Connection status:
name               value  (state)
-----------------  ----------------
name               test2
server             http://blahblah
default-namespace  root/cimv2
user               fred
password           argh
timeout            18
use-pull
verify             False
certfile
keyfile
mock-server
ca-certs
""",
      'test': 'innows'},
     None, OK],

    ['Verify connection command show test2, masked password',
     {'general': [],
      'args': ['show', 'test2']},
     {'stdout': """Connection status:
name               value  (state)
-----------------  ----------------
name               test2
server             http://blahblah
default-namespace  root/cimv2
user               fred
password           ******
timeout            18
use-pull
verify             False
certfile
keyfile
mock-server
ca-certs
""",
      'test': 'innows'},
     None, OK],

    ['Verify connection command list with 2 servers defined',
     {'general': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections(brief): (#: default, *: current)',
                 'name    server           mock-server',
                 'test1   http://blah',
                 'test2   http://blahblah'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command select test2',
     {'general': [],
      'args': ['select', 'test2', '--default']},
     {'stdout': ['test2', 'default'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command show test2 includes "current"',
     {'general': [],
      'args': ['show', 'test2']},
     {'stdout': ['test2', 'http://blahblah', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command select test2 shows it is current',
     {'general': [],
      'args': ['select', 'test2']},
     {'stdout': ['test2', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command select test3 fails',
     {'general': [],
      'args': ['select', 'test9']},
     {'stderr': ['Connection name "test9" does not exist'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify connection command list with 2 servers defined, not sel after '
     'next pywbemcli call',
     {'general': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections(brief): (#: default, *: current)',
                 'name     server           mock-server',
                 '*#test2  http://blahblah',
                 'test1    http://blah'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command list with 2 servers defined, not sel after '
     'next pywbemcli call',
     {'general': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections(brief): (#: default, *: current)',
                 'name    server           mock-server',
                 'test1   http://blah',
                 'test2   http://blahblah'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command list with 2 servers defined, not sel after '
     'next pywbemcli call --full',
     {'general': ['--output-format', 'plain'],
      'args': ['list', '--full']},
     {'stdout': ['WBEM server connections(full): (#: default, *: current)',
                 'name   server namespace  user  timeout  use_pull  verify  '
                 'certfile  keyfile  mock-server',
                 '*#test2  http://blahblah  root/cimv2 fred 18 False',
                 'test1  http://blah  root/cimv2 30  True'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command list with 2 servers defined, not sel after '
     'next pywbemcli call -f',
     {'general': ['--output-format', 'plain'],
      'args': ['list', '-f']},
     {'stdout': ['WBEM server connections(full): (#: default, *: current)',
                 'name   server namespace  user  timeout  use_pull  verify  '
                 'certfile  keyfile  mock-server',
                 '*#test2  http://blahblah  root/cimv2 fred 18 False',
                 'test1  http://blah  root/cimv2 30  True'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command delete test1',
     {'general': [],
      'args': ['delete', 'test1']},
     {'stdout': ['Deleted', 'test1'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command test',
     {'general': [],
      'args': ['test']},
     {'stdout': "Connection OK: FakedUrl",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify connection command test with pull option',
     {'general': [],
      'args': ['test', '--test-pull']},
     {'stdout': ["Pull Operation test results (Connection OK): FakedUrl",
                 "Operation                    Result",
                 "OpenEnumerateInstances       OK",
                 "OpenEnumerateInstancePaths   OK",
                 "OpenAssociatorInstances      OK",
                 "OpenAssociatorInstancePaths  OK",
                 "OpenReferenceInstances       OK",
                 "OpenReferenceInstancePaths   OK",
                 "OpenQueryInstances           14 "
                 "(CIM_ERR_QUERY_LANGUAGE_NOT_SUPPORTED): FilterQueryLanguage "
                 "'DMTF:CQL' not supported"],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify connection command test with pull option, no',
     {'general': ['-o', 'text'],
      'args': ['test', '--test-pull']},
     {'stdout': ["Connection OK: FakedUrl",
                 "OpenEnumerateInstances: OK",
                 "OpenEnumerateInstancePaths: OK",
                 "OpenAssociatorInstances: OK",
                 "OpenAssociatorInstancePaths: OK",
                 "OpenReferenceInstances: OK",
                 "OpenReferenceInstancePaths: OK",
                 "OpenQueryInstances: 14 "
                 "(CIM_ERR_QUERY_LANGUAGE_NOT_SUPPORTED): FilterQueryLanguage "
                 "'DMTF:CQL' not supported"],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify connection command test with pull but no instances fails',
     {'general': [],
      'args': ['test', '--test-pull']},
     {'stderr': "No instances",
      'rc': 1,
      'test': 'innows'},
     ONE_CLASS_MOCK_FILE, OK],


    # TODO: Future; Add test for --pull-options where the mocker has
    # pull disabled.  Note that this must be a completely new test, not
    # just the existing because there is no external way to turh off
    # the mocker operations without creating a new python file to load and
    # execute.so it is marked future

    ['Verify connection command delete test2',
     {'general': [],
      'args': ['delete', 'test2']},
     {'stdout': ['Deleted', 'test2', 'connection'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    ['Verify connection command list empty repository.',
     {'general': ['-o', 'simple'],
      'args': ['list']},
     {'stdout': [
         "WBEM server connections(brief):", ""],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    # End of sequence - repository is empty.

    #
    #  Sequence that creates, shows and deletes a single server definition
    #

    # Begin of sequence - repository is empty.

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
     {'general': [],
      'args': ['show', 'addallargs']},
     {'stdout': [
         'name addallargs',
         'server http://blahblah',
         'default-namespace root/blahblah',
         'user john',
         'password ******',
         'certfile mycertfile.pem',
         'keyfile mykeyfile.pem',
         'mock-server'],
      'test': 'innows'},
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
     {'general': [],
      'args': ['show', 'addallargs', '--show-password']},
     {'stdout': [
         'name addallargs',
         'server http://blah',
         'default-namespace root/blah',
         'user john',
         'password pw',
         'certfile mycertfile.pem',
         'keyfile mykeyfile.pem',
         'mock-server'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command delete addallargs',
     {'general': [],
      'args': ['delete', 'addallargs']},
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
     {'general': [],
      'args': ['export']},
     {'stderr': ['No server currently defined as current'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    # End of sequence - repository is empty.

    #
    #  Sequence that tests command line parameter errors, select, show, and
    #  delete with no repository
    #

    # Begin of sequence - repository is empty.

    ['Verify connection command show with name not in empty repo',
     {'general': [],
      'args': ['show', 'Blah']},
     {'stderr': ['Name "Blah" not current and no connections file'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command show with no name empty repo',
     {'general': [],
      'args': ['show']},
     {'stderr': ['No current connection and no connections file'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command select, empty repo fails',
     {'general': [],
      'args': ['select']},
     {'stderr': ["Connection repository", "does not exist"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command select blah, empty repo fails',
     {'general': [],
      'args': ['select', 'blah']},
     {'stderr': ["Connection repository", "does not exist"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command delete, empty repo fails',
     ['delete'],
     {'stderr': ["Connection repository", "does not exist"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command delete, empty repo fails',
     {'general': [],
      'args': ['delete', 'blah']},
     {'stderr': ["Connection repository", "does not exist"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    # End of sequence - repository is empty.

    #
    #  Sequence that verifies create and save mock connection
    #

    # Begin of sequence - repository is empty.

    ['Verify mock connection exists.',
     {'general': ['--mock-server', MOCK_FILE_PATH],
      'args': ['save', 'mocktest']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command shows mock file ',
     {'general': [],
      'args': ['show', 'mocktest']},
     {'stdout': [
         "name mocktest",
         "default-namespace root/cimv2",
         "user",
         "password",
         "timeout 30",
         "verify True",
         "certfile",
         "keyfile",
         "mock-server", "simple_mock_model.mof"],
      'test': 'innows'},
     None, OK],

    ['Verify connection command test against existing mock def',
     {'args': ['test'],
      'general': ['--name', 'mocktest']},
     {'stdout': "Connection OK: FakedUrl",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command select mocktest with prompt',
     {'general': [],
      'args': ['select']},
     {'stdout': "",
      'test': 'in',
      'file': {'before': 'exists', 'after': 'exists'}},
     MOCK_PROMPT_0_FILE, OK],

    ['Verify connection command show with prompt',
     {'general': [],
      'args': ['show', '?']},
     {'stdout': ['name mocktest'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     MOCK_PROMPT_0_FILE, OK],

    ['Verify connection command delete last one that deletes w/o prompt',
     {'general': [],
      'args': ['delete']},
     {'stdout': ['Deleted connection "mocktest"'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     MOCK_PROMPT_0_FILE, OK],

    ['Verify Add mock server to empty connections file.',
     {'general': ['--mock-server', MOCK_FILE_PATH],
      'args': ['save', 'mocktest']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command delete, empty repository',
     {'general': [],
      'args': ['delete', 'mocktest']},
     {'stdout': ['Deleted connection "mocktest"'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    # End of sequence - repository is empty.

    #
    #  Sequence that verifies create from mock with cmd line params, save,
    #  show, delete works
    #

    # Begin of sequence - repository is empty.

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
     None, OK],

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
         "name mocktest2",
         "default-namespace root/blah",
         "user john",
         "password **",
         "timeout 45",
         "verify False",
         "certfile mycertfile.pem",
         "keyfile mykeyfile.pem",
         "mock-server", "simple_mock_model.mof"],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command shows svrtest2 ',
     ['show', 'svrtest2'],
     {'stdout': [
         "name svrtest2",
         "server http://blah",
         "default-namespace root/blah",
         "user john",
         "password **",
         "timeout 45",
         "verify True",
         "certfile mycertfile.pem",
         "keyfile mykeyfile.pem"],
      'test': 'innows',
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

    # End of sequence - repository is empty.

    #
    #  Sequence that tests select variations
    #

    # Begin of sequence - repository is empty.

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
     {'stdout': ['WBEM server connections(brief): (#: default, *: current)',
                 '*not-saved http://blah'],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    # End of sequence - repository is empty.

    #
    #  Sequence to test
    #

    # Begin of sequence - repository is empty.

    ['Verify Create new connection names svrtest works.',
     {'general': ['--server', 'http://blah'],
      'args': ['save', 'svrtest']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection list with current server from general options, grid',
     {'args': ['list'],
      'general': ['--output-format', 'table', '--server', 'http://blah']},
     {'stdout': ['WBEM server connections(brief): (#: default, *: current)',
                 'file:',
                 'pywbemcli_connection_definitions.yaml',
                 '+------------+-------------+---------------+',
                 '| name       | server      | mock-server   |',
                 '|------------+-------------+---------------|',
                 '| *not-saved | http://blah |               |',
                 '| svrtest    | http://blah |               |',
                 '+------------+-------------+---------------+'],
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

    # End of sequence - repository is empty.

    #
    #  Sequence that tests creating a server and saving it from stdin all in
    #  single interactive sequence
    #

    # Begin of sequence - repository is empty.

    ['Verify Create new connection in interactive mode and delete - single',
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

    # End of sequence - repository is empty.

    #
    #  Sequence to assure that the interactive creation of a server actually
    #  puts the server in the repository
    #

    # Begin of sequence - repository is empty.

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

    # End of sequence - repository is empty.

    #
    #  Sequence to confirm fix to issue #396
    #

    # Begin of sequence - repository is empty.

    ['Create mock server definition.',
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

    ['Verify connection list with mof output format mof fails',
     {'args': ['list'],
      'general': ['--output-format', 'mof', '--server', 'http://blah']},
     {'stderr': ['Output format "mof" not allowed'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'None', 'after': 'None'}},
     None, OK],

    # End of sequence - repository is empty.

    ['Verify connection show no connection fails',
     {'args': ['show'],
      'general': []},
     {'stderr': ['No current connection'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'None', 'after': 'None'}},
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
                    'Fail. File {} should exist'.format(pywbemserversfile)
            elif file_test.lower() == 'none':
                if os.path.isfile(pywbemserversfile):
                    print('FILE THAT SHOULD NOT EXIST')
                    with open(pywbemserversfile, 'r') as fin:
                        print(fin.read())

                assert not os.path.isfile(pywbemserversfile), \
                    'Fail. File {} should not exist'.format(pywbemserversfile)

            else:
                assert False, 'File test option name {} invalid' \
                    .format(file_test)

        if not condition:
            pytest.skip("Condition for test case not met")

        if condition == 'pdb':
            import pdb  # pylint: disable=import-outside-toplevel
            pdb.set_trace()

        if 'file' in exp_response:
            if 'before' in exp_response['file']:
                test_file_existence(exp_response['file']['before'])
        # TODO: Remove this.  This forces all tests to be in test dir
        if 'general' in inputs:
            inputs['general'].extend(['--connections-file', pywbemserversfile])
        else:
            inputs = {"args": inputs}
            inputs['general'] = ['--connections-file', pywbemserversfile]
        assert '--connections-file' in inputs['general']

        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition)

        if 'file' in exp_response:
            if 'after' in exp_response['file']:
                test_file_existence(exp_response['file']['after'])
