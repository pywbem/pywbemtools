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
Tests the commands in the server command group.
"""
from __future__ import absolute_import, print_function

import os
import pytest
from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_NAMES_ONLY_HELP_LINE, \
    CMD_OPTION_HELP_HELP_LINE, CMD_OPTION_SUMMARY_HELP_LINE, \
    CMD_OPTION_NAMESPACE_HELP_LINE, CMD_OPTION_PROPERTYLIST_HELP_LINE, \
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE, CMD_OPTION_VERIFY_HELP_LINE, \
    CMD_OPTION_INCLUDE_QUALIFIERS_LIST_HELP_LINE, \
    CMD_OPTION_INCLUDE_QUALIFIERS_GET_HELP_LINE, \
    CMD_OPTION_FILTER_QUERY_LINE, \
    CMD_OPTION_FILTER_QUERY_LANGUAGE_LINE, \
    CMD_OPTION_LOCAL_ONLY_INSTANCE_LIST_HELP_LINE, \
    CMD_OPTION_LOCAL_ONLY_INSTANCE_GET_HELP_LINE, \
    CMD_OPTION_MULTIPLE_NAMESPACE_HELP_LINE

TEST_DIR = os.path.dirname(__file__)

SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
ASSOC_MOCK_FILE = 'simple_assoc_mock_model.mof'
SIMPLE_MOCK_FILE_EXT = 'simple_mock_model_ext.mof'
ALLTYPES_MOCK_FILE = 'all_types.mof'
INVOKE_METHOD_MOCK_FILE = "simple_mock_invokemethod.py"
MOCK_PROMPT_0_FILE = "mock_prompt_0.py"
MOCK_PROMPT_PICK_RESPONSE_3_FILE = 'mock_prompt_pick_response_3.py'
MOCK_CONFIRM_Y_FILE = "mock_confirm_y.py"
MOCK_CONFIRM_N_FILE = "mock_confirm_n.py"
ALLTYPES_INVOKEMETHOD_MOCK_FILE = 'all_types_method_mock.py'


#
# The following list define the help for each command in terms of particular
# parts of lines that are to be tested.
# For each test, try to include:
# 1. The usage line and in particular the argument component
# 2. The single
# 2. The last line CMD_OPTION_HELP_HELP_LINE
# Defined in alphabetical order

INSTANCE_HELP_LINES = [
    'Usage: pywbemcli instance [COMMAND-OPTIONS] COMMAND [ARGS]...',
    'Command group for CIM instances.',
    CMD_OPTION_HELP_HELP_LINE,
    'associators   List the instances associated with an instance.',
    'count         Count the instances of each class with matching class '
    'name.',
    'create        Create an instance of a class in a namespace.',
    'delete        Delete an instance of a class.',
    'enumerate     List the instances of a class.',
    'get           Get an instance of a class.',
    'invokemethod  Invoke a method on an instance.',
    'modify        Modify properties of an instance.',
    'query         Execute a query on instances in a namespace.',
    'references    List the instances referencing an instance.',
]

INSTANCE_ASSOCIATORS_HELP_LINES = [
    'Usage: pywbemcli instance associators [COMMAND-OPTIONS] INSTANCENAME',
    'List the instances associated with an instance.',
    '--ac, --assoc-class CLASSNAME Filter the result set by association clas',
    '--rc, --result-class CLASSNAME Filter the result set by result class',
    '-r, --role PROPERTYNAME Filter the result set by source end role',
    '--rr, --result-role PROPERTYNAME Filter the result set by far end role',
    CMD_OPTION_INCLUDE_QUALIFIERS_LIST_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_PROPERTYLIST_HELP_LINE,
    CMD_OPTION_NAMES_ONLY_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_FILTER_QUERY_LINE,
    CMD_OPTION_FILTER_QUERY_LANGUAGE_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

INSTANCE_COUNT_HELP_LINES = [
    'Usage: pywbemcli instance count [COMMAND-OPTIONS] CLASSNAME-GLOB',
    'Count the instances of each class with matching class name.',
    '-s, --sort Sort by instance count.',
    CMD_OPTION_MULTIPLE_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

INSTANCE_CREATE_HELP_LINES = [
    'Usage: pywbemcli instance create [COMMAND-OPTIONS] CLASSNAME',
    'Create an instance of a class in a namespace.',
    '-p, --property PROPERTYNAME=VALUE Initial property value',
    CMD_OPTION_VERIFY_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

INSTANCE_DELETE_HELP_LINES = [
    'Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME',
    'Delete an instance of a class.',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

INSTANCE_ENUMERATE_HELP_LINES = [
    'Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME',
    'List the instances of a class.',
    CMD_OPTION_LOCAL_ONLY_INSTANCE_LIST_HELP_LINE,
    '--di, --deep-inheritance Include subclass properties in the returned',
    CMD_OPTION_INCLUDE_QUALIFIERS_LIST_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_PROPERTYLIST_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_NAMES_ONLY_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_FILTER_QUERY_LINE,
    CMD_OPTION_FILTER_QUERY_LANGUAGE_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

INSTANCE_GET_HELP_LINES = [
    'Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME',
    'Get an instance of a class.',
    CMD_OPTION_LOCAL_ONLY_INSTANCE_GET_HELP_LINE,
    CMD_OPTION_INCLUDE_QUALIFIERS_GET_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_PROPERTYLIST_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

INSTANCE_INVOKEMETHOD_HELP_LINES = [
    'Usage: pywbemcli instance invokemethod [COMMAND-OPTIONS] INSTANCENAME '
    'METHODNAME',
    'Invoke a method on an instance.',
    '-p, --parameter PARAMETERNAME=VALUE Specify a method input parameter',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

INSTANCE_MODIFY_HELP_LINES = [
    'Usage: pywbemcli instance modify [COMMAND-OPTIONS] INSTANCENAME',
    'Modify properties of an instance.',
    '-p, --property PROPERTYNAME=VALUE Property to be modified',
    '--pl, --propertylist PROPERTYLIST Reduce the properties to be modified',
    CMD_OPTION_VERIFY_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

INSTANCE_QUERY_HELP_LINES = [
    'Usage: pywbemcli instance query [COMMAND-OPTIONS] INSTANCENAME',
    'Execute a query on instances in a namespace.',
    '-l, --query-language QUERY-LANGUAGE The query language to be used',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

INSTANCE_REFERENCES_HELP_LINES = [
    'Usage: pywbemcli instance references [COMMAND-OPTIONS] INSTANCENAME',
    'List the instances referencing an instance.',
    '--rc, --result-class CLASSNAME Filter the result set by result class',
    '-r, --role PROPERTYNAME Filter the result set by source end role',
    CMD_OPTION_INCLUDE_QUALIFIERS_LIST_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_PROPERTYLIST_HELP_LINE,
    CMD_OPTION_NAMES_ONLY_HELP_LINE,
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_FILTER_QUERY_LINE,
    CMD_OPTION_FILTER_QUERY_LANGUAGE_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

ENUM_INSTANCE_RESP = """instance of CIM_Foo {
   InstanceID = "CIM_Foo1";
   IntegerProp = 1;
};

instance of CIM_Foo {
   InstanceID = "CIM_Foo2";
   IntegerProp = 2;
};

instance of CIM_Foo {
   InstanceID = "CIM_Foo3";
};

"""

GET_INSTANCE_ALL_TYPES = """instance of PyWBEM_AllTypes {
   InstanceId = "test_instance";
   scalBool = true;
   scalUint8 = 8;
   scalSint8 = -8;
   scalUint16 = 45;
   scalSint16 = -45;
   scalUint32 = 9999;
   scalSint32 = -9999;
   scalUint64 = 99999;
   scalSint64 = -99999;
   scalReal32 = 1.9;
   scalReal64 = 1.9;
   scalString = "This is a test string";
   scalDateTime = "19991224120000.000000+360";
   arrayBool = { true, false };
   arrayUint8 = { 0, 8, 125 };
   arraySint8 = { -8 };
   arrayUint16 = { 0, 45 };
   arraySint16 = { 0, 45 };
   arrayUint32 = { 0, 9999 };
   arraySint32 = { 0, -9999 };
   arrayUint64 = { 0, 99999 };
   arraySint64 = { -99999, 0, 99999 };
   arrayReal32 = { 0.0, 1.9 };
   arrayReal64 = { 0.0, 1.9 };
   arrayString = { "This is a test string", "Second String" };
   arrayDateTime = { "19991224120000.000000+360", "19991224120000.000000+360" };
};

"""

ENUM_INSTANCE_TABLE_RESP = """Instances: CIM_Foo
+--------------+---------------+
| InstanceID   | IntegerProp   |
+==============+===============+
| "CIM_Foo1"   | 1             |
+--------------+---------------+
| "CIM_Foo2"   | 2             |
+--------------+---------------+
| "CIM_Foo3"   |               |
+--------------+---------------+
"""


ENUM_INSTANCE_GET_TABLE_RESP = """Instances: CIM_Foo
InstanceID      IntegerProp
------------  -------------
"CIM_Foo1"                1
"""

REF_INSTS = """instance of TST_Lineage {
   InstanceID = "MikeGabi";
   parent = "/root/cimv2:TST_Person.name=\\\"Mike\\\"";
   child = "/root/cimv2:TST_Person.name=\\\"Gabi\\\"";
};

instance of TST_Lineage {
   InstanceID = "MikeSofi";
   parent = "/root/cimv2:TST_Person.name=\\\"Mike\\\"";
   child = "/root/cimv2:TST_Person.name=\\\"Sofi\\\"";
};

instance of TST_MemberOfFamilyCollection {
   family = "/root/cimv2:TST_FamilyCollection.name=\\\"Family2\\\"";
   member = "/root/cimv2:TST_Person.name=\\\"Mike\\\"";
};
"""

ASSOC_INSTS = """instance of TST_FamilyCollection {
   name = "Family2";
};

instance of TST_Person {
   name = "Gabi";
};

instance of TST_Person {
   name = "Sofi";
};

"""

# TODO: Add tests for output format xml, repr, txt

# pylint: enable=line-too-long

OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet

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

    #
    #   instance --help
    #
    ['Verify instance command --help response',
     '--help',
     {'stdout': INSTANCE_HELP_LINES,
      'test': 'insnows'},
     None, OK],

    ['Verify instance command -h response',
     '-h',
     {'stdout': INSTANCE_HELP_LINES,
      'test': 'insnows'},
     None, OK],

    #
    #  Instance Enumerate command good responses
    #
    ['Verify instance command enumerate --help response',
     ['enumerate', '--help'],
     {'stdout': INSTANCE_ENUMERATE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify instance command enumerate -h response',
     ['enumerate', '-h'],
     {'stdout': INSTANCE_ENUMERATE_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify instance command enumerate CIM_Foo',
     ['enumerate', 'CIM_Foo'],
     {'stdout': ENUM_INSTANCE_RESP,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate names CIM_Foo --no',
     ['enumerate', 'CIM_Foo', '--no'],
     {'stdout': ['', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate names CIM_Foo --no -s',
     ['enumerate', 'CIM_Foo', '--no', '--summary'],
     {'stdout': ['3 CIMInstanceName(s) returned'],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate names CIM_Foo --no --namespace',
     ['enumerate', 'CIM_Foo', '--no', '--namespace', 'root/cimv2'],
     {'stdout': ['', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate CIM_Foo --include-qualifiers',
     ['enumerate', 'CIM_Foo', '--include-qualifiers'],
     {'stdout': ENUM_INSTANCE_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate CIM_Foo include-qualifiers and '
     ' --use-pull no',
     {'args': ['enumerate', 'CIM_Foo', '--include-qualifiers'],
      'general': ['--use-pull', 'no']},
     {'stdout': ENUM_INSTANCE_RESP,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate CIM_Foo with --use-pull yes and '
     '--pull-max-cnt=2',
     {'args': ['enumerate', 'CIM_Foo', '--include-qualifiers'],
      'general': ['--use-pull', 'yes', '--pull-max-cnt', '2', '--log',
                  'all=stderr']},
     {'stderr': [r'PullInstancesWithPath\(pull_inst_result_tuple\(context='
                 'None, eos=True,',
                 r'PullInstancesWithPath\(MaxObjectCount=2',
                 r'OpenEnumerateInstances\(ClassName='],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate CIM_Foo with --use-pull yes and '
     '--pull-max-cnt=2 and --namesonly',
     {'args': ['enumerate', 'CIM_Foo', '--names-only'],
      'general': ['--use-pull', 'yes', '--pull-max-cnt', '2', '--log',
                  'all=stderr']},
     {'stderr': [r'PullInstancePaths\(pull_path_result_tuple\(context='
                 'None, eos=True,',
                 r'PullInstancePaths\(MaxObjectCount=2',
                 r'OpenEnumerateInstancePaths\(ClassName='],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate deep-inheritance CIM_Foo --di',
     ['enumerate', 'CIM_Foo', '--di'],
     {'stdout': ENUM_INSTANCE_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate deep-inheritance CIM_Foo '
     '--deep-inheritance',
     ['enumerate', 'CIM_Foo', '--deep-inheritance'],
     {'stdout': ENUM_INSTANCE_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command -o grid enumerate deep-inheritance CIM_Foo '
     '--di',
     {'args': ['enumerate', 'CIM_Foo', '--di'],
      'general': ['--output-format', 'grid']},
     {'stdout': ENUM_INSTANCE_TABLE_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command -o grid enumerate di CIM_Foo --di -o',
     {'args': ['enumerate', 'CIM_Foo', '--di', '--no'],
      'general': ['--output-format', 'grid']},
     {'stdout': """InstanceNames: CIM_Foo
+--------+-------------+---------+-----------------------+
| host   | namespace   | class   | keysbindings          |
+========+=============+=========+=======================+
|        | root/cimv2  | CIM_Foo | InstanceID="CIM_Foo1" |
+--------+-------------+---------+-----------------------+
|        | root/cimv2  | CIM_Foo | InstanceID="CIM_Foo2" |
+--------+-------------+---------+-----------------------+
|        | root/cimv2  | CIM_Foo | InstanceID="CIM_Foo3" |
+--------+-------------+---------+-----------------------+
""",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command -o grid enumerate di CIM_Foo --di --no',
     {'args': ['enumerate', 'CIM_Foo', '--di', '--no'],
      'general': ['--output-format', 'txt']},
     {'stdout': ['root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"',
                 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"'],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify instance command -o grid enumerate di CIM_Foo -d -o',
     {'args': ['enumerate', 'CIM_Foo'],
      'general': ['--output-format', 'txt']},
     {'stdout': ["CIMInstance(classname='CIM_Foo', "
                 "path=CIMInstanceName(classname='CIM_Foo', "
                 "keybindings=NocaseDict({'InstanceID': 'CIM_Foo1'}), "
                 "namespace='root/cimv2', host=None), ...)",
                 "CIMInstance(classname='CIM_Foo', "
                 "path=CIMInstanceName(classname='CIM_Foo', "
                 "keybindings=NocaseDict({'InstanceID': 'CIM_Foo2'}), "
                 "namespace='root/cimv2', host=None), ...)",
                 "CIMInstance(classname='CIM_Foo', "
                 "path=CIMInstanceName(classname='CIM_Foo', "
                 "keybindings=NocaseDict({'InstanceID': 'CIM_Foo3'}), "
                 "namespace='root/cimv2', host=None), ...)"],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command -o grid enumerate di alltypes, datetime',
     {'args': ['enumerate', 'Pywbem_Alltypes', '--di',
               '--propertylist', 'scalDateTime', '--pl', 'scalTimeDelta'],
      'general': ['--output-format', 'grid']},
     {'stdout': ["""Instances: PyWBEM_AllTypes
+-----------------------------+
| scalDateTime                |
+=============================+
| "19991224120000.000000+360" |
+-----------------------------+
"""],
      'test': 'linesnows'},
     ALLTYPES_MOCK_FILE, OK],

    # TODO: modify this to output log and test for info in return and log

    ['Verify instance command enumerate with query.',
     ['enumerate', 'CIM_Foo', '--filter-query', 'InstanceID = 3'],
     {'stdout': ENUM_INSTANCE_RESP,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate with query, traditional ops fails',
     {'args': ['enumerate', 'CIM_Foo', '--filter-query', 'InstanceID = 3'],
      'general': ['--use-pull', 'no']},
     {'stderr': ["ValueError",
                 "EnumerateInstances does not support FilterQuery"],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify command enumerate with CIM_Foo inst name table output',
     {'args': ['enumerate', 'CIM_Foo', '--names-only'],
      'general': ['--output-format', 'table']},
     {'stdout': """InstanceNames: CIM_Foo
+--------+-------------+---------+-----------------------+
| host   | namespace   | class   | keysbindings          |
|--------+-------------+---------+-----------------------|
|        | root/cimv2  | CIM_Foo | InstanceID="CIM_Foo1" |
|        | root/cimv2  | CIM_Foo | InstanceID="CIM_Foo2" |
|        | root/cimv2  | CIM_Foo | InstanceID="CIM_Foo3" |
+--------+-------------+---------+-----------------------+

""",
      'rc': 0,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify command enumerate with CIM_Foo summary table output',
     {'args': ['enumerate', 'CIM_Foo', '--summary'],
      'general': ['--output-format', 'table']},
     {'stdout': """Summary of CIMInstance returned
+---------+-------------+
|   Count | CIM Type    |
|---------+-------------|
|       3 | CIMInstance |
+---------+-------------+
""",
      'rc': 0,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    # TODO the following uses deep-inheritance because of issue in pywbem_mock
    ['Verify command enumerate with PyWBEM_AllTypes table with scalar '
     'properties returns instance with all property types',
     {'args': ['enumerate', 'PyWBEM_AllTypes', '--deep-inheritance',
               '--propertylist',
               'instanceid,scalbool,scaluint32,scalsint32'],
      'general': ['--output-format', 'grid']},
     {'stdout': """
Instances: PyWBEM_AllTypes
+-----------------+------------+--------------+--------------+
| InstanceId      | scalBool   |   scalUint32 |   scalSint32 |
+=================+============+==============+==============+
| "test_instance" | true       |         9999 |        -9999 |
+-----------------+------------+--------------+--------------+
""",
      'rc': 0,
      'test': 'linesnows'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify command enumerate with PyWBEM_AllTypes with array properties '
     'returns instance with all property types',
     {'args': ['enumerate', 'PyWBEM_AllTypes', '--deep-inheritance',
               '--propertylist',
               'instanceid,arraybool,arrayuint32,arraysint32'],
      'general': ['--output-format', 'grid']},
     {'stdout': """
Instances: PyWBEM_AllTypes
+-----------------+-------------+---------------+---------------+
| InstanceId      | arrayBool   | arrayUint32   | arraySint32   |
+=================+=============+===============+===============+
| "test_instance" | true, false | 0, 9999       | 0, -9999      |
+-----------------+-------------+---------------+---------------+

""",
      'rc': 0,
      'test': 'linesnows'},
     ALLTYPES_MOCK_FILE, OK],

    #
    # instance enumerate error returns
    #
    ['Verify instance command enumerate error, invalid classname fails',
     ['enumerate', 'CIM_Foox'],
     {'stderr': ["Error: CIMError: 6"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate error, no classname fails',
     ['enumerate'],
     {'stderr':
      ['Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME', ],
      'rc': 2,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate error, invalid namespace',
     ['enumerate', 'CIM_Foo', '--namespace', 'root/blah'],
     {'stderr':
      ["CIMError: 3 (CIM_ERR_INVALID_NAMESPACE): Namespace does not exist in "
       "mock repository: 'root/blah'", ],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate fails invalid query language',
     ['enumerate', 'CIM_Foo', '--filter-query-language', 'blah',
      '--filter-query', 'InstanceID = 3'],
     {'stderr': ['CIMError', '14', 'CIM_ERR_QUERY_LANGUAGE_NOT_SUPPORTED'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command enumerate fails using traditional op',
     {'args': ['enumerate', 'CIM_Foo', '--filter-query', 'InstanceID = 3'],
      'general': ['--use-pull', 'no']},
     {'stderr':
      ['ValueError', 'EnumerateInstances does not support FilterQuery'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance get command
    #

    ['Verify instance command get --help response',
     ['get', '--help'],
     {'stdout': INSTANCE_GET_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command get -h response',
     ['get', '-h'],
     {'stdout': INSTANCE_GET_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command get with instancename returns data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename, namespace returns data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--namespace', 'root/cimv2'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename local_only returns data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--lo'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename --local-only returns '
     ' data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--local-only'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename --include-qualifiers '
     'returns data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--include-qualifiers'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename --include-qualifiers '
     'and general --use-pull returns data',
     {'args': ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--iq'],
      'general': ['--use-pull', 'no']},
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename prop list -p returns '
     ' one property',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--pl', 'InstanceID'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename prop list '
     '--propertylist returns property',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--propertylist', 'InstanceID'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename prop list -p  '
     ' InstanceID,IntegerProp returns 2 properties',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--pl', 'InstanceID,IntegerProp'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename prop list -p '
     ' multiple instances of option returns 2 properties',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--pl', 'InstanceID',
      '--pl', 'IntegerProp'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename empty  prop list '
     'returns  empty instance',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--pl', '""'],
     {'stdout': ['instance of CIM_Foo {',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with instancename PyWBEM_AllTypes'
     ' returns instance with all property types',
     ['get', 'PyWBEM_AllTypes.InstanceID="test_instance"'],
     {'stdout': GET_INSTANCE_ALL_TYPES,
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command -o grid get CIM_Foo',
     {'args': ['get', 'CIM_Foo.InstanceID="CIM_Foo1"'],
      'general': ['-o', 'simple']},
     {'stdout': ENUM_INSTANCE_GET_TABLE_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    # Cannot insure order of the pick and we are using an integer to
    # pick so result is very general
    ['Verify instance command get with interactive wild card on classname',
     ['get', 'TST_Person.?'],
     {'stdout':
      ['Input integer between 0 and 7',
       'root/cimv2:TST_Person',
       'instance of TST_Person'],
      'rc': 0,
      'test': 'regex'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], OK],

    #
    #  get command errors
    #
    ['instance command get error. no classname',
     ['get'],
     {'stderr':
      ['Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME', ],
      'rc': 2,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['instance command get error. invalid namespace',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"',
      '--namespace', 'root/invalidnamespace'],
     {'stderr':
      ['CIMError: 3 (CIM_ERR_INVALID_NAMESPACE): Namespace does not exist'
       " in mock repository: 'root/invalidnamespace'", ],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command get with none existentinstancename',
     ['get', 'CIM_Foo.InstanceID="CIM_NOTEXIST"'],
     {'stderr': ["Error: CIMError: 6 (CIM_ERR_NOT_FOUND): Instance not found "
                 "in repository namespace 'root/cimv2'. Path=CIMInstanceName("
                 "classname='CIM_Foo', keybindings=NocaseDict({'InstanceID': "
                 "'CIM_NOTEXIST'}), namespace='root/cimv2', host=None)"],
      'rc': 1,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance create command
    #
    ['Verify instance command create --help response',
     ['create', '--help'],
     {'stdout': INSTANCE_CREATE_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command create -h response',
     ['create', '-h'],
     {'stdout': INSTANCE_CREATE_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command create, new instance of CIM_Foo one property',
     ['create', 'CIM_Foo', '-p', 'InstanceID=blah'],
     {'stdout': 'root/cimv2:CIM_Foo.InstanceID="blah"',
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command create, new instance of CIM_Foo one '
     'property and verify yes',
     ['create', 'CIM_Foo', '-p', 'InstanceID=blah', '--verify'],
     {'stdout': ['instance of CIM_Foo {',
                 'InstanceID = "blah";',
                 'root/cimv2:CIM_Foo.InstanceID="blah"',
                 'Execute CreateInstance'],
      'rc': 0,
      'test': 'in '},
     [SIMPLE_MOCK_FILE, MOCK_CONFIRM_Y_FILE], OK],

    ['Verify instance command create, new instance of CIM_Foo one '
     'property and verify no',
     ['create', 'CIM_Foo', '-p', 'InstanceID=blah', '--verify'],
     {'stdout': ['instance of CIM_Foo {',
                 'InstanceID = "blah";',
                 'root/cimv2:CIM_Foo.InstanceID="blah"',
                 'Execute CreateInstance'
                 'Request aborted'],
      'rc': 0,
      'test': 'in '},
     [SIMPLE_MOCK_FILE, MOCK_CONFIRM_N_FILE], OK],

    ['Verify instance command create, new instance of CIM_Foo, '
     'one property, explicit namespace definition',
     ['create', 'CIM_Foo', '-p', 'InstanceID=blah', '-n', 'root/cimv2'],
     {'stdout': "",
      'rc': 0,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    # TODO: This test fails sometimes due to unexpected order of instances.
    ['Verify create, get, delete work with stdin',
     {'stdin': ['instance create CIM_Foo -p InstanceID=blah',
                'instance get CIM_Foo.?',
                'instance delete CIM_Foo.?']},
     {'stdout': ['CIM_Foo', 'instance of CIM_Foo', 'IntegerProp= NULL'],
      'rc': 0,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, MOCK_PROMPT_PICK_RESPONSE_3_FILE], FAIL],

    ['Verify multiple creates verify with enum summary with stdin',
     {'stdin': ['instance create CIM_Foo -p InstanceID=blah1',
                'instance enumerate CIM_Foo -s',
                'instance create CIM_Foo -p InstanceID=blah2',
                'instance enumerate CIM_Foo -s']},
     {'stdout': ['4 CIMInstance', '5 CIMInstance'],
      'rc': 0,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE], OK],


    # TODO: For some reason the required quote marks on the instance IDs in
    # INSTANCENAME do not make it through stdin. What click presents is the
    # option as CIM_Foo.InstanceID=blah no matter how you define the
    # blah: quotes, quotes with escape.
    # TEST MARKED FAIL
    ['Verify create, get, delete works with stdin',
     {'stdin': ['instance create CIM_Foo -p InstanceID=blah',
                'instance get CIM_Foo.InstanceID=blah',
                'instance delete CIM_Foo.InstanceID=blah']},
     {'stdout': ['CIM_Foo', 'instance of CIM_Foo', 'IntegerProp= NULL'],
      'rc': 0,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, FAIL],

    # TODO This sequence locks up pywbemcli
    ['Verify create, get, delete works with stdin, scnd delete fails',
     {'stdin': ['instance create CIM_Foo -p InstanceID=blah',
                'instance get CIM_Foo.?',
                'instance delete CIM_Foo.?',
                'instance delete CIM_Foo.?']},
     {'stdout': ['CIM_Foo', 'instance of CIM_Foo', 'IntegerProp= NULL'
                 'CIM_ERR_NOT_FOUND'],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, MOCK_PROMPT_PICK_RESPONSE_3_FILE], FAIL],

    ['Verify instance command create, new instance of all_types '
     'with scalar types',
     ['create', 'PyWBEM_AllTypes',
      '-p', 'InstanceID=BunchOfValues',
      '-p', 'scalBool=true', '-p', 'scalUint8=1',
      '-p', 'scalUint16=9', '-p', 'scalSint16=-9',
      '-p', 'scalUint32=999', '-p', 'scalSint32=-999',
      '-p', 'scalSint64=-9999',
      '-p', 'scalUint64=9999',
      '-p', 'scalString="test\"embedded\"quote"',
      '-p', 'scalDateTime=19991224120000.000000+360'],
     {'stdout': 'root/cimv2:PyWBEM_AllTypes.InstanceId="BunchOfValues"',
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command create, new instance of all_types '
     "with array values",
     ['create', 'PyWBEM_AllTypes',
      '-p', 'InstanceID=blah',
      '-p', 'arrayBool=true,false',
      '-p', 'arrayUint8=1,2,3',
      '-p', 'arraySint8=-1,-2,-3',
      '-p', 'arrayUint16=9,19',
      '-p', 'arrayUint32=0,99,999', '-p', 'arraySint32=0,-999,-999',
      '-p', 'arrayUint64=0,999,9999', '-p', 'arraySint64=-9999,0,9999',
      '-p', 'scalString="abc", "def", "jhijk"'],
     {'stdout': 'root/cimv2:PyWBEM_AllTypes.InstanceId="blah"',
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command create, new instance Error in Property Type'
     " with array values",
     ['create', 'PyWBEM_AllTypes', '-p', 'InstanceID=blah',
      '-p', 'arrayBool=8,9',
      '-p', 'arrayUint8=1,2,3',
      '-p', 'arraySint8=-1,-2,-3',
      '-p', 'arrayUint16=9,19',
      '-p', 'arrayUint32=0,99,999', '-p', 'arraySint32=0,-999,-999',
      '-p', 'arrayUint64=0,999,9999', '-p', 'arraySint64=-9999,0,9999',
      '-p', 'scalString="abc", "def", "jhijk"'],
     {'stderr': "Error: Type mismatch property 'arrayBool' between expected "
                "type='boolean', array=True and input value='8,9'. "
                'Exception: Invalid boolean value: "8"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command create, new instance already exists',
     ['create', 'PyWBEM_AllTypes', '-p', 'InstanceID=test_instance'],
     {'stderr': ['Error: CIMClass: "PyWBEM_AllTypes" does not exist in ',
                 'namespace "root/cimv2" in WEB server: FakedWBEMConnection'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command create, new instance invalid ns',
     ['create', 'PyWBEM_AllTypes', '-p', 'InstanceID=test_instance', '-n',
      'blah'],
     {'stderr': ["Error: Exception 3", "CIM_ERR_INVALID_NAMESPACE"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify instance command create, new instance invalid class',
     ['create', 'CIM_blah', '-p', 'InstanceID=test_instance'],
     {'stderr': ["Error:", "CIMClass"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],
    # NOTE: Since the instance creation logic is the same for modify and
    # create instance. The error tests in modify also test the error logic.
    # We have not repeated a bunch of those in for the CreateInstance

    #
    #  instance modify command
    #
    ['Verify instance command modify --help response',
     ['modify', '--help'],
     {'stdout': INSTANCE_MODIFY_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command modify -h response',
     ['modify', '-h'],
     {'stdout': INSTANCE_MODIFY_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command modify, single good change',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'scalBool=False'],
     {'stdout': "",
      'rc': 0,
      'test': 'linesnows'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, single good change with verify yes',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'scalBool=False', '--verify'],
     {'stdout': ['instance of PyWBEM_AllTypes {',
                 'scalBool = false;',
                 '};',
                 'Execute ModifyInstance'],
      'rc': 0,
      'test': 'regex'},
     [ALLTYPES_MOCK_FILE, MOCK_CONFIRM_Y_FILE], OK],

    ['Verify instance command modify, single good change with verify no',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'scalBool=False', '--verify'],
     {'stdout': ['instance of PyWBEM_AllTypes {',
                 'scalBool = false;',
                 'Execute ModifyInstance',
                 'Request aborted'],
      'rc': 0,
      'test': 'regex'},
     [ALLTYPES_MOCK_FILE, MOCK_CONFIRM_N_FILE], OK],


    ['Verify instance command modify, single good change, explicit ns',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"', '-n',
      'root/cimv2', '-p', 'scalBool=False'],
     {'stdout': "",
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, single good change, explicit ns',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"', '--namespace',
      'root/cimv2', '--property', 'scalBool=False'],
     {'stdout': "",
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, multiple good change',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'scalBool=False',
      '-p', 'arrayBool=true,false,true',
      '-p', 'arrayUint32=0,99,999, 3', '-p', 'arraySint32=0,-999,-999,9',
      '-p', 'arrayUint64=0,999,9999,3000', '-p', 'arraySint64=-9999,0,9999,4',
      '-p', 'scalString="abc", "def", "jhijk"'],
     {'stdout': "",
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    #
    # Instance modify errors
    #
    ['Verify instance command modify, invalid class',
     ['modify', 'PyWBEM_AllTypesxxx.InstanceID="test_instance"',
      '-p', 'scalBool=9'],
     {'stderr': ["CIMClass:", "PyWBEM_AllTypesxxx",
                 "does not exist in WEB server",
                 "FakedUrl"],
      'rc': 1,
      'test': 'regex'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, single property, Type Error bool',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'scalBool=9'],
     {'stderr': "Error: Type mismatch property 'scalBool' between expected "
                "type='boolean', array=False and input value='9'. "
                'Exception: Invalid boolean value: "9"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, single property, Fail modifies key',
     ['modify', 'PyWBEM_AllTypes.InstanceId="test_instance"',
      '-p', 'InstanceId=9'],
     {'stderr': ['Server Error modifying instance',
                 'Exception: CIMError:',
                 '4',
                 'CIM_ERR_INVALID_PARAMETER',
                 "'InstanceId'"],
      'rc': 1,
      'test': 'innows'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, single property, Type Error uint32. '
     'Uses regex because Exception msg different between python 2 and 3',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'scalUint32=Fred'],
     {'stderr': ["Error: Type mismatch property 'scalUint32' between expected ",
                 "type='uint32', array=False and input value='Fred'. ",
                 "Exception: invalid literal for", "with base 10: 'Fred'"],
      'rc': 1,
      'test': 'regex'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, single Property arrayness error',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'scalBool=False,True'],
     {'stderr': "Error: Type mismatch property 'scalBool' between expected "
                "type='boolean', array=False and input value='False,True'. "
                'Exception: Invalid boolean value: "False,True"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, Error value types mismatch with array',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'arrayBool=9,8'],
     {'stderr': "Error: Type mismatch property 'arrayBool' between expected "
                "type='boolean', array=True and input value='9,8'. "
                'Exception: Invalid boolean value: "9"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, Error different value types',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'arrayBool=true,8'],
     {'stderr': "Error: Type mismatch property 'arrayBool' between expected "
                "type='boolean', array=True and input value='true,8'. "
                'Exception: Invalid boolean value: "8"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, Error integer out of range',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'arrayUint32=99999999999999999999999'],
     {'stderr': "Error: Type mismatch property 'arrayUint32' between expected "
                "type='uint32', array=True and input "
                "value='99999999999999999999999'. "
                "Exception: Integer value 99999999999999999999999 is out of "
                "range for CIM datatype uint32",
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance command modify, Error property not in class',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-p', 'blah=9'],
     {'stderr': 'Error: Property name "blah" not in class "PyWBEM_AllTypes".',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    # TODO additional modify error tests required

    #
    #  instance delete command
    #
    ['Verify instance command delete --help response',
     ['delete', '--help'],
     {'stdout': INSTANCE_DELETE_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command delete -h response',
     ['delete', '-h'],
     {'stdout': INSTANCE_DELETE_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command delete, valid delete',
     ['delete', 'CIM_Foo.InstanceID="CIM_Foo1"'],
     {'stdout': '',
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command delete, valid delete, explicit ns',
     ['delete', 'CIM_Foo.InstanceID="CIM_Foo1"', '-n', 'root/cimv2'],
     {'stdout': '',
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command delete, valid delete, explicit ns',
     ['delete', 'CIM_Foo.InstanceID="CIM_Foo1"', '--namespace', 'root/cimv2'],
     {'stdout': '',
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command delete with interactive wild card on classname',
     ['delete', 'TST_Person.?'],
     {'stdout':
      ['root/cimv2:TST_Person.name="Mike"'],
      'rc': 0,
      'test': 'in'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], OK],

    #
    # Delete command error tests
    #
    ['Verify instance command delete, missing instance name',
     ['delete'],
     {'stderr':
      ['Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME', ],
      'rc': 2,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command delete, instance name invalid',
     ['delete', "blah"],
     {'stderr':
      ['Invalid wbem uri', ],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command delete, instance name not in repo',
     ['delete', 'CIM_Foo.InstanceID="xxxxx"', '--namespace', 'root/cimv2'],
     {'stderr':
      ["CIMError", "6", "CIM_ERR_NOT_FOUND"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command delete, namespace not in repo',
     ['delete', 'CIM_Foo.InstanceID=1', '--namespace', 'Argh'],
     {'stderr':
      ["CIMError", "3", "CIM_ERR_INVALID_NAMESPACE"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance references command
    #
    ['Verify instance command references --help response',
     ['references', '--help'],
     {'stdout': INSTANCE_REFERENCES_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command references -h response',
     ['references', '-h'],
     {'stdout': INSTANCE_REFERENCES_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command references, returns instances',
     ['references', 'TST_Person.name="Mike"'],
     {'stdout': REF_INSTS,
      'rc': 0,
      'test': 'lineswons'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references, returns instances, explicit ns',
     ['references', 'TST_Person.name="Mike"', '-n', 'root/cimv2'],
     {'stdout': REF_INSTS,
      'rc': 0,
      'test': 'lineswons'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references --no, returns paths',
     ['references', 'TST_Person.name="Mike"', '--no'],
     {'stdout': ['"root/cimv2:TST_FamilyCollection.name=\\"Family2\\"",member',
                 '=\"root/cimv2:TST_Person.name=\\"Mike\\""',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"',
                 '//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection.family'],
      'rc': 0,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references --no, returns paths with result '
     'class valid returns paths',
     ['references', 'TST_Person.name="Mike"', '--no',
      '--result-class', 'TST_Lineage'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"', ],
      'rc': 0,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references CIM_Foo with --use-pull yes '
     'and --pull-max-cnt=1',
     {'args': ['references', 'TST_Person.name="Mike"'],
      'general': ['--use-pull', 'yes', '--pull-max-cnt', '1', '--log',
                  'all=stderr']},
     {'stderr': [r'PullInstancesWithPath\(MaxObjectCount=1',
                 r'OpenReferenceInstances\(pull_inst_result_tuple\('
                 'context=',
                 r'TST_MemberOfFamilyCollection',
                 r'TST_Lineage'],
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command reference paths CIM_Foo with --use-pull '
     'yes and --pull-max-cnt=1 and --names-only',
     {'args': ['references', 'TST_Person.name="Mike"', '--names-only'],
      'general': ['--use-pull', 'yes', '--pull-max-cnt', '1', '--log',
                  'all=stderr']},
     {'stderr': [r'PullInstancePaths\(MaxObjectCount=1',
                 r'OpenReferenceInstancePaths\(pull_path_result_tuple\('
                 'context=',
                 r'TST_MemberOfFamilyCollection',
                 r'TST_Lineage'],
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references -o, returns paths with result '
     'class valid returns paths sorted',
     ['references', 'TST_Person.name="Mike"', '--no',
      '--result-class', 'TST_Lineage'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"', ],
      'rc': 0,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references -o, returns paths with result '
     'class short form valid returns paths',
     ['references', 'TST_Person.name="Mike"', '--no',
      '--rc', 'TST_Lineage'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"', ],
      'rc': 0,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references --no, returns paths with result '
     'class short form valid returns paths',
     ['references', 'TST_Person.name="Mike"', '--no', '--summary',
      '--rc', 'TST_Lineage'],
     {'stdout': ['2 CIMInstanceName(s) returned'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],


    ['Verify instance command references --no, returns paths with result '
     'class short form valid returns paths',
     {'args': ['references', 'TST_Person.name="Mike"', '--no', '--summary',
               '--rc', 'TST_Lineage'],
      'general': ['--output-format', 'table']},
     {'stdout': ["""Summary of CIMInstanceName returned
+---------+-----------------+
|   Count | CIM Type        |
|---------+-----------------|
|       2 | CIMInstanceName |
+---------+-----------------+
"""],
      'rc': 0,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references -s, returns paths with result '
     'class short form valid returns paths',
     ['references', 'TST_Person.name="Mike"', '-s',
      '--rc', 'TST_Lineage'],
     {'stdout': ['2 CIMInstance(s) returned'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references --include-qualifiers',
     ['references', 'TST_Person.name="Mike"', '--include-qualifiers'],
     {'stdout': REF_INSTS,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references include-qualifiers and '
     ' --use-pull no',
     {'args': ['references', 'TST_Person.name="Mike"', '--include-qualifiers'],
      'general': ['--use-pull', 'no']},
     {'stdout': REF_INSTS,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],

    # Behavior changed pywbem 0.15.0 to exception rtn
    ['Verify instance command references -o, returns paths with result '
     'class not a real ref returns no paths',
     ['references', 'TST_Person.name="Mike"', '--no',
      '--result-class', 'TST_Lineagex'],
     {'stderr': [''],
      'rc': 1,
      'test': 'linnows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references, no instance name',
     ['references'],
     {'stderr': ['Usage: pywbemcli instance references [COMMAND-OPTIONS] '
                 'INSTANCENAME', ],
      'rc': 2,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    # Behavior changed pywbem 0.15.0 to exception rtn
    ['Verify instance command references, invalid instance name',
     ['references', 'TST_Blah.blah="abc"'],
     {'stderr': "",
      'rc': 1,
      'test': 'innows'},
     ASSOC_MOCK_FILE, OK],

    # Because the order of pick is not guaranteed, we test minimum data
    # Issue #458 TODO: Marked fail because for some rason with pywbem 0.15.0.
    # this test fails without building instance on some python version.
    ['Verify instance command references with selection suffix keys wild card ',
     ['references', 'TST_Person.?'],
     {'stdout':
      ['instance of TST', '{', '}'],
      'rc': 0,
      'test': 'innows'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], FAIL],

    ['Verify instance command references with query.',
     ['references', 'TST_Person.name="Mike"', '--filter-query',
      'InstanceID = 3'],
     {'stdout': REF_INSTS,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command references with query, traditional ops fails',
     {'args': ['references', 'TST_Person.name="Mike"', '--filter-query',
               'InstanceID = 3'],
      'general': ['--use-pull', 'no']},
     {'stderr': ["ValueError:",
                 "References does not support FilterQuery"],
      'rc': 1,
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    # TODO add more invalid references tests

    #
    #  instance associators command
    #
    ['Verify instance command associators --help response',
     ['associators', '--help'],
     {'stdout': INSTANCE_ASSOCIATORS_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command associators -h response',
     ['associators', '-h'],
     {'stdout': INSTANCE_ASSOCIATORS_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command associators, returns instances',
     ['associators', 'TST_Person.name="Mike"'],
     {'stdout': ASSOC_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command associators, --include-qualifiers',
     ['associators', 'TST_Person.name="Mike"', '--include-qualifiers'],
     {'stdout': ASSOC_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command associators, --include-qualifiers wo pull',
     {'general': ['--use-pull', 'no'],
      'args': ['associators', 'TST_Person.name="Mike"',
               '--include-qualifiers']},
     {'stdout': ASSOC_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command associators -o, returns data',
     ['associators', 'TST_Person.name="Mike"', '--no'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_FamilyCollection.name="Family2"'
                 '//FakedUrl/root/cimv2:TST_Person.name="Gabi"',
                 '//FakedUrl/root/cimv2:TST_Person.name="Sofi"'],
      'rc': 0,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command associators CIM_Foo with --use-pull yes '
     'and --pull-max-cnt=1',
     {'args': ['associators', 'TST_Person.name="Mike"'],
      'general': ['--use-pull', 'yes', '--pull-max-cnt', '1', '--log',
                  'all=stderr']},
     {'stderr': [r'PullInstancesWithPath\(MaxObjectCount=1',
                 r'OpenAssociatorInstances\(pull_inst_result_tuple\('
                 'context=',
                 r'TST_Person'],
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command associator paths CIM_Foo with --use-pull '
     'yes and --pull-max-cnt=1 and --names-only',
     {'args': ['associators', 'TST_Person.name="Mike"', '--names-only'],
      'general': ['--use-pull', 'yes', '--pull-max-cnt', '1', '--log',
                  'all=stderr']},
     {'stderr': [r'PullInstancePaths\(MaxObjectCount=1',
                 r'OpenAssociatorInstancePaths\(pull_path_result_tuple\('
                 'context=',
                 r'TST_Person'],
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    # Invalid associators tests

    ['Verify instance command associators, no instance name',
     ['associators'],
     {'stderr': ['Usage: pywbemcli instance associators [COMMAND-OPTIONS] '
                 'INSTANCENAME', ],
      'rc': 2,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    # Starting with pywbem 0.15.0, it returns a CIM error.
    ['Verify instance command associators, invalid instance name',
     ['associators', 'TST_Blah.blah="abc"'],
     {'stderr': ['CIMError:',
                 '4',
                 'CIM_ERR_INVALID_PARAMETER',
                 "Class 'TST_Blah' not found in namespace 'root/cimv2'"],
      'rc': 1,
      'test': 'innows'},
     ASSOC_MOCK_FILE, OK],

    # Issue #457; Starting with pywbem 0.15.0, this fails on some python
    # versions
    ['Verify instance command associators with interactive wild card on '
     'classname',
     ['associators', 'TST_Person.?'],
     {'stdout':
      ['root/cimv2:TST_Person.name="Mike"',
       'instance of TST_Person {',
       'instance of TST_FamilyCollection {'],
      'rc': 0,
      'test': 'innows'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], FAIL],

    ['Verify instance command associators with query.',
     ['associators', 'TST_Person.name="Mike"', '--filter-query',
      'InstanceID = 3'],
     {'stdout': ASSOC_INSTS,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command associators with query, traditional ops',
     {'args': ['associators', 'TST_Person.name="Mike"', '--filter-query',
               'InstanceID = 3'],
      'general': ['--use-pull', 'no']},
     {'stderr': ["ValueError:",
                 "Associators does not support FilterQuery"],
      'rc': 1,
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    # TODO add more associators error tests

    #
    #  instance count command
    #
    ['Verify instance command count --help response',
     ['count', '--help'],
     {'stdout': INSTANCE_COUNT_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    ['Verify instance command count -h response',
     ['count', '-h'],
     {'stdout': INSTANCE_COUNT_HELP_LINES,
      'rc': 0,
      'test': 'innows'},
     None, OK],

    # The following use interop ns to avoid warning about namespaces.
    ['Verify instance command count CIM_* simple model, Rtn tbl of instances',
     {'args': ['count', 'CIM_*'],
      'general': ['--default-namespace', 'interop']},
     {'stdout': """Count of instances per class
+-------------+---------+---------+
| Namespace   | Class   |   count |
|-------------+---------+---------|
| interop     | CIM_Foo |       3 |
+-------------+---------+---------+
""",
      'rc': 0,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance command count CIM_*  sorted, Rtn table of inst counts',
     {'args': ['count', 'CIM_*', '--sort'],
      'general': ['--default-namespace', 'interop']},
     {'stdout': """Count of instances per class
+-------------+-----------------+---------+
| Namespace   | Class           |   count |
|-------------+-----------------+---------|
| interop     | CIM_Foo_sub_sub |       3 |
| interop     | CIM_Foo_sub     |       4 |
| interop     | CIM_Foo         |       5 |
+-------------+-----------------+---------+
""",
      'rc': 0,
      'test': 'innows'},
     SIMPLE_MOCK_FILE_EXT, OK],

    ['Verify instance command count CIM_*. Rtn table of inst counts',
     {'args': ['count', 'CIM_*'],
      'general': ['--default-namespace', 'interop']},
     {'stdout': """Count of instances per class
+-------------+-----------------+---------+
| Namespace   | Class           |   count |
|-------------+-----------------+---------|
| interop     | CIM_Foo         |       5 |
| interop     | CIM_Foo_sub     |       4 |
| interop     | CIM_Foo_sub_sub |       3 |
+-------------+-----------------+---------+
""",
      'rc': 0,
      'test': 'innows'},
     SIMPLE_MOCK_FILE_EXT, OK],

    ['Verify instance command count mock assoc. Return table of instances',
     {'args': ['count', '*'],
      'general': ['--default-namespace', 'interop', '--output-format',
                  'plain']},
     {'stdout': [
         'Count of instances per class',
         'Namespace    Class                           count',
         'interop      TST_FamilyCollection                2',
         'interop      TST_Lineage                         3',
         'interop      TST_MemberOfFamilyCollection        3',
         'interop      TST_Person                          4',
         'interop      TST_Personsub                       4', ],
      'rc': 0,
      'test': 'innows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance command count *Person* . Return table of instances',
     {'args': ['count', '*Person*'],
      'general': ['--default-namespace', 'interop']},
     {'stdout': """Count of instances per class
Namespace    Class            count
interop      TST_Person           4
interop      TST_Personsub        4
""",
      'rc': 0,
      'test': 'lonnows'},
     ASSOC_MOCK_FILE, OK],

    #
    #  instance invokemethod tests
    #

    ['class command invokemethod --help',
     ['invokemethod', '--help'],
     {'stdout': INSTANCE_INVOKEMETHOD_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['class command invokemethod -h',
     ['invokemethod', '-h'],
     {'stdout': INSTANCE_INVOKEMETHOD_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify instance command invokemethod, returnvalue = 0',
     ['invokemethod', ':CIM_Foo.InstanceID="CIM_Foo1"', 'Fuzzy'],
     {'stdout': ['ReturnValue=0'],
      'rc': 0,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify instance command invokemethod with multiple scalar params',
     ['invokemethod', ':CIM_Foo.InstanceID="CIM_Foo1"', 'Fuzzy',
      '-p', 'TestInOutParameter="blah"',
      '-p', 'TestRef=CIM_Foo.InstanceID="CIM_Foo1"'],
     {'stdout': ['ReturnValue=0',
                 'TestInOutParameter=', 'blah',
                 'TestRef=', 'CIM_Foo.InstanceID=', 'CIM_Foo1'],
      'rc': 0,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],


    ['Verify instance command invokemethod with all_types method',
     ['invokemethod', 'Pywbem_alltypes.InstanceID="test_instance"',
      'AllTypesMethod',
      '-p', 'scalBool=true',
      '-p', 'arrBool=false,true',
      '-p', 'scalUint32=9',
      '-p', 'arrUint32=9,3,255',
      '-p', 'scalString=abcdefjh',
      '-p', 'arrString="abc","def"',
      '-p', 'scalRef=PyWBEM_AllTypes.InstanceID="1"'],
     {'stdout': ['ReturnValue=0',
                 'scalBool=true',
                 'arrBool=false, true',
                 'scalUint32=9',
                 'arrUint32=9, 3, 255',
                 'scalString="abcdefjh"',
                 'arrString=', 'abc', 'def',
                 'scalRef=', 'PyWBEM_AllTypes.InstanceID='],
      'rc': 0,
      'test': 'innows'},
     [ALLTYPES_MOCK_FILE, ALLTYPES_INVOKEMETHOD_MOCK_FILE], OK],

    ['Verify instance command invokemethod fails Invalid Class',
     ['invokemethod', ':CIM_Foox.InstanceID="CIM_Foo1"', 'Fuzzy', '-p',
      'TestInOutParameter="blah"'],
     {'stderr': ["Error: CIMError: 6"],
      'rc': 1,
      'test': 'regex'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify instance command invokemethod fails Method not registered',
     ['invokemethod', ':CIM_Foo.InstanceID="CIM_Foo1"', 'Fuzzy', '-p',
      'TestInOutParameter=blah'],
     {'stderr': ["Error: CIMError: 17"],
      'rc': 1,
      'test': 'in'},
     [SIMPLE_MOCK_FILE], OK],

    # TODO expand the number of invokemethod tests to include all options
    # in classnametests
    # TODO: Create new method that has all param types and options


    #
    #  instance query command. We have not implemented this command
    #
    ['Verify instance command query --help response',
     ['query', '--help'],
     {'stdout': INSTANCE_QUERY_HELP_LINES,
      'rc': 0,
      'test': 'linnows'},
     None, OK],

    ['Verify instance command query -h response',
     ['query', '-h'],
     {'stdout': INSTANCE_QUERY_HELP_LINES,
      'rc': 0,
      'test': 'linnows'},
     None, OK],

    ['Verify instance command query execution. Returns error becasue '
     'mock does not support query',
     ['query', 'Select blah from blah'],
     {'stderr': ['Error: CIMError: 14 (CIM_ERR_QUERY_LANGUAGE_NOT_SUPPORTED): ',
                 "FilterQueryLanguage 'DMTF:CQL' not supported"],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE], OK],
]


class TestSubcmd(CLITestsBase):
    """
    Test all of the class command variations.
    """
    command_group = 'instance'
    # mock_mof_file = 'simple_mock_model.mof'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition", TEST_CASES)
    def test_execute_pywbemcli(self, desc, inputs, exp_response, mock,
                               condition):
        """
        Execute pybemcli with the defined input and test output.
        """
        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition, verbose=False)
