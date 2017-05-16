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
Functions to persist and restore the connections table.  This works from
a pickle file that maintains defined connections. If any exist they are
loaded at startup and available through an interactive session.  Functions
are provided to create, delete, and view existing connections. A set function
allows setting the current active connection into the repository.
"""
from __future__ import absolute_import

import os
import pickle
import copy

CONNECTIONS_FILE = 'pywbemcliservers.p'
CONNECTIONS_LOADED = False
PYWBEMCLI_SERVERS = {}

# TODO make this into a class to clean up the code. This is a temp hack


def get_pywbemcli_servers():
    """Load the connections pickle file"""
    global CONNECTIONS_FILE  # pylint: disable=global-variable-not-assigned
    global CONNECTIONS_LOADED  # pylint: disable=global-statement
    global PYWBEMCLI_SERVERS  # pylint: disable=global-statement
    if CONNECTIONS_LOADED:
        return PYWBEMCLI_SERVERS
    CONNECTIONS_LOADED = True
    if os.path.isfile(CONNECTIONS_FILE):
        with open(CONNECTIONS_FILE, 'rb') as fh:
            PYWBEMCLI_SERVERS = pickle.load(fh)
    return PYWBEMCLI_SERVERS


def server_definitions_create_new(name, svr_definition):
    """Add a new connection to the repository and save it"""
    pywbemcli_servers = get_pywbemcli_servers()
    pywbemcli_servers[name] = svr_definition
    global CONNECTIONS_LOADED
    CONNECTIONS_LOADED = True
    server_definitions_file_save(pywbemcli_servers)


def server_definitions_delete(name):
    """Add a new connection to the repository and save it"""
    pywbemcli_servers = get_pywbemcli_servers()
    del pywbemcli_servers[name]
    server_definitions_file_save(pywbemcli_servers)


def server_definitions_file_save(pywbemcli_servers):
    """Dump the connections pickle file if one has been loaded.
    If the dictionary is empty, it attempts to delete the file.
    This is a temporary solution to persisting connection information.
    """

    if CONNECTIONS_LOADED:
        if len(pywbemcli_servers) != 0:
            if os.path.isfile(CONNECTIONS_FILE):
                os.remove(CONNECTIONS_FILE)
            # clear the wbem_server attribute
            dict_copy = copy.deepcopy(pywbemcli_servers)
            for name, svr in dict_copy.iteritems():
                # TODO we are accessing protected member here
                svr._wbem_server = None
            with open(CONNECTIONS_FILE, "wb") as fh:
                pickle.dump(dict_copy, fh)
