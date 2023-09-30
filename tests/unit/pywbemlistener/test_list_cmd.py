# (C) Copyright 2021 Inova Development Inc.
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
Test the 'pywbemlistener list' command.
"""

from __future__ import absolute_import, print_function

import pytest

from .cli_test_extensions import pywbemlistener_test, RUN, RUN_NO_WIN_NO_PY27

# pylint: disable=use-dict-literal

# Output patterns for 'pywbemlistener list --help'
LIST_HELP_PATTERNS = [
    r"^Usage: pywbemlistener \[GENERAL-OPTIONS\] list \[COMMAND-OPTIONS\]$",
    r"^Command Options:$",
    r"^ *-h, --help ?",
]

# Output patterns for 'list' command when there are no running listeners
LIST_NONE_PATTERNS = [
    r"No running listeners",
]

LIST_TESTCASES = [

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
        "Verify output of 'list --help'",
        dict(
            args=['list', '--help'],
        ),
        dict(
            stdout=LIST_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'list -h'",
        dict(
            args=['list', '-h'],
        ),
        dict(
            stdout=LIST_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'list' with no listener running",
        dict(
            args=['list'],
        ),
        dict(
            stdout=LIST_NONE_PATTERNS,
            test='all',
        ),
        RUN,
    ),
    (
        "Verify output of 'list' with one http listener running",
        dict(
            args=['-o', 'plain', 'list'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001'],
            ]
        ),
        dict(
            stdout=[
                r"^Name +Port +Scheme +Bind addr +PID +Created$",
                r"^lis1 +50001 +http +none +[0-9]+ +[0-9\- :\.]+$",
            ],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify output of 'list' with two http listeners running",
        dict(
            args=['-o', 'plain', 'list'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001'],
                ['lis2', '--scheme', 'http', '--port', '50002'],
                ['lis3', '--scheme', 'http', '--port', '50003',
                 '--bind-addr', 'localhost'],
            ]
        ),
        dict(
            stdout=[
                r"^Name +Port +Scheme +Bind addr +PID +Created$",
                r"^lis1 +50001 +http +none +[0-9]+ +[0-9\- :\.]+$",
                r"^lis2 +50002 +http +none +[0-9]+ +[0-9\- :\.]+$",
                r"^lis3 +50003 +http +localhost +[0-9]+ +[0-9\- :\.]+$",
            ],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
]


@pytest.mark.parametrize(
    "desc, inputs, exp_results, condition",
    LIST_TESTCASES
)
def test_lis_list(desc, inputs, exp_results, condition):
    """
    Test general options of pywbemlistener.
    """
    pywbemlistener_test(desc, inputs, exp_results, condition)
