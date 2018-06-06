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
Tests the class subcommand
"""
import os
import pytest
from .cli_test_extensions import CLITestsBase

TEST_DIR = os.path.dirname(__file__)

SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
ASSOC_MOCK_FILE = 'simple_assoc_mock_model.mof'

INST_HELP = """Usage: pywbemcli instance [COMMAND-OPTIONS] COMMAND [ARGS]...

  Command group to manage CIM instances.

  This incudes functions to get, enumerate, create, modify, and delete
  instances in a namspace and additional functions to get more general
  information on instances (ex. counts) within the namespace

  In addition to the command-specific options shown in this help text, the
  general options (see 'pywbemcli --help') can also be specified before the
  command. These are NOT retained after the command is executed.

Options:
  -h, --help  Show this message and exit.

Commands:
  associators   Get associated instances or names.
  count         Get instance count for classes.
  create        Create an instance of classname.
  delete        Delete a single CIM instance.
  enumerate     Enumerate instances or names of CLASSNAME.
  get           Get a single CIMInstance.
  invokemethod  Invoke a CIM method.
  query         Execute an execquery request.
  references    Get the reference instances or names.
"""

INST_ENUM_HELP = """Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME

  Enumerate instances or names of CLASSNAME.

  Enumerate instances or instance names from the WBEMServer starting either
  at the top  of the hierarchy (if no CLASSNAME provided) or from the
  CLASSNAME argument if provided.

  Displays the returned instances or names

Options:
  -l, --localonly                 Show only local properties of the class.
  -d, --deepinheritance           Return properties in subclasses of defined
                                  target.  If not specified only properties in
                                  target class are returned
  -q, --includequalifiers         Include qualifiers in the result.
  -c, --includeclassorigin        Include ClassOrigin in the result.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  not included a Null property list is defined
                                  and the server returns all properties. If
                                  defined as empty string the server returns
                                  no properties. ex: -p propertyname1 -p
                                  propertyname2 or -p
                                  propertyname1,propertyname2
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -o, --names_only                Show only local properties of the class.
  -s, --sort                      Sort into alphabetical order by classname.
  -S, --summary                   Return only summary of objects (count).
  -h, --help                      Show this message and exit.
"""

ENUM_INST_RESP = """instance of CIM_Foo {
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

INST_CREATE_HELP = """Usage: pywbemcli instance create [COMMAND-OPTIONS] CLASSNAME

  Create an instance of classname.

  Creates an instance of the class `CLASSNAME` with the properties defined
  in the property option.

  The propertylist option limits the created instance to the properties in
  the list. This parameter is NOT passed to the server

Options:
  -P, --property property         Optional property definitions of form
                                  name=value.Multiple definitions allowed, one
                                  for each property
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  not included a Null property list is defined
                                  and the server returns all properties. If
                                  defined as empty string the server returns
                                  no properties. ex: -p propertyname1 -p
                                  propertyname2 or -p
                                  propertyname1,propertyname2
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -h, --help                      Show this message and exit.
"""

INST_DELETE_HELP = """Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME

  Delete a single CIM instance.

  Delete the instanced defined by INSTANCENAME from the WBEM server. This
  may be executed interactively by providing only a class name and the
  interactive option.

Options:
  -i, --interactive       If set, INSTANCENAME argument must be a class and
                          user is provided with a list of instances of the
                          class from which the instance to delete is selected.
  -n, --namespace <name>  Namespace to use for this operation. If defined that
                          namespace overrides the general options namespace
  -h, --help              Show this message and exit.
"""

INST_COUNT_HELP = """Usage: pywbemcli instance count [COMMAND-OPTIONS] CLASSNAME-REGEX

  Get instance count for classes.

  Displays the count of instances for the classes defined by the `CLASSNAME-
  REGEX` argument in one or more namespaces.

  The size of the response may be limited by CLASSNAME-REGEX argument which
  defines a regular expression based on the desired class names so that only
  classes that match the regex are counted. The CLASSNAME-regex argument is
  optional.

  The CLASSNAME-regex argument may be either a complete classname or a
  regular expression that can be matched to one or more classnames. To limit
  the filter to a single classname, terminate the classname with $.

  The CLASSNAME-REGEX regular expression is anchored to the beginning of the
  classname and is case insensitive. Thus `pywbem_` returns all classes that
  begin with `PyWBEM_`, `pywbem_`, etc.

  This operation can take a long time to execute.

Options:
  -s, --sort              Sort by instance count. Otherwise sorted by
                          classname
  -n, --namespace <name>  Namespace to use for this operation. If defined that
                          namespace overrides the general options namespace
  -h, --help              Show this message and exit.
"""

INST_REFERENCES_HELP = """Usage: pywbemcli instance references [COMMAND-OPTIONS] INSTANCENAME

  Get the reference instances or names.

  Gets the reference instances or instance names(--names-only option) for a
  target instance name in the target WBEM server.

  For the INSTANCENAME argument provided return instances or instance names
  filtered by the --role and --resultclass options.

  This may be executed interactively by providing only a class name and the
  interactive option(-i). Pywbemcli presents a list of instances names in
  the class from which one can be chosen as the target.

Options:
  -R, --resultclass <class name>  Filter by the result class name provided.
  -r, --role <role name>          Filter by the role name provided.
  -q, --includequalifiers         Include qualifiers in the result.
  -c, --includeclassorigin        Include classorigin in the result.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  not included a Null property list is defined
                                  and the server returns all properties. If
                                  defined as empty string the server returns
                                  no properties. ex: -p propertyname1 -p
                                  propertyname2 or -p
                                  propertyname1,propertyname2
  -o, --names_only                Show only local properties of the class.
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -s, --sort                      Sort into alphabetical order by classname.
  -i, --interactive               If set, INSTANCENAME argument must be a
                                  class and  user is provided with a list of
                                  instances of the  class from which the
                                  instance to delete is selected.
  -S, --summary                   Return only summary of objects (count).
  -h, --help                      Show this message and exit.
"""

INST_ASSOCIATORS_HELP = """Usage: pywbemcli instance associators [COMMAND-OPTIONS] INSTANCENAME

  Get associated instances or names.

  Returns the associated instances or names (--names-only option) for the
  INSTANCENAME argument filtered by the --assocclass, --resultclass, --role
  and --resultrole options.

  This may be executed interactively by providing only a classname and the
  interactive option. Pywbemcli presents a list of instances in the class
  from which one can be chosen as the target.

Options:
  -a, --assocclass <class name>   Filter by the associated instancename
                                  provided.
  -c, --resultclass <class name>  Filter by the result class name provided.
  -R, --role <role name>          Filter by the role name provided.
  -R, --resultrole <class name>   Filter by the result role name provided.
  -q, --includequalifiers         Include qualifiers in the result.
  -c, --includeclassorigin        Include classorigin in the result.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  not included a Null property list is defined
                                  and the server returns all properties. If
                                  defined as empty string the server returns
                                  no properties. ex: -p propertyname1 -p
                                  propertyname2 or -p
                                  propertyname1,propertyname2
  -o, --names_only                Show only local properties of the class.
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -s, --sort                      Sort into alphabetical order by classname.
  -i, --interactive               If set, INSTANCENAME argument must be a
                                  class and  user is provided with a list of
                                  instances of the  class from which the
                                  instance to delete is selected.
  -S, --summary                   Return only summary of objects (count).
  -h, --help                      Show this message and exit.
"""

REF_INSTS = """instance of TST_Lineage {
   InstanceID = "MikeSofi";
   parent = "/root/cimv2:TST_Person.name=\"Mike\"";
   child = "/root/cimv2:TST_Person.name=\"Sofi\"";
};

instance of TST_Lineage {
   InstanceID = "MikeGabi";
   parent = "/root/cimv2:TST_Person.name=\"Mike\"";
   child = "/root/cimv2:TST_Person.name=\"Gabi\"";
};

instance of TST_MemberOfFamilyCollection {
   family = "/root/cimv2:TST_FamilyCollection.name=\"Family2\"";
   member = "/root/cimv2:TST_Person.name=\"Mike\"";
};
"""

OK = False
RUN = True
FAIL = False

MOCK_TEST_CASES = [
    # desc, args, exp_response, mock, condition

    #
    #   instance --help
    #
    ['instance subcommand help response',
     '--help',
     {'stdout': INST_HELP,
      'test': 'lines'},
     None, OK],
    #
    #  Instance Enumerate subcommand
    #
    ['instance subcommand enumerate  --help response',
     ['enumerate', '--help'],
     {'stdout': INST_ENUM_HELP,
      'test': 'lines'},
     None, OK],
    ['instance subcommand enumerate CIM_Foo',
     ['enumerate', 'CIM_Foo'],
     {'stdout': ENUM_INST_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],
    ['instance subcommand enumerate names CIM_Foo -o',
     ['enumerate', 'CIM_Foo', '-o'],
     {'stdout': ['root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"',
                 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],
    #
    #  instance get subcommand
    #
    ['instance subcommand enumerate deepinheritance CIM_Foo -d',
     ['enumerate', 'CIM_Foo', '-d'],
     {'stdout': ENUM_INST_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, False],

    #
    # instance enumerate error returns
    #
    ['instance subcommand enumerate error. invalid classname',
     ['enumerate', 'CIM_Foox'],
     {'stderr': 'Error: CIMError: 5: Class CIM_Foox not found in namespace'
                ' root/cimv2',
      'rc': 1,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],
    ['instance subcommand enumerate error. no classname',
     ['enumerate'],
     {'stderr':
         ['Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME',
          '',
          'Error: Missing argument "classname".'],
      'rc': 2,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance create subcommand
    #
    # TODO  tests
    ['instance subcommand create, --help response',
     ['create', '--help'],
     {'stdout': INST_CREATE_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],
    # TODO create valid instance tests
    # TODO create invaid instance tests

    #
    #  instance delete subcommand
    #
    ['instance subcommand delete, --help response',
     ['delete', '--help'],
     {'stdout': INST_DELETE_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],
    # TODO This test fails because we are incorrectly parsing the instance ID
    # fix with issue on moving to wbemurl from hand coded parser
    ['instance subcommand delete, valid delete',
     ['delete', 'CIM_Foo.InstanceID="CIM_Foo1"'],
     {'stdout': "Deleted",
      'rc': 2,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, False],

    ['instance subcommand delete, missing instance name',
     ['delete'],
     {'stderr':
         ['Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME',
          '',
          'Error: Missing argument "instancename".'],
      'rc': 2,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['instance subcommand delete, instance name not in repo',
     ['delete'],
     {'stderr':
         ['Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME',
          '',
          'Error: Missing argument "instancename".'],
      'rc': 2,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance references subcommand
    #
    ['instance subcommand references, --help response',
     ['references', '--help'],
     {'stdout': INST_REFERENCES_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],
    # TODO  add valid references test
    ['instance subcommand references, returns data',
     ['references', 'TST_Person.name="Mike"'],
     {'stdout': REF_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['instance subcommand references -o, returns data',
     ['references', 'TST_Person.name="Mike"', '-o'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"',
                 '//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection.family'
                 '="/root/cimv2:TST_FamilyCollection.name=\"Family2\"",member'
                 '="/root/cimv2:TST_Person.name=\"Mike\""'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, RUN],

    # TODO add invalid references tests
    ['instance subcommand references, no instance name',
     ['references'],
     {'stderr': ['Usage: pywbemcli instance references [COMMAND-OPTIONS] '
                 'INSTANCENAME',
                 '',
                 'Error: Missing argument "instancename".'],
      'rc': 2,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['instance subcommand references, invalid instance name',
     ['references', 'TST_Blah.blah="abc"'],
     {'stdout': ['Return empty.'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    #
    #  instance associators subcommand
    #
    ['instance subcommand associators, --help response',
     ['associators', '--help'],
     {'stdout': INST_ASSOCIATORS_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],
    # TODO  add valid associators tests
    # TODO add invalid associators tests

    #
    #  instance count subcommand
    #
    ['instance subcommand count, --help response',
     ['count', '--help'],
     {'stdout': INST_COUNT_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],
    ['instance subcommand count, Return table of instances',
     ['count', 'CIM_'],
     {'stdout': ['Count of instances per class',
                 'Class      count',
                 '-------  -------',
                 'CIM_Foo        3', ],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance invokemethod subcommand
    #

    #
    #  instance query subcommand
    #
    # We have not implemented this command

]


class TestSubcmdMock(CLITestsBase):
    """
    Test all of the class subcommand variations.
    """
    subcmd = 'instance'
    # mock_mof_file = 'simple_mock_model.mof'

    @pytest.mark.parametrize(
        "desc, args, exp_response, mock, condition",
        MOCK_TEST_CASES)
    def test_execute_pywbemcli(self, desc, args, exp_response, mock, condition):
        """
        Execute pybemcli with the defined input and test output.
        """
        env = None
        self.mock_subcmd_test(desc, self.subcmd, args, env, exp_response,
                              mock, condition)
