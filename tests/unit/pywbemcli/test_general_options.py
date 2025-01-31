# (C) Copyright 2017 IBM Corp.
# (C) Copyright 2017 Inova Development Inc.
# All Rights Reserved
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
Test the pywbemcli general options.  That is those options that are defined and
used in pywbemcli.py and show up in the help output from pywbemcli --help.

NOTE: The --log options are tested in a separate file.
"""


import os
import sys
import pytest

from pywbemtools.pywbemcli._connection_file_names import CONNECTIONS_FILENAME

from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE
from ..utils import CLICK_VERSION

# pylint: disable=use-dict-literal

TEST_DIR = os.path.dirname(__file__)

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

# Test connection definition with url
TEST_CONNECTIONS_FILE_DICT_SERVER = {
    'connection_definitions': {
        'realsvr': {
            'name': 'blah',
            'server': 'http://blah',
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
            'mock-server': [],
        },
    },
    'default_connection_name': None,
}

EMPTY_CONNECTIONS_FILE_PATH = 'empty_connections_file.yaml'


MOCK_DEFINITION_ENVVAR = 'PYWBEMCLI_STARTUP_SCRIPT'
BAD_PY_ERR_STRTUP_FILE = 'error/py_err_processatstartup.py'
BAD_PY_ERR_STRTUP_FILE_PATH = os.path.join(TEST_DIR, BAD_PY_ERR_STRTUP_FILE)
MOCK_PW_PROMPT_FILE_PATH = os.path.join(TEST_DIR, 'mock_password_prompt.py')

SIMPLE_MOCK_MODEL_FILE_PATH = os.path.join(TEST_DIR, "simple_mock_model.mof")
PYTHON_MOCK_FILE_PATH = os.path.join(TEST_DIR, 'simple_python_mock_script.py')
BAD_MOF_FILE_PATH = os.path.join(TEST_DIR, 'mof_with_error.mof')
BAD_PY_FILE_PATH = os.path.join(TEST_DIR, 'py_with_error.py')

SIMPLE_DISABLEPULL_MOCK_SCRIPT = 'simple_disablepull_mock_script.py'
SIMPLE_DISABLEPULL_MOCK_SCRIPT_PATH = os.path.join(
    TEST_DIR, SIMPLE_DISABLEPULL_MOCK_SCRIPT)

MOCK_SERVER_MODEL = os.path.join(TEST_DIR, 'testmock',
                                 'wbemserver_mock_script.py')

GENERAL_HELP_LINES = [
    """
    Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS] [COMMAND-OPTIONS]

      Pywbemcli is a command line WBEM client that uses the DMTF CIM-XML
      protocol
      to communicate with WBEM servers. Pywbemcli can:

      * Manage the information in WBEM servers CIM objects using the
        operations defined in the DMTF specification.  It can manage CIM
        classes, CIM instances and CIM qualifier declarations in the WBEM
        Server and execute CIM methods and queries on the server.

      * Inspect WBEM server characteristics including namespaces, registered
        profiles, and other server information.

      * Capture detailed information on communication with the WBEM
        server including time statistics and logs of the operations.

      * Maintain a persistent list of named connections to WBEM servers
        and execute operations on them by name.

      Pywbemcli implements command groups and commands to execute the CIM-XML
      operations defined by the DMTF CIM Operations Over HTTP specification
      (DSP0200).

      The general options shown below can also be specified on any of the
      commands, positioned right after the 'pywbemcli' command name.

      The width of help texts of this command can be set with the
      PYWBEMTOOLS_TERMWIDTH environment variable.

      For more detailed documentation, see:

      https://pywbemtools.readthedocs.io/en/stable/""",
    CMD_OPTION_HELP_HELP_LINE,
    "General Options:",
    "-n, --name NAME Use the WBEM server defined by the WBEM",
    "-m, --mock-server FILE  Use a mock WBEM server that is automatically",
    "-s, --server URL  Use the WBEM server at the specified URL with",
    "-u, --user TEXT   User name for the WBEM server.",
    "-p, --password TEXT  Password for the WBEM server. Default: EnvVar",
    "--verify / --no-verify  If --verify, client verifies the X.509 server",
    "--ca-certs CACERTS  Certificates used to validate the certificate",
    "-c, --certfile FILE  Path name of a PEM file containing a X.509",
    "-t, --timeout INT  Client-side timeout (seconds) on data read for",
    "-U, --use-pull [yes|no|either] Determines whether pull operations are ",
    "--pull-max-cnt INT  Maximum number of instances to be returned by",
    "-T, --timestats / --no-timestats",
    "-d, --default-namespace NAMESPACE Default namespace, to be used when ",
    "-o, --output-format FORMAT Output format for the command result. The",
    "-l, --log COMP[=DEST[:DETAIL]]",
    "Enable logging of WBEM operations,",
    "-C, --connections-file FILE PATH Path name of the connections file",
    CONNECTIONS_FILENAME,
    "-v, --verbose / --no-verbose Display extra information about the",
    "--warn / --no-warn",
    "--pdb    Pause execution in the built-in pdb debugger",
    "--version   Show the version of this command and the",
    """Commands:
      class       Command group for CIM classes.
      instance    Command group for CIM instances.
      namespace   Command group for CIM namespaces.
      profile     Command group for WBEM management profiles.
      qualifier   Command group for CIM qualifier declarations.
      server      Command group for WBEM servers.
      statistics  Command group for WBEM operation statistics.
      subscription  Command group to manage WBEM indication subscriptions.
      connection  Command group for WBEM connection definitions.
      repl        Enter interactive mode (default).
      help        Show help for pywbemcli subjects.
      docs        Get pywbemtools documentation in web browser."""
]

# pylint: disable=line-too-long
REPL_HELP = """Usage: pywbemcli [GENERAL-OPTIONS] repl

  Enter interactive mode (default).

  Enter the interactive mode where pywbemcli commands can be entered
  interactively. The prompt is changed to 'pywbemcli>'.

  <COMMAND> <COMMAND OPTIONS> - Execute pywbemcli command COMMAND

  <GENERAL_OPTIONS> <COMMAND> <COMMAND_OPTIONS> - Execute command with general
  options.  General options set here exist only for the current command.

  -h, --help - Show pywbemcli general help message, including a
  list of pywbemcli commands. COMMAND -h, --help - Show help message for
  pywbemcli command COMMAND.

  !SHELL-CMD - Execute shell command SHELL-CMD

  Pywbemcli termination - <CTRL-D>, :q, :quit, :exit

  Command history is supported. The command history is stored in a file
  ~/.pywbemcli_history.

  <UP>, <DOWN> - Scroll through pwbemcli command history.

  <CTRL-r> <search string> - initiate an interactive search of the pywbemcli
  history file. Can be used with <UP>, <DOWN> to display commands that match the
  search string. Editing the search string updates the search.

  <TAB> - tab completion for current command line (can be used anywhere in
  command)

  Interactive mode also includes an autosuggest feature that makes suggestions
  from the command history as the command the user types in the command and
  options.

Command Options:
  -h, --help  Show this help message.

"""  # noqa: E501


SUBJECT_HELP = """Usage: pywbemcli [GENERAL-OPTIONS] help SUBJECT

  Show help for pywbemcli subjects.

  Show help for specific pywbemcli subjects.  This is in addition to the help
  messages that are available with the -h or --help option for every command
  group and command in pywbemcli. It helps document pywbemcli subjects that are
  more general than specific commands and configuration subjects that do not
  have specific commands

  If there is no argument provided, outputs a list and summary of the existing
  help subjects.

  If an argument is provided, it outputs the help for the subject(s) defined by
  the argument.

Command Options:
  -h, --help  Show this help message.
"""

OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet
SKIP = False

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

    ['Verify help command --help response lines',
     {'general': ['--help'],
      'cmdgrp': 'class',
      'args': ['get', 'blah']},
     {'stdout': GENERAL_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify help command -h response lines',
     {'general': ['--help'],
      'cmdgrp': 'class',
      'args': ['get', 'blah']},
     {'stdout': GENERAL_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify repl -h option shows REPL help',
     {'general': [],
      'cmdgrp': 'repl',
      'args': ['-h']},
     {'stdout': REPL_HELP,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify help response (help command).',
     {'general': [],
      'cmdgrp': 'help',
      'args': ['--help']},
     {'stdout': SUBJECT_HELP,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify invalid server definition.',
     {'general': ['-s', 'httpx://blah'],
      'cmdgrp': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['Error: Invalid scheme on server argument: httpx://blah. Use '
                 '"http" or "https"'],
      'rc': 1,
      'test': 'in'},
     None, OK],


    ['Verify invalid server port definition fails. pywbem version 1',
     {'general': ['-s', 'http://blah:abcd'],
      'cmdgrp': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['ValueError:', "Invalid port number 'abcd' in URL "
                 "'http://blah:abcd'"],
      'rc': 1,
      'test': 'innows'},
     None, OK],


    ['Verify valid --use-pull option parameter yes.',
     {'general': ['-s', 'http://blah', '--use-pull', 'yes'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull True'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify valid --use-pull option parameter no.',
     {'general': ['-s', 'http://blah', '--use-pull', 'no'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull False'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify valid --use-pull option parameter either.',
     {'general': ['-s', 'http://blah', '--use-pull', 'either'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull pull-max-cnt 1000 verify'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify valid --use-pull yes option returns data from mock.',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH,
      '--use-pull', 'yes'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo']},
     {'stdout': ["class CIM_Foo"],
      'test': 'innows'},
     None, OK],

    ['Verify valid --use-pull either option returns data from mock.',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH,
                  '--use-pull', 'either'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo']},
     {'stdout': ["class CIM_Foo"],
      'test': 'innows'},
     None, OK],

    ['Verify valid --use-pull no option returns data from mock.',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH,
      '--use-pull', 'no'],
      'cmdgrp': 'class',
      'args': ['get', 'CIM_Foo']},
     {'stdout': ["class CIM_Foo"],
      'test': 'innows'},
     None, OK],

    ['Verify simultaneous --server and --mock-server on cmd line invalid.',
     {'general': ['--server', 'http://blah', '--mock-server',
                  SIMPLE_MOCK_MODEL_FILE_PATH],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Conflicting options: `server` is mutually exclusive with "
                 "options: (--mock-server, --name)"],
      'rc': 2,
      'test': 'in'},
     None, OK],

    ['Verify simultaneous --mock-server option and --name option fails',
     {'general': ['-m', SIMPLE_MOCK_MODEL_FILE_PATH, '--name', 'MyConnName'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Conflicting options: `connection-name` is mutually exclusive "
                 "with options: (--mock-server, --server)"],
      'rc': 2,
      'test': 'innows'},
     None, OK],

    ['Verify conflicting --server option and --name option fails',
     {'general': ['--server', 'http://blah', '--name', 'MyConnName'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Conflicting options: `connection-name` is mutually exclusive "
                 "with options: (--mock-server, --server)"],
      'rc': 2,
      'test': 'innows'},
     None, OK],

    ['Verify invalid --use-pull option parameter fails.',
     {'general': ['-s', 'http://blah', '--use-pull', 'blah'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Invalid value', '-U', '--use-pull',
                 'invalid choice: blah. (choose from yes, no, either)'
                 if CLICK_VERSION < (8, 0) else
                 "'blah' is not one of 'yes', 'no', 'either'"
                 ],
      'rc': 2,
      'test': 'innows'},
     None, OK],

    ['Verify valid --pull-max-cnt option parameter with single command.',
     {'general': ['-s', 'http://blah', '--pull-max-cnt', '2000'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': ['pull-max-cnt 2000'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify invalid --pull-max-cnt option parameter fails.',
     {'general': ['-s', 'http://blah', '--pull-max-cnt', 'blah'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Invalid value for', '--pull-max-cnt',
                 "blah is not a valid integer"
                 if CLICK_VERSION < (8, 0) else
                 "'blah' is not a valid integer"],
      'rc': 2,
      'test': 'innows'},
     None, OK],  # Only tests that the option is accepted

    ['Verify --no-warn general option included.',
     {'general': ['-s', 'http://blah', '--no-warn'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': [''],
      'rc': 0,
      'test': 'innows'},
     None, OK],  # Only tests that the option is accepted

    ['Verify --warn general option included.',
     {'general': ['-s', 'http://blah', '--warn'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': [''],
      'rc': 0,
      'test': 'innows'},
     None, OK],  # Only tests that the option is accepted

    ['Verify --warn general option where warning is generated. Python <=3.4',
     {'general': ['-s', 'http://blah', '--warn'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Pywbemcli support for Python", "is deprecated"],
      'rc': 0,
      'test': 'innows'},
     None, sys.version_info[0:2] == (2, 7)],

    ['Verify --warn general option where warning is generated with stdin.',
     {'general': ['-s', 'http://blah'],
      'stdin': ["--warn connection show"]},
     {'stderr': ["Pywbemcli support for Python", "is deprecated"],
      'rc': 0,
      'test': 'innows'},
     None, FAIL],  # was sys.version_info[0:2] == (2, 7)
    # Issue 867,TODO Marked fail because results inconsistent.

    ['Verify --warn general option where warning is NOT generated.',
     {'general': ['-s', 'http://blah', '--warn'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': [""],
      'rc': 0,
      'test': 'innows'},
     None, sys.version_info[0:2] >= (3, 6)],

    ['Verify --version general option.',
     {'general': ['-s', 'http://blah', '--version'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': [r'^pywbemcli, version [0-9]+\.[0-9]+\.[0-9]+',
                 r'^pywbem, version [0-9]+\.[0-9]+\.[0-9]+'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    #
    #  Test --verify and --no-verify general option using the connection show
    #
    ['Verify --verify general option.',
     {'general': ['--server', 'http://blah', '--verify'],
      'args': ['show'],
      'cmdgrp': 'connection'},
     {'stdout': "verify True",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'None'}},
     None, OK],

    ['Verify --no-verify general option.',
     {'general': ['--server', 'http://blah', '--no-verify'],
      'args': ['show'],
      'cmdgrp': 'connection'},
     {'stdout': "verify False",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'None'}},
     None, OK],

    ['Verify --verify general options  Default value.',
     {'general': ['--server', 'http://blah'],
      'args': ['show'],
      'cmdgrp': 'connection'},
     {'stdout': "verify True",
      'test': 'innows',
      'file': {'before': 'none', 'after': 'None'}},
     None, OK],

    ['Verify -m option one file',
     {'general': ['-m', SIMPLE_MOCK_MODEL_FILE_PATH],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': ['^name *not-saved \\(current\\)$',
                 '^server$',
                 '^mock-server *.*simple_mock_model.mof$',
                 '^default-namespace *root/cimv2$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify -m option, multiple files',
     {'general': ['-m', SIMPLE_MOCK_MODEL_FILE_PATH,
                  '-m', PYTHON_MOCK_FILE_PATH],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': ['^name *not-saved \\(current\\)$',
                 '^server$',
                 '^mock-server *.*simple_mock_model.mof$',
                 'simple_python_mock_script.py$',
                 '^default-namespace *root/cimv2$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    #
    #  Test errors with --mock-server option
    #

    ['Verify --mock-server option, file does not exist',
     {'general': ['--mock-server', 'invalidfilename.mof'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': "Invalid value for '-m' / '--mock-server': "
                "File 'invalidfilename.mof' does not exist.",
      'rc': 2,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server option, file with bad extension',
     {'general': ['--mock-server', 'invalidfilename.mofx'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': "Invalid value for '-m' / '--mock-server': File "
                "'invalidfilename.mofx' does not exist.",
      'rc': 2,
      'test': 'innows'},
     None, OK],

    ['Verify -m option, file with mof containing syntax error',
     {'general': ['-m', BAD_MOF_FILE_PATH],
      'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stdout': "",
      'stderr': ['MOF compile failed:',
                 BAD_MOF_FILE_PATH,
                 "(see above)",
                 'Aborted!'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify -m option, file with python containing syntax error',
     {'general': ['-m', BAD_PY_FILE_PATH],
      'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stderr': [BAD_PY_FILE_PATH,
                 'Traceback (most recent call last)',
                 "NameError: name 'globalsx' is not defined",
                 'Aborted!'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify -m option, file with python startup file containing syntax error',
     {'general': ['-m', SIMPLE_MOCK_MODEL_FILE_PATH],
      'cmdgrp': 'class',
      'args': ['enumerate'],
      'env': {MOCK_DEFINITION_ENVVAR: BAD_PY_ERR_STRTUP_FILE_PATH}},
     {'stderr': ['Traceback (most recent call last)',
                 'def mock?prompt(msg):',
                 'SyntaxError:'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    #
    #  Test errors with --name option, --mock-server option
    #

    ['Verify --name with non-existent connection file fails',
     {'general': ['--name', 'fred', '--connections-file',
                  './filenotfound.yaml'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Connections file does not exist: ./filenotfound.yaml',
                 'Aborted!'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --name with non-existent connection name',
     {'general': ['--name', 'name does not exist', '--connections-file',
                  './filenotfound.yaml'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Connections file does not exist: ./filenotfound.yaml',
                 'Aborted!'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server and WBEMConnection only option user',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH,
                  '--user', 'fred'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Error: General option(s): (--user) not allowed when using a "
                 "mock server"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server and WBEMConnection only options user and password',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH,
                  '--user', 'fred', '--password', 'fred'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Error: General option(s): (--user, --password) not allowed "
                 "when using a mock server."],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server and WBEMConnection only options certfile, keyfile',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH,
                  '--certfile', 'fred', '--keyfile', 'fred'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Error: General option(s): (--certfile, --keyfile) not "
                 "allowed when using a mock server."],
      'rc': 1,
      'test': 'innows'},
     None, OK],


    ['Verify --mock-server and WBEMConnection only option no-verify',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH,
                  '--no-verify'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Error: General option(s): (--verify) not allowed "
                 "when using a mock server."],
      'rc': 1,
      'test': 'innows'},
     None, OK],


    ['Verify --mock-server and WBEMConnection only option --verify',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH,
                  '--verify'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Error: General option(s): (--verify) not allowed "
                 "when using a mock server."],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    # TODO: Add test where file exists.


    ['Verify --mock-server invalid name',
     {'general': ['--mock-server', 'fred'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ["Invalid value for", "'-m' / '--mock-server'", "File",
                 "'fred'", "does not exist."],
      'rc': 2,
      'test': 'innows'},
     None, OK],


    ['Verify --timestats',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH, '--timestats'],
      'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stdout': ['class CIM_Foo {',
                 'Client statistics',
                 'Operation Count Errors',
                 'EnumerateClasses'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify uses pull operation with option --use-pull either',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH, '--timestats',
                  '--use-pull', 'either', '--pull-max-cnt', '1'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': [r'instance of CIM_Foo {',
                 r'Client statistics',
                 r'Operation +Count +Errors',
                 r'^ *OpenEnumerateInstances'],  # Does not confirm no Enum...
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify pull fails options --use-pull either, --disable-pull-operations',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH, '--timestats',
                  '--use-pull', 'either', '--pull-max-cnt', '1'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': [r'instance of CIM_Foo {',
                 r'Client statistics',
                 r'Operation +Count +Errors',
                 r'^ *OpenEnumerateInstances'],  # Does not confirm no Enum...
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify pull fails options --use-pull either & disabled pull operations, '
     'confirms exception on OpenEnumerateInstances',
     {'general': ['--mock-server', SIMPLE_DISABLEPULL_MOCK_SCRIPT_PATH,
                  '--log', 'api=stderr:summary', '--use-pull', 'either'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stderr': ['Exception:.*OpenEnumerateInstances'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify pull fails options --use-pull either & disabled pull operations, '
     'confirms only EnumerateInstances on second request',
     {'general': ['--mock-server', SIMPLE_DISABLEPULL_MOCK_SCRIPT_PATH,
                  '--use-pull', 'either'],
      'stdin': ['instance enumerate CIM_Foo',
                'statistics reset',
                '--timestats instance enumerate CIM_Foo']},
     {'stdout': [r'instance of CIM_Foo {',
                 r'Client statistics',
                 r'Operation +Count +Errors',
                 r'EnumerateInstances',
                 r'[^n]EnumerateInstances'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify uses pull operation with option --use-pull yes',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH, '--timestats',
                  '--use-pull', 'yes', '--pull-max-cnt', '1'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': ['instance of CIM_Foo {',
                 'Client statistics',
                 'Operation Count Errors',
                 'OpenEnumerateInstances 1',
                 'PullInstancesWithPath 11'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify uses traditional operation with option --use-pull no',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH, '--timestats',
                  '--use-pull', 'no'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': [r'instance of CIM_Foo ',
                 r'Client statistics',
                 r'Operation +Count +Errors',
                 r'^ *EnumerateInstances',      # Enumerate returned
                 r'[^n]EnumerateInstances'],    # no OpenEnumerate
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --mock-server and -server not allowed',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH,
                  '--server', 'http://blah'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stderr': ['Conflicting options: `mock-server` is mutually exclusive '
                 'with options: (--name, --server)'],
      'rc': 2,
      'test': 'innows'},
     None, OK],

    #
    #   The following is a new sequence but depends on the repo being empty
    #   It creates, shows and deletes a single server definition to demo
    #   effect of other parameters than the --name parameter
    #

    ['Verify Create a connection for test.',
     {'general': ['--server', 'http://blah',
                  '--timeout', '45',
                  '--default-namespace', 'root/blah',
                  '--user', 'john',
                  '--password', 'pw',
                  '--no-verify',
                  '--certfile', 'mycertfile.pem',
                  '--keyfile', 'mykeyfile.pem'],
      'args': ['save', 'generaltest1'],
      'cmdgrp': 'connection', },
     {'stdout': "",
      'test': 'innows'},
     None, OK],

    ['Verify --name option with non-existent connection file fails',
     {'general': ['--name', 'namedoesnotexist'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Connection definition',
                 'namedoesnotexist',
                 'not found in connections file'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify connection gets deleted.',
     {'cmdgrp': 'connection',
      'args': ['delete', 'generaltest1']},
     {'stdout': '',
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify connection already deleted.',
     {'cmdgrp': 'connection',
      'args': ['delete', 'generaltest1']},
     {'stderr': ['Connections file',
                 'does not exist'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify connection without server definition and command that requires a '
     'connection actually fails.',
     {'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stderr': ['No current server for command "class enumerate" that '
                 'requires a WBEM server.'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --keyfile allowed only if --certfile exists.',
     {'cmdgrp': 'class',
      'args': ['enumerate'],
      'general': ['--keyfile', 'mykey.pem']},
     {'stderr': ['The --keyfile option',
                 'is allowed only if the --certfile option is also used'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify password prompt with server that requires one',
     {'general': ['--server', "http://blahblah",
                  '--user', 'john'],
      'cmdgrp': 'connection',
      'args': ['test'],
      'env': {MOCK_DEFINITION_ENVVAR: MOCK_PW_PROMPT_FILE_PATH}},
     {'stdout': ["MOCK_CLICK_PROMPT Enter password (user john)"],
      'stderr': ["ConnectionError: Failed to establish"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    #
    #   Verify password prompt. This is a sequence using a connections file
    #
    ['Create a mock server with user but no password. Sequence 0,1.',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH, ],
      'args': ['save', 'mocktestVerifyPWPrompt'],
      'cmdgrp': 'connection', },
     {'stdout': "",
      'test': 'innows'},
     None, OK],

    # TODO: This test is worthless the prompt is not called
    ['Verify server in repository.  Sequence 0,2.',
     {'cmdgrp': 'connection',
      'args': ['list'],
      'env': {MOCK_DEFINITION_ENVVAR: MOCK_PW_PROMPT_FILE_PATH}},
     {'stdout': ['mocktestVerifyPWPrompt', 'WBEM server connections(brief)'],
      'test': 'innows'},
     None, OK],

    ['Verify load of this server and class enumerate triggers password prompt. '
     ' Sequence 0,3.',
     {'general': ['--name', 'mocktestVerifyPWPrompt', ],
      'cmdgrp': 'class',
      'args': ['enumerate'],
      'env': {MOCK_DEFINITION_ENVVAR: MOCK_PW_PROMPT_FILE_PATH}},
     {'stdout': ['CIM_Foo'],
      'test': 'innows'},
     None, OK],

    ['Delete our test server. Sequence 0,4. Last',
     {'general': ['--name', 'mocktestVerifyPWPrompt'],
      'cmdgrp': 'connection',
      'args': ['delete', 'mocktestVerifyPWPrompt']},
     {'stdout': ['Deleted'],
      'test': 'innows'},
     None, OK],

    ['Open non-existent server with user but no password. use stdin to test '
     'for prompt',
     # NOTE: the class enumerate fails but is required to ask for pw
     {'general': ['--server', "http://blahblah",
                  '--user', 'john'],
      'stdin': ['class enumerate'],
      'env': {MOCK_DEFINITION_ENVVAR: MOCK_PW_PROMPT_FILE_PATH}},
     {'stdout': ['MOCK_CLICK_PROMPT Enter password',
                 '(user john)'],
      'test': 'innows'},
     None, OK],

    #
    #  The following is a sequence that tests use of default connection
    #  Creates server and saves. Tests that save works and then uses
    #  select to set the default server to this connection
    #  Tests that pywbemcli execute with no --name, etc. gets the default.
    #  Removes the connection
    #

    ['Create a connection to test default connection. sequence:1,1',
     {'general': ['--server', 'http://blah'],
      'args': ['save', 'test-default'],
      'cmdgrp': 'connection', },
     {'stdout': '',
      'test': 'innows'},
     None, OK],

    ['Verify select of test-default. sequence:1,2',
     {'args': ['select', 'test-default'],
      'cmdgrp': 'connection', },
     {'stdout': ['test-default', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify show test-default connection. sequence:1,3',
     {'args': ['show', 'test-default'],
      'cmdgrp': 'connection', },
     {'stdout': ['test-default'],
      'test': 'innows'},
     None, OK],

    ['Verify select of test-default connection. sequence:1,4',
     {'args': ['select', 'test-default', '--set-default'],
      'cmdgrp': 'connection', },
     {'stdout': ['test-default', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify show current which is test-default.  sequence:1,5',
     {'args': ['show'],
      'cmdgrp': 'connection', },
     {'stdout': ['test-default'],
      'test': 'innows'},
     None, OK],

    ['Verify show current which is test-default because it loads the default. '
     'sequence:1,6',
     {'general': ['--verbose'],
      'args': ['show'],
      'cmdgrp': 'connection', },
     {'stdout': ['test-default (current, default)'],
      'test': 'innows'},
     None, OK],

    ['Delete test-default.  sequence:1,7',
     {'args': ['delete', 'test-default'],
      'cmdgrp': 'connection', },
     {'stdout': "",
      'test': 'innows'},
     None, OK],

    ['Verify delete worked by requesting again expecting failure. sequence:1,8 '
     '. Last',
     {'args': ['delete', 'test-default'],
      'cmdgrp': 'connection', },
     {'stderr': ['Connections file',
                 'does not exist'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    # End of sequence - There should be no connections file

    #
    # Test using environment variables as input
    #
    ['Verify setting one environment variable (PYWBEMCLI_SERVER) for input.',
     {'env': {'PYWBEMCLI_SERVER': 'http://blah'},
      'cmdgrp': 'connection',
      'args': ['show', '--show-password']},
     {'stdout': ['^name *not-saved \\(current\\)$',
                 '^server *http://blah$',
                 '^default-namespace *root/cimv2$',
                 '^user$',
                 '^password$',
                 '^timeout *30$',
                 '^verify *True$',
                 '^certfile$',
                 '^keyfile$',
                 '^mock-server$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify setting all env vars for input.',
     {'env': {'PYWBEMCLI_SERVER': 'http://blah',
              'PYWBEMCLI_DEFAULT_NAMESPACE': 'fred/fred',
              'PYWBEMCLI_USER': 'RonaldMcDonald',
              'PYWBEMCLI_PASSWORD': 'abcxdfG',
              'PYWBEMCLI_TIMEOUT': '99',
              'PYWBEMCLI_VERIFY': 'True',
              'PYWBEMCLI_CERTFILE': 'certfile.pem',
              'PYWBEMCLI_KEYFILE': 'keyfile.pem',
              'PYWBEMCLI_USE_PULL': 'no',
              'PYWBEMCLI_PULL_MAX_CNT': '10',
              'PYWBEMCLI_LOG': 'api=all', },
      'cmdgrp': 'connection',
      'args': ['show', '--show-password']},
     {'stdout': ['^name *not-saved \\(current\\)$',
                 '^server *http://blah$',
                 '^default-namespace *fred/fred$',
                 '^user *RonaldMcDonald$',
                 '^password *abcxdfG$',
                 '^timeout *99$',
                 '^verify *True$',
                 '^certfile *certfile.pem$',
                 '^keyfile *keyfile.pem$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify mixed env var and input options.',
     {'env': {'PYWBEMCLI_DEFAULT_NAMESPACE': 'fred/fred',
              'PYWBEMCLI_USER': 'RonaldMcDonald',
              'PYWBEMCLI_PASSWORD': 'abcxdfG',
              'PYWBEMCLI_TIMEOUT': '99',
              'PYWBEMCLI_NO_VERIFY': 'True',
              'PYWBEMCLI_CERTFILE': 'certfile.pem',
              'PYWBEMCLI_KEYFILE': 'keyfile.pem',
              'PYWBEMCLI_USE_PULL': 'no',
              'PYWBEMCLI_PULL_MAX_CNT': '10',
              'PYWBEMCLI_LOG': 'api=all', },
      'cmdgrp': 'connection',
      'general': ['--server', 'http://blah'],
      'args': ['show', '--show-password']},
     {'stdout': ['^name *not-saved \\(current\\)$',
                 '^server *http://blah$',
                 '^default-namespace *fred/fred$',
                 '^user *RonaldMcDonald$',
                 '^password *abcxdfG$',
                 '^timeout *99$',
                 '^verify *True$',
                 '^certfile *certfile.pem$',
                 '^keyfile *keyfile.pem$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --connection-file general option in interactive mode bad file.',
     {'general': ['--server', 'http://blah', ],
      'stdin': ['--connections-file blah.yaml --name blah connection list']},
     {'stderr': ["Connections file ", "blah.yaml", "does not exist"],
      'test': 'innows'},
     None, OK],

    #
    #  Test setting general options in interactive mode
    #

    ['Verify multiple commands in interacive mode.',
     {'general': ['--server', 'http://blah', ],
      # 'args' not allowed in interactive mode
      'stdin': ['--certfile cert1.pem --keyfile keys1.pem connection show',
                'connection show',
                '--certfile cert2.pem --keyfile keys2.pem connection show',
                'connection show'],             # should show None
      'cmdgrp': 'connection', },
     {'stdout': ['^certfile$',              # at startup and other times
                 '^certfile *cert1.pem$',         # after first change
                 '^certfile *cert2.pem$',         # after second change
                 '^keyfile$',               # at startup and other times
                 '^keyfile *keys1.pem$',
                 '^keyfile *keys2.pem$'],
      'test': 'regex'},
     None, OK],

    ['Verify Change --mock-server to --server in interactive mode.',
     {'general': ['--mock-server', SIMPLE_MOCK_MODEL_FILE_PATH, ],
      # args not allowed in interactive mode
      'stdin': ['connection show',
                '--server  http://blah connection show',
                '--mock-server tests/unit/pywbemcli/simple_mock_model.mof '
                'connection show',
                'connection show'],
      'cmdgrp': None,
      },
     {'stdout': ['^server$',
                 '^server *http://blah$',
                 '^mock-server *.*simple_mock_model.mof$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify Change --server to --mock-server in interactive mode.',
     {'general': ['--server', 'http://blah', ],
      # args not allowed in interactive mode
      'stdin': ['connection show',
                '--mock-server tests/unit/pywbemcli/simple_mock_model.mof '
                '--server  http://blah connection show',
                'connection show',
                'connection show'],
      'cmdgrp': None,
      },
     {'stdout': ["name not-saved (current)"],
      'stderr': ["Conflicting options: `server` is mutually exclusive with "
                 "options: (--mock-server, --name)"],
      'rc': 0,
      'test': 'innows'},
     None, OK],  # TODO: this test fails on windows. Outputs don't compare'

    # TODO: This one now fails because we added test for default conn file.
    ['Verify Change --name invalid in interactive mode. command no connections '
     'file',
     {'general': ['--name', 'NAMEDOESNOTEXIST'],
      'args': ['show'],
      'cmdgrp': 'connection',
      },
     {'stderr': ['Connections file does not exist:',
                 '.pywbemcli_connections.yaml',
                 'Aborted!'],
      'rc': 1,
      'test': 'innows'},
     None, FAIL],

    ['Verify Change --name invalid in interactive mode . stdin. Connection '
     'file exists and we delete',
     {'general': ['--server', 'http://blah'],
      # args not allowed in interactive mode
      'stdin': ['connection save argh',
                '--name NAMEDOESNOTEXIST connection show',
                'connection delete argh'],
      'cmdgrp': None,
      },
     {'stderr': ['Connection definition',
                 'NAMEDOESNOTEXIST',
                 'not found in connections file'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    # Test that interactive --connections-file works. The connections file
    # is set in an interactive command and not there in third command.
    ['Verify --connection-file general option in interactive mode works.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['--server', 'http://initialserver', ],
      'stdin': ['-o table connection show',
                f'-v --connections-file {TEST_CONNECTIONS_FILE_PATH} -n blah '
                'connection list',
                # Show that the original server is restored
                'connection show']},
     {'stdout': ["| name | not-saved (current) |",     # Results, first cmd
                 "| server  | http://initialserver |",
                 # results from second command (defines new connection file)
                 "Connections file loaded",         # test blah.yaml loaded
                 "tmp_general_options.yaml",        # and the name of the file
                 "*blah",                           # test connection list cmd
                 # results from third command (connection show)
                 "name   not-saved (current)",
                 "server http://initialserver", ],
      'test': 'innows'},
     None, OK],

    #
    #   The following is a sequence. Creates a server and changes almost all
    #   parameters interactively. It is run as a sequence so that pywbemcli
    #   is restarted for each test in the sequence
    #
    ['Verify Create a connection for test of mods through general opts. '
     'Sequence 2,1',
     {'general': ['--server', 'http://blah',
                  '--timeout', '45',
                  '--default-namespace', 'root/fred',
                  '--user', 'RonaldMcDonald',
                  '--password', 'pw',
                  '--no-verify',
                  '--certfile', 'certfile.pem',
                  '--keyfile', 'keyfile.pem'],
      'args': ['save', 'testGeneralOpsMods'],
      'cmdgrp': 'connection', },
     {'stdout': "",
      'test': 'innows'},
     None, OK],

    ['Verify show current which is testGeneralOpsMods. Sequence 2,2',
     {'args': ['show', 'testGeneralOpsMods', '--show-password'],
      'cmdgrp': 'connection', },
     {'stdout': ['testGeneralOpsMods',
                 '^server *http://blah$',
                 '^default-namespace *root/fred$',
                 '^user *RonaldMcDonald$',
                 '^password *pw$',
                 '^timeout *45$',
                 '^verify *False$',
                 '^certfile *certfile.pem$',
                 '^keyfile *keyfile.pem$'],
      'test': 'regex'},
     None, OK],

    ['Verify Change server parameters and show result. Sequence 2,3',
     {'general': ['--name', 'testGeneralOpsMods'],
      # args not allowed in interactive mode
      'stdin': ['--timeout 90 --user Fred '
                '--default-namespace root/john --password  abcd '
                ' --verify --certfile c1.pem --keyfile k1.pem '
                'connection show testGeneralOpsMods --show-password'],
      'cmdgrp': None},
     {'stdout': ['testGeneralOpsMods',
                 'server *http://blah$',
                 'default-namespace *root/john$',
                 'user *Fred',
                 'password *abcd',
                 'timeout *90',
                 'verify *True',
                 'certfile *c1.pem',
                 'keyfile *k1.pem'],
      'rc': 0,
      'test': 'regex'},
     None, OK],  # See issue #732

    ['Change all parameters and save as t1. Sequence 2,4',
     {'general': ['--name', 'testGeneralOpsMods', '-v'],
      'stdin': ['--server  http://blahblah --timeout 90 --user Fred '
                '--default-namespace root/john --password  abcd '
                '--verify --certfile c1.pem --keyfile k1.pem connection '
                'save t1', 'connection show t1'],
      'cmdgrp': None},
     {'stdout': [''],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify  load t1 and changed parameters are correct. Sequence 2,5',
     {'general': ['--name', 't1'],
      'args': ['show', '--show-password'],
      'cmdgrp': 'connection'},
     {'stdout': ['t1',
                 '^server *http://blahblah$',
                 '^default-namespace *root/john$',
                 '^user *Fred$',
                 '^password *abcd$',
                 '^timeout *90$',
                 '^verify *True$',
                 '^certfile *c1.pem$',
                 '^keyfile *k1.pem$'
                 ],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Delete testGeneralOpsMods.. Sequence 2,6',
     {'args': ['show', 'ServerDoesNotExist'],
      'cmdgrp': 'connection', },
     {'stderr': "",
      'rc': 1,
      'test': 'innows'},

     None, OK],
    ['Delete testGeneralOpsMods.. Sequence 2,7. Last',
     {'args': ['delete', 'testGeneralOpsMods'],
      'cmdgrp': 'connection', },
     {'stdout': "",
      'test': 'innows'},
     None, OK],

    # End of sequence

    #
    #  Test verbose option
    #
    ['Verify --verbose on by doing a connection show with --verbose',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT_SERVER),
      'general': ['-n', 'realsvr', '--verbose', '-C',
                  TEST_CONNECTIONS_FILE_PATH],
      'args': 'show',
      'cmdgrp': 'connection'},
     {'stdout': ['Connections file loaded:',
                 'server http://blah',
                 'default-namespace root/cimv2',
                 'user ',
                 'timeout 30',
                 'verify True',
                 'certfile ',
                 'keyfile'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify --verbose on by doing a connection show with -v',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT_SERVER),
      'general': ['-n', 'realsvr', '-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'args': 'show',
      'cmdgrp': 'connection'},
     {'stdout': ['Connections file loaded:'],
      'test': 'innows'},
     None, OK],

    ['Verify --no-verbose',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT_SERVER),
      'general': ['-n', 'realsvr', '--no-verbose', '--user', 'fred',
                  '--password', 'abcd', '-C', TEST_CONNECTIONS_FILE_PATH],
      'args': ['show', '--show-password'],
      'cmdgrp': 'connection'},
     {'stdout': ['name blah (current)',
                 'server http://blah',
                 'default-namespace root/cimv2',
                 'user ',
                 'timeout 30',
                 'verify True',
                 'certfile ',
                 'keyfile'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify -verbose but turned off on interactive cmd --show-password',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT_SERVER),
      'general': ['-n', 'realsvr', '--user', 'fred',
                  '--password', 'abcd', '-C', TEST_CONNECTIONS_FILE_PATH],
      'stdin': ['--no-verbose connection show --show-password'],
      'cmdgrp': None},
     {'stdout': ['name  blah  (current)',
                 'server  http://blah',
                 'default-namespace  root/cimv2',
                 'user  fred',
                 'password  abcd',
                 'timeout  30',
                 'verify  True',
                 'certfile',
                 'keyfile'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify  server general options with "" value reset the option to None',
     {'general': ['--server', 'http://blah',
                  '--default-namespace', 'root/blah',
                  '--user', 'fred',
                  '--password', 'blah',
                  '--keyfile', 'mykeyfile.pem',
                  '--certfile', 'mycertfile.pem',
                  '--use-pull', 'yes'],
      'stdin': ['--user "" --password ""  --keyfile "" --certfile "" '
                '--default-namespace ""  --use-pull either connection show'],
      'cmdgrp': None},
     # Test for user and password with no values
     {'stdout': ['default-namespace  root/cimv2',
                 'user password timeout',
                 'certfile keyfile mock-server',
                 'use-pull pull-max-cnt'],
      'rc': 0,
      'test': 'innows'},

     None, OK],

    ['Verify  misc general options with value "" resetting the option to None',
     {'general': ['--server', 'http://blah',
                  '--default-namespace', 'root/blah',
                  '--user', 'fred',
                  '--password', 'blah',
                  '--keyfile', 'mykeyfile.pem',
                  '--certfile', 'mycertfile.pem',
                  '--use-pull', 'yes',
                  '--log', 'all',
                  '--output-format', "table"],
      'stdin': ['--log "" --output-format "" connection show'],
      'cmdgrp': None},
     # Test for user and password with no values
     # NOTE: We cannot really test --log, changes
     {'stdout': ['default-namespace  root/blah'],
      'rc': 0,
      'test': 'innows'},
     None, RUN],

    # NOTE: Other tests for --log option in interactive mode in test_log_option

    #
    #  Test that bad mock_error file names do not cause Abort but bad MOF
    #  or python script do cause Abort
    #
    ['Verify interactive create mock with bad file name does not fail.',
     {'connections_file_args': ('tmpconfig.yaml', None),
      'general': ['--server', 'http://blah', '--user', 'fred', '--password',
                  'fred', '-C', 'tmpconfig.yaml'],
      'stdin': ['connection save connectiontoprovestdincontinues',
                '--mock-server DoesNotExist.mof class enumerate',
                '-m DoesNotExist.py class enumerate',
                'connection select connectiontoprovestdincontinues',
                'connection show',
                'connection delete connectiontoprovestdincontinues']},
     {'stdout': ['connectiontoprovestdincontinues (current)',
                 'server http://blah',
                 'default-namespace root/cimv2',
                 'user fred',
                 'Deleted default connection '
                 '"connectiontoprovestdincontinues"'],
      'stderr': ['DoesNotExist.mof',
                 'DoesNotExist.py',
                 'does not exist'],
      'test': 'innows'},
     None, OK],

    # TODO this test fails on windows because the statement that builds the
    # --mock-server ... class enumerate inserts the filepath without
    # the backslashes. This is a windows issue, and problem occurs for both
    # python 2 and 3
    ['Verify interactive MOF or PY failures don"t cause Abort.',
     {'general': [],
      'stdin': ['--server http://blah --user fred --password fred '
                'connection save fred',
                f'--mock-server {BAD_MOF_FILE_PATH} class enumerate',
                'connection select fred',
                'connection show',
                'connection delete fred'],
      'platform': 'win32'},  # ignore this platform.  See comments above
     {'stdout': ['Deleted connection "fred"'],
      'rc': 0,
      'test': 'not-innows'},
     None, OK],

    # NOTE Test ignored on windows because of issue in previous test
    # This test depends on the previous one
    ['Delete fred. This one will fail if previous does not abort',
     {'general': [],
      'args': ['delete', 'fred'],
      'cmdgrp': 'connection',
      'platform': 'win32'},  # ignore this platform.  See comments above
     {'stderr': 'Connection definition "fred" not found in connections file',
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify operation that makes request to WBEM server fails with no server.',
     {'args': ['enumerate'],
      'cmdgrp': 'class', },
     {'stderr': "No current server for command ",
      'rc': 1,
      'test': 'innows'},
     None, OK],

    #
    #  Verify operation that tries interactive general options for name
    #  and server/mock server fails.
    #

    ['Test conflicting server definitions interactive mode --mock-server.',
     {'stdin': ['--server http://blah --mock-server '
                'tests/unit/pywbemcli/simple_mock_model.mof']},
     {'stderr': "Conflicting options: `server` is mutually exclusive with "
                "options: (--mock-server, --name)",
      'rc': 0,
      'test': 'innows'},
     None, OK],

    # Test of ways to execute same simple command. Creates a mock
    # and tests combination of single command. Uses -v to test for
    # Connect and disconnect

    ['Verify new config file with defined data is created and saved.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH, None),
      'general': ['-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'stdin': ['connection save blah',   # saves SIMPLE_MOCK_MODEL as blah
                'connection show']},
     {'stdout': ['default-namespace root/cimv2'],
      'test': 'innows'},
     SIMPLE_MOCK_MODEL_FILE_PATH, OK],

    ['Verify simple pywbem command against file works and verbose connect and '
     'disconnect work.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-n', 'blah', '-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'args': ['enumerate', '--di', '--no', '--subclass-of', 'CIM_Foo_sub'],
      'cmdgrp': 'class'},
     {'stdout': ["Connecting to mock environment",
                 'CIM_Foo_sub_sub',
                 "Disconnecting from mock environment"],
      'test': 'innows'},
     None, OK],

    ['Verify simple pywbem command with stdin on same connection name.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-n', 'blah', '-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'stdin': ['class enumerate --di --no --subclass-of CIM_Foo_sub']},
     {'stdout': ["Connections file loaded: tmp_general_options.yaml",
                 "Connecting to mock environment",
                 'CIM_Foo_sub_sub',
                 "Disconnecting from mock environment"],
      'test': 'innows'},
     None, OK],

    ['Verify cmd with --name option in stdin.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-n', 'blah', '-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'stdin': ['-n blah -v class enumerate --di --no '
                '--subclass-of CIM_Foo_sub']},
     {'stdout': ["Connecting to mock environment",
                 'CIM_Foo_sub_sub',
                 "Disconnecting from mock environment"],
      'test': 'innows'},
     None, OK],

    ['Verify interactive delete connection name does not fail.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT),
      'general': ['-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'stdin': ['connection delete blah']},
     {'stdout': ['Deleted connection "blah"'],
      'test': 'innows', },
     None, OK],

    ['Verify new config file with defined server is created with additional '
     'options.',
     {'general': ['-v',
                  '--server', 'http://blah', '--user', 'fred',
                  '--password', 'fred', '--timeout', '90', '-d', 'root/cimv3',
                  '--no-verify', '--certfile', 'certfile.pem',
                  '--keyfile', 'keyfile.pem', '--ca-certs', 'blah',
                  '--use-pull', 'no', '--pull-max-cnt', '222'],
      'stdin': ['connection show']},
     {'stdout': ['default-namespace root/cimv3',
                 'server http://blah',
                 'user fred',
                 'timeout 90',
                 'verify False',
                 'use-pull False',
                 'pull-max-cnt 222',
                 'certfile certfile.pem',
                 'keyfile keyfile.pem',
                 'ca-certs  blah'],
      'test': 'innows'},
     None, OK],

    # Test of interactive change of all server options.  Creates server,
    # modifies server options in interactive cmd with connection show,
    # does second connection show to test for original parameters
    ['Verify created server with interactive modify server options works.',
     {'general': ['-v', '--server', 'http://blah', '--user', 'fred',
                  '--password', 'fred', '--timeout', '90', '-d', 'root/cimv3',
                  '--no-verify', '--certfile', 'certfile.pem',
                  '--keyfile', 'keyfile.pem', '--ca-certs', 'blah',
                  '--use-pull', 'no', '--pull-max-cnt', '222'],
      'stdin': ['--server http://blah2 --user john '
                '--password john --timeout 45 -d root/cimv4 '
                '--verify --certfile certfile2.pem '
                '--keyfile keyfile2.pem --ca-certs blah2 '
                '--use-pull yes --pull-max-cnt 444 '
                'connection show',                       # first cmd
                'connection show']},                     # second cmd
     {'stdout': ['default-namespace root/cimv4',  # params from first cmd
                 'server http://blah2',
                 'user john',
                 'timeout 45',
                 'verify True',
                 'use-pull True',
                 'pull-max-cnt 444',
                 'certfile certfile2.pem',
                 'keyfile keyfile2.pem',
                 'ca-certs  blah2',
                 'default-namespace root/cimv3',  # params from second cmd
                 'server http://blah',
                 'user fred',
                 'timeout 90',
                 'verify False',
                 'use-pull False',
                 'pull-max-cnt 222',
                 'certfile certfile.pem',
                 'keyfile keyfile.pem',
                 'ca-certs  blah'],
      'test': 'innows'},
     None, OK],

    ['Verify --name  with all server general_options modified in interactive '
     'cmd.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT_SERVER),
      'general': ['-n', 'realsvr', '-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'stdin': ['--server http://blah2 --user john '
                '--password john --timeout 45 -d root/cimv4 '
                '--no-verify --certfile certfile2.pem '
                '--keyfile keyfile2.pem --ca-certs blah2 '
                '--use-pull yes --pull-max-cnt 444 '
                'connection show',                       # first cmd
                'connection show']},
     {'stdout': ['default-namespace root/cimv4',  # params from first show cmd
                 'server http://blah2',
                 'user john',
                 'timeout 45',
                 'verify False',
                 'use-pull True',
                 'pull-max-cnt 444',
                 'certfile certfile2.pem',
                 'keyfile keyfile2.pem',
                 'ca-certs  blah2',
                 'default-namespace root/cimv2',  # params from second show
                 'server http://blah',
                 'user',
                 'timeout 30',
                 'verify False',
                 'use-pull True',
                 'pull-max-cnt 1000',
                 'certfile',
                 'keyfile',
                 'ca-certs'],
      'test': 'innows'},
     None, OK],

    ['Verify cmd with --name and all server option modifications.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT_SERVER),
      'general': ['-n', 'realsvr', '-v', '-C', TEST_CONNECTIONS_FILE_PATH,
                  '--user', 'john',
                  '--password', 'john', '--timeout', '45', '-d', 'root/cimv4',
                  '--no-verify', '--certfile', 'certfile2.pem',
                  '--keyfile', 'keyfile2.pem', '--ca-certs', 'blah2',
                  '--use-pull', 'yes', '--pull-max-cnt', '444',
                  'connection', 'show']},
     {'stdout': ['default-namespace root/cimv4',
                 'server http://blah',
                 'user  john',
                 'timeout 45',
                 'verify False',
                 'use-pull True',
                 'pull-max-cnt 444',
                 'certfile certfile2.pem',
                 'keyfile  keyfile2.pem',
                 'ca-certs blah2'],
      'test': 'innows'},
     None, OK],

    ['Verify default name request where default name not in repo fails.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                {'connection_definitions': {
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
                                        'mock-server': []}},
                                 'default_connection_name': 'DoesNotExist'}
                                ),
      'general': ['-v', '-C', TEST_CONNECTIONS_FILE_PATH, 'connection',
                  'show']},
     {'stderr': ['Default connection name: "DoesNotExist" not found in '
                 'connections file'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify request with invalid connection file name fails.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH, None),
      'general': ['-n', 'blah', '-v', '-C', TEST_CONNECTIONS_FILE_PATH,
                  'connection', 'show']},
     {'stderr': ['Connections file does not exist: tmp_general_options.yaml'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    # pylint: disable=line-too-long

    ['Verify multiple defs with interactive cmds'
     'cmd.',
     {'connections_file_args': (TEST_CONNECTIONS_FILE_PATH,
                                TEST_CONNECTIONS_FILE_DICT_SERVER),
      'general': ['-n', 'realsvr', '-v', '-C', TEST_CONNECTIONS_FILE_PATH],
      'stdin': ['--server http://realsvr1 --user john '         # define 2nd svr
                '--password john --timeout 45 -d root/cimv4 '
                '--no-verify --certfile certfile2.pem '
                '--keyfile keyfile2.pem --ca-certs blah2 '
                '--use-pull yes --pull-max-cnt 444',
                'connection save realsvr1',                       # scnd svr
                '--server http://realsvr2 --user fred --pull-max-cnt 999 '
                '--timeout 90 -d root/cim5 --use-pull no',
                'connection save realsvr2',                       # third svr
                'connection list --full ']},
     {'stdout': """
WBEM server connections(full): (#: default, *: current)
file: tmp_general_options.yaml
name  server   namespace user  timeout use-pull  pull-max-cnt verify certfile  keyfile  mock-server
-------- --------------- ----------- ------ --------- ---------- -------------- -------- ------------- ------------ -------------
*blah     http://realsvr2  root/cim5    fred           90  False                  999  False     certfile2.pem  keyfile2.pem
*realsvr  http://blah      root/cimv2                  30                        1000  True
realsvr1  http://realsvr1  root/cimv4   john           45  True                   444  False     certfile2.pem  keyfile2.pem
realsvr2  http://realsvr2  root/cim5    fred           90  False                  999  False     certfile2.pem  keyfile2.pem

""",  # noqa: E501
      'test': 'innows'},
     None, RUN],
    # pylint: enable=line-too-long

]

# TODO add test for pull operations with pull ops max size variations
# There is one in test_generaloptions for size 1 that tests results with
# statistics report.


class TestGeneralOptions(CLITestsBase):
    # pylint: disable=too-few-public-methods
    """
    Test the general options including statistics,  --server,
    --timeout, --use-pull, --pull-max-cnt, --output-format
    """
    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition", TEST_CASES)
    def test_execute_pywbemcli(self, desc, inputs, exp_response, mock,
                               condition):
        """
        Execute pybemcli with the defined input and test output.
        """
        # Temp bypass of windows platform because of issue with one test
        if 'platform' in inputs:
            if sys.platform == inputs['platform']:
                return

        cmd_grp = inputs['cmdgrp'] if 'cmdgrp' in inputs else ''

        self.command_test(desc, cmd_grp, inputs, exp_response,
                          mock, condition)
