# Copyright 2017 IBM Corp. All Rights Reserved.
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
Tests the commands in thequalifier command group
"""
import os
import pytest
from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE, \
    CMD_OPTION_NAMESPACE_HELP_LINE, CMD_OPTION_SUMMARY_HELP_LINE

TEST_DIR = os.path.dirname(__file__)

# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'

QD_HELP_LINES = [
    'Usage: pywbemcli qualifier [COMMAND-OPTIONS] COMMAND [ARGS]...'
    'Command group for CIM qualifier declarations.',
    CMD_OPTION_HELP_HELP_LINE,
    'enumerate  List the qualifier declarations in a namespace.',
    'get        Get a qualifier declaration.',
]

QD_ENUMERATE_HELP_LINES = [
    'Usage: pywbemcli qualifier enumerate [COMMAND-OPTIONS]',
    'List the qualifier declarations in a namespace.',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

QD_GET_HELP_LINES = [
    'Usage: pywbemcli qualifier get [COMMAND-OPTIONS] QUALIFIERNAME',
    "Get a qualifier declaration.",
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

QD_ENUM_MOCK = """Qualifier Abstract : boolean = false,
    Scope(class, association, indication),
    Flavor(EnableOverride, Restricted);

Qualifier Aggregate : boolean = false,
    Scope(reference),
    Flavor(DisableOverride, ToSubclass);

Qualifier Association : boolean = false,
    Scope(association),
    Flavor(DisableOverride, ToSubclass);

Qualifier Description : string,
    Scope(any),
    Flavor(EnableOverride, ToSubclass, Translatable);

Qualifier In : boolean = true,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

Qualifier Indication : boolean = false,
    Scope(class, indication),
    Flavor(DisableOverride, ToSubclass);

Qualifier Key : boolean = false,
    Scope(property, reference),
    Flavor(DisableOverride, ToSubclass);

Qualifier Out : boolean = false,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

Qualifier Override : string,
    Scope(property, reference, method),
    Flavor(EnableOverride, Restricted);

"""

QD_GET_MOCK = """Qualifier Description : string,
    Scope(any),
    Flavor(EnableOverride, ToSubclass, Translatable);

"""

QD_TBL_OUT = """Qualifier Declarations
+-------------+---------+---------+---------+-------------+-----------------+
| Name        | Type    | Value   | Array   | Scopes      | Flavors         |
+=============+=========+=========+=========+=============+=================+
| Abstract    | boolean | False   | False   | CLASS       | EnableOverride  |
|             |         |         |         | ASSOCIATION | Restricted      |
|             |         |         |         | INDICATION  |                 |
+-------------+---------+---------+---------+-------------+-----------------+
| Aggregate   | boolean | False   | False   | REFERENCE   | DisableOverride |
|             |         |         |         |             | ToSubclass      |
+-------------+---------+---------+---------+-------------+-----------------+
| Association | boolean | False   | False   | ASSOCIATION | DisableOverride |
|             |         |         |         |             | ToSubclass      |
+-------------+---------+---------+---------+-------------+-----------------+
| Description | string  |         | False   | ANY         | EnableOverride  |
|             |         |         |         |             | ToSubclass      |
|             |         |         |         |             | Translatable    |
+-------------+---------+---------+---------+-------------+-----------------+
| In          | boolean | True    | False   | PARAMETER   | DisableOverride |
|             |         |         |         |             | ToSubclass      |
+-------------+---------+---------+---------+-------------+-----------------+
| Indication  | boolean | False   | False   | CLASS       | DisableOverride |
|             |         |         |         | INDICATION  | ToSubclass      |
+-------------+---------+---------+---------+-------------+-----------------+
| Key         | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |         |         |         | REFERENCE   | ToSubclass      |
+-------------+---------+---------+---------+-------------+-----------------+
| Out         | boolean | False   | False   | PARAMETER   | DisableOverride |
|             |         |         |         |             | ToSubclass      |
+-------------+---------+---------+---------+-------------+-----------------+
| Override    | string  |         | False   | PROPERTY    | EnableOverride  |
|             |         |         |         | REFERENCE   | Restricted      |
|             |         |         |         | METHOD      |                 |
+-------------+---------+---------+---------+-------------+-----------------+
"""

QD_TBL_GET_OUT = """Qualifier Declarations
+----------+---------+---------+---------+-------------+----------------+
| Name     | Type    | Value   | Array   | Scopes      | Flavors        |
+==========+=========+=========+=========+=============+================+
| Abstract | boolean | False   | False   | CLASS       | EnableOverride |
|          |         |         |         | ASSOCIATION | Restricted     |
|          |         |         |         | INDICATION  |                |
+----------+---------+---------+---------+-------------+----------------+
"""

# TODO: Add tests for xml, repr, txt formats.

# The following variables are used to control tests executed during
# development of tests
OK = True      # set to OK for tests passed. Set OK = False to execute one test
RUN = True     # set RUN condition in test being run
FAIL = False   # flag any tests that fail

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

    ['Verify qualifier command --help response',
     '--help',
     {'stdout': QD_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify qualifier command -h response',
     '-h',
     {'stdout': QD_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify qualifier command enumerate --help response',
     ['enumerate', '--help'],
     {'stdout': QD_ENUMERATE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify qualifier command enumerate -h response.',
     ['enumerate', '-h'],
     {'stdout': QD_ENUMERATE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify qualifier command get --help response.',
     ['get', '--help'],
     {'stdout': QD_GET_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify qualifier command get -h response.',
     ['get', '-h'],
     {'stdout': QD_GET_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify qualifier command enumerate returns qual decls.',
     ['enumerate'],
     {'stdout': QD_ENUM_MOCK,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command enumerate with namespace returns qual decls.',
     ['enumerate', '--namespace', 'root/cimv2'],
     {'stdout': QD_ENUM_MOCK,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command enumerate summary returns qual decls.',
     ['enumerate', '--summary'],
     {'stdout': ['9', 'CIMQualifierDeclaration'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify qualifier command enumerate summary returns qual decls table',
     {'args': ['enumerate', '--summary'],
      'general': ['--output-format', 'table']},
     {'stdout': ["""Summary of CIMQualifierDeclaration returned
+---------+-------------------------+
|   Count | CIM Type                |
|---------+-------------------------|
|       9 | CIMQualifierDeclaration |
+---------+-------------------------+
"""],
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command get  Description',
     ['get', 'Description'],
     {'stdout': QD_GET_MOCK,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command get invalid qual decl name .',
     ['get', 'NoSuchQualDecl'],
     {'stderr': ["Error: CIMError: 6"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command get  Description outputformat xml',
     {'args': ['get', 'Description'],
      'general': ['--output-format', 'xml']},
     {'stdout': ['<QUALIFIER.DECLARATION( | .+ )NAME="Description"',
                 '<SCOPE( | .+ )ASSOCIATION="true"'],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command -o grid enumerate produces table out',
     {'args': ['enumerate'],
      'general': ['-o', 'grid']},
     {'stdout': QD_TBL_OUT,
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify qualifier command -o grid get Abstract table out',
     {'args': ['get', 'abstract'],
      'general': ['-o', 'grid']},
     {'stdout': QD_TBL_GET_OUT,
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command enumerate invalid namespace Fails',
     ['enumerate', '--namespace', 'root/blah'],
     {'stderr': ["Error: CIMError: 3", "CIM_ERR_INVALID_NAMESPACE"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command --timestats gets stats output. Cannot test'
     'with lines because execution time is variable.',
     {'args': ['get', 'IN'],
      'general': ['--timestats']},
     {'stdout': ['Qualifier In : boolean = true,',
                 'Scope(parameter),',
                 'Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 '      1      0',
                 '0           0  GetQualifier'],
      'rc': 0,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command -o repr get Description produces repr out',
     {'args': ['get', 'Description'],
      'general': ['-o', 'repr']},
     {'stdout': "CIMQualifierDeclaration(name='Description', value=None, "
                "type='string', is_array=False, array_size=None, "
                "scopes=NocaseDict({'CLASS': False, 'ASSOCIATION': False, "
                "'INDICATION': False, 'PROPERTY': False, 'REFERENCE': False, "
                "'METHOD': False, 'PARAMETER': False, 'ANY': True}), "
                "tosubclass=True, overridable=True, translatable=True, "
                "toinstance=None)",
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],
]


class TestcmdQualifiers(CLITestsBase):
    """
    Test all of the qualifiers command variations.
    """
    command_group = 'qualifier'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition", TEST_CASES)
    def test_qualdecl(self, desc, inputs, exp_response, mock, condition):
        """
        Common test method for those commands and options in the
        qualifier command group that can be tested.  This includes:

          * Subcommands like help that do not require access to a server

          * Subcommands that can be tested with a single execution of a
            pywbemcli command.
        """
        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition)
