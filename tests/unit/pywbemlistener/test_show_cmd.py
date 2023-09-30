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
Test the 'pywbemlistener show' command.
"""

from __future__ import absolute_import, print_function

import pytest

from .cli_test_extensions import pywbemlistener_test, RUN, RUN_NO_WIN_NO_PY27

# pylint: disable=use-dict-literal

# Output patterns for 'pywbemlistener show --help'
SHOW_HELP_PATTERNS = [
    r"^Usage: pywbemlistener \[GENERAL-OPTIONS\] show NAME "
    r"\[COMMAND-OPTIONS\]$",
    r"^Command Options:$",
    r"^ *-h, --help ?",
]

# Output patterns for 'show' command when the listener is not found
SHOW_NOTFOUND_PATTERNS = [
    r"No running listener found with name ",
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
        "Verify output of 'show --help'",
        dict(
            args=['show', '--help'],
        ),
        dict(
            stdout=SHOW_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'show -h'",
        dict(
            args=['show', '-h'],
        ),
        dict(
            stdout=SHOW_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'show' on non-existing listener",
        dict(
            args=['show', 'lis1'],
        ),
        dict(
            rc=1,
            stderr=SHOW_NOTFOUND_PATTERNS,
            test='all',
        ),
        RUN,
    ),
    (
        "Verify output of 'show' on existing listener",
        dict(
            args=['-o', 'plain', 'show', 'lis1'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001'],
            ]
        ),
        dict(
            stdout=[
                r"^Attribute +Value$",
                r"^Name +lis1$",
                r"^Port +50001$",
                r"^Scheme +http$",
                r"^Bind addr +none",
                r"^Certificate file *$",
                r"^Key file *$",
                r"^Indication call *$",
                r"^Indication file *$",
                r"^Log file *$",
                r"^PID +[0-9]+$",
                r"^Start PID +[0-9]+$",
                r"^Created +[0-9\- :\.]+$",
            ],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify output of 'show' on existing listener with bind-addr set",
        dict(
            args=['-o', 'plain', 'show', 'lis1'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001',
                 '--bind-addr', 'localhost'],
            ]
        ),
        dict(
            stdout=[
                r"^Attribute +Value$",
                r"^Name +lis1$",
                r"^Port +50001$",
                r"^Scheme +http$",
                r"^Bind addr +localhost",
                r"^Certificate file *$",
                r"^Key file *$",
                r"^Indication call *$",
                r"^Indication file *$",
                r"^Log file *$",
                r"^PID +[0-9]+$",
                r"^Start PID +[0-9]+$",
                r"^Created +[0-9\- :\.]+$",
            ],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
]


@pytest.mark.parametrize(
    "desc, inputs, exp_results, condition",
    SHOW_TESTCASES
)
def test_lis_show(desc, inputs, exp_results, condition):
    """
    Test general options of pywbemlistener.
    """
    pywbemlistener_test(desc, inputs, exp_results, condition)
