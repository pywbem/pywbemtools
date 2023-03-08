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
Tests for _context_obj.py module
"""

from __future__ import absolute_import, print_function

from pywbemtools.pywbemcli._context_obj import ContextObj
from pywbemtools.pywbemcli._pywbem_server import PywbemServer

# pylint: disable=use-dict-literal


def test_ContextObj_init():
    """
    Test creation of ContextObj object.
    """

    server = 'http://localhost'
    ns = 'root/cimv2'
    user = 'Fred'
    pw = 'blah'
    svr = PywbemServer(server, ns, user=user, password=pw)

    output_format = 'mof'
    timestats = False
    log = 'all'
    verbose = True
    pdb = False
    warn = False
    connections_repo = None
    interactive_mode = True
    close_interactive_server = True

    ctxobj = ContextObj(
        pywbem_server=svr,
        output_format=output_format,
        timestats=timestats,
        log=log,
        verbose=verbose,
        pdb=pdb,
        warn=warn,
        connections_repo=connections_repo,
        interactive_mode=interactive_mode,
        close_interactive_server=close_interactive_server)

    assert ctxobj.pywbem_server == svr
    assert ctxobj.interactive_mode is True
