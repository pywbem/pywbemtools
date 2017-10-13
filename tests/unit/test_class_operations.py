#!/usr/bin/env python

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
Prototype test of using mock to enable tests of pywbemcli
"""
from __future__ import absolute_import, print_function

import unittest
from mock import Mock
from click.testing import CliRunner
from pywbemcli import cli

from pywbem import CIMClass, CIMProperty, WBEMConnection, CIMError

# mock get_class
def getclass():

    # Initialise with properties

    c = CIMClass('CIM_Foo', properties={'InstanceID':
                                        CIMProperty('InstanceID', None,
                                                    type='string')})
    return c

#
#   Prototype mocking
#
class FakedWBEMConnection(WBEMConnection):
    """
    A faked Session class for the zhmcclient package, that can be used as a
    replacement for the :class:`zhmcclient.Session` class.

    Implement mock of _methodcall and _imethodclall as the place to catch
    operations and return results.
    """
    pass

class ClassOperationTests(unittest.TestCase):
    """
    Test Class subcommand functions.
    """
    def test_help(self):
        """
        Test the class get help function.
        """
        runner = CliRunner()
        result = runner.invoke(cli, ['-h'])
        assert result.exit_code == 0
        print(result.output)

    def test_class_help(self):
        """
        Test the class get help function. Not a mock, just executes
        pywbemcli class get -h. This works
        """
        runner = CliRunner()
        result = runner.invoke(cli, ['class', 'get', '-h'])
        assert result.exit_code == 0
        print(result.output)

    def test_class_get_class(self):
        """
        Test the class get help function. This is NOT a mock test. Should
        return exception
        """
        runner = CliRunner()
        result = runner.invoke(cli, ['-s http://blah', 'class', 'get', 'CIM_x'])
        print(result)
        assert result.exception

    def test_mock_get_class(self):
        """
        Test mocking wbemconnection getClass accessed through pywbemtools
        class get

        test using Mock directly and returning a class.

        Currently fails  result <Result SystemExit(1,)>
        """
        real = WBEMConnection('http://blah')
        test_class = getclass()
        real._methodcall = Mock(name="_methodcall", side_effect=test_class)
        #real._methodcall.return_value = getclass()

        runner = CliRunner()
        result = runner.invoke(cli, ['-s http://localhost', 'class', 'get',
                                     'CIM_blah'])
        print('result %r' % result)
        assert result.exit_code == 0
        print(result.output)

if __name__ == '__main__':
    unittest.main()
