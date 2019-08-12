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
Defines a set of mocks to implement prompted responses that can be used
during testing.  This is NOT intended to be used beyond testing.
"""
from mock import Mock
import pywbemtools

RETURN_VALUE = None
MSG = "mock"


def mock_confirm(msg):
    """Mock function to replace pywbemcli_prompt and return a value"""
    print(MSG + msg)
    return RETURN_VALUE


def mock_prompt(msg):
    """Mock function to replace pywbemcli_prompt and return a value"""
    print(MSG + msg)
    return RETURN_VALUE


def setup_mock(mock_txt):
    """
    Set up the mock.  Creates a message that will be output
    """
    for m in mock_txt:
        name, value = m.split(':')
        global RETURN_VALUE
        global MSG
        if name == 'confirm':
            RETURN_VALUE = True if value == 'y' else False
            MSG = 'MOCK coclick.confirm (%s): ' % value
            # print('CONFIRMMOCK %s %s' % (MSG, RETURN_VALUE))
            pywbemtools.pywbemcli.click.confirm = Mock(side_effect=mock_confirm)
        if name == 'prompt':
            RETURN_VALUE = int(value)
            MSG = 'MOCK click.prompt for value(%s): ' % RETURN_VALUE
            # print('PROMPTMOCK %s %s' % (RETURN_VALUE, MSG))
            pywbemtools.pywbemcli.click.prompt = Mock(side_effect=mock_prompt)
