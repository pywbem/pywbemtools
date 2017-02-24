#!/usr/bin/env python
# Copyright  2017 IBM Corp. and Inova Development Inc.
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
    Execute and test the validity of the help output from pywbemcli
"""

from __future__ import print_function, absolute_import

import unittest
import re
from subprocess import Popen, PIPE
import shlex
import six


HOST = 'http://localhost'


class TestsContainer(unittest.TestCase):
    """Container class for all tests"""

    def execute_cmd(self, cmd_str, shell=None):  # pylint: disable=no-self-use
        """Execute the command defined by cmd_str and return results."""
        args = shlex.split(cmd_str)

        proc = Popen(args, stdout=PIPE, stderr=PIPE, shell=shell)
        std_out_str, std_err_str = proc.communicate()
        exitcode = proc.returncode

        # return tuple of exitcode, stdout, stderr
        return exitcode, std_out_str, std_err_str

    def class_cmd(self, params):
        """Adds the cmd name prefix and executes"""
        cmd = 'pywbemcli -s %s class %s' % (HOST, params)
        exitcode, std_out_str, std_err_str = self.execute_cmd(cmd)
        return exitcode, std_out_str, std_err_str

    def assert_not_found(self, regex, test_str):
        """ Test of find regex on multiline string.
        If regex is a list each entry is tested.
        """
        if isinstance(regex, list):
            for i in regex:
                self.assert_not_found(i, test_str)
        else:
            match = re.search(regex, test_str)
            if match:
                self.fail('Found in error search regex %s, str %s' %
                          (regex, test_str))

    def assert_found(self, regex, test_str):
        """ Test of find regex on multiline string.
        If regex is a list each entry is tested.
        """
        if isinstance(regex, list):
            for i in regex:
                self.assert_found(i, test_str)
        else:
            match = re.search(regex, test_str)
            if match is None:
                self.fail('Failed search regex %s, str %s' % (regex, test_str))

    def assertRegexp(self, regex, test_str):
        """
        This function eliminates the issue between the unittest assertRegex
        and assertRegexpMatches functions between unittiest in python 2 and 3
        """
        if six.PY3:
            # pylint: disable=no-member
            return self.assertRegex(test_str, regex)
        else:
            return self.assertRegexpMatches(test_str,
                                            regex)  # pylint: disable=no-member


class ClassTests(TestsContainer):
    """Test operations in the class group"""

    def test_get_simple(self):
        """ """
        print('get_simple')
        exitcode, out, err = self.class_cmd('get CIM_ManagedElement')

        self.assertEqual(exitcode, 0)
        self.assert_found('CIM_ManagedElement', out)

    def test__get_localonly(self):
        """ """
        exitcode, out, err = self.class_cmd('get CIM_ManagedElement -l')

        self.assertEqual(exitcode, 0)
        self.assert_found('CIM_ManagedElement', out)

        exitcode, out, err = self.class_cmd(
            'get CIM_ManagedElement --localonly')

        self.assertEqual(exitcode, 0)
        self.assert_found('CIM_ManagedElement', out)

    def test_get_no_includequalifiers(self):
        """ """
        exitcode, out, err = self.class_cmd(
            'get CIM_ManagedElement --no_includequalifiers')

        self.assertEqual(exitcode, 0)
        self.assert_found('CIM_ManagedElement', out)

    def test_propertylist(self):
        """Test property list on the get"""
        exitcode, out, err = self.class_cmd(
            'get CIM_ManagedElement -p InstanceID')
        self.assertEqual(exitcode, 0)
        self.assert_found(['class CIM_ManagedElement', 'InstanceID'], out)

        exitcode, out, err = self.class_cmd(
            'get CIM_ManagedElement -p InstanceID -p Caption')
        self.assertEqual(exitcode, 0)
        self.assert_found('class CIM_ManagedElement', out)
        self.assert_found('InstanceID', out)
        self.assert_found('Caption', out)

        exitcode, out, err = self.class_cmd(
            'get CIM_ManagedElement -p ""')
        self.assertEqual(exitcode, 0)
        self.assert_found('class CIM_ManagedElement', out)
        self.assert_not_found(['InstanceID','Caption'], out )
      

# TODO finish this based on the test_ops in the tools directory

# cmd "class get CIM_ManagedElement -c"
# cmd "class get CIM_ManagedElement --includeclassorigin"
# cmd "class get CIM_ManagedElement --namespace root/PG_Interop"

# TODO create tests for instance, qualifier, server


if __name__ == '__main__':

    unittest.main()
