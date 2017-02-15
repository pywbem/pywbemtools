#!/usr/bin/env python

# Copyright TODO
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
Tests for _common functions.
"""

from __future__ import absolute_import, print_function
import unittest

from pywbemcli._common import parse_wbem_uri, create_connection


class ParseWbemUriTest(unittest.TestCase):
    """test the fparse_wbem_uri function"""

    def test_one(self):
        """test simple uri input"""
        uri = 'testclass.abc=3'
        inst_name = parse_wbem_uri(uri)
        # test resulting ciminstancename object
        self.assertEqual(inst_name.classname, 'testclass')
        self.assertTrue(inst_name.has_key('abc'))  # noqa: W601
        self.assertEqual(inst_name.get('abc'), 3)

    def test_two(self):
        """test simple uri input"""
        uri = 'testclass2.abc=3,def=blah'
        inst_name = parse_wbem_uri(uri)
        # test resulting ciminstancename object
        self.assertEqual(inst_name.classname, 'testclass2')
        self.assertTrue(inst_name.has_key('abc'))  # noqa: W601
        self.assertEqual(inst_name.get('abc'), 3)
        self.assertTrue(inst_name.has_key('def'))  # noqa: W601
        self.assertEqual(inst_name.get('def'), 'blah')


# server, namespace, user=None, password=None, cert_file=None, key_file=None,
# ca_certs=None,  no_verify_cert=False
class CreateConnectionTest(unittest.TestCase):
    """Test the create_connection function"""

    def test_simple(self):
        """Test simple creation of a connection"""
        url = 'http://localhost'
        conn = create_connection(url, namespace='root/cimvxx', user='fred',
                                 password='blah')
        self.assertEqual(conn.url, url)
        self.assertEqual(conn.default_namespace, 'root/cimvxx')


if __name__ == '__main__':
    unittest.main()
