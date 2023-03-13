# -*- coding: utf-8 -*-
# (C) Copyright 2020 IBM Corp.
# (C) Copyright 2020 Inova Development Inc.
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
Tests for _common.py functions.  This is a unit test of the function and its
API, not a test of pywbemcli commands.
"""

from __future__ import absolute_import, print_function

import sys
from datetime import datetime
from packaging.version import parse as parse_version
import pytest

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict  # pylint: disable=import-error

from pywbem import CIMProperty, CIMInstance, CIMInstanceName, Uint32, Uint64, \
    Sint32, CIMDateTime, __version__

from pywbemtools.pywbemcli._display_cimobjects import \
    _format_instances_as_rows, _display_instances_as_table

from pywbemtools._output_formatting import DEFAULT_MAX_CELL_WIDTH

from ..pytest_extensions import simplified_test_function

# pylint: disable=use-dict-literal

OK = True    # mark tests OK when they execute correctly
RUN = True    # Mark OK = False and current test case being created RUN
FAIL = False  # Any test currently FAILING or not tested yet
SKIP = False  # mark tests that are to be skipped.

DATETIME1_DT = datetime(2014, 9, 22, 10, 49, 20, 524789)
DATETIME1_OBJ = CIMDateTime(DATETIME1_DT)
DATETIME1_STR = '"20140922104920.524789+000"'

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


# NOTE: The following methods are testcase parameters.  They define instances
# used in TESTCASES_FMT_INSTANCE_AS_ROWS
def simple_instance(pvalue=None):
    """
    Build a simple instance to test and return that instance. The properties
    in the instance are sorted by (lower cased) property name.

    If the parameter pvalue is provided, it must be a scalar value and an
    instance with a single property with that value is returned.
    """
    if pvalue:
        properties = [CIMProperty("P", pvalue)]
    else:
        properties = [
            CIMProperty("Pbf", value=False),
            CIMProperty("Pbt", value=True),
            CIMProperty("Pdt", DATETIME1_OBJ),
            CIMProperty("Pint32", Uint32(99)),
            CIMProperty("Pint64", Uint64(9999)),
            CIMProperty("Pstr1", u"Test String"),
        ]
    inst = CIMInstance("CIM_Foo", properties)
    return inst


def array_instance(pvalue, ptype):
    """
    Build an instance with a single property named P and the value  and type
    defined. Used to build test instance with array properties because
    type cannot be determined from the data since it is an array.
    """
    properties = [CIMProperty("P", pvalue, type=ptype)]
    return CIMInstance("CIM_Foo", properties)


def simple_instance_unsorted(pvalue=None):
    """
    Build a simple instance to test and return that instance. The properties
    in the instance are not sorted by (lower cased) property name, but
    the property order when sorted is the same as in the instance returned by
    simple_instance().

    If the parameter pvalue is provided, it must be a scalar value and an
    instance with a single property with that value is returned.
    """
    if pvalue:
        properties = [CIMProperty("P", pvalue)]
    else:
        properties = [
            CIMProperty("Pbt", value=True),
            CIMProperty("Pbf", value=False),  # out of order
            CIMProperty("pdt", DATETIME1_OBJ),  # lower cased
            CIMProperty("PInt64", Uint64(9999)),  # out of order when case ins.
            CIMProperty("Pint32", Uint32(99)),
            CIMProperty("Pstr1", u"Test String"),
        ]
    inst = CIMInstance("CIM_Foo", properties)
    return inst


def simple_instance2(pvalue=None):
    """
    Build a simple instance to test and return that instance. The properties
    in the instance are sorted by (lower cased) property name.

    If the parameter pvalue is provided, it must be a scalar value and an
    instance with a single property with that value is returned.
    """
    if pvalue:
        properties = [CIMProperty("P", pvalue)]
    else:
        properties = [
            CIMProperty("Pbf", value=False),
            CIMProperty("Pbt", value=True),
            CIMProperty("Pdt", DATETIME1_OBJ),
            CIMProperty("Pint64", Uint64(9999)),
            CIMProperty("Psint32", Sint32(-2147483648)),
            CIMProperty("Pstr1", u"Test String"),
            CIMProperty("Puint32", Uint32(4294967295)),
        ]
    inst = CIMInstance("CIM_Foo", properties)
    return inst


def simple_array_instance2(pvalue=None):
    """
    Build a simple instance to test and return that instance. The properties
    in the instance are sorted by (lower cased) property name.

    For this test all of the array elements have a single value
    """
    if pvalue:
        properties = [CIMProperty("P", pvalue)]
    else:
        properties = [
            CIMProperty("Pbf", is_array=True, value=[False]),
            CIMProperty("Pbt", is_array=True, value=[True]),
            CIMProperty("Pdt", is_array=True, value=[DATETIME1_OBJ]),
            CIMProperty("Pint64", is_array=True, value=[Uint64(9999)]),
            CIMProperty("Psint32", is_array=True, value=[Sint32(-2147483648)]),
            CIMProperty("Pstr1", is_array=True, value=[u"Test String"]),
            CIMProperty("Puint32", is_array=True, value=[Uint32(4294967295)]),
        ]
    inst = CIMInstance("CIM_Foo", properties)
    return inst


def simple_array_instance21(pvalue=None):
    """
    Build a simple instance to test and return that instance. The properties
    in the instance are sorted by (lower cased) property name.

    For this test all of the array elements have a two values
    """
    if pvalue:
        properties = [CIMProperty("P", pvalue)]
    else:
        properties = [
            CIMProperty("Pbf", is_array=True, value=[False, False]),
            CIMProperty("Pbt", is_array=True, value=[True, True]),
            CIMProperty("Pdt", is_array=True, value=[DATETIME1_OBJ,
                                                     DATETIME1_OBJ]),
            CIMProperty("Pint64", is_array=True, value=[Uint64(9999),
                                                        Uint64(9999)]),
            CIMProperty("Psint32", is_array=True, value=[Sint32(-2147483648),
                                                         Sint32(-2147483648)]),
            CIMProperty("Pstr1", is_array=True, value=[u"Test String",
                                                       u"Test String"]),
            CIMProperty("Puint32", is_array=True, value=[Uint32(4294967295),
                                                         Uint32(4294967295)]),
        ]
    inst = CIMInstance("CIM_Foo", properties)
    return inst


def string_instance(tst_str):
    """
    Build a CIM instance with a single property.
    """
    properties = [CIMProperty("Pstr1", tst_str)]
    inst = CIMInstance("CIM_Foo", properties)
    return inst


# Testcases for _format_instances_as_rows()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * args: Positional args for _format_instances_as_rows().
    #   * kwargs: Keyword args for _format_instances_as_rows().
    #   * exp_rtn: Expected return value of _format_instances_as_rows().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_rtn: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

TESTCASES_FORMAT_INSTANCES_AS_ROWS = [
    (
        "Verify simple instance to table",
        dict(
            args=([simple_instance()], None),
            kwargs={},
            exp_rtn=[
                ["false", "true", DATETIME1_STR, "99", "9999",
                 u'"Test String"']],
        ),
        None, None, OK),

    (
        "Verify simple instance to table with quote_strings=False",
        dict(
            args=(),
            kwargs=dict(
                insts=[simple_instance()],
                max_cell_width=DEFAULT_MAX_CELL_WIDTH,
                quote_strings=False),
            exp_rtn=[
                ["false", "true", DATETIME1_STR, "99", "9999",
                 u'Test String']],
        ),
        None, None, OK),

    (
        "Verify simple instance str array to table with quote_strings=False",
        dict(
            args=(),
            kwargs=dict(
                insts=[simple_instance(pvalue=["abc", 'def'])],
                max_cell_width=DEFAULT_MAX_CELL_WIDTH,
                quote_strings=False),
            exp_rtn=[
                ['"abc", "def"']],
        ),
        None, None, OK),
    (

        "Verify simple instance int array with quote_strings=True",
        dict(
            args=(),
            kwargs=dict(
                insts=[array_instance(pvalue=[Uint32(12345), Uint32(67891)],
                                      ptype='uint32')],
                max_cell_width=DEFAULT_MAX_CELL_WIDTH,
                quote_strings=True),
            exp_rtn=[
                ['12345, 67891']],
        ),
        None, None, OK),

    (
        "Verify simple instance int array with col limit,quote_strings=True",
        dict(
            args=(),
            kwargs=dict(
                insts=[array_instance(pvalue=[Uint32(12345), Uint32(67891)],
                                      ptype='uint32')],
                max_cell_width=6,
                quote_strings=True),
            exp_rtn=[
                ['12345,\n67891']],
        ),
        None, None, OK),

    (
        "Verify simple instance int array with quote_strings=False",
        dict(
            args=(),
            kwargs=dict(
                insts=[array_instance(pvalue=[Uint32(12345), Uint32(67891)],
                                      ptype='uint32')],
                max_cell_width=DEFAULT_MAX_CELL_WIDTH,
                quote_strings=False),
            exp_rtn=[
                ['12345, 67891']],
        ),
        None, None, OK),

    (
        "Verify simple instance int array with col limit,quote_strings=False",
        dict(
            args=(),
            kwargs=dict(
                insts=[array_instance(pvalue=[Uint32(12345), Uint32(67891)],
                                      ptype='uint32')],
                max_cell_width=6,
                quote_strings=False),
            exp_rtn=[
                ['12345,\n67891']],
        ),
        None, None, OK),

    (
        "Verify simple instance to table with col limit",
        dict(
            args=([simple_instance()], 30),
            kwargs={},
            exp_rtn=[
                ["false", "true", DATETIME1_STR, "99", "9999",
                 u'"Test String"']],
        ),
        None, None, OK),

    (
        "Verify simple instance to table, unsorted",
        dict(
            args=([simple_instance_unsorted()],
                  DEFAULT_MAX_CELL_WIDTH,),
            kwargs={},
            exp_rtn=[
                ["false", "true", DATETIME1_STR, "99", "9999",
                 u'"Test String"']],
        ),
        None, None, OK),

    (
        "Verify instance with 2 keys and 2 non-keys, unsorted",
        dict(
            args=(),
            kwargs=dict(
                insts=[
                    CIMInstance(
                        "CIM_Foo",
                        properties=[
                            CIMProperty("P2", value="V2"),
                            CIMProperty("p1", value="V1"),
                            CIMProperty("Q2", value="K2"),
                            CIMProperty("q1", value="K1"),
                        ],
                        path=CIMInstanceName(
                            "CIM_Foo",
                            keybindings=[
                                CIMProperty("Q2", value="K2"),
                                CIMProperty("q1", value="K1"),
                            ]
                        ),
                    ),
                ],
                max_cell_width=DEFAULT_MAX_CELL_WIDTH,
            ),
            exp_rtn=[
                ['"K1"', '"K2"', '"V1"', '"V2"'],
            ],
        ),
        None, None, OK),

    (
        "Verify 2 instances with different sets of properties",
        dict(
            args=(),
            kwargs=dict(
                insts=[
                    CIMInstance(
                        "CIM_Foo",
                        properties=[
                            CIMProperty("P2", value="VP2a"),
                            CIMProperty("p1", value="VP1a"),
                            CIMProperty("P3", value="VP3a"),
                        ],
                    ),
                    CIMInstance(
                        "CIM_FooSub",
                        properties=[
                            CIMProperty("P2", value="VP2b"),
                            CIMProperty("p1", value="VP1b"),
                            CIMProperty("N1", value="VN1b"),
                        ],
                    ),
                ],
                max_cell_width=DEFAULT_MAX_CELL_WIDTH,
            ),
            exp_rtn=[
                ['', '"VP1a"', '"VP2a"', '"VP3a"'],
                ['"VN1b"', '"VP1b"', '"VP2b"', ''],
            ],
        ),
        None, None, OK),

    (
        "Verify 2 instances where second one has path",
        dict(
            args=(),
            kwargs=dict(
                insts=[
                    CIMInstance(
                        "CIM_Foo",
                        properties=[
                            CIMProperty("P2", value="VP2a"),
                            CIMProperty("p1", value="VP1a"),
                        ],
                    ),
                    CIMInstance(
                        "CIM_FooSub",
                        properties=[
                            CIMProperty("P2", value="VP2b"),
                            CIMProperty("p1", value="VP1b"),
                            CIMProperty("Q2", value="K2b"),
                            CIMProperty("q1", value="K1b"),
                        ],
                        path=CIMInstanceName(
                            "CIM_Foo",
                            keybindings=[
                                CIMProperty("q2", value="K2b"),
                                CIMProperty("Q1", value="K1b"),
                            ]
                        ),
                    ),
                ],
                max_cell_width=DEFAULT_MAX_CELL_WIDTH,
            ),
            exp_rtn=[
                ['', '', '"VP1a"', '"VP2a"'],
                ['"K1b"', '"K2b"', '"VP1b"', '"VP2b"'],
            ],
        ),
        None, None, OK),

    (
        "Verify simple instance with one string all components overflow line1",
        dict(
            args=([simple_instance(pvalue="A B C D")],
                  4),
            kwargs={},
            exp_rtn=[
                ['"A "\n"B "\n"C "\n"D"']],
        ),
        None, None, OK),

    (
        "Verify simple instance with one string all components overflow line2",
        dict(
            args=([simple_instance(pvalue="ABCD")],
                  4),
            kwargs={},
            exp_rtn=[
                ['"AB"\n"CD"']],
        ),
        None, None, OK),

    (
        "Verify simple instance with one string overflows line",
        dict(
            args=([simple_instance(pvalue="A B C D")],
                  8),
            kwargs={},
            exp_rtn=[
                ['"A B C "\n"D"']],
        ),
        None, None, OK),

    (
        "Verify simple instance withone unit32 max val",
        dict(
            args=([simple_instance(pvalue=Uint32(4294967295))],
                  8),
            kwargs={},
            exp_rtn=[
                ['4294967295']],
        ),
        None, None, OK),


    (
        "Verify simple instance with one string fits on line",
        dict(
            args=([simple_instance(pvalue="A B C D")],
                  12),
            kwargs={},
            exp_rtn=[
                ['"A B C D"']],
        ),
        None, None, OK),

    (
        "Verify datetime property, folded",
        dict(
            args=([simple_instance(pvalue=DATETIME1_OBJ)],
                  20),
            kwargs={},
            exp_rtn=[
                ['"20140922104920.524"\n"789+000"']],
        ),
        None, None, OK),

    (
        "Verify datetime property not folded",
        dict(
            args=([simple_instance(pvalue=DATETIME1_OBJ)],
                  30),
            kwargs={},
            exp_rtn=[
                ['"20140922104920.524789+000"']],
        ),
        None, None, OK),

    (
        "Verify integer property where len too small",
        dict(
            args=([simple_instance(pvalue=Uint32(999999))],
                  4),
            kwargs={},
            exp_rtn=[['999999']],
        ),
        None, None, OK),

    (
        "Verify char16 property",
        dict(
            args=([CIMInstance('P', [CIMProperty('P',
                                                 type='char16',
                                                 value='f')])],
                  4),
            kwargs={},
            exp_rtn=[[u"'f'"]],
        ),
        None, None, OK),

    (
        "Verify properties with no value",
        dict(
            args=([CIMInstance('P', [CIMProperty('P', value=None,
                                                 type='char16'),
                                     CIMProperty('Q', value=None,
                                                 type='uint32'),
                                     CIMProperty('R', value=None,
                                                 type='string'), ])],
                  4),
            kwargs={},
            exp_rtn=[[u'', u'', u'']],
        ),
        None, None, OK),

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
            kwargs={},
            exp_rtn=[
                [u'"/:REF_CLN.k1=\\"v1\\""']],
        ),
        None, None, OK),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_FORMAT_INSTANCES_AS_ROWS)
@simplified_test_function
def test_format_instances_as_rows(testcase, args, kwargs, exp_rtn):
    """
    Test the output of the common _format_instances_as_rows() function
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


# Testcases for _display_instances_as_table()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * args: Positional args for _display_instances_as_table().
    #   * kwargs: Keyword args for _display_instances_as_table().
    #   * exp_stdout: Expected output on stdout.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

TESTCASES_DISPLAY_INSTANCES_AS_TABLE = [
    (
        "Verify print of simple instance to table",
        dict(
            args=([simple_instance()], None, 'simple'),
            kwargs={},
            exp_stdout="""\
Instances: CIM_Foo
Pbf    Pbt    Pdt                     Pint32    Pint64  Pstr1
-----  -----  --------------------  --------  --------  -------------
false  true   "20140922104920.524"        99      9999  "Test String"
              "789+000"
""",

        ),
        None, None, not CLICK_ISSUE_1590
    ),
    (
        "Verify print of simple instance to table with col limit",
        dict(
            args=([simple_instance2()], 80, 'simple'),
            kwargs={},
            exp_stdout="""\
Instances: CIM_Foo
Pbf    Pbt    Pdt            Pint64      Psint32  Pstr1        Puint32
-----  -----  -----------  --------  -----------  --------  ----------
false  true   "201409221"      9999  -2147483648  "Test "   4294967295
              "04920.524"                         "String"
              "789+000"
""",
        ),
        None, None, not CLICK_ISSUE_1590
    ),

    (
        "Verify print of simple array instance to table with col limit",
        dict(
            args=([simple_array_instance2()], 80, 'simple'),
            kwargs={'ctx_options': None},
            exp_stdout="""\
Instances: CIM_Foo
Pbf    Pbt    Pdt            Pint64      Psint32  Pstr1        Puint32
-----  -----  -----------  --------  -----------  --------  ----------
false  true   "201409221"      9999  -2147483648  "Test "   4294967295
              "04920.524"                         "String"
              "789+000"
""",
        ),
        None, None, not CLICK_ISSUE_1590
    ),

    (
        "Verify print of simple array instance21 to table with col limit",
        dict(
            args=([simple_array_instance21()], 220, 'simple'),
            kwargs={'ctx_options': None},
            exp_stdout="""\
Instances: CIM_Foo
Pbf           Pbt         Pdt                                                       Pint64      Psint32                   Pstr1                         Puint32
------------  ----------  --------------------------------------------------------  ----------  ------------------------  ----------------------------  ----------------------
false, false  true, true  "20140922104920.524789+000", "20140922104920.524789+000"  9999, 9999  -2147483648, -2147483648  "Test String", "Test String"  4294967295, 4294967295
""",   # noqa: E501
        ),
        None, None, not CLICK_ISSUE_1590
    ),

    # The following test fails apparently in an issue in the capsys so marked
    # fail until we sort out issu es when a second instance is added. Did same
    # ctest above with very largeell size and another with single instance
    # and that works.  TODO
    (
        "Verify print of simple array instance21 to table with col limit",
        dict(
            args=([simple_array_instance21()], 80, 'simple'),
            kwargs={'ctx_options': None},
            exp_stdout="""\
Instances: CIM_Foo
Pbf    Pbt    Pdt          Pint64      Psint32  Pstr1        Puint32
-----  -----  ---------  --------  -----------  --------  ----------
false  true   "2014092"      9999  -2147483648  "Test "   4294967295
              "2104920"                         "String"
              ".524789"
              "+000"
false  true   "2014092"      9999  -2147483648  "Test "   4294967295
              "2104920"                         "String"
              ".524789"
              "+000"
""",
        ),
        None, None, FAIL  # WAS not CLICK_ISSUE_1590
    ),

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
            kwargs={'ctx_options': None},
            exp_stdout="""\
Instances: CIM_Foo
P
---------------------------
"/:REF_CLN.k1=\\"v1\\",k2=32"
""",
        ),
        None, None, not CLICK_ISSUE_1590 and PYWBEM_1_0_0B1
    ),
]

# NOTE: The following test cannot use simplified test function because it uses
# pytest capsys to capture date.


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_DISPLAY_INSTANCES_AS_TABLE)
def test_display_instances_as_table(
        desc, kwargs, exp_exc_types, exp_warn_types, condition, capsys):
    """
    Test the output of the print_insts_as_table function. This primarily
    tests for overall format and the ability of the function to output to
    stdout. The previous test tests the row formatting and handling of
    multiple instances.
    """
    if not condition:
        pytest.skip("Testcase condition not satisfied")

    # This logic only supports successful testcases without warnings
    assert exp_exc_types is None
    assert exp_warn_types is None

    args = kwargs['args']
    kwargs_ = kwargs['kwargs']
    exp_stdout = kwargs['exp_stdout']
    # The code to be tested
    _display_instances_as_table(*args, **kwargs_)

    stdout, _ = capsys.readouterr()

    assert exp_stdout == stdout, \
        "Unexpected output in test case: {}\n" \
        "Actual:\n" \
        "{}\n" \
        "Expected:\n" \
        "{}\n" \
        "End\n".format(desc, stdout, exp_stdout)
