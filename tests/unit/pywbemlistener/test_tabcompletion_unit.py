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
Unit tests for the completer functions implemented in pywbemlistener and are
executed when the user does <TAB> and the shell or repl calls back to pywbemcli
with a partial entity (argument or option value) to get possible completion.

These unit tests just test the completer functions themselves in isolation but
not in a command line environment.
"""

from __future__ import absolute_import, print_function

import packaging.version
import pytest
import click

from pywbemtools.pywbemlistener._cmd_listener import listener_name_completer

from ..pytest_extensions import simplified_test_function

from .cli_test_extensions import ensure_no_listeners, start_listeners, \
    RUN, RUN_NOWIN

# pylint: disable=use-dict-literal

# Click version as a tuple. Used to control tab-completion features
CLICK_VERSION = packaging.version.parse(click.__version__).release
# boolean True if click version 8 or greater.
CLICK_V8 = CLICK_VERSION[0] >= 8


TESTCASES_LISTENER_NAME_COMPLETE = [
    # Testcases for pywbemlistener.listener_name_complete()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * listeners - definition of listeners to start to provide names
    #   * incomplete; the incomplete value for the listener name
    #   * ext_rtn; list of listener names to be returned
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify with partial valid incomplete name, returns good name',
     dict(listeners=[['lis1', '--scheme', 'http', '--port', '50001'],
                     ['lis2', '--scheme', 'http', '--port', '50002'],
                     ['fred', '--scheme', 'http', '--port', '50003'], ],
          incomplete="fre",
          exp_rtn=['fred']),
     None, None, RUN),

    ('Verify with empty listener name, returns list',
     dict(listeners=[['lis1', '--scheme', 'http', '--port', '50001'],
                     ['lis2', '--scheme', 'http', '--port', '50002'],
                     ['fred', '--scheme', 'http', '--port', '50003'], ],
          incomplete="",
          exp_rtn=['lis1', 'lis2', 'fred']),
     None, None, RUN),

    ('Verify with incorrect listener name, returns empty list',
     dict(listeners=[['fred', '--scheme', 'http', '--port', '50003'], ],
          incomplete="blah",
          exp_rtn=[]),
     None, None, RUN),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_LISTENER_NAME_COMPLETE)
@simplified_test_function
def test_listener_name_complete(testcase, listeners, incomplete, exp_rtn):
    """
    Unit test function for connection_name_complete() function.  This tests
    only the function and not the path through bash and pywbemcli to
    execute the function when <TAB> entered fro command line.
    """
    verbose = False

    # Ignore the test for Click  version 7
    if not CLICK_V8:
        return

    # Do not run on windows. Setup consistently timing out trying to
    # create listeners and the target shells (bash, etc. are not on windows)
    if not RUN_NOWIN:
        return

    ensure_no_listeners(verbose, 'test setup')

    start_listeners(listeners, verbose, 'test setup')

    # These parameters not used by completer function
    ctx = None
    param = None

    # Function to be tested
    rtn_items = listener_name_completer(ctx, param, incomplete)

    ensure_no_listeners(verbose, 'test teardown')

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    act_rtn_values = [item.value for item in rtn_items]
    assert sorted(act_rtn_values) == sorted(exp_rtn)
