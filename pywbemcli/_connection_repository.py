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
import json

CONNECTIONS_FILE = 'pywbemcliservers.p'
CONNECTIONS_LOADED = False
PYWBEMCLI_SERVERS = {}

# TODO make this into a class to clean up the code.


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


def server_definitions_file_save():
    """Dump the connections pickle file if one has been loaded.
    If the dictionary is empty, it attempts to delete the file.
    """
    if CONNECTIONS_LOADED:
        if len(PYWBEMCLI_SERVERS) == 0:
            if os.path.isfile(CONNECTIONS_FILE):
                os.remove(CONNECTIONS_FILE)
        else:
            with open(CONNECTIONS_FILE, "wb") as fh:
                pickle.dump(PYWBEMCLI_SERVERS, fh)


class DictPersistJSON(dict):
    """
    A persistent dictionary that writes to a python file
    """
    # pylint: disable=super-init-not-called
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        self._load()
        self.update(*args, **kwargs)

    def _load(self):
        """
        Load the file if it is found.
        """
        if os.path.isfile(self.filename) and os.path.getsize(self.filename) > 0:
            with open(self.filename, 'r') as fh:
                self.update(json.load(fh))

    def _dump(self):
        """
        Dump the current dictionary to filename as JSON data
        """
        with open(self.filename, 'w') as fh:
            json.dump(self, fh)

    def __getitem__(self, key):
        """
        Get a single item from the dictionary based on the key provided.
        """
        return dict.__getitem__(self, key)

    def __setitem__(self, key, val):
        """
            Set the value defined into the key entry in the dictionary
            and save the dictionary
        """
        dict.__setitem__(self, key, val)
        self._dump()

    def __repr__(self):
        """ repr function for the dictionary object"""
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)

    def update(self, *args, **kwargs):
        """
        General update for the dictionary.
        """
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
        self._dump()


class Connections(object):
    """
    This is a singleton object that creates an instance the first time the
    constructor is called by attempting to read from a file.
    """

    def __init__(self):
        """ If not already loaded, load the pickle file"""
        self.loaded = False
        self.connections_file = 'pywbemcliservers.p'
        self.pywbem_servers = self.load()

    def save(self):
        """Save any existing pickle file"""
        if self.loaded:
            pickle.dump(self.pywbem_servers, open(self.connections_file, "wb"))

    def load(self):
        """
        Install any current connection file. If
        """
        if self.loaded is False:
            if os.path.isfile(self.connections_file):
                self.loaded = True
                self.pywbem_servers = \
                    pickle.load(open(self.connections_file, 'rb'))
            else:
                return {}

    def keys(self):
        """TODO"""
        pass

    def value(self, key):
        """TODO"""
        pass
