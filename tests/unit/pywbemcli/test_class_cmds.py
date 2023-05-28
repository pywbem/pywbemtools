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

import sys
import os
from packaging.version import parse as parse_version
import pytest
from pywbem import __version__ as pywbem_version

from .cli_test_extensions import CLITestsBase, PYWBEM_0, \
    FAKEURL_STR
from .common_options_help_lines import CMD_OPTION_NAMES_ONLY_HELP_LINE, \
    CMD_OPTION_HELP_HELP_LINE, CMD_OPTION_SUMMARY_HELP_LINE, \
    CMD_OPTION_NAMESPACE_HELP_LINE, CMD_OPTION_PROPERTYLIST_HELP_LINE, \
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE, \
    CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE, CMD_OPTION_NO_QUALIFIERS_HELP_LINE, \
    CMD_OPTION_MULTIPLE_NAMESPACE_ALL_HELP_LINE, \
    CMD_OPTION_MULTIPLE_NAMESPACE_DFLT_CONN_HELP_LINE, \
    CMD_OPTION_ASSOCIATION_FILTER_HELP_LINE, \
    CMD_OPTION_INDICATION_FILTER_HELP_LINE, \
    CMD_OPTION_EXPERIMENTAL_FILTER_HELP_LINE, \
    CMD_OPTION_DEPRECATED_FILTER_HELP_LINE, \
    CMD_OPTION_SINCE_FILTER_HELP_LINE, \
    CMD_OPTION_SCHEMA_FILTER_HELP_LINE, \
    CMD_OPTION_SUBCLASSOF_FILTER_HELP_LINE, \
    CMD_OPTION_LEAFCLASSES_FILTER_HELP_LINE

# pylint: disable=use-dict-literal

_PYWBEM_VERSION = parse_version(pywbem_version)
# pywbem 1.0.0 or later
PYWBEM_1_0_0 = _PYWBEM_VERSION.release >= (1, 0, 0)

# Create variable that is True if python ge version 3.8.  This python version
# was the first to impose ordering on XML attributes. Without ordering
# XML tests against XML data returned from pywbemcli can fail. See issue #1173
PYTHON_GE_38 = sys.version_info > (3, 8)

# Mock scripts with setup() function are supported
MOCK_SETUP_SUPPORTED = sys.version_info >= (3, 6)

TEST_DIR = os.path.dirname(__file__)

# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'

INVOKE_METHOD_MOCK_FILE_0 = 'simple_mock_invokemethod_v0.py'
INVOKE_METHOD_MOCK_FILE_1 = 'simple_mock_invokemethod_v1old.py'
INVOKE_METHOD_MOCK_FILE = INVOKE_METHOD_MOCK_FILE_0 if PYWBEM_0 else \
    INVOKE_METHOD_MOCK_FILE_1

SIMPLE_ASSOC_MOCK_FILE = 'simple_assoc_mock_model.mof'
QUALIFIER_FILTER_MODEL = 'qualifier_filter_model.mof'

TREE_TEST_MOCK_FILE = 'tree_test_mock_model.mof'

SIMPLE_INTEROP_MOCK_FILE = 'simple_interop_mock_script.py'

THREE_NS_MOCK_FILE = 'simple_three_ns_mock_script.py'


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
    'enumerate     List top classes or subclasses of a class in namespace(s).',
    'get           Get a class.',
    'delete        Delete a class.',
    'find          List the classes with matching class names on the server.',
    'get           Get a class.',
    'invokemethod  Invoke a method on a class.',
    'associators   List the classes associated with a class.',
    'references    List the classes referencing a class.',
    'find          List the classes with matching class names on the server.',
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
    CMD_OPTION_MULTIPLE_NAMESPACE_DFLT_CONN_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_DELETE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class delete CLASSNAME '
    '[COMMAND-OPTIONS]',
    'Delete a class.',
    '--include-instances Delete any instances of the class as well.',
    CMD_OPTION_NAMESPACE_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_ENUMERATE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class enumerate CLASSNAME '
    '[COMMAND-OPTIONS]',
    'List top classes or subclasses of a class in namespace(s).',
    '--di, --deep-inheritance Include the complete subclass hierarchy',
    CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE,
    CMD_OPTION_NO_QUALIFIERS_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_NAMES_ONLY_HELP_LINE,
    CMD_OPTION_MULTIPLE_NAMESPACE_DFLT_CONN_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    # NOTE: The FILTER options are a group. Define all of them.
    CMD_OPTION_ASSOCIATION_FILTER_HELP_LINE,
    CMD_OPTION_INDICATION_FILTER_HELP_LINE,
    CMD_OPTION_EXPERIMENTAL_FILTER_HELP_LINE,
    CMD_OPTION_DEPRECATED_FILTER_HELP_LINE,
    CMD_OPTION_SINCE_FILTER_HELP_LINE,
    CMD_OPTION_SCHEMA_FILTER_HELP_LINE,
    CMD_OPTION_SUBCLASSOF_FILTER_HELP_LINE,
    CMD_OPTION_LEAFCLASSES_FILTER_HELP_LINE,

    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_FIND_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class find CLASSNAME-GLOB '
    '[COMMAND-OPTIONS]',
    'List the classes with matching class names on the server.',
    '-s, --sort  Sort by namespace. Default is to sort by',
    CMD_OPTION_MULTIPLE_NAMESPACE_ALL_HELP_LINE,
    # FILTER OPTIONS
    CMD_OPTION_ASSOCIATION_FILTER_HELP_LINE,
    CMD_OPTION_INDICATION_FILTER_HELP_LINE,
    CMD_OPTION_EXPERIMENTAL_FILTER_HELP_LINE,
    CMD_OPTION_DEPRECATED_FILTER_HELP_LINE,
    CMD_OPTION_SINCE_FILTER_HELP_LINE,
    CMD_OPTION_SCHEMA_FILTER_HELP_LINE,
    CMD_OPTION_SUBCLASSOF_FILTER_HELP_LINE,
    CMD_OPTION_LEAFCLASSES_FILTER_HELP_LINE,

    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_GET_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class get CLASSNAME [COMMAND-OPTIONS]',
    'Get a class.',
    CMD_OPTION_LOCAL_ONLY_CLASS_HELP_LINE,
    CMD_OPTION_NO_QUALIFIERS_HELP_LINE,
    CMD_OPTION_INCLUDE_CLASSORIGIN_HELP_LINE,
    CMD_OPTION_PROPERTYLIST_HELP_LINE,
    CMD_OPTION_MULTIPLE_NAMESPACE_DFLT_CONN_HELP_LINE,
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
    CMD_OPTION_MULTIPLE_NAMESPACE_DFLT_CONN_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

CLASS_TREE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] class tree CLASSNAME [COMMAND-OPTIONS]',
    'Show the subclass or superclass hierarchy for a class.',
    '-s, --superclasses Show the superclass hierarchy.',
    ' -d, --detail               Show details about the class: the Version',
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

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

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
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();
};

"""  # noqa: E501
# pylint: enable=line-too-long

CIMFOO_SUB_SUB_NO_QUALS = """
class CIM_Foo_sub_sub : CIM_Foo_sub {

   string cimfoo_sub_sub;

   string cimfoo_sub;

   string InstanceID;

   uint32 IntegerProp;

   string cimfoo_emb3;

   uint32 Method1(
      string OutputParam2);

   uint32 Fuzzy(
      string TestInOutParameter,
      CIM_FooRef1 REF TestRef,
      string OutputParam,
      uint32 OutputRtnValue);

   uint32 FuzzyStatic(
      string TestInOutParameter,
      CIM_Foo REF TestRef,
      string OutputParam,
      uint32 OutputRtnValue,
      string cimfoo_emb1);

   string DeleteNothing();
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

# pylint: disable=line-too-long
# This output only valid for python versin ge 3.8
ASSOCIATORS_CLASS_XML_GE_38 = """<CLASSPATH>
    <NAMESPACEPATH>
        <HOST>FakedUrl:5988</HOST>
        <LOCALNAMESPACEPATH>
            <NAMESPACE NAME="root"/>
            <NAMESPACE NAME="cimv2"/>
        </LOCALNAMESPACEPATH>
    </NAMESPACEPATH>
    <CLASSNAME NAME="TST_Person"/>
</CLASSPATH>

<CLASS NAME="TST_Person">
    <PROPERTY NAME="name" TYPE="string" PROPAGATED="false">
        <QUALIFIER NAME="Key" TYPE="boolean" PROPAGATED="false" OVERRIDABLE="false" TOSUBCLASS="true">
            <VALUE>TRUE</VALUE>
        </QUALIFIER>
        <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="false" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE>This is key prop</VALUE>
        </QUALIFIER>
    </PROPERTY>
    <PROPERTY NAME="extraProperty" TYPE="string" PROPAGATED="false">
        <VALUE>defaultvalue</VALUE>
    </PROPERTY>
    <PROPERTY NAME="gender" TYPE="uint16" PROPAGATED="false">
        <QUALIFIER NAME="ValueMap" TYPE="string" PROPAGATED="false" OVERRIDABLE="true" TOSUBCLASS="true">
            <VALUE.ARRAY>
                <VALUE>1</VALUE>
                <VALUE>2</VALUE>
            </VALUE.ARRAY>
        </QUALIFIER>
        <QUALIFIER NAME="Values" TYPE="string" PROPAGATED="false" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE.ARRAY>
                <VALUE>female</VALUE>
                <VALUE>male</VALUE>
            </VALUE.ARRAY>
        </QUALIFIER>
    </PROPERTY>
    <PROPERTY.ARRAY NAME="likes" TYPE="uint16" PROPAGATED="false">
        <QUALIFIER NAME="ValueMap" TYPE="string" PROPAGATED="false" OVERRIDABLE="true" TOSUBCLASS="true">
            <VALUE.ARRAY>
                <VALUE>1</VALUE>
                <VALUE>2</VALUE>
            </VALUE.ARRAY>
        </QUALIFIER>
        <QUALIFIER NAME="Values" TYPE="string" PROPAGATED="false" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE.ARRAY>
                <VALUE>books</VALUE>
                <VALUE>movies</VALUE>
            </VALUE.ARRAY>
        </QUALIFIER>
    </PROPERTY.ARRAY>
</CLASS>

"""  # noqa: E501

# This output only for python version ge 3.8. Contains qualifier output
CIMFOO_SUB_SUB_WITH_QUALS_XML = """<CLASS NAME="CIM_Foo_sub_sub" SUPERCLASS="CIM_Foo_sub">
    <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="false" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
        <VALUE>Subclass of CIM_Foo_sub</VALUE>
    </QUALIFIER>
    <PROPERTY NAME="cimfoo_sub_sub" TYPE="string" PROPAGATED="false"/>
    <PROPERTY NAME="cimfoo_sub" TYPE="string" PROPAGATED="true"/>
    <PROPERTY NAME="InstanceID" TYPE="string" PROPAGATED="true">
        <QUALIFIER NAME="Key" TYPE="boolean" PROPAGATED="true" OVERRIDABLE="false" TOSUBCLASS="true">
            <VALUE>TRUE</VALUE>
        </QUALIFIER>
        <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="true" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE>This is key property.</VALUE>
        </QUALIFIER>
    </PROPERTY>
    <PROPERTY NAME="IntegerProp" TYPE="uint32" PROPAGATED="true">
        <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="true" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE>This is Uint32 property.</VALUE>
        </QUALIFIER>
    </PROPERTY>
    <PROPERTY NAME="cimfoo_emb3" TYPE="string" PROPAGATED="true">
        <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="true" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE>Embedded instance property</VALUE>
        </QUALIFIER>
        <QUALIFIER NAME="EmbeddedInstance" TYPE="string" PROPAGATED="true" OVERRIDABLE="true" TOSUBCLASS="true">
            <VALUE>CIM_FooEmb3</VALUE>
        </QUALIFIER>
    </PROPERTY>
    <METHOD NAME="Method1" TYPE="uint32" PROPAGATED="false">
        <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="false" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE>Sample method with input and output parameters</VALUE>
        </QUALIFIER>
        <PARAMETER NAME="OutputParam2" TYPE="string">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>FALSE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="OUT" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Response param 2</VALUE>
            </QUALIFIER>
        </PARAMETER>
    </METHOD>
    <METHOD NAME="Fuzzy" TYPE="uint32" PROPAGATED="true">
        <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="true" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE>Method with in and out parameters</VALUE>
        </QUALIFIER>
        <PARAMETER NAME="TestInOutParameter" TYPE="string">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="OUT" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Define data to be returned in output parameter</VALUE>
            </QUALIFIER>
        </PARAMETER>
        <PARAMETER.REFERENCE NAME="TestRef" REFERENCECLASS="CIM_FooRef1">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="OUT" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Test of ref in/out parameter</VALUE>
            </QUALIFIER>
        </PARAMETER.REFERENCE>
        <PARAMETER NAME="OutputParam" TYPE="string">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>FALSE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="OUT" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Rtns method name if exists on input</VALUE>
            </QUALIFIER>
        </PARAMETER>
        <PARAMETER NAME="OutputRtnValue" TYPE="uint32">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Defines return value if provided.</VALUE>
            </QUALIFIER>
        </PARAMETER>
    </METHOD>
    <METHOD NAME="FuzzyStatic" TYPE="uint32" PROPAGATED="true">
        <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="true" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE>Static method with in and out parameters</VALUE>
        </QUALIFIER>
        <QUALIFIER NAME="Static" TYPE="boolean" PROPAGATED="true" OVERRIDABLE="false" TOSUBCLASS="true">
            <VALUE>TRUE</VALUE>
        </QUALIFIER>
        <PARAMETER NAME="TestInOutParameter" TYPE="string">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="OUT" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Define data to be returned in output parameter</VALUE>
            </QUALIFIER>
        </PARAMETER>
        <PARAMETER.REFERENCE NAME="TestRef" REFERENCECLASS="CIM_Foo">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="OUT" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Test of ref in/out parameter</VALUE>
            </QUALIFIER>
        </PARAMETER.REFERENCE>
        <PARAMETER NAME="OutputParam" TYPE="string">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>FALSE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="OUT" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Rtns method name if exists on input</VALUE>
            </QUALIFIER>
        </PARAMETER>
        <PARAMETER NAME="OutputRtnValue" TYPE="uint32">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Defines return value if provided.</VALUE>
            </QUALIFIER>
        </PARAMETER>
        <PARAMETER NAME="cimfoo_emb1" TYPE="string">
            <QUALIFIER NAME="IN" TYPE="boolean" OVERRIDABLE="false" TOSUBCLASS="true">
                <VALUE>TRUE</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="Description" TYPE="string" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
                <VALUE>Embedded instance parameter</VALUE>
            </QUALIFIER>
            <QUALIFIER NAME="EmbeddedInstance" TYPE="string">
                <VALUE>CIM_FooEmb1</VALUE>
            </QUALIFIER>
        </PARAMETER>
    </METHOD>
    <METHOD NAME="DeleteNothing" TYPE="string" PROPAGATED="true">
        <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="true" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
            <VALUE>Method with no parameters but embedded instance return</VALUE>
        </QUALIFIER>
        <QUALIFIER NAME="EmbeddedInstance" TYPE="string" PROPAGATED="true" OVERRIDABLE="true" TOSUBCLASS="true">
            <VALUE>CIM_FooEmb2</VALUE>
        </QUALIFIER>
    </METHOD>
</CLASS>
"""  # noqa: E501

CIMFOO_SUB_SUB_NO_QUALS_XML = """<CLASS NAME="CIM_Foo_sub_sub" SUPERCLASS="CIM_Foo_sub">
    <PROPERTY NAME="cimfoo_sub_sub" TYPE="string" PROPAGATED="false"/>
    <PROPERTY NAME="cimfoo_sub" TYPE="string" PROPAGATED="true"/>
    <PROPERTY NAME="InstanceID" TYPE="string" PROPAGATED="true"/>
    <PROPERTY NAME="IntegerProp" TYPE="uint32" PROPAGATED="true"/>
    <PROPERTY NAME="cimfoo_emb3" TYPE="string" PROPAGATED="true"/>
    <METHOD NAME="Method1" TYPE="uint32" PROPAGATED="false">
        <PARAMETER NAME="OutputParam2" TYPE="string"/>
    </METHOD>
    <METHOD NAME="Fuzzy" TYPE="uint32" PROPAGATED="true">
        <PARAMETER NAME="TestInOutParameter" TYPE="string"/>
        <PARAMETER.REFERENCE NAME="TestRef" REFERENCECLASS="CIM_FooRef1"/>
        <PARAMETER NAME="OutputParam" TYPE="string"/>
        <PARAMETER NAME="OutputRtnValue" TYPE="uint32"/>
    </METHOD>
    <METHOD NAME="FuzzyStatic" TYPE="uint32" PROPAGATED="true">
        <PARAMETER NAME="TestInOutParameter" TYPE="string"/>
        <PARAMETER.REFERENCE NAME="TestRef" REFERENCECLASS="CIM_Foo"/>
        <PARAMETER NAME="OutputParam" TYPE="string"/>
        <PARAMETER NAME="OutputRtnValue" TYPE="uint32"/>
        <PARAMETER NAME="cimfoo_emb1" TYPE="string"/>
    </METHOD>
    <METHOD NAME="DeleteNothing" TYPE="string" PROPAGATED="true"/>
</CLASS>
"""  # noqa E501
# pylint: enable=line-too-long

ENUMERATE_CLASS_2_NAMESPACE = """
#pragma namespace ("root/cimv2")
   [Description ( "Subclass of CIM_Foo" )]
class CIM_Foo_sub : CIM_Foo {

   string cimfoo_sub;

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();

};

#pragma namespace ("root/cimv2")
class CIM_Foo_sub2 : CIM_Foo {

   string cimfoo_sub2;

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();

};

#pragma namespace ("root/cimv3")
   [Description ( "Subclass of CIM_Foo" )]
class CIM_Foo_sub : CIM_Foo {

   string cimfoo_sub;

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();

};

#pragma namespace ("root/cimv3")
class CIM_Foo_sub2 : CIM_Foo {

   string cimfoo_sub2;

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();
};
"""

ENUMERATE_CLASS_2_NAMESPACE_OBJECT_ORDER = """#pragma namespace ("root/cimv2")
   [Description ( "Subclass of CIM_Foo" )]
class CIM_Foo_sub : CIM_Foo {

   string cimfoo_sub;

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();

};

#pragma namespace ("root/cimv3")
   [Description ( "Subclass of CIM_Foo" )]
class CIM_Foo_sub : CIM_Foo {

   string cimfoo_sub;

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();

};

#pragma namespace ("root/cimv2")
class CIM_Foo_sub2 : CIM_Foo {

   string cimfoo_sub2;

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();

};

#pragma namespace ("root/cimv3")
class CIM_Foo_sub2 : CIM_Foo {

   string cimfoo_sub2;

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();

};

"""

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
| CIM_BaseEmb  |
| CIM_BaseRef  |
| CIM_Foo      |
| CIM_FooAssoc |
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

    ['Verify class command enumerate CIM_Foo summary default output format',
     ['enumerate', 'CIM_Foo', '-s'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo summary, default output format',
     ['enumerate', 'CIM_Foo', '--summary'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate CIM_Foo summary table output',
     {'args': ['enumerate', 'CIM_Foo', '--summary'],
      'general': ['--output-format', 'table']},
     {'stdout': ["""Summary of CIMClass(s) returned
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
     {'stdout': ["CIMClass(classname='CIM_BaseEmb', ...)",
                 "CIMClass(classname='CIM_BaseRef', ...)",
                 "CIMClass(classname='CIM_Foo', ...)",
                 "CIMClass(classname='CIM_FooAssoc', ...)"],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate with xml output format).',
     {'args': ['enumerate'],
      'general': ['--output-format', 'xml']},
     {'stdout': ['<CLASS( | .+ )NAME="CIM_Foo">',
                 '<PROPERTY( | .+ )NAME="InstanceID"',
                 '<PROPERTY( | .+ )NAME="IntegerProp"',
                 '<METHOD( | .+ )NAME="DeleteNothing"'],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    # Test output compare of all components but only python v 3.8*
    ['Verify class command enumerate CIM_Foo with qualifiers, xml',
     {'args': ['enumerate', 'CIM_Foo_sub'],
      'general': ['--output-format', 'xml']},
     {'stdout': CIMFOO_SUB_SUB_WITH_QUALS_XML,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, PYTHON_GE_38],  # issue 1173. Only good for py 3.8+

    ['Verify class command enumerate CIM_Foo with --no qualifiers, xml',
     {'args': ['enumerate', 'CIM_Foo_sub', '--no-qualifiers'],
      'general': ['--output-format', 'xml']},
     {'stdout': CIMFOO_SUB_SUB_NO_QUALS_XML,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, PYTHON_GE_38],  # issue 1173, Property attribute ordering

    ['Verify class command enumerate  --di --no --namespace',
     ['enumerate', '--di', '--no', '-n', 'interop'],
     {'stdout': ['CIM_Namespace', 'CIM_ObjectManager'],
      'test': 'innows'},
     SIMPLE_INTEROP_MOCK_FILE, OK],

    #
    # Enumerate commands with the filter options
    #

    ['Verify class command enumerate with --association filter.',
     ['enumerate', '--association', '--names-only'],
     {'stdout': ['TST_Lineage', 'TST_MemberOfFamilyCollection'],
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command enumerate with --association filter --summary.',
     ['enumerate', '--association', '--summary'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command enumerate with --association filter.',
     ['enumerate', '--association', '--names-only'],
     {'stdout': ['TST_Lineage', 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionDep',
                 'TST_MemberOfFamilyCollectionExp'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --association filter --summary.',
     ['enumerate', '--association', '--summary'],
     {'stdout': ['4 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

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
                 'string cimfoo_emb3;',
                 'uint32 Fuzzy(',
                 'string TestInOutParameter,',
                 'CIM_FooRef1 REF TestRef,',
                 'string OutputParam,',
                 'uint32 OutputRtnValue);',
                 'uint32 FuzzyStatic(',
                 'string TestInOutParameter,',
                 'CIM_Foo REF TestRef,',
                 'string OutputParam,',
                 'uint32 OutputRtnValue,',
                 'string cimfoo_emb1);',
                 'string DeleteNothing();',
                 '};'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate with --no-association filter, simple mod.',
     ['enumerate', '--no-association', '--names-only'],
     {'stdout': ['TST_FamilyCollection', 'TST_Person'],
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command enumerate with --no-association, --summary.',
     ['enumerate', '--no-association', '--summary'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'innows'},
     SIMPLE_ASSOC_MOCK_FILE, OK],

    ['Verify class command enumerate with --no-association filter qual filt.',
     ['enumerate', '--no-association', '--names-only'],
     {'stdout': ['BLA_Person', 'EXP_TestExperimental1',
                 'EXP_TestExperimental2', 'EXP_TestExperimental3',
                 'EXP_TestExperimental4', 'TST_FamilyCollection',
                 'TST_Indication', 'TST_IndicationDeprecated',
                 'TST_IndicationExperimental', 'TST_Person'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-association, --summary.',
     ['enumerate', '--no-association', '--summary'],
     {'stdout': ['10 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --indication filter.',
     ['enumerate', '--indication', '--names-only'],
     {'stdout': ['TST_Indication', 'TST_IndicationDeprecated',
                 'TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --indication filter --summary.',
     ['enumerate', '--indication', '--summary'],
     {'stdout': ['3 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-indication filter.',
     ['enumerate', '--no-indication', '--names-only'],
     {'stdout': ['BLA_Person', 'EXP_TestExperimental1',
                 'EXP_TestExperimental2', 'EXP_TestExperimental3',
                 'EXP_TestExperimental4', 'TST_FamilyCollection',
                 'TST_FamilyCollection',
                 'TST_Lineage',
                 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionExp',
                 'TST_Person'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-indication filter, --summary.',
     ['enumerate', '--no-indication', '--summary'],
     {'stdout': ['11 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimentat filter.',
     ['enumerate', '--experimental', '--names-only'],
     {'stdout': ['EXP_TestExperimental1', ' EXP_TestExperimental2',
                 'EXP_TestExperimental3', 'EXP_TestExperimental4',
                 'TST_IndicationExperimental',
                 'TST_MemberOfFamilyCollectionExp'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimentat filter -- summary.',
     ['enumerate', '--experimental', '--summary'],
     {'stdout': ['6 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-experimental filter.',
     ['enumerate', '--no-experimental', '--names-only'],
     {'stdout': ['BLA_Person',
                 'TST_FamilyCollection',
                 'TST_Indication',
                 'TST_IndicationDeprecated',
                 'TST_Lineage',
                 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionDep',
                 'TST_Person'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-experimental, --summary.',
     ['enumerate', '--no-experimental', '--summary'],
     {'stdout': ['8 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimental, --association.',
     ['enumerate', '--experimental', '--association', '--names-only'],
     {'stdout': ['EXP_TestExperimental1',
                 'EXP_TestExperimental2',
                 'EXP_TestExperimental3',
                 'EXP_TestExperimental4',
                 'TST_IndicationExperimental',
                 'TST_MemberOfFamilyCollectionExp'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimental, --association, '
     '--summary',
     ['enumerate', '--experimental', '--association', '--summary'],
     {'stdout': ['6 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimental , --no-association.',
     ['enumerate', '--experimental', '--no-association', '--names-only'],
     {'stdout': ['EXP_TestExperimental1', 'EXP_TestExperimental2',
                 'EXP_TestExperimental3', 'EXP_TestExperimental4',
                 'TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --indication and --experimental.',
     ['enumerate', '--experimental', '--indication', '--names-only'],
     {'stdout': ['TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --indication, --no-experimental.',
     ['enumerate', '--no-experimental', '--indication', '--names-only'],
     {'stdout': ['TST_Indication', 'TST_IndicationDeprecated'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-indication, --no-experimental, '
     '--no-association',
     ['enumerate', '--no-experimental', '--no-indication', '--no-association',
      '--names-only'],
     {'stdout': ['BLA_Person',
                 'TST_FamilyCollection',
                 'TST_Person'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --deprecated, --no-association.',
     ['enumerate', '--deprecated', '--no-association', '--names-only'],
     {'stdout': ['TST_IndicationDeprecated',
                 'TST_MemberOfFamilyCollectionDep'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --deprecated, --no-association, '
     '--summary',
     ['enumerate', '--deprecated', '--no-association', '--summary'],
     {'stdout': ['2 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-deprecated, --association',
     ['enumerate', '--no-deprecated', '--association', '--names-only'],
     {'stdout': ['BLA_Person', 'EXP_TestExperimental1',
                 'EXP_TestExperimental2', 'EXP_TestExperimental3',
                 'EXP_TestExperimental4', 'TST_FamilyCollection',
                 'TST_Indication', 'TST_IndicationExperimental',
                 'TST_Lineage', 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionExp', 'TST_Person'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --no-deprecated, --no-association'
     '--summary',
     ['enumerate', '--no-deprecated', '--association', '--summary'],
     {'stdout': ['12 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimental, --since 2.42.0.',
     ['enumerate', '--experimental', '--since', '2.42.0', '--names-only'],
     {'stdout': ['TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimental and --since 2.42.0'
     '--summary',
     ['enumerate', '--experimental', '--since', '2.42.0', '--summary'],
     {'stdout': ['3 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimental and --since 2.45.0.',
     ['enumerate', '--experimental', '--since', '2.45.0', '--names-only'],
     {'stdout': [],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --experimental and --since 2.45.x.',
     ['enumerate', '--experimental', '--since', '2.45.x', '--names-only'],
     {'stderr': ['--since option value invalid. ',
                 'Must contain 3 integer elements',
                 '2.45.x'],
      'rc': 1,
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --indication and --since 2.45.',
     ['enumerate', '--experimental', '--since', '2.45', '--names-only'],
     {'stderr': ['Version value must contain 3 integer elements (int.int.int)',
                 '2.45'],
      'rc': 1,
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "TST".',
     ['enumerate', '--schema', 'TST', '--names-only'],
     {'stdout': ['TST_FamilyCollection', 'TST_Indication',
                 'TST_IndicationDeprecated', 'TST_IndicationExperimental',
                 'TST_Lineage', 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionDep',
                 'TST_MemberOfFamilyCollectionExp', 'TST_Person', ],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "BLA".',
     ['enumerate', '--schema', 'BLA', '--names-only'],
     {'stdout': ['BLA_Person', ],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "EXP".',
     ['enumerate', '--schema', 'EXP', '--names-only'],
     {'stdout': ['EXP_TestExperimental1', 'EXP_TestExperimental2',
                 'EXP_TestExperimental3', 'EXP_TestExperimental4'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "EXP" --summary',
     ['enumerate', '--schema', 'EXP', '--summary'],
     {'stdout': ['4 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "EXP" and --experimental.',
     ['enumerate', '--schema', 'EXP', '--experimental', '--names-only'],
     {'stdout': ['EXP_TestExperimental1', 'EXP_TestExperimental2',
                 'EXP_TestExperimental3', 'EXP_TestExperimental4'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "EXP" and --experimental.',
     ['enumerate', '--schema', 'EXP', '--experimental', '--summary'],
     {'stdout': ['4 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "EXP",--experimental, '
     '--summary.',
     ['enumerate', '--schema', 'EXP', '--experimental', '--summary'],
     {'stdout': ['4 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "EXP" , --no-experimental.',
     ['enumerate', '--schema', 'EXP', '--no-experimental', '--names-only'],
     {'stdout': [],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "EXP" , --no-experimental '
     '--summary',
     ['enumerate', '--schema', 'EXP', '--no-experimental', '--summary'],
     {'stdout': ['0 objects returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --schema "NOT_EXIST".',
     ['enumerate', '--schema', 'NOT_EXIST', '--names-only'],
     {'stdout': [],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --subclass-of TST_Person.',
     ['enumerate', '--subclass-of', 'TST_Person', '--di', '--names-only'],
     {'stdout': ['TST_PersonClsDep', 'TST_PersonDep',
                 'TST_PersonExp', 'TST_PersonExpProperty',
                 'TST_PersonPropDep', 'TST_PersonSub'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --subclass-of TST_Person --summary.',
     ['enumerate', '--subclass-of', 'TST_Person', '--di', '--summary'],
     {'stdout': ['6 CIMClass(s) returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --subclass-of TST_Person '
     '-- association--summary .',
     ['enumerate', '--association', '--subclass-of', 'TST_Person', '--di',
      '--summary'],
     {'stdout': ['0 objects returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --subclass-of TST_PersonDep.',
     ['enumerate', '--subclass-of', 'TST_PersonDep', '--di', '--names-only'],
     {'stdout': [],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --subclass-of TST_PersonDep '
     '--summary.',
     ['enumerate', '--subclass-of', 'TST_PersonDep', '--di', '--summary'],
     {'stdout': ['0 objects returned'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --subclass-of NOT_EXIST excepts.',
     ['enumerate', '--subclass-of', 'NOT_EXIST', '--names-only'],
     {'stderr': ['Classname NOT_EXIST for "subclass-of" not found'],
      'rc': 1,
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
     {'stderr': ['CIM_ERR_INVALID_CLASS'],
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

    ['Verify class command enumerate invalid namespace.',
     ['enumerate', '-n', 'blah'],
     {'stderr': ["namespace:blah", "CIMError:CIM_ERR_INVALID_NAMESPACE",
                 "Description:Namespace does not exist in CIM repository:",
                 " 'blah'"],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate non-existent class).',
     ['enumerate', 'InvalidClassname'],
     {'stderr': ["namespace:root/cimv2", "CIM_ERR_INVALID_CLASS",
                 "Description:The class 'InvalidClassname' defined by "
                 "'ClassName' parameter does not exist in namespace "],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command enumerate non-existent svr. fails).',
     {'args': ['enumerate'],
      'general': ['--server', 'http://NotAValidServer']},
     {'stderr': ["Error: ConnectionError:"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

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
                 '   string cimfoo_emb3;',
                 '',
                 '   uint32 Fuzzy(',
                 '      string TestInOutParameter,',
                 '      CIM_FooRef1 REF TestRef,',
                 '      string OutputParam,',
                 '      uint32 OutputRtnValue);',
                 '',
                 '   uint32 FuzzyStatic(',
                 '      string TestInOutParameter,',
                 '      CIM_Foo REF TestRef,',
                 '      string OutputParam,',
                 '      uint32 OutputRtnValue,',
                 '      string cimfoo_emb1);',
                 '',
                 '   string DeleteNothing();',
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
                 '   string cimfoo_emb3;',
                 '',
                 '   uint32 Fuzzy(',
                 '      string TestInOutParameter,',
                 '      CIM_FooRef1 REF TestRef,',
                 '      string OutputParam,',
                 '      uint32 OutputRtnValue);',
                 '',
                 '   uint32 FuzzyStatic(',
                 '      string TestInOutParameter,',
                 '      CIM_Foo REF TestRef,',
                 '      string OutputParam,',
                 '      uint32 OutputRtnValue,',
                 '      string cimfoo_emb1);',
                 '',
                 '   string DeleteNothing();',
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
                 '      CIM_FooRef1 REF TestRef,',
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
                 '      uint32 OutputRtnValue,',
                 '         [IN ( true ),',
                 '          Description ( "Embedded instance parameter" ),',
                 '          EmbeddedInstance ( "CIM_FooEmb1" )]',
                 '      string cimfoo_emb1);',
                 '',
                 '      [Description ( "Method with no parameters but embedded instance return" ),',  # noqa: E501
                 '       EmbeddedInstance ( "CIM_FooEmb2" )]',
                 '   string DeleteNothing();',
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
                 '      CIM_FooRef1 REF TestRef,',
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
                 '      uint32 OutputRtnValue,',
                 '         [IN ( true ),',
                 '          Description ( "Embedded instance parameter" ),',
                 '          EmbeddedInstance ( "CIM_FooEmb1" )]',
                 '      string cimfoo_emb1);',
                 '',
                 '      [Description ( "Method with no parameters but embedded instance return" ),',  # noqa: E501
                 '       EmbeddedInstance ( "CIM_FooEmb2" )]',
                 '   string DeleteNothing();',
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

    ['Verify class command get with xml output format).',
     {'args': ['get', 'CIM_Foo'],
      'general': ['--output-format', 'xml']},
     {'stdout': ['<CLASS( | .+ )NAME="CIM_Foo">',
                 '<PROPERTY( | .+ )NAME="InstanceID"',
                 '<PROPERTY( | .+ )NAME="IntegerProp"',
                 '<METHOD( | .+ )NAME="DeleteNothing"'],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    # pylint: disable=line-too-long
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
                 '      CIM_FooRef1 REF TestRef,',
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
                 '      uint32 OutputRtnValue,',
                 '         [IN ( true ),',
                 '          Description ( "Embedded instance parameter" ),',
                 '          EmbeddedInstance ( "CIM_FooEmb1" )]',
                 '      string cimfoo_emb1);',
                 '      [Description ( "Method with no parameters but embedded instance return" ),',  # noqa: E501
                 '       EmbeddedInstance ( "CIM_FooEmb2" )]',
                 '   string DeleteNothing();',
                 '};', ''],
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],
    # pylint: enable=line-too-long

    ['Verify class command get  --di --no --namespace',
     ['get', 'CIM_Namespace', '-n', 'interop'],
     {'stdout': ['class CIM_Namespace',
                 'string ObjectManagerCreationClassName;'],
      'test': 'innows'},
     SIMPLE_INTEROP_MOCK_FILE, OK],

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

    ['Verify class command get non-existent svr. fails).',
     {'args': ['get', 'CIM_Foo'],
      'general': ['--server', 'http://NotAValidServer']},
     {'stderr': ["Error: ConnectionError:"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

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
     {'stdout': ["  root/cimv2: CIM_Foo",
                 "  root/cimv2: CIM_Foo_sub",
                 "  root/cimv2: CIM_Foo_sub2",
                 "  root/cimv2: CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in all namespaces wo case',
     ['find', 'cim_*'],
     {'stdout': ["  root/cimv2: CIM_Foo",
                 "  root/cimv2: CIM_Foo_sub",
                 "  root/cimv2: CIM_Foo_sub2",
                 "  root/cimv2: CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in all namespaces lead wc',
     ['find', '*sub_sub*'],
     {'stdout': ["  root/cimv2: CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in all namespaces wo case',
     ['find', '*sub_su?*'],
     {'stdout': ["  root/cimv2: CIM_Foo_sub_sub"],
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in known namespace',
     ['find', 'CIM_*', '-n', 'root/cimv2'],
     {'stdout': ["  root/cimv2: CIM_BaseEmb",
                 "  root/cimv2: CIM_BaseRef",
                 "  root/cimv2: CIM_Foo",
                 "  root/cimv2: CIM_FooAssoc",
                 "  root/cimv2: CIM_FooEmb1",
                 "  root/cimv2: CIM_FooEmb2",
                 "  root/cimv2: CIM_FooEmb3",
                 "  root/cimv2: CIM_FooRef1",
                 "  root/cimv2: CIM_FooRef2",
                 "  root/cimv2: CIM_Foo_sub",
                 "  root/cimv2: CIM_Foo_sub2",
                 "  root/cimv2: CIM_Foo_sub_sub"],
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find simple name in interop namespace',
     ['find', 'CIM_*'],
     {'stdout': ["  interop: CIM_Namespace",
                 "  interop: CIM_ObjectManager"],
      'test': 'in'},
     SIMPLE_INTEROP_MOCK_FILE, OK],

    ['Verify class command find name in known namespace -o grid',
     {'general': ['-o', 'grid'],
      'args': ['find', 'CIM_*', '-n', 'root/cimv2']},
     {'stdout': ['Find class CIM_*',
                 '+-------------+-----------------+',
                 '| Namespace   | Classname       |',
                 '+=============+=================+',
                 '| root/cimv2  | CIM_BaseEmb     |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_BaseRef     |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_Foo         |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_FooAssoc    |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_FooEmb1     |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_FooEmb2     |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_FooEmb3     |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_FooRef1     |',
                 '+-------------+-----------------+',
                 '| root/cimv2  | CIM_FooRef2     |',
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
     {'stdout': "  root/cimv2: CIM_Foo_sub2",
      'test': 'lines'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command find with --association filter',
     ['find', '*TST_*', '-n', 'root/cimv2', '--association'],
     {'stdout': ['TST_Lineage',
                 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionExp'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --indication filter',
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
     {'stdout': ['TST_MemberOfFamilyCollectionExp'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --no-association & --no-experimental, '
     'filters',
     ['find', 'TST_*', '-n', 'root/cimv2', '--no-association',
      '--no-experimental', '--no-indication'],
     {'stdout': ['root/cimv2: TST_FamilyCollection', 'root/cimv2: TST_Person',
                 'root/cimv2: TST_PersonClsDep', 'root/cimv2: TST_PersonDep',
                 'root/cimv2: TST_PersonPropDep', 'root/cimv2: TST_PersonSub'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --no-association & --deprecated, ',
     ['find', 'TST_*', '-n', 'root/cimv2', '--no-association', '--deprecated'],
     {'stdout': ['root/cimv2: TST_IndicationDeprecated',
                 'root/cimv2: TST_PersonClsDep',
                 'root/cimv2: TST_PersonDep',
                 'root/cimv2: TST_PersonExpProperty',
                 'root/cimv2: TST_PersonPropDep'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --experimental and --since 2.42.0.',
     ['find', "*", '--experimental', '--since', '2.42.0'],
     {'stdout': ['TST_IndicationExperimental'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --experimental and --since 2.45.0.',
     ['find', "*", '--experimental', '--since', '2.45.0'],
     {'stdout': [],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --experimental and --since 2.45.x.',
     ['find', "*", '--experimental', '--since', '2.45.x'],
     {'stderr': ['--since option value invalid. ',
                 'Must contain 3 integer elements',
                 '2.45.x'],
      'rc': 1,
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --schema "BLA".',
     ['find', '*', '--schema', 'BLA'],
     {'stdout': ['BLA_Person', ],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --schema "EXP".',
     ['find', '*', '--schema', 'EXP'],
     {'stdout': ['EXP_TestExperimental1', 'EXP_TestExperimental2',
                 'EXP_TestExperimental3', 'EXP_TestExperimental4'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --schema "EXP". test not-innows',
     ['find', '*', '--schema', 'EXP'],
     {'stdout': ['BLA_Person', 'TST_FamilyCollection', 'TST_Indication',
                 'TST_IndicationDeprecated', 'TST_IndicationExperimental',
                 'TST_Lineage', 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionDep',
                 'TST_MemberOfFamilyCollectionExp',
                 'TST_Person', 'TST_PersonClsDep', 'TST_PersonDep',
                 'TST_PersonExp', 'TST_PersonExpProperty',
                 'TST_PersonPropDep', 'TST_PersonSub'],
      'test': 'not-innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --schema "EXP" and --experimental.',
     ['find', '*', '--schema', 'EXP', '--experimental'],
     {'stdout': ['EXP_TestExperimental1', 'EXP_TestExperimental2',
                 'EXP_TestExperimental3', 'EXP_TestExperimental4'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --subclass-of.',
     ['find', '*', '--subclass-of', 'TST_Person'],
     {'stdout': ['root/cimv2: TST_PersonClsDep',
                 'root/cimv2: TST_PersonDep', 'root/cimv2: TST_PersonExp',
                 'root/cimv2: TST_PersonExpProperty',
                 'root/cimv2: TST_PersonPropDep', 'root/cimv2: TST_PersonSub'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command find with --subclass-of.',
     ['find', '*Sub', '--subclass-of', 'TST_Person'],
     {'stdout': ['root/cimv2: TST_PersonSub'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    # Tests with --leaf-classes
    ['Verify class command enumerate with --leaf-classes. test innows',
     ['enumerate', '--di', '--no', '--leaf-classes'],
     {'stdout': ['BLA_Person', 'EXP_TestExperimental1', 'EXP_TestExperimental2',
                 'EXP_TestExperimental3', 'EXP_TestExperimental4',
                 'TST_FamilyCollection', 'TST_Indication',
                 'TST_IndicationDeprecated', 'TST_IndicationExperimental',
                 'TST_Lineage', 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionDep',
                 'TST_MemberOfFamilyCollectionExp', 'TST_PersonClsDep',
                 'TST_PersonDep', 'TST_PersonExp', 'TST_PersonExpProperty',
                 'TST_PersonPropDep', 'TST_PersonSub'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --leaf-classes. test not-innows',
     ['enumerate', '--di', '--no', '--leaf-classes'],
     {'stdout': ['TST_Person'],
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --leaf-classes & --subclass-of',
     ['enumerate', '--di', '--no', '--leaf-classes', '--subclass-of',
      'TST_Person'],
     {'stdout': """TST_PersonClsDep
TST_PersonDep
TST_PersonExp
TST_PersonExpProperty
TST_PersonPropDep
TST_PersonSub
""",
      'test': 'innows'},
     QUALIFIER_FILTER_MODEL, OK],

    ['Verify class command enumerate with --leaf-classes & --subclass-of, '
     'not-innows',
     ['enumerate', '--di', '--no', '--leaf-classes', '--subclass-of',
      'TST_Person'],
     {'stdout': ['BLA_Person', 'EXP_TestExperimental1', 'EXP_TestExperimental2',
                 'EXP_TestExperimental3', 'EXP_TestExperimental4',
                 'TST_FamilyCollection', 'TST_Indication',
                 'TST_IndicationDeprecated', 'TST_IndicationExperimental',
                 'TST_Lineage', 'TST_MemberOfFamilyCollection',
                 'TST_MemberOfFamilyCollectionDep',
                 'TST_MemberOfFamilyCollectionExp'],
      'test': 'not-innows'},
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

    ['Verify class command delete successful with no subclasses, '
     '--include-instances',
     ['delete', 'CIM_Foo_sub_sub', '--include-instances'],
     {'stdout': ['Deleted instance root/cimv2:CIM_Foo_sub_sub.',
                 'Deleted class CIM_Foo_sub_sub'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete successful with no subclasses, --namespace '
     'and --include-instances',
     ['delete', 'CIM_Foo_sub_sub', '--namespace', 'root/cimv2',
      '--include-instances'],
     {'stdout': ['Deleted instance root/cimv2:CIM_Foo_sub_sub.',
                 'Deleted class CIM_Foo_sub_sub'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete (interactive) successful with no subclasses, '
     '--include-instances, --dry-run',
     {'stdin': ['class delete CIM_Foo_sub_sub --include-instances --dry-run',
                'class get CIM_Foo_sub_sub',
                'instance count CIM_Foo_sub_sub']},
     {'stdout': ['Dry run: Deleted instance root/cimv2:CIM_Foo_sub_sub.'
                 'InstanceID="CIM_Foo_sub_sub1"',
                 'Dry run: Deleted class CIM_Foo_sub_sub',
                 'class CIM_Foo_sub_sub : CIM_Foo_sub {',
                 'root/cimv2 CIM_Foo_sub_sub 3'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    # Class delete errors
    # NOTE: Missing argument tests use regex test because with Python 3.4
    # the Missing Argument output from click uses double quotes rather than
    # single quotes
    ['Verify class command delete no classname',
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

    ['Verify class command delete fail instances exist',
     ['delete', 'CIM_Foo_sub_sub'],
     {'stderr': 'Cannot delete class CIM_Foo_sub_sub because it has '
                '3 instances',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail subclasses exist',
     ['delete', 'CIM_Foo'],
     {'stderr': 'Cannot delete class CIM_Foo because it has 12 instances',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail subclasses exist, --include-instances',
     ['delete', 'CIM_Foo', '--include-instances'],
     {'stderr': 'Cannot delete class CIM_Foo because these classes depend on '
                'it: CIM_Foo_sub, CIM_Foo_sub2',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail referencing class CIM_FooRef1 exist',
     ['delete', 'CIM_FooRef1'],
     {'stderr': 'Cannot delete class CIM_FooRef1 because it has 1 instances',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail referencing class CIM_FooRef1 exist, '
     '--include-instances',
     ['delete', 'CIM_FooRef1', '--include-instances'],
     {'stderr': 'Cannot delete class CIM_FooRef1 because these classes depend '
                'on it: CIM_Foo',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail referencing class CIM_FooRef2 exist',
     ['delete', 'CIM_FooRef2'],
     {'stderr': 'Cannot delete class CIM_FooRef2 because it has 1 instances',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail referencing class CIM_FooRef2 exist, '
     '--include-instances',
     ['delete', 'CIM_FooRef2', '--include-instances'],
     {'stderr': 'Cannot delete class CIM_FooRef2 because these classes depend '
                'on it: CIM_Foo',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail referencing class CIM_FooAssoc exist',
     ['delete', 'CIM_FooAssoc'],
     {'stderr': 'Cannot delete class CIM_FooAssoc because it has 1 instances',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete succesd for referencing class CIM_FooAssoc, '
     '--include-instances',
     ['delete', 'CIM_FooAssoc', '--include-instances'],
     {'stdout': '',
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail embedding class CIM_FooEmb1 exist',
     ['delete', 'CIM_FooEmb1'],
     {'stderr': 'Cannot delete class CIM_FooEmb1 because these classes depend '
                'on it: CIM_Foo',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail embedding class CIM_FooEmb1 exist, '
     '--include-instances',
     ['delete', 'CIM_FooEmb1', '--include-instances'],
     {'stderr': 'Cannot delete class CIM_FooEmb1 because these classes depend '
                'on it: CIM_Foo',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail embedding class CIM_FooEmb2 exist',
     ['delete', 'CIM_FooEmb2'],
     {'stderr': 'Cannot delete class CIM_FooEmb2 because these classes depend '
                'on it: CIM_Foo',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail embedding class CIM_FooEmb2 exist, '
     '--include-instances',
     ['delete', 'CIM_FooEmb2', '--include-instances'],
     {'stderr': 'Cannot delete class CIM_FooEmb2 because these classes depend '
                'on it: CIM_Foo',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail embedding class CIM_FooEmb3 exist',
     ['delete', 'CIM_FooEmb3'],
     {'stderr': 'Cannot delete class CIM_FooEmb3 because these classes depend '
                'on it: CIM_Foo',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fail embedding class CIM_FooEmb3 exist, '
     '--include-instances',
     ['delete', 'CIM_FooEmb3', '--include-instances'],
     {'stderr': 'Cannot delete class CIM_FooEmb3 because these classes depend '
                'on it: CIM_Foo',
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify class command delete fails if instance provider rejects delete',
     {'args': ['delete', 'CIM_Foo_sub_sub', '--include-instances']},
     {'stderr': ['CIM_ERR_FAILED',
                 'Deletion of CIM_Foo_sub_sub instances is rejected'],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, 'reject_deleteinstance_provider.py'],
     MOCK_SETUP_SUPPORTED],

    ['Verify class command delete using --namespace interop fails because of '
     'instances',
     ['delete', 'CIM_ObjectManager', '-n', 'interop'],
     {'stderr': ['Cannot delete class', 'instances'],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_INTEROP_MOCK_FILE, OK],

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
 +-- CIM_BaseEmb
 |   +-- CIM_FooEmb1
 |   +-- CIM_FooEmb2
 |   +-- CIM_FooEmb3
 +-- CIM_BaseRef
 |   +-- CIM_FooRef1
 |   +-- CIM_FooRef2
 +-- CIM_Foo
 |   +-- CIM_Foo_sub
 |   |   +-- CIM_Foo_sub_sub
 |   +-- CIM_Foo_sub2
 +-- CIM_FooAssoc
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

    ['Verify class command tree with --detail',
     ['tree', '--detail'],
     {'stdout': """root
 +-- CIM_Foo (Version=2.30.0)
 |   +-- CIM_Foo_sub (Version=2.31.0)
 |       +-- CIM_Foo_sub_sub (Version=2.20.1)
 +-- CIM_Foo_no_version ()
 +-- CIM_Indication (Abstract,Indication,Version=2.24.0)
 +-- CIM_Indication_no_version (Abstract,Indication)
 +-- TST_Lineage (Association,Version=2.20.1)
 +-- TST_Lineage_no_version (Association)


""",
      'test': 'innows'},
     TREE_TEST_MOCK_FILE, OK],

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

    ['Verify class command associators simple request, xml output ge py_3.8,',
     {'args': ['associators', 'TST_Person'],
      'general': ['--output-format', 'xml']},
     {'stdout': ASSOCIATORS_CLASS_XML_GE_38,
      'test': 'lines'},
     SIMPLE_ASSOC_MOCK_FILE, PYTHON_GE_38],

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

    ['Verify class command references non-existent svr. fails).',
     {'args': ['associators', 'CIM_Foo'],
      'general': ['--server', 'http://NotAValidServer']},
     {'stderr': ["Error: ConnectionError:"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

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

    ['Verify class command references table output fails).',
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

    ['Verify class command references non-existent svr. fails).',
     {'args': ['references', 'CIM_Foo'],
      'general': ['--server', 'http://NotAValidServer']},
     {'stderr': ["Error: ConnectionError:"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

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

    ['Verify class command invokemethod CIM_Foo.FuzzyStatic() with --namespace',
     ['invokemethod', 'CIM_Foo', 'FuzzyStatic', '--namespace', 'root/cimv2'],
     {'stdout': ["ReturnValue=0"],
      'rc': 0,
      'test': 'lines'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

    # Cannot do a test with interop as default because of issue #991
    ['Verify class command invokemethod CIM_Foo.FuzzyStatic() with --namespace'
     ' interop not found to validate that --namspace used',
     ['invokemethod', 'CIM_Foo', 'FuzzyStatic', '--namespace', 'interop'],
     {'stderr': ["CIM_ERR_NOT_FOUND", "not found in namespace 'interop'"],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_INTEROP_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], OK],

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

    ['Verify class command invokemethod fails non-static method, pywbem 1.0',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stderr': ["Non-static method 'Fuzzy' in class 'CIM_Foo'"],
      'rc': 1,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], PYWBEM_1_0_0],

    ['Verify class command invokemethod succeeds non-static method, pywbem 0.x',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stdout': ['ReturnValue=0'],
      'rc': 0,
      'test': 'innows'},
     [SIMPLE_MOCK_FILE, INVOKE_METHOD_MOCK_FILE], not PYWBEM_1_0_0],

    ['Verify class command invokemethod fails Method not registered',
     ['invokemethod', 'CIM_Foo', 'Fuzzy'],
     {'stderr': ['CIMError'],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify  --timestats gets stats output. Cannot test with lines,execution '
     'time is variable.',
     {'args': ['get', 'CIM_Foo'],
      'general': ['--timestats']},
     {'stdout': ['Operation Count Errors',
                 'GetClass  1     0'],
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

    #
    #  Multiple Namespaces Option tests --namespace a,b and -n a -n b
    #  The following tests exercise the multiple-namespace functionality
    #  for classes (enumerate, get, associators, references) and
    #  corresponding names-only options.
    #

    ['Verify class get from two namespaces. single namespace/comma option',
     {'args': ['get', 'CIM_Foo', '--namespace', 'root/cimv2,root/cimv3']},
     {'stdout': ["""#pragma namespace ("root/cimv2")
   [Description ( "Simple CIM Class" )]
class CIM_Foo {

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();

};

#pragma namespace ("root/cimv3")
   [Description ( "Simple CIM Class" )]
class CIM_Foo {

      [Key ( true ),
       Description ( "This is key property." )]
   string InstanceID;

      [Description ( "This is Uint32 property." )]
   uint32 IntegerProp;

      [Description ( "Embedded instance property" ),
       EmbeddedInstance ( "CIM_FooEmb3" )]
   string cimfoo_emb3;

      [Description ( "Method with in and out parameters" )]
   uint32 Fuzzy(
         [IN ( true ),
          OUT ( true ),
          Description ( "Define data to be returned in output parameter" )]
      string TestInOutParameter,
         [IN ( true ),
          OUT ( true ),
          Description ( "Test of ref in/out parameter" )]
      CIM_FooRef1 REF TestRef,
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
      uint32 OutputRtnValue,
         [IN ( true ),
          Description ( "Embedded instance parameter" ),
          EmbeddedInstance ( "CIM_FooEmb1" )]
      string cimfoo_emb1);

      [Description ( "Method with no parameters but embedded instance return" ),
       EmbeddedInstance ( "CIM_FooEmb2" )]
   string DeleteNothing();

};
"""],
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class get from two namespaces use multiple namespace option',
     {'args': ['get', 'CIM_Foo', '--namespace', 'root/cimv2',
               '--namespace', 'root/cimv3']},
     {'stdout': ['#pragma namespace ("root/cimv2")',
                 '#pragma namespace ("root/cimv3")',
                 'CIM_Foo {'],
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class get from two namespaces 2nd ns no class ',
     {'args': ['get', 'CIM_Foo', '--namespace', 'root/cimv2,interop']},
     {'stdout': ['#pragma namespace ("root/cimv2")',
                 'CIM_Foo {'],
      'stderr': ["Namespace: interop", 'CIMError:CIM_ERR_NOT_FOUND'],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class get from two namespaces first ns no class ',
     {'args': ['get', 'CIM_Foo', '--namespace', 'interop,root/cimv2']},
     {'stdout': ['#pragma namespace ("root/cimv2")',
                 'CIM_Foo {'],
      'stderr': ["Namespace: interop", 'CIMError:CIM_ERR_NOT_FOUND',
                 "Error: Errors encountered on 1 server request(s)"],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class get from two namespaces class not in either namespace ',
     {'args': ['get', 'CIM_Foox', '--namespace', 'root/cimv3,root/cimv2']},
     {'stderr': ["namespace:root/cimv3", "CIMError:CIM_ERR_NOT_FOUND",
                 "namespace:root/cimv2", "CIMError:CIM_ERR_NOT_FOUND"],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class enumerate two namespaces CIM_Foo',
     {'args': ['enumerate', 'CIM_Foo', '--namespace', 'root/cimv2,root/cimv3']},
     {'stdout': [ENUMERATE_CLASS_2_NAMESPACE],
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],



    ['Verify class enumerate two namespaces CIM_Foo --object-order',
     {'args': ['enumerate', 'CIM_Foo', '-n', 'root/cimv2,root/cimv3',
               '--object-order']},
     {'stdout': [ENUMERATE_CLASS_2_NAMESPACE_OBJECT_ORDER],
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class enumerate from two namespaces, CIM_Foo comma separted',
     {'args': ['enumerate', 'CIM_Foo', '--namespace', 'root/cimv2,root/cimv3']},
     {'stdout': ['#pragma namespace ("root/cimv2")',
                 '#pragma namespace ("root/cimv3")',
                 'class CIM_Foo_sub : CIM_Foo {'],
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class enumerate from two namespaces summary',
     {'args': ['enumerate', 'CIM_Foo', '--summary',
               '--namespace', 'root/cimv2,root/cimv3']},
     {'stdout': ["""root/cimv2 2 CIMClass(s) returned
root/cimv3 2 CIMClass(s) returned
"""],
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class enumerate from two namespaces summary, table',
     {'args': ['enumerate', 'CIM_Foo', '--summary',
               '--namespace', 'root/cimv2,root/cimv3'],
      'general': ['--output-format', 'table']},
     {'stdout': """Summary of CIMClass(s) returned
+-------------+---------+------------+
| Namespace   |   Count | CIM Type   |
|-------------+---------+------------|
| root/cimv2  |       2 | CIMClass   |
| root/cimv3  |       2 | CIMClass   |
+-------------+---------+------------+
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify classnames (--no) enumerate from two namespaces summary',
     {'args': ['enumerate', 'CIM_Foo', '--no', '--summary',
               '--namespace', 'root/cimv2,root/cimv3']},
     {'stdout': """root/cimv2 2 CIMClassName(s) returned
root/cimv3 2 CIMClassName(s) returned
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify classnames (--no) enumerate from two namespaces ',
     {'args': ['enumerate', 'CIM_Foo', '--no',
               '--namespace', 'root/cimv2,root/cimv3']},
     {'stdout': """
root/cimv2:CIM_Foo_sub
root/cimv2:CIM_Foo_sub2
root/cimv3:CIM_Foo_sub
root/cimv3:CIM_Foo_sub2
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify classnames (--no) enumerate from two namespaces --object-order',
     {'args': ['enumerate', 'CIM_Foo', '--no', '--object-order',
               '--namespace', 'root/cimv2,root/cimv3']},
     {'stdout': """
root/cimv2:CIM_Foo_sub
root/cimv3:CIM_Foo_sub
root/cimv2:CIM_Foo_sub2
root/cimv3:CIM_Foo_sub2
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify classnames enumerate from two namespaces --no --summary, -o table',
     {'args': ['enumerate', 'CIM_Foo', '--no', '--summary',
               '--namespace', 'root/cimv2,root/cimv3'],
      'general': ['--output-format', 'table']},
     {'stdout': """Summary of CIMClassName(s) returned
+-------------+---------+--------------+
| Namespace   |   Count | CIM Type     |
|-------------+---------+--------------|
| root/cimv2  |       2 | CIMClassName |
| root/cimv3  |       2 | CIMClassName |
+-------------+---------+--------------+
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class enumerate from two namespaces first ns no class ',
     {'args': ['enumerate', 'CIM_Foo', '--namespace', 'interop,root/cimv2']},
     {'stdout': ['#pragma namespace ("root/cimv2")',
                 'CIM_Foo {'],
      'stderr': ["namespace:interop", "CIMError:CIM_ERR_INVALID_NAMESPACE"],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class enumerate from two namespaces class not in either ns ',
     {'args': ['enumerate', 'CIM_Foox', '--namespace',
               'root/cimv3,root/cimv2']},
     {'stderr': ["namespace:root/cimv3", "CIMError:CIM_ERR_INVALID_CLASS"],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class enumerate --no from three namespaces',
     {'args': ['enumerate', '--no', '-n', 'root/cimv2,root/cimv3,interop']},
     {'stdout': """root/cimv2:CIM_BaseEmb
root/cimv2:CIM_BaseRef
root/cimv2:CIM_Foo
root/cimv2:CIM_FooAssoc
root/cimv3:CIM_BaseEmb
root/cimv3:CIM_BaseRef
root/cimv3:CIM_Foo
root/cimv3:CIM_FooAssoc
interop:CIM_Namespace
interop:CIM_ObjectManager
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class enumerate --no from three namespaces different ns order',
     {'args': ['enumerate', '--no', '-n', 'root/cimv3,root/cimv2,interop']},
     {'stdout': """root/cimv3:CIM_BaseEmb
root/cimv3:CIM_BaseRef
root/cimv3:CIM_Foo
root/cimv3:CIM_FooAssoc
root/cimv2:CIM_BaseEmb
root/cimv2:CIM_BaseRef
root/cimv2:CIM_Foo
root/cimv2:CIM_FooAssoc
interop:CIM_Namespace
interop:CIM_ObjectManager
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],


    #  References requests with multiple namespaces tests

    ['Verify class references classnames from two namespaces',
     {'args': ['references', 'CIM_FooRef1',
               '--namespace', 'root/cimv2,root/cimv3'], },
     {'stdout': """//FakedUrl:5988/root/cimv2:CIM_FooAssoc
   [Association ( true ),
    Description ( "Simple CIM Association" )]
class CIM_FooAssoc {

      [Key ( true ),
       Description ( "This is key property." )]
   CIM_FooRef1 REF Ref1;

      [Key ( true ),
       Description ( "This is key property." )]
   CIM_FooRef2 REF Ref2;

};

//FakedUrl:5988/root/cimv3:CIM_FooAssoc
   [Association ( true ),
    Description ( "Simple CIM Association" )]
class CIM_FooAssoc {

      [Key ( true ),
       Description ( "This is key property." )]
   CIM_FooRef1 REF Ref1;

      [Key ( true ),
       Description ( "This is key property." )]
   CIM_FooRef2 REF Ref2;

};
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    # TODO: Add tests for reference and reference --no with object-order

    ['Verify references classname (--no) from two namespaces',
     {'args': ['references', 'CIM_FooRef1', '--no',
               '--namespace', 'root/cimv2,root/cimv3'], },
     {'stdout': """//FakedUrl:5988/root/cimv2:CIM_FooAssoc
//FakedUrl:5988/root/cimv3:CIM_FooAssoc

""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify class references from two namespaces, XML format, Min compare',
     {'args': ['references', 'CIM_FooRef1',
               '--namespace', 'root/cimv2,root/cimv3'],
      'general': ['--output-format', 'xml']},
     {'stdout': '''<!-- Namespace = root/cimv2 -->
<CLASSPATH>
</CLASSPATH>
<CLASS NAME="CIM_FooAssoc">
</CLASS>
<!-- Namespace = root/cimv3 -->
''',
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, FAIL],  # Fails compare of XML

    ['Verify class references from two namespaces, XML format, Min compare',
     {'args': ['references', 'CIM_FooRef1',
               '--namespace', 'root/cimv2,root/cimv3'],
      'general': ['--output-format', 'repr']},
     {'stdout': """(CIMClassName(classname='CIM_FooAssoc',
CIMClass(classname='CIM_FooAssoc',
(CIMClassName(classname='CIM_FooAssoc', namespace='root/cimv3',
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, FAIL],  # Fails compare of XML

    ['Verify references classname (--no) from two namespaces, not in one ns',
     {'args': ['references', 'CIM_FooRef1', '--no',
               '--namespace', 'interop,root/cimv2'], },
     {'stdout': """//FakedUrl:5988/root/cimv2:CIM_FooAssoc

""",
      'stderr': ["interop"],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    # Associators requests with multiple namespaces tests

    ['Verify associators classnames from two namespaces --names-only',
     {'args': ['associators', 'CIM_FooRef1', '--no',
               '--namespace', 'root/cimv2,root/cimv3'], },
     {'stdout': """//FakedUrl:5988/root/cimv2:CIM_FooRef2
//FakedUrl:5988/root/cimv3:CIM_FooRef2
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify associators from two namespaces --names-only',
     {'args': ['associators', 'CIM_FooRef1',
               '--namespace', 'root/cimv2,root/cimv3'], },
     {'stdout': """//FakedUrl:5988/root/cimv2:CIM_FooRef2
   [Description ( "Class 2 that is referenced" )]
class CIM_FooRef2 : CIM_BaseRef {
};
//FakedUrl:5988/root/cimv3:CIM_FooRef2
   [Description ( "Class 2 that is referenced" )]
class CIM_FooRef2 : CIM_BaseRef {
};
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    # TODO: Add test for associators and associator names with object-order.

    # pylint: disable=line-too-long
    ['Verify associators from two namespaces xml output',
     {'args': ['associators', 'CIM_FooRef1',
               '--namespace', 'root/cimv2,root/cimv3'],
      'general': ['--output-format', 'xml']},
     {'stdout': ['<!-- Namespace = root/cimv2 -->',
                 '<CLASSPATH>',
                 '<NAMESPACEPATH>',
                 '<HOST>FakedUrl:5988</HOST>',
                 '<LOCALNAMESPACEPATH>',
                 '<NAMESPACE NAME="root"/>',
                 '<NAMESPACE NAME="cimv2"/>',
                 '</LOCALNAMESPACEPATH>',
                 '</NAMESPACEPATH>',
                 '</CLASSPATH>',
                 '<!-- Namespace = root/cimv3 -->',
                 '<CLASS NAME="CIM_FooRef2" SUPERCLASS="CIM_BaseRef">',
                 '</QUALIFIER>',
                 '</CLASS>'],
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    # Test limited to python ge python v 3.8 because qualifier ordering
    # not determinate with python version lt 3.8.  See issue #1173
    # pylint: disable=line-too-long
    ['Verify associators from two namespaces xml output, version ge 38',
     {'args': ['associators', 'CIM_FooRef1',
               '--namespace', 'root/cimv2,root/cimv3'],
      'general': ['--output-format', 'xml']},
     {'stdout': '''<!-- Namespace = root/cimv2 -->
<CLASSPATH>
    <NAMESPACEPATH>
        <HOST>FakedUrl:5988</HOST>
        <LOCALNAMESPACEPATH>
            <NAMESPACE NAME="root"/>
            <NAMESPACE NAME="cimv2"/>
        </LOCALNAMESPACEPATH>
    </NAMESPACEPATH>
    <CLASSNAME NAME="CIM_FooRef2"/>
</CLASSPATH>

<CLASS NAME="CIM_FooRef2" SUPERCLASS="CIM_BaseRef">
    <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="false" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
        <VALUE>Class 2 that is referenced</VALUE>
    </QUALIFIER>
</CLASS>

<!-- Namespace = root/cimv3 -->
<CLASSPATH>
    <NAMESPACEPATH>
        <HOST>FakedUrl:5988</HOST>
        <LOCALNAMESPACEPATH>
            <NAMESPACE NAME="root"/>
            <NAMESPACE NAME="cimv3"/>
        </LOCALNAMESPACEPATH>
    </NAMESPACEPATH>
    <CLASSNAME NAME="CIM_FooRef2"/>
</CLASSPATH>

<CLASS NAME="CIM_FooRef2" SUPERCLASS="CIM_BaseRef">
    <QUALIFIER NAME="Description" TYPE="string" PROPAGATED="false" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
        <VALUE>Class 2 that is referenced</VALUE>
    </QUALIFIER>
</CLASS>
''',  # noqa: E501
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, PYTHON_GE_38],

    # Test all versions by not requesting qualifiers.  see issue #1173
    # pylint: disable=line-too-long
    ['Verify associators from two namespaces xml output, no-qualifiers',
     {'args': ['associators', 'CIM_FooRef1', '--no-qualifiers',
               '--namespace', 'root/cimv2,root/cimv3'],
      'general': ['--output-format', 'xml']},
     {'stdout': '''<!-- Namespace = root/cimv2 -->
<CLASSPATH>
    <NAMESPACEPATH>
        <HOST>FakedUrl:5988</HOST>
        <LOCALNAMESPACEPATH>
            <NAMESPACE NAME="root"/>
            <NAMESPACE NAME="cimv2"/>
        </LOCALNAMESPACEPATH>
    </NAMESPACEPATH>
    <CLASSNAME NAME="CIM_FooRef2"/>
</CLASSPATH>

<CLASS NAME="CIM_FooRef2" SUPERCLASS="CIM_BaseRef"/>

<!-- Namespace = root/cimv3 -->
<CLASSPATH>
    <NAMESPACEPATH>
        <HOST>FakedUrl:5988</HOST>
        <LOCALNAMESPACEPATH>
            <NAMESPACE NAME="root"/>
            <NAMESPACE NAME="cimv3"/>
        </LOCALNAMESPACEPATH>
    </NAMESPACEPATH>
    <CLASSNAME NAME="CIM_FooRef2"/>
</CLASSPATH>

<CLASS NAME="CIM_FooRef2" SUPERCLASS="CIM_BaseRef"/>
''',  # noqa: E501
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    # pylint: enable=line-too-long

    ['Verify associators classnames from two namespaces --names-only',
     {'args': ['associators', 'CIM_FooRef1', '--no',
               '--namespace', 'root/cimv2,interop'], },
     {'stdout': """//FakedUrl:5988/root/cimv2:CIM_FooRef2
""",
      'stderr': ['Error', 'interop'],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify associators classnames from two namespaces class not in either',
     {'args': ['associators', 'CIM_FooRefX', '--no',
               '--namespace', 'root/cimv2,root/cimv3'], },
     {'stderr': ['Error', 'root/cimv2', 'root/cimv3', 'CIM_FooRefX'],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

]

# TODO command class delete. Extend this test to use stdin (delete, test)
# namespace
# other tests.  Test local-only on top level
# TODO: Test class  REPR outputs


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
