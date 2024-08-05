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
Tests for _context_obj.py module
"""


from pywbemtools.pywbemlistener._context_obj import ContextObj


def test_lis_ContextObj_init():
    """
    Test creation of ContextObj object.
    """

    output_format = 'table'
    logdir = 'log'
    verbose = True
    pdb = False
    warn = False

    ctx_obj = ContextObj(
        output_format=output_format,
        logdir=logdir,
        verbose=verbose,
        pdb=pdb,
        warn=warn)

    assert ctx_obj.output_format == output_format
    assert ctx_obj.logdir == logdir
    assert ctx_obj.verbose == verbose
    assert ctx_obj.pdb == pdb
    assert ctx_obj.warn == warn
