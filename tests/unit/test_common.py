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
Tests for _common functions. This is a mix of pytest and unittests.
TODO: Future, move all tests to pytest.
"""

from __future__ import absolute_import, print_function

from datetime import datetime
import unittest
import pytest
import click
from mock import patch

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict  # pylint: disable=import-error

from pywbem import CIMClass, CIMProperty, CIMQualifier, CIMInstance, \
    CIMQualifierDeclaration, CIMInstanceName, Uint8, Uint32, Uint64, Sint32, \
    CIMDateTime, CIMClassName
from pywbem._nocasedict import NocaseDict
from pywbemtools.pywbemcli._common import parse_wbemuri_str, \
    filter_namelist, parse_kv_pair, split_array_value, sort_cimobjects, \
    create_ciminstance, compare_instances, resolve_propertylist, \
    _format_instances_as_rows, _print_instances_as_table, is_classname, \
    pick_one_from_list, pick_multiple_from_list, hide_empty_columns, \
    verify_operation, split_str_w_esc, format_keys
# pylint: disable=unused-import
from pywbemtools.pywbemcli._context_obj import ContextObj


from tests.unit.pytest_extensions import simplified_test_function
# from tests.unit.utils import assert_lines

DATETIME1_DT = datetime(2014, 9, 22, 10, 49, 20, 524789)
DATETIME1_OBJ = CIMDateTime(DATETIME1_DT)
DATETIME1_STR = '"20140922104920.524789+000"'

OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet
SKIP = False  # mark tests that are to be skipped.


TESTCASES_ISCLASSNAME = [
    # TESTCASES for resolve_propertylist
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * name: string containing classname or instancename
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('verify is a classname',
     dict(name=u"CIM_Blah", exp_rtn=True),
     None, None, True),

    ('verify is instance name',
     dict(name=u"CIM_Blah.px=3", exp_rtn=True),
     None, None, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_ISCLASSNAME)
@simplified_test_function
def test_is_classname(testcase, name, exp_rtn):
    """Test for resolve_propertylist function"""
    # The code to be tested

    act_rtn = is_classname(name)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_FORMAT_KEYBINDINGS = [
    # TESTCASES for resolve_propertylist
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * kb: keybinding
    #   * width - integer representing width of resulting field
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify simple keybinding',
     dict(kb=NocaseDict([('kEY1', u'Ham')]),
          width=100,
          exp_rtn='kEY1="Ham"'),
     None, None, True),

    ('Verify multiple keys keybinding',
     dict(kb=NocaseDict([('kEY1', u'Ham'), ('key2', 3)]),
          width=100,
          exp_rtn='kEY1="Ham",key2=3'),
     None, None, True),

    ('Verify multiple keys binding with spaces in keys',
     dict(kb=NocaseDict([('kEY1', u'Ham and eggs'), ('key2', 'More eggs')]),
          width=100,
          exp_rtn='kEY1="Ham and eggs",key2="More eggs"'),
     None, None, True),

    ('Verify multiple keys binding multiple key types',
     dict(kb=NocaseDict([('Name', 'Foo'),
                         ('Number', Uint8(42)),
                         ('Boolean', False),
                         ('Ref', CIMInstanceName('CIM_Bar'))]),
          width=100,
          exp_rtn='Name="Foo",Number=42,Boolean=FALSE,Ref="/:CIM_Bar"'),
     None, None, True),

    ('Verify mutliple keys that fold into multiple lines',
     dict(kb=NocaseDict([('kEY1', u'Ham'), ('key2', 3)]),
          width=14,
          exp_rtn='kEY1="Ham"\nkey2=3'),
     None, None, True),

    ('Verify multiple keys binding with spaces in keys that fold',
     dict(kb=NocaseDict([('kEY1', u'Ham and eggs'), ('key2', 'More eggs')]),
          width=25,
          exp_rtn='kEY1="Ham and eggs"\nkey2="More eggs"'),
     None, None, True),

    ('Verify multiple keys binding with many keys keys without fold',
     dict(kb=NocaseDict([('k1', 1), ('k2', 2), ('k3', 3), ('k4', 4), ('k5', 5),
                         ('k6', 6), ('k7', 7), ('k8', 8)]),
          width=100,
          exp_rtn=('k1=1,k2=2,k3=3,k4=4,k5=5,k6=6,k7=7,k8=8')),
     None, None, True),

    ('Verify multiple keys binding with many keys every key folds',
     dict(kb=NocaseDict([('k1', 1), ('k2', 2), ('k3', 3), ('k4', 4), ('k5', 5),
                         ('k6', 6), ('k7', 7), ('k8', 8)]),
          width=3,
          exp_rtn=('k1=1\nk2=2\nk3=3\nk4=4\nk5=5\nk6=6\nk7=7\nk8=8')),
     None, None, True),


    ('Verify multiple keys binding with many keys keys some fold',
     dict(kb=NocaseDict([('k1', 1), ('k2', 2), ('k3', 3), ('k4', 4), ('k5', 5),
                         ('k6', 6), ('k7', 7), ('k8', 8)]),
          width=8,
          exp_rtn=('k1=1,k2=2\nk3=3,k4=4\nk5=5,k6=6\nk7=7,k8=8')),
     None, None, False),

    ('Verify multiple keys binding with spaces in keys',
     dict(kb=NocaseDict([('Name', 'Foo'),
                         ('Number', Uint8(42)),
                         ('Boolean', False),
                         ('Ref', CIMInstanceName('CIM_Bar'))]),
          width=4,
          exp_rtn='Name="Foo"\nNumber=42\nBoolean=FALSE\nRef="/:CIM_Bar"'),
     None, None, True),

    # Test no keys
    ('Verify no keys',
     dict(kb=NocaseDict(),
          width=100,
          exp_rtn=''),
     None, None, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_FORMAT_KEYBINDINGS)
@simplified_test_function
def test_format_keybindings(testcase, kb, width, exp_rtn):
    """Test for resolve_propertylist function"""
    # The code to be tested

    kbs = CIMInstanceName('blah', kb)
    act_rtn = format_keys(kbs, width)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_HIDE_EMPTY_COLUMNS = [
    # TESTCASES for hide_empty_column
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * rows: Array of strings (columns, rows)
    #   * headrs: list of strings
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify deletes nothing with integers in rows',
     dict(rows=[[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]],
          headers=['h1', 'h2', 'h3'],
          exp_rtn={'rows': [[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]],
                   'headers': ['h1', 'h2', 'h3']}),
     None, None, True),

    ('Verify deletes nothing with integers in rows',
     dict(rows=[[1, 2, 0],
                [4, 5, 0],
                [7, 8, 0]],
          headers=['h1', 'h2', 'h3'],
          exp_rtn={'rows': [[1, 2, 0],
                            [4, 5, 0],
                            [7, 8, 0]],
                   'headers': ['h1', 'h2', 'h3']}),
     None, None, True),

    ('Verify deletes nothing with strings in rows',
     dict(rows=[['1', '2', '3'],
                ['4', '5', '6'],
                ['7', '8', '9']],
          headers=['h1', 'h2', 'h3'],
          exp_rtn={'rows': [['1', '2', '3'],
                            ['4', '5', '6'],
                            ['7', '8', '9']],
                   'headers': ['h1', 'h2', 'h3']}),
     None, None, True),

    ('Verify deletes nothing with strings in rows',
     dict(rows=[['1', '2', ''],
                ['4', '5', ''],
                ['7', '8', '']],
          headers=['h1', 'h2', 'h3'],
          exp_rtn={'rows': [['1', '2'],
                            ['4', '5'],
                            ['7', '8']],
                   'headers': ['h1', 'h2']}),
     None, None, True),

    ('Verify deletes nothing with strings in rows',
     dict(rows=[['1', '2', '3'],
                ['4', '5', ''],
                ['7', '8', '']],
          headers=['h1', 'h2', 'h3'],
          exp_rtn={'rows': [['1', '2', '3'],
                            ['4', '5', ''],
                            ['7', '8', '']],
                   'headers': ['h1', 'h2', 'h3']}),
     None, None, True),

    ('Verify deletes 3rd with strings in rows',
     dict(rows=[['1', '2', None],
                ['4', '5', None],
                ['7', '8', None]],
          headers=['h1', 'h2', 'h3'],
          exp_rtn={'rows': [['1', '2'],
                            ['4', '5'],
                            ['7', '8']],
                   'headers': ['h1', 'h2']}),
     None, None, True),

    ('Verify deletes 2nd with strings in rows',
     dict(rows=[['1', None, '3'],
                ['4', None, '6'],
                ['7', None, '9']],
          headers=['h1', 'h2', 'h3'],
          exp_rtn={'rows': [['1', '3'],
                            ['4', '6'],
                            ['7', '9']],
                   'headers': ['h1', 'h3']}),
     None, None, True),

    ('Verify deletes 1st 2nd with strings in rows',
     dict(rows=[[None, None, '3'],
                [None, None, '6'],
                [None, None, '9']],
          headers=['h1', 'h2', 'h3'],
          exp_rtn={'rows': [['3'],
                            ['6'],
                            ['9']],
                   'headers': ['h3']}),
     None, None, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_HIDE_EMPTY_COLUMNS)
@simplified_test_function
def test_hide_empty_columns(testcase, rows, headers, exp_rtn):
    """Test for resolve_propertylist function"""
    # The code to be tested

    act_rtn_headrs, act_rtn_rows = hide_empty_columns(headers, rows)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn_rows == exp_rtn['rows']
    assert act_rtn_headrs == exp_rtn['headers']


TESTCASES_SPLIT_STR = [
    # TESTCASES for split_value_str
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * input_str: string to split
    #   * delimiter: split delimiter
    #   * exp_rtn: expected list of strings returned
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify simple split',
     dict(input_str="abc,def,ijk",
          delimiter=',',
          exp_rtn=['abc', 'def', 'ijk']),
     None, None, True),

    ('Verify simple split empty entry',
     dict(input_str="abc,,ijk",
          delimiter=',',
          exp_rtn=['abc', '', 'ijk']),
     None, None, True),

    ('Verify string with escape',
     dict(input_str="abc,de\\,f,ijk",
          delimiter=',',
          exp_rtn=['abc', 'de,f', 'ijk']),
     None, None, True),

    ('Verify string with double escape',
     dict(input_str="abc,de\\,f,ijk",
          delimiter=',',
          exp_rtn=['abc', 'de,f', 'ijk']),
     None, None, True),

    ('Verify string with escape that should be ignored',
     dict(input_str="abc,de\\xf,ijk",
          delimiter=',',
          exp_rtn=['abc', 'de\\xf', 'ijk']),
     None, None, True),

    ('Verify string with trailingescape that should be ignored',
     dict(input_str="abc,def,ijk\\",
          delimiter=',',
          exp_rtn=['abc', 'def', 'ijk\\']),
     None, None, True),

    ('Verify string with leading escape that should be ignored',
     dict(input_str="\\abc,def,ijk",
          delimiter=',',
          exp_rtn=['\\abc', 'def', 'ijk']),
     None, None, True),

    ('Verify string with leading escape',
     dict(input_str="\\,abc,def,ijk",
          delimiter=',',
          exp_rtn=[',abc', 'def', 'ijk']),
     None, None, True),

    ('Verify string with multiple escape',
     dict(input_str="\\,abc\\,,def,\\,ijk",
          delimiter=',',
          exp_rtn=[',abc,', 'def', ',ijk']),
     None, None, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SPLIT_STR)
@simplified_test_function
def test_split_str(testcase, input_str, delimiter, exp_rtn):
    """Test for resolve_propertylist function"""
    # The code to be tested

    act_result = [item for item in split_str_w_esc(input_str, delimiter)]

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_rtn


TESTCASES_PICK_ONE_FROM_LIST = [
    # TESTCASES for resolve_propertylist
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * options: tuple of strings defining properties
    #   * choices: list of choices to return from mock
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify returns correct choice, in this case, ZERO',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['0'], exp_rtn=u'ZERO'),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['1'], exp_rtn=u'ONE'),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE after one error',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['9', '1'],
          exp_rtn=u'ONE'),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE after multipleerror',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['9', '-1', 'a', '2'],
          exp_rtn=u'TWO'),
     None, None, OK),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PICK_ONE_FROM_LIST)
@simplified_test_function
def test_pick_one_from_list(testcase, options, choices, exp_rtn):
    """
    Test for pick_one_from_list function. Uses mock patch to define return
    values from the mock.
    """
    # setup mock for this test
    mock_function = 'pywbemtools.pywbemcli.click.prompt'
    with patch(mock_function, side_effect=choices) as mock_prompt:
        # The code to be tested
        title = "Test pick_one_from_list"
        context = ContextObj(None, None, None, None, None, None, None, None)
        act_rtn = pick_one_from_list(context, options, title)
        context.spinner.stop()
        assert mock_prompt.call_count == len(choices)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_PICK_MULTIPLE_FROM_LIST = [
    # TESTCASES for resolve_propertylist
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * options: tuple of strings defining properties
    #   * choices: item index from options that is to be chosen
    #   * exp_rtn: expected function return, a list of selected items.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # NOTE: choises must end with '' element to close the
    #       pick_multiple_from_list function.

    ('verify good choice ZERO made',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['0', ''],
          exp_rtn=[u'ZERO']),
     None, None, OK),

    ('verify good choice ONE made',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['1', ''],
          exp_rtn=[u'ONE']),
     None, None, OK),

    ('verify good choice TWO after bad choices',
     dict(options=[u'ZERO', u'ONE', u'TWO'],
          choices=['-1', '9', '3', 'a', '2', ''],
          exp_rtn=[u'TWO']),
     None, None, OK),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PICK_MULTIPLE_FROM_LIST)
@simplified_test_function
def test_pick_multiple_from_list(testcase, options, choices, exp_rtn):
    """Test for pick_one_from_list function"""
    # setup mock for this test
    mock_function = 'pywbemtools.pywbemcli.click.prompt'
    with patch(mock_function, side_effect=choices) as mock_prompt:
        # The code to be tested
        title = "test_pick_multiple_from_list"
        # context = ContextObj(None, None, None, None, None, None, None, None)
        act_rtn = pick_multiple_from_list(None, options, title)
        # context.spinner.stop()
        assert mock_prompt.call_count == len(choices)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


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


TESTCASES_COMPARE_INSTANCES = [
    # TESTCASES for resolve_propertylist
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * inst1: first instance for compare
    #   * inst2: second instance for compare
    #   * result: TODO
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('verify instances match',
     dict(inst1=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          inst2=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          result=True),
     None, None, True),

    ('verify classnames do not match',
     dict(inst1=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          inst2=CIMInstance('CIM_Foo1',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          result=False),
     None, None, True),

    ('verify property values do not match',
     dict(inst1=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          inst2=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo1', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          result=False),
     None, None, True),

    ('verify property names do not match',
     dict(inst1=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          inst2=CIMInstance('CIM_Foo',
                            properties={'Name1': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          result=False),
     None, None, True),

    ('verify classnames qualifiers do not match',
     dict(inst1=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          inst2=CIMInstance('CIM_Foo1',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          result=False),
     None, None, True),

    ('verify instances do not match diff  in number of properties',
     dict(inst1=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          inst2=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          result=False),
     None, None, True),

    ('verify instances values do not match',
     dict(inst1=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo', 'Chicken': 'Ham'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          inst2=CIMInstance('CIM_Foo',
                            properties={'Name': 'Foo', 'Chicken': 'Ham1'},
                            qualifiers={'Key': CIMQualifier('Key', True)},
                            path=CIMInstanceName('CIM_Foo', {'Name': 'Foo'})),
          result=False),
     None, None, True),

]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_COMPARE_INSTANCES)
@simplified_test_function
def test_compare_instances(testcase, inst1, inst2, result):
    """Test for _common compare_instances function"""
    # The code to be tested

    rtn = compare_instances(inst1, inst2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert rtn == result


# TODO: The mock for the following test is broken. Not sure yet how to
# fix it
TESTCASES_VERIFY_OPERATION = [
    # TESTCASES for resolve_propertylist
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * txt: Text that would be fdisplayed
    #   * abort_msg: message that outputs with abort if response is n
    #   * result: True or False
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify response y',
     dict(txt="blah",
          abort_msg=None,
          result=True),
     None, None, True),

    ('Verify response n',
     dict(txt="blahno",
          abort_msg=None,
          result=False),
     None, None, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_VERIFY_OPERATION)
@simplified_test_function
def test_verify_operation(testcase, txt, abort_msg, result):
    """
    This method mocks the click.confirm function to generate a response
    to the verify operation function
    """
    @patch('pywbemtools.pywbemcli.click.confirm', return_value=result)
    def test_verify_operation(txt, test_patch):
        return verify_operation(txt)

    # The code to be tested
    rtn = test_verify_operation(txt)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert rtn == result


# TODO: move this to pytest
class TestParseWbemUri(object):  # TODO: move this to pytest
    # pylint: disable=too-few-public-methods, useless-object-inheritance
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
        # * condition: If True the test is executed, if 'pdb' the test breaks in
        #     the debugger, otherwise the test is skipped.
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
            None, True
        ),
        (
            "class and keybinding only",
            'CIM_Foo.k1="v1"',
            None,
            dict(
                classname=u'CIM_Foo',
                namespace=None,
                keys={'k1': 'v1'},
                host=None,),
            None, True
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
            import pdb  # pylint: disable=import-outside-toplevel
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


# TODO: Future pytestify this test and the others in this file
class FilterNamelistTest(object):  # pylint: disable=useless-object-inheritance
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


# TODO: move this to pytest
class NameValuePairTest(object):
    # pylint: disable=too-few-public-methods, , useless-object-inheritance
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
        sorted_rslt = sort_cimobjects(classes)
        self.assertEqual(len(classes), len(sorted_rslt))
        self.assertEqual(sorted_rslt[0].classname, 'CID_Boo')
        self.assertEqual(sorted_rslt[1].classname, 'CIM_Boo')
        self.assertEqual(sorted_rslt[2].classname, 'CIM_Foo')

        classes = []
        sorted_rslt = sort_cimobjects(classes)
        self.assertEqual(len(classes), len(sorted_rslt))

        classes = []
        sorted_rslt = sort_cimobjects(classes)
        classes.append(CIMClass(
            'CIM_Foo', properties={'InstanceID':
                                   CIMProperty('InstanceID', None,
                                               type='string')}))
        self.assertEqual(len(classes), len(sorted_rslt))
        self.assertEqual(sorted_rslt[0].classname, 'CIM_Foo')

    def test_sort_classnames(self):
        """Test sorting list of list of CIMClassName"""

        cln1 = CIMClassName("whoops", host="fred", namespace="root/cimv2")
        cln2 = CIMClassName("blah", host="fred", namespace="root/cimv2")
        cln3 = CIMClassName("blah", host="john", namespace="root/cimv2")
        cln4 = CIMClassName("blah", host="fred", namespace="root/cimv3")

        clns_in = [cln1, cln2, cln3, cln4]
        clns_exp = [cln2, cln1, cln4, cln3]

        sorted_rslt = sort_cimobjects(clns_in)

        self.assertEqual(len(clns_in), len(sorted_rslt))
        self.assertEqual(sorted_rslt, clns_exp)
        for obj in sorted_rslt:
            self.assertEqual(type(obj), CIMClassName)

    def test_sort_class_ref_rtn(self):
        """
        Test the return from the class references and class associators
        commands which is a tuple of CIMCLassName and CIMClass
        """

        cl1 = (CIMClass(
            'CIM_Foo', properties={'InstanceID':
                                   CIMProperty('InstanceID', None,
                                               type='string')}))
        cl2 = (CIMClass(
            'CIM_Boo', properties={'InstanceID':
                                   CIMProperty('InstanceID', None,
                                               type='string')}))
        cl3 = (CIMClass(
            'CID_Boo', properties={'InstanceID':
                                   CIMProperty('InstanceID', None,
                                               type='string')}))

        cln1 = CIMClassName("CIM_Foo", host="fred", namespace="root/cimv2")
        cln2 = CIMClassName("CIM_Boo", host="fred", namespace="root/cimv1")
        cln3 = CIMClassName("CIM_Boo", host="john", namespace="root/cimv2")

        input_tup = [(cln1, cl1), (cln2, cl2), (cln3, cl3)]
        sorted_rslt = sort_cimobjects(input_tup)
        self.assertEqual(len(input_tup), len(sorted_rslt))
        self.assertEqual(sorted_rslt[0][0], cln2)
        self.assertEqual(sorted_rslt[1][0], cln1)
        self.assertEqual(sorted_rslt[2][0], cln3)

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

        sorted_rslt = sort_cimobjects(inst_names)
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
        instances_sorted = sort_cimobjects(instances)
        self.assertEqual(len(instances), len(instances_sorted))
        self.assertEqual(instances_sorted[0].classname, 'CIM_Boo')
        # TODO create multiple and test result

    def test_sort_qualifierdecls(self):
        """Test ability to sort list of qualifier declaractions"""

        qual_decls = []

        obj = CIMQualifierDeclaration('FooQualDecl3', 'uint32')
        qual_decls.append(obj)

        obj = CIMQualifierDeclaration('FooQualDecl2', 'uint32')
        qual_decls.append(obj)

        obj = CIMQualifierDeclaration('FooQualDecl1', 'uint32')
        qual_decls.append(obj)

        sorted_rslt = sort_cimobjects(qual_decls)
        self.assertEqual(len(qual_decls), len(sorted_rslt))
        self.assertEqual(sorted_rslt[0].name, 'FooQualDecl1')
        self.assertEqual(sorted_rslt[1].name, 'FooQualDecl2')
        self.assertEqual(sorted_rslt[2].name, 'FooQualDecl3')

    def test_sort_stringss(self):
        """Test ability to sort list of qualifier declaractions"""
        inputs = ['xyz', 'abc']
        sorted_rslt = sort_cimobjects(inputs)
        self.assertEqual(sorted_rslt, ['abc', 'xyz'])


# TODO: move this to pytest
class SplitTestNone(object):  # pylint: disable=useless-object-inheritance
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


# TODO: move this to pytest
class KVPairParsingTest(object):  # pylint: disable=useless-object-inheritance
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


# TODO; Convert this test to pytest
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


# TODO this is a pytest. param
def simple_instance(pvalue=None):
    """
    Build a simple instance to test and return that instance. If the param
    pvalue is provided it is a scalar value and the instance with just
    this property is returned.
    """
    if pvalue:
        properties = [CIMProperty("P", pvalue)]
    else:
        properties = [CIMProperty("Pbt", value=True),
                      CIMProperty("Pbf", value=False),
                      CIMProperty("Pint32", Uint32(99)),
                      CIMProperty("Pint64", Uint64(9999)),
                      CIMProperty("Pdt", DATETIME1_OBJ),
                      CIMProperty("Pstr1", u"Test String")]
    inst = CIMInstance("CIM_Foo", properties)
    return inst


def simple_instance2(pvalue=None):
    """
    Build a simple instance to test and return that instance. If the param
    pvalue is provided it is a scalar value and the instance with just
    this property is returned.
    """
    if pvalue:
        properties = [CIMProperty("P", pvalue)]
    else:
        properties = [CIMProperty("Pbt", value=True),
                      CIMProperty("Pbf", value=False),
                      CIMProperty("Puint32", Uint32(4294967295)),
                      CIMProperty("Psint32", Sint32(-2147483648)),
                      CIMProperty("Pint64", Uint64(9999)),
                      CIMProperty("Pdt", DATETIME1_OBJ),
                      CIMProperty("Pstr1", u"Test String")]
    inst = CIMInstance("CIM_Foo", properties)
    return inst


def string_instance(tst_str):
    """
    Build a CIM instance with a single property.
    """
    properties = [CIMProperty("Pstr1", tst_str)]
    inst = CIMInstance("CIM_Foo", properties)
    return inst


# Testcases for format_inst_to_table()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * args: CIMInstance(s) object to be tested and col_width field
    #   * kwargs: Dict of input args for tocimxml().
    #   * exp_xml_str: Expected CIM-XML string, as a tuple/list of parts.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_rtn: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

TESTCASES_FMT_INSTANCE_AS_ROWS = [
    (
        "Verify simple instance to table",
        dict(
            args=([simple_instance()], None),
            kwargs=dict(),
            exp_rtn=[
                ["true", "false", "99", "9999", DATETIME1_STR,
                 u'"Test String"', ]],
        ),
        None, None, True, ),

    (
        "Verify simple instance to table with col limit",
        dict(
            args=([simple_instance()], 30),
            kwargs=dict(),
            exp_rtn=[
                ["true", "false", "99", "9999", DATETIME1_STR,
                 u'"Test String"']],
        ),
        None, None, True, ),

    (
        "Verify simple instance with one string all components overflow line",
        dict(
            args=([simple_instance(pvalue="A B C D")], 4),
            kwargs=dict(),
            exp_rtn=[
                ['"A "\n"B "\n"C "\n"D"']],
        ),
        None, None, True, ),

    (
        "Verify simple instance with one string all components overflow line",
        dict(
            args=([simple_instance(pvalue="ABCD")], 4),
            kwargs=dict(),
            exp_rtn=[
                ['\n"AB"\n"CD"']],
        ),
        None, None, True, ),

    (
        "Verify simple instance with one string overflows line",
        dict(
            args=([simple_instance(pvalue="A B C D")], 8),
            kwargs=dict(),
            exp_rtn=[
                ['"A B C "\n"D"']],
        ),
        None, None, True, ),

    (
        "Verify simple instance withone unit32 max val",
        dict(
            args=([simple_instance(pvalue=Uint32(4294967295))], 8),
            kwargs=dict(),
            exp_rtn=[
                ['4294967295']],
        ),
        None, None, True, ),


    (
        "Verify simple instance with one string fits on line",
        dict(
            args=([simple_instance(pvalue="A B C D")], 12),
            kwargs=dict(),
            exp_rtn=[
                ['"A B C D"']],
        ),
        None, None, True, ),

    (
        "Verify datetime property",
        dict(
            args=([simple_instance(pvalue=DATETIME1_OBJ)], 20),
            kwargs=dict(),
            exp_rtn=[
                ['\n"20140922104920.524"\n"789+000"']],
        ),
        None, None, True, ),

    (
        "Verify datetime property",
        dict(
            args=([simple_instance(pvalue=DATETIME1_OBJ)], 30),
            kwargs=dict(),
            exp_rtn=[
                ['"20140922104920.524789+000"']],
        ),
        None, None, True, ),

    (
        "Verify integer property where len too small",
        dict(
            args=([simple_instance(pvalue=Uint32(999999))], 4),
            kwargs=dict(),
            exp_rtn=[['999999']],
        ),
        None, None, True, ),

    (
        "Verify char16 property",
        dict(
            args=([CIMInstance('P', [CIMProperty('P',
                                                 type='char16',
                                                 value='f')])], 4),
            kwargs=dict(),
            exp_rtn=[[u"'f'"]],
        ),
        None, None, True, ),

    (
        "Verify properties with no value",
        dict(
            args=([CIMInstance('P', [CIMProperty('P', value=None,
                                                 type='char16'),
                                     CIMProperty('Q', value=None,
                                                 type='uint32'),
                                     CIMProperty('R', value=None,
                                                 type='string'), ])], 4),
            kwargs=dict(),
            exp_rtn=[[u'', u'', u'']],
        ),
        None, None, True, ),

    (
        "Verify format of instance with reference property as row entry",
        dict(
            args=([CIMInstance("TST_REFPROP",
                               [CIMProperty(
                                   'P',
                                   type='reference',
                                   reference_class="blah",
                                   value=CIMInstanceName(
                                       "REF_CLN",
                                       keybindings=OrderedDict(k1='v1')))])],
                  30),
            kwargs=dict(),
            exp_rtn=[
                [u'"/:REF_CLN.k1=\\"v1\\""']],
        ),
        None, None, True, ),

]

# TODO: See line 973. We have some test duplication.


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_FMT_INSTANCE_AS_ROWS)
@simplified_test_function
def test_format_insts_as_rows(testcase, args, kwargs, exp_rtn):
    """
    Test the output of the common:format_insts_as_table function
    """

    # The code to be tested
    act_rtn = _format_instances_as_rows(*args, **kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None
    # result is list of lists.  we want to test each item in inner list

    assert len(act_rtn) == len(exp_rtn), \
        "Unexpected number of lines in test desc: {}:\n" \
        "Expected line cnt={}:\n" \
        "{}\n\n" \
        "Actual line cnt={}:\n" \
        "{}\n". \
        format(testcase.desc, len(act_rtn), '\n'.join(act_rtn),
               len(exp_rtn), '\n'.join(exp_rtn))

    assert exp_rtn == act_rtn, \
        "Unequal values for test desc: {}:\n" \
        "Expected = {}:\n" \
        "Actual   = {}:\n". \
        format(testcase.desc, exp_rtn, act_rtn)


# Testcases for format_inst_to_table()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * args: CIMInstance(s) object to be tested, col_width field, ouput_fmt
    #   * kwargs: Dict of input args for tocimxml().
    #   * exp_tbl: Expected Table to be output.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

TESTCASES_PRINT_INSTANCE_AS_TABLE = [
    (
        "Verify print of simple instance to table",
        dict(
            args=([simple_instance()], None, 'simple'),
            kwargs=dict(),
            exp_tbl=[
                'Pbt    Pbf      Pint32    Pint64  Pdt                    '
                'Pstr1\n'
                '-----  -----  --------  --------  ---------------------  '
                '-------------\n'
                'true   false        99      9999  "20140922104920.5247"'
                '  "Test String"\n'
                '                                  "89+000"\n'
            ],
        ),
        None, None, True, ),

    (
        "Verify print of simple instance to table with col limit",
        dict(
            args=([simple_instance2()], 80, 'simple'),
            kwargs=dict(),
            exp_tbl=[
                ["true", "false", "99", '"Test String"']],
        ),
        None, None, True, ),
    (
        "Verify print of instance with reference property",
        dict(
            args=([CIMInstance("CIM_Foo",
                               [CIMProperty(
                                   'P',
                                   type='reference',
                                   reference_class="blah",
                                   value=CIMInstanceName(
                                       "REF_CLN",
                                       keybindings=OrderedDict(k1='v1',
                                                               k2=32)))])],
                  80, 'simple'),
            kwargs=dict(),
            exp_tbl=[
                ["/:REF_CLN.k2=32,k1=\"v1\""]],
        ),
        None, None, True, ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PRINT_INSTANCE_AS_TABLE)
@simplified_test_function
def test_print_insts_as_table(testcase, args, kwargs, exp_tbl):
    """
    Test the output of the print_insts_as_table function. This primarily
    tests for overall format and the ability of the function to output to
    stdout. The previous test tests the row formatting and handling of
    multiple instances.
    """
    # TODO fix simplified_test_function so we can use so we capture output.
    # capsys in a builtin fixture that must be passed to this function.
    # Currently the simplified_test_function does not allow any other
    # parameters so we cannot use pytest capsys

    # The code to be tested
    _print_instances_as_table(*args, **kwargs)
    # stdout, stderr = capsys.readouterr()
    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    # assertexp_tbl, stdout, testcase.desc)


# TODO Test compare and failure in compare_obj

# TODO Test compare with errors

# NOTE: Format table is in test_tableformat.py
