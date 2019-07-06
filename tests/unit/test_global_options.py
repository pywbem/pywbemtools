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
Test global options.
NOTE: The --log opetions are tested in a separate file.
"""
from __future__ import absolute_import, print_function

import os
import pytest

from .cli_test_extensions import CLITestsBase

TEST_DIR = os.path.dirname(__file__)

SIMPLE_MOCK_FILE_PATH = os.path.join(TEST_DIR, 'simple_mock_model.mof')
PYTHON_MOCK_FILE_PATH = os.path.join(TEST_DIR, 'simple_python_mock_script.py')

GLOBAL_HELP = """
Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...

  WBEM Server command line browser. This cli tool implements the CIM/XML
  client APIs as defined in pywbem to make requests to a WBEM server. This
  browser uses subcommands to:

      * Explore the characteristics of WBEM Servers based on using the
        pywbem client APIs.  It can manage/inspect CIM_Classes and
        CIM_instances on the server.

      * In addition it can inspect namespaces, profiles, subscriptions,
        and other server information and inspect and manage WBEM
        indication subscriptions.

  The global options shown above that can also be specified on any of the
  (sub-)commands as well as the command line.

Options:
  -s, --server URI                Hostname or IP address with scheme of the
                                  WBEMServer in format:
                                  [{scheme}://]{host}[:{port}]
                                  The server
                                  parameter is conditionally optional (see
                                  --name)
                                  * Scheme: must be "https" or "http"
                                  [Default: "https"]
                                  * Host: defines
                                  short/fully qualified DNS hostname, literal
                                  IPV4 address (dotted), or literal IPV6
                                  address
                                  * Port: (optional) defines WBEM
                                  server port to be used [Defaults: 5988(HTTP)
                                  and 5989(HTTPS)].
                                  (EnvVar:
                                  PYWBEMCLI_SERVER).
  -N, --name NAME                 Name for the connection(optional, see
                                  --server).  If this option exists and the
                                  server option does not exist pywbemcli
                                  attempts to retrieve the connection
                                  information from the connections file. If
                                  the server option exists that is used as the
                                  connection definition with the name
                                  "default". This option and --server are
                                  mutually exclusive.(EnvVar: PYWBEMCLI_NAME).
  -d, --default_namespace NAMESPACE
                                  Default Namespace to use in the target
                                  WBEMServer if no namespace is defined in the
                                  subcommand(EnvVar: PYWBEMCLI_NAME)
                                  []Default: root/cimv2].
  -u, --user USER                 User name for the WBEM Server connection.
                                  (EnvVar: PYWBEMCLI_NAME)
  -p, --password PASSWORD         Password for the WBEM Server. Will be
                                  requested as part  of initialization if user
                                  name exists and it is not  provided by this
                                  option.(EnvVar: PYWBEMCLI_PASSWORD).
  -t, --timeout INTEGER           Operation timeout for the WBEM Server in
                                  seconds.
                                  (EnvVar:
                                  PYWBEMCLI_PYWBEMCLI_TIMEOUT)
  -n, --noverify                  If set, client does not verify server
                                  certificate.(EnvVar: PYWBEMCLI_NOVERIFY).
  -c, --certfile TEXT             Server certfile. Ignored if noverify flag
                                  set. (EnvVar: PYWBEMCLI_CERTFILE).
  -k, --keyfile FILE PATH         Client private key file. (EnvVar:
                                  PYWBEMCLI_KEYFILE).
  --ca_certs TEXT                 File or directory containing certificates
                                  that will be matched against certificate
                                  received from WBEM server. Set --no-verify-
                                  cert option to bypass client verification of
                                  the WBEM server certificate.  (EnvVar:
                                  PYWBEMCLI_CA_CERTS).
                                  [Default: Searches for
                                  matching certificates in the following
                                  system directories: /etc/pki/ca-
                                  trust/extracted/openssl/ca-bundle.trust.crt]
                                  /etc/ssl/certs]
                                  /etc/ssl/certificates]
  -o, --output-format <choice>    Output format. Multiple table and CIMObjects
                                  formats. pywbemcli may override the format
                                  choice depending on the operation since not
                                  all formats apply to all output data types.
                                  Choices further defined in documentation.
                                  Choices: Table:
                                  [table|plain|simple|grid|psql|rst|html],
                                  Object: [mof|xml|txt|tree]
                                  [Default:
                                  "simple"]
  --use-pull-ops [yes|no|either]  Determines whether the pull operations are
                                  used for EnumerateInstances,
                                  associatorinstances, referenceinstances, and
                                  ExecQuery operations.
                                  * "yes": pull
                                  operations used; if server does not support
                                  pull, the operation will fail.
                                  * "no":
                                  forces pywbemcli to try only the traditional
                                  non-pull operations.
                                  * "either": pywbemcli
                                  trys first pull and then  traditional
                                  operations.
                                  (EnvVar: PYWBEMCLI_USE_PULL)
                                  [Default: either]
  --pull-max-cnt INTEGER          MaxObjectCount of objects to be returned for
                                  each request if pull operations are used.
                                  Must be  a positive non-zero
                                  integer.(EnvVar: PYWBEMCLI_PULL_MAX_CNT)
                                  [Default: 1000]
  -T, --timestats                 Show time statistics of WBEM server
                                  operations after each command execution.
  -l, --log COMP=DEST:DETAIL,...  Enable logging of CIM Operations and set a
                                  component to a log level, destination, and
                                  detail level.
                                  * COMP: [api|http|all],
                                  Default: all
                                  * DEST: [file|stderr], Default:
                                  file
                                  * DETAIL:[all|paths|summary], Default:
                                  all
  -v, --verbose                   Display extra information about the
                                  processing.
  -m, --mock-server FILENAME      Defines, a mock WBEM server is as the target
                                  WBEM server. The option value defines a MOF
                                  or Python file path used to populate the
                                  mock repository. This option may be used
                                  multiple times where each use defines a
                                  single file_path.See the pywbemtools
                                  documentation for more information.(EnvVar:
                                  PYWBEMCLI_MOCK_SERVER).
  --version                       Show the version of this command and the
                                  package and exit
  -h, --help                      Show this message and exit.

Commands:
  class       Command group to manage CIM classes.
  connection  Command group to manage WBEM connections.
  help        Show help message for interactive mode.
  instance    Command group to manage CIM instances.
  qualifier   Command group to view QualifierDeclarations.
  repl        Enter interactive (REPL) mode (default).
  server      Command Group for WBEM server operations.
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

    ['Verify invalid server port definition.',
     {'global': ['-s', 'http://blah:abcd'],
      'subcmd': 'class',
      'args': ['get', 'blah']},
     {'stderr': ['Error:', 'ConnectionError', 'Socket error'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify valid pull_ops parameter.',
     {'global': ['-s', 'http://blah', '--use-pull-ops', 'yes'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull-ops: True'],
      'rc': 0,
      'test': 'in'},
     None, OK],

    ['Verify valid pull_ops parameter.',
     {'global': ['-s', 'http://blah', '--use-pull-ops', 'no'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull-ops: False'],
      'rc': 0,
      'test': 'in'},
     None, OK],

    ['Verify valid pull_ops parameter.',
     {'global': ['-s', 'http://blah', '--use-pull-ops', 'either'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['use-pull-ops: None'],
      'rc': 0,
      'test': 'in'},
     None, OK],

    ['Verify invalid pull-ops parameter.',
     {'global': ['-s', 'http://blah', '--use-pull-ops', 'blah'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': ['Error: Invalid value for "--use-pull-ops": invalid choice: '
                 'blah. (choose from yes, no, either)'],
      'rc': 2,
      'test': 'in'},
     None, OK],

    ['Verify valid pull-max-cnt parameter.',
     {'global': ['-s', 'http://blah', '--pull-max-cnt', '2000'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['pull-max-cnt: 2000'],
      'rc': 0,
      'test': 'in'},
     None, OK],

    ['Verify invalid pull-max-cnt parameter.',
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
     {'stdout': [r'^pywbemcli, version [0-9]+\.[0-9]+\.[0-9]+'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option one file',
     {'global': ['-m', SIMPLE_MOCK_FILE_PATH],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['Name: default',
                 'WBEMServer uri: None',
                 'mock:',
                 'simple_mock_model.mof',
                 'Default_namespace: root/cimv2'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option, multiple files',
     {'global': ['-m', SIMPLE_MOCK_FILE_PATH,
                 '-m', PYTHON_MOCK_FILE_PATH],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['Name: default',
                 'WBEMServer uri: None',
                 'mock: ',
                 r'simple_mock_model\.mof',
                 r'simple_python_mock_script\.py',
                 'Default_namespace: root/cimv2'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option, file does not exist',
     {'global': ['-m', 'invalidfilename.mof'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': ['Error: --mock-server: File: ',
                 'pywbemtools', 'invalidfilename.mof ',
                 'does not exist',
                 'Aborted!'],
      'rc': 1,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option, file with bad extension',
     {'global': ['-m', 'invalidfilename.mofx'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': ['Error: --mock-server: File: ',
                 'pywbemtools', 'invalidfilename.mofx ',
                 'extension ".mofx" not valid. "py" or "mof" required',
                 'Aborted!'],
      'rc': 1,
      'test': 'regex'},
     None, OK],


    ['Verify --name options with new name but not in repo failse',
     {'global': ['-N', 'fred'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': 'Error: Named connection "fred" does not exist',
      'rc': 1,
      'test': 'in'},
     None, OK],



    ['Verify --name options with new name but not in repo failse',
     {'global': ['--name', 'fred'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stderr': 'Error: Named connection "fred" does not exist',
      'rc': 1,
      'test': 'in'},
     None, OK],

    ['Verify --mock option one file and name OK',
     {'global': ['-m', SIMPLE_MOCK_FILE_PATH, '--name', 'MyConnName'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['Name: MyConnName',
                 'WBEMServer uri: None',
                 'mock: ',
                 'pywbemtools', 'tests', 'simple_mock_model.mof',
                 'Default_namespace: root/cimv2'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --mock option one file and name OK',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '--name',
                 'MyConnName'],
      'subcmd': 'connection',
      'args': ['show']},
     {'stdout': ['Name: MyConnName',
                 'WBEMServer uri: None',
                 'mock: ',
                 'pywbemtools', 'tests', 'simple_mock_model.mof',
                 'Default_namespace: root/cimv2'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify --timestats',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '--name',
                 'MyConnName', '--timestats'],
      'subcmd': 'class',
      'args': ['enumerate']},
     {'stdout': ['class CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 'EnumerateClasses'],
      'rc': 0,
      'test': 'regex'},
     None, OK],


    ['Verify --timestats -T',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '--name',
                 'MyConnName', '-T'],
      'subcmd': 'class',
      'args': ['enumerate']},
     {'stdout': ['class CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 'EnumerateClasses'],
      'rc': 0,
      'test': 'regex'},
     None, OK],


    ['Verify uses pull Operation when us. Uses timestats for output test',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH, '--timestats'],
      'subcmd': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': ['instance of CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 'EnumerateInstances'],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify uses pull Operation  with option either',
     {'global': ['--mock-server', SIMPLE_MOCK_FILE_PATH,
                 '--timestats',
                 '--use-pull-ops', 'either'],
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
                 '--use-pull-ops', 'yes'],
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
                 '--use-pull-ops', 'no'],
      'subcmd': 'instance',
      'args': ['enumerate', 'CIM_Foo']},
     {'stdout': ['instance of CIM_Foo {',
                 '  Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 ' EnumerateInstances'],
      'rc': 0,
      'test': 'regex'},
     None, OK],
]

# TODO add test for pull operations with pull ops max size variations


class TestGlobalOptions(CLITestsBase):
    """
    Test the global options including statistics,  --server,
    --timeout, --use-pull_ops, --pull-max-cnt, --output-format
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
