# The previous statement is used by pywbemcli to force this script to be
# run at pywbemcli startup and not included in the list of --mock-server
# files that are used to build the repository.  This is a development
# test aid.
# (C) Copyright 2017 IBM Corp.
# (C) Copyright 2017 Inova Development Inc.
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
Python code to mock click.click_prompt. Returns the
value defined in RETURN_VALUE

Used to mock response from commmon_verify_operation

    This file is enabled during testing through the PYWBEMCLI_STARTUP_SCRIPT
    environment variable.
"""

from mock import Mock
import pywbemtools

RETURN_VALUE = "mypw"


def mock_prompt(msg, hide_input=True,
                confirmation_prompt=False, type=str, err=True):
    # pylint: disable=unused-argument,redefined-builtin
    """Mock function to replace pywbemcli_prompt and return a value"""
    print('MOCK_CLICK_PROMPT {}'.format(msg))
    return RETURN_VALUE


# pylint: disable=protected-access
pywbemtools.pywbemcli.click.prompt = Mock(side_effect=mock_prompt)
