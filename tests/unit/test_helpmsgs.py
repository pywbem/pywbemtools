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

from __future__ import print_function, absolute_import
import unittest
from re import findall
from subprocess import Popen, PIPE
import six


# Map of all tests to be defined.
# each test is defined as
#   name,
#   list of:
#       list of components of pywbemcli help function to execute
#       list of text pieces that must be in result
# TODO ks Mar 17 Some day we should match the entire test result but lets keep
#    it simple until code stabilizes.
TESTS_MAP = {  # pylint: disable=invalid-name
    'top': ["", ['--server', '--default_namespace']],
    "class": ["class", ['get', 'invokemethod']],
    "classget": ["class get", ['localonly', 'propertylist']],
    "classenum": ["class enumerate", []],
    "classassoc": ["class associators", []],
    "classref": ["class references", []],
    "classinvoke": ["class invokemethod", []],
    "classfind": ["class find", []],
    "classhier": ["class hierarchy", []],

    "instance": ["instance", ['associators', 'references', 'get',
                              'create', 'delete', 'invoke', 'query']],
    "instget": ["instance get", ['-p', '--propertylist']],
    "instcreate": ["instance create", []],
    "instdelete": ["instance delete", []],
    "instinvok": ["instance invokemethod", []],
    "instquery": ["instance query", []],
    "instnames": ["instance names", []],
    "instenum": ["instance enumerate", []],
    "instcount": ["instance count", []],
    "instref": ["instance references", []],
    "instassoc": ["instance associators", []],

    "qualifier": ["qualifier", []],
    "qualenum": ["qualifier enumerate", []],
    "qualget": ["qualifier get", []],

    "server": ["server", []],
    "serverbrand": ["server brand", []],
    "serverconn": ["server connection", []],
    "serverinfo": ["server info", []],
    "serverns": ["server namespaces", []],
    "serverinterop": ["server interop", []],
    "serverprof": ["server profiles", []],

    "connection": ["connection", ['show', 'export', 'set']],
    "connectionshow": ["connection show", []],
    "connectionexport": ["connection export", []],
    "connectionset": ["connection set", []],
    "connectionlist": ["connection list", []],
    "connectiondelete": ["connection delete", []],
    "connectioncreate": ["connection create", []], }


class ContainerMeta(type):
    """Class to define the function to generate test instances"""

    def __new__(mcs, name, bases, dict):  # pylint: disable=redefined-builtin

        def gen_test(test_name, cmd_str, result_data):
            """
            Defines the test method that we generate for each test
            and returns the method.

            Each test builds the pywbemcli command executes it and tests the
            results
            """
            def test(self):  # pylint: disable=missing-docstring
                command = 'pywbemcli -s http://blah %s --help' % (cmd_str)
                # Disable python warnings for pywbemcli call.See issue #42
                command = 'export PYTHONWARNINGS="" && %s' % command
                proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                std_out, std_err = proc.communicate()
                exitcode = proc.returncode
                if six.PY3:
                    std_out = std_out.decode()
                    std_err = std_err.decode()

                if exitcode != 0:
                    print('exitcode %s, err %s' % (exitcode, std_err))
                self.assertEqual(exitcode, 0, ('%s: ExitCode Err, cmd="%s" '
                                               'exitcode %s' %
                                               (test_name, command, exitcode)))

                # issue 21. The following generates a deprecation warning
                # during the coverage test. Fixed.
                self.assertEqual(std_err, "", '%s stderr not empty. returned %s'
                                 % (test_name, std_err))

                for item in result_data:
                    match_result = findall(item, std_out)
                    self.assertIsNotNone(match_result,
                                         "Expecting some result")
            return test

        for tname, params in TESTS_MAP.iteritems():
            test_name = "test_%s" % tname
            dict[test_name] = gen_test(test_name, params[0], params[1])
        return type.__new__(mcs, name, bases, dict)


class TestsContainer(unittest.TestCase):
    """Container class for all tests"""
    __metaclass__ = ContainerMeta


if __name__ == '__main__':

    unittest.main()
