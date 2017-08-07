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
a file that maintains defined connections. If any exist they are
loaded at startup and available through an interactive session.  Functions
are provided to create, delete, and view existing connections. A set function
allows setting the current active connection into the repository.
"""
from __future__ import absolute_import

import os
import json
import six
# import pickle
from ._pywbem_server import PywbemServer

CONNECTIONS_FILE = 'pywbemcliservers.json'
CONNECTIONS_LOADED = False

# dictionary of known wbem servers
PYWBEMCLI_SERVERS = {}

# TODO make this into a class to clean up the code. This is a temp hack


def get_pywbemcli_servers():
    """Load the connections file"""
    global CONNECTIONS_FILE  # pylint: disable=global-variable-not-assigned
    global CONNECTIONS_LOADED  # pylint: disable=global-statement
    global PYWBEMCLI_SERVERS  # pylint: disable=global-statement
    if CONNECTIONS_LOADED:
        return PYWBEMCLI_SERVERS
    CONNECTIONS_LOADED = True
    if os.path.isfile(CONNECTIONS_FILE):
        with open(CONNECTIONS_FILE, 'r') as fh:
            try:
                dict_ = json.load(fh)
                try:
                    for svr_name, svr in six.iteritems(dict_):
                        PYWBEMCLI_SERVERS[svr_name] = \
                            PywbemServer.create(**svr)
                except KeyError as ke:
                    raise KeyError("Items missing from json record %s" % ke)
            except ValueError as ve:
                raise ValueError("Invalid json file %s" % ve)
    return PYWBEMCLI_SERVERS


def server_definitions_new(name, svr_definition):
    """Add a new connection to the repository and save it"""
    pywbemcli_servers = get_pywbemcli_servers()
    pywbemcli_servers[name] = svr_definition
    global CONNECTIONS_LOADED
    CONNECTIONS_LOADED = True
    server_definitions_save(pywbemcli_servers)


def server_definitions_delete(name):
    """Add a new connection to the repository and save it"""
    pywbemcli_servers = get_pywbemcli_servers()
    del pywbemcli_servers[name]
    server_definitions_save(pywbemcli_servers)


def server_definitions_save(pywbemcli_servers):
    """Dump the connections file if one has been loaded.
    If the dictionary is empty, it attempts to delete the file.
    This is a temporary solution to persisting connection information.
    """
    if CONNECTIONS_LOADED:
        if pywbemcli_servers:
            if os.path.isfile(CONNECTIONS_FILE):
                os.remove(CONNECTIONS_FILE)
            dict_ = {}
            for svr_name in pywbemcli_servers:
                dict_[svr_name] = pywbemcli_servers[svr_name].to_dict()
            with open(CONNECTIONS_FILE, "w") as fh:
                json.dump(dict_, fh)
