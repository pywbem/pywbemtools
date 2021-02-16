# Copyright 2021 IBM Corp. All Rights Reserved.
# (C) Copyright 2021 Inova Development Inc.
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
pywbemcli mock script that calls the WBEMServerMock class in
tests/unit/testmock and creates an instance of a WBEM server using the default
dictionary definition of the server defined in the same file as the
WBEMServerMock class.  This just separates the class from the script initiator
in pywbemcli so that other dictionary definitions of the mock can be created.
"""

from __future__ import absolute_import, print_function


from tests.unit.testmock.wbemserver_mock_class import *  # noqa: F403

# TODO: Future. switch to this mock script setup
# def setup(conn, server, verbose):
#    """
#    Setup function to initiate the setup of the mock environment.
#    """
#    WbemServerMock(conn, server, interop_ns='interop', verbose=verbose)

# Execute the WBEM Server configuration build using the old mock script
# interface

# pylint: disable=undefined-variable
WbemServerMock(CONN, SERVER,  # noqa: F821, F405
               interop_ns=None,
               verbose=VERBOSE)  # noqa: F821, F405
