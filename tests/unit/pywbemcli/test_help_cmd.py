# (C) Copyright 2023 IBM Corp.
# (C) Copyright 2023 Inova Development Inc.
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
subjects. This command is not part of any command group.
"""

import pytest

from .cli_test_extensions import CLITestsBase

# pylint: disable=use-dict-literal

DEFAULT_HELP_LINES = """
Help Subjects:
Subject name    Subject description
--------------  ---------------------------------------------
activate        Activating shell tab completion
instancename    InstanceName parameter in instance cmd group
repl            Using the repl command
tab-completion  Where tab completion is provided by pywbemcli
"""

REPL_HELP_LINES = [
    'repl - Using the repl command',
    'In the interactive mode pywbem returns control to a terminal. General'
]

# This is only a one line test becasuse it is also tested with instance cmds
INSTANCENAME_HELP_LINES = [
    "An instance path is specified using the INSTANCENAME argument and "
]

TABCOMPLETION_HELP_LINES = [
    "Tab completion is always available in the interactive mode (see help repl)"
]

ACTIVATE_HELP_LINES = [
    "Pywbemcli includes tab-completion capability for all commands for certain"
]


OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet
SKIP = False


TEST_CASES = [
    # List of testcases for command help <subject>.
    # Each testcase is a list with the following items:
    # * desc: Description of testcase.
    # * inputs:
    # * inputs.subject: argument (i.e. subject for the help command)
    # *
    # * exp_response: Dictionary of expected responses (stdout, stderr, rc) and
    #     test definition (test: <testname>). See the 'exp_response' parameter
    #     of CLITestsBase.command_test() in cli_test_extensions.py for
    #     detailed documentation.
    # * mock: None, name of file (.mof or .py), or list thereof.
    # * condition: If True the test is executed, if 'pdb' the test breaks in the
    #     the debugger, if 'verbose' print verbose messages, if False the test
    #     is skipped.

    ['Verify help command default response list of subjects',
     {'args': ['help'], },
     {'stdout': DEFAULT_HELP_LINES,
      'test': 'innows'},
     None, RUN],

    ['Verify help command  arg repl',
     {'args': ['help', 'repl']},
     {'stdout': REPL_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify help command  arg instancename',
     {'args': ['help', 'instancename']},
     {'stdout': INSTANCENAME_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify help command arg tab-completion',
     {'args': ['help', 'tab-completion']},
     {'stdout': TABCOMPLETION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify help command arg tab-completion unique partial input',
     {'args': ['help', 'tab-c']},
     {'stdout': TABCOMPLETION_HELP_LINES,
      'test': 'innows'},
     None, OK],

    ['Verify help command arg tab-completion',
     {'args': ['help', 'blah']},
     {'stderr': ["'blah' is not a valid help subject."],
      'rc': 1,
      'test': 'innows'},
     None, OK],
]


class TestCmdHelp(CLITestsBase):  # pylint: disable=too-few-public-methods
    """
    Test the help command
    """

    command_group = None

    @pytest.mark.parametrize(
        "desc, inputs, exp_response, mock, condition", TEST_CASES)
    def test_help_cmd(self, desc, inputs, exp_response, mock, condition):
        """
       Test the help command
        """
        self.command_test(desc, self.command_group, inputs, exp_response,
                          mock, condition)
