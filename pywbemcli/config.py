#!/usr/bin/env python
# Copyright TODO
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
Pywbemcli supports a very limited number of configuration variables that
influence certain specific behavior.

These configuration variables are read by pywbem only after its modules have
been loaded, so they can be modified by the user directly after importing
pywbem. For example:

::

    import pywbemcli
    pywbem.DEFAULT_CONNECTION_TIMEOUT = 40

Note that the pywbem source file defining these variables should not be changed
by the user. Instead, the technique shown in the example above should be used to
modify the configuration variables.

Note: Due to limitations of the documentatin tooling, the following
configuration variables are shown in the ``pywbemcli.config`` namespace.
However, they should be used from the ``pywbemcli`` namespace.
"""

# This module is meant to be safe for 'import *'.

__all__ = ['DEFAULT_CONNECTION_TIMEOUT', 'DEFAULT_OUTPUT_FORMAT',
           'DEFAULT_NAMESPACE']

#: Default value in seconds for a WBEMConnection to timeout if the value
#: is not set by an input parameter.
#: Positive integer.
DEFAULT_CONNECTION_TIMEOUT = 30

#: Specifies the default output format selected if no output format is
#: defined on the cmd line, environment variable, or a config file.

DEFAULT_OUTPUT_FORMAT = 'mof'

#: Specifies the default namespace uses if no default namespace is defined
#: on the cmd line, environment variable, or a config file.

DEFAULT_NAMESPACE = 'root/cimv2'

#: Specifies the default query language to be used for exedquery operations
#: when a query language is not specified in the request or config

DEFAULT_QUERY_LANGUAGE = 'DMTF:CQL'
