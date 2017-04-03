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

import shlex
from subprocess import Popen, PIPE
from re import findall


# map of all tests to be defined.
# each test is defined as
#   name
#   list of
#     pywbemcli help function to execute
#     list of text pieces that must be in result
# TODO Some day we should match the entire test result but lets keep
#    it simple until this stabilizes.
TESTS_MAP = {  # pylint: disable=invalid-name
    'top': ["", ['--server', '--default_namespace']],
    "class": ["class", ['get', 'invokemethod']],
    "classget": ["class get", []],
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
    "serverprof": ["server profiles", []]}


class ContainerMeta(type):
    """Class to define the function to generate test instances"""

    def __new__(mcs, name, bases, dict):  # pylint: disable=redefined-builtin

        def gen_test(tname, cmd_str, result_data):
            """
            Defines the test method and returns the method.

            Test is the method for each test. Each test builds the pywbemcli
            command executes it and tests the results
            """
            def test(self):  # pylint: disable=missing-docstring
                command = 'pywbemcli %s --help' % (cmd_str)
                args = shlex.split(command)
                proc = Popen(args, stdout=PIPE, stderr=PIPE)
                out, err = proc.communicate()
                exitcode = proc.returncode

                self.assertEqual(exitcode, 0, '%s: ExitCond Err, cmd="%s" '
                                 'exitcode %s' % (tname, command, exitcode))

                # issue 21. The following generates a deprecation warning
                # during the coverage test.
                self.assertEqual(err, "", '%s stderr not empty. returned %s'
                                 % (tname, err))
                for item in result_data:
                    # print('test item:%s\n out:\n%s\n' % (item, out))
                    match_result = findall(item, out)
                    # print('match_result %s' % match_result)
                    self.assertIsNotNone(match_result,
                                         "Expecting some result")
            return test

        for tname, params in TESTS_MAP.iteritems():
            test_name = "test_%s" % tname
            # print('tname: %s cmd_str: %s, match snippets: %s' %
            #      (tname, params[0], params[1]))
            dict[test_name] = gen_test(test_name, params[0], params[1])
        return type.__new__(mcs, name, bases, dict)


class TestsContainer(unittest.TestCase):
    """Container class for all tests"""
    __metaclass__ = ContainerMeta


if __name__ == '__main__':

    unittest.main()
