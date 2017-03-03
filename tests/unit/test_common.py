#!/usr/bin/env python

# Copyright 2017 IBM Corp. and Inova Development Inc.
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

from pywbemcli._common import parse_wbem_uri, _create_connection, \
    filter_namelist, parse_kv_pair, split, objects_sort

from pywbem import CIMClass, CIMProperty, CIMQualifier, CIMInstance, \
    CIMInstanceName, Uint32


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
        conn = _create_connection(url, namespace='root/cimvxx', user='fred',
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


class SorterTest(unittest.TestCase):
    """Test the object sort function in _common"""

    def test_sort_classes(self):
        """Test sorting list of classes"""

        classes = []

        classes.append(CIMClass(
            'CIM_Foo', properties={'InstanceID':
                                   CIMProperty('InstanceID', None,
                                               type='string')}))
        classes.append(CIMClass(
            'CIM_Boo', properties={'InstanceID':
                                   CIMProperty('InstanceID', None,
                                               type='string')}))
        classes.append(CIMClass(
            'CID_Boo', properties={'InstanceID':
                                   CIMProperty('InstanceID', None,
                                               type='string')}))
        sorted_rslt = objects_sort(classes)
        self.assertEqual(len(classes), len(sorted_rslt))
        self.assertEqual(sorted_rslt[0].classname, 'CID_Boo')
        self.assertEqual(sorted_rslt[1].classname, 'CIM_Boo')
        self.assertEqual(sorted_rslt[2].classname, 'CIM_Foo')

        classes = []
        sorted_rslt = objects_sort(classes)
        self.assertEqual(len(classes), len(sorted_rslt))

        classes = []
        sorted_rslt = objects_sort(classes)
        classes.append(CIMClass(
            'CIM_Foo', properties={'InstanceID':
                                   CIMProperty('InstanceID', None,
                                               type='string')}))
        self.assertEqual(len(classes), len(sorted_rslt))
        self.assertEqual(sorted_rslt[0].classname, 'CIM_Foo')

    def test_sort_instancenames(self):
        """Test ability to sort list of instance names"""

        inst_names = []

        kb = {'Chicken': 'Ham', 'Beans': 42}
        obj = CIMInstanceName('CIM_Foo', kb)
        inst_names.append(obj)

        kb = {'Chicken': 'Ham', 'Beans': 42}
        obj = CIMInstanceName('CIM_Boo', kb)
        inst_names.append(obj)

        kb = {'Chicken': 'Ham', 'Beans': 42}
        obj = CIMInstanceName('CID_Foo', kb)
        inst_names.append(obj)

        sorted_rslt = objects_sort(inst_names)
        self.assertEqual(len(inst_names), len(sorted_rslt))
        self.assertEqual(sorted_rslt[0].classname, 'CID_Foo')
        self.assertEqual(sorted_rslt[1].classname, 'CIM_Boo')
        self.assertEqual(sorted_rslt[2].classname, 'CIM_Foo')

    def test_sort_instances(self):
        """Test sort of instances"""

        instances = []

        props = {'Chicken': CIMProperty('Chicken', 'Ham'),
                 'Number': CIMProperty('Number', Uint32(42))}
        quals = {'Key': CIMQualifier('Key', True)}
        path = CIMInstanceName('CIM_Foo', {'Chicken': 'Ham'})

        obj = CIMInstance('CIM_Foo',
                          properties=props,
                          qualifiers=quals,
                          path=path)
        instances.append(obj)


class SplitTest(unittest.TestCase):
    """Test splitting input parameters"""

    def do_split(self, input_str, exp_result):
        """
        Common function to do the split and compare input to expected
        result.
        """
        result = split(input_str, ',')
        # print('split input %s result %s' % (input_str, result))
        self.assertEqual(result, exp_result)

    def test_split(self):
        """Define strings to split and call test function"""
        self.do_split('0,1,2,3,4,5,6',
                      ['0', '1', '2', '3', '4', '5', '6'])

        self.do_split('abc,def,jhi,klm,nop',
                      ['abc', 'def', 'jhi', 'klm', 'nop'])

        self.do_split('abc,def,jhi,klm,n\,op',
                      ['abc', 'def', 'jhi', 'klm', 'n\,op'])


if __name__ == '__main__':
    unittest.main()
