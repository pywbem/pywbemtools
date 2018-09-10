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
INVOKE_METHOD_MOCK_FILE = 'simple_mock_invokemethod.py'

CLS_HELP = """Usage: pywbemcli class [COMMAND-OPTIONS] COMMAND [ARGS]...

  Command group to manage CIM classes.

  In addition to the command-specific options shown in this help text, the
  general options (see 'pywbemcli --help') can also be specified before the
  command. These are NOT retained after the command is executed.

Options:
  -h, --help  Show this message and exit.

Commands:
  associators   Get the associated classes for CLASSNAME.
  delete        Delete a single class.
  enumerate     Enumerate classes from the WBEM Server.
  find          Find all classes that match CLASSNAME-REGEX.
  get           Get and display a single CIM class.
  invokemethod  Invoke the class method named methodname.
  references    Get the reference classes for CLASSNAME.
  tree          Display CIM class inheritance hierarchy tree.
"""

CLS_ENUM_HELP = """Usage: pywbemcli class enumerate [COMMAND-OPTIONS] CLASSNAME

  Enumerate classes from the WBEM Server.

  Enumerates the classes (or classnames) from the WBEMServer starting either
  at the top of the class hierarchy or from  the position in the class
  hierarchy defined by `CLASSNAME` argument if provided.

  The output format is defined by the output-format global option.

  The includeclassqualifiers, includeclassorigin options define optional
  information to be included in the output.

  The deepinheritance option defines whether the complete hiearchy is
  retrieved or just the next level in the hiearchy.

Options:
  -d, --deepinheritance     Return complete subclass hierarchy for this class
                            if set. Otherwise retrieve only the next hierarchy
                            level.
  -l, --localonly           Show only local properties of the class.
  --no-qualifiers           If set, request server to not include qualifiers
                            in the returned class(s). The default behavior is
                            to request include qualifiers in the returned
                            class(s).
  -c, --includeclassorigin  Include classorigin in the result.
  -o, --names_only          Show only local properties of the class.
  -s, --sort                Sort into alphabetical order by classname.
  -n, --namespace <name>    Namespace to use for this operation. If defined
                            that namespace overrides the general options
                            namespace
  -S, --summary             Return only summary of objects (count).
  -h, --help                Show this message and exit.
"""

# pylint: disable=line-too-long
CLASS_FIND_HELP = """Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME-REGEX

  Find all classes that match CLASSNAME-REGEX.

  Find all classes in the namespace(s) of the target WBEMServer that match
  the CLASSNAME-REGEX regular expression argument. The CLASSNAME-REGEX
  argument is required.

  The CLASSNAME-REGEX argument may be either a complete classname or a
  regular expression that can be matched to one or more classnames. To limit
  the filter to a single classname, terminate the classname with $.

  The regular expression is anchored to the beginning of the classname and
  is case insensitive. Thus, `pywbem_` returns all classes that begin with
  `PyWBEM_`, `pywbem_`, etc.

  The namespace option limits the search to the defined namespace. Otherwise
  all namespaces in the target server are searched.

  Output is in table format if table output specified. Otherwise it is in
  the form <namespace>:<classname>

Options:
  -s, --sort              Sort into alphabetical order by classname.
  -n, --namespace <name>  Namespace to use for this operation. If defined that
                          namespace overrides the general options namespace
  -h, --help              Show this message and exit.
"""  # pylint: enable=line-too-long

CLASS_TREE_HELP = """Usage: pywbemcli class tree [COMMAND-OPTIONS] CLASSNAME

  Display CIM class inheritance hierarchy tree.

  Displays a tree of the class hiearchy to show superclasses and subclasses.

  CLASSNAMe is an optional argument that defines the starting point for the
  hiearchy display

  If the --superclasses option not specified the hiearchy starting either at
  the top most classes of the class hiearchy or at the class defined by
  CLASSNAME is displayed.

  if the --superclasses options is specified and a CLASSNAME is defined the
  class hiearchy of superclasses leading to CLASSNAME is displayed.

  This is a separate subcommand because t is tied specifically to displaying
  in a tree format.so that the --output-format global option is ignored.

Options:
  -s, --superclasses      Display the superclasses to CLASSNAME as a tree.
                          When this option is set, the CLASSNAME argument is
                          required
  -n, --namespace <name>  Namespace to use for this operation. If defined that
                          namespace overrides the general options namespace
  -h, --help              Show this message and exit.
"""

OK = True
RUN = True
FAIL = False

# pylint: enable=line-too-long
MOCK_TEST_CASES = [
    # desc - Description of test
    # args - List of arguments or string of arguments
    # exp_response - Dictionary of expected responses,
    # mock - None or name of files (mof or .py),
    # condition - If True, the test is executed,  Otherwise it is skipped.

    ['class subcommand help response',
     '--help',
     {'stdout': CLS_HELP,
      'test': 'lines'},
     None, OK],
    #
    # Enumerate subcommand and its options
    #
    ['class subcommand enumerate  --help response',
     ['enumerate', '--help'],
     {'stdout': CLS_ENUM_HELP,
      'test': 'lines'},
     None, OK],

    ['class subcommand enumerate  -h response.',
     ['enumerate', '-h'],
     {'stdout': CLS_ENUM_HELP,
      'test': 'lines'},
     None, OK],

    ['class subcommand enumerate CIM_Foo',
     ['enumerate', 'CIM_Foo'],
     {'stdout': '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo local only',
     ['enumerate', 'CIM_Foo', '-l'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo localonly',
     ['enumerate', 'CIM_Foo', '--localonly'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo -d',
     ['enumerate', 'CIM_Foo', '-d'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo --deepinheritance',
     ['enumerate', 'CIM_Foo', '--deepinheritance'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo -c',
     ['enumerate', 'CIM_Foo', '-c'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo --includeclassorigin',
     ['enumerate', 'CIM_Foo', '--includeclassorigin'],
     {'stdout':
      '   [Description ( "Subclass of CIM_Foo" )]',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo -o names only',
     ['enumerate', 'CIM_Foo', '-o'],
     {'stdout': 'CIM_Foo',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo --names_only',
     ['enumerate', 'CIM_Foo', '--names_only'],
     {'stdout': 'CIM_Foo',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo summary',
     ['enumerate', 'CIM_Foo', '-S'],
     {'stdout': '2 CIMClass(s) returned',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo summary',
     ['enumerate', 'CIM_Foo', '--summary'],
     {'stdout': '2 CIMClass(s) returned',
      'test': 'startswith'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo names and deepinheritance',
     ['enumerate', 'CIM_Foo', '-do'],
     {'stdout': ['CIM_Foo_sub', 'CIM_Foo_sub2', 'CIM_Foo_sub_sub'],
      'test': 'patterns'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand enumerate CIM_Foo include qualifiers',
     ['enumerate', 'CIM_Foo'],
     {'stdout': ['Key ( true )', '[Description (', 'class CIM_Foo'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    #
    # Test class get
    #
    ['class subcommand get  --help response',
     ['get', '--help'],
     {'stdout': 'Usage: pywbemcli class get [COMMAND-OPTIONS] CLASSNAME',
      'test': 'startswith'},
     None, OK],

    # subcommand get localonly option
    ['class subcommand get not localonly. Tests for property names',
     ['get', 'CIM_Foo_sub2'],
     {'stdout': ['string cimfoo_sub2;', 'InstanceID', 'IntegerProp', 'Fuzzy',
                 'Key ( true )', 'IN ( false )'],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand get localonly. Tests whole response',
     ['get', 'CIM_Foo_sub2', '-l'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '};', '', ],
      'test': 'patterns'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand get localonly. Tests whole response',
     ['get', 'CIM_Foo_sub2', '--localonly'],
     {'stdout': ['class CIM_Foo_sub2 : CIM_Foo {',
                 '',
                 '   string cimfoo_sub2;',
                 '',
                 '};', '', ],
      'test': 'patterns'},
     SIMPLE_MOCK_FILE, OK],

    # includequalifiers. Test the flag that excludes qualifiers
    ['class subcommand get without qualifiers, . Tests whole response',
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
    ['class subcommand get with propertylist, . Tests whole response',
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

    ['class subcommand get with empty propertylist, . Tests whole response',
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
    ['class subcommand get with propertylist and classorigin,',
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
    ['class subcommand find -h, ',
     ['find', '-h'],
     {'stdout': CLASS_FIND_HELP,
      'test': 'lines'},
     None, OK],

    ['class subcommand find  --help',
     ['find', '--help'],
     {'stdout': CLASS_FIND_HELP,
      'test': 'lines'},
     None, OK],

    # TODO Add detailed tests for find

    #
    # subcommand "class tree"
    #
    ['class subcommand tree --help response',
     ['tree', '--help'],
     {'stdout': CLASS_TREE_HELP,
      'test': 'lines'},
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
    ['class subcommand tree top down. Order uncertain so use "in" test ',
     ['tree'],
     {'stdout': ['root',
                 ' +-- CIM_Foo',
                 '     +-- CIM_Foo_sub2',
                 '     +-- CIM_Foo_sub',
                 '[| ]*  +-- CIM_Foo_sub_sub', ],  # account for ordering issue
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    # TODO The following test fails right now completely.
    ['class subcommand tree top down starting at defined class ',
     ['tree', 'CIM_Foo_sub'],
     {'stdout': ['CIM_Foo_sub',
                 ' +-- CIM_Foo_sub_sub', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand tree bottom up. Ordering guaranteed here',
     ['tree', '-s', 'CIM_Foo_sub_sub'],
     {'stdout': ['root',
                 ' +-- CIM_Foo',
                 '     +-- CIM_Foo_sub',
                 '         +-- CIM_Foo_sub_sub', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['class subcommand tree with invalid class',
     ['tree', '-s', 'CIM_Foo_subx'],
     {'stderr': ['CIMError:', 'Class CIM_Foo_subx not found in namespace',
                 'root/cimv2.'],
      'rc': 1,
      'test': 'regex'},

     SIMPLE_MOCK_FILE, OK],
    #
    # associators subcommand tests
    #
    ['class subcommand associators --help, . ',
     ['associators', '--help'],
     {'stdout': ['Usage: pywbemcli class associators [COMMAND-OPTIONS] '
                 'CLASSNAME',
                 'Get the associated classes for CLASSNAME.',
                 '-a, --assocclass <class name>   Filter by the associated '
                 'class name',
                 '-c, --resultclass <class name>  Filter by the result class '
                 'name provided.',
                 '-r, --role <role name>          Filter by the role name '
                 'provided.',
                 '-R, --resultrole <role name>    Filter by the role name '
                 'provided.',
                 '--no-qualifiers',
                 '-c, --includeclassorigin', ],
      'test': 'in'},
     None, OK],

    # TODO add detailed associators tests.  Need new mock file with
    # associations to do this
    #
    # references subcommand tests
    #
    ['class subcommand reference --help, . ',
     ['references', '--help'],
     {'stdout': ['Usage: pywbemcli class references [COMMAND-OPTIONS] '
                 'CLASSNAME',
                 'Get the reference classes for CLASSNAME.',
                 '-R, --resultclass <class name>  Filter by the classname '
                 'provided.',
                 '-r, --role <role name>          Filter by the role name '
                 'provided.',
                 '--no-qualifiers',
                 '-c, --includeclassorigin', ],
      'test': 'in'},
     None, OK],
    # TODO add detailed reference tests

    #
    # invokemethod subcommand tests
    #
    ['class subcommand invokemethod --help, . ',
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
     {'stdout': [],
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
     {'stderr': ["Error: CIMError: 6: Class CIM_Foox not found in namespace "
                 "root/cimv2."],
      'rc': 1,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify class subcommand invokemethod fails Invalid Method',
     ['invokemethod', 'CIM_Foo', 'Fuzzyx', '-p', 'TestInOutParameter=blah'],
     {'stderr': ["Error: CIMError: 17: Method Fuzzyx not in class CIM_Foo in "
                 "server"],
      'rc': 1,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],


    ['Verify class subcommand invokemethod fails Method not registered',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stderr': ["Error: CIMError: 17: Method Fuzzy in namespace root/cimv2 "
                 "not registered in repository"],
      'rc': 1,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE], OK],
]

# TODO subcommand class delete. NOTE: cannot really test this with current
# code since each test reloads repository
# namespace
# TODO: add test for  errors: class invalid, namespace invalid
# other tests.  Test localonly on top level


class TestSubcmdClass(CLITestsBase):
    """
    Test all of the class subcommand variations.
    """
    subcmd = 'class'

    @pytest.mark.parametrize(
        "desc, args, exp_response, mock, condition",
        MOCK_TEST_CASES)
    def test_class(self, desc, args, exp_response, mock, condition):
        """
        Common test method for those subcommands and options in the
        class subcmd that can be tested.  This includes:

          * Subcommands like help that do not require access to a server

          * Subcommands that can be tested with a single execution of a
            pywbemcli command.
        """
        env = None
        self.mock_subcmd_test(desc, self.subcmd, args, env, exp_response,
                              mock, condition)


class TestClassGeneral(object):  # pylint: disable=too-few-public-methods
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


class TestClassEnumerate(object):  # pylint: disable=too-few-public-methods
    """
    Test the options of the pywbemcli class enumerate' subcommand
    """
    # TODO remap this to use the same test_funct decorator as pywbem when
    # that code is committed.
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
