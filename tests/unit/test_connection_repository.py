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
    Execute and test the validity of the help output from pywbemcli
"""

from __future__ import absolute_import, print_function

import os
import unittest
import shlex
from re import findall
from subprocess import Popen, PIPE
import six

from pywbemcli._connection_repository import CONNECTIONS_FILE

SCRIPT_DIR = os.path.dirname(__file__)
REPO_FILE = os.path.join(SCRIPT_DIR, CONNECTIONS_FILE)


class ConnectionRepositoryTest(unittest.TestCase):
    """
    Execute shell tests to determine that connection persistence
    works
    """
    def setUp(self):
        """
        Setup for the test
        """
        if os.path.isfile(REPO_FILE):
            os.remove(REPO_FILE)

    def tearDown(self):
        """
        Delete any leftover pickle file
        """
        if os.path.isfile(REPO_FILE):
            os.remove(REPO_FILE)

    def do_test(self, command, err=None, result_regex=None):
        """
        Execute the command defined.  If err is not None, confirm that
        error received.  If result_regex is not None, test the response
        against the list of regex entries
        Return stdout
        """
        args = shlex.split(command)
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode
        if six.PY3:
            out = out.decode()
            err = err.decode()

        if not err:
            if exitcode != 0:
                print('exitcode %s, err %s' % (exitcode, err))
            self.assertEqual(exitcode, 0, ('ExitCode Err, cmd="%s" '
                                           'exitcode %s' %
                                           (command, exitcode)))

            self.assertEqual(err, "", 'stderr not empty. returned %s'
                             % (err))
        if result_regex:
            for item in result_regex:
                match_result = findall(item, out)
                self.assertIsNotNone(match_result,
                                     "Expecting some result")
        return out

    def test_simple_script(self):
        """
        Test a simple script that just shows current connections
        """
        result = ['WBEMServer uri: http://localhost']
        out = self.do_test('pywbemcli -s http://localhost connection show',
                           err=False, result_regex=result)
        print(out)

    def test_create_delete(self):
        """
        Test the creation of a connection and deletion
        """
        out = self.do_test('pywbemcli -s http://localhost '
                           'connection create blah http://junkhost',
                           err=False, result_regex=['blah', 'http://junkhost'])

        out = self.do_test('pywbemcli -s http://localhost '
                           'connection list',
                           err=False, result_regex=['blah', 'http://junkhost'])

        out = self.do_test('pywbemcli -s http://localhost '
                           'connection delete blah',
                           err=False,)

        out = self.do_test('pywbemcli -s http://localhost '
                           'connection list',
                           err=False, result_regex=['default',
                                                    'http://localhost',
                                                    'User: None'])

        # TODO this can be removed when correct persistence installed.
        print('test_create_delete stdout result:\n%s' % out)


if __name__ == '__main__':

    unittest.main()
