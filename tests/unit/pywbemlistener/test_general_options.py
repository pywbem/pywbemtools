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
Test the pywbemlistener general options. That is those options that show up in
the help output from pywbemlistener --help.

NOTE: The --logdir and --output-format options are tested in a separate file.
"""

from __future__ import absolute_import, print_function

import sys
import pytest

from .cli_test_extensions import pywbemlistener_test, RUN

# pylint: disable=use-dict-literal

# Output patterns for 'pywbemlistener --help'
HELP_PATTERNS = [
    r"^Usage: pywbemlistener \[GENERAL-OPTIONS\] COMMAND \[ARGS\] "
    r"\[COMMAND-OPTIONS\]$",
    r"^General Options:$",
    r"-o, --output-format FORMAT ?",
    r"-l, --logdir DIR ?",
    r"-v, --verbose ?",
    r"--pdb ?",
    r"--warn ?",
    r"--version ?",
    r"-h, --help ?",
    r"^Commands:$",
    r"list ",
    r"show ",
    r"start ",
    r"stop ",
    r"run ",
]

# Output patterns for 'list' command when testing options
LIST_NONE_PATTERNS = [
    r"No running listeners",
]

GENERAL_OPTIONS_TESTCASES = [

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
        "Verify output of '--help'",
        dict(
            args=['--help'],
        ),
        dict(
            stdout=HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of '-h'",
        dict(
            args=['-h'],
        ),
        dict(
            stdout=HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify that '--warn' option is valid",
        dict(
            args=['--warn', 'list'],
        ),
        dict(
            stdout=LIST_NONE_PATTERNS,
            test='all',
        ),
        RUN,
    ),
    (
        "Verify '--warn' option with warning for Python <= 3.4",
        dict(
            args=['--warn', 'list'],
        ),
        dict(
            rc=0,
            stderr=[r"Pywbemlistener support for Python .* is deprecated"],
            test='contains',
        ),
        sys.version_info[0:2] == (2, 7),
    ),
    (
        "Verify that '--verbose' option is valid",
        dict(
            args=['--verbose', 'list'],
        ),
        dict(
            stdout=LIST_NONE_PATTERNS,
            test='all',
        ),
        RUN,
    ),
    (
        "Verify that '-v' option is valid",
        dict(
            args=['-v', 'list'],
        ),
        dict(
            stdout=LIST_NONE_PATTERNS,
            test='all',
        ),
        RUN,
    ),
    (
        "Verify that '--verbose' option can be specified two times",
        dict(
            args=['--verbose', '--verbose', 'list'],
        ),
        dict(
            stdout=LIST_NONE_PATTERNS,
            test='all',
        ),
        RUN,
    ),
    (
        "Verify that '-v' option can be specified two times",
        dict(
            args=['-vv', 'list'],
        ),
        dict(
            stdout=LIST_NONE_PATTERNS,
            test='all',
        ),
        RUN,
    ),
    (
        "Verify '--version' option",
        dict(
            args=['--version'],
        ),
        dict(
            stdout=[
                r"^pywbemlistener, version [0-9]+\.[0-9]+\.[0-9]+",
                r"^pywbem, version [0-9]+\.[0-9]+\.[0-9]+",
            ],
            test='all',
        ),
        RUN,
    ),
]


@pytest.mark.parametrize(
    "desc, inputs, exp_results, condition",
    GENERAL_OPTIONS_TESTCASES
)
def test_lis_general_options(desc, inputs, exp_results, condition):
    """
    Test general options of pywbemlistener.
    """
    pywbemlistener_test(desc, inputs, exp_results, condition)
