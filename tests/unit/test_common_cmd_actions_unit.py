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
Unit tests for the pywbemtools/_common_comd_action.py functions that provide
common action functions for commands that are used by multiple tools

These unit tests just test the functions themselves in isolation but not in a
command line environment.

NOTE: This unit test is only in pywbemcli because the same code is used
in both pywbemcli and pywbemlistener.
"""

from __future__ import absolute_import, print_function

import click
import pytest

from pywbemtools.pywbemcli._context_obj import ContextObj
from pywbemtools._common_cmd_actions import help_subjects_action

# pylint: disable=relative-beyond-top-level
from .pytest_extensions import simplified_test_function
# pylint: enable=relative-beyond-top-level

# pylint: disable=use-dict-literal

OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet
SKIP = False  # mark tests that are to be skipped.

REPL_HELP_MSG = "HELP for repl"
ACTIVATE_MSG = "HELP for activate message"
ACTIVATE2_MSG = "HELP for activate2 message"
ACTIVATE3_MSG = "HELP for activate3 message"
INSTANCENAME_MSG = "HELP for instancename"

PYWBEMCLI_TEST_HELP_SUBJECTS_DICT = {
    "repl": ("Using the repl command", REPL_HELP_MSG),
    'activate': ("Activating shell tab completion",
                 ACTIVATE_MSG),
    'instancename': ('InstanceName parameter in instance cmd group',
                     INSTANCENAME_MSG),
    'activate2': ("Activating2 shell tab completion",
                  ACTIVATE2_MSG),
    'activate3': ("Activating3 shell tab completion",
                  ACTIVATE3_MSG),
}

#
# These tests were added to test some code that cannot be tested by the
# functional tests because in those tests, we do not control the subjects
# dictionary.
#


TESTCASES_COMMON_ACTION_HELP = [
    # Testcases for _cmd_help.help_arg_subject_shell_complete()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * subject: string representing the incomplete subject name
    #   * exp_rtn: Expected return
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify correct completion with complete input',
     dict(subject="activate",
          exp_rtn="activate - Activating shell tab completion\n"
                  "HELP for activate message"),
     None, None, OK),

    ('Verify correct completion with last character missing',
     dict(subject="act",
          exp_rtn="""
Help Subjects: Input: `act` matches multiple subjects:` `activate, activate2, activate3`
Subject name    Subject description
--------------  --------------------------------
activate        Activating shell tab completion
activate2       Activating2 shell tab completion
activate3       Activating3 shell tab completion"""),  # noqa: E501
     None, None, OK),

    ('Verify exception for invalid input',
     dict(subject="blah",
          exp_rtn=""),
     click.ClickException, None, OK),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_COMMON_ACTION_HELP)
@simplified_test_function
def test_help(testcase, subject, exp_rtn):
    """
    Test function for help_arg_subject_shell_complete() function. Note that
    the parameters ctx and param are not used by the function being tested
    """

    obj = ContextObj(
        pywbem_server=None,
        output_format=None,
        timestats=None,
        log=None,
        verbose=None,
        pdb=None,
        warn=None,
        connections_repo=None,
        interactive_mode=False,
        close_interactive_server=False)

    # The code to be tested
    result = help_subjects_action(obj, subject,
                                  PYWBEMCLI_TEST_HELP_SUBJECTS_DICT)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    if result != exp_rtn:
        print("Expected:\n{}\nReturned:\n{}".format(exp_rtn, result))

    assert result == exp_rtn
