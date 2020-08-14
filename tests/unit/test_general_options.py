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

from __future__ import absolute_import, print_function

import os
import sys
import pytest
import pywbem

from pywbemtools.pywbemcli._connection_repository import CONNECTIONS_FILENAME

from .cli_test_extensions import CLITestsBase, PYWBEM_0, PYWBEM_1
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE

SCRIPT_DIR = os.path.dirname(__file__)

SIMPLE_MOCK_FILE_PATH = os.path.join(SCRIPT_DIR, 'simple_mock_model.mof')
PYTHON_MOCK_FILE_PATH = os.path.join(SCRIPT_DIR, 'simple_python_mock_script.py')
BAD_MOF_FILE_PATH = os.path.join(SCRIPT_DIR, 'mof_with_error.mof')
BAD_PY_FILE_PATH = os.path.join(SCRIPT_DIR, 'py_with_error.py')
BAD_PY_ERR_STRTUP_PATH = os.path.join(SCRIPT_DIR, 'py_err_processatstartup.py')
MOCK_PW_PROMPT_PATH = os.path.join(SCRIPT_DIR, 'mock_password_prompt.py')

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
      PYWBEMCLI_TERMWIDTH environment variable.

      For more detailed documentation, see:

      https://pywbemtools.readthedocs.io/en/stable/""",
    CMD_OPTION_HELP_HELP_LINE,
    "General Options:",
    "-n, --name NAME Use the WBEM server defined by the WBEM",
    "-m, --mock-server FILE  Use a mock WBEM server that is automatically",
    "-s, --server URL  Use the WBEM server at the specified URL with",
    "-u, --user TEXT   User name for the WBEM server. Default: EnvVar",
    "-p, --password TEXT  Password for the WBEM server. Default: EnvVar",
    "--verify / --no-verify  If --verify, client verifies the X.509 server",
    "--ca-certs CACERTS  Certificates used to validate the certificate",
    "-c, --certfile FILE  Path name of a PEM file containing a X.509",
    "-t, --timeout INT  Client-side timeout in seconds for operations",
    "-U, --use-pull [yes|no|either] Determines whether pull operations are ",
    "--pull-max-cnt INT  Maximum number of instances to be returned by",
    "-T, --timestats   Show time statistics of WBEM server",
    "-d, --default-namespace NAMESPACE Default namespace, to be used when ",
    "-o, --output-format FORMAT Output format for the command result. The",
    "-l, --log COMP[=DEST[:DETAIL]]",
    "Enable logging of the WBEM operations,",
    "-C, --connections-file FILE PATH Path name of the connections file",
    CONNECTIONS_FILENAME,
    "-v, --verbose / --no-verbose Display extra information about the",
    "--deprecation-warnings / --no-deprecation-warnings",
    "--pdb    Pause execution in the built-in pdb debugger",
    "--version   Show the version of this command and the",
    """Commands:
      class       Command group for CIM classes.
      instance    Command group for CIM instances.
      profile     Command group for WBEM management profiles.
      qualifier   Command group for CIM qualifier declarations.
      server      Command group for WBEM servers.
      connection  Command group for WBEM connection definitions.
      help        Show help message for interactive mode.
      repl        Enter interactive mode (default)."""
]

# pylint: disable=line-too-long
REPL_HELP = """Usage: pywbemcli [GENERAL-OPTIONS] repl

  Enter interactive mode (default).

  Enter the interactive mode where pywbemcli commands can be entered interactively. The prompt is changed to 'pywbemcli>'.

  Command history is supported. The command history is stored in a file ~/.pywbemcli_history.

  Pywbemcli may be terminated from this mode by entering <CTRL-D>, :q, :quit, :exit

  In the repl mode, <CTRL-r> man be used to initiate an interactive search of the history file.

  Interactive mode also includes an autosuggest feature that makes suggestions from the command history as the command the user types in the
  command and options.

Command Options:
  -h, --help  Show this help message.

"""  # noqa: E501

INTERACTIVE_HELP = """
The following can be entered in interactive mode:

  COMMAND                     Execute pywbemcli command COMMAND.
  !SHELL-CMD                  Execute shell command SHELL-CMD.
  <CTRL-D>, :q, :quit, :exit  Exit interactive mode.
  <CTRL-r>  <search string>   To search the  command history file.
                              Can be used with <UP>, <DOWN>
                              to display commands that match the search string.
                              Editing the search string updates the search.
  <TAB>                       Tab completion (can be used anywhere).
  -h, --help                  Show pywbemcli general help message, including a
                              list of pywbemcli commands.
  COMMAND --help              Show help message for pywbemcli command COMMAND.
  help                        Show this help message.
  :?, :h, :help               Show help message about interactive mode.
  <UP>, <DOWN>                Scroll through pwbemcli command history.

  COMMAND: May be two words (class enumerate) for commands that are within
  a group or a single word for special commands like `repl` that are not in
  a group.
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

    ['Verify help response (interactive help)).',
     {'general': [],
      'cmdgrp': 'help',
      'args': []},
     {'stdout': INTERACTIVE_HELP,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify invalid server definition.',
     {'general': ['-s', 'httpx://blah'],
      'cmdgrp': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['Error: Invalid scheme on server argument. httpx://blah Use '
                 '"http" or "https"'],
      'rc': 1,
      'test': 'in'},
     None, OK],

    ['Verify invalid server port definition fails. pywbem version 0.x',
     {'general': ['-s', 'http://blah:abcd'],
      'cmdgrp': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['Error:', 'ConnectionError',
                 'Failed to parse'
                 if getattr(pywbem, 'PYWBEM_USES_REQUESTS', False)
                 else 'Socket error'],
      'rc': 1,
      'test': 'regex'},
     None, PYWBEM_0],

    ['Verify invalid server port definition fails. pywbem version 1',
     {'general': ['-s', 'http://blah:abcd'],
      'cmdgrp': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['ValueError:', "Invalid port number 'abcd' in URL "
                 "'http://blah:abcd'"],
      'rc': 1,
      'test': 'innows'},
     None, PYWBEM_1],


    ['Verify valid --use-pull option parameter yes.',
     {'general': ['-s', 'http://blah', '--use-pull', 'yes'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull True'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify valid --server and --mock-server invalid.',
     {'general': ['--server', 'http://blah', '--mock-server',
                  SIMPLE_MOCK_FILE_PATH],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Conflicting server definitions:',
                 'mock-server:', 'simple_mock_model.mof',
                 'server:', 'http://blah'],
      'rc': 1,
      'test': 'in'},
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
     {'stdout': ['use-pull pull-max-cnt verify'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify invalid --use-pull option parameter fails.',
     {'general': ['-s', 'http://blah', '--use-pull', 'blah'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Invalid value', '-U', '--use-pull',
                 'invalid choice: blah. (choose from yes, no, either)'],
      'rc': 2,
      'test': 'innows'},
     None, OK],

    ['Verify valid --pull-max-cnt option parameter.',
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
                 'blah is not a valid integer'],
      'rc': 2,
      'test': 'innows'},
     None, OK],  # Only tests that the option is accepted

    ['Verify --no-deprecation-warnings general option.',
     {'general': ['-s', 'http://blah', '--no-deprecation-warnings'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': [''],
      'rc': 0,
      'test': 'innows'},
     None, OK],  # Only tests that the option is accepted


    ['Verify --deprecation-warnings general option.',
     {'general': ['-s', 'http://blah', '--deprecation-warnings'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stdout': [''],
      'rc': 0,
      'test': 'innows'},
     None, OK],

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
     {'general': ['-m', SIMPLE_MOCK_FILE_PATH],
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
     {'general': ['-m', SIMPLE_MOCK_FILE_PATH,
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
     {'stderr': ['Error: Mock file ',
                 'invalidfilename.mof',
                 ' does not exist'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server option, file with bad extension',
     {'general': ['--mock-server', 'invalidfilename.mofx'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Mock file ',
                 'invalidfilename.mofx',
                 ' has invalid suffix'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify -m option, file with mof containing syntax error',
     {'general': ['-m', BAD_MOF_FILE_PATH],
      'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stdout': "^^^^^^^^^^" if PYWBEM_0 else "",
      'stderr': ['MOF compile failed:',
                 BAD_MOF_FILE_PATH,
                 "^^^^^^^^^^" if PYWBEM_1 else "(see above)",
                 'Aborted!'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify -m option, file with python containing syntax error',
     {'general': ['-m', BAD_PY_FILE_PATH],
      'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stderr': [r'Traceback \(most recent call last\)',
                 r'pywbemtools', r'_pywbemcli_operations\.py',
                 r'line ', 'in build_repository',
                 r"NameError: name 'globalsx' is not defined",
                 'Aborted'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify -m option, file with python startup file containing syntax error',
     {'general': ['-m', SIMPLE_MOCK_FILE_PATH],
      'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stderr': ['Mock Python process-at-startup',
                 'Traceback (most recent call last)',
                 'pywbemtools', 'pywbemcli.py',
                 'line ', 'in cli',
                 'py_err_processatstartup.py',
                 'def mock?prompt(msg):',
                 'SyntaxError: invalid syntax'],
      'rc': 1,
      'test': 'innows'},
     BAD_PY_ERR_STRTUP_PATH, OK],

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

    # TODO: Add test where file exists.

    ['Verify simultaneous --mock-server and --server options fail',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                  '--server', 'http://localhost'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Error: Conflicting server definitions:',
                 'mock-server:', SIMPLE_MOCK_FILE_PATH,
                 'server:', 'http://localhost'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server invalid name',
     {'general': ['--mock-server', 'fred'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Error: Mock file',
                 'fred',
                 'has invalid suffix'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify -m option one file and name fails',
     {'general': ['-m', SIMPLE_MOCK_FILE_PATH, '--name', 'MyConnName'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Error: Conflicting server definitions:',
                 'mock-server:', SIMPLE_MOCK_FILE_PATH,
                 'name:', 'MyConnName'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --timestats',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '--timestats'],
      'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stdout': ['class CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 'EnumerateClasses'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify --timestats -T',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '-T'],
      'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stdout': ['class CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 'EnumerateClasses'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify uses pull Operation  with option either',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                  '--timestats',
                  '--use-pull', 'either'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': ['instance of CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 ' OpenEnumerateInstances'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify uses pull Operation with option yes',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                  '--timestats',
                  '--use-pull', 'yes'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': ['instance of CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 ' OpenEnumerateInstances'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify uses pull Operation with option no',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                  '--timestats',
                  '--use-pull', 'no'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': ['instance of CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 ' EnumerateInstances'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify --mock-server and -server not allowed',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                  '--server', 'http://blah'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stderr': ['Error: Conflicting server definitions:',
                 'mock-server:', SIMPLE_MOCK_FILE_PATH,
                 'server:', 'http://blah'],
      'rc': 1,
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

    ['Verify -n option with non-existent connection file fails',
     {'general': ['-n', 'namedoesnotexist'],
      'cmdgrp': 'connection',
      'args': ['show']},
     {'stderr': ['Connection name', 'namedoesnotexist',
                 'not found in connections file',
                 CONNECTIONS_FILENAME],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --name and other options fails',
     {'general': ['--name', 'generaltest1', '--timeout', '90'],
      'cmdgrp': 'connection',
      'args': ['delete', 'generaltest1']},
     {'stderr': ['timeout 90', 'invalid when'],
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
     {'stderr': ['Connection repository',
                 CONNECTIONS_FILENAME,
                 'does not exist'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify connection without server definition and command that '
     ' requires a connection actually fails.',
     {'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stderr': ['No server specified for a command that requires a WBEM '
                 'server. To specify a server, use the "--server", '
                 '"--mock-server", or "--name" general options, or set the '
                 'corresponding environment variables, or in interactive mode '
                 'use "connection select"'],
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

    #
    #   Verify password prompt. This is a sequence
    #
    ['Create a mock serve with user but no password.',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                  '--user', 'john'],
      'args': ['save', 'mocktestVerifyPWPrompt'],
      'cmdgrp': 'connection', },
     {'stdout': "",
      'test': 'innows'},
     None, OK],

    ['Verify server in repository',
     {'general': [],
      'cmdgrp': 'connection',
      'args': ['list']},
     {'stdout': ['mocktestVerifyPWPrompt'],
      'test': 'innows'},
     MOCK_PW_PROMPT_PATH, OK],

    ['Verify load of this server and class enumerate triggers password prompt',
     {'general': ['--name', 'mocktestVerifyPWPrompt'],
      'cmdgrp': 'class',
      'args': ['enumerate']},
     {'stdout': ['CIM_Foo'],
      'test': 'innows'},
     MOCK_PW_PROMPT_PATH, OK],

    ['Delete our test server',
     {'general': ['--name', 'mocktestVerifyPWPrompt'],
      'cmdgrp': 'connection',
      'args': ['delete', 'mocktestVerifyPWPrompt']},
     {'stdout': ['Deleted'],
      'test': 'innows'},
     None, OK],

    ['Create a mock server with user but no password. stdin to test for prompt',
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                  '--user', 'john'],
      'stdin': ['class enumerate']},
     {'stdout': ['MOCK_CLICK_PROMPT Enter password',
                 '(user john)',
                 'class CIM_Foo {'],
      'test': 'innows'},
     MOCK_PW_PROMPT_PATH, OK],

    #
    #  The following is a sequence that tests use of default connection
    #  Creates server and saves. Tests that save works and then uses
    #  select to set the default server to this connection
    #  Tests that pywbemcli execute with no --name, etc. gets the default.
    #  Removes the connection
    #

    ['Create a connection to test default connection.',
     {'general': ['--server', 'http://blah'],
      'args': ['save', 'test-default'],
      'cmdgrp': 'connection', },
     {'stdout': '',
      'test': 'innows'},
     None, OK],

    ['Verify select of test-default.',
     {'args': ['select', 'test-default'],
      'cmdgrp': 'connection', },
     {'stdout': ['test-default', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify show test-default connection.',
     {'args': ['show', 'test-default'],
      'cmdgrp': 'connection', },
     {'stdout': ['test-default'],
      'test': 'innows'},
     None, OK],

    ['Verify select of test-default connection.',
     {'args': ['select', 'test-default', '--default'],
      'cmdgrp': 'connection', },
     {'stdout': ['test-default', 'current'],
      'test': 'innows'},
     None, OK],

    ['Verify show current which is test-default',
     {'args': ['show'],
      'cmdgrp': 'connection', },
     {'stdout': ['test-default'],
      'test': 'innows'},
     None, OK],

    ['Verify show current which is test-default because it loads the default',
     {'general': ['--verbose'],
      'args': ['show'],
      'cmdgrp': 'connection', },
     {'stdout': ['Current connection: "test-default"'],
      'test': 'innows'},
     None, OK],

    ['Delete test-default.',
     {'args': ['delete', 'test-default'],
      'cmdgrp': 'connection', },
     {'stdout': "",
      'test': 'innows'},
     None, OK],

    ['Verify delete worked by requesting again expecting failure.',
     {'args': ['delete', 'test-default'],
      'cmdgrp': 'connection', },
     {'stderr': ['Connection  repository',
                 CONNECTIONS_FILENAME,
                 'does not exist'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    # End of sequence - There should be no connections file

    #
    # Test using environment variables as input
    #
    ['Verify setting one env var for input.',
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
     {'general': ['--mock-server', SIMPLE_MOCK_FILE_PATH, ],
      # args not allowed in interactive mode
      'stdin': ['connection show',
                '--server  http://blah connection show',
                '--mock-server tests/unit/simple_mock_model.mof '
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
                '--mock-server tests/unit/simple_mock_model.mof '
                '--server  http://blah connection show',
                'connection show',
                'connection show'],
      'cmdgrp': None,
      },
     {'stderr': ['Conflicting server definitions:',
                 'http://blah',
                 'mock-server: tests/unit/simple_mock_model.mof'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify Change --name in interactive mode, name invalid. command',
     {'general': ['--name', 'NAMEDOESNOTEXIST'],
      'args': ['show'],
      'cmdgrp': 'connection',
      },
     {'stderr': ['Connections file does not exist:',
                 '.pywbemcli_connections.yaml',
                 'Aborted'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify Change --name in interactive mode, name invalid stdin.',
     {'general': ['--server', 'http://blah'],
      # args not allowed in interactive mode
      'stdin': ['--name NAMEDOESNOTEXIST connection show'],
      'cmdgrp': None,
      },
     {'stderr': ['Fatal error loading connections file',
                 '.pywbemcli_connections.yaml',
                 'Aborted'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    #
    #   The following is a sequence. Creates a server and changes almost all
    #   parameters interactively.
    #
    ['Verify Create a connection for test of mods through general opts.',
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

    ['Verify show current which is testGeneralOpsMods',
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

    ['Verify Change server parameters and show result.',
     {'general': ['--name', 'testGeneralOpsMods'],
      # args not allowed in interactive mode
      'stdin': ['--timeout 90 --user Fred '
                '--default-namespace root/john --password  abcd '
                ' --verify --certfile c1.pem --keyfile k1.pem '
                'connection select testGeneralOpsMods',
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
     None, FAIL],  # See issue #732

    ['Change all parameters and save as t1.',
     {'general': ['--name', 'testGeneralOpsMods'],
      # args not allowed in interactive mode
      'stdin': ['--server  http://blahblah --timeout 90 --user Fred '
                '--default-namespace root/john --password  abcd '
                ' --verify --certfile c1.pem --keyfile k1.pem connection '
                'save t1',
                'connection list'],
      'cmdgrp': None},
     {'stdout': [''],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify  load t1 and changed parameters are correct',
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

    ['Delete testGeneralOpsMods.',
     {'args': ['show', 'ServerDoesNotExist'],
      'cmdgrp': 'connection', },
     {'stderr': "",
      'rc': 1,
      'test': 'innows'},

     None, OK],
    ['Delete testGeneralOpsMods.',
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
     {'general': ['--name', 't1', '--verbose'],
      'args': 'show',
      'cmdgrp': 'connection'},
     {'stdout': ['t1',
                 '^server *http://blahblah$',
                 '^default-namespace *root/john$',
                 '^user *Fred$',
                 '^timeout *90$',
                 '^verify *True$',
                 '^certfile *c1.pem$',
                 '^keyfile *k1.pem$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --verbose on by doing a connection show with -v',
     {'general': ['--name', 't1', '-v'],
      'args': 'show',
      'cmdgrp': 'connection'},
     {'stdout': ['t1',
                 '^server *http://blahblah$',
                 '^default-namespace *root/john$',
                 '^user *Fred$',
                 '^timeout *90$',
                 '^verify *True$',
                 '^certfile *c1.pem$',
                 '^keyfile *k1.pem$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --no-verbose',
     {'general': ['--name', 't1', '--no-verbose'],
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
                 '^keyfile *k1.pem$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify -verbose but turned off on interactive cmd --show-password',
     {'general': ['--name', 't1', '-v'],
      'stdin': ['--no-verbose connection show --show-password'],
      'cmdgrp': None},
     {'stdout': ['t1',
                 '^server *http://blahblah$',
                 '^default-namespace *root/john$',
                 '^user *Fred$',
                 '^password *abcd$',
                 '^timeout *90$',
                 '^verify *True$',
                 '^certfile *c1.pem$',
                 '^keyfile *k1.pem$'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify -verbose but turned off on interactive cmd',
     {'general': ['--name', 't1', '-v'],
      'stdin': ['--no-verbose connection show'],
      'cmdgrp': None},
     {'stdout': ['COMMAND', 'params='],
      'rc': 0,
      'test': 'not-innows'},
     None, OK],

    ['Delete testGeneralOpsMods.',
     {'args': ['delete', 't1'],
      'cmdgrp': 'connection', },
     {'stdout': "",
      'test': 'innows'},
     None, OK],

    #
    #  Test that bad mock_error file names do not cause Abort but bad MOF
    #  or python script do cause Abort
    #

    ['Verify interactive create mock with bad file name does not fail.',
     {'general': [],
      'stdin': ['--server http://blah --user fred --password fred '
                ' connection save connectiontoprovestdincontinues',
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
    ['Verify interactive MOF or PY failures causes Abort.',
     {'general': [],
      'stdin': ['--server http://blah --user fred --password fred ',
                'connection save fred',
                '--mock-server {} class enumerate'.format(BAD_MOF_FILE_PATH),
                'connection select fred',
                'connection show',
                'connection delete fred'],
      'platform': 'win32'},  # ignore this platform.  See comments above
     {'stdout': ['Deleted connection "fred"'],
      'rc': 1,
      'test': 'not-innows'},
     None, OK],

    # NOTE That we are not using this because of possible issue with previous
    # test and windows.  Enable this before we add any more tests in future.
    ['Delete fred. This one will fail if previous does not abort',
     {'general': [],
      'args': ['delete', 'fred'],
      'cmdgrp': 'connection', },
     {'stdout': "",
      'test': 'innows'},
     None, FAIL],


    ['Verify operation that makes request to WBEM server fails with no server.',
     {'args': ['enumerate'],
      'cmdgrp': 'class', },
     {'stderr': "No server specified for a command that requires a WBEM server",
      'rc': 1,
      'test': 'innows'},
     None, OK],

    #
    #  Verify operation that tries interactive general options for name
    #  and server/mock server fails
    #

    ['Test conflicting server defintions interactive mode.',
     {'stdin': ['--server http://blah --name blah connection show']},
     {'stderr': "Conflicting server definitions:",
      'rc': 0,
      'test': 'innows'},
     None, OK],
]

# TODO add test for pull operations with pull ops max size variations


class TestGeneralOptions(CLITestsBase):
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
