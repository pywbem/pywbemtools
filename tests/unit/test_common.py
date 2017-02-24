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

from pywbemcli._common import parse_wbem_uri, create_connection, \
    filter_namelist, parse_kv_pair, escape_split, split


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


class FilterNamelistTest(unittest.TestCase):
    """Test the common filter_namelist function."""

    def test_case_insensitive(self):
        """Test case insensitive match"""
        name_list = ['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc']

        self.assertEqual(filter_namelist('TST_', name_list), ['TST_abc'])
        self.assertEqual(filter_namelist('TSt_', name_list), ['TST_abc'])
        self.assertEqual(filter_namelist('XST_', name_list), [])
        self.assertEqual(filter_namelist('CIM_', name_list), ['CIM_abc',
                                                              'CIM_def',
                                                              'CIM_123'])

    def test_case_sensitive(self):
        """Test case sensitive matches"""
        name_list = ['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc']

        self.assertEqual(filter_namelist('TSt_', name_list,
                                         ignore_case=False), [])

    def test_wildcard_filters(self):
        """Test more complex regex"""
        name_list = ['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc']
        self.assertEqual(filter_namelist(r'.*abc$', name_list), ['CIM_abc',
                                                                 'TST_abc'])
        self.assertEqual(filter_namelist(r'.*def', name_list), ['CIM_def'])


class NameValuePairTest(unittest.TestCase):
    """Test simple name value pair parser"""

    def test_simple_pairs(self):
        """Test simple pair parsing"""
        name, value = parse_kv_pair('abc=test')
        self.assertEqual(name, 'abc')
        self.assertEqual(value, 'test')

        name, value = parse_kv_pair('abc=')
        self.assertEqual(name, 'abc')
        self.assertEqual(value, '')

        name, value = parse_kv_pair('abc')
        self.assertEqual(name, 'abc')
        self.assertEqual(value, '')

        name, value = parse_kv_pair('abc=12345')
        self.assertEqual(name, 'abc')
        self.assertEqual(value, '12345')

        name, value = parse_kv_pair('abc="fred"')
        self.assertEqual(name, 'abc')
        self.assertEqual(value, '"fred"')

        name, value = parse_kv_pair('abc="fr ed"')
        self.assertEqual(name, 'abc')
        self.assertEqual(value, '"fr ed"')

        name, value = parse_kv_pair('abc="fre\"d"')
        self.assertEqual(name, 'abc')
        self.assertEqual(value, '"fre"d"')

        name, value = parse_kv_pair('=def')
        self.assertEqual(name, '')
        self.assertEqual(value, 'def')

class SplitTest(unittest.TestCase):

    def do_split(self, str):
        result = split(str, ',')
        print('split result %s' % result)
              
    def test_split(self):
        self.do_split('0,1,2,3,4,5,6')
        self.do_split('abc,def,jhi,klm,nop')
        self.do_split('abc,def,jhi,klm,n\,op')



if __name__ == '__main__':
    unittest.main()
