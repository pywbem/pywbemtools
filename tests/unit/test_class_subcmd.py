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
Tests the class subcommand
"""
import os
import pytest
from .cli_test_extensions import CLITestsBase

from .utils import execute_pywbemcli, assert_rc

TEST_DIR = os.path.dirname(__file__)

# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
SIMPLE_MOCK_FILE_EXT = 'simple_mock_model_ext.mof'
INVOKE_METHOD_MOCK_FILE = 'simple_mock_invokemethod.py'
SIMPLE_ASSOC_MOCK_FILE = 'simple_assoc_mock_model.mof'

CLS_HELP = """
Usage: pywbemcli class [COMMAND-OPTIONS] COMMAND [ARGS]...

  Command group to manage CIM classes.

  In addition to the command-specific options shown in this help text, the
  general options (see 'pywbemcli --help') can also be specified before the
  command. These are NOT retained after the command is executed.

Options:
  -h, --help  Show this message and exit.

Commands:
  associators   Get the associated classes for CLASSNAME.
  delete        Delete a single CIM class.
  enumerate     Enumerate classes from the WBEM Server.
  find          Find all classes that match CLASSNAME-GLOB.
  get           Get and display a single CIM class.
  invokemethod  Invoke the class method named methodname.
  references    Get the reference classes for CLASSNAME.
  tree          Display CIM class inheritance hierarchy tree.
"""

CLS_GET_HELP = """
Usage: pywbemcli class get [COMMAND-OPTIONS] CLASSNAME

  Get and display a single CIM class.

  Get a single CIM class defined by the CLASSNAME argument from the WBEM
  server and display it. Normally it is retrieved from the default namespace
  in the server.

  If the class is not found in the WBEM Server, the server returns an
  exception.

  The --includeclassorigin, --includeclassqualifiers, and --propertylist
  options determine what parts of the class definition are retrieved.

  Results are formatted as defined by the output format general option.

Options:
  -l, --localonly                 Show only local properties of the class.
  --no-qualifiers                 If set, request server to not include
                                  qualifiers in the returned class(s). The
                                  default behavior is to request qualifiers in
                                  returned class(s).
  -c, --includeclassorigin        Request that server include classorigin in
                                  the result.On some WBEM operations, server
                                  may ignore this option.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  option not specified a Null property list is
                                  created and the server returns all
                                  properties. Multiple properties may be
                                  defined with either a comma separated list
                                  or by using the option multiple times. (ex:
                                  -p pn1 -p pn22 or -p pn1,pn2). If defined as
                                  empty string the server should return no
                                  properties.
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -h, --help                      Show this message and exit.
"""


CLS_ENUM_HELP = """
Usage: pywbemcli class enumerate [COMMAND-OPTIONS] CLASSNAME

  Enumerate classes from the WBEM Server.

  Enumerates the classes (or classnames) from the WBEMServer starting either
  at the top of the class hierarchy or from  the position in the class
  hierarchy defined by `CLASSNAME` argument if provided.

  The output format is defined by the output-format general option.

  The includeclassqualifiers, includeclassorigin options define optional
  information to be included in the output.

  The deepinheritance option defines whether the complete hiearchy is
  retrieved or just the next level in the hiearchy.

  Results are formatted as defined by the output format general option.

Options:
  -d, --deepinheritance     Return complete subclass hierarchy for this class
                            if set. Otherwise retrieve only the next hierarchy
                            level.
  -l, --localonly           Show only local properties of the class.
  --no-qualifiers           If set, request server to not include qualifiers
                            in the returned class(s). The default behavior is
                            to request qualifiers in returned class(s).
  -c, --includeclassorigin  Request that server include classorigin in the
                            result.On some WBEM operations, server may ignore
                            this option.
  -o, --names_only          Show only the returned object names.
  -s, --sort                Sort into alphabetical order by classname.
  -n, --namespace <name>    Namespace to use for this operation. If defined
                            that namespace overrides the general options
                            namespace
  -S, --summary             Return only summary of objects (count).
  -h, --help                Show this message and exit.
"""

CLASS_FIND_HELP = """
Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME-GLOB

  Find all classes that match CLASSNAME-GLOB.

  Find all classes in the namespace(s) of the target WBEMServer that match
  the CLASSNAME-GLOB regular expression argument and return the classnames.
  The CLASSNAME-GLOB argument is required.

  The CLASSNAME-GLOB argument may be either a complete classname or a
  regular expression that can be matched to one or more classnames. To limit
  the filter to a single classname, terminate the classname with $.

  The GLOB expression is anchored to the beginning of the CLASSNAME-GLOB, is
  is case insensitive and uses the standard GLOB special characters (*(match
  everything), ?(match single character)). Thus, `pywbem_*` returns all
  classes that begin with `PyWBEM_`, `pywbem_`, etc. '.*system*' returns
  classnames that include the case insensitive string `system`.

  The namespace option limits the search to the defined namespaces.
  Otherwise all namespaces in the target server are searched.

  Output is in table format if table output specified. Otherwise it is in
  the form <namespace>:<classname>

Options:
  -s, --sort              Sort into alphabetical order by classname.
  -n, --namespace <name>  Namespace(s) to use for this operation. If defined
                          only those namespaces are searched rather than all
                          available namespaces. ex: -n root/interop -n
                          root/cimv2
  -h, --help              Show this message and exit.
"""
CLASS_TREE_HELP = """
Usage: pywbemcli class tree [COMMAND-OPTIONS] CLASSNAME

  Display CIM class inheritance hierarchy tree.

  Displays a tree of the class hiearchy to show superclasses and subclasses.

  CLASSNAMe is an optional argument that defines the starting point for the
  hiearchy display

  If the --superclasses option not specified the hiearchy starting either at
  the top most classes of the class hiearchy or at the class defined by
  CLASSNAME is displayed.

  if the --superclasses options is specified and a CLASSNAME is defined the
  class hiearchy of superclasses leading to CLASSNAME is displayed.

  This is a separate subcommand because it is tied specifically to
  displaying in a tree format.so that the --output-format general option is
  ignored.

Options:
  -s, --superclasses      Display the superclasses to CLASSNAME as a tree.
                          When this option is set, the CLASSNAME argument is
                          required
  -n, --namespace <name>  Namespace to use for this operation. If defined that
                          namespace overrides the general options namespace
  -h, --help              Show this message and exit.
"""

CLASS_DELETE_HELP = """
Usage: pywbemcli class delete [COMMAND-OPTIONS] CLASSNAME

  Delete a single CIM class.

  Deletes the CIM class defined by CLASSNAME from the WBEM Server.

  If the class has instances, the command is refused unless the --force
  option is used. If --force is used, instances are also deleted.

  If the class has subclasses, the command is rejected.

  WARNING: Removing classes from a WBEM Server can cause damage to the
  server. Use this with caution.  It can impact instance providers and other
  components in the server.

  Some servers may refuse the operation.

Options:
  -f, --force             Force the delete request to be issued even if there
                          are instances in the server or subclasses to this
                          class. The WBEM Server may still refuse the request.
  -n, --namespace <name>  Namespace to use for this operation. If defined that
                          namespace overrides the general options namespace
  -h, --help              Show this message and exit.
"""

CLS_REFERENCES_HELP = """
Usage: pywbemcli class references [COMMAND-OPTIONS] CLASSNAME

  Get the reference classes for CLASSNAME.

  Get the reference classes (or class names) for the CLASSNAME argument
  filtered by the role and result class options and modified by the other
  options.

  Results are displayed as defined by the output format general option.

Options:
  -R, --resultclass <class name>  Filter by the result classname provided.
                                  Each returned class (or classname) should be
                                  this class or its subclasses. Optional.
  -r, --role <role name>          Filter by the role name provided. Each
                                  returned class (or classname) should refer
                                  to the target class through a property with
                                  a name that matches the value of this
                                  parameter. Optional.
  --no-qualifiers                 If set, request server to not include
                                  qualifiers in the returned class(s). The
                                  default behavior is to request qualifiers in
                                  returned class(s).
  -c, --includeclassorigin        Request that server include classorigin in
                                  the result.On some WBEM operations, server
                                  may ignore this option.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  option not specified a Null property list is
                                  created and the server returns all
                                  properties. Multiple properties may be
                                  defined with either a comma separated list
                                  or by using the option multiple times. (ex:
                                  -p pn1 -p pn22 or -p pn1,pn2). If defined as
                                  empty string the server should return no
                                  properties.
  -o, --names_only                Show only the returned object names.
  -s, --sort                      Sort into alphabetical order by classname.
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -S, --summary                   Return only summary of objects (count).
  -h, --help                      Show this message and exit.
"""

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
    '', ]

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
    # inputs - String, or list of args or dict of 'env', 'args', 'globals',
    #          and 'stdin'. See See CLITestsBase.subcmd_test()  for
    #          detailed documentation
    # exp_response - Dictionary of expected responses (stdout, stderr, rc) and
    #                test definition (test: <testname>).
    #                See CLITestsBase.subcmd_test() for detailed documentation.
    # mock - None or name of files (mof or .py),
    # condition - If True, the test is executed,  Otherwise it is skipped.

    ['Verify class subcommand help response',
     '--help',
     {'stdout': CLS_HELP,
      'test': 'linesnows'},
     None, OK],
    #
    # Enumerate subcommand and its options
    #
    ['Verify class subcommand enumerate  --help response',
     ['enumerate', '--help'],
     {'stdout': CLS_ENUM_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify class subcommand enumerate  -h response.',
     ['enumerate', '-h'],
     {'stdout': CLS_ENUM_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify class subcommand enumerate CIM_Foo',
     ['enumerate', 'CIM_Foo'],
     {'stdout': '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo local only',
     ['enumerate', 'CIM_Foo', '-l'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo_sub',
     ['enumerate', 'CIM_Foo_sub'],
     {'stdout': CIMFOO_SUB_SUB,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify class subcommand enumerate CIM_Foo localonly',
     ['enumerate', 'CIM_Foo', '--localonly'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo -no-qualifiers',
     ['enumerate', 'CIM_Foo_sub', '--no-qualifiers'],
     {'stdout': CIMFOO_SUB_SUB_NO_QUALS,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo -d',
     ['enumerate', 'CIM_Foo', '-d'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo --deepinheritance',
     ['enumerate', 'CIM_Foo', '--deepinheritance'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo -c',
     ['enumerate', 'CIM_Foo', '-c'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo --includeclassorigin',
     ['enumerate', 'CIM_Foo', '--includeclassorigin'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo -o names only',
     ['enumerate', 'CIM_Foo', '-o'],
     {'stdout': ['CIM_Foo', 'CIM_Foo_sub', 'CIM_Foo_sub2'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo --names_only',
     ['enumerate', 'CIM_Foo', '--names_only'],
     {'stdout': ['CIM_Foo', 'CIM_Foo_sub', 'CIM_Foo_sub2'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo summary',
     ['enumerate', 'CIM_Foo', '-S'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo summary',
     ['enumerate', 'CIM_Foo', '--summary'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo names and deepinheritance',
     ['enumerate', 'CIM_Foo', '-do'],
     {'stdout': ['CIM_Foo_sub', 'CIM_Foo_sub2', 'CIM_Foo_sub_sub'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand enumerate CIM_Foo include qualifiers',
     ['enumerate', 'CIM_Foo'],
     {'stdout': ['Key ( true )', '[Description (', 'class CIM_Foo'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    #
    # Test class get
    #
    ['Verify class subcommand get --help response',
     ['get', '--help'],
     {'stdout': CLS_GET_HELP,
      'test': 'linesnows'},
     None, OK],

    # subcommand get localonly option
    ['Verify class subcommand get not localonly. Tests for property names',
     ['get', 'CIM_Foo_sub2'],
     {'stdout': ['string cimfoo_sub2;', 'InstanceID', 'IntegerProp', 'Fuzzy',
                 'Key ( true )', 'IN ( false )'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand get localonly. Tests whole response with -l',
     ['get', 'CIM_Foo_sub2', '-l'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '};', '', ],
      'test': 'patterns'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand get localonly. Tests whole response --localonly',
     ['get', 'CIM_Foo_sub2', '--localonly'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '};', '', ],
      'test': 'patterns'},
     SIMPLE_MOCK_FILE, OK],

    # includequalifiers. Test the flag that excludes qualifiers
    ['Verify class subcommand get without qualifiers, . Tests whole response',
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
                 '', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    # pylint: disable=line-too-long
    ['Verify class subcommand get with propertylist, . Tests whole response',
     ['get', 'CIM_Foo_sub2', '-p', 'InstanceID'],
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
                 '', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand get with empty propertylist, . Tests whole '
     'response',
     ['get', 'CIM_Foo_sub2', '-p', '""'],
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
                 '', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    # pylint: enable=line-too-long
    # TODO include class origin. TODO not returning class origin correctly.
    ['Verify class subcommand get with propertylist and classorigin,',
     ['get', 'CIM_Foo_sub2', '-p', 'InstanceID', '-c'],
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
                 '};', '', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, FAIL],

    #
    # find subcommand
    #
    ['Verify class subcommand find -h, ',
     ['find', '-h'],
     {'stdout': CLASS_FIND_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify class subcommand find  --help',
     ['find', '--help'],
     {'stdout': CLASS_FIND_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify class subcommand find simple name in all namespaces',
     ['find', 'CIM_*'],
     {'stdout': ["  root/cimv2:CIM_Foo",
                 "  root/cimv2:CIM_Foo_sub",
                 "  root/cimv2:CIM_Foo_sub2",
                 "  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand find simple name in all namespaces wo case',
     ['find', 'cim_*'],
     {'stdout': ["  root/cimv2:CIM_Foo",
                 "  root/cimv2:CIM_Foo_sub",
                 "  root/cimv2:CIM_Foo_sub2",
                 "  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand find simple name in all namespaces lead wc',
     ['find', '*sub_sub*'],
     {'stdout': ["  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify class subcommand find simple name in all namespaces wo case',
     ['find', '*sub_su?*'],
     {'stdout': ["  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand find simple name in known namespace',
     ['find', 'CIM_*', '-n', 'root/cimv2'],
     {'stdout': ["  root/cimv2:CIM_Foo",
                 "  root/cimv2:CIM_Foo_sub",
                 "  root/cimv2:CIM_Foo_sub2",
                 "  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand find simple name in known namespace with -s',
     ['find', 'CIM_*', '-n', 'root/cimv2', '-s'],
     {'stdout': ["  root/cimv2:CIM_Foo",
                 "  root/cimv2:CIM_Foo_sub",
                 "  root/cimv2:CIM_Foo_sub2",
                 "  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand find simple name in known namespace with --sort',
     ['find', 'CIM_*', '-n', 'root/cimv2', '-s'],
     {'stdout': ["  root/cimv2:CIM_Foo",
                 "  root/cimv2:CIM_Foo_sub",
                 "  root/cimv2:CIM_Foo_sub2",
                 "  root/cimv2:CIM_Foo_sub_sub"],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand find name in known namespace with -s, 0 grid',
     {'global': ['-o', 'grid'],
      'args': ['find', 'CIM_*', '-n', 'root/cimv2', '-s']},
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
                 '+-------------+-----------------+', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand verify nothing found for BLAH_ regex',
     ['find', 'BLAH_*', '-n', 'root/cimv2'],
     {'stdout': "",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcmd find simple name in known namespace with wildcard',
     ['find', '*sub2', '-n', 'root/cimv2'],
     {'stdout': "  root/cimv2:CIM_Foo_sub2",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    #
    # subcommand "class delete"
    #
    ['Verify class subcommand delete --help response',
     ['delete', '--help'],
     {'stdout': CLASS_DELETE_HELP,
      'test': 'linesnows'},
     None, OK],

    # Class delete successful
    ['Verify class subcommand delete successful with no subclasses, --force',
     ['delete', 'CIM_Foo_sub_sub', '--force'],
     {'stdout': 'CIM_Foo_sub_sub delete successful',
      'test': 'in'},
     [SIMPLE_MOCK_FILE_EXT], OK],

    ['Verify class subcommand delete fail instances exist',
     ['delete', 'CIM_Foo_sub_sub'],
     {'stdout': 'CIM_Foo_sub_sub delete successful',
      'rc': 0,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    # Class delete errors
    ['Verify class subcommand delete no classname',
     ['delete'],
     {'stderr': 'Error: Missing argument "CLASSNAME"',
      'rc': 2,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand delete fail subclasses exist',
     ['delete', 'CIM_Foo', '--force'],
     {'stderr': 'Error: Delete rejected; subclasses exist',
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    #
    ['Verify class subcommand delete faile, instances exist',
     ['delete', 'CIM_Foo_sub_sub'],
     {'stderr': 'Error: Delete rejected; instances exist',
      'rc': 1,
      'test': 'in'},
     [SIMPLE_MOCK_FILE_EXT], OK],

    #
    # subcommand "class tree"
    #
    ['Verify class subcommand tree --help response',
     ['tree', '--help'],
     {'stdout': CLASS_TREE_HELP,
      'test': 'linesnows'},
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
    ['Verify class subcommand tree top down. Order uncertain.',
     ['tree'],
     {'stdout': [r'root',
                 r' \+-- CIM_Foo',
                 r'     \+-- CIM_Foo_sub2',
                 r'     \+-- CIM_Foo_sub',
                 r'[| ]*\+-- CIM_Foo_sub_sub', ],  # account for ordering issue
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand tree top down starting at defined class ',
     ['tree', 'CIM_Foo_sub'],
     {'stdout': ['CIM_Foo_sub',
                 ' +-- CIM_Foo_sub_sub', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand tree bottom up. Ordering guaranteed here',
     ['tree', '-s', 'CIM_Foo_sub_sub'],
     {'stdout': ['root',
                 ' +-- CIM_Foo',
                 '     +-- CIM_Foo_sub',
                 '         +-- CIM_Foo_sub_sub', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    # class tree' error tests
    ['Verify class subcommand tree with invalid class',
     ['tree', '-s', 'CIM_Foo_subx'],
     {'stderr': ['CIMError:'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class subcommand tree with superclass option, no class',
     ['tree', '-s'],
     {'stderr': ['Error: Classname argument required for superclasses option'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    #
    # associators subcommand tests
    #
    ['Verify class subcommand associators --help, . ',
     ['associators', '--help'],
     {'stdout': ['Usage: pywbemcli class associators [COMMAND-OPTIONS] '
                 'CLASSNAME',
                 'Get the associated classes for CLASSNAME.',
                 '-a, --assocclass <class name>   Filter by the association '
                 'class name',
                 '-C, --resultclass <class name>  Filter by the association '
                 'result class name',
                 '-r, --role <role name>          Filter by the role name '
                 'provided.',
                 '-R, --resultrole <role name>    Filter by the result role '
                 'name provided.',
                 '-c, --includeclassorigin', ],
      'test': 'in'},
     None, OK],

    ['Verify class subcommand associators simple request,',
     ['associators', 'TST_Person', ],
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

    ['Verify class subcommand associators simple request, one parameter',
     ['associators', 'TST_Person', '-a', 'TST_MemberOfFamilyCollection'],
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

    ['Verify class subcommand associators request, all filters long',
     ['associators', 'TST_Person',
      '--assocclass', 'TST_MemberOfFamilyCollection',
      '--role', 'member',
      '--resultrole', 'family',
      '--resultclass', 'TST_Person'],
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

    ['Verify class subcommand associators request, all filters short',
     ['associators', 'TST_Person',
      '-a', 'TST_MemberOfFamilyCollection',
      '-r', 'member',
      '-R', 'family',
      '-C', 'TST_Person'],
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

    ['Verify class subcommand associators request, all filters short,  -a '
     'does not pass test',
     ['associators', 'TST_Person',
      '-a', 'TST_MemberOfFamilyCollectionx',
      '-r', 'member',
      '-R', 'family',
      '-C', 'TST_Person'],
     {'stdout': [],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class subcommand associators request, all filters short,  -r '
     'does not pass test',
     ['associators', 'TST_Person',
      '-a', 'TST_MemberOfFamilyCollection',
      '-r', 'memberx',
      '-R', 'family',
      '-C', 'TST_Person'],
     {'stdout': [],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class subcommand associators request, all filters short,  -R '
     'does not pass test',
     ['associators', 'TST_Person',
      '-a', 'TST_MemberOfFamilyCollection',
      '-r', 'member',
      '-R', 'familyx',
      '-C', 'TST_Person'],
     {'stdout': [],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class subcommand associators request, all filters short,  -C '
     'does not pass test',
     ['associators', 'TST_Person',
      '-a', 'TST_MemberOfFamilyCollection',
      '-r', 'member',
      '-R', 'family',
      '-C', 'TST_Personx'],
     {'stdout': [],
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    # Associator errors

    ['Verify class subcommand associators no CLASSNAM, . ',
     ['associators'],
     {'stderr': ['Error: Missing argument "CLASSNAME".', ],
      'rc': 2,
      'test': 'in'},
     None, OK],

    #
    # references subcommand tests
    #
    ['Verify class subcommand references --help, . ',
     ['references', '--help'],
     {'stdout': CLS_REFERENCES_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify class subcommand references simple request, -s',
     ['references', 'TST_Person', '-s'],
     {'stdout': REFERENCES_CLASS_RTN_QUALS1,
      'test': 'linesnows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class subcommand references simple request -o -s',
     ['references', 'TST_Person', '-o', '-s'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage',
                 '//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection'],
      'test': 'linesnows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class subcommand references request, all filters long',
     ['references', 'TST_Person',
      '--role', 'member',
      '--resultclass', 'TST_MemberOfFamilyCollection'],
     {'stdout': REFERENCES_CLASS_RTN_QUALS2,
      'test': 'linesnows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],


    # Reference errors

    ['Verify class subcommand references no CLASSNAME',
     ['references'],
     {'stderr': ['Error: Missing argument "CLASSNAME".', ],
      'rc': 2,
      'test': 'in'},
     None, OK],

    #
    # invokemethod subcommand tests
    #
    ['Verify class subcommand invokemethod --help, . ',
     ['invokemethod', '--help'],
     {'stdout': ['Usage: pywbemcli class invokemethod [COMMAND-OPTIONS] '
                 'CLASSNAME METHODNAME',
                 'Invoke the class method named methodname.',
                 '-p, --parameter parameter  Optional multiple method '
                 'parameters of form', ],
      'test': 'in'},
     None, OK],

    #
    #  class invokemethod subcommand without parameters
    #
    ['Verify class subcommand invokemethod',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stdout': ["ReturnValue=0"],
      'rc': 0,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class subcommand invokemethod',
     ['invokemethod', 'CIM_Foo', 'Fuzzy', '-p', 'TestInOutParameter="blah"'],
     {'stdout': ["ReturnValue=0"],
      'rc': 0,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class subcommand invokemethod fails Invalid Class',
     ['invokemethod', 'CIM_Foox', 'Fuzzy', '-p', 'TestInOutParameter="blah"'],
     {'stderr': ["Error: CIMError: 6"],
      'rc': 1,
      'test': 'in'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class subcommand invokemethod fails Invalid Method',
     ['invokemethod', 'CIM_Foo', 'Fuzzyx', '-p', 'TestInOutParameter=blah'],
     {'stderr': ["Error: CIMError: 17"],
      'rc': 1,
      'test': 'in'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],


    ['Verify class subcommand invokemethod fails Method not registered',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stderr': ["Error: CIMError: 17"],
      'rc': 1,
      'test': 'in'},
     [SIMPLE_MOCK_FILE], OK],

    ['Verify  --timestats gets stats output. Cannot test '
     'with lines because execution time is variable.',
     {'args': ['get', 'CIM_Foo'],
      'global': ['--timestats']},
     {'stdout': ['class CIM_Foo {',
                 'string InstanceID;',
                 'Count    Exc    Time    ReqLen    ReplyLen  Operation',
                 '      1      0',
                 '0           0  GetClass'],
      'rc': 0,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify single subcommand with stdin works',
     {'stdin': ['class get -h']},
     {'stdout': ['Usage: pywbemcli  class get '],
      'rc': 0,
      'test': 'regex'},
     None, OK],

    ['Verify multiple subcommands with stdin work',
     {'stdin': ['class get -h', 'class enumerate -h']},
     {'stdout': ['Usage: pywbemcli  class enumerate ',
                 'Usage: pywbemcli  class get '],
      'rc': 0,
      'test': 'regex'},
     None, OK],
]

# TODO subcommand class delete. Extend this test to use stdin (delete, test)
# namespace
# TODO: add test for  errors: class invalid, namespace invalid
# other tests.  Test localonly on top level


class TestSubcmdClass(CLITestsBase):
    """
    Test all of the class subcommand variations.
    """
    subcmd = 'class'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_class(self, desc, inputs, exp_response, mock, condition):
        """
        Common test method for those subcommands and options in the
        class subcmd that can be tested.  This includes:

          * Subcommands like help that do not require access to a server

          * Subcommands that can be tested with a single execution of a
            pywbemcli command.
        """
        self.subcmd_test(desc, self.subcmd, inputs, exp_response,
                         mock, condition, verbose=False)


class TestClassGeneral(object):
    # pylint: disable=too-few-public-methods, useless-object-inheritance
    """
    Test class using pytest for the subcommands of the class subcommand
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

        assert_rc(1, rc, stdout, stderr)

        assert stdout == ""
        assert stderr.startswith(
            "Error: ConnectionError"), \
            "stderr={!r}".format(stderr)


class TestClassEnumerate(object):
    # pylint: disable=too-few-public-methods, useless-object-inheritance
    """
    Test the options of the pywbemcli class enumerate' subcommand
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
        Test 'pywbemcli class enumerate subcommand based on a simple set of
        classes defined in the file simple_mock_model.mof
        """
        mock_mof_path = os.path.join(TEST_DIR, 'simple_mock_model.mof')

        # build basic cmd line, server, mock-server def, basic enum command
        cmd_line = ['-s', 'http:/blah', '--mock-server',
                    mock_mof_path, 'class', 'enumerate']

        if tst_args:
            cmd_line.extend(tst_args)
        rc, stdout, stderr = execute_pywbemcli(cmd_line)

        assert_rc(0, rc, stdout, stderr)
        assert stderr == ""
        assert stdout.startswith(exp_result_start)
