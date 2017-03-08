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
# from pprint import pprint as pp  # noqa: F401
import click


from pywbem import CIMClass, CIMProperty, CIMQualifier, CIMInstance, \
    CIMInstanceName, Uint32
from pywbemcli._common import parse_cim_namespace_str, _create_connection, \
    filter_namelist, parse_kv_pair, split_array_value, objects_sort, \
    create_ciminstance, compare_instances, resolve_propertylist


class PropertyListResolveTest(unittest.TestCase):
    """
    Test the propertylist resolve function"""
    def test_with_comma(self):
        out = resolve_propertylist(("abc,def",))
        self.assertEqual(out, ['abc', 'def'])

    def test_simple(self):
        val = ("abc",)
        out = resolve_propertylist(val)
        self.assertEqual(out, ['abc'])

    def test_empty(self):
        val = ("",)
        out = resolve_propertylist(val)
        self.assertEqual(out, [])

    def test_multiple(self):
        out = resolve_propertylist(("abc", "def"))
        self.assertEqual(out, ['abc', 'def'])

    def test_combined(self):
        out = resolve_propertylist(("abc", "def", "xyz,rst"))
        self.assertEqual(out, ['abc', 'def', 'xyz', 'rst'])

    def test_none(self):
        out = resolve_propertylist(None)
        self.assertEqual(out, None)


class ParseWbemUriTest(unittest.TestCase):
    """test the fparse_wbem_uri function"""

    def test_one(self):
        """test simple uri input"""
        uri = 'testclass.abc=3'
        inst_name = parse_cim_namespace_str(uri)
        # test resulting ciminstancename object
        self.assertEqual(inst_name.classname, 'testclass')
        self.assertTrue(inst_name.has_key('abc'))  # noqa: W601
        self.assertEqual(inst_name.get('abc'), 3)

    def test_two(self):
        """test simple uri input"""
        uri = 'testclass2.abc=3,def=blah'
        inst_name = parse_cim_namespace_str(uri)
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
        self.assertEqual(value, None)

        name, value = parse_kv_pair('abc')
        self.assertEqual(name, 'abc')
        self.assertEqual(value, None)

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
        props = {'Chicken': CIMProperty('Chicken', 'Ham'),
                 'Number': CIMProperty('Number', Uint32(42))}
        quals = {'Key': CIMQualifier('Key', True)}
        path = CIMInstanceName('CIM_Boo', {'Chicken': 'Ham'})

        obj = CIMInstance('CIM_Boo',
                          properties=props,
                          qualifiers=quals,
                          path=path)
        instances.append(obj)
        instances_sorted = objects_sort(instances)

        self.assertEqual(len(instances), len(instances_sorted))
        self.assertEqual(instances_sorted[0].classname, 'CIM_Boo')
        # TODO create multiple and test result


class SplitTestNone(unittest.TestCase):
    """Test splitting input parameters"""

    def do_split(self, input_str, exp_result):
        """
        Common function to do the split and compare input to expected
        result.
        """
        act_result = split_array_value(input_str, ',')
        # print('split input %s result %s' % (input_str, result))
        self.assertEqual(exp_result, act_result)

    def test_split(self):
        """Define strings to split and call test function"""
        self.do_split('0,1,2,3,4,5,6',
                      ['0', '1', '2', '3', '4', '5', '6'])

        self.do_split('abc,def,jhi,klm,nop',
                      ['abc', 'def', 'jhi', 'klm', 'nop'])

        self.do_split('abc,def,jhi,klm,n\,op',
                      ['abc', 'def', 'jhi', 'klm', 'n\,op'])

        # self.do_split('abc,de f', ['abc','de f'])


class KVPairParsingTest(unittest.TestCase):
    "Test parsing key/value pairs on input"

    def execute_test(self, test_string, exp_name, exp_value):
        """Execute the function and test result"""

        act_name, act_value = parse_kv_pair(test_string)

        self.assertEqual(exp_name, act_name, ' KVPairParsing. Expected '
                         ' name=%s, function returned %s' % (exp_name,
                                                             act_name))
        self.assertEqual(exp_value, act_value, ' KVPairParsing. Expected '
                         ' value=%s, act value=%s' % (exp_value, act_value))

    def test_scalar_int(self):
        """Test for scalar integer value"""
        self.execute_test('prop_name=1', 'prop_name', str(1))
        self.execute_test('prop_name=91999', 'prop_name', str(91999))


class CreateCIMInstanceTest(unittest.TestCase):
    """Test the function that creates a CIMInstance from cli args"""

    def execute_test(self, test_string, exp_inst):
        """Creates instance from input and compares with exp_inst"""
        pass

    @staticmethod
    def create_scalar_class():
        """
        Create and return a class of scalar properties of all types
        except embedded instance and return the class
        """
        cls = CIMClass(
            'CIM_Foo', properties={'ID': CIMProperty('ID', None,
                                                     type='string'),
                                   'Boolp': CIMProperty('Boolp', None,
                                                        type='boolean'),
                                   'Uint8p': CIMProperty('Uint8p', None,
                                                         type='uint8'),
                                   'Sint8p': CIMProperty('Sint8p', None,
                                                         type='sint8'),
                                   'Uint16p': CIMProperty('Uint16p', None,
                                                          type='uint16'),
                                   'Sint16p': CIMProperty('Sint16p', None,
                                                          type='sint16'),
                                   'Uint32p': CIMProperty('Uint32p', None,
                                                          type='uint32'),
                                   'Sint32p': CIMProperty('Sint32p', None,
                                                          type='sint32'),
                                   'Uint64p': CIMProperty('Uint64p', None,
                                                          type='uint64'),
                                   'Sint64p': CIMProperty('Sint64p', None,
                                                          type='sint64'),
                                   'Real32p': CIMProperty('Real32p', None,
                                                          type='real32'),
                                   'Real64p': CIMProperty('Real64p', None,
                                                          type='real64'),
                                   'Dtp': CIMProperty('Dtp', None,
                                                      type='datetime'),
                                   'Strp': CIMProperty('Strp', None,
                                                       type='string')})
        return cls

    @staticmethod
    def create_array_class():
        """
        Create and return a class of scalar properties of all types
        except embedded instance and return the class
        """
        cls = CIMClass(
            'CIM_Foo', properties={'ID': CIMProperty('ID', None,
                                                     type='string'),
                                   'Boolp': CIMProperty('Boolp', None,
                                                        is_array=True,
                                                        type='boolean'),
                                   'Uint8p': CIMProperty('Uint8p', None,
                                                         is_array=True,
                                                         type='uint8'),
                                   'Sint8p': CIMProperty('Sint8p', None,
                                                         is_array=True,
                                                         type='sint8'),
                                   'Uint16p': CIMProperty('Uint16p', None,
                                                          is_array=True,
                                                          type='uint16'),
                                   'Sint16p': CIMProperty('Sint16p', None,
                                                          is_array=True,
                                                          type='sint16'),
                                   'Uint32p': CIMProperty('Uint32p', None,
                                                          is_array=True,
                                                          type='uint32'),
                                   'Sint32p': CIMProperty('Sint32p', None,
                                                          is_array=True,
                                                          type='sint32'),
                                   'Uint64p': CIMProperty('Uint64p', None,
                                                          is_array=True,
                                                          type='uint64'),
                                   'Sint64p': CIMProperty('Sint64p', None,
                                                          is_array=True,
                                                          type='sint64'),
                                   'Real32p': CIMProperty('Real32p', None,
                                                          is_array=True,
                                                          type='real32'),
                                   'Real64p': CIMProperty('Real64p', None,
                                                          is_array=True,
                                                          type='real64'),
                                   'Dtp': CIMProperty('Dtp', None,
                                                      is_array=True,
                                                      type='datetime'),
                                   'Strp': CIMProperty('Strp', None,
                                                       is_array=True,
                                                       type='string')})
        return cls

    def test_simple_scalar_instance(self):
        """Test scalar with one property"""
        cls = CreateCIMInstanceTest.create_scalar_class()

        exp_properties = {'ID': CIMProperty('ID', 'Testid', type='string')}
        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)
        kv_properties = ['ID=Testid']
        act_inst = create_ciminstance(cls, kv_properties)
        # pp(act_inst)
        self.assertEqual(exp_inst, act_inst)

    # TODO add datetime property
    def test_scalar_instance(self):
        """
        Creates an instance from cmd line parameters and tests against
        predefined instance
        """
        cls = CreateCIMInstanceTest.create_scalar_class()

        exp_properties = {'ID': CIMProperty('ID', 'Testid', type='string'),
                          'Boolp': CIMProperty('Boolp', True),
                          'Uint8p': CIMProperty('Uint8p', 220, type='uint8'),
                          'Sint8p': CIMProperty('Sint8p', -120, type='sint8'),
                          'Uint32p': CIMProperty('Uint32p', 999, type='uint32'),
                          'Sint32p': CIMProperty('Sint32p', -99, type='sint32'),
                          'Uint64p': CIMProperty('Uint64p', 999, type='uint64'),
                          'Sint64p': CIMProperty('Sint64p', -99, type='sint64'),

                          'Strp': CIMProperty('Strp', 'hoho', type='string')}
        # pp(exp_properties)
        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)
        # pp(exp_inst)
        kv_properties = ['ID=Testid', 'Boolp=true', 'Uint8p=220', 'Sint8p=-120',
                         'Uint32p=999', 'Sint32p=-99', 'Uint64p=999',
                         'Sint64p=-99', 'Strp=hoho']
        act_inst = create_ciminstance(cls, kv_properties)
        # pp(act_inst)
        self.assertTrue(compare_instances(exp_inst, act_inst))

        self.assertEqual(exp_inst, act_inst)

    def test_simple_scalar_two_prop(self):
        """Test scalar with two property"""
        cls = CreateCIMInstanceTest.create_scalar_class()

        exp_properties = {'ID': CIMProperty('ID', 'Testid', type='string'),
                          'Boolp': CIMProperty('Boolp', False)}
        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)
        kv_properties = ['ID=Testid', 'Boolp=false']
        act_inst = create_ciminstance(cls, kv_properties)
        # pp(act_inst)
        self.assertTrue(compare_instances(exp_inst, act_inst))
        self.assertEqual(exp_inst, act_inst)

    def test_simple_scalar_type_err(self):
        """Test scalar with two property"""
        cls = CreateCIMInstanceTest.create_scalar_class()

        try:
            kv_properties = ['Boolp=123']
            create_ciminstance(cls, kv_properties)
            self.fail('Expected exception to create_instance property type err')
        except click.ClickException:
            pass

        try:
            kv_properties = ['uint32p=shouldnotbestring']
            create_ciminstance(cls, kv_properties)
            self.fail('Expected exception to create_instance property with '
                      'value err')
        except click.ClickException:
            pass

    def test_simple_scalar_real(self):
        """Test scalar with two property"""
        cls = CreateCIMInstanceTest.create_scalar_class()

        exp_properties = {'ID': CIMProperty('ID', 'Testid', type='string'),
                          'Real32p': CIMProperty('Real32p', 1.99,
                                                 type='real32')}
        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)
        kv_properties = ['ID=Testid', 'Real32p=1.99']
        act_inst = create_ciminstance(cls, kv_properties)
        # pp(act_inst)
        self.assertTrue(compare_instances(exp_inst, act_inst))
        self.assertEqual(exp_inst, act_inst)

    # TODO test no properties, test property with no value

    def test_array_small_instance(self):
        """
        Creates an instance from cmd line parameters and tests against
        predefined instance
        """
        cls = CreateCIMInstanceTest.create_array_class()

        exp_properties = {'ID': CIMProperty('ID', 'Testid', type='string'),
                          'Boolp': CIMProperty('Boolp', [True, False])}

        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)

        kv_properties = ['ID=Testid', 'Boolp=true,false']
        act_inst = create_ciminstance(cls, kv_properties)

        self.assertEqual(exp_inst, act_inst)

    # TODO add datetime property
    def test_array_instance(self):
        """
        Creates an instance from cmd line parameters and tests against
        predefined instance
        """
        cls = CreateCIMInstanceTest.create_array_class()

        exp_properties = {'ID': CIMProperty('ID', 'Testid', type='string'),
                          'Boolp': CIMProperty('Boolp', [True, False]),
                          'Uint8p': CIMProperty('Uint8p',
                                                [0, 12, 120], type='uint8'),
                          'Sint8p': CIMProperty('Sint8p',
                                                [-120, 0, 119], type='sint8'),
                          'Uint32p': CIMProperty('Uint32p',
                                                 [0, 999], type='uint32'),
                          'Sint32p': CIMProperty('Sint32p',
                                                 [-99, 0, 9999], type='sint32'),
                          'Uint64p': CIMProperty('Uint64p', [0, 999, 99999],
                                                 type='uint64'),
                          'Sint64p': CIMProperty('Sint64p', [-99, 0, 12345],
                                                 type='sint64'),
                          'Strp': CIMProperty('Strp', ['hoho', 'haha'],
                                              type='string')}
        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)
        kv_properties = ['ID=Testid', 'Boolp=true,false', 'Uint8p=0,12,120',
                         'Sint8p=-120,0,119',
                         'Uint32p=0,999', 'Sint32p=-99,0,9999',
                         'Uint64p=0,999,99999',
                         'Sint64p=-99,0,12345', 'Strp=hoho,haha']

        act_inst = create_ciminstance(cls, kv_properties)
        # compare_instances(exp_inst, act_inst)
        self.assertEqual(exp_inst, act_inst,
                         'test_array_instance failed compare')

    def test_scalar_no_value(self):
        """Test scalar with one property"""
        cls = CreateCIMInstanceTest.create_array_class()

        exp_properties = {'ID': CIMProperty('ID', None, type='string')}
        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)
        kv_properties = ['ID=']
        act_inst = create_ciminstance(cls, kv_properties)
        self.assertTrue(compare_instances(exp_inst, act_inst))
        self.assertEqual(exp_inst, act_inst)

    def test_scalar_empty_str(self):
        """Test scalar with one property"""
        cls = CreateCIMInstanceTest.create_array_class()

        exp_properties = {'ID': CIMProperty('ID', '""', type='string')}
        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)
        kv_properties = ['ID=""']
        act_inst = create_ciminstance(cls, kv_properties)
        self.assertTrue(compare_instances(exp_inst, act_inst))
        self.assertEqual(exp_inst, act_inst)

    # TODO create one that causes keyerror

    # Test compare and failure in compare_obj

    # Test compare with errors

    # test display functionality including table

    # test Context class


if __name__ == '__main__':
    unittest.main()
