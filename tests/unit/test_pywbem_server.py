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
Unit tests for PywbemServer class methods.
"""

from __future__ import absolute_import, print_function

import unittest

from pywbemcli._pywbem_server import PywbemServer


class PywbemServerTests(unittest.TestCase):
    """ Test the PywbemServer class """

    def test_simple(self):
        """ Create the object and test values"""

        server = 'http://localhost'
        ns = 'root/cimv2'
        user = 'Fred'
        pw = 'blah'
        svr = PywbemServer(server, ns, user=user, password=pw)

        self.assertEqual(svr.server_url, server)
        self.assertEqual(svr.default_namespace, ns)
        self.assertEqual(svr.user, user)
        self.assertEqual(svr.password, pw)

        print(svr)

    def test_all_parms(self):
        server = 'http://localhost'
        ns = 'root/cimv2'
        user = 'Fred'
        pw = 'blah'
        timeout = 10
        noverify = False
        certfile = 'mycertfile.blah'
        keyfile = 'mykeys.blah'
        verbose = True

        svr = PywbemServer(server, ns, user=user, password=pw, timeout=timeout,
                           noverify=noverify, certfile=certfile,
                           keyfile=keyfile, verbose=verbose)

        self.assertEqual(svr.server_url, server)
        self.assertEqual(svr.default_namespace, ns)
        self.assertEqual(svr.user, user)
        self.assertEqual(svr.password, pw)
        self.assertEqual(svr.noverify, noverify)
        self.assertEqual(svr.certfile, certfile)
        self.assertEqual(svr.keyfile, keyfile)

    def test_all_connect(self):
        server = 'http://localhost'
        ns = 'root/cimv2'
        user = 'Fred'
        pw = 'blah'
        timeout = 10
        noverify = False
        certfile = 'mycertfile.blah'
        keyfile = 'mykeys.blah'
        verbose = True

        svr = PywbemServer(server, ns, user=user, password=pw, timeout=timeout,
                           noverify=noverify, certfile=certfile,
                           keyfile=keyfile, verbose=verbose)

        self.assertEqual(svr.server_url, server)
        self.assertEqual(svr.default_namespace, ns)
        self.assertEqual(svr.user, user)
        self.assertEqual(svr.password, pw)
        self.assertEqual(svr.noverify, noverify)
        self.assertEqual(svr.certfile, certfile)
        self.assertEqual(svr.keyfile, keyfile)

        # connect and test connection results
        svr.create_connection(False)
        self.assertEqual(svr.conn.url, server)
        self.assertEqual(svr.wbem_server.conn.url, svr.conn.url)

        # TODO test for errors


if __name__ == '__main__':
    unittest.main()
