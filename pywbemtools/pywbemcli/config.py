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

# Issue 224: Some strings are unicode because of this issue.


__all__ = ['DEFAULT_CONNECTION_TIMEOUT',
           'DEFAULT_NAMESPACE', 'PYWBEMCLI_PROMPT', 'PYWBEMCLI_HISTORY_FILE',
           'DEFAULT_MAXPULLCNT', 'MAX_TIMEOUT', 'DEFAULT_URL_SCHEME',
           'USE_TERMINAL_WIDTH', 'DEFAULT_TABLE_WIDTH']

#: Default value in seconds for a WBEMConnection to timeout if the value
#: is not set by an input parameter.
#: Positive integer.
DEFAULT_CONNECTION_TIMEOUT = 30

#: Specifies the default namespace uses if no default namespace is defined
#: on the cmd line, environment variable, or a config file.
DEFAULT_NAMESPACE = u'root/cimv2'

#: Specifies the default query language to be used for exedquery operations
#: when a query language is not specified in the request or config.
DEFAULT_QUERY_LANGUAGE = u'DMTF:CQL'

#: Characters for cmdline prompt when the pywbemcli repl is executing.
#: The prompt is presented at the beginning of a line awaiting a command
#: input.
#: The prompt MUST BE Unicode (prompt-toolkit requirement)
PYWBEMCLI_PROMPT = u'pywbemcli> '

#: File path of history file for interactive mode.
#: If the file name starts with tilde (which is handled by the shell, not by
#: the file system), it is properly expanded.
PYWBEMCLI_HISTORY_FILE = '~/.pywbemcli_history'

#: Default uri scheme if none is provided.  Thus if a server uri without
#: scheme component is provided, this is the default prepended to the
#: uri.

DEFAULT_URL_SCHEME = 'https'

#: Default pull MaxObjectCount if none is provided.  This is the maximum
#: number of objects per request that will be returned if the server
#: uses the pull operations for EnumerateInstances, AssociatorInstances,
#: etc. Set to the same default as used by pywbem.
DEFAULT_MAXPULLCNT = 1000

#: Maximum allowed connection timeout in seconds.  The environment will not
#: allow a connection timeout value larger than this on the command line or
#: internal option for timeout.
MAX_TIMEOUT = 300

#: If True, the table formatter uses the terminal width as the maximum width
#: of a table. If False it uses the DEFAULT_TABLE_WIDTH config variable. This
#: sets the maximum width of table output. The table formatter tries to
#: build any table output within this character width.
USE_TERMINAL_WIDTH = True

#: Default maximum character width of tables if USE_TERMINAL_WIDTH is NOT set.
#: If this variable is an integer, that is the maximum width. If None, tables
#: are output with no limit on width.
DEFAULT_TABLE_WIDTH = 150


#: If True, the auto-suggestion capability is enabled in the interactive
#: mode.  This capability uses the history file to provide suggestions for
#: the command file in addition to other auto-complete capabilities
#: If False, auto-suggestion is disabled.
USE_AUTOSUGGEST = True
