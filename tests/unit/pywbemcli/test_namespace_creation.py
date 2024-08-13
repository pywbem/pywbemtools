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
Tests the namespace creation behavior.
"""


import pytest

from .cli_test_extensions import CLITestsBase

# pylint: disable=use-dict-literal

# Mock environment #1: Namespace-neutral MOF, no Interop namespace
MOCK1_MOF_FILE = 'simple_mock_model.mof'
MOCK1_CLASS = 'CIM_Foo'
MOCK1_FOO_NAMESPACE = 'foo'

# Mock environment #2: Interop namespace and MOF with pragma namespace 'foo'
MOCK2_SCRIPT_FILE = 'simple_foo_mock_script.py'
MOCK2_FOO_MOF_FILE = 'simple_foo_mock_model.mof'
MOCK2_FOO_CLASS = 'CIM_Foo'  # only in user namespace
MOCK2_FOO_NAMESPACE = 'foo'
MOCK2_INTEROP_MOF_FILE = 'mock_interop.mof'
MOCK2_INTEROP_CLASS = 'CIM_ObjectManager'  # only in Interop namespace
MOCK2_INTEROP_NAMESPACE = 'interop'

# Mock environment #3: Interop namespace and namespace-neutral MOF
MOCK3_SCRIPT_FILE = 'simple_interop_mock_script.py'
MOCK3_FOO_MOF_FILE = 'simple_mock_model.mof'
MOCK3_FOO_CLASS = 'CIM_Foo'  # only in user namespace
MOCK3_FOO_NAMESPACE = 'foo'
MOCK3_INTEROP_MOF_FILE = 'mock_interop.mof'
MOCK3_INTEROP_CLASS = 'CIM_ObjectManager'  # only in Interop namespace
MOCK3_INTEROP_NAMESPACE = 'interop'

# Default namespace of pywbem when not specified
DEFAULT_DEFAULT_NAMESPACE = 'root/cimv2'


TEST_CASES = [

    # List of testcases.
    # Each testcase is a tuple with the following items:
    # * desc: Description of testcase.
    # * group: Command group of the pywbemcli command.
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

    (
        "Mock environment #1: Command mode 'class get' with no default "
        "namespace specified can retrieve foo class",
        'class',
        dict(
            args=['get', MOCK1_CLASS, '--nq'],
            general=['-v']
        ),
        dict(
            rc=0,
            stdout=[
                f"^Compiling file .*{MOCK1_MOF_FILE}",
                f"^Target namespace '{DEFAULT_DEFAULT_NAMESPACE}'",
                f"^Creating class {DEFAULT_DEFAULT_NAMESPACE}:{MOCK1_CLASS}$",
                f"^class {MOCK1_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK1_MOF_FILE, True
    ),
    (
        "Mock environment #1: Command mode 'class get' with default namespace "
        "'foo' specified can retrieve foo class",
        'class',
        dict(
            args=['get', MOCK1_CLASS, '--nq'],
            general=['-v', '-d', MOCK1_FOO_NAMESPACE]
        ),
        dict(
            rc=0,
            stdout=[
                f"^Compiling file .*{MOCK1_MOF_FILE}",
                f"^Target namespace '{MOCK1_FOO_NAMESPACE}'",
                f"^Creating class {MOCK1_FOO_NAMESPACE}:{MOCK1_CLASS}$",
                f"^class {MOCK1_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK1_MOF_FILE, True
    ),
    (
        "Mock environment #1: Command mode 'class get' with command namespace "
        "'foo' specified cannot retrieve foo class because it got created in "
        "default default namespace",
        'class',
        dict(
            args=['get', MOCK1_CLASS, '--nq', '-n', MOCK1_FOO_NAMESPACE],
            general=['-v']
        ),
        dict(
            rc=1,
            stdout=[
                f"^Compiling file .*{MOCK1_MOF_FILE}",
                f"^Target namespace '{DEFAULT_DEFAULT_NAMESPACE}'",
                f"^Creating class {DEFAULT_DEFAULT_NAMESPACE}:{MOCK1_CLASS}$",
            ],
            stderr=[
                "CIM_ERR_INVALID_NAMESPACE.* Namespace does not exist in CIM "
                f"repository: ''{MOCK1_FOO_NAMESPACE}'",
            ],
            test='regex'
        ),
        MOCK1_MOF_FILE, True
    ),
    (
        "Mock environment #1: Interactive mode 'class get' with default "
        "namespace 'foo' specified can retrieve foo class",
        None,
        dict(
            stdin=[
                f'-v -d {MOCK1_FOO_NAMESPACE} class get {MOCK1_CLASS} --nq'
            ]
        ),
        dict(
            rc=0,
            stdout=[
                f"^Compiling file .*{MOCK1_MOF_FILE}",
                f"^Target namespace '{MOCK1_FOO_NAMESPACE}'",
                f"^Creating class {MOCK1_FOO_NAMESPACE}:{MOCK1_CLASS}$",
                f"^class {MOCK1_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK1_MOF_FILE, True
    ),
    (
        "Mock environment #1 with default namespace 'bar' specified on command "
        "line: Interactive mode 'class get' with default namespace 'foo' "
        "specified can retrieve foo class",
        None,
        dict(
            general=['-d', 'bar'],
            stdin=[
                f'-v -d {MOCK1_FOO_NAMESPACE} class get {MOCK1_CLASS} --nq'
            ]
        ),
        dict(
            rc=0,
            stdout=[
                f"^Compiling file .*{MOCK1_MOF_FILE}",
                f"^Target namespace '{MOCK1_FOO_NAMESPACE}'",
                f"^Creating class {MOCK1_FOO_NAMESPACE}:{MOCK1_CLASS}$",
                f"^class {MOCK1_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK1_MOF_FILE, True
    ),
    (
        "Mock environment #1: Interactive mode 'class get' with command "
        "namespace 'foo' specified cannot retrieve foo class because it got "
        "created in default default namespace",
        None,
        dict(
            stdin=[
                f'-v class get {MOCK1_CLASS} --nq -n {MOCK1_FOO_NAMESPACE}'
            ]
        ),
        dict(
            rc=0,  # interactive mode rc=1 is not propagated to command line rc
            stdout=[
                f"^Compiling file .*{MOCK1_MOF_FILE}",
                f"^Target namespace '{DEFAULT_DEFAULT_NAMESPACE}'",
                f"^Creating class {DEFAULT_DEFAULT_NAMESPACE}:{MOCK1_CLASS}$",
            ],
            stderr=[
                "CIM_ERR_INVALID_NAMESPACE.* Namespace does not exist in CIM "
                f"repository: ''{MOCK1_FOO_NAMESPACE}'",
            ],
            test='regex'
        ),
        MOCK1_MOF_FILE, True
    ),
    (
        "Mock environment #2: Command mode 'class get' with no default "
        "namespace specified cannot retrieve foo class because it accesses "
        "the default default namespace",
        'class',
        dict(
            args=['get', MOCK2_FOO_CLASS, '--nq'],
            general=['-v']
        ),
        dict(
            rc=1,
            stdout=[
                f"^Creating namespace {MOCK2_INTEROP_NAMESPACE} .in mock "
                "support.",
                f"^Compiling file .*{MOCK2_INTEROP_MOF_FILE}",
                f"^Target namespace '{MOCK2_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK2_INTEROP_NAMESPACE}:"
                f"{MOCK2_INTEROP_CLASS}$",
                f"^Compiling file .*{MOCK2_FOO_MOF_FILE}",
                f"^Target namespace '{DEFAULT_DEFAULT_NAMESPACE}'",
                f"^Switching target namespace to '{MOCK2_FOO_NAMESPACE}'",
                f"^Creating namespace {MOCK2_FOO_NAMESPACE} .in MOF compiler.",
                f"^Creating class {MOCK2_FOO_NAMESPACE}:{MOCK2_FOO_CLASS}$",
            ],
            stderr=[
                f"CIM_ERR_NOT_FOUND.: Class '{MOCK2_FOO_CLASS}' not found "
                f"in namespace '{DEFAULT_DEFAULT_NAMESPACE}'",
            ],
            test='regex'
        ),
        MOCK2_SCRIPT_FILE, True
    ),
    (
        "Mock environment #2 with default namespace 'foo' specified on "
        "command line: Command mode 'class get' can retrieve foo class",
        'class',
        dict(
            args=['get', MOCK2_FOO_CLASS, '--nq'],
            general=['-v', '-d', MOCK2_FOO_NAMESPACE]
        ),
        dict(
            rc=0,
            stdout=[
                f"^Creating namespace {MOCK2_INTEROP_NAMESPACE} .in "
                "mock support.",
                f"^Compiling file .*{MOCK2_INTEROP_MOF_FILE}",
                f"^Target namespace '{MOCK2_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK2_INTEROP_NAMESPACE}:"
                f"{MOCK2_INTEROP_CLASS}$",
                f"^Compiling file .*{MOCK2_FOO_MOF_FILE}",
                f"^Target namespace '{MOCK2_FOO_NAMESPACE}'",
                f"^Switching target namespace to '{MOCK2_FOO_NAMESPACE}'",
                f"^Creating class {MOCK2_FOO_NAMESPACE}:{MOCK2_FOO_CLASS}$",
                f"^class {MOCK2_FOO_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK2_SCRIPT_FILE, True
    ),
    (
        "Mock environment #2: Command mode 'class get' with command namespace "
        "'foo' specified can retrieve foo class",
        'class',
        dict(
            args=['get', MOCK2_FOO_CLASS, '--nq', '-n', MOCK2_FOO_NAMESPACE],
            general=['-v']
        ),
        dict(
            rc=0,
            stdout=[
                f"^Creating namespace {MOCK2_INTEROP_NAMESPACE} .in mock "
                "support.",
                f"^Compiling file .*{MOCK2_INTEROP_MOF_FILE}",
                f"^Target namespace '{MOCK2_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK2_INTEROP_NAMESPACE}:"
                f"{MOCK2_INTEROP_CLASS}$",
                f"^Compiling file .*{MOCK2_FOO_MOF_FILE}",
                f"^Target namespace '{DEFAULT_DEFAULT_NAMESPACE}'",
                f"^Switching target namespace to '{MOCK2_FOO_NAMESPACE}'",
                f"^Creating namespace {MOCK2_FOO_NAMESPACE} .in MOF compiler.",
                f"^Creating class {MOCK2_FOO_NAMESPACE}:{MOCK2_FOO_CLASS}$",
                f"^class {MOCK2_FOO_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK2_SCRIPT_FILE, True
    ),
    (
        "Mock environment #2 with default namespace 'bar' specified on "
        "command line: Interactive mode 'class get' with default namespace "
        "'foo' specified can retrieve foo class",
        None,
        dict(
            general=['-d', 'bar'],
            stdin=[
                f'-v -d {MOCK2_FOO_NAMESPACE} class get {MOCK2_FOO_CLASS} --nq'
            ]
        ),
        dict(
            rc=0,
            stdout=[
                f"^Creating namespace {MOCK2_INTEROP_NAMESPACE} .in mock "
                "support.",
                f"^Compiling file .*{MOCK2_INTEROP_MOF_FILE}",
                f"^Target namespace '{MOCK2_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK2_INTEROP_NAMESPACE}:"
                f"{MOCK2_INTEROP_CLASS}$",
                f"^Compiling file .*{MOCK2_FOO_MOF_FILE}",
                f"^Target namespace '{MOCK2_FOO_NAMESPACE}'",
                f"^Switching target namespace to '{MOCK2_FOO_NAMESPACE}'",
                f"^Creating class {MOCK2_FOO_NAMESPACE}:{MOCK2_FOO_CLASS}$",
                f"^class {MOCK2_FOO_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK2_SCRIPT_FILE, True
    ),
    (
        "Mock environment #2: Interactive mode 'class get' with command "
        "namespace 'foo' specified can retrieve foo class",
        None,
        dict(
            stdin=[
                f'-v class get {MOCK2_FOO_CLASS} --nq -n {MOCK2_FOO_NAMESPACE}'
            ]
        ),
        dict(
            rc=0,
            stdout=[
                f"^Creating namespace {MOCK2_INTEROP_NAMESPACE} .in mock "
                "support.",
                f"^Compiling file .*{MOCK2_INTEROP_MOF_FILE}",
                f"^Target namespace '{MOCK2_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK2_INTEROP_NAMESPACE}:"
                f"{MOCK2_INTEROP_CLASS}$",
                f"^Compiling file .*{MOCK2_FOO_MOF_FILE}",
                f"^Target namespace '{DEFAULT_DEFAULT_NAMESPACE}'",
                f"^Switching target namespace to '{MOCK2_FOO_NAMESPACE}'",
                f"^Creating namespace {MOCK2_FOO_NAMESPACE} .in MOF compiler.",
                f"^Creating class {MOCK2_FOO_NAMESPACE}:{MOCK2_FOO_CLASS}$",
                f"^class {MOCK2_FOO_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK2_SCRIPT_FILE, True
    ),
    (
        # Testcase similar to issue #991, but with new foo mock script
        "Mock environment #2: Interactive mode 'class get' with default "
        "namespace 'interop' specified can retrieve interop class",
        None,
        dict(
            stdin=[
                f"-v -d {MOCK2_INTEROP_NAMESPACE} class get "
                f"{MOCK2_INTEROP_CLASS} --nq"
            ]
        ),
        dict(
            rc=0,
            stdout=[
                f"^Compiling file .*{MOCK2_INTEROP_MOF_FILE}",
                f"^Target namespace '{MOCK2_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK2_INTEROP_NAMESPACE}:"
                f"{MOCK2_INTEROP_CLASS}$",
                f"^Compiling file .*{MOCK2_FOO_MOF_FILE}",
                f"^Target namespace '{MOCK2_INTEROP_NAMESPACE}'",
                f"^Switching target namespace to '{MOCK2_FOO_NAMESPACE}'",
                f"^Creating namespace {MOCK2_FOO_NAMESPACE} .in MOF compiler.",
                f"^Creating class {MOCK2_FOO_NAMESPACE}:{MOCK2_FOO_CLASS}$",
                f"^class {MOCK2_INTEROP_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK2_SCRIPT_FILE, True
    ),
    (
        # Testcase representing issue #991, but with fixed interop mock script
        "Mock environment #3: Interactive mode 'class get' with default "
        "namespace 'interop' specified can retrieve interop class",
        None,
        dict(
            stdin=[
                f"-v -d {MOCK3_INTEROP_NAMESPACE} class get "
                f"{MOCK3_INTEROP_CLASS} --nq"
            ]
        ),
        dict(
            rc=0,
            stdout=[
                f"^Compiling file .*{MOCK3_INTEROP_MOF_FILE}",
                f"^Target namespace '{MOCK3_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK3_INTEROP_NAMESPACE}:"
                f"{MOCK3_INTEROP_CLASS}$",
                f"^Compiling file .*{MOCK3_FOO_MOF_FILE}",
                f"^Target namespace '{MOCK3_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK3_INTEROP_NAMESPACE}:{MOCK3_FOO_CLASS}$",
                f"^class {MOCK3_INTEROP_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK3_SCRIPT_FILE, True
    ),
    (
        "Mock environment #3 with default namespace 'interop' specified: "
        "Interactive mode 'class get' can retrieve interop class",
        None,
        dict(
            general=['-d', MOCK3_INTEROP_NAMESPACE],
            stdin=[
                f'-v class get {MOCK3_INTEROP_CLASS} --nq'
            ]
        ),
        dict(
            rc=0,
            stdout=[
                f"^Compiling file .*{MOCK3_INTEROP_MOF_FILE}",
                f"^Target namespace '{MOCK3_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK3_INTEROP_NAMESPACE}:"
                f"{MOCK3_INTEROP_CLASS}$",
                f"^Compiling file .*{MOCK3_FOO_MOF_FILE}",
                f"^Target namespace '{MOCK3_INTEROP_NAMESPACE}'",
                f"^Creating class {MOCK3_INTEROP_NAMESPACE}:{MOCK3_FOO_CLASS}$",
                f"^class {MOCK3_INTEROP_CLASS} {{$",
            ],
            test='regex'
        ),
        MOCK3_SCRIPT_FILE, True
    ),
]


class TestNamespaceCreation(CLITestsBase):
    # pylint: disable=too-few-public-methods
    """
    Run all testcases for namespace creation behavior.
    """

    @pytest.mark.parametrize(
        "desc, group, inputs, exp_response, mock, condition",
        TEST_CASES)
    def test_namespace(
            self, desc, group, inputs, exp_response, mock, condition):
        """
        Run the test for a single testcase.
        """
        self.command_test(desc, group, inputs, exp_response, mock, condition)
