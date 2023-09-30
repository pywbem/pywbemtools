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
Test the 'pywbemlistener start' command.
"""

from __future__ import absolute_import, print_function

import pytest

from .cli_test_extensions import pywbemlistener_test, RUN, RUN_NO_WIN_NO_PY27
from ..utils import CLICK_VERSION

# pylint: disable=use-dict-literal

# Default indication format (must be in sync with actual default format)
DEFAULT_INDI_FORMAT = '{dt} {h} {i_mof}'

# Output patterns for 'pywbemlistener start --help'
START_HELP_PATTERNS = [
    r"^Usage: pywbemlistener \[GENERAL-OPTIONS\] start NAME "
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

# Output patterns for 'pywbemlistener start --help-call'
START_HELP_CALL_PATTERNS = [
    r"^Help for calling a Python function with option: +--indi-call "
    r"MODULE\.FUNCTION$",
]

# Output patterns for 'pywbemlistener start --help-format'
START_HELP_FORMAT_PATTERNS = [
    r"^Help for the format specification with option: +--indi-format FORMAT$",
]

# Output patterns for 'start' command when the listener already exists
START_EXISTS_PATTERNS = [
    r"Listener .+ already running at ",
]

# Output patterns for 'start' command when the listener was successfully started
START_SUCCESS_LOG_PATTERNS = [
    r"Run process( [0-9]+)?: Output is logged",
]

START_TESTCASES = [

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

    # Test help options
    (
        "Verify output of 'start --help'",
        dict(
            args=['start', '--help'],
        ),
        dict(
            stdout=START_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'start -h'",
        dict(
            args=['start', '-h'],
        ),
        dict(
            stdout=START_HELP_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'start --help-call'",
        dict(
            args=['start', '--help-call'],
        ),
        dict(
            stdout=START_HELP_CALL_PATTERNS,
            test='contains',
        ),
        RUN,
    ),
    (
        "Verify output of 'start --help-format'",
        dict(
            args=['start', '--help-format'],
        ),
        dict(
            stdout=START_HELP_FORMAT_PATTERNS,
            test='contains',
        ),
        RUN,
    ),

    # Test starting listeners with http and https
    (
        "Verify failure of 'start' with invalid scheme",
        dict(
            args=['start', 'lis1', '--scheme', 'badscheme'],
        ),
        dict(
            rc=2,
            stderr=[r"Invalid value for .*--scheme.: " +
                    r"invalid choice: badscheme"
                    if CLICK_VERSION < (8, 0) else
                    r"'badscheme' is not one of 'http', 'https'"],
            test='contains',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify failure of 'start' on existing listener",
        dict(
            args=['start', 'lis1', '--scheme', 'http', '--port', '50001'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50000'],
            ]
        ),
        dict(
            rc=1,
            stderr=START_EXISTS_PATTERNS,
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify success of 'start' on non-existing listener with http",
        dict(
            args=['start', 'lis1', '--scheme', 'http', '--port', '50001'],
        ),
        dict(
            stdout=[''],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify success of 'start' on non-existing listener with http and "
        "bind addr",
        dict(
            args=['start', 'lis1', '--scheme', 'http', '--bind-addr', '0.0.0.0',
                  '--port', '50001'],
        ),
        dict(
            stdout=[''],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify failure of 'start' with invalid bind host name and http,",
        dict(
            args=['start', 'lis1', '--scheme', 'http', '--bind-addr',
                  'nosuchserver', '--port', '50001'],
        ),
        dict(
            rc=1,
            # Note: Text returned is implementation dependent
            stderr=[r"Cannot start listener .+: .*"],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify failure of 'start' with invalid bind addr ip address",
        dict(
            args=['start', 'lis1', '--scheme', 'http', '--bind-addr',
                  '99.99.99.99', '--port', '50001'],
        ),
        dict(
            rc=1,
            # Note: Text of error is system dependent. word assign is common
            stderr=[r"Cannot start listener .+: .*assign.*"],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify failure of 'start' on non-existing listener with https without "
        "specifying a certificate or key file",
        dict(
            args=['start', 'lis1', '--scheme', 'https', '--port', '50001'],
        ),
        dict(
            rc=1,
            stderr=[r"Cannot create listener .+: "
                    r"https_port requires certfile"],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify failure of 'start' on non-existing listener with https with "
        "a non-existing certificate file",
        dict(
            args=['start', 'lis1', '--scheme', 'https', '--port', '50001',
                  '--certfile', 'nofile.pem'],
        ),
        dict(
            rc=1,
            stderr=[r"Cannot start listener .+: "
                    r"Issue opening certificate/key file"],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify failure of 'start' on non-existing listener with https and "
        "existing valid cert-only file without key file",
        dict(
            args=['start', 'lis1', '--scheme', 'https', '--port', '50001',
                  '--certfile', 'tests/certs/server_cert.pem'],
        ),
        dict(
            rc=1,
            stderr=[r"Cannot start listener .+: "
                    r"Invalid password for key file, bad key file, or bad "
                    r"certificate file"],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify success of 'start' on non-existing listener with https and "
        "existing valid certificate+key file",
        dict(
            args=['start', 'lis1', '--scheme', 'https', '--port', '50001',
                  '--certfile', 'tests/certs/server_cert_key.pem'],
        ),
        dict(
            stdout=[''],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify success of 'start' on non-existing listener with https and "
        "existing valid cert-only file and valid key file",
        dict(
            args=['start', 'lis1', '--scheme', 'https', '--port', '50001',
                  '--certfile', 'tests/certs/server_cert.pem',
                  '--keyfile', 'tests/certs/server_key.pem'],
        ),
        dict(
            stdout=[''],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),

    # Test starting listeners with indication processing options and -v
    (
        "Verify success of 'start' with --indi-call on valid module.function, "
        "no log",
        dict(
            args=['-v', 'start', 'lis1', '--scheme', 'http', '--bind-addr',
                  'localhost', '--port', '50001', '--indi-call',
                  'tests.unit.pywbemlistener.indicall_display.display'],
        ),
        dict(
            stdout=[''],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify success of 'start' with --indi-call on valid module.function, "
        "with log and localhost bint addr",
        dict(
            args=['-v', '-l', '.', 'start', 'lis1', '--scheme', 'http',
                  '--bind-addr', 'localhost', '--port', '50001', '--indi-call',
                  'tests.unit.pywbemlistener.indicall_display.display'],
        ),
        dict(
            stdout=START_SUCCESS_LOG_PATTERNS,
            log=(
                'pywbemlistener_lis1.log',
                [
                    r"Opening 'run' output log file at .+",

                    r"Inserting current directory into front of Python module "
                    r"search path",
                    r"Added indication handler for calling function "
                    r"display\(\) in module tests\.unit\.pywbemlistener\."
                    r"indicall_display",

                    r"Running listener lis1 at http://localhost:50001",
                    r"Shut down listener lis1 running at "
                    r"http://localhost:50001",
                    r"Closing 'run' output log file at .+",
                ],
            ),
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify success of 'start' with --indi-call on valid module.function, "
        "with log and default bind addr",
        dict(
            args=['-v', '-l', '.', 'start', 'lis1', '--scheme', 'http',
                  '--port', '50001', '--indi-call',
                  'tests.unit.pywbemlistener.indicall_display.display'],
        ),
        dict(
            stdout=START_SUCCESS_LOG_PATTERNS,
            log=(
                'pywbemlistener_lis1.log',
                [
                    r"Opening 'run' output log file at .+",

                    r"Inserting current directory into front of Python module "
                    r"search path",
                    r"Added indication handler for calling function "
                    r"display\(\) in module tests\.unit\.pywbemlistener\."
                    r"indicall_display",

                    r"Running listener lis1 at http://:50001",
                    r"Shut down listener lis1 running at "
                    r"http://:50001",
                    r"Closing 'run' output log file at .+",
                ],
            ),
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),

    (
        "Verify failure of 'start' with --indi-call on non-existing module",
        dict(
            args=['-v', 'start', 'lis1', '--scheme', 'http',
                  '--port', '50001', '--indi-call',
                  'nomodule.display'],
        ),
        dict(
            rc=1,
            stderr=[r"Cannot import module nomodule: "
                    r"No module named .?nomodule.?"],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify failure of 'start' with --indi-call on existing module with "
        "non-existing function",
        dict(
            args=['-v', 'start', 'lis1', '--scheme', 'http',
                  '--port', '50001', '--indi-call',
                  'tests.unit.pywbemlistener.indicall_display.nofunction'],
        ),
        dict(
            rc=1,
            stderr=[r"Function nofunction\(\) not found in module "
                    r"tests\.unit\.pywbemlistener\.indicall_display"],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify failure of 'start' with --indi-call on existing module that "
        "cannot be imported",
        dict(
            args=['-v', 'start', 'lis1', '--scheme', 'http',
                  '--port', '50001', '--indi-call',
                  'tests.unit.pywbemlistener.indicall_importerror.display'],
        ),
        dict(
            rc=1,
            stderr=[r"Cannot import module tests\.unit\.pywbemlistener\."
                    r"indicall_importerror: ImportError"],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify success of 'start' with --indi-file on non-existing file, no "
        "log",
        dict(
            args=['-v', 'start', 'lis1', '--scheme', 'http',
                  '--port', '50001', '--indi-file', 'new.log'],
        ),
        dict(
            stdout=[''],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify success of 'start' with --indi-file on non-existing file, with "
        "log bind to localhost",
        dict(
            args=['-v', '-l', '.', 'start', 'lis1', '--scheme', 'http',
                  '--bind-addr', 'localhost', '--port', '50001', '--indi-file',
                  'new.log'],
        ),
        dict(
            stdout=START_SUCCESS_LOG_PATTERNS,
            log=(
                'pywbemlistener_lis1.log',
                [
                    r"Opening 'run' output log file at .+",

                    r"Added indication handler for appending to file new\.log "
                    r"with format .{df}.".format(df=DEFAULT_INDI_FORMAT),

                    r"Running listener lis1 at http://localhost:50001",
                    r"Shut down listener lis1 running at "
                    r"http://localhost:50001",
                    r"Closing 'run' output log file at .+",
                ],
            ),
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),

    # Test starting listeners with -vv and bind to localhost
    (
        "Verify success of 'start' with --vv",
        dict(
            args=['-vv', 'start', 'lis1', '--scheme', 'http', '--bind-addr',
                  'localhost', '--port', '50001'],
        ),
        dict(
            stdout=[
                r"Start process( [0-9]+)?: Starting run process as: "
                r"\['pywbemlistener', '-vv', 'run', u?'lis1', '--port', "
                r"'50001', '--scheme', 'http', "
                r"'--start-pid', '[0-9]+', "
                r"'--bind-addr', u?'localhost', "
                r"'--indi-format', u?'{df}'\]".format(df=DEFAULT_INDI_FORMAT),
                r"Start process( [0-9]+)?: Waiting for run process [0-9]+ to "
                r"complete startup",
                r"Start process( [0-9]+)?: Handling success signal .+ from "
                r"run process",
                r"Start process( [0-9]+)?: Startup of run process [0-9]+ "
                r"succeeded",
            ],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
    (
        "Verify failure of 'start' with --vv and same port as existing "
        "listener",
        dict(
            args=['-vv', 'start', 'lis2', '--scheme', 'http',
                  '--port', '50001'],
            listeners=[
                ['lis1', '--scheme', 'http', '--port', '50001'],
            ]
        ),
        dict(
            rc=1,
            stderr=[r"Error: Cannot start listener .+: "
                    r"WBEM listener port 50001 is already in use"],
            test='all',
        ),
        RUN_NO_WIN_NO_PY27,
    ),
]


@pytest.mark.parametrize(
    "desc, inputs, exp_results, condition",
    START_TESTCASES
)
def test_lis_start(desc, inputs, exp_results, condition):
    """
    Test general options of pywbemlistener.
    """
    pywbemlistener_test(desc, inputs, exp_results, condition)
