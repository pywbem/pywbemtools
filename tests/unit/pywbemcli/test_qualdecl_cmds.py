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

from __future__ import absolute_import, print_function

import os
import sys
import pytest

from .cli_test_extensions import CLITestsBase
from .common_options_help_lines import CMD_OPTION_HELP_HELP_LINE, \
    CMD_OPTION_SUMMARY_HELP_LINE, \
    CMD_OPTION_MULTIPLE_NAMESPACE_DFLT_CONN_HELP_LINE

# pylint: disable=use-dict-literal

TEST_DIR = os.path.dirname(__file__)

PYTHON_GE_38 = sys.version_info > (3, 8)
THREE_NS_MOCK_FILE = 'simple_three_ns_mock_script.py'

# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = 'simple_mock_model.mof'

QD_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] qualifier COMMAND [ARGS] '
    '[COMMAND-OPTIONS]'
    'Command group for CIM qualifier declarations.',
    CMD_OPTION_HELP_HELP_LINE,
    'enumerate  List the qualifier declarations in a namespace.',
    'get        Get a qualifier declaration.',
]

QD_ENUMERATE_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] qualifier enumerate [COMMAND-OPTIONS]',
    'List the qualifier declarations in a namespace.',
    CMD_OPTION_MULTIPLE_NAMESPACE_DFLT_CONN_HELP_LINE,
    CMD_OPTION_SUMMARY_HELP_LINE,
    CMD_OPTION_HELP_HELP_LINE,
]

QD_GET_HELP_LINES = [
    'Usage: pywbemcli [GENERAL-OPTIONS] qualifier get QUALIFIERNAME '
    '[COMMAND-OPTIONS]',
    "Get a qualifier declaration.",
    CMD_OPTION_MULTIPLE_NAMESPACE_DFLT_CONN_HELP_LINE,
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

Qualifier EmbeddedInstance : string,
    Scope(property, method, parameter);

Qualifier EmbeddedObject : boolean = false,
    Scope(property, method, parameter),
    Flavor(DisableOverride, ToSubclass);

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

Qualifier Static : boolean = false,
    Scope(property, method),
    Flavor(DisableOverride, ToSubclass);

"""


# pylint: disable=line-too-long
QD_TBL_OUT = """Qualifier Declarations
+------------------+---------+---------+---------+-------------+-----------------+
| Name             | Type    | Value   | Array   | Scopes      | Flavors         |
+==================+=========+=========+=========+=============+=================+
| Abstract         | boolean | False   | False   | CLASS       | EnableOverride  |
|                  |         |         |         | ASSOCIATION | Restricted      |
|                  |         |         |         | INDICATION  |                 |
+------------------+---------+---------+---------+-------------+-----------------+
| Aggregate        | boolean | False   | False   | REFERENCE   | DisableOverride |
|                  |         |         |         |             | ToSubclass      |
+------------------+---------+---------+---------+-------------+-----------------+
| Association      | boolean | False   | False   | ASSOCIATION | DisableOverride |
|                  |         |         |         |             | ToSubclass      |
+------------------+---------+---------+---------+-------------+-----------------+
| Description      | string  |         | False   | ANY         | EnableOverride  |
|                  |         |         |         |             | ToSubclass      |
|                  |         |         |         |             | Translatable    |
+------------------+---------+---------+---------+-------------+-----------------+
| EmbeddedInstance | string  |         | False   | PROPERTY    | DisableOverride |
|                  |         |         |         | METHOD      | Restricted      |
|                  |         |         |         | PARAMETER   |                 |
+------------------+---------+---------+---------+-------------+-----------------+
| EmbeddedObject   | boolean | False   | False   | PROPERTY    | DisableOverride |
|                  |         |         |         | METHOD      | ToSubclass      |
|                  |         |         |         | PARAMETER   |                 |
+------------------+---------+---------+---------+-------------+-----------------+
| In               | boolean | True    | False   | PARAMETER   | DisableOverride |
|                  |         |         |         |             | ToSubclass      |
+------------------+---------+---------+---------+-------------+-----------------+
| Indication       | boolean | False   | False   | CLASS       | DisableOverride |
|                  |         |         |         | INDICATION  | ToSubclass      |
+------------------+---------+---------+---------+-------------+-----------------+
| Key              | boolean | False   | False   | PROPERTY    | DisableOverride |
|                  |         |         |         | REFERENCE   | ToSubclass      |
+------------------+---------+---------+---------+-------------+-----------------+
| Out              | boolean | False   | False   | PARAMETER   | DisableOverride |
|                  |         |         |         |             | ToSubclass      |
+------------------+---------+---------+---------+-------------+-----------------+
| Override         | string  |         | False   | PROPERTY    | EnableOverride  |
|                  |         |         |         | REFERENCE   | Restricted      |
|                  |         |         |         | METHOD      |                 |
+------------------+---------+---------+---------+-------------+-----------------+
| Static           | boolean | False   | False   | PROPERTY    | DisableOverride |
|                  |         |         |         | METHOD      | ToSubclass      |
+------------------+---------+---------+---------+-------------+-----------------+
"""  # noqa: E501
# pylint: enable=line-too-long

QD_TBL_GET_OUT = """Qualifier Declarations
+----------+---------+---------+---------+-------------+----------------+
| Name     | Type    | Value   | Array   | Scopes      | Flavors        |
+==========+=========+=========+=========+=============+================+
| Abstract | boolean | False   | False   | CLASS       | EnableOverride |
|          |         |         |         | ASSOCIATION | Restricted     |
|          |         |         |         | INDICATION  |                |
+----------+---------+---------+---------+-------------+----------------+
"""

# pylint enable=line_too_long
QD_TBL_ENUM_MULTI_NS_OUT = """Qualifier Declarations
+-------------+------------------+---------+---------+---------+-------------+-----------------+
| namespace   | Name             | Type    | Value   | Array   | Scopes      | Flavors         |
|-------------+------------------+---------+---------+---------+-------------+-----------------|
| root/cimv2  | Abstract         | boolean | False   | False   | CLASS       | EnableOverride  |
|             |                  |         |         |         | ASSOCIATION | Restricted      |
|             |                  |         |         |         | INDICATION  |                 |
| root/cimv2  | Aggregate        | boolean | False   | False   | REFERENCE   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv2  | Association      | boolean | False   | False   | ASSOCIATION | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv2  | Description      | string  |         | False   | ANY         | EnableOverride  |
|             |                  |         |         |         |             | ToSubclass      |
|             |                  |         |         |         |             | Translatable    |
| root/cimv2  | EmbeddedInstance | string  |         | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | Restricted      |
|             |                  |         |         |         | PARAMETER   |                 |
| root/cimv2  | EmbeddedObject   | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | ToSubclass      |
|             |                  |         |         |         | PARAMETER   |                 |
| root/cimv2  | In               | boolean | True    | False   | PARAMETER   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv2  | Indication       | boolean | False   | False   | CLASS       | DisableOverride |
|             |                  |         |         |         | INDICATION  | ToSubclass      |
| root/cimv2  | Key              | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | REFERENCE   | ToSubclass      |
| root/cimv2  | Out              | boolean | False   | False   | PARAMETER   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv2  | Override         | string  |         | False   | PROPERTY    | EnableOverride  |
|             |                  |         |         |         | REFERENCE   | Restricted      |
|             |                  |         |         |         | METHOD      |                 |
| root/cimv2  | Static           | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | ToSubclass      |
| root/cimv3  | Abstract         | boolean | False   | False   | CLASS       | EnableOverride  |
|             |                  |         |         |         | ASSOCIATION | Restricted      |
|             |                  |         |         |         | INDICATION  |                 |
| root/cimv3  | Aggregate        | boolean | False   | False   | REFERENCE   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv3  | Association      | boolean | False   | False   | ASSOCIATION | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv3  | Description      | string  |         | False   | ANY         | EnableOverride  |
|             |                  |         |         |         |             | ToSubclass      |
|             |                  |         |         |         |             | Translatable    |
| root/cimv3  | EmbeddedInstance | string  |         | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | Restricted      |
|             |                  |         |         |         | PARAMETER   |                 |
| root/cimv3  | EmbeddedObject   | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | ToSubclass      |
|             |                  |         |         |         | PARAMETER   |                 |
| root/cimv3  | In               | boolean | True    | False   | PARAMETER   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv3  | Indication       | boolean | False   | False   | CLASS       | DisableOverride |
|             |                  |         |         |         | INDICATION  | ToSubclass      |
| root/cimv3  | Key              | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | REFERENCE   | ToSubclass      |
| root/cimv3  | Out              | boolean | False   | False   | PARAMETER   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv3  | Override         | string  |         | False   | PROPERTY    | EnableOverride  |
|             |                  |         |         |         | REFERENCE   | Restricted      |
|             |                  |         |         |         | METHOD      |                 |
| root/cimv3  | Static           | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | ToSubclass      |
+-------------+------------------+---------+---------+---------+-------------+-----------------+
"""  # noqa: E501


QD_TBL_ENUM_MULTI_NS_OUT_OBJECT_ORDER = """Qualifier Declarations
+-------------+------------------+---------+---------+---------+-------------+-----------------+
| namespace   | Name             | Type    | Value   | Array   | Scopes      | Flavors         |
|-------------+------------------+---------+---------+---------+-------------+-----------------|
| root/cimv2  | Abstract         | boolean | False   | False   | CLASS       | EnableOverride  |
|             |                  |         |         |         | ASSOCIATION | Restricted      |
|             |                  |         |         |         | INDICATION  |                 |
| root/cimv3  | Abstract         | boolean | False   | False   | CLASS       | EnableOverride  |
|             |                  |         |         |         | ASSOCIATION | Restricted      |
|             |                  |         |         |         | INDICATION  |                 |
| root/cimv2  | Aggregate        | boolean | False   | False   | REFERENCE   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv3  | Aggregate        | boolean | False   | False   | REFERENCE   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv2  | Association      | boolean | False   | False   | ASSOCIATION | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv3  | Association      | boolean | False   | False   | ASSOCIATION | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv2  | Description      | string  |         | False   | ANY         | EnableOverride  |
|             |                  |         |         |         |             | ToSubclass      |
|             |                  |         |         |         |             | Translatable    |
| root/cimv3  | Description      | string  |         | False   | ANY         | EnableOverride  |
|             |                  |         |         |         |             | ToSubclass      |
|             |                  |         |         |         |             | Translatable    |
| root/cimv2  | EmbeddedInstance | string  |         | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | Restricted      |
|             |                  |         |         |         | PARAMETER   |                 |
| root/cimv3  | EmbeddedInstance | string  |         | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | Restricted      |
|             |                  |         |         |         | PARAMETER   |                 |
| root/cimv2  | EmbeddedObject   | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | ToSubclass      |
|             |                  |         |         |         | PARAMETER   |                 |
| root/cimv3  | EmbeddedObject   | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | ToSubclass      |
|             |                  |         |         |         | PARAMETER   |                 |
| root/cimv2  | In               | boolean | True    | False   | PARAMETER   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv3  | In               | boolean | True    | False   | PARAMETER   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv2  | Indication       | boolean | False   | False   | CLASS       | DisableOverride |
|             |                  |         |         |         | INDICATION  | ToSubclass      |
| root/cimv3  | Indication       | boolean | False   | False   | CLASS       | DisableOverride |
|             |                  |         |         |         | INDICATION  | ToSubclass      |
| root/cimv2  | Key              | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | REFERENCE   | ToSubclass      |
| root/cimv3  | Key              | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | REFERENCE   | ToSubclass      |
| root/cimv2  | Out              | boolean | False   | False   | PARAMETER   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv3  | Out              | boolean | False   | False   | PARAMETER   | DisableOverride |
|             |                  |         |         |         |             | ToSubclass      |
| root/cimv2  | Override         | string  |         | False   | PROPERTY    | EnableOverride  |
|             |                  |         |         |         | REFERENCE   | Restricted      |
|             |                  |         |         |         | METHOD      |                 |
| root/cimv3  | Override         | string  |         | False   | PROPERTY    | EnableOverride  |
|             |                  |         |         |         | REFERENCE   | Restricted      |
|             |                  |         |         |         | METHOD      |                 |
| root/cimv2  | Static           | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | ToSubclass      |
| root/cimv3  | Static           | boolean | False   | False   | PROPERTY    | DisableOverride |
|             |                  |         |         |         | METHOD      | ToSubclass      |
+-------------+------------------+---------+---------+---------+-------------+-----------------+
"""  # noqa: E501
# pylint enable=line_too_long

QD_MOF_ENUM_MULTINS_OUT = """#pragma namespace ("root/cimv2")
Qualifier Abstract : boolean = false,
    Scope(class, association, indication),
    Flavor(EnableOverride, Restricted);

#pragma namespace ("root/cimv2")
Qualifier Aggregate : boolean = false,
    Scope(reference),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Association : boolean = false,
    Scope(association),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Description : string,
    Scope(any),
    Flavor(EnableOverride, ToSubclass, Translatable);

#pragma namespace ("root/cimv2")
Qualifier EmbeddedInstance : string,
    Scope(property, method, parameter);

#pragma namespace ("root/cimv2")
Qualifier EmbeddedObject : boolean = false,
    Scope(property, method, parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier In : boolean = true,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Indication : boolean = false,
    Scope(class, indication),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Key : boolean = false,
    Scope(property, reference),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Out : boolean = false,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Override : string,
    Scope(property, reference, method),
    Flavor(EnableOverride, Restricted);

#pragma namespace ("root/cimv2")
Qualifier Static : boolean = false,
    Scope(property, method),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Abstract : boolean = false,
    Scope(class, association, indication),
    Flavor(EnableOverride, Restricted);

#pragma namespace ("root/cimv3")
Qualifier Aggregate : boolean = false,
    Scope(reference),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Association : boolean = false,
    Scope(association),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Description : string,
    Scope(any),
    Flavor(EnableOverride, ToSubclass, Translatable);

#pragma namespace ("root/cimv3")
Qualifier EmbeddedInstance : string,
    Scope(property, method, parameter);

#pragma namespace ("root/cimv3")
Qualifier EmbeddedObject : boolean = false,
    Scope(property, method, parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier In : boolean = true,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Indication : boolean = false,
    Scope(class, indication),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Key : boolean = false,
    Scope(property, reference),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Out : boolean = false,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Override : string,
    Scope(property, reference, method),
    Flavor(EnableOverride, Restricted);

#pragma namespace ("root/cimv3")
Qualifier Static : boolean = false,
    Scope(property, method),
    Flavor(DisableOverride, ToSubclass);

"""
# pylint enable=line_too_long
QD_MOF_GET_MULTINS_OUT = """
#pragma namespace ("root/cimv2")
Qualifier Abstract : boolean = false,
    Scope(class, association, indication),
    Flavor(EnableOverride, Restricted);

#pragma namespace ("root/cimv3")
Qualifier Abstract : boolean = false,
    Scope(class, association, indication),
    Flavor(EnableOverride, Restricted);

"""

QD_MOF_ENUM_MULTINS_OUT_OBJECT_ORDER = """#pragma namespace ("root/cimv2")
Qualifier Abstract : boolean = false,
    Scope(class, association, indication),
    Flavor(EnableOverride, Restricted);

#pragma namespace ("root/cimv3")
Qualifier Abstract : boolean = false,
    Scope(class, association, indication),
    Flavor(EnableOverride, Restricted);

#pragma namespace ("root/cimv2")
Qualifier Aggregate : boolean = false,
    Scope(reference),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Aggregate : boolean = false,
    Scope(reference),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Association : boolean = false,
    Scope(association),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Association : boolean = false,
    Scope(association),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Description : string,
    Scope(any),
    Flavor(EnableOverride, ToSubclass, Translatable);

#pragma namespace ("root/cimv3")
Qualifier Description : string,
    Scope(any),
    Flavor(EnableOverride, ToSubclass, Translatable);

#pragma namespace ("root/cimv2")
Qualifier EmbeddedInstance : string,
    Scope(property, method, parameter);

#pragma namespace ("root/cimv3")
Qualifier EmbeddedInstance : string,
    Scope(property, method, parameter);

#pragma namespace ("root/cimv2")
Qualifier EmbeddedObject : boolean = false,
    Scope(property, method, parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier EmbeddedObject : boolean = false,
    Scope(property, method, parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier In : boolean = true,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier In : boolean = true,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Indication : boolean = false,
    Scope(class, indication),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Indication : boolean = false,
    Scope(class, indication),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Key : boolean = false,
    Scope(property, reference),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Key : boolean = false,
    Scope(property, reference),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Out : boolean = false,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Out : boolean = false,
    Scope(parameter),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv2")
Qualifier Override : string,
    Scope(property, reference, method),
    Flavor(EnableOverride, Restricted);

#pragma namespace ("root/cimv3")
Qualifier Override : string,
    Scope(property, reference, method),
    Flavor(EnableOverride, Restricted);

#pragma namespace ("root/cimv2")
Qualifier Static : boolean = false,
    Scope(property, method),
    Flavor(DisableOverride, ToSubclass);

#pragma namespace ("root/cimv3")
Qualifier Static : boolean = false,
    Scope(property, method),
    Flavor(DisableOverride, ToSubclass);

"""

QD_TBL_GET_MULTINS_OUT = """Qualifier Declarations
+-------------+----------+---------+---------+---------+-------------+----------------+
| namespace   | Name     | Type    | Value   | Array   | Scopes      | Flavors        |
|-------------+----------+---------+---------+---------+-------------+----------------|
| root/cimv2  | Abstract | boolean | False   | False   | CLASS       | EnableOverride |
|             |          |         |         |         | ASSOCIATION | Restricted     |
|             |          |         |         |         | INDICATION  |                |
| root/cimv3  | Abstract | boolean | False   | False   | CLASS       | EnableOverride |
|             |          |         |         |         | ASSOCIATION | Restricted     |
|             |          |         |         |         | INDICATION  |                |
+-------------+----------+---------+---------+---------+-------------+----------------+
"""  # noqa: E501
# pylint enable=line_too_long

# The following variables are used to control tests executed during
# development of tests
OK = True      # set to OK for tests passed. Set OK = False to execute one test
RUN = True     # set RUN condition in test being run
FAIL = False   # flag any tests that fail

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
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command enumerate with namespace returns qual decls.',
     ['enumerate', '--namespace', 'root/cimv2'],
     {'stdout': QD_ENUM_MOCK,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command enumerate summary returns qual decls.',
     ['enumerate', '--summary'],
     {'stdout': ['12', 'CIMQualifierDeclaration'],
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command enumerate summary returns qual decls table',
     {'args': ['enumerate', '--summary'],
      'general': ['--output-format', 'table']},
     {'stdout': ["""Summary of CIMQualifierDeclaration(s) returned
+---------+-------------------------+
|   Count | CIM Type                |
|---------+-------------------------|
|      12 | CIMQualifierDeclaration |
+---------+-------------------------+
"""],
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command get  Description qual decl',
     ['get', 'Description'],
     {'stdout': "Qualifier Description : string,\n"
                "    Scope(any),\n"
                "    Flavor(EnableOverride, ToSubclass, Translatable);\n",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command get invalid qual decl name .',
     ['get', 'NoSuchQualDecl'],
     {'stderr': ["namespace:root/cimv2", "CIMError:CIM_ERR_NOT_FOUND"],
      'rc': 1,
      'test': 'in'},
     SIMPLE_MOCK_FILE, OK],

    # Output test in pieces because qual decl attributes not ordered in python
    # version lt 3.8
    ['Verify qualifier command get  Description outputformat xml',
     {'args': ['get', 'Description'],
      'general': ['--output-format', 'xml']},
     {'stdout': ['<QUALIFIER.DECLARATION( | .+ )NAME="Description"',
                 '<SCOPE( | .+ )ASSOCIATION="true"'],
      'test': 'regex'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command get  Description outputformat repr',
     {'args': ['get', 'Description'],
      'general': ['--output-format', 'repr']},
     {'stdout': "CIMQualifierDeclaration(name='Description', value=None, "
                "type='string', is_array=False, array_size=None, "
                "scopes=NocaseDict({'CLASS': False, 'ASSOCIATION': False, "
                "'INDICATION': False, 'PROPERTY': False, 'REFERENCE': False, "
                "'METHOD': False, 'PARAMETER': False, 'ANY': True}), "
                "tosubclass=True, overridable=True, translatable=True, "
                "toinstance=None)",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command get  Description outputformat txt',
     {'args': ['get', 'Description'],
      'general': ['--output-format', 'txt']},
     {'stdout': "CIMQualifierDeclaration(name='Description', value=None, "
                "type='string', is_array=False, ...)",
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    # pylint: disable=line-too-long
    ['Verify qualifier command get  Description outputformat xml',
     {'args': ['get', 'Description'],
      'general': ['--output-format', 'xml']},
     {'stdout': '''<QUALIFIER.DECLARATION NAME="Description" TYPE="string" ISARRAY="false" OVERRIDABLE="true" TOSUBCLASS="true" TRANSLATABLE="true">
<SCOPE ASSOCIATION="true" CLASS="true" INDICATION="true" METHOD="true" PARAMETER="true" PROPERTY="true" REFERENCE="true"/>
</QUALIFIER.DECLARATION>
''',  # noqa E501
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, PYTHON_GE_38],
    # pylint: enable=line-too-long

    ['Verify qualifier command -o grid enumerate produces table out',
     {'args': ['enumerate'],
      'general': ['-o', 'grid']},
     {'stdout': QD_TBL_OUT,
      'rc': 0,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command -o grid get Abstract table out',
     {'args': ['get', 'abstract'],
      'general': ['-o', 'grid']},
     {'stdout': QD_TBL_GET_OUT,
      'rc': 0,
      'test': 'linesnows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command enumerate invalid namespace Fails',
     ['enumerate', '--namespace', 'root/blah'],
     {'stderr': ["namespace:root/blah", "CIMError:CIM_ERR_INVALID_NAMESPACE"],
      'rc': 1,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    ['Verify qualifier command --timestats gets stats output. Cannot test'
     'with lines because execution time is variable.',
     {'args': ['get', 'IN'],
      'general': ['--timestats']},
     {'stdout': ['Qualifier In : boolean = true,',
                 'Client statistics',
                 'Operation Count Errors',
                 'GetQualifier 1 0'],
      'rc': 0,
      'test': 'innows'},
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

    ['Verify qualifier command delete Aggregate (unused qualifier) succeeds',
     {'args': ['delete', 'Aggregate'],
      'general': ['-v']},
     {'stdout': "Deleted qualifier type Aggregate",
      'rc': 0,
      'test': 'innows'},
     SIMPLE_MOCK_FILE, OK],

    #
    #  Tests for multiple namespace enumerate
    #
    ['Verify qualifier command enumerate table, multiple ns',
     {'args': ['enumerate', '--namespace', 'root/cimv2,root/cimv3'],
      'general': ['-o', 'table']},
     {'stdout': QD_TBL_ENUM_MULTI_NS_OUT,
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify qualifier command enumerate table, multiple ns',
     {'args': ['enumerate', '--namespace', 'root/cimv2,root/cimv3',
               '--object-order'],
      'general': ['-o', 'table']},
     {'stdout': QD_TBL_ENUM_MULTI_NS_OUT_OBJECT_ORDER,
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify qualifier command enumerate multiple ns MOF out',
     {'args': ['enumerate', '--namespace', 'root/cimv2,root/cimv3'],
      'general': []},
     {'stdout': QD_MOF_ENUM_MULTINS_OUT,
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify qualifier command enumerate multiple ns MOF out',
     {'args': ['enumerate', '--namespace', 'root/cimv2,root/cimv3',
               '--object-order'],
      'general': []},
     {'stdout': QD_MOF_ENUM_MULTINS_OUT_OBJECT_ORDER,
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify qualifier command enumerate multiple ns  table output',
     {'args': ['enumerate', '--namespace', 'root/cimv2,root/cimv3',
               '--summary'],
      'general': ['-o', 'table']},
     {'stdout': """Summary of CIMQualifierDeclaration(s) returned
+-------------+---------+-------------------------+
| Namespace   |   Count | CIM Type                |
|-------------+---------+-------------------------|
| root/cimv2  |      12 | CIMQualifierDeclaration |
| root/cimv3  |      12 | CIMQualifierDeclaration |
+-------------+---------+-------------------------+
""",
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify qualifier command enumerate non-existent svr. fails).',
     {'args': ['enumerate'],
      'general': ['--server', 'http://NotAValidServer']},
     {'stderr': ["Error: ConnectionError:"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

    ['Verify qualifier command get table, multiple ns',
     {'args': ['get', 'Abstract', '--namespace', 'root/cimv2,root/cimv3'],
      'general': ['-o', 'table']},
     {'stdout': QD_TBL_GET_MULTINS_OUT,
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify qualifier command get MOF out, multiple ns',
     {'args': ['get', 'Abstract', '--namespace', 'root/cimv2,root/cimv3'],
      'general': []},
     {'stdout': QD_MOF_GET_MULTINS_OUT,
      'rc': 0,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify qualifier command get MOF out, multiple ns only in one ns',
     {'args': ['get', 'EmbeddedObject', '--namespace', 'root/cimv2,interop'],
      'general': []},
     {'stdout': ['#pragma namespace ("root/cimv2")',
                 'Qualifier EmbeddedObject : boolean = false,'],
      'stderr': ["namespace:interop", "error:CIM_ERR_NOT_FOUND",
                 "Description:Qualifier declaration 'EmbeddedObject' not "
                 "found in namespace 'interop'"],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify qualifier command get MOF out, multiple ns not found',
     {'args': ['get', 'Invalid_QD', '--namespace', 'root/cimv2,root/cimv3'],
      'general': []},
     {'stderr': ["namespace:root/cimv2", "CIMError:CIM_ERR_NOT_FOUND",
                 "Description:Qualifier declaration 'Invalid_QD' not found in "
                 "namespace 'root/cimv2'", "namespace:root/cimv3"],
      'rc': 1,
      'test': 'innows'},
     THREE_NS_MOCK_FILE, OK],

    ['Verify qualifier get non-existent svr. fails).',
     {'args': ['get', 'EmbeddedObject'],
      'general': ['--server', 'http://NotAValidServer']},
     {'stderr': ["Error: ConnectionError:"],
      'rc': 1,
      'test': 'innows'},
     None, OK],

]


class TestcmdQualifiers(CLITestsBase):  # pylint: disable=too-few-public-methods
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
