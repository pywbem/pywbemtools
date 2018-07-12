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
Tests for _common functions.
"""

from __future__ import absolute_import, print_function

import unittest
import pytest
import click

from pywbem import CIMClass, CIMProperty, CIMQualifier, CIMInstance, \
    CIMInstanceName, Uint32
from pywbemcli._common import parse_wbemuri_str, \
    filter_namelist, parse_kv_pair, split_array_value, objects_sort, \
    create_ciminstance, compare_instances, resolve_propertylist

from tests.unit.pytest_extensions import simplified_test_function


TESTCASES_RESOLVE_PROPERTYLIST = [
    # TESTCASES for resolve_propertylist
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * pl_str: tuple of strings defining properties
    #   * exp_pl: expected list return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('verify simple property list with 2 entries',
     dict(pl_str=("abc,def",), exp_pl=['abc', 'def']),
     None, None, True),

    ('verify propertylist with single property entry',
     dict(pl_str=("abc",), exp_pl=['abc']),
     None, None, True),

    ('verify multiple properties',
     dict(pl_str=("abc", "def"), exp_pl=['abc', 'def']),
     None, None, True),

    ('verify multiple properties and both multiple in on option and multiple '
     'options.',
     dict(pl_str=None, exp_pl=None),
     None, None, True),

    ('verify multiple properties and both multiple in on option and multiple '
     'options.',
     dict(pl_str=("ab", "def", "xyz,rst"), exp_pl=['ab', 'def', 'xyz', 'rst']),
     None, None, True),


    ('verify empty propertylist',
     dict(pl_str=("",), exp_pl=[]),
     None, None, False),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_RESOLVE_PROPERTYLIST)
@simplified_test_function
def test_propertylist(testcase, pl_str, exp_pl):
    """Test for resolve_propertylist function"""
    # The code to be tested

    # wraps the test string in a tuple because that is the way the
    # propertylist option returns the list since it is a multiple type
    # option
    plist = resolve_propertylist(pl_str)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert plist == exp_pl


class TestParseWbemUri(object):
    # pylint: disable=too-few-public-methods
    """
    Test CIMClassName.from_wbem_uri().
    """

    testcases = [
        # Testcases for CIMClassName.from_wbem_uri().
        # Each testcase has these items:
        # * desc: Short testcase description.
        # * uri: WBEM URI string to be tested.
        # * ns: namespace parameter or None
        # * exp_result: Dict of all expected attributes of resulting object,
        #     if expected to succeed. Exception type, if expected to fail.
        # * exp_warn_type: Expected warning type.
        #     None, if no warning expected.
        # * condition: Condition for testcase to run.
        (
            "class and keys only case",
            '/root/cimv2:CIM_Foo.k1="v1"',
            None,
            dict(
                classname=u'CIM_Foo',
                namespace='root/cimv2',
                keys={'k1': 'v1'},
                host=None),
            None, True
        ),
        (
            "all components, normal case",
            'https://10.11.12.13:5989/root/cimv2:CIM_Foo.k1="v1"',
            None,
            dict(
                classname=u'CIM_Foo',
                namespace=u'root/cimv2',
                keys={'k1': 'v1'},
                host=u'10.11.12.13:5989'),
            None, False
        ),
    ]

    @pytest.mark.parametrize(
        "desc, uri, ns, exp_result, exp_warn_type, condition",
        testcases)
    def test_parse_wbemuri_str(
            self, desc, uri, ns, exp_result, exp_warn_type, condition):
        # pylint: disable=unused-argument, no-self-use
        """Test function for parse_wbemuri_str."""

        if not condition:
            pytest.skip("Condition for test case not met")

        if isinstance(exp_result, type) and issubclass(exp_result, Exception):
            # We expect an exception
            exp_exc_type = exp_result
            exp_attrs = None
        else:
            # We expect the code to return
            exp_exc_type = None
            exp_attrs = exp_result

        if condition == 'pdb':
            import pdb
            pdb.set_trace()

        if exp_warn_type:
            with pytest.warns(exp_warn_type) as rec_warnings:
                if exp_exc_type:
                    with pytest.raises(exp_exc_type):
                        # The code to be tested
                        obj = parse_wbemuri_str(uri)

                else:
                    # The code to be tested
                    obj = parse_wbemuri_str(uri)

            assert len(rec_warnings) == 1

        else:
            if exp_exc_type:
                with pytest.raises(exp_exc_type):

                    # The code to be tested
                    obj = parse_wbemuri_str(uri)

            else:

                # The code to be tested
                obj = parse_wbemuri_str(uri)

        if exp_attrs:
            exp_classname = exp_attrs['classname']
            exp_namespace = exp_attrs['namespace']
            exp_host = exp_attrs['host']
            exp_keybindings = exp_attrs['keys']

            assert isinstance(obj, CIMInstanceName)

            assert obj.classname == exp_classname
            assert isinstance(obj.classname, type(exp_classname))

            assert obj.namespace == exp_namespace

            assert obj.keybindings == exp_keybindings

            assert obj.host == exp_host
            assert isinstance(obj.host, type(exp_host))


# TODO pytestify this test and the others in this file
class FilterNamelistTest(object):
    """Test the common filter_namelist function."""

    name_list = ['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc']

    @pytest.mark.parametrize(
        "desc, regex, nl, match, ign_case",

        ['Verify TST_ case insensitive',
         'TST_', name_list, ['TST_abc'], True],

        ['Verify TSt_ case insensitive',
         'TSt_', name_list, ['TST_abc'], True],

        ['Verify TSt_ case insensitive',
         'TXST_', name_list, [], True],

        ['Verify TSt_ case insensitive',
         'CIM_', name_list, ['CIM_abc', 'CIM_def', 'CIM_123'], True],

        ['Verify TSt_ case sensitive',
         'TSt__', name_list, [], False],

        ['Verify wildcard filters',
         r'.*abc$', name_list, ['CIM_abc', 'TST_abc'], True],

        ['Verify wildcard filters',
         r'.*def', name_list, ['CIM_def'], True],
    )
    def test_filter_nameslist(self, desc, regex, nl, match, ign_case):
        # pylint: disable=no-self-use
        """
        Test filter_namelist function.
        """
        assert (filter_namelist(regex, nl, ignore_case=ign_case) == match), desc

    def test_case_insensitive(self):
        # pylint: disable=no-self-use
        """Test case insensitive match"""
        name_list = ['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc']

        assert filter_namelist('TST_', name_list) == ['TST_abc']
        assert filter_namelist('TSt_', name_list) == ['TST_abc']
        assert filter_namelist('XST_', name_list) == []
        assert filter_namelist('CIM_', name_list) == ['CIM_abc',
                                                      'CIM_def',
                                                      'CIM_123']

    def test_case_sensitive(self):
        # pylint: disable=no-self-use
        """Test case sensitive matches"""
        name_list = ['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc']

        assert filter_namelist('TSt_', name_list,
                               ignore_case=False) == []

    def test_wildcard_filters(self):
        # pylint: disable=no-self-use
        """Test more complex regex"""
        name_list = ['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc']
        assert filter_namelist(r'.*abc$', name_list) == ['CIM_abc',
                                                         'TST_abc']
        assert filter_namelist(r'.*def', name_list) == ['CIM_def']


class NameValuePairTest(object):  # pylint: disable=too-few-public-methods
    """Test simple name value pair parser"""

    def test_simple_pairs(self):
        # pylint: disable=no-self-use
        """Test simple pair parsing"""
        pname, value = parse_kv_pair('abc=test')
        assert pname == 'abc'
        assert value == 'test'

        pname, value = parse_kv_pair('abc=')
        assert pname == 'abc'
        assert value is None

        pname, value = parse_kv_pair('abc')
        assert pname == 'abc'
        assert value is None

        pname, value = parse_kv_pair('abc=12345')
        assert pname == 'abc'
        assert value == '12345'

        pname, value = parse_kv_pair('abc="fred"')
        assert pname == 'abc'
        assert value == '"fred"'

        pname, value = parse_kv_pair('abc="fr ed"')
        assert pname == 'abc'
        assert value == '"fr ed"'

        pname, value = parse_kv_pair('abc="fre\"d"')
        assert pname == 'abc'
        assert value == '"fre"d"'

        pname, value = parse_kv_pair('=def')
        assert pname == ''
        assert value == 'def'


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


class SplitTestNone(object):
    """Test splitting input parameters"""

    def split_test(self, input_str, exp_result):
        # pylint: disable=no-self-use
        """
        Common function to do the split and compare input to expected
        result.
        """
        act_result = split_array_value(input_str, ',')
        # print('split input %s result %s' % (input_str, result))
        assert (exp_result == act_result) % \
            'Failed split test exp %r, act %r' % (exp_result, act_result)

    def test_split(self):
        # pylint: disable=no-self-use
        """Define strings to split and call test function"""
        self.split_test('0,1,2,3,4,5,6',
                        ['0', '1', '2', '3', '4', '5', '6'])

        self.split_test('abc,def,jhi,klm,nop',
                        ['abc', 'def', 'jhi', 'klm', 'nop'])

        self.split_test('abc,def,jhi,klm,n\\,op',
                        ['abc', 'def', 'jhi', 'klm', 'n\\,op'])

        # self.split_test('abc,de f', ['abc','de f'])


class KVPairParsingTest(object):
    "Test parsing key/value pairs on input"

    def execute_test(self, test_string, exp_name, exp_value):
        # pylint: disable=no-self-use
        """Execute the function and test result"""

        act_name, act_value = parse_kv_pair(test_string)

        assert (exp_name == act_name), \
            ' KVPairParsing. Expected ' \
            ' name=%s, function returned %s' % (exp_name, act_name)
        assert (exp_value == act_value), \
            ' KVPairParsing. Expected ' \
            ' value=%s, act value=%s' % (exp_value, act_value)

    def test_scalar_int(self):
        # pylint: disable=no-self-use
        """Test for scalar integer value"""
        self.execute_test('prop_name=1', 'prop_name', str(1))
        self.execute_test('prop_name=91999', 'prop_name', str(91999))


# TODO cvt to pytest
class CreateCIMInstanceTest(unittest.TestCase):
    """Test the function that creates a CIMInstance from cli args"""

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

        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)

        kv_properties = ['ID=Testid', 'Boolp=true', 'Uint8p=220', 'Sint8p=-120',
                         'Uint32p=999', 'Sint32p=-99', 'Uint64p=999',
                         'Sint64p=-99', 'Strp=hoho']
        act_inst = create_ciminstance(cls, kv_properties)

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

    # TODO expand this to test errors for other types
    def test_simple_scalar_type_err(self):
        """Test scalar with type error"""
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
        """Test scalar with one property with no value component"""
        cls = CreateCIMInstanceTest.create_array_class()

        exp_properties = {'ID': CIMProperty('ID', None, type='string')}
        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)
        kv_properties = ['ID=']
        act_inst = create_ciminstance(cls, kv_properties)
        self.assertTrue(compare_instances(exp_inst, act_inst))
        self.assertEqual(exp_inst, act_inst)

    def test_scalar_empty_str(self):
        """Test scalar with one property where value is empty string"""
        cls = CreateCIMInstanceTest.create_array_class()

        exp_properties = {'ID': CIMProperty('ID', '""', type='string')}
        exp_inst = CIMInstance('CIM_Foo',
                               properties=exp_properties)
        kv_properties = ['ID=""']
        act_inst = create_ciminstance(cls, kv_properties)
        self.assertTrue(compare_instances(exp_inst, act_inst))
        self.assertEqual(exp_inst, act_inst)

    def test_invalid_propname(self):
        """Test scalar where input is property name not in class"""
        cls = CreateCIMInstanceTest.create_scalar_class()

        try:
            kv_properties = ['Boolpxxx=True']
            create_ciminstance(cls, kv_properties)
            self.fail('Expected exception to create_instance property type err')
        except click.ClickException:
            pass

# TODO Test compare and failure in compare_obj

# TODO Test compare with errors

# NOTE: Format table is in test_tableformat.py
