# (C) Copyright 2017 IBM Corp.
# (C) Copyright 2017 Inova Development Inc.
# All Rights Reserved
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
Test the help command that displays help text on specific pywbemcli
subjects.

"""

import pytest

from .cli_test_extensions import CLITestsBase

DEFAULT_HELP_LINES = """Help subjects
subject name    subject description
--------------  --------------------------------------------
instancename    InstanceName parameter in instance cmd group
repl            Using the repl command
"""
REPL_HELP_LINES = [
    'repl - Using the repl command',
    'In the interactive mode pywbem returns control to a terminal. General'
]

# This is only a one line test becasuse it is also tested with instance cmds
INSTANCENAME_HELP_LINES = [
    "An instance path is specified using the INSTANCENAME argument and "
]

OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet
SKIP = False


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

    ['Verify help command default response list of subjects',
     {'subject': []},
     {'stdout': DEFAULT_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify help command repl',
     {'subject': ['repl']},
     {'stdout': REPL_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify help command instancename',
     {'subject': ['instancename']},
     {'stdout': INSTANCENAME_HELP_LINES,
      'test': 'innows'},
     None, OK],
]


class TestHelpCmd(CLITestsBase):  # pylint: disable=too-few-pubic-methods
    """
    Test the general options including statistics,  --server,
    --timeout, --use-pull, --pull-max-cnt, --output-format
    """
    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition", TEST_CASES)
    def test_execute_pywbemcli(self, desc, inputs, exp_response, mock,
                               condition):
        # pylint: disable=unused-argument
        """
        Execute pybemcli with the defined input and test output.

        """

        command_group = 'help'

        if inputs['subject']:
            inputs = inputs['subject']
        else:
            inputs = []

        self.command_test(desc, command_group, inputs, exp_response,
                          None, condition)
