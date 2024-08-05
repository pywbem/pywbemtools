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
Test the 'pywbemlistener test' command.
"""


import pytest

from .cli_test_extensions import pywbemlistener_test, RUN, RUN_NO_WIN

# pylint: disable=use-dict-literal

# Output patterns for 'pywbemlistener list --help'
TEST_HELP_PATTERNS = [
    r"^Usage: pywbemlistener \[GENERAL-OPTIONS\] test NAME "
    r"\[COMMAND-OPTIONS\]$",
    r"^Command Options:$",
    r"^ *-c, --count INT ?",
    r"^ *-l, --listener HOST?",
    r"^ *-h, --help ?",
]

TEST_TESTCASES = [

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
        "Verify output of 'test --help'",
        dict(
            args=['test', '--help'],
        ),
        dict(
            stdout=TEST_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'test -h'",
        dict(
            args=['test', '-h'],
        ),
        dict(
            stdout=TEST_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify 'test' with no listener running",
        dict(
            args=['test', 'lis1'],
            listeners=[]
        ),
        dict(
            rc=1,
            stderr=[
                r"^Error: No running listener found with name lis1$",
            ],
            test='all',
        ),
        RUN,
    ),
    (
        "Verify 'test' with one http listener running",
        dict(
            args=['test', 'lis1'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001'],
            ]
        ),
        dict(
            stdout=[
                r"^Sending the following test indication:$",
                r"^instance of ",
                r"^Sent test indication #1 to listener lis1 at ",
            ],
            test='contains',
        ),
        RUN_NO_WIN,
    ),
    (
        "Verify 'test' with one http listener running and -c 2",
        dict(
            args=['test', 'lis1', '-c', '2'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001'],
            ]
        ),
        dict(
            stdout=[
                r"^Sending the following test indication:$",
                r"^instance of ",
                r"^Sent test indication #1 to listener lis1 at ",
                r"^Sent test indication #2 to listener lis1 at ",
            ],
            test='contains',
        ),
        RUN_NO_WIN,
    ),
    (
        "Verify 'test' with one http listener running and --count 2",
        dict(
            args=['test', 'lis1', '--count', '2'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001'],
            ]
        ),
        dict(
            stdout=[
                r"^Sending the following test indication:$",
                r"^instance of ",
                r"^Sent test indication #1 to listener lis1 at ",
                r"^Sent test indication #2 to listener lis1 at ",
            ],
            test='contains',
        ),
        RUN_NO_WIN,
    ),
    (
        "Verify 'test' with one http listener running and invalid --count 0",
        dict(
            args=['test', 'lis1', '--count', '0'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001'],
            ]
        ),
        dict(
            rc=1,
            stderr=[
                r"^Error: Invalid count specified: 0$",
            ],
            test='all',
        ),
        RUN_NO_WIN,
    ),
]


@pytest.mark.parametrize(
    "desc, inputs, exp_results, condition",
    TEST_TESTCASES
)
def test_lis_test(desc, inputs, exp_results, condition):
    """
    Test the 'pywbemlistener test' command.
    """
    pywbemlistener_test(desc, inputs, exp_results, condition)
