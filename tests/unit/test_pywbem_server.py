#!/usr/bin/env python

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
Unit tests for PywbemServer class methods.
"""

from __future__ import absolute_import, print_function

import pytest

from pywbemtools.pywbemcli._pywbem_server import PywbemServer

from tests.unit.pytest_extensions import simplified_test_function


TESTCASES_INITIALIZE = [
    # TESTCASES for pywbem_server intitalize
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * init_kwargs: __init__ kwargs.
    #   * exp_attrs: Dict of expected attributes of resulting object.
    #   * exp_repr: string
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Verify url arg only",
        dict(
            init_args=[],
            init_kwargs=dict(
                server='http://localhost',
            ),
            exp_attrs=dict(
                server=u'http://localhost',
                default_namespace='root/cimv2',
                user=None,
                password=None,
                verify=None,
                certfile=None,
                keyfile=None,
                mock_server=[]
            )
        ),
        None, None, True
    ),
    (
        "Verify multiple arguments",
        dict(
            init_args=[],
            init_kwargs=dict(
                server='http://localhost',
                default_namespace='root/cimv2',
                user='fred',
                password='blah',
            ),
            exp_attrs=dict(
                server=u'http://localhost',
                default_namespace='root/cimv2',
                user='fred',
                password='blah',
                verify=None,
                certfile=None,
                keyfile=None,
                mock_server=[]
            )
        ),
        None, None, True
    ),
    (
        "Verify url arg only",
        dict(
            init_args=[],
            init_kwargs=dict(
                server='http://localhost',
                default_namespace='root/cimv3',
                user='fred',
                password='blah',
                verify=True,
                certfile='mycert.pem',
                keyfile='mykey.pem'
            ),
            exp_attrs=dict(
                server=u'http://localhost',
                default_namespace='root/cimv3',
                user='fred',
                password='blah',
                verify=True,
                certfile='mycert.pem',
                keyfile='mykey.pem',
                mock_server=[]
            )
        ),
        None, None, True
    ),
    (
        "Verify mockfile",
        dict(
            init_args=[],
            init_kwargs=dict(
                mock_server='testmock.mof',
            ),
            exp_attrs=dict(
                server=None,
                default_namespace='root/cimv2',
                user=None,
                password=None,
                verify=None,
                certfile=None,
                keyfile=None,
                mock_server='testmock.mof'
            )
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_INITIALIZE)
@simplified_test_function
def test_initialize(testcase, init_args, init_kwargs, exp_attrs):
    """
    Test object construction
    """
    svr = PywbemServer(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert svr.server == exp_attrs['server']
    assert svr.default_namespace == exp_attrs['default_namespace']
    assert svr.user == exp_attrs['user']
    assert svr.password == exp_attrs['password']
    assert svr.verify == exp_attrs['verify']
    assert svr.certfile == exp_attrs['certfile']
    assert svr.keyfile == exp_attrs['keyfile']
    assert svr.mock_server == exp_attrs['mock_server']

    # assert '{0}'.format(svr) == \
    #                 "PywbemServer(url=http://localhost name=default)"


TESTCASES_CONNECT = [
    # TESTCASES for pywbem_server connect
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * init_kwargs: __init__ positional args.
    #   * exp_attrs: Dict of expected attributes of resulting object.
    #   * exp_repr: string
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Verify url arg only",
        dict(
            init_args=[],
            init_kwargs=dict(
                server='http://localhost',
            ),
            exp_attrs=dict(
                server=u'http://localhost',
                default_namespace='root/cimv2',
                user=None,
                password=None,
                verify=None,
                certfile=None,
                keyfile=None,
                ca_certs=None,
                mock_server=None
            )
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_CONNECT)
@simplified_test_function
def test_connect(testcase, init_args, init_kwargs, exp_attrs):
    """
    Test object connect
    """
    svr = PywbemServer(*init_args, **init_kwargs)

    # connect and test connection results
    svr.create_connection(False)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert svr.server == exp_attrs['server']
    assert svr.default_namespace == exp_attrs['default_namespace']
    assert svr.user == exp_attrs['user']
    assert svr.password == exp_attrs['password']
    assert svr.verify == exp_attrs['verify']
    assert svr.certfile == exp_attrs['certfile']
    assert svr.keyfile == exp_attrs['keyfile']


# TODO test name setter
# TODO password setter
# TODO invalid timeout value
# TODO password prompt (get_password)
# TODO str and repr strings
