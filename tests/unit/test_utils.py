# (C) Copyright 2021 Inova Development Inc.
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
Tests for _utils.py module
"""

from __future__ import absolute_import, print_function

import os
import shutil
import mock
import click
import six
import pytest
from pywbemtools._utils import ensure_bytes, ensure_unicode, \
    to_unicode, get_terminal_width
import pywbemtools._utils

from .pytest_extensions import simplified_test_function

# pylint: disable=use-dict-literal

TESTCASES_ENSURE_BYTES = [

    # Testcases for ensure_bytes()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: input object
    #   * exp_result: expected returned object
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Input object is None",
        dict(
            obj=None,
            exp_result=None,
        ),
        None, None, True
    ),
    (
        "Input object is an integer",
        dict(
            obj=42,
            exp_result=42,
        ),
        None, None, True
    ),
    (
        "Input object is an empty Byte string",
        dict(
            obj=b'',
            exp_result=b'',
        ),
        None, None, True
    ),
    (
        "Input object is a Byte string with 7-bit ASCII chars",
        dict(
            obj=b'abc',
            exp_result=b'abc',
        ),
        None, None, True
    ),
    (
        "Input object is a Byte string with UCS-2 chars",
        dict(
            # UCS-2 char U+00E9: LATIN SMALL LETTER E WITH ACUTE
            obj=b'a\xC3\xA9b',
            exp_result=b'a\xC3\xA9b',
        ),
        None, None, True
    ),
    (
        "Input object is a Byte string with UCS-4 chars",
        dict(
            # UCS-4 char U+010142: GREEK ACROPHONIC ATTIC ONE DRACHMA
            obj=b'a\xF0\x90\x85\x82b',
            exp_result=b'a\xF0\x90\x85\x82b',
        ),
        None, None, True
    ),
    (
        "Input object is an empty Unicode string",
        dict(
            obj=u'',
            exp_result=b'',
        ),
        None, None, True
    ),
    (
        "Input object is a Unicode string with 7-bit ASCII chars",
        dict(
            obj=u'abc',
            exp_result=b'abc',
        ),
        None, None, True
    ),
    (
        "Input object is a Unicode string with UCS-2 chars",
        dict(
            # UCS-2 char U+00E9: LATIN SMALL LETTER E WITH ACUTE
            obj=u'a\u00E9b',
            exp_result=b'a\xC3\xA9b',
        ),
        None, None, True
    ),
    (
        "Input object is a Unicode string with UCS-4 chars",
        dict(
            # UCS-4 char U+010142: GREEK ACROPHONIC ATTIC ONE DRACHMA
            obj=u'a\U00010142b',
            exp_result=b'a\xF0\x90\x85\x82b',
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_ENSURE_BYTES)
@simplified_test_function
def test_ensure_bytes(testcase, obj, exp_result):
    """
    Test function for ensure_bytes().
    """

    # The code to be tested
    act_result = ensure_bytes(obj)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_result


TESTCASES_ENSURE_UNICODE = [

    # Testcases for ensure_unicode()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: input object
    #   * exp_result: expected returned object
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Input object is None",
        dict(
            obj=None,
            exp_result=None,
        ),
        None, None, True
    ),
    (
        "Input object is an integer",
        dict(
            obj=42,
            exp_result=42,
        ),
        None, None, True
    ),
    (
        "Input object is an empty Byte string",
        dict(
            obj=b'',
            exp_result=u'',
        ),
        None, None, True
    ),
    (
        "Input object is a Byte string with 7-bit ASCII chars",
        dict(
            obj=b'abc',
            exp_result=u'abc',
        ),
        None, None, True
    ),
    (
        "Input object is a Byte string with UCS-2 chars",
        dict(
            # UCS-2 char U+00E9: LATIN SMALL LETTER E WITH ACUTE
            obj=b'a\xC3\xA9b',
            exp_result=u'a\u00E9b',
        ),
        None, None, True
    ),
    (
        "Input object is a Byte string with UCS-4 chars",
        dict(
            # UCS-4 char U+010142: GREEK ACROPHONIC ATTIC ONE DRACHMA
            obj=b'a\xF0\x90\x85\x82b',
            exp_result=u'a\U00010142b',
        ),
        None, None, True
    ),
    (
        "Input object is an empty Unicode string",
        dict(
            obj=u'',
            exp_result=u'',
        ),
        None, None, True
    ),
    (
        "Input object is a Unicode string with 7-bit ASCII chars",
        dict(
            obj=u'abc',
            exp_result=u'abc',
        ),
        None, None, True
    ),
    (
        "Input object is a Unicode string with UCS-2 chars",
        dict(
            # UCS-2 char U+00E9: LATIN SMALL LETTER E WITH ACUTE
            obj=u'a\u00E9b',
            exp_result=u'a\u00E9b',
        ),
        None, None, True
    ),
    (
        "Input object is a Unicode string with UCS-4 chars",
        dict(
            # UCS-4 char U+010142: GREEK ACROPHONIC ATTIC ONE DRACHMA
            obj=u'a\U00010142b',
            exp_result=u'a\U00010142b',
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_ENSURE_UNICODE)
@simplified_test_function
def test_ensure_unicode(testcase, obj, exp_result):
    """
    Test function for ensure_unicode().
    """

    # The code to be tested
    act_result = ensure_unicode(obj)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_result


TESTCASES_TO_UNICODE = [

    # Testcases for to_unicode()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * obj: input object
    #   * exp_result: expected returned object
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Input object is None",
        dict(
            obj=None,
            exp_result=None,
        ),
        AttributeError, None, True
    ),
    (
        "Input object is an integer",
        dict(
            obj=42,
            exp_result=None,
        ),
        AttributeError, None, True
    ),
    (
        "Input object is a Unicode string",
        dict(
            obj=u'abc',
            exp_result=u'abc',
        ),
        AttributeError if six.PY3 else None, None, True
    ),
    (
        "Input object is an empty Byte string",
        dict(
            obj=b'',
            exp_result=u'',
        ),
        None, None, True
    ),
    (
        "Input object is a Byte string with 7-bit ASCII chars",
        dict(
            obj=b'abc',
            exp_result=u'abc',
        ),
        None, None, True
    ),
    (
        "Input object is a Byte string with UCS-2 chars",
        dict(
            # UCS-2 char U+00E9: LATIN SMALL LETTER E WITH ACUTE
            obj=b'a\xC3\xA9b',
            exp_result=u'a\u00E9b',
        ),
        None, None, True
    ),
    (
        "Input object is a Byte string with UCS-4 chars",
        dict(
            # UCS-4 char U+010142: GREEK ACROPHONIC ATTIC ONE DRACHMA
            obj=b'a\xF0\x90\x85\x82b',
            exp_result=u'a\U00010142b',
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_TO_UNICODE)
@simplified_test_function
def test_to_unicode(testcase, obj, exp_result):
    """
    Test function for to_unicode().
    """

    # The code to be tested
    act_result = to_unicode(obj)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert act_result == exp_result


# Special value to expect the actual terminal width.
ACTUAL_TERMINAL_WIDTH = -1

TESTCASES_GET_TERMINAL_WIDTH = [

    # Testcases for get_terminal_width()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * termwidth_env: Input value for TERMWIDTH_ENVVAR env var, None for
    #     unsetting it.
    #   * use_terminal_width_conf: Input value for USE_TERMINAL_WIDTH config
    #     parameter, None for using the built-in default.
    #   * default_table_width_conf: Input value for DEFAULT_TABLE_WIDTH config
    #     parameter, None for using the built-in default.
    #   * exp_result: Expected returned terminal width. The special value
    #     ACTUAL_TERMINAL_WIDTH can be used to expect the actual terminal width.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "All defaults",
        dict(
            termwidth_env=None,
            use_terminal_width_conf=None,
            default_table_width_conf=None,
            exp_result=ACTUAL_TERMINAL_WIDTH,
        ),
        None, None, True
    ),
    (
        "Setting terminal width in environment to an integer",
        dict(
            termwidth_env='83',
            use_terminal_width_conf=None,
            default_table_width_conf=None,
            exp_result=83,
        ),
        None, None, True
    ),
    (
        "Setting terminal width in environment to a string (ignored)",
        dict(
            termwidth_env='abc',
            use_terminal_width_conf=None,
            default_table_width_conf=None,
            exp_result=ACTUAL_TERMINAL_WIDTH,
        ),
        None, None, True
    ),
    (
        "Configured to use click terminal width",
        dict(
            termwidth_env=None,
            use_terminal_width_conf=True,
            default_table_width_conf=83,
            exp_result=ACTUAL_TERMINAL_WIDTH,
        ),
        None, None, True
    ),
    (
        "Configured to use configured default terminal width",
        dict(
            termwidth_env=None,
            use_terminal_width_conf=False,
            default_table_width_conf=83,
            exp_result=83,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_GET_TERMINAL_WIDTH)
@simplified_test_function
def test_get_terminal_width(
        testcase, termwidth_env, use_terminal_width_conf,
        default_table_width_conf, exp_result):
    """
    Test function for get_terminal_width().
    """

    termwidth_envvar = 'PYWBEMTOOLS_TERMWIDTH'

    # Save the environment variable
    saved_termwidth = os.environ.get(termwidth_envvar, None)

    try:
        # Set the environment variable as needed by the testcase
        if termwidth_env is None:
            try:
                del os.environ[termwidth_envvar]
            except KeyError:
                pass
        else:
            os.environ[termwidth_envvar] = termwidth_env

        # pylint: disable=protected-access

        # Prepare the patching of the config parameters. Because this is done
        # using the context manager ability of the mock object, we always patch
        # but use the original value if the testcase does not intend to change
        # it.
        if use_terminal_width_conf is None:
            use_terminal_width_conf = pywbemtools._utils.USE_TERMINAL_WIDTH
        use_terminal_width_mock = mock.patch.object(
            pywbemtools._utils, 'USE_TERMINAL_WIDTH', use_terminal_width_conf
        )
        if default_table_width_conf is None:
            default_table_width_conf = pywbemtools._utils.DEFAULT_TABLE_WIDTH
        default_table_width_mock = mock.patch.object(
            pywbemtools._utils, 'DEFAULT_TABLE_WIDTH', default_table_width_conf
        )

        # pylint: enable=protected-access

        with use_terminal_width_mock:
            with default_table_width_mock:

                # The code to be tested
                act_result = get_terminal_width()

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None

        if exp_result == ACTUAL_TERMINAL_WIDTH:
            try:
                exp_result = shutil.get_terminal_size()[0]
            except AttributeError:
                # pylint: disable=no-member
                exp_result = click.get_terminal_size()[0]

        assert act_result == exp_result

    finally:

        # Restore the environment variable
        if saved_termwidth is None:
            del os.environ[termwidth_envvar]
        else:
            os.environ[termwidth_envvar] = saved_termwidth


# The pywbemtools_warn() and pywbemtools_warn_explicit() functions are not
# tested directly because the pytest capturing of warnings nullifies their
# patching of warnings.formatwarning(). These functions are tested indirectly
# though, by the tests that invoke the pywbemtools commands.
