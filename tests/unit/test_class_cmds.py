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
import os
import pytest
from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_NAMES_ONLY_HELP_LINE, \
    CMD_OPTION_HELP_HELP_LINE, CMD_OPTION_SUMMARY_HELP_LINE, \
    CMD_OPTION_NAMESPACE_HELP_LINE, CMD_OPTION_PROPERTYLIST_HELP_LINE, \
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE, \
    CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE, CMD_OPTION_NO_QUALIFIERS_HELP_LINE, \
    CMD_OPTION_MULTIPLE_NAMESPACE_HELP_LINE

from .utils import execute_pywbemcli, assert_rc

TEST_DIR = os.path.dirname(__file__)

# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
SIMPLE_MOCK_FILE_EXT = 'simple_mock_model_ext.mof'
INVOKE_METHOD_MOCK_FILE = 'simple_mock_invokemethod.py'
SIMPLE_ASSOC_MOCK_FILE = 'simple_assoc_mock_model.mof'


#
# The following list define the help for each command in terms of particular
# parts of lines that are to be tested.
# For each test, try to include:
# 1. The usage line and in particular the argument component
# 2. The single
# 2. The last line CMD_OPTION_HELP_HELP_LINE
#
CLASS_HELP_LINES = [
    'Usage: pywbemcli class [COMMAND-OPTIONS] COMMAND [ARGS]...',
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
    'Usage: pywbemcli class associators [COMMAND-OPTIONS] CLASSNAME',
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
    'Usage: pywbemcli class delete [COMMAND-OPTIONS] CLASSNAME',
    'Delete a class.',
    '-f, --force Delete any instances of the class as well.',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_ENUMERATE_HELP_LINES = [
    'Usage: pywbemcli class enumerate [COMMAND-OPTIONS] CLASSNAME',
    'List top classes or subclasses of a class in a namespace.',
    '--di, --deep-inheritance Include the complete subclass hierarchy',
    CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE,
    CMD_OPTION_NO_QUALIFIERS_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_NAMES_ONLY_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_FIND_HELP_LINES = [
    'Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME-GLOB',
    'List the classes with matching class names on the server.',
    '-s, --sort                 Sort by namespace. Default is to sort by',
    CMD_OPTION_MULTIPLE_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_GET_HELP_LINES = [
    'Usage: pywbemcli class get [COMMAND-OPTIONS] CLASSNAME',
    'Get a class.',
    CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE,
    CMD_OPTION_NO_QUALIFIERS_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_PROPERTYLIST_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_INVOKEMETHOD_HELP_LINES = [
    'Usage: pywbemcli class invokemethod [COMMAND-OPTIONS] CLASSNAME '
    'METHODNAME',
    'Invoke a method on a class.',
    '-p, --parameter PARAMETERNAME=VALUE Specify a method input parameter',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_REFERENCES_HELP_LINES = [
    'Usage: pywbemcli class references [COMMAND-OPTIONS] CLASSNAME',
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
    'Usage: pywbemcli class tree [COMMAND-OPTIONS] CLASSNAME',
    'Show the subclass or superclass hierarchy for a class.',
    '-s, --superclasses Show the superclass hierarchy.',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

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

      [Description ( "Method with no Parameters" )]
   uint32 DeleteNothing();

};

"""

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

   uint32 DeleteNothing();

};
"""
REFERENCES_CLASS_RTN = [
    '//FakedUrl/root/cimv2:TST_Lineage',
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
    '//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection',
    'class TST_MemberOfFamilyCollection {',
    '',
    '   TST_Person REF family;',
    '',
    '   TST_Person REF member;',
    '',
    '};',
    '']

REFERENCES_CLASS_RTN2 = [
    '//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection',
    'class TST_MemberOfFamilyCollection {',
    '',
    '   TST_Person REF family;',
    '',
    '   TST_Person REF member;',
    '',
    '};',
    '',
    '']

REFERENCES_CLASS_RTN_QUALS1 = """
//FakedUrl/root/cimv2:TST_Lineage
   [Association ( true ),
    Description (
       " Lineage defines the relationship between parents and children." )]
class TST_Lineage {

      [key ( true )]
   string InstanceID;

   TST_Person REF parent;

   TST_Person REF child;

};

//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection
   [Association ( true ),
    Description ( " Family gathers person to family." )]
class TST_MemberOfFamilyCollection {

      [key ( true )]
   TST_Person REF family;

      [key ( true )]
   TST_Person REF member;

};
"""

REFERENCES_CLASS_RTN_QUALS2 = """
//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection
   [Association ( true ),
    Description ( " Family gathers person to family." )]
class TST_MemberOfFamilyCollection {

      [key ( true )]
   TST_Person REF family;

      [key ( true )]
   TST_Person REF member;

};
"""


OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet

# pylint: enable=line-too-long
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

    ['Verify class command --help response',
     ['--help'],
     {'stdout': CLASS_HELP_LINES,
      'test': 'innows'},
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

    ['Verify class command enumerate CIM_Foo summary',
     ['enumerate', 'CIM_Foo', '-s'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo summary',
     ['enumerate', 'CIM_Foo', '--summary'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'linesnows'},
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


    ['Verify class command get with repr output format).',
     {'args': ['enumerate'],
      'general': ['--output-format', 'xml']},
     {'stdout': ['<CLASS( | .+ )NAME="CIM_Foo">',
                 '<PROPERTY( | .+ )NAME="InstanceID"',
                 '<PROPERTY( | .+ )NAME="IntegerProp"',
                 '<METHOD( | .+ )NAME="DeleteNothing"'],
      'test': 'regex'},
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
                 '   uint32 DeleteNothing();',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    # pylint: disable=line-too-long
    ['Verify class command get with propertylist. Tests whole response',
     ['get', 'CIM_Foo_sub2', '--pl', 'InstanceID'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {', '',
                 '      [Key ( true ),',
                 '       Description ( "This is key property." )]', ''
                 '   string InstanceID;', '',
                 '      [Description ( "Method with in and out parameters" )'
                 ']',
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
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {', '',
                 '      [Description ( "Method with in and out parameters" )'
                 ']',
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
                 '      [Description ( "Method with no Parameters" )]',
                 '   uint32 DeleteNothing();',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

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

    # pylint: enable=line-too-long
    # TODO include class origin. TODO not returning class origin correctly.
    ['Verify class command get with propertylist and classorigin,',
     ['get', 'CIM_Foo_sub2', '--pl', 'InstanceID', '-c'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {', '',
                 '      [Key ( true ),',
                 '       Description ( "This is key property." )]', ''
                 '   string InstanceID;', '',
                 '      [Description ( "Method with in and out parameters" )'
                 ']',
                 '   uint32 Fuzzy(',
                 '         [IN ( true ),',
                 '          Description ( "FuzzyMethod Param" )]',
                 '      string FuzzyParameter,',
                 '         [IN ( true ),',
                 '          OUT ( true ),',
                 '          Description ( "Test of ref in/out parameter" )]',
                 '      CIM_Foo REF Foo,',
                 '         [IN ( false ),',
                 '          OUT ( true ),',
                 '          Description ( "TestMethod Param" )]',
                 '      string OutputParam,',
                 '',
                 '      [Description ( "Method with no Parameters" )]',
                 '',
                 '   uint32 DeleteNothing();', '',
                 '};', ''],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, FAIL],

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
     {'stdout': 'CIM_Foo_sub_sub delete successful',
      'test': 'in'},
     [SIMPLE_MOCK_FILE_EXT], OK],

    ['Verify class command delete fail instances exist',
     ['delete', 'CIM_Foo_sub_sub'],
     {'stdout': 'CIM_Foo_sub_sub delete successful',
      'rc': 0,
      'test': 'in'},
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
     {'stderr': 'Error: Delete rejected; subclasses exist',
      'rc': 1,
      'test': 'in'},
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
     {'stderr': 'Error: Delete rejected; instances exist',
      'rc': 1,
      'test': 'in'},
     [SIMPLE_MOCK_FILE_EXT], OK],

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

    # Order inconsistent on output. so we just test that some of the lines are

    # in the output
    # root
    #  +-- CIM_Foo
    #      +-- CIM_Foo_sub2
    #      +-- CIM_Foo_sub
    #          +-- CIM_Foo_sub_sub
    # or
    # root
    #  +-- CIM_Foo
    #      +-- CIM_Foo_sub
    #      |   +-- CIM_Foo_sub_sub
    #      +-- CIM_Foo_sub2
    ['Verify class command tree top down. Order uncertain.',
     ['tree'],
     {'stdout': [r'root',
                 r' \+-- CIM_Foo',
                 r'     \+-- CIM_Foo_sub2',
                 r'     \+-- CIM_Foo_sub',
                 r'[| ]*\+-- CIM_Foo_sub_sub'],  # account for ordering issue
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command tree top down starting at defined class ',
     ['tree', 'CIM_Foo_sub'],
     {'stdout': ['CIM_Foo_sub',
                 ' +-- CIM_Foo_sub_sub'],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command tree bottom up. Ordering guaranteed here',
     ['tree', '-s', 'CIM_Foo_sub_sub'],
     {'stdout': ['root',
                 ' +-- CIM_Foo',
                 '     +-- CIM_Foo_sub',
                 '         +-- CIM_Foo_sub_sub'],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    # class tree' error tests
    ['Verify class command tree with invalid class',
     ['tree', '-s', 'CIM_Foo_subx'],
     {'stderr': ['CIMError:'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command tree with superclass option, no class',
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
     {'stdout': ['//FakedUrl/root/cimv2:TST_Person',
                 'class TST_Person {',
                 '',
                 '      [Key ( true ),',
                 '       Description ( "This is key prop" )]',
                 '   string name;',
                 '',
                 '   string extraProperty = "defaultvalue";',
                 '',
                 '};',
                 ''],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],


    ['Verify class command associators simple request names only,',
     ['associators', 'TST_Person', '--names-only'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Person'],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command associators simple request, one parameter',
     ['associators', 'TST_Person', '--ac', 'TST_MemberOfFamilyCollection'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Person',
                 'class TST_Person {',
                 '',
                 '      [Key ( true ),',
                 '       Description ( "This is key prop" )]',
                 '   string name;',
                 '',
                 '   string extraProperty = "defaultvalue";',
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
     {'stdout': ['//FakedUrl/root/cimv2:TST_Person',
                 'class TST_Person {',
                 '',
                 '      [Key ( true ),',
                 '       Description ( "This is key prop" )]',
                 '   string name;',
                 '',
                 '   string extraProperty = "defaultvalue";',
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
     {'stdout': ['//FakedUrl/root/cimv2:TST_Person',
                 'class TST_Person {',
                 '',
                 '      [Key ( true ),',
                 '       Description ( "This is key prop" )]',
                 '   string name;',
                 '',
                 '   string extraProperty = "defaultvalue";',
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
     {'stdout': REFERENCES_CLASS_RTN_QUALS1,
      'test': 'linesnows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command references simple request -o',
     ['references', 'TST_Person', '--no'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage',
                 '//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection'],
      'test': 'linesnows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command references request, all filters long',
     ['references', 'TST_Person',
      '--role', 'member',
      '--result-class', 'TST_MemberOfFamilyCollection'],
     {'stdout': REFERENCES_CLASS_RTN_QUALS2,
      'test': 'linesnows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],


    ['Verify class command references request, filters short',
     ['references', 'TST_Person',
      '-r', 'member',
      '--rc', 'TST_MemberOfFamilyCollection'],
     {'stdout': REFERENCES_CLASS_RTN_QUALS2,
      'test': 'linesnows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

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
    ['Verify class command invokemethod',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stdout': ["ReturnValue=0"],
      'rc': 0,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class command invokemethod',
     ['invokemethod', 'CIM_Foo', 'Fuzzy', '-p', 'TestInOutParameter="blah"'],
     {'stdout': ['ReturnValue=0',
                 'TestInOutParameter=', 'blah'],
      'rc': 0,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class command invokemethod fails Invalid Class',
     ['invokemethod', 'CIM_Foox', 'Fuzzy', '-p', 'TestInOutParameter="blah"'],
     {'stderr': ["Error: CIMError: 6"],
      'rc': 1,
      'test': 'in'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class command invokemethod fails Invalid Method',
     ['invokemethod', 'CIM_Foo', 'Fuzzyx', '-p', 'TestInOutParameter=blah'],
     {'stderr': ["Error: ClickException: .* CIM_Foo .* Fuzzyx"],
      'rc': 1,
      'test': 'regex'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],


    ['Verify class command invokemethod fails Method not registered',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stderr': ["CIMError: 17"],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE], OK],

    ['Verify  --timestats gets stats output. Cannot test '
     'with lines because execution time is variable.',
     {'args': ['get', 'CIM_Foo'],
      'general': ['--timestats']},
     {'stdout': ['class CIM_Foo {',
                 'string InstanceID;',
                 'Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 '      1      0',
                 '0           0  GetClass'],
      'rc': 0,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify single command with stdin works',
     {'stdin': ['class get -h']},
     {'stdout': ['Usage: pywbemcli  class get '],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify multiple commands with stdin work',
     {'stdin': ['class get -h', 'class enumerate -h']},
     {'stdout': ['Usage: pywbemcli  class enumerate ',
                 'Usage: pywbemcli  class get '],
      'rc': 0,
      'test': 'regex'},
     None, OK],
]

# TODO command class delete. Extend this test to use stdin (delete, test)
# namespace
# TODO: add test for  errors: class invalid, namespace invalid
# other tests.  Test local-only on top level


# TODO the following two test classes should be removed as I believe they
# are redundant.


class TestSubcmdClass(CLITestsBase):
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
                          mock, condition, verbose=False)


class TestClassGeneral(object):
    # pylint: disable=too-few-public-methods, useless-object-inheritance
    """
    Test class using pytest for the commands of the class command
    """
    # @pytest.mark.skip(reason="Unfinished test")
    def test_class_error_no_server(self):  # pylint: disable=no-self-use
        """Test 'pywbemcli ... class getclass' when no host is provided

        This test runs against a real url so we set timeout to the mininum
        to minimize test time since the expected result is a timeout exception.
        """

        # Invoke the command to be tested
        rc, stdout, stderr = execute_pywbemcli(['-s', 'http://fred', '-t', '1',
                                                'class', 'get', 'CIM_blah'])

        assert_rc(1, rc, stdout, stderr, "test_class_error_no_server")

        assert stdout == ""
        assert stderr.startswith(
            "Error: ConnectionError"), \
            "stderr={!r}".format(stderr)


class TestClassEnumerate(object):
    # pylint: disable=too-few-public-methods, useless-object-inheritance
    """
    Test the options of the pywbemcli class enumerate' command
    """
    @pytest.mark.parametrize(
        "desc, tst_args, exp_result_start, exp_result_end",
        [
            [
                ["No extra parameters"],
                [],
                '   [Description ( "Simple CIM Class" )]\n',
                None
            ],
            [
                ["Class parameter"],
                ['CIM_Foo'],
                '   [Description ( "Subclass of CIM_Foo" )]\n',
                None
            ]
        ]
    )
    # pylint: disable=unused-argument
    def test_enumerate_simple_mock(self, desc, tst_args, exp_result_start,
                                   exp_result_end):
        # pylint: disable=no-self-use
        """
        Test 'pywbemcli class enumerate command based on a simple set of
        classes defined in the file simple_mock_model.mof
        """
        mock_mof_path = os.path.join(TEST_DIR, 'simple_mock_model.mof')

        # build basic cmd line, server, mock-server def, basic enum command
        cmd_line = ['--mock-server', mock_mof_path, 'class', 'enumerate']

        if tst_args:
            cmd_line.extend(tst_args)
        rc, stdout, stderr = execute_pywbemcli(cmd_line)

        assert_rc(0, rc, stdout, stderr, "test_enumerate_simple_mock")
        assert stderr == ""
        assert stdout.startswith(exp_result_start)
