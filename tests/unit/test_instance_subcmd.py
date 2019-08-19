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
from __future__ import absolute_import, print_function

import os
import pytest
from .cli_test_extensions import CLITestsBase

TEST_DIR = os.path.dirname(__file__)

SIMPLE_MOCK_FILE = 'simple_mock_model.mof'
ASSOC_MOCK_FILE = 'simple_assoc_mock_model.mof'
ALLTYPES_MOCK_FILE = 'all_types.mof'
INVOKE_METHOD_MOCK_FILE = "simple_mock_invokemethod.py"
MOCK_PROMPT_0_FILE = "mock_prompt_0.py"
MOCK_CONFIRM_Y_FILE = "mock_confirm_y.py"
MOCK_CONFIRM_N_FILE = "mock_confirm_n.py"

INST_HELP = """
Usage: pywbemcli instance [COMMAND-OPTIONS] COMMAND [ARGS]...

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
  create        Create a CIM instance of CLASSNAME.
  delete        Delete a single CIM instance.
  enumerate     Enumerate instances or names of CLASSNAME.
  get           Get a single CIMInstance.
  invokemethod  Invoke a CIM method on a CIMInstance.
  modify        Modify an existing instance.
  query         Execute an execquery request.
  references    Get the reference instances or names.
"""

# pylint: disable=line-too-long
INST_ENUMERATE_HELP = """
Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME

  Enumerate instances or names of CLASSNAME.

  Get CIMInstance or CIMInstanceName (--name_only option) objects from the
  WBEMServer starting either at the top  of the hierarchy (if no CLASSNAME
  provided) or from the CLASSNAME argument if provided.

  Displays the returned instances in mof, xml, or table formats or the
  instance names as a string or XML formats (--names-only option).

  Results are formatted as defined by the --output_format general option.

Options:
  -l, --localonly                 Show only local properties of the instances.
                                  This subcommand may use either pull or
                                  traditional operations depending on the
                                  server and the "--use--pull-ops" general
                                  option. If pull operations are used, this
                                  parameters will not be included, even if
                                  specified. If traditional operations are
                                  used, some servers do not process the
                                  parameter.
  -d, --deepinheritance           If set, requests server to return properties
                                  in subclasses of the target instances class.
                                  If option not specified only properties from
                                  target class are returned
  -q, --includequalifiers         If set, requests server to include
                                  qualifiers in the returned instances. This
                                  subcommand may use either pull or
                                  traditional operations depending on the
                                  server and the "--use--pull-ops" general
                                  option. If pull operations are used,
                                  qualifiers will not be included, even if
                                  this option is specified. If traditional
                                  operations are used, inclusion of qualifiers
                                  depends on the server.
  -c, --includeclassorigin        Include class origin attribute in returned
                                  instance(s).
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
  -n, --namespace <name>          Namespace to use for this operation, instead
                                  of the default namespace of the connection
  -o, --names-only                Retrieve only the returned object names.
  -s, --sort                      Sort into alphabetical order by classname.
  -S, --summary                   Return only summary of objects (count).
  -f, --filterquery TEXT          A filter query to be passed to the server if
                                  the pull operations are used. If this option
                                  is defined and the --filterquerylanguage is
                                  None, pywbemcli assumes DMTF:FQL. If this
                                  option is defined and the traditional
                                  operations are used, the filter is not sent
                                  to the server. See the documentation for
                                  more information. (Default: None)
  --filterquerylanguage TEXT      A filterquery language to be used with a
                                  filter query defined by --filterquery.
                                  (Default: None)
  -h, --help                      Show this message and exit.

"""

INST_GET_HELP = """
Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME

  Get a single CIMInstance.

  Gets the instance defined by `INSTANCENAME` where `INSTANCENAME` must
  resolve to the instance name of the desired instance. This may be supplied
  directly as an untyped wbem_uri formatted string or through the
  --interactive option. The wbemuri may contain the namespace or the
  namespace can be supplied with the --namespace option. If no namespace is
  supplied, the connection default namespace is used.  Any host name in the
  wbem_uri is ignored.

  This method may be executed interactively by providing only a classname
  and the interactive option (-i).

  Otherwise the INSTANCENAME must be a CIM instance name in the format
  defined by DMTF `DSP0207`.

  Results are formatted as defined by the --output_format general option.

Options:
  -l, --localonly                 Request that server show only local
                                  properties of the returned instance. Some
                                  servers may not process this parameter.
  -q, --includequalifiers         If set, requests server to include
                                  qualifiers in the returned instances. Not
                                  all servers return qualifiers on instances
  -c, --includeclassorigin        Include class origin attribute in returned
                                  instance(s).
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
  -n, --namespace <name>          Namespace to use for this operation, instead
                                  of the default namespace of the connection
  -i, --interactive               If set, `INSTANCENAME` argument must be a
                                  class rather than an instance and user is
                                  presented with a list of instances of the
                                  class from which the instance to process is
                                  selected.
  -h, --help                      Show this message and exit.

"""

INST_CREATE_HELP = """
Usage: pywbemcli instance create [COMMAND-OPTIONS] CLASSNAME

  Create a CIM instance of CLASSNAME.

  Creates an instance of the class CLASSNAME with the properties defined in
  the property option.

  Pywbemcli creates the new instance using CLASSNAME retrieved from the
  current WBEM server as a template for property characteristics. Therefore
  pywbemcli will generate an exception if CLASSNAME does not exist in the
  current WBEM server or if the data definition in the properties options
  does not match the properties characteristics defined the returned class.

  ex. pywbemcli instance create CIM_blah -p id=3 -p strp="bla bla", -p p3=3

Options:
  -P, --property name=value  Optional property definitions of the form
                             name=value. Multiple definitions allowed, one for
                             each property to be included in the
                             createdinstance. Array property values defined by
                             comma-separated-values. EmbeddedInstance not
                             allowed.
  -V, --verify               If set, The change is displayed and verification
                             requested before the change is executed
  -n, --namespace <name>     Namespace to use for this operation, instead of
                             the default namespace of the connection
  -h, --help                 Show this message and exit.

"""

INST_DELETE_HELP = """
Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME

  Delete a single CIM instance.

  Delete the instanced defined by INSTANCENAME from the WBEM server.

  This may be executed interactively by providing only a class name and the
  interactive option.

  Otherwise the INSTANCENAME must be a CIM instance name in the format
  defined by DMTF `DSP0207`.

Options:
  -i, --interactive       If set, `INSTANCENAME` argument must be a class
                          rather than an instance and user is presented with a
                          list of instances of the class from which the
                          instance to process is selected.
  -n, --namespace <name>  Namespace to use for this operation, instead of the
                          default namespace of the connection
  -h, --help              Show this message and exit.

"""

INST_COUNT_HELP = """
Usage: pywbemcli instance count [COMMAND-OPTIONS] CLASSNAME-GLOB

  Get instance count for classes.

  Displays the count of instances for the classes defined by the `CLASSNAME-
  GLOB` argument in one or more namespaces.

  The size of the response may be limited by CLASSNAME-GLOB argument which
  defines a regular expression based on the desired class names so that only
  classes that match the regex are counted. The CLASSNAME-GLOB argument is
  optional.

  The CLASSNAME-GLOB argument may be either a complete classname or a
  regular expression that can be matched to one or more classnames. To limit
  the filter to a single classname, terminate the classname with $.

  The GLOB expression is anchored to the beginning of the CLASSNAME-GLOB, is
  is case insensitive and uses the standard GLOB special characters (*(match
  everything), ?(match single character)). Thus, `pywbem_*` returns all
  classes that begin with `PyWBEM_`, `pywbem_`, etc. '.*system*' returns
  classnames that include the case insensitive string `system`.

  This operation can take a long time to execute since it enumerates all
  classes in the namespace.

Options:
  -s, --sort              Sort by instance count. Otherwise sorted by
                          classname
  -n, --namespace <name>  Namespace to use for this operation, instead of the
                          default namespace of the connection
  -h, --help              Show this message and exit.

"""

INST_REFERENCES_HELP = """
Usage: pywbemcli instance references [COMMAND-OPTIONS] INSTANCENAME

  Get the reference instances or names.

  Gets the reference instances or instance names(--names-only option) for a
  target `INSTANCENAME` in the target WBEM server filtered by the `role` and
  `resultclass` options.

  INSTANCENAME must be a CIM instance name in the format defined by DMTF
  `DSP0207`.

  This may be executed interactively by providing only a class name for
  `INSTANCENAME` and the `interactive` option(-i). Pywbemcli presents a list
  of instances names in the class from which you can be chosen as the
  target.

  Results are formatted as defined by the --output_format general option.

Options:
  -R, --resultclass <class name>  Filter by the result class name provided.
                                  Each returned instance (or instance name)
                                  should be a member of this class or its
                                  subclasses. Optional
  -r, --role <role name>          Filter by the role name provided. Each
                                  returned instance (or instance name) should
                                  refer to the target instance through a
                                  property with aname that matches the value
                                  of this parameter. Optional.
  -q, --includequalifiers         If set, requests server to include
                                  qualifiers in the returned instances. This
                                  subcommand may use either pull or
                                  traditional operations depending on the
                                  server and the "--use--pull-ops" general
                                  option. If pull operations are used,
                                  qualifiers will not be included, even if
                                  this option is specified. If traditional
                                  operations are used, inclusion of qualifiers
                                  depends on the server.
  -c, --includeclassorigin        Include class origin attribute in returned
                                  instance(s).
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
  -o, --names-only                Retrieve only the returned object names.
  -n, --namespace <name>          Namespace to use for this operation, instead
                                  of the default namespace of the connection
  -s, --sort                      Sort into alphabetical order by classname.
  -i, --interactive               If set, `INSTANCENAME` argument must be a
                                  class rather than an instance and user is
                                  presented with a list of instances of the
                                  class from which the instance to process is
                                  selected.
  -S, --summary                   Return only summary of objects (count).
  -f, --filterquery TEXT          A filter query to be passed to the server if
                                  the pull operations are used. If this option
                                  is defined and the --filterquerylanguage is
                                  None, pywbemcli assumes DMTF:FQL. If this
                                  option is defined and the traditional
                                  operations are used, the filter is not sent
                                  to the server. See the documentation for
                                  more information. (Default: None)
  --filterquerylanguage TEXT      A filterquery language to be used with a
                                  filter query defined by --filterquery.
                                  (Default: None)
  -h, --help                      Show this message and exit.

"""

INST_MODIFY_HELP = """
Usage: pywbemcli instance modify [COMMAND-OPTIONS] INSTANCENAME

  Modify an existing instance.

  Modifies CIM instance defined by INSTANCENAME in the WBEM server using the
  property names and values defined by the property option and the CIM class
  defined by the instance name.  The propertylist option if provided is
  passed to the WBEM server as part of the ModifyInstance operation
  (normally the WBEM server limits modifications) to just those properties
  defined in the property list.

  INSTANCENAME must be a CIM instance name in the format defined by DMTF
  `DSP0207`.

  Pywbemcli builds only the properties defined with the --property option
  into an instance based on the CIMClass and forwards that to the WBEM
  server with the ModifyInstance method.

  ex. pywbemcli instance modify CIM_blah.fred=3 -p id=3 -p strp="bla bla"

Options:
  -P, --property name=value       Optional property definitions of the form
                                  name=value. Multiple definitions allowed,
                                  one for each property to be included in the
                                  createdinstance. Array property values
                                  defined by comma-separated-values.
                                  EmbeddedInstance not allowed.
  -p, --propertylist <property name>
                                  Define a propertylist for the request. If
                                  option not specified a Null property list is
                                  created. Multiple properties may be defined
                                  with either a comma separated list defining
                                  the option multiple times. (ex: -p pn1 -p
                                  pn22 or -p pn1,pn2). If defined as empty
                                  string an empty propertylist is created. The
                                  server uses the propertylist to limit
                                  changes made to the instance to properties
                                  in the propertylist.
  -i, --interactive               If set, `INSTANCENAME` argument must be a
                                  class rather than an instance and user is
                                  presented with a list of instances of the
                                  class from which the instance to process is
                                  selected.
  -V, --verify                    If set, The change is displayed and
                                  verification requested before the change is
                                  executed
  -n, --namespace <name>          Namespace to use for this operation, instead
                                  of the default namespace of the connection
  -h, --help                      Show this message and exit.
"""

INST_ASSOCIATORS_HELP = """
Usage: pywbemcli instance associators [COMMAND-OPTIONS] INSTANCENAME

  Get associated instances or names.

  Returns the associated instances or names (--names-only option) for the
  `INSTANCENAME` argument filtered by the --assocclass, --resultclass,
  --role and --resultrole options.

  INSTANCENAME must be a CIM instance name in the format defined by DMTF
  `DSP0207`.

  This may be executed interactively by providing only a classname and the
  interactive option. Pywbemcli presents a list of instances in the class
  from which one can be chosen as the target.

  Results are formatted as defined by the --output_format general option.

Options:
  -a, --assocclass <class name>   Filter by the association class name
                                  provided.Each returned instance (or instance
                                  name) should be associated to the source
                                  instance through this class or its
                                  subclasses. Optional.
  -c, --resultclass <class name>  Filter by the result class name provided.
                                  Each returned instance (or instance name)
                                  should be a member of this class or one of
                                  its subclasses. Optional
  -r, --role <role name>          Filter by the role name provided. Each
                                  returned instance (or instance name)should
                                  be associated with the source instance
                                  (INSTANCENAME) through an association with
                                  this role (property name in the association
                                  that matches this parameter). Optional.
  -R, --resultrole <role name>    Filter by the result role name provided.
                                  Each returned instance (or instance
                                  name)should be associated with the source
                                  instance name (`INSTANCENAME`) through an
                                  association with returned object having this
                                  role (property name in the association that
                                  matches this parameter). Optional.
  -q, --includequalifiers         If set, requests server to include
                                  qualifiers in the returned instances. This
                                  subcommand may use either pull or
                                  traditional operations depending on the
                                  server and the "--use--pull-ops" general
                                  option. If pull operations are used,
                                  qualifiers will not be included, even if
                                  this option is specified. If traditional
                                  operations are used, inclusion of qualifiers
                                  depends on the server.
  -c, --includeclassorigin        Include class origin attribute in returned
                                  instance(s).
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
  -o, --names-only                Retrieve only the returned object names.
  -n, --namespace <name>          Namespace to use for this operation, instead
                                  of the default namespace of the connection
  -s, --sort                      Sort into alphabetical order by classname.
  -i, --interactive               If set, `INSTANCENAME` argument must be a
                                  class rather than an instance and user is
                                  presented with a list of instances of the
                                  class from which the instance to process is
                                  selected.
  -S, --summary                   Return only summary of objects (count).
  -f, --filterquery TEXT          A filter query to be passed to the server if
                                  the pull operations are used. If this option
                                  is defined and the --filterquerylanguage is
                                  None, pywbemcli assumes DMTF:FQL. If this
                                  option is defined and the traditional
                                  operations are used, the filter is not sent
                                  to the server. See the documentation for
                                  more information. (Default: None)
  --filterquerylanguage TEXT      A filterquery language to be used with a
                                  filter query defined by --filterquery.
                                  (Default: None)
  -h, --help                      Show this message and exit.
"""

INST_INVOKE_METHOD_HELP = """
Usage: pywbemcli instance invokemethod [COMMAND-OPTIONS] INSTANCENAME
                                       METHODNAME

  Invoke a CIM method on a CIMInstance.

  Invoke the method defined by INSTANCENAME and METHODNAME arguments with
  parameters defined by the --parameter options.

  This issues an instance level invokemethod request and displays the
  results.

  INSTANCENAME must be a CIM instance name in the format defined by  DMTF
  `DSP0207`.

  Pywbemcli creates the method call using the class in INSTANCENAME
  retrieved from the current WBEM server as a template for parameter
  characteristics. Therefore pywbemcli will generate an exception if
  CLASSNAME does not exist in the current WBEM server or if the data
  definition in the parameter options does not match the parameter
  characteristics defined the returned class.

  A class level invoke method is available as `pywbemcli class
  invokemethod`.

  Example:

  pywbmcli instance invokemethod  CIM_x.InstanceID='hi" methodx -p id=3

Options:
  -p, --parameter name=value  Multiple definitions allowed, one for each
                              parameter to be included in the new instance.
                              Array parameter values defined by comma-
                              separated-values. EmbeddedInstance not allowed.
  -i, --interactive           If set, `INSTANCENAME` argument must be a class
                              rather than an instance and user is presented
                              with a list of instances of the class from which
                              the instance to process is selected.
  -n, --namespace <name>      Namespace to use for this operation, instead of
                              the default namespace of the connection
  -h, --help                  Show this message and exit.

"""

INST_QUERY_HELP = """
Usage: pywbemcli instance query [COMMAND-OPTIONS] QUERY_STRING

  Execute an execquery request.

  Executes a query request on the target WBEM server with the QUERY_STRING
  argument and query language options.

  The results of the query are displayed as mof or xml.

  Results are formatted as defined by the --output_format general option.

Options:
  -l, --querylanguage QUERY LANGUAGE
                                  Use the query language defined. (Default:
                                  DMTF:CQL.
  -n, --namespace <name>          Namespace to use for this operation, instead
                                  of the default namespace of the connection
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

GET_INST_ALL_TYPES = """instance of PyWBEM_AllTypes {
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

ENUM_INST_TABLE_RESP = """Instances: CIM_Foo
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

ENUM_INSTNAME_TABLE_RESP = """InstanceNames: CIM_Foo
+--------+-------------+----------------------------------------+
| host   | namespace   | keybindings                            |
+========+=============+========================================+
|        | root/cimv2  | NocaseDict({'InstanceID': 'CIM_Foo1'}) |
+--------+-------------+----------------------------------------+
|        | root/cimv2  | NocaseDict({'InstanceID': 'CIM_Foo2'}) |
+--------+-------------+----------------------------------------+
|        | root/cimv2  | NocaseDict({'InstanceID': 'CIM_Foo3'}) |
+--------+-------------+----------------------------------------+
"""

ENUM_INST_GET_TABLE_RESP = """Instances: CIM_Foo
InstanceID      IntegerProp
------------  -------------
"CIM_Foo1"                1
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

OK = True    # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet

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

    #
    #   instance --help
    #
    ['Verify instance subcommand help response',
     '--help',
     {'stdout': INST_HELP,
      'test': 'linesnows'},
     None, OK],

    #
    #  Instance Enumerate subcommand good responses
    #
    ['Verify instance subcommand enumerate  --help response',
     ['enumerate', '--help'],
     {'stdout': INST_ENUMERATE_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify instance subcommand enumerate CIM_Foo',
     ['enumerate', 'CIM_Foo'],
     {'stdout': ENUM_INST_RESP,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate names CIM_Foo -o',
     ['enumerate', 'CIM_Foo', '-o'],
     {'stdout': ['', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate names CIM_Foo -o -s',
     ['enumerate', 'CIM_Foo', '-o', '--summary'],
     {'stdout': ['3 CIMInstanceName(s) returned'],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate names CIM_Foo -o --namespace',
     ['enumerate', 'CIM_Foo', '-o', '--namespace', 'root/cimv2'],
     {'stdout': ['', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate names CIM_Foo -o --sort',
     ['enumerate', 'CIM_Foo', '--names-only', '--sort'],
     {'stdout': ['', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"',
                 '', 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"', ],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate CIM_Foo --includequalifiers',
     ['enumerate', 'CIM_Foo', '--includequalifiers'],
     {'stdout': ENUM_INST_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate CIM_Foo includequalifiers and '
     ' --use-pull-ops no',
     {'args': ['enumerate', 'CIM_Foo', '--includequalifiers'],
      'global': ['--use-pull-ops', 'no']},
     {'stdout': ENUM_INST_RESP,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate CIM_Foo with --use-pull-ops yes and '
     '--pull_max_cnt=2',
     {'args': ['enumerate', 'CIM_Foo', '--includequalifiers'],
      'global': ['--use-pull-ops', 'yes', '--pull-max-cnt', '2', '--log',
                 'all=stderr']},
     {'stderr': [r'PullInstancesWithPath\(pull_inst_result_tuple\(context='
                 'None, eos=True,',
                 r'PullInstancesWithPath\(MaxObjectCount=2',
                 r'OpenEnumerateInstances\(ClassName='],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate CIM_Foo with --use-pull-ops yes and '
     '--pull_max_cnt=2 and --namesonly',
     {'args': ['enumerate', 'CIM_Foo', '--names-only'],
      'global': ['--use-pull-ops', 'yes', '--pull-max-cnt', '2', '--log',
                 'all=stderr']},
     {'stderr': [r'PullInstancePaths\(pull_path_result_tuple\(context='
                 'None, eos=True,',
                 r'PullInstancePaths\(MaxObjectCount=2',
                 r'OpenEnumerateInstancePaths\(ClassName='],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate deepinheritance CIM_Foo -d',
     ['enumerate', 'CIM_Foo', '-d'],
     {'stdout': ENUM_INST_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate deepinheritance CIM_Foo '
     '--deepinheritance',
     ['enumerate', 'CIM_Foo', '--deepinheritance'],
     {'stdout': ENUM_INST_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand -o grid enumerate deepinheritance CIM_Foo -d',
     {'args': ['enumerate', 'CIM_Foo', '-d'],
      'global': ['--output-format', 'grid']},
     {'stdout': ENUM_INST_TABLE_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand -o grid enumerate di CIM_Foo -d -o',
     {'args': ['enumerate', 'CIM_Foo', '-d', '-o'],
      'global': ['--output-format', 'grid']},
     {'stdout': ENUM_INSTNAME_TABLE_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand -o grid enumerate di CIM_Foo -d -o',
     {'args': ['enumerate', 'CIM_Foo', '-d', '-o'],
      'global': ['--output-format', 'txt']},
     {'stdout': ['root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"',
                 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"',
                 'root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"'],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify instance subcommand -o grid enumerate di CIM_Foo -d -o',
     {'args': ['enumerate', 'CIM_Foo'],
      'global': ['--output-format', 'txt']},
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

    ['Verify instance subcommand -o grid enumerate di alltypes, datetime',
     {'args': ['enumerate', 'Pywbem_Alltypes', '-d',
               '--propertylist', 'scalDateTime', '-p', 'scalTimeDelta'],
      'global': ['--output-format', 'grid']},
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

    ['Verify instance subcommand enumerate with query.',
     ['enumerate', 'CIM_Foo', '--filterquery', 'InstanceID = 3'],
     {'stdout': ENUM_INST_RESP,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate with query, traditional ops fails',
     {'args': ['enumerate', 'CIM_Foo', '--filterquery', 'InstanceID = 3'],
      'global': ['--use-pull-ops', 'no']},
     {'stderr': ["ValueError",
                 "EnumerateInstances does not support FilterQuery"],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify subcommand enumerate with CIM_Foo summary table output',
     {'args': ['enumerate', 'CIM_Foo', '--names-only'],
      'global': ['--output-format', 'table']},
     {'stdout': """InstanceNames: CIM_Foo
+--------+-------------+----------------------------------------+
| host   | namespace   | keybindings                            |
|--------+-------------+----------------------------------------|
|        | root/cimv2  | NocaseDict({'InstanceID': 'CIM_Foo1'}) |
|        | root/cimv2  | NocaseDict({'InstanceID': 'CIM_Foo2'}) |
|        | root/cimv2  | NocaseDict({'InstanceID': 'CIM_Foo3'}) |
+--------+-------------+----------------------------------------+
""",
      'rc': 0,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify subcommand enumerate with CIM_Foo summary table output',
     {'args': ['enumerate', 'CIM_Foo', '--summary'],
      'global': ['--output-format', 'table']},
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

    # TODO the following uses deepinheritance because of issue in pywbem_mock
    ['Verify subcommand enumerate with PyWBEM_AllTypes table with scalar '
     'properties returns instance with all property types',
     {'args': ['enumerate', 'PyWBEM_AllTypes', '--deepinheritance',
               '--propertylist',
               'instanceid,scalbool,scaluint32,scalsint32'],
      'global': ['--output-format', 'grid']},
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

    ['Verify subcommand enumerate with PyWBEM_AllTypes with array properties '
     'returns instance with all property types',
     {'args': ['enumerate', 'PyWBEM_AllTypes', '--deepinheritance',
               '--propertylist',
               'instanceid,arraybool,arrayuint32,arraysint32'],
      'global': ['--output-format', 'grid']},
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
    ['Verify instance subcommand enumerate error, invalid classname fails',
     ['enumerate', 'CIM_Foox'],
     {'stderr': ["Error: CIMError: 6"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate error, no classname fails',
     ['enumerate'],
     {'stderr':
      ['Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME', ],
      'rc': 2,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate error, invalid namespace',
     ['enumerate', 'CIM_Foo', '--namespace', 'root/blah'],
     {'stderr':
      ["CIMError: 3 (CIM_ERR_INVALID_NAMESPACE): Namespace does not exist in "
       "mock repository: 'root/blah'", ],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate fails invalid query language',
     ['enumerate', 'CIM_Foo', '--filterquerylanguage', 'blah',
      '--filterquery', 'InstanceID = 3'],
     {'stderr': ['CIMError', '14', 'CIM_ERR_QUERY_LANGUAGE_NOT_SUPPORTED'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand enumerate fails using traditional op',
     {'args': ['enumerate', 'CIM_Foo', '--filterquery', 'InstanceID = 3'],
      'global': ['--use-pull-ops', 'no']},
     {'stderr':
      ['ValueError', 'EnumerateInstances does not support FilterQuery'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance get subcommand
    #

    ['Verify instance subcommand get with instancename returns data',
     ['get', '--help'],
     {'stdout': INST_GET_HELP,
      'rc': 0,
      'test': 'linesnows'},
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

    ['Verify instance subcommand get with instancename, namespace returns data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--namespace', 'root/cimv2'],
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

    ['Verify instance subcommand get with instancename --includequalifiers '
     'returns data',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--includequalifiers'],
     {'stdout': ['instance of CIM_Foo {',
                 '   InstanceID = "CIM_Foo1";',
                 '   IntegerProp = 1;',
                 '};',
                 ''],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with instancename --includequalifiers and '
     'general --use-pull-ops returns data',
     {'args': ['get', 'CIM_Foo.InstanceID="CIM_Foo1"', '--includequalifiers'],
      'global': ['--use-pull-ops', 'no']},
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
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with instancename PyWBEM_AllTypes'
     ' returns instance with all property types',
     ['get', 'PyWBEM_AllTypes.InstanceID="test_instance"'],
     {'stdout': GET_INST_ALL_TYPES,
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand -o grid get CIM_Foo',
     {'args': ['get', 'CIM_Foo.InstanceID="CIM_Foo1"'],
      'global': ['-o', 'simple']},
     {'stdout': ENUM_INST_GET_TABLE_RESP,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with interactive option',
     ['get', 'TST_Person', '-i'],
     {'stdout':
      ['root/cimv2:TST_Person.name="Mike"',
       'instance of TST_Person {'],
      'rc': 0,
      'test': 'in'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], OK],

    ['Verify instance subcommand get with interactive option',
     ['get', 'TST_Person', '--interactive'],
     {'stdout':
      ['root/cimv2:TST_Person.name="Mike"',
       'instance of TST_Person {'],
      'rc': 0,
      'test': 'in'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], OK],

    #
    #  get subcommand errors
    #
    ['instance subcommand get error. no classname',
     ['get'],
     {'stderr':
      ['Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME', ],
      'rc': 2,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['instance subcommand get error. invalid namespace',
     ['get', 'CIM_Foo.InstanceID="CIM_Foo1"',
      '--namespace', 'root/invalidnamespace'],
     {'stderr':
      ['CIMError: 3 (CIM_ERR_INVALID_NAMESPACE): Namespace does not exist'
       " in mock repository: 'root/invalidnamespace'", ],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand get with none existentinstancename',
     ['get', 'CIM_Foo.InstanceID="CIM_NOTEXIST"'],
     {'stderr': ["Error: CIMError: 6 (CIM_ERR_NOT_FOUND): Instance not found "
                 "in repository namespace 'root/cimv2'. Path=CIMInstanceName("
                 "classname='CIM_Foo', keybindings=NocaseDict({'InstanceID': "
                 "'CIM_NOTEXIST'}), namespace='root/cimv2', host=None)"],
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
      'test': 'linesnows'},
     None, OK],

    ['Verify instance subcommand create, new instance of CIM_Foo one property',
     ['create', 'CIM_Foo', '-P', 'InstanceID=blah'],
     {'stdout': 'root/cimv2:CIM_Foo.InstanceID="blah"',
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand create, new instance of CIM_Foo one '
     'property and verify yes',
     ['create', 'CIM_Foo', '-P', 'InstanceID=blah', '--verify'],
     {'stdout': ['instance of CIM_Foo {',
                 'InstanceID = "blah";',
                 'root/cimv2:CIM_Foo.InstanceID="blah"',
                 'Execute CreateInstance'],
      'rc': 0,
      'test': 'in '},
     [SIMPLE_MOCK_FILE, MOCK_CONFIRM_Y_FILE], OK],

    ['Verify instance subcommand create, new instance of CIM_Foo one '
     'property and verify no',
     ['create', 'CIM_Foo', '-P', 'InstanceID=blah', '--verify'],
     {'stdout': ['instance of CIM_Foo {',
                 'InstanceID = "blah";',
                 'root/cimv2:CIM_Foo.InstanceID="blah"',
                 'Execute CreateInstance'
                 'Request aborted'],
      'rc': 0,
      'test': 'in '},
     [SIMPLE_MOCK_FILE, MOCK_CONFIRM_N_FILE], OK],

    ['Verify instance subcommand create, new instance of CIM_Foo, '
     'one property, explicit namespace definition',
     ['create', 'CIM_Foo', '-P', 'InstanceID=blah', '-n', 'root/cimv2'],
     {'stdout': "",
      'rc': 0,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    # This test skipped because click stdin broken
    ['Verify create, get, delete works with stdin',
     {'stdin': ['instance create CIM_foo -P InstancID=blah',
                'instance get CIM_Foo=/"blah/"',
                'instance delete CIM_Foo/"blah/"']},
     {'stdout': [''],
      'rc': 0,
      'test': 'regex'},
     None, FAIL],

    ['Verify instance subcommand create, new instance of all_types '
     'with scalar types',
     ['create', 'PyWBEM_AllTypes',
      '-P', 'InstanceID=BunchOfValues',
      '-P', 'scalBool=true', '-P', 'scalUint8=1',
      '-P', 'scalUint16=9', '-P', 'scalSint16=-9',
      '-P', 'scalUint32=999', '-P', 'scalSint32=-999',
      '-P', 'scalSint64=-9999',
      '-P', 'scalUint64=9999',
      '-P', 'scalString="test\"embedded\"quote"',
      '-P', 'scalDateTime=19991224120000.000000+360'],
     {'stdout': 'root/cimv2:PyWBEM_AllTypes.InstanceId="BunchOfValues"',
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand create, new instance of all_types '
     "with array values",
     ['create', 'PyWBEM_AllTypes',
      '-P', 'InstanceID=blah',
      '-P', 'arrayBool=true,false',
      '-P', 'arrayUint8=1,2,3',
      '-P', 'arraySint8=-1,-2,-3',
      '-P', 'arrayUint16=9,19',
      '-P', 'arrayUint32=0,99,999', '-P', 'arraySint32=0,-999,-999',
      '-P', 'arrayUint64=0,999,9999', '-P', 'arraySint64=-9999,0,9999',
      '-P', 'scalString="abc", "def", "jhijk"'],
     {'stdout': 'root/cimv2:PyWBEM_AllTypes.InstanceId="blah"',
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand create, new instance Error in Property Type'
     " with array values",
     ['create', 'PyWBEM_AllTypes', '-P', 'InstanceID=blah',
      '-P', 'arrayBool=8,9',
      '-P', 'arrayUint8=1,2,3',
      '-P', 'arraySint8=-1,-2,-3',
      '-P', 'arrayUint16=9,19',
      '-P', 'arrayUint32=0,99,999', '-P', 'arraySint32=0,-999,-999',
      '-P', 'arrayUint64=0,999,9999', '-P', 'arraySint64=-9999,0,9999',
      '-P', 'scalString="abc", "def", "jhijk"'],
     {'stderr': "Error: Type mismatch property 'arrayBool' between expected "
                "type='boolean', array=True and input value='8,9'. "
                'Exception: Invalid boolean value: "8"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand create, new instance already exists',
     ['create', 'PyWBEM_AllTypes', '-P', 'InstanceID=test_instance'],
     {'stderr': ['Error: CIMClass: "PyWBEM_AllTypes" does not exist in ',
                 'namespace "root/cimv2" in WEB server: FakedWBEMConnection'],
      'rc': 1,
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand create, new instance invalid ns',
     ['create', 'PyWBEM_AllTypes', '-P', 'InstanceID=test_instance', '-n',
      'blah'],
     {'stderr': ["Error: Exception 3", "CIM_ERR_INVALID_NAMESPACE"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify instance subcommand create, new instance invalid class',
     ['create', 'CIM_blah', '-P', 'InstanceID=test_instance'],
     {'stderr': ["Error:", "CIMClass"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],
    # NOTE: Since the instance creation logic is the same for modify and
    # create instance. The error tests in modify also test the error logic.
    # We have not repeated a bunch of those in for the CreateInstance

    #
    #  instance modify subcommand
    #
    ['Verify instance subcommand modify, --help response',
     ['modify', '--help'],
     {'stdout': INST_MODIFY_HELP,
      'rc': 0,
      'test': 'linesnows'},
     None, OK],

    ['Verify instance subcommand modify, single good change',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'scalBool=False'],
     {'stdout': "",
      'rc': 0,
      'test': 'linesnows'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, single good change with verify yes',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'scalBool=False', '--verify'],
     {'stdout': ['instance of PyWBEM_AllTypes {',
                 'scalBool = false;',
                 '};',
                 'Execute ModifyInstance'],
      'rc': 0,
      'test': 'regex'},
     [ALLTYPES_MOCK_FILE, MOCK_CONFIRM_Y_FILE], OK],

    ['Verify instance subcommand modify, single good change with verify no',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'scalBool=False', '--verify'],
     {'stdout': ['instance of PyWBEM_AllTypes {',
                 'scalBool = false;',
                 'Execute ModifyInstance',
                 'Request aborted'],
      'rc': 0,
      'test': 'regex'},
     [ALLTYPES_MOCK_FILE, MOCK_CONFIRM_N_FILE], OK],


    ['Verify instance subcommand modify, single good change, explicit ns',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"', '-n',
      'root/cimv2', '-P', 'scalBool=False'],
     {'stdout': "",
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, single good change, explicit ns',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"', '--namespace',
      'root/cimv2', '--property', 'scalBool=False'],
     {'stdout': "",
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, multiple good change',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'scalBool=False',
      '-P', 'arrayBool=true,false,true',
      '-P', 'arrayUint32=0,99,999, 3', '-P', 'arraySint32=0,-999,-999,9',
      '-P', 'arrayUint64=0,999,9999,3000', '-P', 'arraySint64=-9999,0,9999,4',
      '-P', 'scalString="abc", "def", "jhijk"'],
     {'stdout': "",
      'rc': 0,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    #
    # Instance modify errors
    #
    ['Verify instance subcommand modify, invalid class',
     ['modify', 'PyWBEM_AllTypesxxx.InstanceID="test_instance"',
      '-P', 'scalBool=9'],
     {'stderr': ["CIMClass:", "PyWBEM_AllTypesxxx",
                 "does not exist in WEB server",
                 "FakedUrl"],
      'rc': 1,
      'test': 'regex'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, single property, Type Error bool',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'scalBool=9'],
     {'stderr': "Error: Type mismatch property 'scalBool' between expected "
                "type='boolean', array=False and input value='9'. "
                'Exception: Invalid boolean value: "9"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, single property, Fail modifies key',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'InstanceID=9'],
     {'stderr': 'Error: Server Error modifying instance. Exception: CIMError:'
                " 4 (CIM_ERR_INVALID_PARAMETER): Property 'InstanceID' in "
                "ModifiedInstance not in class 'PyWBEM_AllTypes'",
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, single property, Type Error uint32. '
     'Uses regex because Exception msg different between python 2 and 3',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'scalUint32=Fred'],
     {'stderr': ["Error: Type mismatch property 'scalUint32' between expected ",
                 "type='uint32', array=False and input value='Fred'. ",
                 "Exception: invalid literal for", "with base 10: 'Fred'"],
      'rc': 1,
      'test': 'regex'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, single Property arrayness error',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'scalBool=False,True'],
     {'stderr': "Error: Type mismatch property 'scalBool' between expected "
                "type='boolean', array=False and input value='False,True'. "
                'Exception: Invalid boolean value: "False,True"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, Error value types mismatch with array',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'arrayBool=9,8'],
     {'stderr': "Error: Type mismatch property 'arrayBool' between expected "
                "type='boolean', array=True and input value='9,8'. "
                'Exception: Invalid boolean value: "9"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, Error different value types',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'arrayBool=true,8'],
     {'stderr': "Error: Type mismatch property 'arrayBool' between expected "
                "type='boolean', array=True and input value='true,8'. "
                'Exception: Invalid boolean value: "8"',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, Error integer out of range',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'arrayUint32=99999999999999999999999'],
     {'stderr': "Error: Type mismatch property 'arrayUint32' between expected "
                "type='uint32', array=True and input "
                "value='99999999999999999999999'. "
                "Exception: Integer value 99999999999999999999999 is out of "
                "range for CIM datatype uint32",
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    ['Verify instance subcommand modify, Error property not in class',
     ['modify', 'PyWBEM_AllTypes.InstanceID="test_instance"',
      '-P', 'blah=9'],
     {'stderr': 'Error: Property name "blah" not in class "PyWBEM_AllTypes".',
      'rc': 1,
      'test': 'lines'},
     ALLTYPES_MOCK_FILE, OK],

    # TODO additional modify error tests required

    #
    #  instance delete subcommand
    #
    ['Verify instance subcommand delete, --help response',
     ['delete', '--help'],
     {'stdout': INST_DELETE_HELP,
      'rc': 0,
      'test': 'linesnows'},
     None, OK],

    ['Verify instance subcommand delete, valid delete',
     ['delete', 'CIM_Foo.InstanceID="CIM_Foo1"'],
     {'stdout': '',
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand delete, valid delete, explicit ns',
     ['delete', 'CIM_Foo.InstanceID="CIM_Foo1"', '-n', 'root/cimv2'],
     {'stdout': '',
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand delete, valid delete, explicit ns',
     ['delete', 'CIM_Foo.InstanceID="CIM_Foo1"', '--namespace', 'root/cimv2'],
     {'stdout': '',
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand delete with interactive option',
     ['delete', 'TST_Person', '-i'],
     {'stdout':
      ['root/cimv2:TST_Person.name="Mike"'],
      'rc': 0,
      'test': 'in'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], OK],

    ['Verify instance subcommand delete with interactive option',
     ['delete', 'TST_Person', '--interactive'],
     {'stdout':
      ['root/cimv2:TST_Person.name="Mike"'],
      'rc': 0,
      'test': 'in'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], OK],

    #
    # Delete subcommand error tests
    #
    ['Verify instance subcommand delete, missing instance name',
     ['delete'],
     {'stderr':
      ['Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME', ],
      'rc': 2,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand delete, instance name invalid',
     ['delete', "blah"],
     {'stderr':
      ['Invalid wbem uri', ],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand delete, instance name not in repo',
     ['delete', 'CIM_Foo.InstanceID="xxxxx"', '--namespace', 'root/cimv2'],
     {'stderr':
      ["CIMError", "6", "CIM_ERR_NOT_FOUND"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand delete, namespace not in repo',
     ['delete', 'CIM_Foo.InstanceID=1', '--namespace', 'Argh'],
     {'stderr':
      ["CIMError", "3", "CIM_ERR_INVALID_NAMESPACE"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  instance references subcommand
    #
    ['Verify instance subcommand references, --help response',
     ['references', '--help'],
     {'stdout': INST_REFERENCES_HELP,
      'rc': 0,
      'test': 'linesnows'},
     None, OK],

    ['Verify instance subcommand references, returns instances',
     ['references', 'TST_Person.name="Mike"'],
     {'stdout': REF_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references, returns instances, explicit ns',
     ['references', 'TST_Person.name="Mike"', '-n', 'root/cimv2'],
     {'stdout': REF_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references -o, returns paths',
     ['references', 'TST_Person.name="Mike"', '-o'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"',
                 '//FakedUrl/root/cimv2:TST_MemberOfFamilyCollection.family',
                 '"root/cimv2:TST_FamilyCollection.name=\\"Family2\\"",member',
                 '=\"root/cimv2:TST_Person.name=\\"Mike\\""'],
      'rc': 0,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references -o, returns paths with resultclass '
     'valid returns paths',
     ['references', 'TST_Person.name="Mike"', '-o',
      '--resultclass', 'TST_Lineage'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"', ],
      'rc': 0,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references CIM_Foo with --use-pull-ops yes '
     'and --pull_max_cnt=1',
     {'args': ['references', 'TST_Person.name="Mike"'],
      'global': ['--use-pull-ops', 'yes', '--pull-max-cnt', '1', '--log',
                 'all=stderr']},
     {'stderr': [r'PullInstancesWithPath\(MaxObjectCount=1',
                 r'OpenReferenceInstances\(pull_inst_result_tuple\('
                 'context=',
                 r'TST_MemberOfFamilyCollection',
                 r'TST_Lineage'],
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand reference paths CIM_Foo with --use-pull-ops '
     'yes and --pull_max_cnt=1 and --names_only',
     {'args': ['references', 'TST_Person.name="Mike"', '--names-only'],
      'global': ['--use-pull-ops', 'yes', '--pull-max-cnt', '1', '--log',
                 'all=stderr']},
     {'stderr': [r'PullInstancePaths\(MaxObjectCount=1',
                 r'OpenReferenceInstancePaths\(pull_path_result_tuple\('
                 'context=',
                 r'TST_MemberOfFamilyCollection',
                 r'TST_Lineage'],
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references -o, returns paths with resultclass '
     'valid returns paths sorted',
     ['references', 'TST_Person.name="Mike"', '-o', '-s',
      '--resultclass', 'TST_Lineage'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"', ],
      'rc': 0,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references -o, returns paths with resultclass '
     'short form valid returns paths',
     ['references', 'TST_Person.name="Mike"', '-o',
      '-R', 'TST_Lineage'],
     {'stdout': ['//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"',
                 '//FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"', ],
      'rc': 0,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references -o, returns paths with resultclass '
     'short form valid returns paths',
     ['references', 'TST_Person.name="Mike"', '-o', '--summary',
      '-R', 'TST_Lineage'],
     {'stdout': ['2 CIMInstanceName(s) returned'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],


    ['Verify instance subcommand references -o, returns paths with resultclass '
     'short form valid returns paths',
     {'args': ['references', 'TST_Person.name="Mike"', '-o', '--summary',
               '-R', 'TST_Lineage'],
      'global': ['--output-format', 'table']},
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

    ['Verify instance subcommand references -S, returns paths with resultclass '
     'short form valid returns paths',
     ['references', 'TST_Person.name="Mike"', '-S',
      '-R', 'TST_Lineage'],
     {'stdout': ['2 CIMInstance(s) returned'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references --includequalifiers',
     ['references', 'TST_Person.name="Mike"', '--includequalifiers'],
     {'stdout': REF_INSTS,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references includequalifiers and '
     ' --use-pull-ops no',
     {'args': ['references', 'TST_Person.name="Mike"', '--includequalifiers'],
      'global': ['--use-pull-ops', 'no']},
     {'stdout': REF_INSTS,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],


    ['Verify instance subcommand references -o, returns paths with resultclass '
     'not a real ref returns no paths',
     ['references', 'TST_Person.name="Mike"', '-o',
      '--resultclass', 'TST_Lineagex'],
     {'stdout': [],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references, no instance name',
     ['references'],
     {'stderr': ['Usage: pywbemcli instance references [COMMAND-OPTIONS] '
                 'INSTANCENAME', ],
      'rc': 2,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references, invalid instance name',
     ['references', 'TST_Blah.blah="abc"'],
     {'stdout': "",
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references with interactive option -i',
     ['references', 'TST_Person', '-i'],
     {'stdout':
      ['root/cimv2:TST_Person.name="Mike"',
       'instance of TST_Lineage {',
       'instance of TST_MemberOfFamilyCollection {'],
      'rc': 0,
      'test': 'in'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], OK],

    ['Verify instance subcommand references with interactive option '
     '--interactive',
     ['references', 'TST_Person', '--interactive'],
     {'stdout':
      ['root/cimv2:TST_Person.name="Mike"',
       'instance of TST_Lineage {',
       'instance of TST_MemberOfFamilyCollection {'],
      'rc': 0,
      'test': 'in'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], OK],

    ['Verify instance subcommand references with query.',
     ['references', 'TST_Person.name="Mike"', '--filterquery',
      'InstanceID = 3'],
     {'stdout': REF_INSTS,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand references with query, traditional ops fails',
     {'args': ['references', 'TST_Person.name="Mike"', '--filterquery',
               'InstanceID = 3'],
      'global': ['--use-pull-ops', 'no']},
     {'stderr': ["ValueError:",
                 "References does not support FilterQuery"],
      'rc': 1,
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    # TODO add more invalid references tests

    #
    #  instance associators subcommand
    #
    ['Verify instance subcommand associators, --help response',
     ['associators', '--help'],
     {'stdout': INST_ASSOCIATORS_HELP,
      'rc': 0,
      'test': 'linesnows'},
     None, OK],

    ['Verify instance subcommand associators, returns instances',
     ['associators', 'TST_Person.name="Mike"'],
     {'stdout': ASSOC_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associators, --includequalifiers',
     ['associators', 'TST_Person.name="Mike"', '--includequalifiers'],
     {'stdout': ASSOC_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associators, --includequalifiers wo pull',
     {'global': ['--use-pull-ops', 'no'],
      'args': ['associators', 'TST_Person.name="Mike"', '--includequalifiers']},
     {'stdout': ASSOC_INSTS,
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associators -o, returns data',
     ['associators', 'TST_Person.name="Mike"', '-o'],
     {'stdout': ['', '//FakedUrl/root/cimv2:TST_Person.name="Sofi"',
                 '', '//FakedUrl/root/cimv2:TST_Person.name="Gabi"',
                 '',
                 '//FakedUrl/root/cimv2:TST_FamilyCollection.name="Family2"'],
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associators CIM_Foo with --use-pull-ops yes '
     'and --pull_max_cnt=1',
     {'args': ['associators', 'TST_Person.name="Mike"'],
      'global': ['--use-pull-ops', 'yes', '--pull-max-cnt', '1', '--log',
                 'all=stderr']},
     {'stderr': [r'PullInstancesWithPath\(MaxObjectCount=1',
                 r'OpenAssociatorInstances\(pull_inst_result_tuple\('
                 'context=',
                 r'TST_Person'],
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associator paths CIM_Foo with --use-pull-ops '
     'yes and --pull_max_cnt=1 and --names_only',
     {'args': ['associators', 'TST_Person.name="Mike"', '--names-only'],
      'global': ['--use-pull-ops', 'yes', '--pull-max-cnt', '1', '--log',
                 'all=stderr']},
     {'stderr': [r'PullInstancePaths\(MaxObjectCount=1',
                 r'OpenAssociatorInstancePaths\(pull_path_result_tuple\('
                 'context=',
                 r'TST_Person'],
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],



    # Invalid associators tests

    ['Verify instance subcommand associators, no instance name',
     ['associators'],
     {'stderr': ['Usage: pywbemcli instance associators [COMMAND-OPTIONS] '
                 'INSTANCENAME', ],
      'rc': 2,
      'test': 'in'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associators, invalid instance name',
     ['associators', 'TST_Blah.blah="abc"'],
     {'stdout': '',
      'rc': 0,
      'test': 'lines'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associators with interactive option -i',
     ['associators', 'TST_Person', '-i'],
     {'stdout':
      ['root/cimv2:TST_Person.name="Mike"',
       'instance of TST_Person {',
       'instance of TST_FamilyCollection {'],
      'rc': 0,
      'test': 'in'},
     [ASSOC_MOCK_FILE, MOCK_PROMPT_0_FILE], OK],

    ['Verify instance subcommand associators with query.',
     ['associators', 'TST_Person.name="Mike"', '--filterquery',
      'InstanceID = 3'],
     {'stdout': ASSOC_INSTS,
      'test': 'linesnows'},
     ASSOC_MOCK_FILE, OK],

    ['Verify instance subcommand associators with query, traditional ops',
     {'args': ['associators', 'TST_Person.name="Mike"', '--filterquery',
               'InstanceID = 3'],
      'global': ['--use-pull-ops', 'no']},
     {'stderr': ["ValueError:",
                 "Associators does not support FilterQuery"],
      'rc': 1,
      'test': 'regex'},
     ASSOC_MOCK_FILE, OK],

    # TODO add more associators error tests

    #
    #  instance count subcommand
    #
    ['Verify instance subcommand count, --help response',
     ['count', '--help'],
     {'stdout': INST_COUNT_HELP,
      'rc': 0,
      'test': 'linesnows'},
     None, OK],

    ['Verify instance subcommand count, Return table of instances',
     ['count', 'CIM_*'],
     {'stdout': ['Count of instances per class',
                 '+---------+---------+',
                 '| Class   |   count |',
                 '|---------+---------|',
                 '| CIM_Foo |       3 |',
                 '+---------+---------+', ],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],


    ['Verify instance subcommand count, Return table of instances',
     ['count', 'CIM_*', '--sort'],
     {'stdout': ['Count of instances per class',
                 '+---------+---------+',
                 '| Class   |   count |',
                 '|---------+---------|',
                 '| CIM_Foo |       3 |',
                 '+---------+---------+', ],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify instance subcommand count, --sort. Return table of instances',
     ['count', 'CIM_*'],
     {'stdout': ['Count of instances per class',
                 '+---------+---------+',
                 '| Class   |   count |',
                 '|---------+---------|',
                 '| CIM_Foo |       3 |',
                 '+---------+---------+', ],
      'rc': 0,
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    # TODO add subclass instances to the count test.

    #
    #  instance invokemethod tests
    #

    ['class subcommand invokemethod --help, . ',
     ['invokemethod', '--help'],
     {'stdout': INST_INVOKE_METHOD_HELP,
      'test': 'linesnows'},
     None, OK],

    ['Verify instance subcommand invokemethod',
     ['invokemethod', ':CIM_Foo.InstanceID="CIM_Foo1"', 'Fuzzy'],
     {'stdout': ['ReturnValue=0'],
      'rc': 0,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify instance subcommand invokemethod with param',
     ['invokemethod', ':CIM_Foo.InstanceID="CIM_Foo1"', 'Fuzzy',
      '-p', 'TestInOutParameter="blah"'],
     {'stdout': ["ReturnValue=0"],
      'rc': 0,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify instance subcommand invokemethod fails Invalid Class',
     ['invokemethod', ':CIM_Foox.InstanceID="CIM_Foo1"', 'Fuzzy', '-p',
      'TestInOutParameter="blah"'],
     {'stderr': ["Error: CIMError: 6"],
      'rc': 1,
      'test': 'regex'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    ['Verify instance subcommand invokemethod fails Method not registered',
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
    #  instance query subcommand. We have not implemented this command
    #
    ['Verify instance subcommand query, --help response',
     ['query', '--help'],
     {'stdout': INST_QUERY_HELP,
      'rc': 0,
      'test': 'linesnows'},
     None, OK],

    ['Verify instance subcommand query execution. Returns error becasue '
     'mock does not support query',
     ['query', 'Select blah from blah'],
     {'stderr': ['Error: CIMError: 14 (CIM_ERR_QUERY_LANGUAGE_NOT_SUPPORTED): '
                 "FilterQueryLanguage 'DMTF:CQL' not supported"],
      'rc': 1,
      'test': 'in'},
     [SIMPLE_MOCK_FILE], OK],
]


class TestSubcmd(CLITestsBase):
    """
    Test all of the class subcommand variations.
    """
    subcmd = 'instance'
    # mock_mof_file = 'simple_mock_model.mof'

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition", TEST_CASES)
    def test_execute_pywbemcli(self, desc, inputs, exp_response, mock,
                               condition):
        """
        Execute pybemcli with the defined input and test output.
        """
        self.subcmd_test(desc, self.subcmd, inputs, exp_response,
                         mock, condition)
