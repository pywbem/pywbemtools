# -*- coding: utf-8 -*-
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
Tests for _common.py functions.
"""

from __future__ import absolute_import, print_function

import sys
import os
import six
from packaging.version import parse as parse_version
import click
from mock import patch
from nocaselist import NocaseList
import pytest

from pywbem import CIMClass, CIMProperty, CIMQualifier, CIMInstance, \
    CIMQualifierDeclaration, CIMInstanceName, Uint8, \
    CIMClassName, CIMMethod, CIMParameter, __version__, MOFCompiler, \
    ToleratedSchemaIssueWarning

from pywbem._mof_compiler import MOFWBEMConnection


from pywbemtools.pywbemcli._common import parse_wbemuri_str, \
    filter_namelist, parse_kv_pair, split_array_value, sort_cimobjects, \
    create_ciminstance, compare_instances, resolve_propertylist, \
    is_classname, pick_one_from_list, pick_one_index_from_list, \
    pick_multiple_from_list, verify_operation, split_str_w_esc, \
    shorten_path_str, get_subclass_names, \
    dependent_classnames, depending_classnames, all_classnames_depsorted, \
    parse_version_value, is_experimental_class, to_wbem_uri_folded

from .cli_test_extensions import setup_mock_connection
from ..pytest_extensions import simplified_test_function

# pylint: disable=use-dict-literal

# from tests.unit.utils import assert_lines

OK = True     # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet
SKIP = False  # mark tests that are to be skipped.

# Click (as of 7.1.2) raises UnsupportedOperation in click.echo() when
# the pytest capsys fixture is used. That happens only on Windows.
# See Click issue https://github.com/pallets/click/issues/1590. This
# run condition skips the testcases on Windows.
CLICK_ISSUE_1590 = sys.platform == 'win32'

_PYWBEM_VERSION = parse_version(__version__)
# pywbem 1.0.0b1 or later
PYWBEM_1_0_0B1 = _PYWBEM_VERSION.release >= (1, 0, 0) and \
    _PYWBEM_VERSION.dev is None
# pywbem 1.0.0 (dev, beta, final) or later
PYWBEM_1_0_0 = _PYWBEM_VERSION.release >= (1, 0, 0)

# A mof file that defines basic qualifier decls, classes, and instances
# but not tied to the DMTF classes.
SIMPLE_MOCK_FILE = os.path.join(
    os.path.dirname(__file__), 'simple_mock_model.mof')

TESTCASES_ISCLASSNAME = [
    # Testcases for _common.is_classname()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * name: string containing classname or instancename
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify is a classname',
     dict(name=u"CIM_Blah", exp_rtn=True),
     None, None, True),

    ('Verify is instance name',
     dict(name=u"CIM_Blah.px=3", exp_rtn=True),
     None, None, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_ISCLASSNAME)
@simplified_test_function
def test_is_classname(testcase, name, exp_rtn):
    """
    Test function for _common.is_classname()
    """

    # The code to be tested
    act_rtn = is_classname(name)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_SHORTEN_PATH_STR = [
    # Testcases for _common.shorten_path_str()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * kb: keybinding
    #   * rpl - definition of replacement parameter
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify simple keybinding replacement',
     dict(kb=[('kEY1', u'Ham')],
          rpl={'kEY1': u'Ham'},
          fp=False,
          exp_rtn='/:cln.~'),
     None, None, True),

    ('Verify multiple keys keybinding, replace all',
     dict(kb=[('kEY1', u'Ham'), ('key2', 3)],
          rpl={'kEY1': u'Ham', 'key2': 3},
          fp=False,
          exp_rtn='/:cln.~,~'),
     None, None, True),

    ('Verify multiple keys keybinding, one replacement',
     dict(kb=[('kEY1', u'Ham'), ('key2', 3)],
          rpl={'kEY1': u'Ham', },
          fp=False,
          exp_rtn='/:cln.~,key2=3'),
     None, None, True),

    ('Verify multiple keys keybinding, no replacement because value different',
     dict(kb=[('kEY1', u'Ham'), ('key2', 3)],
          rpl={'kEY1': u'Hamxxxx', },
          fp=False,
          exp_rtn='/:cln.kEY1="Ham",key2=3'),
     None, None, True),

    ('Verify multiple keys keybinding, replacement because value None',
     dict(kb=[('kEY1', u'Ham'), ('key2', 3)],
          rpl={'kEY1': None, },
          fp=False,
          exp_rtn='/:cln.~,key2=3'),
     None, None, True),

    ('Verify multiple keys keybinding, replaced with tilde because values '
     'match',
     dict(kb=[('kEY1', u'Ham'), ('key2', 3)],
          rpl={'kEY1': None, 'key2': None},
          fp=False,
          exp_rtn='/:cln.~,~'),
     None, None, True),

    ('Verify multiple keys keybinding, replaced with tilde because values '
     'match',
     dict(kb=[('kEY1', u'Ham'), ('key2', 3)],
          rpl={'kEY1': u'xxx', 'key2': 3},
          fp=False,
          exp_rtn='/:cln.kEY1="Ham",~'),
     None, None, True),

    ('Verify multiple keys binding with spaces in keys',
     dict(kb=[('kEY1', u'Ham and eggs'), ('key2', 'More eggs')],
          rpl={'kEY1': u'Ham and eggs', 'key2': 'More eggs'},
          fp=False,
          exp_rtn='/:cln.~,~'),
     None, None, True),

    ('Verify multiple keys binding with spaces in keys',
     dict(kb=[('kEY1', u'Ham and eggs'), ('key2', 'More eggs')],
          rpl={'kEY1': u'Ham and eggs', 'key2': 'More eggs'},
          fp=True,
          exp_rtn='/:cln.kEY1="Ham and eggs",key2="More eggs"'),
     None, None, True),

    ('Verify multiple keys binding multiple key types',
     dict(kb=[('Boolean', False),
              ('Name', 'Foo'),
              ('Number', Uint8(42)),
              ('Ref', CIMInstanceName('CIM_Bar',
                                      keybindings={'Chicken': 'Ham'}))],
          rpl={},
          fp=False,
          exp_rtn='/:cln.Boolean=FALSE,Name="Foo",Number=42,'
          'Ref="/:CIM_Bar.Chicken=\\"Ham\\""'),
     None, None, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SHORTEN_PATH_STR)
@simplified_test_function
def test_shorten_path_str(testcase, kb, rpl, fp, exp_rtn):
    """
    Test function for _common.shorten_path_str()
    """

    inst_name = CIMInstanceName('cln', keybindings=kb)

    # The code to be tested
    act_rtn = shorten_path_str(inst_name, rpl, fp)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_SPLIT_STR_W_ESC = [
    # Testcases for _common.split_str_w_esc()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
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
    TESTCASES_SPLIT_STR_W_ESC)
@simplified_test_function
def test_split_str_w_esc(testcase, input_str, delimiter, exp_rtn):
    """
    Test function for _common.split_str_w_esc()
    """

    # The code to be tested
    act_result = list(split_str_w_esc(input_str, delimiter))

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_rtn


TESTCASES_PICK_ONE_INDEX_FROM_LIST = [
    # Testcases for _common.pick_one_from_list()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * options: tuple of strings defining properties
    #   * choices: list of choices to return from mock
    #   * pa: pickBoolean
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify returns correct choice, in this case, ZERO',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['0'], pa=False,
          exp_rtn=0),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['1'], pa=None,
          exp_rtn=1),
     None, None, OK),

    ('Verify returns correct choice, in this case TWO',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['2'], pa=None,
          exp_rtn=2),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE after one error',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['9', '1'], pa=False,
          exp_rtn=1),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE after one error',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['3', '2'], pa=False,
          exp_rtn=2),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE after multiple inputs',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['9', '-1', 'a', '2'],
          pa=False, exp_rtn=2),
     None, None, OK),

    ('Verify returns correct choice with only single choice so no usr request',
     dict(options=[u'ZERO'], choices=None, pa=False, exp_rtn=0),
     None, None, OK),

    ('Verify returns correct choice with only single choice pick_always set',
     dict(options=[u'ZERO'], choices=['0'], pa=True, exp_rtn=0),
     None, None, OK),

    ('Verify exception with empty options',
     dict(options=[], choices=None, pa=None, exp_rtn=None),
     None, None, OK),

    ('Verify returns None with None options',
     dict(options=None, choices=None, pa=None, exp_rtn=None),
     None, None, OK),

]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PICK_ONE_INDEX_FROM_LIST)
@simplified_test_function
def test_pick_one_index_from_list(testcase, options, choices, pa, exp_rtn):
    """
    Test function for _common.pick_one_index_from_list().

    Uses mock patch to define return values from the mock.
    """
    title = "Test pick_one_index_from_list"

    # test option with only one choice bypasses user request
    if not choices and not pa:

        # The code to be tested
        act_rtn = pick_one_index_from_list(None, options, title, pick_always=pa)

        # Ensure that exceptions raised in the remainder of this
        # function are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None
    else:
        # Setup mock for this test.
        # Mock the prompt with choices from the testcases as prompt response
        mock_prompt_funct = 'pywbemtools.pywbemcli.click.prompt'
        # side_effect returns next item in choices for each prompt call
        with patch(mock_prompt_funct, side_effect=choices) as mock_prompt:
            # mock the echo to hide output
            mock_echo_func = 'pywbemtools.pywbemcli.click.echo'
            with patch(mock_echo_func):

                # The code to be tested
                act_rtn = pick_one_index_from_list(None, options, title,
                                                   pick_always=pa)

                # Ensure that exceptions raised in the remainder of this
                # function are not mistaken as expected exceptions
                assert testcase.exp_exc_types is None

                assert mock_prompt.call_count == len(choices)

    assert act_rtn == exp_rtn


TESTCASES_PICK_ONE_FROM_LIST = [
    # Testcases for _common.pick_one_from_list()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * options: tuple of strings defining properties
    #   * choices: list of choices to return from mock
    #   * pa: pick_always optional parameter, boolean
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify returns correct choice, in this case, ZERO',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['0'], exp_rtn=u'ZERO',
          pa=False),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['1'], exp_rtn=u'ONE',
          pa=False),
     None, None, OK),

    ('Verify returns correct choice, in this case TWO',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['2'], exp_rtn=u'TWO',
          pa=False),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE after one error',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['9', '1'],
          exp_rtn=u'ONE', pa=False),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE after one error',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['3', '2'],
          exp_rtn=u'TWO', pa=False),
     None, None, OK),

    ('Verify returns correct choice, in this case ONE after multiple inputs',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['9', '-1', 'a', '2'],
          exp_rtn=u'TWO', pa=False),
     None, None, OK),

    ('Verify returns correct choice with only single choice so no usr request',
     dict(options=[u'ZERO'], choices=['0'], exp_rtn=u'ZERO', pa=True),
     None, None, OK),

    ('Verify returns None with empty list input',
     dict(options=[], choices=None, exp_rtn=None, pa=True),
     None, None, OK),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PICK_ONE_FROM_LIST)
@simplified_test_function
def test_pick_one_from_list(testcase, options, choices, pa, exp_rtn):
    """
    Test function for _common.pick_one_from_list().

    Uses mock patch to define return values from the mock.
    """

    title = "Test pick_one_from_list"

    # test option with only one choice bypasses user request
    if not choices:

        # The code to be tested
        act_rtn = pick_one_from_list(None, options, title, pick_always=pa)

        # Ensure that exceptions raised in the remainder of this
        # function are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None
    else:
        # Setup mock for this test.
        # Mock the prompt with choices from the testcases as prompt response
        mock_prompt_funct = 'pywbemtools.pywbemcli.click.prompt'
        # side_effect returns next item in choices for each prompt call
        with patch(mock_prompt_funct, side_effect=choices) as mock_prompt:
            # mock the echo to hide output
            mock_echo_func = 'pywbemtools.pywbemcli.click.echo'
            with patch(mock_echo_func):
                # The code to be tested
                act_rtn = pick_one_from_list(None, options, title,
                                             pick_always=pa)

                # Ensure that exceptions raised in the remainder of this
                # function are not mistaken as expected exceptions
                assert testcase.exp_exc_types is None
                assert mock_prompt.call_count == len(choices)

    assert act_rtn == exp_rtn


TESTCASES_PICK_MULTIPLE_FROM_LIST = [
    # Testcases for _common.pick_multiple_from_list()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * options: tuple of strings defining properties
    #   * choices: list of item indexes from options to be chosen rtnd from
    #     prompt. Allows chosing multiple items.
    #   * exp_rtn: expected function return, a list of selected items.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # NOTE: choises must end with '' element to close the
    #       pick_multiple_from_list function.

    ('Verify good choice ZERO made',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['0', ''],
          exp_rtn=[u'ZERO']),
     None, None, OK),

    ('Verify good choice ONE made',
     dict(options=[u'ZERO', u'ONE', u'TWO'], choices=['1', ''],
          exp_rtn=[u'ONE']),
     None, None, OK),

    ('Verify good choice TWO after bad choices',
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
    """
    Test function for _common.pick_multiple_from_list()
    """

    # setup mock for this test
    mock_clickprompt = 'pywbemtools.pywbemcli.click.prompt'
    with patch(mock_clickprompt, side_effect=choices) as mock_prompt:
        # mock the echo to hide output
        mock_echo_func = 'pywbemtools.pywbemcli.click.echo'
        with patch(mock_echo_func):
            title = "test_pick_multiple_from_list"

            # The code to be tested
            act_rtn = pick_multiple_from_list(None, options, title)

            # Ensure that exceptions raised in the remainder of this function
            # are not mistaken as expected exceptions
            assert testcase.exp_exc_types is None

            # context.spinner_stop()
            assert mock_prompt.call_count == len(choices)

    if act_rtn != exp_rtn:
        print('act {0}\nexp {1}'.format(act_rtn, exp_rtn))
    assert act_rtn == exp_rtn


TESTCASES_RESOLVE_PROPERTYLIST = [
    # Testcases for _common.resolve_propertylist()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * pl_str: tuple of strings defining properties
    #   * exp_pl: expected list return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify simple property list with 2 entries',
     dict(pl_str=("abc,def",), exp_pl=['abc', 'def']),
     None, None, OK),

    ('Verify propertylist with single property entry',
     dict(pl_str=("abc",), exp_pl=['abc']),
     None, None, OK),

    ('Verify multiple properties',
     dict(pl_str=("abc", "def"), exp_pl=['abc', 'def']),
     None, None, OK),

    ('Verify multiple properties and both multiple in one option and multiple '
     'options.',
     dict(pl_str=None, exp_pl=None),
     None, None, OK),

    ('Verify multiple properties and both multiple in on option and multiple '
     'options.',
     dict(pl_str=("ab", "def", "xyz,rst"), exp_pl=['ab', 'def', 'xyz', 'rst']),
     None, None, OK),

    ('Verify empty propertylist',
     dict(pl_str=(""), exp_pl=None),
     None, None, OK),

    ('Verify propertylist with commas and spaces fails',
     dict(pl_str=("a, b,c",), exp_pl=[]),
     click.ClickException, None, OK),

    ('Verify propertylist with commas and spaces fails',
     dict(pl_str=("a, b,c", "abc"), exp_pl=[]),
     click.ClickException, None, OK),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_RESOLVE_PROPERTYLIST)
@simplified_test_function
def test_resolve_propertylist(testcase, pl_str, exp_pl):
    """
    Test function for _common.resolve_propertylist()
    """

    # The code to be tested
    plist = resolve_propertylist(pl_str)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert plist == exp_pl


TESTCASES_COMPARE_INSTANCES = [
    # Testcases for _common.compare_instances()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * inst1: first instance for compare
    #   * inst2: second instance for compare
    #   * result: Boolean. Expect result
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify instances match',
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

    ('Verify classnames do not match',
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

    ('Verify property values do not match',
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

    ('Verify property names do not match',
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

    ('Verify classnames qualifiers do not match',
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

    ('Verify instances do not match diff  in number of properties',
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

    ('Verify instances values do not match',
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
    """
    Test function for _common.compare_instances()
    """

    mock_echo_func = 'pywbemtools.pywbemcli.click.echo'
    with patch(mock_echo_func):

        # The code to be tested
        tst_rtn = compare_instances(inst1, inst2)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert tst_rtn == result


TESTCASES_VERIFY_OPERATION = [
    # Testcases for _common.verify_operation()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * txt: Text that would be displayed
    #   * abort_msg: message that outputs with abort if response is n
    #   * result: True or False
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify response y',
     dict(txt="blah",
          clickconfirm=True,
          abort_msg=None,
          result=True),
     None, None, True),

    ('Verify response n',
     dict(txt="blahno",
          clickconfirm=False,
          abort_msg=None,
          result=False),
     None, None, True),

    ('Verify response n with msg',
     dict(txt="blahno",
          clickconfirm=False,
          abort_msg=True,
          result=False),
     None, None, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_VERIFY_OPERATION)
@simplified_test_function
def test_verify_operation(testcase, txt, clickconfirm, abort_msg, result):
    """
    Test function for _common.verify_operation()

    This method mocks the click.confirm and click_echo function to generate a
    response to the verify operation function. Mock Click.confirm returns a
    value defined by the test. Mock click.echo confirms data in call to
    click_echo
    """

    # NOTE: This does not really test the abort_msg that is output
    # in some conditions, it just hides it since the mock of echo is
    # defined with called_with=txt
    @patch('pywbemtools.pywbemcli.click.confirm', called_with=txt,
           return_value=clickconfirm)
    @patch('pywbemtools.pywbemcli.click.echo', called_with=txt)
    def run_verify_operation(txt, mock_click_confirm, mock_click_echo):

        # The code to be tested
        # pylint: disable=unused-argument
        return verify_operation(txt, abort_msg)

    # pylint: disable=no-value-for-parameter
    rtn = run_verify_operation(txt)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert rtn == result


TESTCASES_PARSE_WBEMURI_STR = [
    # Testcases for _common.parse_wbemuri_str()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * url: WBEM URI string to be tested.
    #   * exp_result: Dict of all expected attributes of resulting object,
    #     if expected to succeed. Exception type, if expected to fail.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "class and keys only case",
        dict(
            url='/root/cimv2:CIM_Foo.k1="v1"',
            exp_result=dict(
                classname=u'CIM_Foo',
                namespace='root/cimv2',
                keys={'k1': 'v1'},
                host=None),
        ),
        None, None, True
    ),

    (
        "all components, normal case",
        dict(
            url='https://10.11.12.13:5989/root/cimv2:CIM_Foo.k1="v1"',
            exp_result=dict(
                classname=u'CIM_Foo',
                namespace=u'root/cimv2',
                keys={'k1': 'v1'},
                host=u'10.11.12.13:5989'),
        ),
        None, None, True
    ),

    (
        "class and keybinding only",
        dict(
            url='CIM_Foo.k1="v1"',
            exp_result=dict(
                classname=u'CIM_Foo',
                namespace=None,
                keys={'k1': 'v1'},
                host=None,),
        ),
        None, None, True
    ),

    (
        "all components, But wbem uri invalid",
        dict(
            url='https://10.11.12.13:5989/root/cimv2:CIM_Foo.k1=v1',
            exp_result=dict(
                classname=u'CIM_Foo',
                namespace=u'root/cimv2',
                keys={'k1': 'v1'},
                host=u'10.11.12.13:5989'),
        ),
        click.ClickException, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PARSE_WBEMURI_STR)
@simplified_test_function
def test_parse_wbemuri_str(testcase, url, exp_result):
    """
    Test function for _common.parse_wbemuri_str()
    """

    # The code to be tested
    obj = parse_wbemuri_str(url)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    if exp_result:
        exp_classname = exp_result['classname']
        exp_namespace = exp_result['namespace']
        exp_host = exp_result['host']
        exp_keybindings = exp_result['keys']

        assert isinstance(obj, CIMInstanceName)

        assert obj.classname == exp_classname
        assert isinstance(obj.classname, type(exp_classname))

        assert obj.namespace == exp_namespace

        assert obj.keybindings == exp_keybindings

        assert obj.host == exp_host
        assert isinstance(obj.host, type(exp_host))


TESTCASES_FILTER_NAMELIST = [
    # Testcases for _common.filter_namelist()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * nl: List of names to filter
    #   * regex: Filter regex statement
    #   * ign_case: If True, ignore case in the match
    #   * exp_result: resulting list to match
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Verify TST_ case insensitive 1",
        dict(
            nl=['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc'],
            regex='TST_*',
            ign_case=True,
            exp_result=['TST_abc'],
        ),
        None, None, OK),
    (
        "Verify TST_ case insensitive 2. Returns nothing",
        dict(
            nl=['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc'],
            regex='TSt_*',
            ign_case=True,
            exp_result=['TST_abc'],
        ),
        None, None, OK),
    (
        "Verify TST_ case insensitive . Returns match to *abc",
        dict(
            nl=['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc'],
            regex='*abc',
            ign_case=True,
            exp_result=['CIM_abc', 'TST_abc'],
        ),
        None, None, OK),
    (
        "Verify TST_ case insensitive returns nothing",
        dict(
            nl=['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc'],
            regex='TSTX_*',
            ign_case=True,
            exp_result=[],
        ),
        None, None, OK),
    (
        "Verify TST_ case insensitive 3",
        dict(
            nl=['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc'],
            regex='CIM_*',
            ign_case=True,
            exp_result=['CIM_abc', 'CIM_def', 'CIM_123'],
        ),
        None, None, OK),
    (
        "Verify TST_ case sensitive 1",
        dict(
            nl=['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc'],
            regex='TSt_*',
            ign_case=False,
            exp_result=[],
        ),
        None, None, FAIL),  # Failing with regex compile error
    (
        "Verify wildcard * filters",
        dict(
            nl=['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc'],
            regex='*def',
            ign_case=True,
            exp_result=['CIM_def'],
        ),
        None, None, OK),
    (
        "Verify wildcard * filters 2",
        dict(
            nl=['CIM_abc', 'CIM_def', 'CIM_123', 'TST_abc'],
            regex='*abc',
            ign_case=True,
            exp_result=['CIM_abc', 'TST_abc'],
        ),
        None, None, OK),
    (
        "Verify ? wildcard",
        dict(
            nl=['CIM_abc', 'CIM_abd', 'CIM_abe', 'TST_abc'],
            regex='CIM_ab?',
            ign_case=True,
            exp_result=['CIM_abc', 'CIM_abd', 'CIM_abe'],
        ),
        None, None, OK),
    (
        "Verify ? wildcard 2",
        dict(
            nl=['CIM_abc', 'CIM_abd', 'CIM_abe', 'TST_abc'],
            regex='???_ab?',
            ign_case=True,
            exp_result=['CIM_abc', 'CIM_abd', 'CIM_abe', 'TST_abc'],
        ),
        None, None, OK),
    (
        "Verify ? and *wildcard ",
        dict(
            nl=['CIM_abc', 'CIM_abd', 'CIM_abe', 'TST_abc'],
            regex='*_ab?',
            ign_case=True,
            exp_result=['CIM_abc', 'CIM_abd', 'CIM_abe', 'TST_abc'],
        ),
        None, None, OK),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_FILTER_NAMELIST)
@simplified_test_function
def test_filter_namelist(testcase, nl, regex, exp_result, ign_case):
    """
    Test function for _common.filter_namelist()
    """

    # The code to be tested
    tst_rslt = filter_namelist(regex, nl, ignore_case=ign_case)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert tst_rslt == exp_result


TESTCASES_PARSE_KV_PAIR = [
    # Testcases for _common.parse_kv_pair()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * kvpair: String defining the key=value to be tested.
    #   * exp_name: Name expected in response.
    #   * exp_value: Value expected in response.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ("Verify unquoted text value",
     dict(kvpair='abc=test',
          exp_name='abc',
          exp_value='test'),
     None, None, True),
    ("Verify 'name='' without value",
     dict(kvpair='abc=',
          exp_name='abc',
          exp_value=None),
     None, None, True),
    ("Verify 'name' without = or value",
     dict(kvpair='abc',
          exp_name='abc',
          exp_value=None),
     None, None, True),
    ("Verify numeric value",
     dict(kvpair='abc=12345',
          exp_name='abc',
          exp_value='12345'),
     None, None, True),
    ("Verify value in quotes works",
     dict(kvpair='abc="Fred"',
          exp_name='abc',
          exp_value='"Fred"'),
     None, None, True),
    ("Verify quoted value with space",
     dict(kvpair='abc="Fr ed"',
          exp_name='abc',
          exp_value='"Fr ed"'),
     None, None, True),
    ("Verify quoted value with escaped quote",
     dict(kvpair='abc="fre\\"d"',
          exp_name='abc',
          exp_value='"fre\\"d"'),
     None, None, True),
    ("Verify value without name",
     dict(kvpair='=def',
          exp_name='',
          exp_value='def'),
     None, None, True),
    ("Verify pair, integer value",
     dict(kvpair='prop_name=91999',
          exp_name='prop_name',
          exp_value='91999'),
     None, None, True),
    ("Verify just '=', no name or value",
     dict(kvpair='=',
          exp_name='',
          exp_value=None),
     None, None, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PARSE_KV_PAIR)
@simplified_test_function
def test_parse_kv_pair(testcase, kvpair, exp_name, exp_value):
    """
    Test function for _common.parse_kv_pair()
    """

    # The code to be tested
    name, value = parse_kv_pair(kvpair)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert name == exp_name
    assert value == exp_value


TESTCASES_SORT_CIMOBJECTS = [
    # Testcases for _common.sort_cimobjects()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * objects: List of input objects to sort.
    #   * exp_indexes: List of expected indexes of objects in sorted result.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Empty list of objects",
        dict(
            objects=[],
            exp_indexes=[]
        ),
        None, None, OK
    ),
    (
        "string: One object",
        dict(
            objects=['abc'],
            exp_indexes=[0]
        ),
        None, None, OK
    ),
    (
        "string: Two objects, opposite sort order",
        dict(
            objects=['xyz', 'abc'],
            exp_indexes=[1, 0]
        ),
        None, None, OK
    ),
    (
        "CIMClass: One object",
        dict(
            objects=[
                CIMClass(
                    'CIM_Foo',
                    properties=[
                        CIMProperty('InstanceID', None, type='string'),
                    ]),
            ],
            exp_indexes=[0]
        ),
        None, None, OK
    ),
    (
        "CIMClass: Verify that equal sort keys are supported and sort is "
        "stable",
        dict(
            objects=[
                CIMClass(
                    'CIM_Foo',
                    properties=[
                        CIMProperty('InstanceID', None, type='string'),
                    ]),
                CIMClass(
                    'CIM_Boo',
                    properties=[
                        CIMProperty('InstanceID', None, type='string'),
                    ]),
                CIMClass(
                    'CIM_Boo',
                    properties=[
                        CIMProperty('InstanceID', None, type='string'),
                    ]),
            ],
            exp_indexes=[1, 2, 0]
        ),
        None, None, OK
    ),
    (
        "CIMClass: Verify that sort key is only by class name and does not "
        "also include the name of properties",
        dict(
            objects=[
                CIMClass(
                    'CIM_Foo',
                    properties=[
                        CIMProperty('InstanceID', None, type='string'),
                    ]),
                CIMClass(
                    'CIM_Boo',
                    properties=[
                        CIMProperty('InstanceID2', None, type='string'),
                    ]),
                CIMClass(
                    'CIM_Boo',
                    properties=[
                        CIMProperty('InstanceID1', None, type='string'),
                    ]),
            ],
            exp_indexes=[1, 2, 0]
        ),
        None, None, OK
    ),
    (
        "CIMClassName: One object",
        dict(
            objects=[
                CIMClassName(host="fred", namespace="cimv2", classname="foo"),
            ],
            exp_indexes=[0]
        ),
        None, None, OK
    ),
    (
        "CIMClassName: Verify that equal sort keys are supported and sort is "
        "stable",
        dict(
            objects=[
                CIMClassName(host="fred", namespace="cimv3", classname="bla"),
                CIMClassName(host="fred", namespace="cimv2", classname="foo"),
                CIMClassName(host="fred", namespace="cimv2", classname="foo"),
            ],
            exp_indexes=[1, 2, 0]
        ),
        None, None, OK
    ),
    (
        "CIMClassName: Verify sort precedence of host, namespace, classname",
        dict(
            objects=[
                CIMClassName(host="fred", namespace="cimv2", classname="foo"),
                CIMClassName(host="fred", namespace="cimv2", classname="bla"),
                CIMClassName(host="john", namespace="cimv2", classname="bla"),
                CIMClassName(host="fred", namespace="cimv3", classname="bla"),
            ],
            exp_indexes=[1, 0, 3, 2]
        ),
        None, None, OK
    ),
    (
        "CIMInstanceName: One object",
        dict(
            objects=[
                CIMInstanceName(
                    host='fred',
                    namespace='root/cimv2',
                    classname='CIM_Foo',
                    keybindings={'Chicken': 'Ham', 'Beans': 42}),
            ],
            exp_indexes=[0]
        ),
        None, None, OK
    ),
    (
        "CIMInstanceName: Verify that equal sort keys are supported and sort "
        "is stable",
        dict(
            objects=[
                CIMInstanceName(
                    host='fred',
                    namespace='root/cimv3',
                    classname='CIM_Foo',
                    keybindings={'Chicken': 'Ham', 'Beans': 42}),
                CIMInstanceName(
                    host='fred',
                    namespace='root/cimv2',
                    classname='CIM_Foo',
                    keybindings={'Chicken': 'Ham', 'Beans': 42}),
                CIMInstanceName(
                    host='fred',
                    namespace='root/cimv2',
                    classname='CIM_Foo',
                    keybindings={'Chicken': 'Ham', 'Beans': 42}),
            ],
            exp_indexes=[1, 2, 0]
        ),
        None, None, OK
    ),
    (
        "CIMInstanceName: Verify sort precedence of host, namespace, "
        "classname, keybindings",
        dict(
            objects=[
                CIMInstanceName(
                    host='john',
                    namespace='root/cimv2',
                    classname='CIM_Foo',
                    keybindings={'Chicken': 'Ham', 'Beans': 42}),
                CIMInstanceName(
                    host='fred',
                    namespace='root/cimv3',
                    classname='CIM_Boo',
                    keybindings={'Chicken': 'Ham', 'Beans': 42}),
                CIMInstanceName(
                    host='fred',
                    namespace='root/cimv2',
                    classname='CIM_Foo',
                    keybindings={'Chicken': 'Ham', 'Beans': 42}),
                CIMInstanceName(
                    host='fred',
                    namespace='root/cimv2',
                    classname='CIM_Foo',
                    keybindings={'AChicken': 'Ham', 'Beans': 42}),
            ],
            exp_indexes=[3, 2, 1, 0]
        ),
        None, None, OK
    ),
    (
        "CIMInstance: One object",
        dict(
            objects=[
                CIMInstance(
                    'CIM_Foo',
                    path=CIMInstanceName('CIM_Foo', {'Chicken': 'Ham'})),
            ],
            exp_indexes=[0]
        ),
        None, None, OK
    ),
    (
        "CIMInstance: Verify that equal sort keys are supported and sort "
        "is stable",
        dict(
            objects=[
                CIMInstance(
                    'CIM_Foo',
                    path=CIMInstanceName('CIM_Foo', {'Chicken': 'Ham'})),
                CIMInstance(
                    'CIM_Foo',
                    path=CIMInstanceName('CIM_Foo', {'Chicken': 'Ham'})),
                CIMInstance(
                    'CIM_Boo',
                    path=CIMInstanceName('CIM_Boo', {'Chicken': 'Ham'})),
            ],
            exp_indexes=[2, 0, 1]
        ),
        None, None, OK
    ),
    (
        "CIMInstance: Verify that sort is by instance path, and does not also"
        "include class name",
        dict(
            objects=[
                CIMInstance(
                    'CIM_Foo',
                    path=CIMInstanceName('CIM_Foo', {'Chicken': 'Ham'})),
                CIMInstance(
                    'CIM_Boo',  # intentionally inconsistent with path
                    path=CIMInstanceName('CIM_Foo', {'Chicken': 'Ham'})),
                CIMInstance(
                    'CIM_Foo',  # intentionally inconsistent with path
                    path=CIMInstanceName('CIM_Boo', {'Chicken': 'Ham'})),
            ],
            exp_indexes=[2, 0, 1]
        ),
        None, None, OK
    ),
    (
        "CIMInstance: Invalid objects without path set",
        dict(
            objects=[
                CIMInstance('CIM_Foo'),
                CIMInstance('CIM_Boo'),
            ],
            exp_indexes=None
        ),
        ValueError, None, OK
    ),
    (
        "CIMQualifierDeclaration: One object",
        dict(
            objects=[
                CIMQualifierDeclaration('FooQualDecl1', 'uint32'),
            ],
            exp_indexes=[0]
        ),
        None, None, OK
    ),
    (
        "CIMQualifierDeclaration: Verify that equal sort keys are supported "
        "and sort is stable",
        dict(
            objects=[
                CIMQualifierDeclaration('FooQualDecl2', 'uint32'),
                CIMQualifierDeclaration('FooQualDecl2', 'uint32'),
                CIMQualifierDeclaration('FooQualDecl1', 'uint32'),
            ],
            exp_indexes=[2, 0, 1]
        ),
        None, None, OK
    ),
    (
        "CIMQualifierDeclaration: Verify that sort key is by qualifier name, "
        "and does not also include qualifier value",
        dict(
            objects=[
                CIMQualifierDeclaration('FooQualDecl2', 'string', 'abc'),
                CIMQualifierDeclaration('FooQualDecl1', 'string', 'xyz'),
                CIMQualifierDeclaration('FooQualDecl1', 'string', 'abc'),
            ],
            exp_indexes=[1, 2, 0]
        ),
        None, None, OK
    ),
    (
        "tuple(CIMClassName, CIMClass): Three objects in opposite sort order "
        "(return from class references/associators)",
        dict(
            objects=[
                (
                    CIMClassName(
                        'CIM_Foo', host="fred", namespace="root/cimv2"),
                    CIMClass(
                        'CIM_Foo',
                        properties=[
                            CIMProperty('InstanceID', None, type='string'),
                        ]),
                ),
                (
                    CIMClassName(
                        'CIM_Boo', host="fred", namespace="root/cimv1"),
                    CIMClass(
                        'CIM_Boo',
                        properties=[
                            CIMProperty('InstanceID', None, type='string'),
                        ]),
                ),
                (
                    CIMClassName(
                        'CIM_Boo', host="john", namespace="root/cimv2"),
                    CIMClass(
                        'CIM_Boo',
                        properties=[
                            CIMProperty('InstanceID', None, type='string'),
                        ]),
                ),
            ],
            exp_indexes=[1, 0, 2]
        ),
        None, None, OK
    ),
    (
        "Invalid type: single tuple(CIMClass, CIMClassName)",
        dict(
            objects=[
                (
                    CIMClass(
                        'CIM_Foo',
                        properties=[
                            CIMProperty('InstanceID', None, type='string'),
                        ]),
                    CIMClassName(
                        'CIM_Foo', host="fred", namespace="root/cimv2"),
                ),
            ],
            exp_indexes=None
        ),
        TypeError, None, OK
    ),
    (
        "Invalid type: single tuple(CIMInstanceName, CIMClass)",
        dict(
            objects=[
                (
                    CIMInstanceName(
                        'CIM_Foo', host="fred", namespace="root/cimv2"),
                    CIMClass(
                        'CIM_Foo',
                        properties=[
                            CIMProperty('InstanceID', None, type='string'),
                        ]),
                ),
            ],
            exp_indexes=None
        ),
        TypeError, None, OK
    ),
    (
        "Invalid type: single int object",
        dict(
            objects=[42],
            exp_indexes=None
        ),
        TypeError, None, OK
    ),
    (
        "Invalid type: two int objects",
        dict(
            objects=[42, 43],
            exp_indexes=None
        ),
        TypeError, None, OK
    ),
    (
        "Invalid type: Single CIMQualifier object",
        dict(
            objects=[
                CIMQualifier('Key', value=OK),
            ],
            exp_indexes=None
        ),
        TypeError, None, OK
    ),
    (
        "Invalid type: Two CIMQualifier objects",
        dict(
            objects=[
                CIMQualifier('Key', value=True),
                CIMQualifier('Units', value='Bytes'),
            ],
            exp_indexes=None
        ),
        TypeError, None, OK
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SORT_CIMOBJECTS)
@simplified_test_function
def test_sort_cimobjects(testcase, objects, exp_indexes):
    """
    Test function for _common.sort_cimobjects()
    """

    # The code to be tested
    result_objects = sort_cimobjects(objects)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert len(result_objects) == len(objects)

    # Assert the list of actual vs expected object IDs. This form of assertion
    # lets pytest show the difference and allows easily recognizing where the
    # order is incorrect.
    result_ids = [id(obj) for obj in result_objects]
    exp_ids = [id(objects[ix]) for ix in exp_indexes]
    assert result_ids == exp_ids, "Ids misorder\n{}\n{}".format(result_ids,
                                                                exp_ids)


TESTCASES_SPLIT_ARRAY_VALUE = [
    # Testcases for _common.split_array_value()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * in: String defining the key=value to be tested.
    #   * exp_rslt: Name expected in response.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ("Verify simple numeric array",
     dict(input_='0,1,2,3,4,5,6',
          exp_rslt=['0', '1', '2', '3', '4', '5', '6']),
     None, None, 'OK'),

    ("Verify simple non-numeric array",
     dict(input_='abc,def,jhi,klm,nop',
          exp_rslt=['abc', 'def', 'jhi', 'klm', 'nop']),
     None, None, OK),

    ("Verify split array with escape for ,",
     dict(input_='abc,def,jhi,klm,n\\,op',
          exp_rslt=['abc', 'def', 'jhi', 'klm', 'n,op']),
     None, None, OK),

    ("Verify split array with space ,",
     dict(input_='abc,de f',
          exp_rslt=['abc', 'de f']),
     None, None, OK),

    ("Verify split single string with space ,",
     dict(input_='abcde f',
          exp_rslt=['abcde f']),
     None, None, OK),

    ("Verify split empty string ,",
     dict(input_='',
          exp_rslt=['']),
     None, None, OK),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SPLIT_ARRAY_VALUE)
@simplified_test_function
def test_split_array_value(testcase, input_, exp_rslt):
    """
    Test function for _common.split_array_value()
    """

    # The code to be tested
    act_rslt = split_array_value(input_, ',')

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert exp_rslt == act_rslt,  \
        'Failed split test exp {!r}, act {!r}'.format(exp_rslt, act_rslt)


# Class definitions for _common.create_ciminstance()

# A class with scalar properties of all types except embedded instances
CLASS_SCALAR = CIMClass(
    classname='CIM_Foo',
    properties=[
        CIMProperty('ID', None, type='string'),
        CIMProperty('Boolp', None, type='boolean'),
        CIMProperty('Uint8p', None, type='uint8'),
        CIMProperty('Sint8p', None, type='sint8'),
        CIMProperty('Uint16p', None, type='uint16'),
        CIMProperty('Sint16p', None, type='sint16'),
        CIMProperty('Uint32p', None, type='uint32'),
        CIMProperty('Sint32p', None, type='sint32'),
        CIMProperty('Uint64p', None, type='uint64'),
        CIMProperty('Sint64p', None, type='sint64'),
        CIMProperty('Real32p', None, type='real32'),
        CIMProperty('Real64p', None, type='real64'),
        CIMProperty('Dtp', None, type='datetime'),
        CIMProperty('Strp', None, type='string'),
        CIMProperty('Char16p', None, type='char16'),
    ],
)

# A class with array properties of all types except embedded instances
CLASS_ARRAY = CIMClass(
    classname='CIM_Foo',
    properties=[
        CIMProperty('ID', None, type='string'),
        CIMProperty('Boolp', None, is_array=True, type='boolean'),
        CIMProperty('Uint8p', None, is_array=True, type='uint8'),
        CIMProperty('Sint8p', None, is_array=True, type='sint8'),
        CIMProperty('Uint16p', None, is_array=True, type='uint16'),
        CIMProperty('Sint16p', None, is_array=True, type='sint16'),
        CIMProperty('Uint32p', None, is_array=True, type='uint32'),
        CIMProperty('Sint32p', None, is_array=True, type='sint32'),
        CIMProperty('Uint64p', None, is_array=True, type='uint64'),
        CIMProperty('Sint64p', None, is_array=True, type='sint64'),
        CIMProperty('Real32p', None, is_array=True, type='real32'),
        CIMProperty('Real64p', None, is_array=True, type='real64'),
        CIMProperty('Dtp', None, is_array=True, type='datetime'),
        CIMProperty('Strp', None, is_array=True, type='string'),
        CIMProperty('Char16p', None, is_array=True, type='char16'),
    ],
)


TESTCASES_CREATE_CIMINSTANCE = [
    # Testcases for _common.create_ciminstance()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * cls: Dict with attributes from which test class is constructed
    #   * kv_properties: List of "name=value" strings for input properties
    #   * exp_inst - The expected instance name
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Test instance of scalar class with string property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['ID=Testid'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('ID', 'Testid', type='string'),
                ]
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with string+bool properties",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['ID=Testid', 'Boolp=false'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('ID', 'Testid', type='string'),
                    CIMProperty('Boolp', False),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with string+real32 properties",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['ID=Testid', 'Real32p=1.99'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('ID', 'Testid', type='string'),
                    CIMProperty('Real32p', 1.99, type='real32'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with most properties",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=[
                'ID=Testid', 'Boolp=true', 'Uint8p=220', 'Sint8p=-120',
                'Uint32p=999', 'Sint32p=-99', 'Uint64p=999',
                'Sint64p=-99', 'Strp=hoho',
                'Dtp=19991224120000.000000+360',
            ],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('ID', 'Testid', type='string'),
                    CIMProperty('Boolp', True),
                    CIMProperty('Uint8p', 220, type='uint8'),
                    CIMProperty('Sint8p', -120, type='sint8'),
                    CIMProperty('Uint32p', 999, type='uint32'),
                    CIMProperty('Sint32p', -99, type='sint32'),
                    CIMProperty('Uint64p', 999, type='uint64'),
                    CIMProperty('Sint64p', -99, type='sint64'),
                    CIMProperty('Dtp', "19991224120000.000000+360",
                                type='datetime'),
                    CIMProperty('Strp', 'hoho', type='string'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with empty property list",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=[],
            exp_inst=CIMInstance(classname='CIM_Foo'),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with no value (NULL) for string "
        "property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Strp='],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Strp', None, type='string'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with no =value (NULL) for string "
        "property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Strp'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Strp', None, type='string'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with no value (NULL) for uint32 "
        "property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Uint32p='],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Uint32p', None, type='uint32'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with no =value (NULL) for uint32 "
        "property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Uint32p'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Uint32p', None, type='uint32'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with no value (NULL) for bool property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Boolp='],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Boolp', None, type='boolean'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with no =value (NULL) for bool property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Boolp'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Boolp', None, type='boolean'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of scalar class with invalid property name",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['DoesNotExist'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of scalar class with incorrect int value for bool "
        "property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Boolp=123'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of scalar class with incorrect string value for uint32 "
        "property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Uint32p=shouldnotbestring'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of scalar class with incorrect bool value for uint32 "
        "property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Uint32p=true'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of scalar class with incorrect bool value for real32 "
        "property",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Real32p=true'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of scalar class with two-char value for char16 property "
        "(pywbem.cimvalue() does not reject that)",
        dict(
            cls=CLASS_SCALAR,
            kv_properties=['Char16p=ab'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Char16p', 'ab', type='char16'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of array class with most properties",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=[
                'ID=Testid', 'Boolp=true,false', 'Uint8p=0,12,120',
                'Sint8p=-120,0,119', 'Uint32p=0,999', 'Sint32p=-99,0,9999',
                'Uint64p=0,999,99999', 'Sint64p=-99,0,12345', 'Strp=hoho,haha',
            ],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('ID', 'Testid', type='string'),
                    CIMProperty('Boolp', [True, False]),
                    CIMProperty('Uint8p', [0, 12, 120], type='uint8'),
                    CIMProperty('Sint8p', [-120, 0, 119], type='sint8'),
                    CIMProperty('Uint32p', [0, 999], type='uint32'),
                    CIMProperty('Sint32p', [-99, 0, 9999], type='sint32'),
                    CIMProperty('Uint64p', [0, 999, 99999], type='uint64'),
                    CIMProperty('Sint64p', [-99, 0, 12345], type='sint64'),
                    CIMProperty('Strp', ['hoho', 'haha'], type='string'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of array class with empty property list",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=[],
            exp_inst=CIMInstance(classname='CIM_Foo'),
        ),
        None, None, True
    ),
    (
        "Test instance of array class with no value (NULL) for string "
        "property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Strp='],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Strp', None, is_array=True, type='string'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of array class with no =value (NULL) for string "
        "property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Strp'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Strp', None, is_array=True, type='string'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of array class with no value (NULL) for uint32 "
        "property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Uint32p='],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Uint32p', None, is_array=True, type='uint32'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of array class with no =value (NULL) for uint32 "
        "property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Uint32p'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Uint32p', None, is_array=True, type='uint32'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of array class with no value (NULL) for bool property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Boolp='],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Boolp', None, is_array=True, type='boolean'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of array class with no =value (NULL) for bool property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Boolp'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Boolp', None, is_array=True, type='boolean'),
                ],
            ),
        ),
        None, None, True
    ),
    (
        "Test instance of array class with invalid property name",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['DoesNotExist'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of array class with incorrect int value for bool "
        "property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Boolp=123'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of array class with incorrect string value for uint32 "
        "property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Uint32p=shouldnotbestring'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of array class with incorrect bool value for uint32 "
        "property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Uint32p=true'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of array class with incorrect bool value for real32 "
        "property",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Real32p=true'],
            exp_inst=None,
        ),
        click.ClickException, None, True
    ),
    (
        "Test instance of array class with two-char value for char16 property "
        "(pywbem.cimvalue() does not reject that)",
        dict(
            cls=CLASS_ARRAY,
            kv_properties=['Char16p=ab'],
            exp_inst=CIMInstance(
                classname='CIM_Foo',
                properties=[
                    CIMProperty('Char16p', ['ab'], type='char16'),
                ],
            ),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CREATE_CIMINSTANCE)
@simplified_test_function
def test_create_ciminstance(testcase, cls, kv_properties, exp_inst):
    """
    Test function for _common.create_ciminstance()
    """

    # The code to be tested
    inst = create_ciminstance(cls, kv_properties)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert isinstance(inst, CIMInstance)
    assert inst == exp_inst


# Simple hierarchy of classes for get_subclass_names test
SUBCLASS_LIST = [
    CIMClass('TST_L0', superclass=None),
    CIMClass('TST_L1', superclass='TST_L0'),
    CIMClass('TST_L2', superclass='TST_L0'),

    CIMClass('TST_L11', superclass='TST_L1'),
    CIMClass('TST_L21', superclass='TST_L2'),

    CIMClass('TST_L111', superclass='TST_L11'),
    CIMClass('TST_L211', superclass='TST_L21'),

    CIMClass('TST_L1111', superclass='TST_L111'),
    CIMClass('TST_L1112', superclass='TST_L111'),
    CIMClass('TST_L1113', superclass='TST_L111'),

    CIMClass('TST_L2111', superclass='TST_L211'),
    CIMClass('TST_L2112', superclass='TST_L211'),
    CIMClass('TST_L2113', superclass='TST_L211'),
    CIMClass('TST_L2114', superclass='TST_L211'),
]
TESTCASES_GET_SUBCLASS_NAMES = [
    # Testcases for get_subclasses()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * classes - List of classes for which hiearchy to be generated
    #   * classname: target classname from which to find subclasses or None,
    #   * deep_inheritance: flag (True, False, None)
    #   * exp_rtn: List of classes to be returned
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify list of subclasses for TST_L1',
     dict(classes=SUBCLASS_LIST,
          classname="TST_L1",
          deep_inheritance=True,
          exp_rtn=['TST_L11', 'TST_L111', 'TST_L1111', 'TST_L1112',
                   'TST_L1113']),
     None, None, OK, ),

    ('Verify list of subclasses for TST_L21',
     dict(classes=SUBCLASS_LIST,
          classname="TST_L21",
          deep_inheritance=True,
          exp_rtn=['TST_L211', 'TST_L2111', 'TST_L2112', 'TST_L2113',
                   'TST_L2114']),
     None, None, OK, ),
    ('Verify list of subclasses for TST_L211',
     dict(classes=SUBCLASS_LIST,
          classname="TST_L21",
          deep_inheritance=True,
          exp_rtn=['TST_L211', 'TST_L2111', 'TST_L2112', 'TST_L2113',
                   'TST_L2114']),
     None, None, OK, ),

    ('Verify list of subclasses for TST_L2111',
     dict(classes=SUBCLASS_LIST,
          classname="TST_L2111",
          deep_inheritance=True,
          exp_rtn=[]),
     None, None, OK, ),

    ('Verify list of subclasses for TST_L2111',
     dict(classes=SUBCLASS_LIST,
          classname="blah",
          deep_inheritance=True,
          exp_rtn=[]),
     ValueError, None, OK, ),

    ('Verify list of subclasses for TST_L1',
     dict(classes=SUBCLASS_LIST,
          classname="TST_L1",
          deep_inheritance=False,
          exp_rtn=['TST_L11']),
     None, None, OK, ),

    ('Verify list of subclasses for TST_L21',
     dict(classes=SUBCLASS_LIST,
          classname="TST_L21",
          deep_inheritance=False,
          exp_rtn=['TST_L211']),
     None, None, OK, ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_GET_SUBCLASS_NAMES)
@simplified_test_function
def test_get_subclassnames(testcase, classes, classname, deep_inheritance,
                           exp_rtn):
    """
    Test function for _common.get_subclassnames()
    """
    # The code to be tested
    act_rtn = get_subclass_names(classes, classname,
                                 deep_inheritance=deep_inheritance)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    if act_rtn != exp_rtn:
        print('MOF\n{0}\nEXP\n{1}\nACT\n{2}\n'.format(classes, exp_rtn,
                                                      act_rtn))
    assert act_rtn == exp_rtn


TESTCASES_DEPENDENT_CLASSNAMES = [
    # Testcases for _common.dependent_classnames()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * cls_obj: CIMClass object used as input
    #   * exp_rtn: Expected return value: NocaseList with class names of
    #     dependent classes.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        'Verify class with no dependent classes',
        dict(
            cls_obj=CIMClass('Foo'),
            exp_rtn=NocaseList(),
        ),
        None, None, True
    ),
    (
        'Verify class with a superclass',
        dict(
            cls_obj=CIMClass('Foo', superclass='Super'),
            exp_rtn=NocaseList(['Super']),
        ),
        None, None, True
    ),
    (
        'Verify class with a reference property to another class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                properties=[
                    CIMProperty('P1', value=None, type='reference',
                                reference_class='Ref'),
                ],
            ),
            exp_rtn=NocaseList(['Ref']),
        ),
        None, None, True
    ),
    (
        'Verify class with a reference property to the same class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                properties=[
                    CIMProperty('P1', value=None, type='reference',
                                reference_class='Foo'),
                ],
            ),
            exp_rtn=NocaseList(),
        ),
        None, None, True
    ),
    (
        'Verify class with a method with a reference parameter to another '
        'class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                methods=[
                    CIMMethod(
                        'M1', return_type='string',
                        parameters=[
                            CIMParameter('P1', value=None, type='reference',
                                         reference_class='Ref'),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(['Ref']),
        ),
        None, None, True
    ),
    (
        'Verify class with a method with a reference parameter to same class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                methods=[
                    CIMMethod(
                        'M1', return_type='string',
                        parameters=[
                            CIMParameter('P1', value=None, type='reference',
                                         reference_class='Foo'),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(),
        ),
        None, None, True
    ),
    (
        'Verify class with a embedded instance property to another class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                properties=[
                    CIMProperty(
                        'P1', value=None, type='string',
                        qualifiers=[
                            CIMQualifier('EmbeddedInstance', 'Emb'),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(['Emb']),
        ),
        None, None, True
    ),
    (
        'Verify class with a embedded instance property to same class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                properties=[
                    CIMProperty(
                        'P1', value=None, type='string',
                        qualifiers=[
                            CIMQualifier('EmbeddedInstance', 'Foo'),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(),
        ),
        None, None, True
    ),
    (
        'Verify class with a method that returns an embedded instance to '
        'another class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                methods=[
                    CIMMethod(
                        'M1', return_type='string',
                        qualifiers=[
                            CIMQualifier('EmbeddedInstance', 'Emb'),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(['Emb']),
        ),
        None, None, True
    ),
    (
        'Verify class with a method that returns an embedded instance to '
        'same class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                methods=[
                    CIMMethod(
                        'M1', return_type='string',
                        qualifiers=[
                            CIMQualifier('EmbeddedInstance', 'Foo'),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(),
        ),
        None, None, True
    ),
    (
        'Verify class with a method with a embedded instance parameter to '
        'another class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                methods=[
                    CIMMethod(
                        'M1',
                        return_type='string',
                        parameters=[
                            CIMParameter(
                                'P1', value=None, type='string',
                                qualifiers=[
                                    CIMQualifier('EmbeddedInstance', 'Emb'),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(['Emb']),
        ),
        None, None, True
    ),
    (
        'Verify class with a method with a embedded instance parameter to '
        'same class',
        dict(
            cls_obj=CIMClass(
                'Foo',
                methods=[
                    CIMMethod(
                        'M1',
                        return_type='string',
                        parameters=[
                            CIMParameter(
                                'P1', value=None, type='string',
                                qualifiers=[
                                    CIMQualifier('EmbeddedInstance', 'Foo'),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(),
        ),
        None, None, True
    ),
    (
        'Verify class with all possible dependent classes to different classes',
        dict(
            cls_obj=CIMClass(
                'Foo',
                superclass='Super',
                properties=[
                    CIMProperty(
                        'P1', value=None, type='reference',
                        reference_class='RefP1',
                    ),
                    CIMProperty(
                        'P2', value=None, type='string',
                        qualifiers=[
                            CIMQualifier('EmbeddedInstance', 'EmbP2'),
                        ],
                    ),
                ],
                methods=[
                    CIMMethod(
                        'M1',
                        return_type='string',
                        qualifiers=[
                            CIMQualifier('EmbeddedInstance', 'EmbM1'),
                        ],
                        parameters=[
                            CIMParameter(
                                'Pa1', value=None, type='reference',
                                reference_class='RefM1Pa1',
                            ),
                            CIMParameter(
                                'Pa2', value=None, type='string',
                                qualifiers=[
                                    CIMQualifier(
                                        'EmbeddedInstance', 'EmbM1Pa2'),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(['Super', 'RefP1', 'EmbP2', 'EmbM1',
                                'RefM1Pa1', 'EmbM1Pa2']),
        ),
        None, None, True
    ),
    (
        'Verify class with all possible dependent classes to partly the same '
        'classes, also referencing itself',
        dict(
            cls_obj=CIMClass(
                'Foo',
                superclass='Super',
                properties=[
                    CIMProperty(
                        'P1', value=None, type='reference',
                        reference_class='Ref',
                    ),
                    CIMProperty(
                        'P2', value=None, type='string',
                        qualifiers=[
                            CIMQualifier('EmbeddedInstance', 'EmbP2'),
                        ],
                    ),
                    CIMProperty(
                        'P3', value=None, type='reference',
                        reference_class='Foo',
                    ),
                ],
                methods=[
                    CIMMethod(
                        'M1',
                        return_type='string',
                        qualifiers=[
                            CIMQualifier('EmbeddedInstance', 'EmbM1'),
                        ],
                        parameters=[
                            CIMParameter(
                                'Pa1', value=None, type='reference',
                                reference_class='Ref',
                            ),
                            CIMParameter(
                                'Pa2', value=None, type='string',
                                qualifiers=[
                                    CIMQualifier(
                                        'EmbeddedInstance', 'EmbM1'),
                                ],
                            ),
                            CIMParameter(
                                'Pa3', value=None, type='reference',
                                reference_class='Foo',
                            ),
                        ],
                    ),
                ],
            ),
            exp_rtn=NocaseList(['Super', 'Ref', 'EmbP2', 'EmbM1']),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DEPENDENT_CLASSNAMES)
@simplified_test_function
def test_dependent_classnames(testcase, cls_obj, exp_rtn):
    """
    Test function for _common.dependent_classnames()
    """

    # The code to be tested
    act_rtn = dependent_classnames(cls_obj)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert isinstance(act_rtn, NocaseList)
    assert set(act_rtn) == set(exp_rtn)


TESTCASES_DEPENDING_CLASSNAMES = [
    # Testcases for _common.depending_classnames()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * mock_items: List of mock items to be set up in mock environment
    #   * classname: Class name used as input
    #   * exp_rtn: Expected return value: List of class names of depending
    #     classes.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        'Verify class CIM_Foo in simple mock model',
        dict(
            mock_items=[SIMPLE_MOCK_FILE],
            classname='CIM_Foo',
            exp_rtn=['CIM_Foo_sub', 'CIM_Foo_sub2'],
        ),
        None, None, True
    ),
    (
        'Verify class CIM_Foo_sub in simple mock model',
        dict(
            mock_items=[SIMPLE_MOCK_FILE],
            classname='CIM_Foo_sub',
            exp_rtn=['CIM_Foo_sub_sub'],
        ),
        None, None, True
    ),
    (
        'Verify class CIM_Foo_sub2 in simple mock model',
        dict(
            mock_items=[SIMPLE_MOCK_FILE],
            classname='CIM_Foo_sub2',
            exp_rtn=[],
        ),
        None, None, True
    ),
    (
        'Verify class CIM_FooRef1 in simple mock model',
        dict(
            mock_items=[SIMPLE_MOCK_FILE],
            classname='CIM_FooRef1',
            exp_rtn=['CIM_Foo', 'CIM_FooAssoc'],
        ),
        None, None, True
    ),
    (
        'Verify class CIM_FooEmb1 in simple mock model',
        dict(
            mock_items=[SIMPLE_MOCK_FILE],
            classname='CIM_FooEmb1',
            exp_rtn=['CIM_Foo'],
        ),
        None, None, True
    ),
    (
        'Verify class CIM_FooAssoc in simple mock model',
        dict(
            mock_items=[SIMPLE_MOCK_FILE],
            classname='CIM_FooAssoc',
            exp_rtn=[],
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DEPENDING_CLASSNAMES)
@simplified_test_function
def test_depending_classnames(testcase, mock_items, classname, exp_rtn):
    """
    Test function for _common.depending_classnames()
    """
    namespace = 'root/foo'

    conn = setup_mock_connection(mock_items, namespace)

    # The code to be tested
    act_rtn = depending_classnames(classname, namespace, conn)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert isinstance(act_rtn, NocaseList)
    assert set(act_rtn) == set(exp_rtn)


TESTCASES_ALL_CLASSNAMES_DEPSORTED = [
    # Testcases for _common.all_classnames_depsorted()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * mock_items: List of mock items to be set up in mock environment
    #   * exp_rtn: Expected return value: List of all class names in dependency
    #     order.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        'Verify simple mock model',
        dict(
            mock_items=[SIMPLE_MOCK_FILE],
            exp_rtn=[
                'CIM_Foo_sub_sub',
                'CIM_Foo_sub2',
                'CIM_Foo_sub',
                'CIM_FooAssoc',
                'CIM_Foo',
                'CIM_FooRef2',
                'CIM_FooRef1',
                'CIM_FooEmb3',
                'CIM_FooEmb2',
                'CIM_FooEmb1',
                'CIM_BaseRef',
                'CIM_BaseEmb',
            ],
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_ALL_CLASSNAMES_DEPSORTED)
@simplified_test_function
def test_all_classnames_depsorted(testcase, mock_items, exp_rtn):
    """
    Test function for _common.all_classnames_depsorted()
    """
    namespace = 'root/foo'

    conn = setup_mock_connection(mock_items, namespace)

    # The code to be tested
    act_rtn = all_classnames_depsorted(namespace, conn)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert list(act_rtn) == list(exp_rtn)


TESTCASES_PARSE_VERSION_VALUE = [
    # Testcases for parse_version_value()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * ver: String defining the version (valid is str . str . str)
    #     where each str has only integer characters
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify valid version string 1',
     dict(ver="2.41.1",
          exp_rtn=[2, 41, 1]),
     None, None, OK, ),

    ('Verify valid version string 2',
     dict(ver="1.1.1",
          exp_rtn=[1, 1, 1]),
     None, None, OK, ),

    ('Verify valid version string 3',
     dict(ver="99.99.99",
          exp_rtn=[99, 99, 99]),
     None, None, OK, ),

    ('Verify invalid string with only two items returns 3 items',
     dict(ver="2.41",
          exp_rtn=[2, 41, 0]),
     None, ToleratedSchemaIssueWarning, OK, ),

    ('Verify invalid string with 4 items returns 3 items',
     dict(ver="2.41.1.1",
          exp_rtn=[2, 41, 1]),
     None, ToleratedSchemaIssueWarning, OK, ),

    ('Verify invalid string with alphabetic characters returns 0.0.0',
     dict(ver="a.41.1",
          exp_rtn=[0, 0, 0]),
     None, ToleratedSchemaIssueWarning, OK, ),

    ('Verify invalid string with alphabetic characters returns 0.0.0',
     dict(ver="2.abcdef.1",
          exp_rtn=[0, 0, 0]),
     None, ToleratedSchemaIssueWarning, OK, ),


    ('Verify invalid string with alphabetic characters returns 0.0.0',
     dict(ver="xyz.abcdef.jkl",
          exp_rtn=[0, 0, 0]),
     None, ToleratedSchemaIssueWarning, OK, ),

    ('Verify invalid string empty returns 3 items',
     dict(ver="",
          exp_rtn=[0, 0, 0]),
     None, ToleratedSchemaIssueWarning, OK, ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PARSE_VERSION_VALUE)
@simplified_test_function
def test_parse_version_value(testcase, ver, exp_rtn):
    """
    Test function for _common.get_subclassnames()
    """
    # The code to be tested
    act_rtn = parse_version_value(ver, "CIM_Fakeclassname")
    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_IS_EXPERIMENTAL = [
    # Testcases for parse_version_value()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * klass: MOF for class including version qualifier
    #   * exp_rtn: True if function returns True, else False
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify experimintal in class qualifiers',
     dict(klass="""
[Version ( "2.6.0" ), Experimental]
class TST_Exp{
    string p;
    uint32 counter;
    string M1;
    uint32 M2(
      string P1);
};
""",
          exp_rtn=True),
     None, None, OK, ),

    ('Verify experimental in property quaifier',
     dict(klass="""
                [Version ( "2.6.0" )]
                class TST_Exp{
                    [Experimental] string p;
                    uint32 counter;
                    string M1;
                    uint32 M2(
                      string P1);
                };
                """,
          exp_rtn=True),
     None, None, OK, ),

    ('Verify experimental in method qualifiers',
     dict(klass="""
                [Version ( "2.6.0" )]
                class TST_Exp{
                    string p;
                    uint32 counter;
                    string M1;
                    [ Experimental] uint32 M2(
                      string P1);
                };
                """,
          exp_rtn=True),
     None, None, OK, ),


    ('Verify experimental in first method qualifiers',
     dict(klass="""
                [Version ( "2.6.0" )]
                class TST_Exp{
                    string p;
                    uint32 counter;
                    [ Experimental] string M1;
                    uint32 M2(
                      string P1);
                };
                """,
          exp_rtn=True),
     None, None, OK, ),

    ('Verify experimental in parameter qualifiers',
     dict(klass="""
                [Version ( "2.6.0" )]
                class TST_Exp{
                    string p;
                    uint32 counter;
                    string M1;
                     uint32 M2(
                      [ Experimental] string P1);
                };
                """,
          exp_rtn=True),
     None, None, OK, ),

    ('Verify no experimental qualifiers',
     dict(klass="""
                [Version ( "2.6.0" )]
                class TST_Exp{
                    string p;
                    uint32 counter;
                    string M1;
                    uint32 M2(
                      string P1);
                };
                """,
          exp_rtn=False),
     None, None, OK, ),

    ('Verify experimental with value False',
     dict(klass="""
                [Version ( "2.6.0" ), Experimental(false)]
                class TST_Exp{
                    string p;
                    uint32 counter;
                    string M1;
                    uint32 M2(
                      string P1);
                };
                """,
          exp_rtn=False),
     None, None, OK, ),

]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_IS_EXPERIMENTAL)
@simplified_test_function
def test_is_experimental(testcase, klass, exp_rtn):
    """
    Test function for _common.get_subclassnames(). Note that we compile each
    test class with a single qualifier, experimental
    """

    qualifier = """
Qualifier Experimental : boolean = false,
    Scope(any),
    Flavor(EnableOverride, Restricted);
Qualifier Version : string = null,
    Scope(class, association, indication),
    Flavor(EnableOverride, Restricted, Translatable);

"""
    test_mof = qualifier + klass

    # skip_if_moftab_regenerated()
    mofcomp = MOFCompiler(
        MOFWBEMConnection(),
        search_paths=None,
        verbose=False,
        log_func=None)

    mofcomp.compile_string(test_mof, ns='root/cimv2')
    repo = mofcomp.handle

    klass = repo.GetClass('TST_Exp', namespace='root/cimv2',
                          LocalOnly=False, IncludeQualifiers=True)

    # The code to be tested
    act_rtn = is_experimental_class(klass)
    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_TO_WBEMURI_FOLDED = [
    # Testcases for to_wbem_uri_folded()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * path: CIMInstanceName object to be formatted
    #   * uri_format: None or string 'standard', 'canonical', 'cimobject',
    #     'historical'. If None, the default 'standard' is used.
    #   * maxlen: Integer or list of integers. The list form allows creating
    #     multiple tests with a single instancename. Only works if testing
    #     for successful return
    #   * exp_rtn, String or list of strings if maxlen is a list.  The
    #     formatted wbemuri including folding as a string
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger
    # TODO: Remove the first two tests.
    ('Verify simple sucessful format without  fold',
     dict(path=CIMInstanceName(classname='CIM_Foo',
                               keybindings=dict(InstanceID='1234'),
                               namespace='root/cimv2',
                               host='fred'),
          uri_format=None,
          max_lens=60,
          exp_rtns='//fred/root/cimv2:CIM_Foo.InstanceID="1234"'),
     None, None, OK, ),

    ('Verify simple sucessful format with  fold',
     dict(path=CIMInstanceName(classname='CIM_Foo',
                               keybindings=dict(InstanceID='1234'),
                               namespace='root/cimv2',
                               host='fred'),
          uri_format=None,
          max_lens=30,
          exp_rtns='//fred/root/cimv2:CIM_Foo.InstanceID=\n"1234"'),
     None, None, OK, ),

    ('Verify simple sucessful format with fold and no fold',
     dict(path=CIMInstanceName(classname='CIM_Foo',
                               keybindings=dict(InstanceID='1234'),
                               namespace='root/cimv2',
                               host='fred'),
          uri_format=None,
          max_lens=[60, 30],
          exp_rtns=['//fred/root/cimv2:CIM_Foo.InstanceID="1234"',
                    '//fred/root/cimv2:CIM_Foo.InstanceID=\n"1234"']),
     None, None, OK, ),

    ('Verify simple sucessful format with vers small fold int',
     dict(path=CIMInstanceName(classname='CIM_Foo',
                               keybindings=dict(InstanceID='1234'),
                               namespace='root/cimv2',
                               host='fred'),
          uri_format=None,
          max_lens=[5, 10],
          exp_rtns=['//fred/\nroot/cimv2:\nCIM_Foo.\nInstanceID=\n"1234"',
                    '//fred/root/cimv2:\nCIM_Foo.InstanceID=\n"1234"']),
     None, None, OK, ),
    # TODO: Add more test values to cover multiple keys more complex keys and
    # keys with very long name and values.
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_TO_WBEMURI_FOLDED)
@simplified_test_function
def test_to_wbemuri_folded(testcase, path, uri_format, max_lens, exp_rtns):
    """
    Test function for _common.to_wbemuri_folded().
    """
    # setup to allow multiple maxlen and exprtn items.
    if isinstance(max_lens, int):
        assert isinstance(exp_rtns, six.string_types)
        max_lens = [max_lens]
        exp_rtns = [exp_rtns]
        assert len(exp_rtns) == len(max_lens)

    # The code to be tested. Loops to test multiple max lengths
    for max_len, exp_rtn in zip(max_lens, exp_rtns):
        if uri_format is None:
            act_rtn = to_wbem_uri_folded(path, max_len=max_len)
        else:
            act_rtn = to_wbem_uri_folded(path, uri_format=uri_format,
                                         max_len=max_len)
        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None

        assert act_rtn == exp_rtn


# TODO Test compare and failure in compare_obj and with errors.


# NOTE: Format table tests are in test_tableformat.py
