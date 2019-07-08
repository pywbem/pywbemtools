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
import codecs
import six
from ._pywbem_server import PywbemServer

DEFAULT_CONNECTIONS_FILE = 'pywbemcliservers.json'

DEFAULT_CONNECTIONS_PATH = os.path.join(os.getcwd(), DEFAULT_CONNECTIONS_FILE)


class ConnectionRepository(object):
    """
    Manage the set of connections defined.  The data for the predefined
    connection exists on disk between pywbemcli sessions and within an
    instance of ConnectionRepository while pywbemcli is running.
    """
    # class variables
    _pywbemcli_servers = {}
    _loaded = False
    _connections_file = None

    # class level variable so
    def __init__(self, connections_file=None):
        """
        Initialize the object instance if it has not already been initialized
        (class level variable is not None)by reading the connection file.
        """
        if not ConnectionRepository._loaded:
            if connections_file is None:
                ConnectionRepository._connections_file = \
                    DEFAULT_CONNECTIONS_PATH
            else:
                ConnectionRepository._connections_file = connections_file
            self._read_json_file()

        else:
            if connections_file is not None and \
                    connections_file != self._connections_file:
                raise ValueError("Cannot change connection file name after"
                                 "initalization original {} new {}".
                                 format(self._connections_file,
                                        connections_file))

    @property
    def connections_file(self):
        """
        Return the current connections file
        """
        return self._connections_file

    def __repr__(self):
        """
        Return a string representation of the
        servers dictionary that is suitable for debugging.

        The order of items in the result is the preserved order of
        adding or deleting items.

        The lexical case of the keys in the result is the preserved lexical
        case.
        """
        # items = [_format("{0!A}: {1!A}", key, value)
        #         for key, value in self._pywbemcli_servers.iteritems()]
        items = []
        for key, value in self._pywbemcli_servers.items():
            items.append("%s: %s" % (key, value))
        items_str = ', '.join(items)
        return "{0.__class__.__name__}({{{1}}})".format(self, items_str)

    def __contains__(self, key):
        return key in self._pywbemcli_servers

    def __getitem__(self, key):
        return self._pywbemcli_servers[key]

    def __delitem__(self, key):
        del self._pywbemcli_servers[key]
        self.save()

    def __len__(self):
        return len(ConnectionRepository._pywbemcli_servers)

    def __iter__(self):
        return six.iterkeys(ConnectionRepository._pywbemcli_servers)

    def items(self):
        """
        Return a list of the items in the server repo
        """
        return list(self.__iteritems__())

    def keys(self):
        """
        Return a copied list of the dictionary keys, in their original case.
        """
        return list(self.iterkeys())

    def __iteritems__(self):  # pylint: disable=no-self-use
        return six.iteritems(self._pywbemcli_servers)

    def iterkeys(self):
        """
        Return an iterator through the dictionary keys in their original
        case, preserving the original order of items.
        """
        for item in six.iterkeys(self._pywbemcli_servers):
            yield item

    def iteritems(self):
        """
        Return an iterator through the dictionary items, where each item is a
        tuple of its original key and its value, preserving the original order
        of items.
        """
        for item in six.iteritems(self._pywbemcli_servers):
            yield item[1]

    def _read_json_file(self):
        """
        If there is a file, read it in and install into the dictionary.

        """
        if os.path.isfile(self._connections_file):
            with open(self._connections_file, 'r') as fh:
                try:
                    dict_ = json.load(fh)
                    try:
                        for name, svr in six.iteritems(dict_):
                            ConnectionRepository._pywbemcli_servers[name] = \
                                PywbemServer.create(**svr)
                            ConnectionRepository._loaded = True
                    except KeyError as ke:
                        raise KeyError("Items missing from json record %s in "
                                       "connection file %s" %
                                       (ke, self._connections_file))
                except ValueError as ve:
                    raise ValueError("Invalid json in connection file %s. "
                                     "Exception %s" %
                                     (self._connections_file, ve))

    def add(self, name, svr_definition):
        """
        Add a new connection to the connections repository or replace an
        existing connection.  Users of this method should check before add if
        they do not want to replace an existing entry.
        """
        ConnectionRepository._pywbemcli_servers[name] = svr_definition
        self._write_file()

    def delete(self, name):  # pylint: disable=no-self-use
        """Delete a definition from the connections repository"""
        del ConnectionRepository._pywbemcli_servers[name]
        self._write_file()

    def _write_file(self):  # pylint: disable=no-self-use
        """
        Write the connections file if one has been loaded.
        If the dictionary is empty, it attempts to delete the file.

        If there is an existing file it is moved to filename.bak and a new
        current file written.
        """
        jsondata = {}
        if self._pywbemcli_servers:
            if ConnectionRepository._pywbemcli_servers:
                for name in ConnectionRepository._pywbemcli_servers:
                    jsondata[name] = \
                        ConnectionRepository._pywbemcli_servers[name].to_dict()

            # Write to tmp file and if successful create backup file and move
            # the tmpfile to be the new connections file contents.
            tmpfile = "%s.tmp" % self._connections_file
            with open(tmpfile, 'w') as fh:
                if six.PY2:
                    json.dump(jsondata, codecs.getwriter('utf-8')(fh),
                              ensure_ascii=True, indent=4, sort_keys=True)
                else:
                    json.dump(jsondata, fh, ensure_ascii=True, indent=4,
                              sort_keys=True)

        # create bak file and then rename tmp file
        if os.path.isfile(self._connections_file):
            bakfile = "%s.bak" % self._connections_file
            if os.path.isfile(bakfile):
                os.remove(bakfile)
            if os.path.isfile(self._connections_file):
                os.rename(self._connections_file, bakfile)

        if self._pywbemcli_servers:
            os.rename(tmpfile, self._connections_file)
