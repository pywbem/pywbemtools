# -*- coding: utf-8 -*-
# (C) Copyright 2017 IBM Corp.
# (C) Copyright 2017-2021 Inova Development Inc.
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
Tests for _output_formatting.py functions, except for format_table and
fold_strings which is in test_tableformat.py.
"""

from __future__ import absolute_import, print_function

from packaging.version import parse as parse_version
import click
import pytest

from pywbem import CIMInstanceName, Uint8, __version__
try:
    from pywbem import MissingKeybindingsWarning
except ImportError:
    MissingKeybindingsWarning = None

from pywbemtools._output_formatting import validate_output_format, \
    output_format_in_groups, fold_strings, hide_empty_columns, format_keys

from .pytest_extensions import simplified_test_function

# pylint: disable=use-dict-literal

_PYWBEM_VERSION = parse_version(__version__)
# pywbem 1.0.0 (dev, beta, final) or later
PYWBEM_1_0_0 = _PYWBEM_VERSION.release >= (1, 0, 0)


TESTCASES_VALID_OUTPUT_FORMAT = [
    # Testcases for _output_formatting.validate_output_format()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * fmt: output_format defined for this command execution or None
    #   * default: string containing default format or None
    #   * groups: list of groups allowed for this command
    #   * exp_rtn: output_format return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify cmd input, None, default None returns mof',
     dict(fmt=None,
          default=None,
          groups=['CIM'],
          exp_rtn='mof'),
     None, None, True),

    ('Verify cmd input, None, default mof returns mof',
     dict(fmt=None,
          default='mof',
          groups=['CIM'],
          exp_rtn='mof'),
     None, None, True),


    ('Verify cmd input, None, default mof groups TABLE returns mof',
     dict(fmt=None,
          default=None,
          groups=['TABLE'],
          exp_rtn='simple'),
     None, None, True),

    ('Verify cmd input, None, default mof returns mof',
     dict(fmt=None,
          default='table',
          groups=['TABLE'],
          exp_rtn='table'),
     None, None, True),

    ('Verify cmd input, mof, default mof returns mof',
     dict(fmt='mof',
          default='mof',
          groups=['CIM'],
          exp_rtn='mof'),
     None, None, True),

    ('Verify cmd input, mof, default xml returns mof',
     dict(fmt='mof',
          default='mof',
          groups=['CIM'],
          exp_rtn='mof'),
     None, None, True),

    ('Verify cmd input xml returns xml',
     dict(fmt='xml',
          default='mof',
          groups=['CIM'],
          exp_rtn='xml'),
     None, None, True),

    ('Verify cmd input None default xml returns xml',
     dict(fmt=None,
          default='xml',
          groups=['CIM'],
          exp_rtn='xml'),
     None, None, True),

    ('Verify cmd input None default xml group table fails, AssertionError',
     dict(fmt=None,
          default='xml',
          groups=['Table'],
          exp_rtn='xml'),
     AssertionError, None, True),

    ('Verify cmd input blah default xml group table fails, AssertionError',
     dict(fmt='Blah',
          default='xml',
          groups=['Table'],
          exp_rtn='xml'),
     AssertionError, None, True),

    ('Verify cmd input None default xml group blah fails, AssertionError',
     dict(fmt='simple',
          default='xml',
          groups=['Blah'],
          exp_rtn='xml'),
     AssertionError, None, True),

    ('Verify cmd input None default xml group blah fails, AssertionError',
     dict(fmt='simple',
          default='blah',
          groups=['Table'],
          exp_rtn='xml'),
     AssertionError, None, True),

    ('Verify cmd input table group CIM fails',
     dict(fmt='table',
          default='xml',
          groups=['CIM'],
          exp_rtn='xml'),
     click.ClickException, None, True),

    ('Verify cmd input mof group TABLE fails',
     dict(fmt='mof',
          default='xml',
          groups=['TABLE'],
          exp_rtn=''),
     click.ClickException, None, True),

    ('Verify cmd input None, default xml group None OK',
     dict(fmt=None,
          default='xml',
          groups=None,
          exp_rtn='xml'),
     None, None, True),

    ('Verify cmd input xml, default xml group None OK',
     dict(fmt='xml',
          default='xml',
          groups=None,
          exp_rtn='xml'),
     None, None, True),

    ('Verify cmd input None, default xml group TABLE, CIM OK',
     dict(fmt=None,
          default='xml',
          groups=['TABLE', 'CIM'],
          exp_rtn='xml'),
     None, None, True),

    ('Verify cmd input None, default xml group None OK',
     dict(fmt=None,
          default=None,
          groups=None,
          exp_rtn='mof'),
     None, None, True),

]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_VALID_OUTPUT_FORMAT)
@simplified_test_function
def test_validate_output_format(testcase, fmt, default, groups, exp_rtn):
    """
    Test function for _output_formatting.validate_output_format()
    """

    # The code to be tested
    act_rtn = validate_output_format(fmt, groups, default_format=default)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_OUTPUT_FORMAT_IN_GROUPS = [
    # Testcases for _output_formatting.output_format_in_groups()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * fmt: output_format being tested
    #   * groups[]: string or list of stringscontaining group names
    #   * exp_rtn: output_format return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify mof in CIM',
     dict(fmt='mof',
          groups='CIM',
          exp_rtn=True),
     None, None, True),

    ('Verify mof CIM as a list',
     dict(fmt='mof',
          groups=['CIM'],
          exp_rtn=True),
     None, None, True),

    ('Verify mof CIM as a tuple',
     dict(fmt='mof',
          groups=('CIM'),
          exp_rtn=True),
     None, None, True),

    ('Verify table not in CIM',
     dict(fmt='table',
          groups=['CIM'],
          exp_rtn=False),
     None, None, False),

    ('Verify table not in CIM or TEXT',
     dict(fmt='table',
          groups=['CIM', 'TEXT'],
          exp_rtn=False),
     None, None, False),

]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_OUTPUT_FORMAT_IN_GROUPS)
@simplified_test_function
def test_output_format_in_groups(testcase, fmt, groups, exp_rtn):
    """
    Test function for _output_formatting.output_format_in_groups()
    """

    # The code to be tested
    act_rtn = output_format_in_groups(fmt, groups)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_FORMAT_KEYS = [
    # Testcases for _output_formatting.format_keys()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * kb: keybinding
    #   * width - integer representing width of resulting field
    #   * exp_rtn: expected function return.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify simple keybinding',
     dict(kb=[('kEY1', u'Ham')],
          width=100,
          exp_rtn='kEY1="Ham"'),
     None, None, True),

    ('Verify multiple keys keybinding',
     dict(kb=[('kEY1', u'Ham'), ('key2', 3)],
          width=100,
          exp_rtn='kEY1="Ham",key2=3'),
     None, None, True),

    ('Verify multiple keys binding with spaces in keys',
     dict(kb=[('kEY1', u'Ham and eggs'), ('key2', 'More eggs')],
          width=100,
          exp_rtn='kEY1="Ham and eggs",key2="More eggs"'),
     None, None, True),

    ('Verify multiple unsorted keys binding multiple key types, pywbem >=1.0',
     dict(kb=[('Name', 'Foo'),
              ('Number', Uint8(42)),
              ('Boolean', False),
              ('Ref', CIMInstanceName('CIM_Bar',
                                      keybindings={'Chicken': 'Ham'}))],
          width=100,
          exp_rtn='Boolean=FALSE,Name="Foo",Number=42,'
          'Ref="/:CIM_Bar.Chicken=\\"Ham\\""'),
     None, None, PYWBEM_1_0_0),

    ('Verify multiple unsorted keys binding multiple key types, pywbem <1.0',
     dict(kb=[('Name', 'Foo'),
              ('Number', Uint8(42)),
              ('Boolean', False),
              ('Ref', CIMInstanceName('CIM_Bar',
                                      keybindings={'Chicken': 'Ham'}))],
          width=100,
          exp_rtn='Name="Foo",Number=42,Boolean=FALSE,'
          'Ref="/:CIM_Bar.Chicken=\\"Ham\\""'),
     None, None, not PYWBEM_1_0_0),

    ('Verify mutliple keys that fold into multiple lines',
     dict(kb=[('kEY1', u'Ham'), ('key2', 3)],
          width=14,
          exp_rtn='kEY1="Ham"\nkey2=3'),
     None, None, True),

    ('Verify multiple keys binding with spaces in keys that fold',
     dict(kb=[('kEY1', u'Ham and eggs'), ('key2', 'More eggs')],
          width=25,
          exp_rtn='kEY1="Ham and eggs"\nkey2="More eggs"'),
     None, None, True),

    ('Verify multiple keys binding with many keys keys without fold',
     dict(kb=[('k1', 1), ('k2', 2), ('k3', 3), ('k4', 4), ('k5', 5),
              ('k6', 6), ('k7', 7), ('k8', 8)],
          width=100,
          exp_rtn=('k1=1,k2=2,k3=3,k4=4,k5=5,k6=6,k7=7,k8=8')),
     None, None, True),

    ('Verify multiple keys binding with many keys every key folds',
     dict(kb=[('k1', 1), ('k2', 2), ('k3', 3), ('k4', 4), ('k5', 5),
              ('k6', 6), ('k7', 7), ('k8', 8)],
          width=3,
          exp_rtn=('k1=1\nk2=2\nk3=3\nk4=4\nk5=5\nk6=6\nk7=7\nk8=8')),
     None, None, True),


    ('Verify multiple keys binding with many keys keys some fold',
     dict(kb=[('k1', 1), ('k2', 2), ('k3', 3), ('k4', 4), ('k5', 5),
              ('k6', 6), ('k7', 7), ('k8', 8)],
          width=8,
          exp_rtn=('k1=1,k2=2\nk3=3,k4=4\nk5=5,k6=6\nk7=7,k8=8')),
     None, None, False),

    # Test no keys
    ('Verify no keys. Causes MissingKeybindingWarning',
     dict(kb=[],
          width=100,
          exp_rtn=''),
     None, MissingKeybindingsWarning, True),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_FORMAT_KEYS)
@simplified_test_function
def test_format_keys(testcase, kb, width, exp_rtn):
    """
    Test function for _output_formatting.format_keys()
    """

    kbs = CIMInstanceName('blah', kb)

    # The code to be tested
    act_rtn = format_keys(kbs, width)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn == exp_rtn


TESTCASES_HIDE_EMPTY_COLUMNS = [
    # Testcases for _output_formatting.hide_empty_columns()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
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
    """
    Test function for _output_formatting.hide_empty_columns()
    """

    # The code to be tested
    act_rtn_headrs, act_rtn_rows = hide_empty_columns(headers, rows)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_rtn_rows == exp_rtn['rows']
    assert act_rtn_headrs == exp_rtn['headers']


TESTCASES_FOLD_STRINGS = [
    # Testcases for _output_formatting.fold_strings()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * input_str: The input string or list of strings to be folded
    #   * max_width: Max width of line in result
    #   * brk_long_wds: Boolean flag to request long words be folded
    #   * brk_hyphen: Boolean flag to request that fold occur on hyphens
    #   * fold_list: Sets the fold_list_items argument boolean value
    #   * separator:
    #   * init_indent:
    #   * sub_indent:
    #   * exp_rtn: String defining expected result
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    ('Verify String does not change with max_len > string length',
     dict(input_str='The red fox jumped over the fence',
          max_width=100,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent=None,
          exp_rtn='The red fox jumped over the fence'),
     None, None, True),

    ('Verify String folds with small len',
     dict(input_str='The red fox jumped over the fence',
          max_width=5,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent=None,
          exp_rtn='The\nred\nfox\njumped\nover\nthe\nfence'),
     None, None, True),

    ('Verify String folds once',
     dict(input_str='The red fox jumped over the fence',
          max_width=18,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent=None,
          exp_rtn='The red fox jumped\nover the fence'),
     None, None, True),

    ('Verify String with fold already in string',
     dict(input_str='The red fox jumped\nover the fence',
          max_width=19,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent=None,
          exp_rtn='The red fox jumped\nover the fence'),
     None, None, True),

    ('Verify String with existing fold refolds',
     dict(input_str='The red\nfox jumped over\nthe fence',
          max_width=19,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent=None,
          exp_rtn='The red fox jumped\nover the fence'),
     None, None, True),

    ('Verify String with existing fold refolds with initial indent string',
     dict(input_str='The red\nfox jumped over\nthe fence',
          max_width=19,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent='    ',
          sub_indent=None,
          exp_rtn='    The red fox\njumped over the\nfence'),
     None, None, True),

    ('Verify String with existing fold refolds with initial indent integer',
     dict(input_str='The red\nfox jumped over\nthe fence',
          max_width=19,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=4,
          sub_indent=None,
          exp_rtn='    The red fox\njumped over the\nfence'),
     None, None, True),

    ('Verify String with existing fold refolds with subsequent indent string',
     dict(input_str='The red\nfox jumped over\nthe fence',
          max_width=19,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent='    ',
          exp_rtn='The red fox jumped\n    over the fence'),
     None, None, True),

    ('Verify String with existing fold refolds with subsequent indent integer',
     dict(input_str='The red\nfox jumped over\nthe fence',
          max_width=19,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent=4,
          exp_rtn='The red fox jumped\n    over the fence'),
     None, None, True),

    ('Verify String folds with longword',
     dict(input_str='Theredfoxjumped over the fence',
          max_width=10,
          brk_long_wds=True,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent=None,
          exp_rtn='Theredfoxj\numped over\nthe fence'),
     None, None, True),

    ('Verify String folds with hyphen in words but brk_hyphen=False',
     dict(input_str='The red-green-blue fox jumped over the '
                    'pink-orange-white fence',
          max_width=10,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent=None,
          exp_rtn='The\nred-green-blue\nfox jumped\nover the\n'
                  'pink-orange-white\nfence'),
     None, None, True),

    ('Verify String folds with hyphen in words but brk_hyphen=True',
     dict(input_str='The red-green-blue fox jumped over the '
                    'pink-orange-white fence',
          max_width=10,
          brk_long_wds=False,
          brk_hyphen=True,
          fold_list=None,
          separator=None,
          init_indent=None,
          sub_indent=None,
          exp_rtn='The red-\ngreen-blue\nfox jumped\nover the\n'
                  'pink-\norange-\nwhite\nfence'),
     None, None, True),

    ('Verify String list folds each item into single string separator=" "',
     dict(input_str=['The red fox jumped over the fence.',
                     'The red fox jumped over the fence.'],
          max_width=27,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=None,
          separator=" ",
          init_indent=None,
          sub_indent=None,
          exp_rtn='The red fox jumped over the\nfence. The red fox jumped\n'
                  'over the fence.'),
     None, None, True),

    ('Verify String list folds each item into separate line separator=" "',
     dict(input_str=['The red fox jumped over the fence.',
                     'The red fox jumped over the fence.'],
          max_width=27,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=True,
          separator=None,
          init_indent=None,
          sub_indent=None,
          exp_rtn='The red fox jumped over the\nfence.\nThe red fox jumped '
                  'over the\nfence.'),
     None, None, True),

    ('Verify String list folds each item into separate line separator=" "  with'
     'with subsequent indent',
     dict(input_str=['The red fox jumped over the fence.',
                     'The red fox jumped over the fence.'],
          max_width=27,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=True,
          separator=None,
          init_indent=0,
          sub_indent=4,
          exp_rtn='The red fox jumped over the\n    fence.\nThe red fox '
                  'jumped over the\n    fence.'),
     None, None, True),

    ('Verify String list of words folds properly',
     dict(input_str=['The', 'red', 'fox', 'jumped', 'over', 'the', 'fence.'],
          max_width=10,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=False,
          separator=" ",
          init_indent=0,
          sub_indent=0,
          exp_rtn='The red\nfox jumped\nover the\nfence.'),
     None, None, True),

    ('Verify String list of words folds properly',
     dict(input_str=['The', 'red', 'fox', 'jumped', 'over', 'the', 'fence.'],
          max_width=3,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=False,
          separator=" ",
          init_indent=0,
          sub_indent=0,
          exp_rtn='The\nred\nfox\njumped\nover\nthe\nfence.'),
     None, None, True),

    ('Verify String list of words folds properly',
     dict(input_str=['The', 'red', 'fox', 'jumped', 'over', 'the', 'fence.'],
          max_width=90,
          brk_long_wds=False,
          brk_hyphen=False,
          fold_list=False,
          separator=" ",
          init_indent=None,
          sub_indent=None,
          exp_rtn='The red fox jumped over the fence.'),
     None, None, True),

]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_FOLD_STRINGS)
@simplified_test_function
def test_fold_strings(testcase, input_str, max_width, brk_long_wds, brk_hyphen,
                      fold_list, separator, init_indent, sub_indent, exp_rtn):
    """
    Test function for _output_formatting.fold_strings()
    """

    initial_indent = init_indent or 0
    subsequent_indent = sub_indent or 0

    # The code to be tested
    act_rtn = fold_strings(input_str, max_width,
                           break_long_words=brk_long_wds,
                           break_on_hyphens=brk_hyphen,
                           fold_list_items=fold_list,
                           separator=separator,
                           initial_indent=initial_indent,
                           subsequent_indent=subsequent_indent)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    if act_rtn != exp_rtn:
        print('IN\n{0}\nEXP\n{1}\nACT\n{2}\n'.format(input_str, exp_rtn,
                                                     act_rtn))
    assert act_rtn == exp_rtn


# NOTE: Format table tests are in test_tableformat.py
