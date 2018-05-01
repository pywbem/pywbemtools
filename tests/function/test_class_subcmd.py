# Copyright 2017 IBM Corp. All Rights Reserved.
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
Test the class subcommand
"""

from __future__ import absolute_import, print_function
import pytest

from .utils import execute_pywbemcli, assert_rc


class TestClassGeneral(object):
    """
    Test class using pytest for the subcommands of the class subcommand
    """
    def test_help(self):
        """Test 'pywbemcli --help'"""

        # Invoke the command to be tested
        rc, stdout, stderr = execute_pywbemcli(['class', '--help'])

        assert_rc(0, rc, stdout, stderr)
        assert stdout.startswith(
            "Usage: pywbemcli class [COMMAND-OPTIONS]"), \
            "stdout={!r}".format(stdout)

        assert stderr == ""

    # @pytest.mark.skip(reason="Unfinished test")
    def test_class_error_no_server(self):
        """Test 'pywbemcli ... class getclass' when no host is provided

        This test runs against a real url so we set timeout to the mininum
        to minimize test time since the expected result is a timeout exception.
        """

        # Invoke the command to be tested
        rc, stdout, stderr = execute_pywbemcli(['-s', 'http://fred', '-t', '1',
                                                'class', 'get', 'CIM_blah'])

        assert_rc(1, rc, stdout, stderr)
        print('stderr %s' % stderr)

        assert stdout == ""
        assert stderr.startswith(
            "Error: ConnectionError"), \
            "stderr={!r}".format(stderr)
