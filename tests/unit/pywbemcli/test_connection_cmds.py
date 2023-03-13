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
import io
import pytest

from pywbemtools._utils import CONNECTIONS_FILENAME

from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE

# pylint: disable=use-dict-literal

SCRIPT_DIR = os.path.dirname(__file__)

# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
ONE_CLASS_MOCK_FILE = 'one_class_mock.mof'
INVOKE_METHOD_MOCK_FILE = 'simple_mock_invokemethod.py'

TEST_DIR = os.path.dirname(__file__)
TEST_DIR_REL = os.path.relpath(TEST_DIR)


def GET_TEST_PATH_STR(filename):  # pylint: disable=invalid-name
    """
    Return the string representing the relative path of the file name provided.
    """
    return (str(os.path.join(TEST_DIR_REL, filename)))


# Test connections file used in some testcases
TEST_CONNECTIONS_FILE_PATH = 'tmp_general_options.yaml'
TEST_CONNECTIONS_FILE_DICT = {
    'connection_definitions': {
        'blah': {
            'name': 'blah',
            'server': None,
            'user': None,
            'password': None,
            'default-namespace': 'root/cimv2',
            'timeout': 30,
            'use_pull': None,
            'pull_max_cnt': 1000,
            'verify': True,
            'certfile': None,
            'keyfile': None,
            'ca-certs': None,
            'mock-server': [
                os.path.join(TEST_DIR, 'simple_mock_model.mof'),
            ],
        },
    },
    'default_connection_name': None,
}


MOCK_DEFINITION_ENVVAR = 'PYWBEMCLI_STARTUP_SCRIPT'
MOCK_PROMPT_0_FILE = "mock_prompt_0.py"

# Get the relative path to the current directory.  This presumes that the
# test was run from the pywbemtools directory
MOCK_FILE_PATH = os.path.join(TEST_DIR_REL, SIMPLE_MOCK_FILE)

CONNECTION_HELP_LINES = [
    # pylint: disable=line-too-long
    'Usage: pywbemcli [GENERAL-OPTIONS] connection COMMAND [ARGS] [COMMAND-OPTIONS]',  # noqa: E501
    'Command group for WBEM connection definitions.',
    CMD_OPTION_HELP_HELP_LINE,
    'delete  Delete a WBEM connection definition.',
    'export  Export the current connection.',
    'list    List the WBEM connection definitions.',
    'save    Save the current connection to a new WBEM connection',
    'select  Select a WBEM connection definition as current or default.',
    'show    Show a WBEM connection definition or the current connection.',
    'test    Test the current connection with a predefined WBEM request.',
    'set-default Set a connection as the default connection.'
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
    '-d, --set-default  If set, the connection is set to be the default ',
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

CONNECTION_SET_DEFAULT_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] connection set-default NAME '
    '[COMMAND-OPTIONS]',
    'Set a connection as the default connection.',
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

    ['Verify connection command set-default --help response',
     ['set-default', '--help'],
     {'stdout': CONNECTION_SET_DEFAULT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify connection command set-default -h response',
     ['set-default', '-h'],
     {'stdout': CONNECTION_SET_DEFAULT_HELP_LINES,
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

    ['Verify connection command delete, empty conn file fails.',
     {'general': [],
      'args': ['delete', 'blah']},
     {'stderr': ["Connections file", "does not exist"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server and --server together fail.',
     {'general': ['--mock-server', MOCK_FILE_PATH, '--server', 'http://blah'],
      'args': ['list']},
     {'stderr': ["Conflicting options: `mock-server` is mutually exclusive "
                 "with options: (--name, --server)"],
      'rc': 2,
      'test': 'innows'},
     None, OK],

    #
    # The following tests are a sequence. Each depends on the previous
    # and what was in the repository when each test is executed.
    # This sequence creates a simple server named test1 and tests the
    # display, etc. of that persisted server name
    #

    # Begin of sequence - repository is empty.

    ['Verify connection command save creates file. SEQ 0.1',
     {'general': ['--server', 'http://blah'],
      'args': ['save', 'test1']},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show of just created test1. SEQ 0.2',
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
pull-max-cnt       1000
verify             True
certfile
keyfile
mock-server
ca-certs
""",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show of just created test1 as table. SEQ 0.3',
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
pull-max-cnt       1000
verify             True
certfile
keyfile
mock-server
ca-certs
""",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command save with complex general options short. '
     'SEQ 0.4',
     {'general': ['--server', 'http://blahblah', '-u', 'fred', '-p',
                  'argh', '-t', '18', '--no-verify', '-l', 'api=file,all'],
      'args': ['save', 'test2']},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show named connnection test1.SEQ 0.5',
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
pull-max-cnt       1000
verify             True
certfile
keyfile
mock-server
ca-certs
""",
      'test': 'innows'},
     None, OK],

    ['Verify connection command show test2 with --show-password. SEQ 0.6',
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
pull-max-cnt       1000
verify             False
certfile
keyfile
mock-server
ca-certs
""",
      'test': 'innows'},
     None, OK],

    ['Verify connection command show test2, masked password. SEQ 0.7',
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
pull-max-cnt       1000
verify             False
certfile
keyfile
mock-server
ca-certs
""",
      'test': 'innows'},
     None, OK],

    ['Verify connection command show test2, masked password. SEQ 0.8',
     {'general': [],
      'args': ['show', 'BADSERVERNAME']},
     {'stderr': ['Connection definition',
                 'BADSERVERNAME',
                 'not found in connections file'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify connection command list with 2 servers defined. SEQ 0.9',
     {'general': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections(brief): (#: default, *: current)',
                 'name    server           mock-server',
                 'test1   http://blah',
                 'test2   http://blahblah'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command select test2 and set default.. SEQ 0.9.1',
     {'general': [],
      'args': ['select', 'test2', '--set-default']},
     {'stdout': ['test2', 'default'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command show test2 includes "current". SEQ 0.10',
     {'general': [],
      'args': ['show', 'test2']},
     {'stdout': ['test2', 'http://blahblah', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command select test2 shows it is current. SEQ 0.11',
     {'general': [],
      'args': ['select', 'test2']},
     {'stdout': ['test2', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command select test3 fails. . SEQ 0.12',
     {'general': [],
      'args': ['select', 'test9']},
     {'stderr': ['Connection definition',
                 'test9',
                 'not found in connections file'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify connection command list with 2 servers defined, not sel after '
     'next pywbemcli call. . SEQ 0.13',
     {'general': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections(brief): (#: default, *: current)',
                 'name     server           mock-server',
                 '*#test2  http://blahblah',
                 'test1    http://blah'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command list with 2 servers defined, not selected '
     'after next pywbemcli call. SEQ 0.14',
     {'general': ['--output-format', 'plain'],
      'args': ['list']},
     {'stdout': ['WBEM server connections(brief): (#: default, *: current)',
                 'name    server           mock-server',
                 'test1   http://blah',
                 'test2   http://blahblah'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command list with 2 servers defined, not sel after '
     'next pywbemcli call --full. SEQ 0.15',
     {'general': ['--output-format', 'plain'],
      'args': ['list', '--full']},
     {'stdout': ['WBEM server connections(full): (#: default, *: current)',
                 'name   server namespace  user  timeout  use-pull  '
                 'pull-max-cnt verify  certfile  keyfile  mock-server',
                 '*#test2  http://blahblah  root/cimv2 fred 18 1000 False',
                 'test1  http://blah  root/cimv2 30 1000 True'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command list with 2 servers defined, not sel after '
     'next pywbemcli call -f. SEQ 0.16',
     {'general': ['--output-format', 'plain'],
      'args': ['list', '-f']},
     {'stdout': ['WBEM server connections(full): (#: default, *: current)',
                 'name server namespace  user  timeout  use-pull '
                 'pull-max-cnt verify certfile keyfile mock-server',
                 '*#test2  http://blahblah  root/cimv2 fred 18 1000 False',
                 'test1  http://blah  root/cimv2 30 1000 True'],
      'test': 'innows'},
     None, OK],

    ['Verify connection command delete test1. SEQ 0.17, last',
     {'general': [],
      'args': ['delete', 'test1']},
     {'stdout': ['Deleted', 'test1'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    # End of sequence - repository is empty.

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

    ['Verify connection command save no current connection.',
     {'general': [],
      'args': ['show']},
     {'stderr': [
         "No current connection exists"],
      'test': 'innows',
      'rc': 1,
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],


    #
    #  Sequence that creates, shows and deletes a single server definition
    #

    # Begin of sequence - repository is empty.

    ['Verify connection command add with all arguments. SEQ 1.1',
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

    ['Verify connection command show addallargs initial version. SEQ 1.2',
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

    ['Verify connection command with that overwrites existing name works.  '
     'SEQ 1.3',
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

    ['Verify connection command show of name addallargs, overwrite changed. '
     'SEQ 1.4',
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

    ['Verify connection command delete addallargs. SEQ 1.5',
     {'general': [],
      'args': ['delete', 'addallargs']},
     {'stdout': "Deleted",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    # uses regex because windows generates set and linux export in statements
    # No file verification required. Does not use file
    ['Verify connection command export current connection. SEQ 1.6',
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

    ['Verify connection command export no current conection. SEQ 1.7',
     {'general': [],
      'args': ['export']},
     {'stderr': ['No current server for command "connection export" that '
                 'requires a WBEM server'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    # End of sequence - repository is empty.

    #
    #  Sequence that tests command line parameter errors, select, show, and
    #  delete with no repository
    #

    # Begin of sequence - connections file does not exist.

    ['Verify connection command show with name, non-existing conn file. '
     'SEQ 2.1',
     {'general': [],
      'args': ['show', 'blah']},
     {'stderr': ['Name', 'blah', 'not current and no connections file',
                 'yaml'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command show with no name, non-existing conn file.'
     'SEQ 2.2',
     {'general': [],
      'args': ['show']},
     {'stderr': ['No current connection exists'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command select, non-existing conn file. SEQ 2.3',
     {'general': [],
      'args': ['select']},
     {'stderr': ["Connections file", "does not exist"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command select blah, non-existing conn file. SEQ 2.4',
     {'general': [],
      'args': ['select', 'blah']},
     {'stderr': ["Connections file", "does not exist"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command delete, non-existing conn file. SEQ 2.5',
     ['delete'],
     {'stderr': ["Connections file", "does not exist"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection command delete, non-existing conn file. SEQ 2.6',
     {'general': [],
      'args': ['delete', 'blah']},
     {'stderr': ["Connections file", "does not exist"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    # End of sequence - connections file does not exist.

    #
    #  Sequence that verifies create and save mock connection
    #

    # Begin of sequence - repository is empty.

    ['Verify mock connection exists. SEQ 3.1',
     {'general': ['--mock-server', MOCK_FILE_PATH],
      'args': ['save', 'mocktest']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command shows mock file. SEQ 3.2',
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

    ['Verify connection command test against existing mock def. SEQ 3.3',
     {'args': ['test'],
      'general': ['--name', 'mocktest']},
     {'stdout': "Connection OK: FakedUrl",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    # The following 3 tests use a file defined to pywbemcli through an
    # environment variable to mock the select prompt.
    ['Verify connection command select mocktest with prompt. SEQ 3.4',
     {'general': [],
      'args': ['select'],
      'env': {MOCK_DEFINITION_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)}},
     {'stdout': "",
      'test': 'in',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command show with prompt. SEQ 3.5',
     {'general': [],
      'args': ['show', '?'],
      'env': {MOCK_DEFINITION_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)}},
     {'stdout': ['name mocktest'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command delete last one that deletes w/o prompt. '
     'SEQ 3.6',
     {'general': [],
      'args': ['delete'],
      'env': {MOCK_DEFINITION_ENVVAR: GET_TEST_PATH_STR(MOCK_PROMPT_0_FILE)}},
     {'stdout': ['Deleted connection "mocktest"'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    ['Verify Add mock server to empty connections file. SEQ 3.7',
     {'general': ['--mock-server', MOCK_FILE_PATH],
      'args': ['save', 'mocktest']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection command delete, empty repository. SEQ 3.8',
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

    ['Verify save server with cmd line params to empty connections file. '
     'SEQ 4.1',
     {'args': ['save', 'svrtest2'],
      'general': ['--server', 'http://blah',
                  '--use-pull', 'no',
                  '--default-namespace', 'root/blah',
                  '--user', 'john',
                  '--timeout', '45',
                  '--password', 'pw',
                  '--verify',
                  '--certfile', 'mycertfile.pem',
                  '--keyfile', 'mykeyfile.pem']},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify save mock server with cmd line params to empty connections file. '
     'SEQ 4.2',
     {'args': ['save', 'mocktest2'],
      'general': ['--mock-server', MOCK_FILE_PATH,
                  '--use-pull', 'no',
                  '--pull-max-cnt', '222',
                  '--default-namespace', 'root/blah', ]},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command shows mock file. SEQ 4.3',
     ['show', 'mocktest2'],
     {'stdout': [
         "name mocktest2",
         "default-namespace root/blah",
         "pull-max-cnt 222",
         "mock-server", "simple_mock_model.mof"],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command shows svrtest2. SEQ 4.4',
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

    ['Verify connection command delete works. SEQ 4.5',
     ['delete', 'mocktest2'],
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection command delete works and file empty. SEQ 4.6 last',
     ['delete', 'svrtest2'],
     {'stderr': "",
      'rc': 0,
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    # End of sequence - repository is empty.

    #
    #  Sequence that tests select/show variations
    #

    # Begin of sequence - repository is empty.

    ['Verify connection show with no server definitions file fails. SEQ 6.1',
     {'general': [],
      'args': ['show']},
     {'stderr': "No current connection exists.",
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection show ? with no server definitions file fails. SEQ 6.2',
     {'general': ['--server', 'http://blah'],
      'args': ['show', "?"]},
     {'stderr': ["Connections file ", ".pywbemcli_connections.yaml",
                 "does not exist"],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],


    ['Verify connection show with just current server defined by --server. '
     'SEQ 6.3',
     {'args': ['show'],
      'general': ['--server', 'http://blah']},
     {'stdout': ['name', 'not-saved'],
      'test': 'innows',
      'file': {'before': 'none', 'after': 'none'}},
     None, OK],

    ['Verify connection list with current server from general options, plain. '
     'SEQ 6.4, last',
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

    ['Verify Create new connection names svrtest works. SEQ 7.1',
     {'general': ['--server', 'http://blah'],
      'args': ['save', 'svrtest']},
     {'stdout': "",
      'test': 'lines',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify connection list with current server from general options, grid. '
     'SEQ 7.2',
     {'args': ['list'],
      'general': ['--output-format', 'table', '--server', 'http://blah']},
     {'stdout': ['WBEM server connections(brief): (#: default, *: current)',
                 'file:',
                 CONNECTIONS_FILENAME,
                 '+------------+-------------+---------------+',
                 '| name       | server      | mock-server   |',
                 '|------------+-------------+---------------|',
                 '| *not-saved | http://blah |               |',
                 '| svrtest    | http://blah |               |',
                 '+------------+-------------+---------------+'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection select of svrtest. SEQ 7.3',
     {'args': ['select', 'svrtest', '--set-default'],
      'general': ['--server', 'http://blah']},
     {'stdout': '"svrtest" default and current',
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify connection select of svrtest as default. SEQ 7.4',
     {'args': ['show'],
      'general': []},
     {'stdout': ['svrtest'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify current connection set with general opts overrides default. '
     'SEQ 7.5',
     {'args': ['show'],
      'general': ['--server', 'https://blahblahblah']},
     {'stdout': ['not-saved', 'https://blahblahblah'],
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, FAIL],

    ['Verify connection delete svrtest. SEQ 7.6, last',
     {'args': ['delete', 'svrtest'],
      'general': []},
     {'stdout': "Deleted default connection",
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'none'}},
     None, OK],

    # End of sequence - repository is empty.

    #
    #  Sequence that tests creating a server, saving it, selecting it, showing
    #  it, and finally deleting from stdin all in
    #  single interactive sequence
    #

    # Begin of sequence - repository is empty.

    ['Verify Create new connection in interactive mode and delete - single, '
     'SEQ 8.1',
     {'general': ['--server', 'http://blah', '--user', 'fred',
                  '--password', 'fred',
                  '--certfile', 'cert1.pem', '--keyfile', 'keys1.pem'],
      'stdin': ['connection save fred',
                'connection select fred',
                'connection show fred',
                'connection delete fred']},
     {'stdout': ['name', 'fred',
                 'server', 'http://blah',
                 'default-namespace', 'root/cimv2',
                 'user', 'fred',
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

    # Begin of sequence - repository is empty.
    # TODO: the show shows the not-saved connection for some reason
    ['Verify Create new connection in interactive mode and delete - single, '
     'SEQ 8.2, last',
     {'general': [],
      'stdin': ['--server http://blah --user fred --password fred '
                '--certfile cert1.pem --keyfile keys1.pem',
                'connection save fred',
                'connection select fred',
                'connection show',
                'connection delete fred']},
     {'stdout': ['name', 'fred',
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
     None, FAIL],

    # End of sequence - repository is empty.

    #
    #  Sequence to assure that the interactive creation of a server actually
    #  puts the server in the repository
    #

    # Begin of sequence - repository is empty.

    ['Verify Create new connection in interactive mode and delete. SEQ 9.1',
     {'general': ['--server', 'http://blah', '--user', 'fred', '--password',
                  'fred', '--certfile', 'cert1.pem', '--keyfile', 'keys1.pem'],
      'stdin': ['connection save fred',
                'connection show fred']},
     {'stdout': ['name', 'fred',
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

    ['Verify connection delete fred. SEQ 9.2, last',
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

    ['Create mock server definition. SEQ 10.1',
     {'args': ['save', 'mocktest3'],
      'general': ['--mock-server', MOCK_FILE_PATH]},
     {'stdout': "",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'exists'}},
     None, OK],

    ['Verify sequence select, list, create new and save, list works. SEQ 10.2',
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

    ['Verify connection list with mof output format mof fails. SEQ 10.3, last',
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

    #
    # Test set-default option on connection save cmd line
    #

    ['Verify --setdefault on connection save works in cmd mode.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-v', '-C', TEST_CONNECTIONS_FILE_PATH, '-s',
                  'http://blahblah'],
      'args': ['save', 'blahblah', '--set-default']},
     {'stdout': ["'blahblah' set as default"],
      'test': 'innows'},
     None, OK],

    ['Verify --set-default on connection save works interactive ',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-v', '-C', TEST_CONNECTIONS_FILE_PATH, '-s',
                  'http://blahblah'],
      'stdin': ['connection save blahblah --set-default',
                'connection list']},
     {'stdout': ["'blahblah' set as default",
                 "#blahblah  http://blahblah"],
      'test': 'innows'},
     None, OK],

    #
    #  Test set-default command
    #

    ['Verify set_default cmd works cmd line mode.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-n', 'blah', '-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'args': ['set-default', 'blah']},
     {'stdout': ["'blah' set as default"],
      'test': 'innows'},
     None, OK],

    ['Verify set_default works interactive mode',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-v', '-C', TEST_CONNECTIONS_FILE_PATH, '-s',
                  'http://blahblah'],
      'stdin': ['connection save blahblah --set-default',
                "connection set-default blahblah",
                "connection list",
                'connection set-default blah',
                'connection list']},
     {'stdout': ["'blahblah' set as default",
                 '#blahblah  http://blahblah',
                 "'blah' set as default replacing 'blahblah",
                 '#blah '],
      'test': 'innows'},
     None, OK],

    ['Verify set_default fails with no existing default and no name arg.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'args': ['set-default']},  # set-default with no name argument
     {'stderr': ["No current connection connection"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify set_default fails name and --clear .',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-n', 'blah', '-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'args': ['set-default', 'blah', '--clear']},
     {'stderr': ["Name argument not allowed with --clear option"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify set_default --clears msg if no default .',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-n', 'blah', '-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'args': ['set-default', '--clear']},
     {'stdout': ["Default connection definition already cleared"],
      'test': 'innows'},
     None, OK],

    ['Verify set_default --clear works in interactive mode',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-v', '-C', TEST_CONNECTIONS_FILE_PATH, '-s',
                  'http://blahblah'],
      'stdin': ['connection save blahblah --set-default',
                "connection set-default blahblah",
                "connection list",
                'connection set-default --clear',
                'connection list']},
     {'stdout': ["'blahblah' set as default",
                 '#blahblah  http://blahblah',
                 "Connection default name cleared replacing 'blahblah",
                 '#blah '],
      'test': 'innows'},
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
                        default_connections_file_path):
        """
        Common test method for those commands and options in the
        connection command group that can be tested.  Note the
        fixture remove_connection_file which is session, autouse so should
        hide any existing connection file at beginning of this test and
        restore it after the test.
        """
        # Where is this file to be located for tests.  It defines the
        # default file location and name
        connections_file = default_connections_file_path

        def test_file_existence(file_test):
            """
            Local function to execute tests on existence of connections file.
            """
            if file_test == 'exists':
                assert os.path.isfile(connections_file) and \
                    os.path.getsize(connections_file) > 0, \
                    'Fail. File {} should exist'.format(connections_file)
            elif file_test.lower() == 'none':
                if os.path.isfile(connections_file):
                    print('FILE THAT SHOULD NOT EXIST')
                    with io.open(connections_file, 'r', encoding='utf-8') \
                            as fin:
                        print(fin.read())

                assert not os.path.isfile(connections_file), \
                    'Fail. File {} should not exist'.format(connections_file)

            else:
                assert False, 'File test option name {} invalid' \
                    .format(file_test)

        if not condition:
            pytest.skip("Condition for test case not met")

        if condition == 'pdb':
            import pdb  # pylint: disable=import-outside-toplevel
            pdb.set_trace()  # pylint: disable=forgotten-debug-statement

        if 'file' in exp_response:
            if 'before' in exp_response['file']:
                test_file_existence(exp_response['file']['before'])

        if 'connections_file_args' not in inputs:
            # add connections file if the general list exists.
            if 'general' in inputs:
                inputs['general'].extend(['--connections-file',
                                          connections_file])
            else:
                inputs = {"args": inputs}
                inputs['general'] = ['--connections-file', connections_file]
            assert '--connections-file' in inputs['general']

        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition)

        if 'file' in exp_response:
            if 'after' in exp_response['file']:
                test_file_existence(exp_response['file']['after'])

#
#   Test invalid connection file
#


YAML_NO_CONNECTIONS_KEY = u"""tst1:
        name: tst1
        server: http://blah
        user: fred
        password: fred
        default-namespace: root/cimv2
        timeout: 30
        use_pull: null
        pull_max_cnt: null
        verify: true
        certfile: null
        keyfile: null
        ca-certs: null
        mock-server: []
default_connection_name: null
"""

YAML_BAD_ATTRIBUTE_NAME = u"""connection_definitions:
    tst1:
        name: tst1
        server: http://blah
        user: fred
        password: fred
        default-namespace: root/cimv2
        timeoutx: 30
        use_pull: null
        pull_max_cnt: null
        verify: true
        certfile: null
        keyfile: null
        ca-certs: null
        mock-server: []
default_connection_name: null
"""

YAML_BAD_DEFAULT_NAME = u"""connection_definitions:
    tst1:
        name: tst1
        server: http://blah
        user: fred
        password: fred
        default-namespace: root/cimv2
        timeoutx: 30
        use_pull: null
        pull_max_cnt: null
        verify: true
        certfile: null
        keyfile: null
        ca-certs: null
        mock-server: []
default_connection_name: THISISBADNAME
"""

# Local connections file to be built for errors test.
SCRIPT_DIR = os.path.dirname(__file__)
CONNECTION_REPO_TEST_FILE_PATH = os.path.join(SCRIPT_DIR,
                                              'tst_connection_cmds.yaml')


@pytest.fixture()
def remove_file_before_after():
    """
    Remove the connections file at beginning and end of test.
    """
    if os.path.isfile(CONNECTION_REPO_TEST_FILE_PATH):
        os.remove(CONNECTION_REPO_TEST_FILE_PATH)
    # The yield causes the remainder of this fixture to be executed at the
    # end of the test.
    yield
    if os.path.isfile(CONNECTION_REPO_TEST_FILE_PATH):
        os.remove(CONNECTION_REPO_TEST_FILE_PATH)


TEST_CASES_ERROR = [

    # List of testcases.
    # Each testcase is a list with the following items:
    # * desc: Description of testcase.
    # * inputs: String, or tuple/list of strings, or dict of 'env', 'args',
    #     'general', and 'stdin'. See the 'inputs' parameter of
    #     CLITestsBase.command_test() in cli_test_extensions.py for detailed
    #     documentation.
    #     Additionally for this test there is a yaml parameter that is used
    #     to build the YAML file. This allows building error files.
    # * exp_response: Dictionary of expected responses (stdout, stderr, rc) and
    #     test definition (test: <testname>). See the 'exp_response' parameter
    #     of CLITestsBase.command_test() in cli_test_extensions.py for
    #     detailed documentation.
    # * mock: None, name of file (.mof or .py), or list thereof.
    # * condition: If True the test is executed, if 'pdb' the test breaks in the
    #     the debugger, if 'verbose' print verbose messages, if False the test
    #     is skipped.

    ['Verify yaml file with key for the connections definitions missing fails',
     {'args': ['show'],
      'general': [],
      'yaml': YAML_NO_CONNECTIONS_KEY},
     {'stderr': ['ConnectionsFileLoadError',
                 'tst_connection_cmds.yaml',
                 'Missing YAML property',
                 'connection_definitions',
                 'Aborted'],
      'rc': 1,
      'test': 'innows', },
     None, OK],

    ['Verify YAML with bad default_connection_name fails',
     {'args': ['show'],
      'general': [],
      'yaml': YAML_BAD_DEFAULT_NAME},
     {'stderr': ['ConnectionsFileLoadError',
                 'tst_connection_cmds.yaml',
                 'Invalid attribute type in connection definition',
                 'tst1',
                 'timeoutx',
                 'Aborted'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

    ['Verify YAML with bad attribute name in definition fails',
     {'args': ['show'],
      'general': [],
      'yaml': YAML_BAD_ATTRIBUTE_NAME},
     {'stderr': ['ConnectionsFileLoadError',
                 'tst_connection_cmds.yaml',
                 'Invalid attribute type in connection definition',
                 'tst1',
                 'unexpected keyword argument',
                 'timeoutx',
                 'Aborted'],
      'rc': 1,
      'test': 'innows',
      'file': {'before': 'exists', 'after': 'exists'}},
     None, OK],

]


@pytest.mark.usefixtures("remove_file_before_after")
class TestSubcmdClassError(CLITestsBase):
    """
    Test pywbemcli when the connections file is invalid.
    """
    command_group = 'connection'

    @pytest.mark.usefixtures("remove_file_before_after")
    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES_ERROR)
    def test_connection(self, desc, inputs, exp_response, mock, condition):
        """
        Common test method for those commands and options in the
        connection command group that can be tested.  Note the
        fixture remove_connection_file which is session, autouse so should
        hide any existing connection file at beginning of this test and
        restore it after the test.
        """
        # Create the connection file from the yaml
        with io.open(CONNECTION_REPO_TEST_FILE_PATH, "w", encoding='utf-8') \
                as repo_file:
            repo_file.write(inputs['yaml'])

        connections_file = CONNECTION_REPO_TEST_FILE_PATH

        def test_file_existence(file_test):
            """
            Local function to execute tests on existence of connections file.
            """
            if file_test == 'exists':
                assert os.path.isfile(connections_file) and \
                    os.path.getsize(connections_file) > 0, \
                    'Fail. File {} should exist'.format(connections_file)
            elif file_test.lower() == 'none':
                if os.path.isfile(connections_file):
                    print('FILE THAT SHOULD NOT EXIST')
                    with io.open(connections_file, 'r', encoding='utf-8') \
                            as fin:
                        print(fin.read())

                assert not os.path.isfile(connections_file), \
                    'Fail. File {} should not exist'.format(connections_file)

            else:
                assert False, 'File test option name {} invalid' \
                    .format(file_test)

        if not condition:
            pytest.skip("Condition for test case not met")

        if condition == 'pdb':
            import pdb  # pylint: disable=import-outside-toplevel
            pdb.set_trace()  # pylint: disable=forgotten-debug-statement

        if 'file' in exp_response:
            if 'before' in exp_response['file']:
                test_file_existence(exp_response['file']['before'])
        if 'general' in inputs:
            inputs['general'].extend(['--connections-file', connections_file])
        else:
            inputs = {"args": inputs}
            inputs['general'] = ['--connections-file', connections_file]
        assert '--connections-file' in inputs['general']

        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition)
