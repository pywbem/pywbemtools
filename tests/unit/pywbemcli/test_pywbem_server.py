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

import os
import io
import pytest

from pywbemtools.pywbemcli._pywbem_server import PywbemServer

from tests.unit.pytest_extensions import simplified_test_function

# pylint: disable=use-dict-literal

OK = True
RUN = True
FAIL = False
PDB = "pdb"

# This is needed by the connect test. Just the file name
# created is required for WBEMConnection constructor with
# cert and key files.
SCRIPT_DIR = os.path.dirname(__file__)
FAKE_PEM = 'test.pem'
FAKE_PEM_PATH = os.path.join(SCRIPT_DIR, FAKE_PEM)


TESTCASES_PYSVR_INIT = [
    # Testcases for PywbemServer.__init__()
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * init_args: __init__() positional args.
    #   * init_kwargs: __init__() keyword args.
    #   * exp_attrs: Dict of expected attributes of resulting object.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "1. Verify url arg only",
        dict(
            init_args=[],
            init_kwargs=dict(
                server='http://localhost',
            ),
            exp_attrs=dict(
                server=u'http://localhost',
                default_namespace='root/cimv2',
                name='default',
                user=None,
                password=None,
                timeout=30,
                verify=None,
                use_pull=None,
                pull_max_cnt=None,
                certfile=None,
                keyfile=None,
                ca_certs=None,
                mock_server=[]
            )
        ),
        None, None, OK
    ),
    (
        "2. Verify server, default_namespace, user, password",
        dict(
            init_args=[],
            init_kwargs=dict(
                server='http://localhost',
                default_namespace='interop',
                user='fred',
                password='blah',
            ),
            exp_attrs=dict(
                server=u'http://localhost',
                default_namespace='interop',
                name='default',
                user='fred',
                password='blah',
                timeout=30,
                verify=None,
                use_pull=True,
                pull_max_cnt=100,
                certfile=None,
                keyfile=None,
                ca_certs=None,
                mock_server=[]
            )
        ),
        None, None, OK
    ),
    (
        "3. Verify url plus all allowed other arguments",
        dict(
            init_args=[],
            init_kwargs=dict(
                server='http://localhost',
                default_namespace='root/cimv3',
                user='fred',
                password='blah',
                timeout=50,
                use_pull=True,
                pull_max_cnt=100,
                verify=False,
                certfile='mycert.pem',
                keyfile='mykey.pem',
                ca_certs='blah'
            ),
            exp_attrs=dict(
                server=u'http://localhost',
                default_namespace='root/cimv3',
                name='default',
                user='fred',
                password='blah',
                timeout=50,
                verify=False,
                use_pull=True,
                pull_max_cnt=100,
                certfile='mycert.pem',
                keyfile='mykey.pem',
                ca_certs='blah',
                mock_server=[]
            )
        ),
        None, None, OK
    ),
    (
        "4. Verify mockfile",
        dict(
            init_args=[],
            init_kwargs=dict(
                mock_server='testmock.mof',
            ),
            exp_attrs=dict(
                server=None,
                default_namespace='root/cimv2',
                name='default',
                user=None,
                password=None,
                timeout=30,
                verify=None,
                use_pull=None,
                pull_max_cnt=None,
                certfile=None,
                keyfile=None,
                ca_certs=None,
                mock_server='testmock.mof'
            )
        ),
        None, None, OK
    ),
    (
        "5. Verify mockfile, list",
        dict(
            init_args=[],
            init_kwargs=dict(
                mock_server=['testmock.mof'],
            ),
            exp_attrs=dict(
                server=None,
                default_namespace='root/cimv2',
                name='default',
                user=None,
                password=None,
                timeout=30,
                verify=None,
                use_pull=None,
                pull_max_cnt=None,
                certfile=None,
                keyfile=None,
                ca_certs=None,
                mock_server=['testmock.mof']
            )
        ),
        None, None, OK
    ),
    (
        "6. Verify mockfile, list with multiple and timeout 0",
        dict(
            init_args=[],
            init_kwargs=dict(
                timeout=100,
                mock_server=['testmock.mof', 'test.py'],
            ),
            exp_attrs=dict(
                server=None,
                default_namespace='root/cimv2',
                name='default',
                user=None,
                password=None,
                timeout=100,
                verify=None,
                use_pull=None,
                pull_max_cnt=None,
                certfile=None,
                keyfile=None,
                ca_certs=None,
                mock_server=['testmock.mof', 'test.py']
            )
        ),
        None, None, OK
    ),

    # verify type errors
    (
        "E1. Verify mockfile, list with multiple and timeout 0",
        dict(
            init_args=[],
            init_kwargs=dict(
                timeout=0,
                mock_server=3,
            ),
        ),
        TypeError, None, OK
    ),

    (
        "E2. Verify server TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                server=['fred'],
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E3. Verify name TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                name=['fred'],
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E4. Verify name TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                name=1.3456,
            ),
        ),
        TypeError, None, OK
    ),

    (
        "E5. Verify default-namespace TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                default_namespace=3,
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E6. Verify name TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                name=3,
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E7. Verify user TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                user=3,
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E8. Verify password TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                password=3,
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E9. Verify timeout TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                timeout='3',
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E10. Verify verify TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                verify='3',
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E11. Verify use-pull TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                use_pull='blah',
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E12. Verify certfile TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                certfile=True,
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E13. Verify keyfile TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                keyfile=True,
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E14. Verify ca_certs TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                ca_certs=True,
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E15. Verify ca_certs TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                ca_certs=True,
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E15. Verify mock_server TypeError",
        dict(
            init_args=[],
            init_kwargs=dict(
                mock_server=True,
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E15. Verify mock_server TypeError with array",
        dict(
            init_args=[],
            init_kwargs=dict(
                mock_server=["blah.mof", 3],
            ),
        ),
        TypeError, None, OK
    ),
    (
        "E16. Verify timeout None valueError",
        dict(
            init_args=[],
            init_kwargs=dict(
                timeout=None,
            ),
            exp_attrs={},
        ),
        ValueError, None, OK
    ),

    # ValueError tests

    (
        "E17. Simultaneous server and mock server not allowed",
        dict(
            init_args=[],
            init_kwargs=dict(
                server="http://blay",
                mock_server="blah.mof"
            ),
            exp_attrs={},
        ),
        ValueError, None, OK
    ),
    (
        "E18. Verify timeout < 0 ValueError ",
        dict(
            init_args=[],
            init_kwargs=dict(
                server='http://blah',
                timeout=-3,
            ),
            exp_attrs={},
        ),
        ValueError, None, OK
    ),
    (
        "E19. Verify timeout < 0 ValueError ",
        dict(
            init_args=[],
            init_kwargs=dict(
                server='http://blah',
                timeout=99999,
            ),
            exp_attrs={},
        ),
        ValueError, None, OK
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PYSVR_INIT)
@simplified_test_function
def test_pysvr_init(testcase, init_args, init_kwargs, exp_attrs):
    """
    Test function for PywbemServer.__init__().
    """
    svr = PywbemServer(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    assert svr.server == exp_attrs['server']
    assert svr.default_namespace == exp_attrs['default_namespace']
    assert svr.user == exp_attrs['user']
    assert svr.password == exp_attrs['password']
    assert svr.timeout == exp_attrs['timeout']
    assert svr.verify == exp_attrs['verify']
    assert svr.certfile == exp_attrs['certfile']
    assert svr.keyfile == exp_attrs['keyfile']
    assert svr.ca_certs == exp_attrs['ca_certs']
    assert svr.mock_server == exp_attrs['mock_server']

    repr_str = repr(svr)
    if exp_attrs['server']:
        assert "server=" in repr_str
        assert exp_attrs['server'] in repr_str


TESTCASES_PYSVR_CONNECT_ATTRS = [
    # Testcases for PywbemServer.connect() for testing attrs
    #
    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function and response:
    #   * init_kwargs: __init__() keyword args.
    #   * exp_attrs: Dict of expected attributes of resulting object.
    #   * exp_repr: string
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Verify url arg only",
        dict(
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
        None, None, OK
    ),
    (
        "Verify with security params",
        dict(
            init_kwargs=dict(
                server='http://localhost',
                user='fred',
                password='blah',
                verify=True,
                certfile=FAKE_PEM_PATH,
                keyfile=FAKE_PEM_PATH,
            ),
            exp_attrs=dict(
                server=u'http://localhost',
                default_namespace='root/cimv2',
                user='fred',
                password='blah',
                verify=True,
                certfile=FAKE_PEM_PATH,
                keyfile=FAKE_PEM_PATH,
                ca_certs=None,
                mock_server=None
            )
        ),
        None, None, OK
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_PYSVR_CONNECT_ATTRS)
@simplified_test_function
def test_pysvr_connect_attrs(testcase, init_kwargs, exp_attrs):
    """
    Test function for PywbemServer.connect() for testing attrs.
    """
    svr = PywbemServer(**init_kwargs)

    # Create temp fake file.
    # NOTE: We cannot use fixtures because we are using simplified_test_function
    with io.open(FAKE_PEM_PATH, 'a', encoding='utf-8'):
        pass

    # connect and test connection results. Try block insures finally is
    # called.
    try:
        svr.connect(False)
    except Exception:  # pylint: disable=broad-except
        pass  # pass all exceptions
    finally:
        # remove the PEM file
        os.remove(FAKE_PEM_PATH)

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


# TODO: Add test for PywbemServer.disconnect().

# TODO: Add test for PywbemServer.get_password().
