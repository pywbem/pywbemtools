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
subjects.

"""

from __future__ import absolute_import, print_function

import pytest

from .cli_test_extensions import pywbemlistener_test, RUN

# pylint: disable=use-dict-literal

SHOW_TABCOMPLETION_HELP_LINES = [
    "Tab completion is always available in the interactive mode (see help repl)"
]

SHOW_ACTIVATE_HELP_LINES = [
    "Pywbemlistener includes tab-completion capability for all commands for "
    "certain"
]

# Output patterns for 'pywbemlistener show --help'
SHOW_HELP_PATTERNS = [
    r"^Usage: pywbemlistener help \[GENERAL-OPTIONS\] SUBJECT",
    r"^Command Options:$",
    r"^ *-h, --help ?",
]

SHOW_HELP_SUMMARY_PATTERNS = [
    r"Help Subjects:",
    r"Subject name    Subject description",
    r"--------------  ---------------------------------------------",
    r"activate        Activating shell tab completion",
    r"tab-completion  Where tab completion is provided by pywbemlistener"
]

SHOW_HELP_ACTIVATE_PATTERNS = [
    r"activate - Activating shell tab completion",
    r"Pywbemlistener includes tab-completion capability",
    r"Manually executing the sourcing statement when required."
]


SHOW_TESTCASES = [

    # List of testcases.
    # Each testcase is a list with the following items:
    # * desc: Description of the testcase.
    # * inputs: Dictionary of inputs (args, env, listeners).
    #     See pywbemlistener_test() for details.
    # * exp_results: Dictionary of expected results (rc, stdout, stderr, log,
    #     test). See pywbemlistener_test() for details.
    # * condition: Condition for running the testcase and how to run it
    #     (True, False, 'pdb', 'verbose').
    #     See pywbemlistener_test() for details.

    (
        "Verify output of 'help --help'",
        dict(
            args=['help', '--help'],
        ),
        dict(
            stdout=SHOW_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'help'",
        dict(
            args=['help'],
        ),
        dict(
            stdout=SHOW_HELP_SUMMARY_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'help activate'",
        dict(
            args=['help', 'activate'],
        ),
        dict(
            stdout=SHOW_HELP_ACTIVATE_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'help act' with unique partial command",
        dict(
            args=['help', 'act'],
        ),
        dict(
            stdout=SHOW_HELP_ACTIVATE_PATTERNS,
            test='contains',
        ),
        RUN,
    ),

    (
        "Verify output of 'help blah' with invalid subject",
        dict(
            args=['help', 'blah'],
        ),
        dict(
            stderr=["Error: 'blah' is not a valid help subject"],
            rc=1,
            test='contains',
        ),
        RUN,
    ),
]


@pytest.mark.parametrize(
    "desc, inputs, exp_results, condition",
    SHOW_TESTCASES
)
def test_help_show(desc, inputs, exp_results, condition):
    """
    Test general options of pywbemlistener.
    """
    pywbemlistener_test(desc, inputs, exp_results, condition)
