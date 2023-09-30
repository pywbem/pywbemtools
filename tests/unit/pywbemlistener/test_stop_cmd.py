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
Test the 'pywbemlistener stop' command.
"""

from __future__ import absolute_import, print_function

import pytest

from .cli_test_extensions import pywbemlistener_test, RUN, RUN_NO_WIN_NO_PY27

# pylint: disable=use-dict-literal

# Output patterns for 'pywbemlistener stop --help'
STOP_HELP_PATTERNS = [
    r"^Usage: pywbemlistener \[GENERAL-OPTIONS\] stop NAME "
    r"\[COMMAND-OPTIONS\]$",
    r"^Command Options:$",
    r"^ *-h, --help ?",
]

# Output patterns for 'stop' command when the listener is not found
STOP_NOTFOUND_PATTERNS = [
    r"No running listener found with name ",
]

# Output patterns for 'stop' command when the listener was successfully stopped
STOP_SUCCESS_PATTERNS = [
    r"Shut down listener .+ running at ",
]

STOP_TESTCASES = [

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
        "Verify output of 'stop --help'",
        dict(
            args=['stop', '--help'],
        ),
        dict(
            stdout=STOP_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'stop -h'",
        dict(
            args=['stop', '-h'],
        ),
        dict(
            stdout=STOP_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'stop' on non-existing listener",
        dict(
            args=['stop', 'lis1'],
        ),
        dict(
            rc=1,
            stderr=STOP_NOTFOUND_PATTERNS,
            test='all',
        ),
        RUN,
    ),
    (
        "Verify output of 'stop' on existing listener",
        dict(
            args=['stop', 'lis1'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001'],
            ]
        ),
        dict(  # pylint:disable=use-dict-literal
            # TODO: Output goes neither on stdout nor on stderr
            # stdout=STOP_SUCCESS_PATTERNS,
            # test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
]


@pytest.mark.parametrize(
    "desc, inputs, exp_results, condition",
    STOP_TESTCASES
)
def test_lis_stop(desc, inputs, exp_results, condition):
    """
    Test general options of pywbemlistener.
    """
    pywbemlistener_test(desc, inputs, exp_results, condition)
