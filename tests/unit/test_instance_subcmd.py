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

# pylint: disable=line-too-long
INST_ENUM_HELP = """Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME

  Enumerate instances or names of CLASSNAME.

  Enumerate instances or instance names (the --name_only option) from the
  WBEMServer starting either at the top  of the hierarchy (if no CLASSNAME
  provided) or from the CLASSNAME argument if provided.

  Displays the returned instances (mof, xml, or table formats) or names

Options:
  -l, --localonly                 Show only local properties of the class.
  -d, --deepinheritance           If set, requests server to return properties
                                  in subclasses of the target instances class.
                                  If option not specified only properties from
                                  target class are returned
  -q, --includequalifiers         If set, requests server to include
                                  qualifiers in the returned instance(s).
  -c, --includeclassorigin        Include ClassOrigin in the result.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  option not specified a Null property
                                  list is created and the server returns all
                                  properties. Multiple properties may be
                                  defined with either a comma separated list
                                  defing the option multiple times. (ex: -p
                                  pn1 -p pn22 or -p pn1,pn2). If defined as
                                  empty string the server should return no
                                  properties.
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -o, --names_only                Show only local properties of the class.
  -s, --sort                      Sort into alphabetical order by classname.
  -S, --summary                   Return only summary of objects (count).
  -h, --help                      Show this message and exit.
"""

INST_GET_HELP = """Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME

  Get a single CIMInstance.

  Gets the instance defined by INSTANCENAME.

  This may be executed interactively by providing only a classname and the
  interactive option (-i).

Options:
  -l, --localonly                 Show only local properties of the returned
                                  instance.
  -q, --includequalifiers         If set, requests server to include
                                  qualifiers in the returned instance(s).
  -c, --includeclassorigin        Include class origin attribute in returned
                                  instance(s).
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  option not specified a Null property
                                  list is created and the server returns all
                                  properties. Multiple properties may be
                                  defined with either a comma separated list
                                  defing the option multiple times. (ex: -p
                                  pn1 -p pn22 or -p pn1,pn2). If defined as
                                  empty string the server should return no
                                  properties.
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -i, --interactive               If set, INSTANCENAME argument must be a
                                  class rather than an instance and user is
                                  presented with a list of instances of the
                                  class from which the instance to process is
                                  selected.
  -h, --help                      Show this message and exit.
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
                                  for each property to be included in the new
                                  instance.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  option not specified a Null property
                                  list is created and the server returns all
                                  properties. Multiple properties may be
                                  defined with either a comma separated list
                                  defing the option multiple times. (ex: -p
                                  pn1 -p pn22 or -p pn1,pn2). If defined as
                                  empty string the server should return no
                                  properties.
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -h, --help                      Show this message and exit.
"""

INST_DELETE_HELP = """Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME

  Delete a single CIM instance.

  Delete the instanced defined by INSTANCENAME from the WBEM server.

  This may be executed interactively by providing only a class name and the
  interactive option.

Options:
  -i, --interactive       If set, INSTANCENAME argument must be a class rather
                          than an instance and user is presented with a list
                          of instances of the class from which the instance to
                          process is selected.
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
   target `INSTANCENAME` in the target WBEM server filtered by the  `role`
   and `resultclass` options.

  This may be executed interactively by providing only a class name for
  `INSTANCENAME` and the `interactive` option(-i). Pywbemcli presents a list
  of instances names in the class from which one can be chosen as the
  target.

Options:
  -R, --resultclass <class name>  Filter by the result class name provided.
  -r, --role <role name>          Filter by the role name provided.
  -q, --includequalifiers         If set, requests server to include
                                  qualifiers in the returned instance(s).
  -c, --includeclassorigin        Include classorigin in the result.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  option not specified a Null property
                                  list is created and the server returns all
                                  properties. Multiple properties may be
                                  defined with either a comma separated list
                                  defing the option multiple times. (ex: -p
                                  pn1 -p pn22 or -p pn1,pn2). If defined as
                                  empty string the server should return no
                                  properties.
  -o, --names_only                Show only local properties of the class.
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -s, --sort                      Sort into alphabetical order by classname.
  -i, --interactive               If set, INSTANCENAME argument must be a
                                  class rather than an instance and user is
                                  presented with a list of instances of the
                                  class from which the instance to process is
                                  selected.
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
  -q, --includequalifiers         If set, requests server to include
                                  qualifiers in the returned instance(s).
  -c, --includeclassorigin        Include classorigin in the result.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  option not specified a Null property
                                  list is created and the server returns all
                                  properties. Multiple properties may be
                                  defined with either a comma separated list
                                  defing the option multiple times. (ex: -p
                                  pn1 -p pn22 or -p pn1,pn2). If defined as
                                  empty string the server should return no
                                  properties.
  -o, --names_only                Show only local properties of the class.
  -n, --namespace <name>          Namespace to use for this operation. If
                                  defined that namespace overrides the general
                                  options namespace
  -s, --sort                      Sort into alphabetical order by classname.
  -i, --interactive               If set, INSTANCENAME argument must be a
                                  class rather than an instance and user is
                                  presented with a list of instances of the
                                  class from which the instance to process is
                                  selected.
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

REF_INSTS = """instance of TST_Lineage {
   InstanceID = "MikeSofi";
   parent = "/root/cimv2:TST_Person.name=\\\"Mike\\\"";
   child = "/root/cimv2:TST_Person.name=\\\"Sofi\\\"";
};

instance of TST_Lineage {
   InstanceID = "MikeGabi";
   parent = "/root/cimv2:TST_Person.name=\\\"Mike\\\"";
   child = "/root/cimv2:TST_Person.name=\\\"Gabi\\\"";
};

instance of TST_MemberOfFamilyCollection {
   family = "/root/cimv2:TST_FamilyCollection.name=\\\"Family2\\\"";
   member = "/root/cimv2:TST_Person.name=\\\"Mike\\\"";
};

"""

ASSOC_INSTS = """instance of TST_Person {
   name = "Sofi";
};

instance of TST_Person {
   name = "Gabi";
};

instance of TST_FamilyCollection {
   name = "Family2";
};

"""

# pylint: enable=line-too-long

OK = True
RUN = True
FAIL = False

MOCK_TEST_CASES = [
    # desc, args, exp_response, mock, condition

    #
    #   instance --help
    #
    ['Verify instance subcommand help response',
     '--help',
     {'stdout': INST_HELP,
      'test': 'lines'},
     None, OK],

    #
    #  Instance Enumerate subcommand good responses
    #
    ['Verify instance subcommand enumerate  --help response',
     ['enumerate', '--help'],
     {'stdout': INST_ENUM_HELP,
      'test': 'lines'},
     None, OK],

    ['Verify instance subcommand enumerate CIM_Foo',
     ['enumerate', 'CIM_Foo'],
     {'stdout': ENUM_INST_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate names CIM_Foo -o',
     ['enumerate', 'CIM_Foo', '-o'],
     {'stdout': ['root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"',
                 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate deepinheritance CIM_Foo -d',
     ['enumerate', 'CIM_Foo', '-d'],
     {'stdout': ENUM_INST_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    #
    # instance enumerate error returns
    #
    ['Verify instance subcommand enumerate error, invalid classname fails',
     ['enumerate', 'CIM_Foox'],
     {'stderr': 'Error: CIMError: 5: Class CIM_Foox not found in namespace'
                ' root/cimv2',
      'rc': 1,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate error, no classname fails',
     ['enumerate'],
     {'stderr':
      ['Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME',
       '',
       'Error: Missing argument "classname".'],
      'rc': 2,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance get subcommand
    #

    ['Verify instance subcommand get with instancename returns data',
     ['get', '--help'],
     {'stdout': INST_GET_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],

    ['Verify instance subcommand get with instancename returns data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with instancename local_only returns data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '-l'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify instance subcommand get with instancename --localonly returns '
     ' data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--localonly'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with instancename prop list -p returns '
     ' one property',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '-p', 'InstanceID'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with instancename prop list '
     '--propertylist returns property',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--propertylist', 'InstanceID'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with instancename prop list -p  '
     ' InstanceID,IntegerProp returns 2 properties',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '-p', 'InstanceID,IntegerProp'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with instancename prop list -p '
     ' multiple instances of option returns 2 properties',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '-p', 'InstanceID',
      '-p', 'IntegerProp'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with instancename empty  prop list '
     'returns  empty instance',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '-p', '""'],
     {'stdout': ['instance of CIM_Foo {',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, FAIL],
    # TODO: This should return an empty instance not the statement Return empty

    #
    #  get subcommand errors
    #
    ['instance subcommand get error. no classname',
     ['get'],
     {'stderr':
      ['Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME',
       '',
       'Error: Missing argument "instancename".'],
      'rc': 2,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get error. no classname',
     ['get', 'CIM_Foo.InstanceID="CIM_blah"'],
     {'stderr':
      ['Error: CIMError: 6: Instance not found in repository namespace '
       'root/cimv2. Path=root/cimv2:CIM_Foo.InstanceID="CIM_blah"'],
      'rc': 1,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance create subcommand
    #
    ['Verify instance subcommand create, --help response',
     ['create', '--help'],
     {'stdout': INST_CREATE_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],

    ['Verify instance subcommand create, new instance of CIM_Foo',
     ['create', 'CIM_Foo', '-P', 'InstanceID=blah'],
     {'stdout': "",
      'rc': 0,
      'test': 'lines'},
     None, FAIL],

    # TODO create more valid create instance tests
    # TODO create invaid create instance tests

    #
    #  instance delete subcommand
    #
    ['Verify instance subcommand delete, --help response',
     ['delete', '--help'],
     {'stdout': INST_DELETE_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],

    ['Verify instance subcommand delete, valid delete',
     ['delete', 'CIM_Foo.InstanceID="CIM_Foo1"'],
     {'stdout': ''
         'Deleted root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand delete, missing instance name',
     ['delete'],
     {'stderr':
      ['Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME',
       '',
       'Error: Missing argument "instancename".'],
      'rc': 2,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand delete, instance name not in repo',
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
    ['Verify instance subcommand references, --help response',
     ['references', '--help'],
     {'stdout': INST_REFERENCES_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],

    ['Verify instance subcommand references, returns instances',
     ['references', 'TST_Person.name="Mike"'],
     {'stdout': REF_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references -o, returns paths',
     ['references', 'TST_Person.name="Mike"', '-o'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"',
                 '//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection.family'
                 '="/root/cimv2:TST_FamilyCollection.name=\\"Family2\\"",member'
                 '="/root/cimv2:TST_Person.name=\\"Mike\\""'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references -o, returns paths with resultclass '
     'valid returns paths',
     ['references', 'TST_Person.name="Mike"', '-o',
      '--resultclass', 'TST_Lineage'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"', ],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references -o, returns paths with resultclass '
     'short formvalid returns paths',
     ['references', 'TST_Person.name="Mike"', '-o',
      '-R', 'TST_Lineage'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"', ],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references -o, returns paths with resultclass '
     'not a real ref returns no paths',
     ['references', 'TST_Person.name="Mike"', '-o',
      '--resultclass', 'TST_Lineagex'],
     {'stdout': [],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    # TODO add invalid references tests
    ['Verify instance subcommand references, no instance name',
     ['references'],
     {'stderr': ['Usage: pywbemcli instance references [COMMAND-OPTIONS] '
                 'INSTANCENAME',
                 '',
                 'Error: Missing argument "instancename".'],
      'rc': 2,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references, invalid instance name',
     ['references', 'TST_Blah.blah="abc"'],
     {'stdout': ['Return empty.'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    #
    #  instance associators subcommand
    #
    ['Verify instance subcommand associators, --help response',
     ['associators', '--help'],
     {'stdout': INST_ASSOCIATORS_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],
    # TODO  add valid associators tests

    ['Verify instance subcommand associators, returns iinstances',
     ['associators', 'TST_Person.name="Mike"'],
     {'stdout': ASSOC_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associators -o, returns data',
     ['associators', 'TST_Person.name="Mike"', '-o'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Person.name="Sofi"',
                 '//FakedUrl/root/cimv2:TST_Person.name="Gabi"',
                 '//FakedUrl/root/cimv2:TST_FamilyCollection.name="Family2"'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    # TODO add invalid associators tests
    ['Verify instance subcommand associators, no instance name',
     ['associators'],
     {'stderr': ['Usage: pywbemcli instance associators [COMMAND-OPTIONS] '
                 'INSTANCENAME',
                 '',
                 'Error: Missing argument "instancename".'],
      'rc': 2,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associators, invalid instance name',
     ['associators', 'TST_Blah.blah="abc"'],
     {'stdout': ['Return empty.'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],
    #
    #  instance count subcommand
    #
    ['Verify instance subcommand count, --help response',
     ['count', '--help'],
     {'stdout': INST_COUNT_HELP,
      'rc': 0,
      'test': 'lines'},
     None, OK],

    ['Verify instance subcommand count, Return table of instances',
     ['count', 'CIM_'],
     {'stdout': ['Count of instances per class',
                 'Class      count',
                 '-------  -------',
                 'CIM_Foo        3', ],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand count, --sort. Return table of instances',
     ['count', 'CIM_'],
     {'stdout': ['Count of instances per class',
                 'Class      count',
                 '-------  -------',
                 'CIM_Foo        3', ],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],
    # TODO add subclass instances to the test.

    #
    #  instance invokemethod subcommand
    #

    #
    #  instance query subcommand. We have not implemented this command

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
