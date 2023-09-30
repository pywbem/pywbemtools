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
Test the 'pywbemlistener run' command.
"""

from __future__ import absolute_import, print_function

import pytest

from .cli_test_extensions import pywbemlistener_test, RUN, RUN_NO_WIN_NO_PY27
from .test_start_cmd import START_HELP_CALL_PATTERNS, \
    START_HELP_FORMAT_PATTERNS

# pylint: disable=use-dict-literal

# Output patterns for 'pywbemlistener run --help'
RUN_HELP_PATTERNS = [
    r"^Usage: pywbemlistener \[GENERAL-OPTIONS\] run NAME "
    r"\[COMMAND-OPTIONS\]$",
    r"^Command Options:$",
    r"^ *-p, --port PORT ?",
    r"^ *-s, --scheme SCHEME ?",
    r"^ *-b, --bind-addr HOST ?",
    r"^ *-c, --certfile FILE ?",
    r"^ *-k, --keyfile FILE ?",
    r"^ *--indi-call MODULE.FUNCTION ?",
    r"^ *--indi-file FILE ?",
    r"^ *--indi-format FORMAT ?",
    r"^ *--help-format ?",
    r"^ *--help-call ?",
    r"^ *-h, --help ?",
]

RUN_HELP_CALL_PATTERNS = START_HELP_CALL_PATTERNS
RUN_HELP_FORMAT_PATTERNS = START_HELP_FORMAT_PATTERNS

# Output patterns for 'run' command when the listener already exists
RUN_EXISTS_PATTERNS = [
    r"Listener .+ already running at ",
]

# Output patterns for 'run' command when the listener was successfully started
RUN_SUCCESS_PATTERNS = [
    r"Running listener .+ at ",
]

RUN_TESTCASES = [

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
        "Verify output of 'run --help'",
        dict(
            args=['run', '--help'],
        ),
        dict(
            stdout=RUN_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'run -h'",
        dict(
            args=['run', '-h'],
        ),
        dict(
            stdout=RUN_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'run --help-call'",
        dict(
            args=['run', '--help-call'],
        ),
        dict(
            stdout=RUN_HELP_CALL_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'run --help-format'",
        dict(
            args=['run', '--help-format'],
        ),
        dict(
            stdout=RUN_HELP_FORMAT_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'run' on existing listener",
        dict(
            args=['run', 'lis1', '--scheme', 'http', '--port', '50001'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50000'],
            ]
        ),
        dict(
            rc=1,
            stderr=RUN_EXISTS_PATTERNS,
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
]


@pytest.mark.parametrize(
    "desc, inputs, exp_results, condition",
    RUN_TESTCASES
)
def test_lis_run(desc, inputs, exp_results, condition):
    """
    Test general options of pywbemlistener.
    """
    pywbemlistener_test(desc, inputs, exp_results, condition)
