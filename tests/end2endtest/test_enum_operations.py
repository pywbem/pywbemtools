# Copyright 2022 IBM Corp. All Rights Reserved.
# (C) Copyright 2022 Inova Development Inc.
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
Test of enumeration operations for characteristics that were hard to test
with mock and to confirm general results.  This includes both class and
instance enumerations.
"""

from __future__ import absolute_import, print_function

import pytest

# pylint: disable=unused-import
from .utils import server_url  # noqa: F401
# pylint: enable=unused-import
from ..unit.pywbemcli.cli_test_extensions import CLITestsBase

OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet
SKIP = False


TEST_CASES = [

    # List of testcases.
    # Each testcase is a list with the following items:
    # * desc: Description of testcase.
    # * inputs: String, or tuple/list of strings, or dict of 'env', 'args',
    #     'general', and 'stdin'. See the 'inputs' parameter of
    #     CLITestsBase.command_test() in cli_test_extensions.py for detailed
    #     documentation.
    #     The test adds the general options for --server and --noverify
    #     along with the server url form server_url.
    # * exp_response: Dictionary of expected responses (stdout, stderr, rc) and
    #     test definition (test: <testname>). See the 'exp_response' parameter
    #     of CLITestsBase.command_test() in cli_test_extensions.py for
    #     detailed documentation.
    # * condition: If True the test is executed, if 'pdb' the test breaks in the
    #     the debugger, if 'verbose' print verbose messages, if False the test
    #     is skipped.

    ['Verify enumerate classes of CIM_ManagedElement',
     {'general': [],
      'cmdgrp': 'class',
      'args': ['enumerate', 'CIM_ManagedElement']},
     {'stdout': 'CIM_ManagedElement',
      'test': 'innows'},
     OK],

    ['Verify enumerate classes of CIM_ManagedElement summary ourput',
     {'general': [],
      'cmdgrp': 'class',
      'args': ['enumerate', 'CIM_ManagedElement', '--summary']},
     {'stdout': '47 CIMClass(s) returned',
      'test': 'innows'},
     OK],

    ['Verify enumerate instances of CIM_ManagedElement and subclasses',
     {'general': [],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_ManagedElement']},
     {'stdout': ['instance of CIM_QueryCapabilities',
                 'instance of PG_UnixProcess'],
      'test': 'innows'},
     OK],

    ['Verify enumerate instances of CIM_ManagedElement table output',
     {'general': ['--output-format', 'simple'],
      'cmdgrp': 'instance',
      'args': ['enumerate', 'CIM_ManagedElement', '--no', '--di']},
     # Test for key components of multiple table output.  Note that we
     # may not in long term know exactly what is in tables or even which
     # tables exist.  We want to be sure multiple tables exist and generally
     # the properties that are displayed.
     {'stdout': ['(table # 1)',
                 'host  namespace    class key= key=',
                 'CreationClassName    Name',
                 'root/cimv2   PG_ComputerSystem  PG_ComputerSystem'],
      'test': 'innows'},
     OK],

]


class TestOperations(CLITestsBase):  # pylint: disable=too-few-public-methods
    """
    Test any of the operations defined in the TEST_CASES
    """
    @pytest.mark.parametrize(
        "desc, inputs, exp_response, condition", TEST_CASES)
    def test_execute_pywbemcli(self, desc, inputs, exp_response, condition,
                               server_url):  # noqa: F811
        # pylint: disable=redefined-outer-name

        """
        Execute pybemcli with the defined input and test output. Note that
        this includes the server_url fixture to setup the docker container
        and get the docker URL. Using the fixture name here causes the
        pylint issue.
        """
        cmd_grp = inputs['cmdgrp'] if 'cmdgrp' in inputs else ''

        # server url acquired from the server_url fixture
        inputs['general'].extend(['-s', server_url, '--no-verify', ])

        self.command_test(desc, cmd_grp, inputs, exp_response, None,
                          condition)
