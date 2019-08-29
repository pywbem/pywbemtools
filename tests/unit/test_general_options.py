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
import pytest

from .cli_test_extensions import CLITestsBase

SCRIPT_DIR = os.path.dirname(__file__)

SIMPLE_MOCK_FILE_PATH = os.path.join(SCRIPT_DIR, 'simple_mock_model.mof')
PYTHON_MOCK_FILE_PATH = os.path.join(SCRIPT_DIR, 'simple_python_mock_script.py')
BAD_MOF_FILE_PATH = os.path.join(SCRIPT_DIR, 'mof_with_error.mof')
BAD_PY_FILE_PATH = os.path.join(SCRIPT_DIR, 'py_with_error.py')


GLOBAL_HELP = """
Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...

  Pywbemcli is a command line WBEM client that uses the DMTF CIM-XML
  protocol to communicate with WBEM servers. Pywbemcli can:

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

  For more detailed documentation, see:

      https://pywbemtools.readthedocs.io/en/stable/

Options:
  -n, --name NAME                 Use the WBEM server defined by the
                                  persistent WBEM connection NAME. This option
                                  is mutually exclusive with the --server and
                                  --name options, since each defines a WBEM
                                  server. Default: EnvVar PYWBEMCLI_NAME, or
                                  none.
  -m, --mock-server FILE          Use a mock WBEM server that is created under
                                  the covers and populated with CIM objects
                                  that are defined in the specified MOF file
                                  or Python script file. See the pywbemcli
                                  documentation for more information. This
                                  option may be specified multiple times, and
                                  is mutually exclusive with the --server and
                                  --name options, since each defines a WBEM
                                  server. Default: EnvVar
                                  PYWBEMCLI_MOCK_SERVER, or none.
  -s, --server URL                Use the WBEM server at the specified URL of
                                  format: [SCHEME://]HOST[:PORT]. SCHEME must
                                  be "https" (default) or "http". HOST is a
                                  short or long hostname or literal IPV4/v6
                                  address. PORT defaults to 5989 for https and
                                  5988 for http. This option is mutually
                                  exclusive with the --mock-server and --name
                                  options, since each defines a WBEM server.
                                  Default: EnvVar PYWBEMCLI_SERVER, or none.
  -u, --user TEXT                 User name for the WBEM server. Default:
                                  EnvVar PYWBEMCLI_USER, or none.
  -p, --password TEXT             Password for the WBEM server. Default:
                                  EnvVar PYWBEMCLI_PASSWORD, or prompted for
                                  if --user specified.
  -N, --no-verify                 If true, client does not verify the X.509
                                  server certificate presented by the WBEM
                                  server during TLS/SSL handshake. Default:
                                  EnvVar PYWBEMCLI_NO_VERIFY, or false.
  --ca-certs FILE                 Path name of a file or directory containing
                                  certificates that will be matched against
                                  the server certificate presented by the WBEM
                                  server during TLS/SSL handshake. Default:
                                  EnvVar PYWBEMCLI_CA_CERTS, or [/etc/pki/ca-
                                  trust/extracted/openssl/ca-bundle.trust.crt,
                                  /etc/ssl/certs, /etc/ssl/certificates].
  -c, --certfile FILE             Path name of a PEM file containing a X.509
                                  client certificate that is used to enable
                                  TLS/SSL 2-way authentication by presenting
                                  the certificate to the WBEM server during
                                  TLS/SSL handshake. Default: EnvVar
                                  PYWBEMCLI_CERTFILE, or none.
  -k, --keyfile FILE              Path name of a PEM file containing a X.509
                                  private key that belongs to the certificate
                                  in the --certfile file. Not required if the
                                  private key is part of the --certfile file.
                                  Default: EnvVar PYWBEMCLI_KEYFILE, or none.
  -t, --timeout INT               Client-side timeout in seconds for
                                  operations with the WBEM server. Default:
                                  EnvVar PYWBEMCLI_TIMEOUT, or 30.
  -U, --use-pull [yes|no|either]  Determines whether pull operations are used
                                  for operations with the WBEM server that
                                  return lists of instances, as follows: "yes"
                                  uses pull operations, failing if not
                                  supported by the server; "no" uses
                                  traditional operations; "either" (default)
                                  uses pull operations if supported by the
                                  server, and otherwise traditional
                                  operations. Default: EnvVar
                                  PYWBEMCLI_USE_PULL, or "either".
  --pull-max-cnt INT              Maximum number of instances to be returned
                                  by the WBEM server in each open or pull
                                  response, if pull operations are used. This
                                  is a tuning parameter that does not affect
                                  the external behavior of the commands.
                                  Default: EnvVar PYWBEMCLI_PULL_MAX_CNT, or
                                  1000
  -T, --timestats                 Show time statistics of WBEM server
                                  operations.
  -d, --default-namespace NAMESPACE
                                  Default namespace, to be used when commands
                                  do not specify the --namespace command
                                  option. Default: EnvVar
                                  PYWBEMCLI_DEFAULT_NAMESPACE, or root/cimv2.
  -o, --output-format FORMAT      Output format for the command result. The
                                  specified format may be overriden since not
                                  all formats apply to all result data types.
                                  FORMAT is a table format
                                  [table|plain|simple|grid|psql|rst|html] or
                                  object format [mof|xml|repr|txt]. Default:
                                  simple.
  -l, --log COMP[=DEST[:DETAIL]],...
                                  Enable logging of the WBEM operations,
                                  defined by a list of log configuration
                                  strings with: COMP: [api|http|all]; DEST:
                                  [file|stderr], default: file; DETAIL:
                                  [all|paths|summary], default: all. Default:
                                  EnvVar PYWBEMCLI_LOG, or all.
  -v, --verbose                   Display extra information about the
                                  processing.
  --version                       Show the version of this command and the
                                  pywbem package and exit.
  -h, --help                      Show this message and exit.

Commands:
  class       Command group for CIM classes.
  connection  Command group for persistent WBEM connections.
  help        Show help message for interactive mode.
  instance    Command group for CIM instances.
  qualifier   Command group for CIM qualifier declarations.
  repl        Enter interactive mode (default).
  server      Command group for WBEM servers.
"""


OK = True
RUN = True
FAIL = False

TEST_CASES = [
    # desc - Description of test
    # inputs - String, or list of args or dict of 'env', 'args', 'globals',
    #          and 'stdin'. See See CLITestsBase.subcmd_test()  for
    #          detailed documentation. This test processor includes an
    #          additional key, `subcmd`
    # exp_response - Dictionary of expected responses (stdout, stderr, rc) and
    #                test definition (test: <testname>).
    #                See CLITestsBase.subcmd_test() for detailed documentation.
    # mock - None or name of files (mof or .py),
    # condition - If True, the test is executed,  Otherwise it is skipped.

    ['Verify -help.',
     {'global': ['--help'],
      'subcmd': 'class',
      'args': ['get', 'blah']},
     {'stdout': GLOBAL_HELP,
      'rc': 0,
      'test': 'linesnows'},
     None, OK],

    ['Verify invalid server definition.',
     {'global': ['-s', 'httpx://blah'],
      'subcmd': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['Error: Invalid scheme on server argument. httpx://blah Use '
                 '"http" or "https"'],
      'rc': 1,
      'test': 'in'},
     None, OK],

    ['Verify invalid server port definition fails.',
     {'global': ['-s', 'http://blah:abcd'],
      'subcmd': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['Error:', 'ConnectionError', 'Socket error'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify valid --use-pull option parameter yes.',
     {'global': ['-s', 'http://blah', '--use-pull', 'yes'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull: True'],
      'rc': 0,
      'test': 'in'},
     None, OK],

    ['Verify valid --use-pull option parameter no.',
     {'global': ['-s', 'http://blah', '--use-pull', 'no'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull: False'],
      'rc': 0,
      'test': 'in'},
     None, OK],

    ['Verify valid --use-pull option parameter.',
     {'global': ['-s', 'http://blah', '--use-pull', 'either'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull: None'],
      'rc': 0,
      'test': 'in'},
     None, OK],

    ['Verify invalid --use-pull option parameter fails.',
     {'global': ['-s', 'http://blah', '--use-pull', 'blah'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': ['Invalid value for "-U" / "--use-pull": invalid choice: '
                 'blah. (choose from yes, no, either)'],
      'rc': 2,
      'test': 'in'},
     None, OK],

    ['Verify valid --pull-max-cnt option parameter.',
     {'global': ['-s', 'http://blah', '--pull-max-cnt', '2000'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['pull-max-cnt: 2000'],
      'rc': 0,
      'test': 'in'},
     None, OK],

    ['Verify invalid --pull-max-cnt option parameter fails.',
     {'global': ['-s', 'http://blah', '--pull-max-cnt', 'blah'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': ['Error: Invalid value for "--pull-max-cnt": blah is not a '
                 'valid integer'],
      'rc': 2,
      'test': 'in'},
     None, OK],

    ['Verify --version global option.',
     {'global': ['-s', 'http://blah', '--version'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': [r'^pywbemcli, version [0-9]+\.[0-9]+\.[0-9]+',
                 r'^pywbem, version [0-9]+\.[0-9]+\.[0-9]+'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option one file',
     {'global': ['-m', SIMPLE_MOCK_FILE_PATH],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['name: default',
                 'server: None',
                 'mock-server:',
                 'simple_mock_model.mof',
                 'default-namespace: root/cimv2'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option, multiple files',
     {'global': ['-m', SIMPLE_MOCK_FILE_PATH,
                 '-m', PYTHON_MOCK_FILE_PATH],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['name', 'default',
                 'server', 'None',
                 'mock-server',
                 'simple_mock_model.mof',
                 'simple_python_mock_script.py',
                 'default-namespace: root/cimv2'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify --mock option, file does not exist',
     {'global': ['--mock-server', 'invalidfilename.mof'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': [r'Error: --mock-server: File:',
                 r'invalidfilename\.mof',
                 r'does not exist',
                 r'Aborted!'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option, file with bad extension',
     {'global': ['--mock-server', 'invalidfilename.mofx'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': [r'Error: --mock-server: File: ',
                 r'invalidfilename\.mofx',
                 r'extension.*not valid',
                 r'"py" or "mof" required',
                 r'Aborted!'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option, file with mof containing syntax error',
     {'global': ['-m', BAD_MOF_FILE_PATH],
      'subcmd': 'class',
      'args': ['enumerate']},
     {'stderr': ['badtypedef InstanceID;',
                 'Repository build exception MOFParseError',
                 'Aborted!'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option, file with python containing syntax error',
     {'global': ['-m', BAD_PY_FILE_PATH],
      'subcmd': 'class',
      'args': ['enumerate']},
     {'stderr': [r'Traceback \(most recent call last\)',
                 r'pywbemtools', r'_pywbemcli_operations\.py',
                 r'line ', 'in build_repository',
                 r"NameError: name 'globalsx' is not defined",
                 'Aborted'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify --name option with new name but not in repo fails',
     {'global': ['-n', 'fred'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': 'Error: Named connection "fred" does not exist',
      'rc': 1,
      'test': 'in'},
     None, OK],

    ['Verify --name option with new name but not in repo fails',
     {'global': ['--name', 'fred'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': 'Error: Named connection "fred" does not exist',
      'rc': 1,
      'test': 'in'},
     None, OK],

    ['Verify simultaneous --mock_server and --server options fail',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                 '--server', 'http://localhost'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': ['Conflicting server definitions. Do not use --server '
                 'and --mock-server simultaneously',
                 'Aborted!'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify --mock_server invalid name',
     {'global': ['--mock-server', 'fred'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': ['--mock-server: File:',
                 'fred',
                 'extension: "" not valid.',
                 'Aborted!'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option one file and name fails',
     {'global': ['-m', SIMPLE_MOCK_FILE_PATH, '--name', 'MyConnName'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': ['The --name "MyConnName" option',
                 'server', 'option',
                 'are mutually exclusive'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify --timestats',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '--timestats'],
      'subcmd': 'class',
      'args': ['enumerate']},
     {'stdout': ['class CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 'EnumerateClasses'],
      'rc': 0,
      'test': 'innows'},
     None, OK],


    ['Verify --timestats -T',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '-T'],
      'subcmd': 'class',
      'args': ['enumerate']},
     {'stdout': ['class CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 'EnumerateClasses'],
      'rc': 0,
      'test': 'innows'},
     None, OK],


    ['Verify uses pull Operation  with option either',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                 '--timestats',
                 '--use-pull', 'either'],
      'subcmd': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': ['instance of CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 ' OpenEnumerateInstances'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify uses pull Operation with option yes',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                 '--timestats',
                 '--use-pull', 'yes'],
      'subcmd': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': ['instance of CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 ' OpenEnumerateInstances'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify uses pull Operation with option no',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                 '--timestats',
                 '--use-pull', 'no'],
      'subcmd': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': ['instance of CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 ' EnumerateInstances'],
      'rc': 0,
      'test': 'regex'},
     None, OK],


    ['Verify --mock-server and -server not allowed',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                 '--server', 'http://blah'],
      'subcmd': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stderr': ['Conflicting server definitions. '],
      'rc': 1,
      'test': 'regex'},
     None, OK],



    #
    #   The following is a new sequence but depends on the repo being empty
    #   It creates, shows and deletes a single server definition to demo
    #   effect of other parameters than the --name parameter
    #

    ['Verify Create a connection for test.',
     {'args': ['add',
               '--name', 'globaltest1',
               '--server', 'http://blah',
               '--timeout', '45',
               '--use-pull', 'no',
               '--default-namespace', 'root/blah',
               '--user', 'john',
               '--password', 'pw',
               '--no-verify',
               '--certfile', 'mycertfile.pem',
               '--keyfile', 'mykeyfile.pem'],
      'subcmd': 'connection', },
     {'stdout': "",
      'test': 'lines'},
     None, OK],

    ['Verify --name and other options generates warnings but works',
     {'global': ['--name', 'globaltest1', '--timeout', '90'],
      'subcmd': 'connection',
      'args': ['delete', 'globaltest1']},
     {'stdout': ['WARNING: "timeout 90" ignored when "-n/--name used',
                 'globaltest1'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify connection already deleted.',
     {'subcmd': 'connection',
      'args': ['delete', 'globaltest1']},
     {'stderr': "globaltest1 not a defined connection name",
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify connection without server definition and subcommand that '
     ' requires connection fails.',
     {'subcmd': 'class',
      'args': ['enumerate']},
     {'stderr': ['No server defined for command that requires server. ',
                 'Define a server with "--server", "--mock-server", or ',
                 '"--name" general options; or in interactive mode, use ',
                 '"connection select" or "connection add" to define a '
                 'connection'],
      'rc': 1,
      'test': 'innows'},
     None, OK],


    ['Verify --keyfile allowed only if --certfile exists.',
     {'subcmd': 'class',
      'args': ['enumerate'],
      'global': ['--keyfile', 'mykey.pem']},
     {'stderr': ['The --keyfile option',
                 'is allowed only if the --certfile option is also used'],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    #
    # Test environment variables
    #
    ['Verify setting one env vars for input.',
     {'env': {'PYWBEMCLI_SERVER': 'http://blah'},
      'subcmd': 'connection',
      'args': 'show'},
     {'stdout': ['name', 'default',
                 'server', 'http://blah',
                 'default-namespace', 'root/cimv2',
                 'user', 'None',
                 'password', 'None',
                 'timeout', '30',
                 'no-verify', 'False',
                 'certfile', 'None',
                 'keyfile', 'None',
                 'use-pull', 'either',
                 'pull-max-cnt', '1000',
                 'mock-server',
                 'log', 'None'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify setting all env vars for input.',
     {'env': {'PYWBEMCLI_SERVER': 'http://blah',
              'PYWBEMCLI_DEFAULT_NAMESPACE': 'fred/fred',
              'PYWBEMCLI_USER': 'RonaldMcDonald',
              'PYWBEMCLI_PASSWORD': 'abcxdfG',
              'PYWBEMCLI_TIMEOUT': '99',
              'PYWBEMCLI_NO_VERIFY': 'True',
              'PYWBEMCLI_CERTFILE': 'certfile.pem',
              'PYWBEMCLI_KEYFILE': 'keyfile.pem',
              'PYWBEMCLI_USE_PULL': 'no',
              'PYWBEMCLI_PULL_MAX_CNT': '10',
              'PYWBEMCLI_LOG': 'api=all', },
      'subcmd': 'connection',
      'args': 'show'},
     {'stdout': ['name', 'default',
                 'server', 'http://blah',
                 'default-namespace', 'fred/fred',
                 'user', 'RonaldMcDonald',
                 'password', 'abcxdfG',
                 'timeout', '99',
                 'no-verify', 'True',
                 'certfile', 'certfile.pem',
                 'keyfile', 'keyfile.pem',
                 'use-pull', 'no',
                 'pull-max-cnt', '10',
                 'log', 'api=all'],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['erify mixed env var and input options.',
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
      'subcmd': 'connection',
      'global': ['--server', 'http://blah'],
      'args': 'show'},
     {'stdout': ['server', 'http://blah',
                 'default-namespace', 'fred/fred',
                 'user', 'RonaldMcDonald',
                 'password', 'abcxdfG',
                 'timeout', '99',
                 'no-verify', 'True',
                 'certfile', 'certfile.pem',
                 'keyfile', 'keyfile.pem',
                 'use-pull', 'False',
                 'pull-max-cnt', '10',
                 'log', 'api=all'],
      'rc': 0,
      'test': 'innows'},
     None, OK],
]

# TODO add test for pull operations with pull ops max size variations


class TestGlobalOptions(CLITestsBase):
    """
    Test the global options including statistics,  --server,
    --timeout, --use-pull, --pull-max-cnt, --output-format
    """
    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition", TEST_CASES)
    def test_execute_pywbemcli(self, desc, inputs, exp_response, mock,
                               condition):
        """
        Execute pybemcli with the defined input and test output.
        """
        subcmd = inputs['subcmd'] if inputs['subcmd'] else ''

        self.subcmd_test(desc, subcmd, inputs, exp_response,
                         mock, condition, verbose=False)
