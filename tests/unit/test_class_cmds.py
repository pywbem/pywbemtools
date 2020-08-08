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
Tests the class command
"""

from __future__ import absolute_import, print_function

import os
import pytest

from .cli_test_extensions import CLITestsBase, PYWBEM_0, \
    FAKEURL_STR
from .common_options_help_lines import CMD_OPTION_NAMES_ONLY_HELP_LINE, \
    CMD_OPTION_HELP_HELP_LINE, CMD_OPTION_SUMMARY_HELP_LINE, \
    CMD_OPTION_NAMESPACE_HELP_LINE, CMD_OPTION_PROPERTYLIST_HELP_LINE, \
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE, \
    CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE, CMD_OPTION_NO_QUALIFIERS_HELP_LINE, \
    CMD_OPTION_MULTIPLE_NAMESPACE_HELP_LINE, \
    CMD_OPTION_ASSOCIATION_FILTER_HELP_LINE, \
    CMD_OPTION_INDICATION_FILTER_HELP_LINE, \
    CMD_OPTION_EXPERIMENTAL_FILTER_HELP_LINE

TEST_DIR = os.path.dirname(__file__)

# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'

INVOKE_METHOD_MOCK_FILE_0 = 'simple_mock_invokemethod_v0.py'
INVOKE_METHOD_MOCK_FILE_1 = 'simple_mock_invokemethod_v1.py'
INVOKE_METHOD_MOCK_FILE = INVOKE_METHOD_MOCK_FILE_0 if PYWBEM_0 else \
    INVOKE_METHOD_MOCK_FILE_1

SIMPLE_ASSOC_MOCK_FILE = 'simple_assoc_mock_model.mof'
QUALIFIER_FILTER_MODEL = 'qualifier_filter_model.mof'


#
# The following list defines the help for each command in terms of particular
# parts of lines that are to be tested.//FakedUrl:5988
# For each test, try to include:
# 1. The usage line and in particular the argument component
# 2. The single
# 2. The last line CMD_OPTION_HELP_HELP_LINE
#
CLASS_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class COMMAND [ARGS] [COMMAND-OPTIONS]',
    'Command group for CIM classes.',
    CMD_OPTION_HELP_HELP_LINE,
    'associators   List the classes associated with a class.',
    'delete        Delete a class.',
    'enumerate     List top classes or subclasses of a class in a namespace.',
    'find          List the classes with matching class names on the server.',
    'get           Get a class.',
    'invokemethod  Invoke a method on a class.',
    'references    List the classes referencing a class.',
    'tree          Show the subclass or superclass hierarchy for a class.',
]

CLASS_ASSOCIATORS_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class associators CLASSNAME '
    '[COMMAND-OPTIONS]',
    'List the classes associated with a class.',
    '--ac, --assoc-class CLASSNAME Filter the result set by association class',
    '--rc, --result-class CLASSNAME Filter the result set by result class',
    '-r, --role PROPERTYNAME Filter the result set by source end role',
    '--rr, --result-role PROPERTYNAME Filter the result set by far end role',
    CMD_OPTION_NO_QUALIFIERS_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_PROPERTYLIST_HELP_LINE,
    CMD_OPTION_NAMES_ONLY_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_DELETE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class delete CLASSNAME '
    '[COMMAND-OPTIONS]',
    'Delete a class.',
    '-f, --force Delete any instances of the class as well.',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_ENUMERATE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class enumerate CLASSNAME '
    '[COMMAND-OPTIONS]',
    'List top classes or subclasses of a class in a namespace.',
    '--di, --deep-inheritance Include the complete subclass hierarchy',
    CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE,
    CMD_OPTION_NO_QUALIFIERS_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_NAMES_ONLY_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_ASSOCIATION_FILTER_HELP_LINE,
    CMD_OPTION_INDICATION_FILTER_HELP_LINE,
    CMD_OPTION_EXPERIMENTAL_FILTER_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_FIND_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class find CLASSNAME-GLOB '
    '[COMMAND-OPTIONS]',
    'List the classes with matching class names on the server.',
    '-s, --sort                 Sort by namespace. Default is to sort by',
    CMD_OPTION_MULTIPLE_NAMESPACE_HELP_LINE,
    CMD_OPTION_ASSOCIATION_FILTER_HELP_LINE,
    CMD_OPTION_INDICATION_FILTER_HELP_LINE,
    CMD_OPTION_EXPERIMENTAL_FILTER_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_GET_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class get CLASSNAME [COMMAND-OPTIONS]',
    'Get a class.',
    CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE,
    CMD_OPTION_NO_QUALIFIERS_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_PROPERTYLIST_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_INVOKEMETHOD_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class invokemethod CLASSNAME '
    'METHODNAME [COMMAND-OPTIONS]',
    'Invoke a method on a class.',
    '-p, --parameter PARAMETERNAME=VALUE Specify a method input parameter',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_REFERENCES_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class references CLASSNAME '
    '[COMMAND-OPTIONS]',
    'List the classes referencing a class.',
    '--rc, --result-class CLASSNAME Filter the result set by result class',
    '-r, --role PROPERTYNAME Filter the result set by source end role',
    CMD_OPTION_NO_QUALIFIERS_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_PROPERTYLIST_HELP_LINE,
    CMD_OPTION_NAMES_ONLY_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_TREE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class tree CLASSNAME [COMMAND-OPTIONS]',
    'Show the subclass or superclass hierarchy for a class.',
    '-s, --superclasses Show the superclass hierarchy.',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

# pylint: disable=line-too-long
CIMFOO_SUB_SUB = """
   [Description ( "Subclass of CIM_Foo_sub" )]
class CIM_Foo_sub_sub : CIM_Foo_sub {

   string cimfoo_sub_sub;

   string cimfoo_sub;

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Sample method with input and output parameters" )]
   uint32 Method1(
         [IN ( false ),
          OUT ( true ),
          Description ( "Response param 2" )]
      string OutputParam2);

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_Foo REF TestRef,
         [IN ( false ),
          OUT ( true ),
          Description ( "Rtns method name if exists on input" )]
      string OutputParam,
         [IN ( true ),
          Description ( "Defines return value if provided." )]
      uint32 OutputRtnValue);

      [Description ( "Static method with in and out parameters" ),
       Static ( true )]
   uint32 FuzzyStatic(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_Foo REF TestRef,
         [IN ( false ),
          OUT ( true ),
          Description ( "Rtns method name if exists on input" )]
      string OutputParam,
         [IN ( true ),
          Description ( "Defines return value if provided." )]
      uint32 OutputRtnValue);

      [Description ( "Method with no Parameters" )]
   uint32 DeleteNothing();

};

"""  # noqa: E501
# pylint: enable=line-too-long

CIMFOO_SUB_SUB_NO_QUALS = """
class CIM_Foo_sub_sub : CIM_Foo_sub {

   string cimfoo_sub_sub;

   string cimfoo_sub;

   string InstanceID;

   uint32 IntegerProp;

   uint32 Method1(
      string OutputParam2);

   uint32 Fuzzy(
      string TestInOutParameter,
      CIM_Foo REF TestRef,
      string OutputParam,
      uint32 OutputRtnValue);

   uint32 FuzzyStatic(
      string TestInOutParameter,
      CIM_Foo REF TestRef,
      string OutputParam,
      uint32 OutputRtnValue);

   uint32 DeleteNothing();

};
"""
# TODO: This never referenced
REFERENCES_CLASS_RTN = [
    FAKEURL_STR + '/root/cimv2:TST_Lineage',
    'class TST_Lineage {',
    '',
    '   string InstanceID;',
    '',
    '   TST_Person REF parent;',
    '',
    '   TST_Person REF child;',
    '',
    '};',
    '',
    FAKEURL_STR + '/root/cimv2:TST_MemberOfFamilyCollection',
    'class TST_MemberOfFamilyCollection {',
    '',
    '   TST_Person REF family;',
    '',
    '   TST_Person REF member;',
    '',
    '};',
    '']

# TODO: This never referenced
REFERENCES_CLASS_RTN2 = [
    FAKEURL_STR + '/root/cimv2:TST_MemberOfFamilyCollection',
    'class TST_MemberOfFamilyCollection {',
    '',
    '   TST_Person REF family;',
    '',
    '   TST_Person REF member;',
    '',
    '};',
    '',
    '']

REFERENCES_CLASS_RTN_QUALS2 = [
    FAKEURL_STR + '/root/cimv2:TST_MemberOfFamilyCollection',
    '   [Association ( true ),',
    '    Description ( " Family gathers person to family." )]',
    'class TST_MemberOfFamilyCollection {',
    '      [key ( true )]',
    '   TST_Person REF family;',
    '      [key ( true )]',
    '   TST_Person REF member;',
    '};']


OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet


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

    ['Verify class command --help response',
     ['--help'],
     {'stdout': CLASS_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command --help command order',
     ['--help'],
     {'stdout': r'Commands:'
                '.*\n  enumerate'
                '.*\n  get'
                '.*\n  delete'
                '.*\n  invokemethod'
                '.*\n  references'
                '.*\n  associators'
                '.*\n  find'
                '.*\n  tree',
      'test': 'regex'},
     None, OK],

    ['Verify class command -h response',
     ['-h'],
     {'stdout': CLASS_HELP_LINES,
      'test': 'innows'},
     None, OK],

    #
    # Enumerate command and its options
    #
    ['Verify class command enumerate --help response',
     ['enumerate', '--help'],
     {'stdout': CLASS_ENUMERATE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command enumerate -h response',
     ['enumerate', '-h'],
     {'stdout': CLASS_ENUMERATE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command enumerate CIM_Foo',
     ['enumerate', 'CIM_Foo'],
     {'stdout': ['[Description ( "Subclass of CIM_Foo" )]'],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --lo',
     ['enumerate', 'CIM_Foo', '--lo'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --lo',
     ['enumerate', 'CIM_Foo', '--local-only'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo_sub',
     ['enumerate', 'CIM_Foo_sub'],
     {'stdout': CIMFOO_SUB_SUB,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo local-only',
     ['enumerate', 'CIM_Foo', '--local-only'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo -no-qualifiers',
     ['enumerate', 'CIM_Foo_sub', '--no-qualifiers'],
     {'stdout': CIMFOO_SUB_SUB_NO_QUALS,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --di',
     ['enumerate', 'CIM_Foo', '--di'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --deep-inheritance',
     ['enumerate', 'CIM_Foo', '--deep-inheritance'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --ico',
     ['enumerate', 'CIM_Foo', '--ico'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --include-classorigin',
     ['enumerate', 'CIM_Foo', '--include-classorigin'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --no names only',
     ['enumerate', 'CIM_Foo', '--no'],
     {'stdout': ['CIM_Foo', 'CIM_Foo_sub', 'CIM_Foo_sub2'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --names only',
     ['enumerate', 'CIM_Foo', '--names-only'],
     {'stdout': ['CIM_Foo', 'CIM_Foo_sub', 'CIM_Foo_sub2'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate --no names only - table',
     {'args': ['enumerate', '--no'],
      'general': ['--output-format', 'table']},
     {'stdout': """Classnames:
+--------------+
| Class Name   |
|--------------|
| CIM_Foo      |
+--------------+
""",
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --no names only - table',
     {'args': ['enumerate', 'CIM_Foo', '--no'],
      'general': ['--output-format', 'table']},
     {'stdout': """Classnames:
+--------------+
| Class Name   |
|--------------|
| CIM_Foo_sub  |
| CIM_Foo_sub2 |
+--------------+
""",
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo --names-only',
     ['enumerate', 'CIM_Foo', '--names-only'],
     {'stdout': ['CIM_Foo', 'CIM_Foo_sub', 'CIM_Foo_sub2'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo summary table',
     ['enumerate', 'CIM_Foo', '-s'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo summary, table',
     ['enumerate', 'CIM_Foo', '--summary'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo summary table output',
     {'args': ['enumerate', 'CIM_Foo', '--summary'],
      'general': ['--output-format', 'table']},
     {'stdout': ["""Summary of CIMClass returned
+---------+------------+
|   Count | CIM Type   |
|---------+------------|
|       2 | CIMClass   |
+---------+------------+
"""],
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo names and --di --no',
     ['enumerate', 'CIM_Foo', '--di', '--no'],
     {'stdout': ['CIM_Foo_sub', 'CIM_Foo_sub2', 'CIM_Foo_sub_sub'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo names and --deep-inheritance '
     '--names-only',
     ['enumerate', 'CIM_Foo', '--names-only', '--deep-inheritance'],
     {'stdout': ['CIM_Foo_sub', 'CIM_Foo_sub2', 'CIM_Foo_sub_sub'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo include qualifiers',
     ['enumerate', 'CIM_Foo'],
     {'stdout': ['Key ( true )', '[Description (', 'class CIM_Foo'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command get with xml output format).',
     {'args': ['enumerate'],
      'general': ['--output-format', 'repr']},
     {'stdout': [r"CIMClass\(classname='CIM_Foo', superclass=None,",
                 r"'InstanceID': CIMProperty\(name='InstanceID', value=None,"],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command get with repr output format).',
     {'args': ['enumerate'],
      'general': ['--output-format', 'txt']},
     {'stdout': ["CIMClass(classname='CIM_Foo', ...)"],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate with repr output format).',
     {'args': ['enumerate'],
      'general': ['--output-format', 'xml']},
     {'stdout': ['<CLASS( | .+ )NAME="CIM_Foo">',
                 '<PROPERTY( | .+ )NAME="InstanceID"',
                 '<PROPERTY( | .+ )NAME="IntegerProp"',
                 '<METHOD( | .+ )NAME="DeleteNothing"'],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate with --association filter.',
     ['enumerate', '--association', '--names-only'],
     {'stdout': ['TST_Lineage', 'TST_MemberOfFamilyCollection'],
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command enumerate with --association filter and no '
     'qualifiers.',
     ['enumerate', '--association', '--nq'],
     {'stdout': ['class TST_Lineage {',
                 'string InstanceID;',
                 'TST_Person REF parent;',
                 'TST_Person REF child;',
                 'class TST_MemberOfFamilyCollection {',
                 'TST_Person REF family;',
                 'TST_Person REF member;', '};'],
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command enumerate with --no-association filter and '
     'no-qualifiers. Tests no qualifiers on parameters',
     ['enumerate', '--no-association', '--no-qualifiers'],
     {'stdout': ['class CIM_Foo {',
                 'string InstanceID;',
                 'uint32 IntegerProp;',
                 'uint32 Fuzzy(',
                 'string TestInOutParameter,',
                 'CIM_Foo REF TestRef,',
                 'string OutputParam,',
                 'uint32 OutputRtnValue);',
                 'uint32 FuzzyStatic(',
                 'string TestInOutParameter,',
                 'CIM_Foo REF TestRef,',
                 'string OutputParam,',
                 'uint32 OutputRtnValue);',
                 'uint32 DeleteNothing();', '};'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate with --association filter.',
     ['enumerate', '--no-association', '--names-only'],
     {'stdout': ['TST_FamilyCollection', 'TST_Person'],
      'test': 'in'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command enumerate with --indication filter.',
     ['enumerate', '--indication', '--names-only'],
     {'stdout': ['TST_Indication', 'TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-indication filter.',
     ['enumerate', '--no-indication', '--names-only'],
     {'stdout': ['TST_FamilyCollection',
                 'TST_Lineage',
                 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionSub',
                 'TST_Person'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimentat filter.',
     ['enumerate', '--experimental', '--names-only'],
     {'stdout': ['TST_Indication', 'TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-experimental filter.',
     ['enumerate', '--no-experimental', '--names-only'],
     {'stdout': ['TST_FamilyCollection',
                 'TST_Indication',
                 'TST_Lineage',
                 'TST_MemberOfFamilyCollection',
                 'TST_Person'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimental and --association.',
     ['enumerate', '--experimental', '--association', '--names-only'],
     {'stdout': ['TST_MemberOfFamilyCollectionSub'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimental and '
     '--not-association.',
     ['enumerate', '--experimental', '--no-association', '--names-only'],
     {'stdout': ['TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --indication and --experimental.',
     ['enumerate', '--experimental', '--indication', '--names-only'],
     {'stdout': ['TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --indication and --no-experimental.',
     ['enumerate', '--no-experimental', '--indication', '--names-only'],
     {'stdout': ['TST_Indication'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --noindication, --no-experimental.'
     '--no-association',
     ['enumerate', '--no-experimental', '--no-indication', '--no-association',
      '--names-only'],
     {'stdout': ['TST_FamilyCollection',
                 'TST_Person'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify instance command enumerate CIM_Foo_sub2, w --verbose rtns msg.',
     {'args': ['enumerate', 'CIM_Foo_sub2'],
      'general': ['--verbose']},
     {'stdout': 'No objects returned',
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    #
    # Enumerate errors
    #

    ['Verify class command enumerate nonexistent class name',
     ['enumerate', 'CIM_FClassDoesNotExist'],
     {'stderr': ['CIMError', 'CIM_ERR_INVALID_CLASS'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate table output fails).',
     {'args': ['enumerate'],
      'general': ['--output-format', 'table']},
     {'stderr': ['Output format "table"', 'not allowed', 'Only CIM formats:'],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    #
    # Test class get
    #
    ['Verify class command get --help response',
     ['get', '--help'],
     {'stdout': CLASS_GET_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command get -h response',
     ['get', '-h'],
     {'stdout': CLASS_GET_HELP_LINES,
      'test': 'innows'},
     None, OK],

    # command get local-only option
    ['Verify class command get not local-only. Tests for property names',
     ['get', 'CIM_Foo_sub2'],
     {'stdout': ['string cimfoo_sub2;', 'InstanceID', 'IntegerProp', 'Fuzzy',
                 'Key ( true )', 'IN ( false )'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command get local-only(--lo)).',
     ['get', 'CIM_Foo_sub2', '--lo'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '};', ''],
      'test': 'patterns'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command get local-only. Tests whole response',
     ['get', 'CIM_Foo_sub2', '--local-only'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '};', ''],
      'test': 'patterns'},
     SIMPLE_MOCK_FILE, OK],

    # includequalifiers. Test the flag that excludes qualifiers
    ['Verify class command get without qualifiers. Tests whole response',
     ['get', 'CIM_Foo_sub2', '--nq'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '   string InstanceID;',
                 '',
                 '   uint32 IntegerProp;',
                 '',
                 '   uint32 Fuzzy(',
                 '      string TestInOutParameter,',
                 '      CIM_Foo REF TestRef,',
                 '      string OutputParam,',
                 '      uint32 OutputRtnValue);',
                 '',
                 '   uint32 FuzzyStatic(',
                 '      string TestInOutParameter,',
                 '      CIM_Foo REF TestRef,',
                 '      string OutputParam,',
                 '      uint32 OutputRtnValue);',
                 '',
                 '   uint32 DeleteNothing();',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command get without qualifiers. Tests whole response',
     ['get', 'CIM_Foo_sub2', '--no-qualifiers'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '   string InstanceID;',
                 '',
                 '   uint32 IntegerProp;',
                 '',
                 '   uint32 Fuzzy(',
                 '      string TestInOutParameter,',
                 '      CIM_Foo REF TestRef,',
                 '      string OutputParam,',
                 '      uint32 OutputRtnValue);',
                 '',
                 '   uint32 FuzzyStatic(',
                 '      string TestInOutParameter,',
                 '      CIM_Foo REF TestRef,',
                 '      string OutputParam,',
                 '      uint32 OutputRtnValue);',
                 '',
                 '   uint32 DeleteNothing();',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    # pylint: disable=line-too-long
    ['Verify class command get with propertylist. Tests whole response',
     ['get', 'CIM_Foo_sub2', '--pl', 'InstanceID'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '      [Key ( true ),',
                 '       Description ( "This is key property." )]',
                 '   string InstanceID;',
                 '',
                 '      [Description ( "Method with in and out parameters" )]',
                 '   uint32 Fuzzy(',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Define data to be returned in output parameter" )]',  # noqa: E501
                 '      string TestInOutParameter,',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Test of ref in/out parameter" )]',
                 '      CIM_Foo REF TestRef,',
                 '         [IN ( false ),',
                 '          OUT ( true ),',
                 '          Description ( "Rtns method name if exists on input" )]',  # noqa: E501
                 '      string OutputParam,',
                 '         [IN ( true ),',
                 '          Description ( "Defines return value if provided." )]',  # noqa: E501
                 '      uint32 OutputRtnValue);',
                 '',
                 '      [Description ( "Static method with in and out parameters" ),',  # noqa: E501
                 '       Static ( true )]',
                 '   uint32 FuzzyStatic(',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Define data to be returned in output parameter" )]',  # noqa: E501
                 '      string TestInOutParameter,',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Test of ref in/out parameter" )]',
                 '      CIM_Foo REF TestRef,',
                 '         [IN ( false ),',
                 '          OUT ( true ),',
                 '          Description ( "Rtns method name if exists on input" )]',  # noqa: E501
                 '      string OutputParam,',
                 '         [IN ( true ),',
                 '          Description ( "Defines return value if provided." )]',  # noqa: E501
                 '      uint32 OutputRtnValue);',
                 '',
                 '      [Description ( "Method with no Parameters" )]',
                 '   uint32 DeleteNothing();',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command get with empty propertylist. Tests whole '
     'response',
     ['get', 'CIM_Foo_sub2', '--pl', '""'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '      [Description ( "Method with in and out parameters" )]',
                 '   uint32 Fuzzy(',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Define data to be returned in output parameter" )]',  # noqa: E501
                 '      string TestInOutParameter,',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Test of ref in/out parameter" )]',
                 '      CIM_Foo REF TestRef,',
                 '         [IN ( false ),',
                 '          OUT ( true ),',
                 '          Description ( "Rtns method name if exists on input" )]',  # noqa: E501
                 '      string OutputParam,',
                 '         [IN ( true ),',
                 '          Description ( "Defines return value if provided." )]',  # noqa: E501
                 '      uint32 OutputRtnValue);',
                 '',
                 '      [Description ( "Static method with in and out parameters" ),',  # noqa: E501
                 '       Static ( true )]',
                 '   uint32 FuzzyStatic(',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Define data to be returned in output parameter" )]',  # noqa: E501
                 '      string TestInOutParameter,',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Test of ref in/out parameter" )]',
                 '      CIM_Foo REF TestRef,',
                 '         [IN ( false ),',
                 '          OUT ( true ),',
                 '          Description ( "Rtns method name if exists on input" )]',  # noqa: E501
                 '      string OutputParam,',
                 '         [IN ( true ),',
                 '          Description ( "Defines return value if provided." )]',  # noqa: E501
                 '      uint32 OutputRtnValue);',
                 '',
                 '      [Description ( "Method with no Parameters" )]',
                 '   uint32 DeleteNothing();',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],
    # pylint: enable=line-too-long

    ['Verify class command get with xml output format).',
     {'args': ['get', 'CIM_Foo'],
      'general': ['--output-format', 'repr']},
     {'stdout': [r"CIMClass\(classname='CIM_Foo', superclass=None,",
                 r"'InstanceID': CIMProperty\(name='InstanceID', value=None,"],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command get with repr output format).',
     {'args': ['get', 'CIM_Foo'],
      'general': ['--output-format', 'txt']},
     {'stdout': ["CIMClass(classname='CIM_Foo', ...)"],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command get with repr output format).',
     {'args': ['get', 'CIM_Foo'],
      'general': ['--output-format', 'xml']},
     {'stdout': ['<CLASS( | .+ )NAME="CIM_Foo">',
                 '<PROPERTY( | .+ )NAME="InstanceID"',
                 '<PROPERTY( | .+ )NAME="IntegerProp"',
                 '<METHOD( | .+ )NAME="DeleteNothing"'],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command get with propertylist and classorigin,',
     ['get', 'CIM_Foo_sub2', '--pl', 'InstanceID', '--ico'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '     [Key ( true ),',
                 '      Description ( "This is key property." )]',
                 '   string InstanceID;',
                 '      [Description ( "Method with in and out parameters" )]',
                 '   uint32 Fuzzy(',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Define data to be returned in '
                 'output parameter" )]',
                 '      string TestInOutParameter,',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Test of ref in/out parameter" )]',
                 '      CIM_Foo REF TestRef,',
                 '         [IN ( false ),',
                 '          OUT ( true ),',
                 '          Description ( "Rtns method name if exists on '
                 'input" )]',
                 '      string OutputParam,',
                 '         [IN ( true ),',
                 '          Description ( "Defines return value if '
                 'provided." )]',
                 '      uint32 OutputRtnValue);',
                 '      [Description ( "Static method with in and out '
                 'parameters" ),',
                 '       Static ( true )]',
                 '   uint32 FuzzyStatic(',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Define data to be returned in '
                 'output parameter" )]',
                 '      string TestInOutParameter,',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Test of ref in/out parameter" )]',
                 '      CIM_Foo REF TestRef,',
                 '         [IN ( false ),',
                 '          OUT ( true ),',
                 '          Description ( "Rtns method name if exists on '
                 'input" )]',
                 '      string OutputParam,',
                 '         [IN ( true ),',
                 '          Description ( "Defines return value if '
                 'provided." )]',
                 '      uint32 OutputRtnValue);',
                 '      [Description ( "Method with no Parameters" )]',
                 '   uint32 DeleteNothing();',
                 '};', ''],
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    # get command errors

    ['Verify class command get invalid classname',
     ['get', 'CIM_Argh'],
     {'stderr': ['CIMError', 'CIM_ERR_NOT_FOUND', '6'],
      'rc': 1,
      'test': 'regex'},

     SIMPLE_MOCK_FILE, OK],
    ['Verify class command get invalid namespace',
     ['get', 'CIM_Foo', '--namespace', 'Argh'],
     {'stderr': ['CIMError', 'CIM_ERR_INVALID_NAMESPACE', '3'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate table output fails).',
     {'args': ['get', 'CIM_Foo'],
      'general': ['--output-format', 'table']},
     {'stderr': ['Output format "table" ', 'not allowed', 'Only CIM formats:'],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    #
    # find command
    #
    ['Verify class command find --help response',
     ['find', '--help'],
     {'stdout': CLASS_FIND_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command find -h response',
     ['find', '-h'],
     {'stdout': CLASS_FIND_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command find simple name in all namespaces',
     ['find', 'CIM_*'],
     {'stdout': ["  root/cimv2:CIM_Foo",
                 "  root/cimv2:CIM_Foo_sub",
                 "  root/cimv2:CIM_Foo_sub2",
                 "  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in all namespaces wo case',
     ['find', 'cim_*'],
     {'stdout': ["  root/cimv2:CIM_Foo",
                 "  root/cimv2:CIM_Foo_sub",
                 "  root/cimv2:CIM_Foo_sub2",
                 "  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in all namespaces lead wc',
     ['find', '*sub_sub*'],
     {'stdout': ["  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in all namespaces wo case',
     ['find', '*sub_su?*'],
     {'stdout': ["  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in known namespace',
     ['find', 'CIM_*', '-n', 'root/cimv2'],
     {'stdout': ["  root/cimv2:CIM_Foo",
                 "  root/cimv2:CIM_Foo_sub",
                 "  root/cimv2:CIM_Foo_sub2",
                 "  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find name in known namespace -o grid',
     {'general': ['-o', 'grid'],
      'args': ['find', 'CIM_*', '-n', 'root/cimv2']},
     {'stdout': ['Find class CIM_*',
                 '+-------------+-----------------+',
                 '| Namespace   | Classname       |',
                 '+=============+=================+',
                 '| root/cimv2  | CIM_Foo         |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_Foo_sub     |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_Foo_sub2    |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_Foo_sub_sub |',
                 '+-------------+-----------------+'],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command verify nothing found for BLAH_ regex',
     ['find', 'BLAH_*', '-n', 'root/cimv2'],
     {'stdout': "",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in known namespace with wildcard',
     ['find', '*sub2', '-n', 'root/cimv2'],
     {'stdout': "  root/cimv2:CIM_Foo_sub2",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find with --association filter',
     ['find', '*TST_*', '-n', 'root/cimv2', '--association'],
     {'stdout': ['TST_Lineage',
                 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionSub'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --indicationfilter',
     ['find', '*TST_*', '-n', 'root/cimv2', '--indication'],
     {'stdout': ['TST_Indication', 'root/cimv2:TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --indication & -no-experimental filters',
     ['find', '*TST_*', '-n', 'root/cimv2', '--indication',
      '--no-experimental'],
     {'stdout': ['TST_Indication'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --association & --experimental filters',
     ['find', '*TST_*', '-n', 'root/cimv2', '--association', '--experimental'],
     {'stdout': ['TST_MemberOfFamilyCollectionSub'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    #
    # command "class delete"
    #
    ['Verify class command delete --help response',
     ['delete', '--help'],
     {'stdout': CLASS_DELETE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command delete -h response',
     ['delete', '-h'],
     {'stdout': CLASS_DELETE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    # Class delete successful
    ['Verify class command delete successful with no subclasses, --force',
     ['delete', 'CIM_Foo_sub_sub', '--force'],
     {'stdout': '',
      'test': 'in'},
     [SIMPLE_MOCK_FILE], OK],

    ['Verify class command delete successful with no subclasses and --n option',
     ['delete', 'CIM_Foo_sub_sub', '--namespace', 'root/cimv2', '--force'],
     {'stdout': '',
      'test': 'in'},
     [SIMPLE_MOCK_FILE], OK],

    # Class delete successful
    ['Verify class command delete successful with no subclasses, --verbose',
     {'args': ['delete', 'CIM_Foo_sub_sub', '--force'],
      'general': ['--verbose']},
     {'stdout': ['Deleted class', 'CIM_Foo_sub_sub'],
      'test': 'innows'},
     [SIMPLE_MOCK_FILE], OK],

    ['Verify class command delete fail instances exist',
     ['delete', 'CIM_Foo_sub_sub'],
     {'stderr': 'Delete rejected; instances exist',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    # Class delete errors
    ['Verify class command delete no classname',
     ['delete'],
     {'stderr': ['Error: Missing argument .CLASSNAME.'],
      'rc': 2,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    # class delete error tests

    ['Verify class command delete fail subclasses exist',
     ['delete', 'CIM_Foo', '--force'],
     {'stderr': 'Delete rejected; subclasses exist',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete no classname fails',
     ['delete'],
     {'stderr': ['Error: Missing argument .CLASSNAME.'],
      'rc': 2,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete nonexistent classname fails',
     ['delete', 'Argh'],
     {'stderr': ['CIMError', 'CIM_ERR_INVALID_CLASS', '5'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fails, instances exist',
     ['delete', 'CIM_Foo_sub_sub'],
     {'stderr': 'Delete rejected; instances exist',
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE], OK],

    #
    # command "class tree"
    #
    ['Verify class command tree --help response',
     ['tree', '--help'],
     {'stdout': CLASS_TREE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command tree -h response',
     ['tree', '-h'],
     {'stdout': CLASS_TREE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command tree top down. Uses simple mock, no argument',
     ['tree'],
     {'stdout': """root
 +-- CIM_Foo
     +-- CIM_Foo_sub
     |   +-- CIM_Foo_sub_sub
     +-- CIM_Foo_sub2
""",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command tree top down starting at defined class ',
     ['tree', 'CIM_Foo_sub'],
     {'stdout': """CIM_Foo_sub
+-- CIM_Foo_sub_sub
""",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command tree top down starting at leaf class',
     ['tree', 'CIM_Foo_sub'],
     {'stdout': """CIM_Foo_sub_sub
""",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command tree bottom up. -s',
     ['tree', '-s', 'CIM_Foo_sub_sub'],
     {'stdout': """root
    +-- CIM_Foo
        +-- CIM_Foo_sub
            +-- CIM_Foo_sub_sub
""",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command tree -s from top class',
     ['tree', '-s', 'CIM_Foo'],
     {'stdout': """root
    +-- CIM_Foo
""",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command tree bottom up. --superclasses',
     ['tree', '--superclasses', 'CIM_Foo_sub_sub'],
     {'stdout': """root
    +-- CIM_Foo
        +-- CIM_Foo_sub
            +-- CIM_Foo_sub_sub
""",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    # class tree' error tests
    ['Verify class command tree with invalid CLASSNAME fails',
     ['tree', '-s', 'CIM_Foo_subx'],
     {'stderr': ['CIMError:'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command tree with superclass option, CLASSNAME fails',
     ['tree', '-s'],
     {'stderr': ['Error: CLASSNAME argument required for --superclasses '
                 'option'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    #
    # associators command tests
    #
    #
    ['Verify class command associators --help response',
     ['associators', '--help'],
     {'stdout': CLASS_ASSOCIATORS_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command associators -h response',
     ['associators', '-h'],
     {'stdout': CLASS_ASSOCIATORS_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command associators simple request,',
     ['associators', 'TST_Person'],
     {'stdout': [FAKEURL_STR + '/root/cimv2:TST_Person',
                 'class TST_Person {',
                 '',
                 '      [Key ( true ),',
                 '       Description ( "This is key prop" )]',
                 '   string name;',
                 '',
                 '   string extraProperty = "defaultvalue";',
                 '',
                 '      [ValueMap { "1", "2" },',
                 '       Values { "female", "male" }]',
                 '   uint16 gender;',
                 '',
                 '      [ValueMap { "1", "2" },',
                 '       Values { "books", "movies" }]',
                 '   uint16 likes[];',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command associators simple request names only,',
     ['associators', 'TST_Person', '--names-only'],
     {'stdout': [FAKEURL_STR + '/root/cimv2:TST_Person'],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command associators simple request, one parameter',
     ['associators', 'TST_Person', '--ac', 'TST_MemberOfFamilyCollection'],
     {'stdout': [FAKEURL_STR + '/root/cimv2:TST_Person',
                 'class TST_Person {',
                 '',
                 '      [Key ( true ),',
                 '       Description ( "This is key prop" )]',
                 '   string name;',
                 '',
                 '   string extraProperty = "defaultvalue";',
                 '',
                 '      [ValueMap { "1", "2" },',
                 '       Values { "female", "male" }]',
                 '   uint16 gender;',
                 '',
                 '      [ValueMap { "1", "2" },',
                 '       Values { "books", "movies" }]',
                 '   uint16 likes[];',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command associators request, all filters long',
     ['associators', 'TST_Person',
      '--assoc-class', 'TST_MemberOfFamilyCollection',
      '--role', 'member',
      '--result-role', 'family',
      '--result-class', 'TST_Person'],
     {'stdout': [FAKEURL_STR + '/root/cimv2:TST_Person',
                 'class TST_Person {',
                 '',
                 '      [Key ( true ),',
                 '       Description ( "This is key prop" )]',
                 '   string name;',
                 '',
                 '   string extraProperty = "defaultvalue";',
                 '',
                 '      [ValueMap { "1", "2" },',
                 '       Values { "female", "male" }]',
                 '   uint16 gender;',
                 '',
                 '      [ValueMap { "1", "2" },',
                 '       Values { "books", "movies" }]',
                 '   uint16 likes[];',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command associators request, all filters short',
     ['associators', 'TST_Person',
      '--ac', 'TST_MemberOfFamilyCollection',
      '-r', 'member',
      '--rr', 'family',
      '--rc', 'TST_Person'],
     {'stdout': [FAKEURL_STR + '/root/cimv2:TST_Person',
                 'class TST_Person {',
                 '',
                 '      [Key ( true ),',
                 '       Description ( "This is key prop" )]',
                 '   string name;',
                 '',
                 '   string extraProperty = "defaultvalue";',
                 '',
                 '      [ValueMap { "1", "2" },',
                 '       Values { "female", "male" }]',
                 '   uint16 gender;',
                 '',
                 '      [ValueMap { "1", "2" },',
                 '       Values { "books", "movies" }]',
                 '   uint16 likes[];',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    # Behavior changed pywbem 0.15.0 to exception rtn
    ['Verify class command associators request, all filters short,  -ac '
     'not valid class',
     ['associators', 'TST_Person',
      '--ac', 'TST_MemberOfFamilyCollectionx',
      '-r', 'member',
      '--rr', 'family',
      '--rc', 'TST_Person'],
     {'stderr': ['CIM_ERR_INVALID_PARAMETER'],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    # Behavior changed pywbem 0.15.0 to exception rtn
    ['Verify class command associators request, all filters short,  -r '
     'not valid role',
     ['associators', 'TST_Person',
      '--ac', 'TST_MemberOfFamilyCollection',
      '-r', 'memberx',
      '--rr', 'family',
      '--rc', 'TST_Person'],
     {'stdout': [],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    # Behavior changed pywbem 0.15.0 to exception rtn
    ['Verify class command associators request, all filters short,  --rc '
     'does not valid class',
     ['associators', 'TST_Person',
      '--ac', 'TST_MemberOfFamilyCollection',
      '-r', 'member',
      '--rr', 'family',
      '--rc', 'TST_Personx'],
     {'stderr': ['CIM_ERR_INVALID_PARAMETER'],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    # Behavior changed pywbem 0.15.0 to exception rtn
    ['Verify class command associators request, all filters long '
     'does not pass test',
     ['associators', 'TST_Person',
      '--assoc-class', 'TST_MemberOfFamilyCollection',
      '--role', 'member',
      '--result-role', 'family',
      '--result-class', 'TST_Personx'],
     {'stderr': ['CIM_ERR_INVALID_PARAMETER'],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    # Associator errors

    ['Verify class command associators no CLASSNAME',
     ['associators'],
     {'stderr': ['Error: Missing argument .CLASSNAME.'],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    # Behavior changed pywbem 0.15.0 to exception rtn
    ['Verify class command associators non-existent CLASSNAME rtns error',
     ['associators', 'CIM_Nonexistentclass'],
     {'stderr': ["CIM_ERR_INVALID_PARAMETER"],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command associators non-existent namespace fails',
     ['associators', 'TST_Person', '--namespace', 'blah'],
     {'stderr': ['CIMError', 'CIM_ERR_INVALID_NAMESPACE'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    #
    # references command tests
    #
    ['Verify class command references --help response',
     ['references', '--help'],
     {'stdout': CLASS_REFERENCES_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command references -h response',
     ['references', '-h'],
     {'stdout': CLASS_REFERENCES_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command references simple request',
     ['references', 'TST_Person'],
     {'stdout': ['class TST_Lineage {',
                 'Lineage defines the relationship',
                 'string InstanceID;',
                 'TST_Person REF parent;',
                 'TST_Person REF child;',
                 '[Association ( true )',
                 'Description ( " Family gathers person to family." )',
                 'class TST_MemberOfFamilyCollection {',
                 '[key ( true )]',
                 'TST_Person REF family;',
                 'TST_Person REF member;',
                 ],
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],


    ['Verify class command references simple request -o',
     ['references', 'TST_Person', '--no'],
     {'stdout': [FAKEURL_STR + '/root/cimv2:TST_Lineage',
                 FAKEURL_STR + '/root/cimv2:TST_MemberOfFamilyCollection'],
      'test': 'linesnows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command references request, all filters long',
     ['references', 'TST_Person',
      '--role', 'member',
      '--result-class', 'TST_MemberOfFamilyCollection'],
     {'stdout': REFERENCES_CLASS_RTN_QUALS2,
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command references request, filters short',
     ['references', 'TST_Person',
      '-r', 'member',
      '--rc', 'TST_MemberOfFamilyCollection'],
     {'stdout': REFERENCES_CLASS_RTN_QUALS2,
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command refereces table output fails).',
     {'args': ['associators', 'TST_Person'],
      'general': ['--output-format', 'table']},
     {'stderr': ['Output format "table" ', 'not allowed', 'Only CIM formats:'],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    # Reference errors

    ['Verify class command references no CLASSNAME',
     ['references'],
     {'stderr': ['Error: Missing argument .CLASSNAME.'],
      'rc': 2,
      'test': 'regex'},
     None, OK],

    # Behavior changed pywbem 0.15.0, references bad param rtns except.
    ['Verify class command references non-existent CLASSNAME rtns error',
     ['references', 'CIM_Nonexistentclass'],
     {'stderr': ["CIM_ERR_INVALID_PARAMETER"],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command references non-existent namespace fails',
     ['references', 'TST_Person', '--namespace', 'blah'],
     {'stderr': ['CIMError', 'CIM_ERR_INVALID_NAMESPACE'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    #
    # invokemethod command tests
    #
    ['Verify class command invokemethod --help response',
     ['invokemethod', '--help'],
     {'stdout': CLASS_INVOKEMETHOD_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify class command invokemethod -h response',
     ['invokemethod', '-h'],
     {'stdout': CLASS_INVOKEMETHOD_HELP_LINES,
      'test': 'innows'},
     None, OK],

    #
    #  class invokemethod command without parameters
    #
    ['Verify class command invokemethod CIM_Foo.FuzzyStatic() - no in parms',
     ['invokemethod', 'CIM_Foo', 'FuzzyStatic'],
     {'stdout': ["ReturnValue=0"],
      'rc': 0,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class command invokemethod CIM_Foo.FuzzyStatic() - one in parm',
     ['invokemethod', 'CIM_Foo', 'FuzzyStatic',
      '-p', 'TestInOutParameter="blah"'],
     {'stdout': ['ReturnValue=0',
                 'TestInOutParameter=', 'blah'],
      'rc': 0,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class command invokemethod fails Invalid Class',
     ['invokemethod', 'CIM_Foox', 'FuzzyStatic'],
     {'stderr': ['CIMError', '6'],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class command invokemethod fails Invalid Method',
     ['invokemethod', 'CIM_Foo', 'Fuzzyx'],
     {'stderr': ['Class CIM_Foo does not have a method Fuzzyx'],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class command invokemethod fails non-static method',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stderr': ["Non-static method 'Fuzzy' in class 'CIM_Foo'"],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class command invokemethod fails Method not registered',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stderr': ['CIMError'],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE], OK],

    ['Verify  --timestats gets stats output. Cannot test with lines,execution '
     'time is variable.',
     {'args': ['get', 'CIM_Foo'],
      'general': ['--timestats']},
     {'stdout': ['class CIM_Foo {',
                 'string InstanceID;',
                 'Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 '      1      0',
                 '0           0  GetClass'],
      'rc': 0,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify single command with stdin works',
     {'stdin': ['class get -h']},
     {'stdout': ['Usage: pywbemcli [GENERAL-OPTIONS]  class get '],
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify multiple commands with stdin work',
     {'stdin': ['class get -h', 'class enumerate -h']},
     {'stdout': ['Usage: pywbemcli [GENERAL-OPTIONS] class enumerate ',
                 'Usage: pywbemcli [GENERAL-OPTIONS] class get '],
      'rc': 0,
      'test': 'innows'},
     None, OK],
]

# TODO command class delete. Extend this test to use stdin (delete, test)
# namespace
# TODO: add test for  errors: class invalid, namespace invalid
# other tests.  Test local-only on top level


class TestSubcmdClass(CLITestsBase):  # pylint: disable=too-few-public-methods
    """
    Test all of the class command variations.
    """
    command_group = 'class'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_class(self, desc, inputs, exp_response, mock, condition):
        """
        Common test method for those commands and options in the
        class command that can be tested.  This includes:

          * Subcommands like help that do not require access to a server

          * Subcommands that can be tested with a single execution of a
            pywbemcli command.
        """
        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition)
