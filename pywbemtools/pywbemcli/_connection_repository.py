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

from __future__ import absolute_import, print_function

import os
import yaml
import six

from ._pywbem_server import PywbemServer

if six.PY2:
    import codecs  # pylint: disable=wrong-import-order


DEFAULT_CONNECTIONS_FILE = 'pywbemcli_connection_definitions.yaml'

DEFAULT_CONNECTIONS_PATH = os.path.join(os.getcwd(), DEFAULT_CONNECTIONS_FILE)


class ConnectionRepository(object):
    # pylint: disable=useless-object-inheritance
    """
    Manage the set of connections defined.  The data for the predefined
    connection exists on disk between pywbemcli sessions and within an
    instance of ConnectionRepository while pywbemcli is running.
    """
    # class variables
    _pywbemcli_servers = {}
    _loaded = False
    _connections_file = None
    connections_group_name = 'connection_definitions'
    default_connection_grp_name = 'default_connection_name'

    # default connection name Must be the name of a
    # connection in the connections file or None.
    default_connection_name = None

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
            self._read_connections_file()

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
            items.append('{}: {}'.format(key, value))
        items_str = ', '.join(items)
        return "{0.__class__.__name__}({{{1}}}, default_connection {2})]". \
            format(self, items_str, self.default_connection_name)

    def __contains__(self, key):
        return key in self._pywbemcli_servers

    def __getitem__(self, key):
        return self._pywbemcli_servers[key]

    def __delitem__(self, key):
        del self._pywbemcli_servers[key]
        self._write_file()

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

    def _read_connections_file(self):
        """
        If there is a file, read it in and install into the dictionary.

        """
        if os.path.isfile(self._connections_file):
            with self.open_file(self._connections_file, 'r') as _fp:
                try:
                    dict_ = yaml.safe_load(_fp)
                    # put all the connection definitions into a group
                    # in the connection file
                    connections_dict = dict_[
                        ConnectionRepository.connections_group_name]

                    ConnectionRepository.default_connection_name = dict_[
                        ConnectionRepository.default_connection_grp_name]
                    try:
                        for name, svr in six.iteritems(connections_dict):
                            ConnectionRepository._pywbemcli_servers[name] = \
                                PywbemServer.create(
                                    replace_underscores=True, **svr)
                            ConnectionRepository._loaded = True
                    except KeyError as ke:
                        raise KeyError("Items missing from record %s in "
                                       "connections file %s" %
                                       (ke, self._connections_file))
                except ValueError as ve:
                    raise ValueError("Invalid YAML in connections file %s. "
                                     "Exception %s" %
                                     (self._connections_file, ve))

    def add(self, name, svr_definition):
        """
        Add a new connection to the connections repository or replace an
        existing connection.  Users of this method should check before add if
        they do not want to replace an existing entry.
        """
        assert svr_definition.mock_server is not None  # must be empty list
        ConnectionRepository._pywbemcli_servers[name] = svr_definition
        self._write_file()

    def delete(self, name):  # pylint: disable=no-self-use
        """Delete a definition from the connections repository"""
        del ConnectionRepository._pywbemcli_servers[name]
        # remove default_name if it is the one being deleted
        if name == self.default_connection_name:
            self.default_connection_name = None
        self._write_file()

    @staticmethod
    def open_file(filename, file_mode='w'):
        """
        A static convenience function that performs the open of the connection
        definitions file correctly for different versions of Python.

        This covers the issue where the file should be opened in text mode but
        that is done differently in Python 2 and Python 3.

        The returned file-like object must be closed by the caller.

        Parameters:

          filename (:term:`string`):
            Name of the file where the recorder output will be written

          file_mode (:term:`string`):
            Optional file mode.  The default is 'w' which overwrites any
            existing file.  if 'a' is used, the data is appended to any
            existing file.

        Returns:

          File-like object.
        """
        if six.PY2:
            # Open with codecs to define text mode
            return codecs.open(filename, mode=file_mode, encoding='utf-8')

        return open(filename, file_mode, encoding='utf8')

    def _write_file(self):  # pylint: disable=no-self-use
        """
        Write the connections file if one has been loaded.
        If the dictionary is empty, it attempts to delete the file.

        If there is an existing file it is moved to filename.bak and a new
        current file written.
        """
        conn_dict = {}
        if self._pywbemcli_servers:
            if ConnectionRepository._pywbemcli_servers:
                conn_dict = \
                    {name: value.to_dict() for name, value in
                     ConnectionRepository._pywbemcli_servers.items()}

            # build dictionary for yaml output
            yaml_dict = {ConnectionRepository.connections_group_name: conn_dict,
                         ConnectionRepository.default_connection_grp_name:
                             self.default_connection_name}

            # Write to tmpfile and if successful create backup file and
            # move the tmpfile to be the new connections file contents.
            tmpfile = '{}.tmp'.format(self._connections_file)

            with self.open_file(tmpfile, 'w') as _fp:
                data = yaml.safe_dump(yaml_dict,
                                      encoding=None,
                                      allow_unicode=True,
                                      default_flow_style=False,
                                      indent=4)
                data = data.replace('\n\n', '\n')  # YAML dump dups newlines
                _fp.write(data)
                _fp.flush()

        # create bak file and then rename tmp file
        if os.path.isfile(self._connections_file):
            bakfile = '{}.bak'.format(self._connections_file)
            if os.path.isfile(bakfile):
                os.remove(bakfile)
            if os.path.isfile(self._connections_file):
                os.rename(self._connections_file, bakfile)

        if self._pywbemcli_servers:
            os.rename(tmpfile, self._connections_file)

    def set_default_connection(self, connection_name):
        """
        Set the connection defined by connection_name to be the current
        connection in the connections file.

        This is accomplished by modifying the "current_connection" entry
        and rewriting the file.
        """
        if connection_name in self._pywbemcli_servers:
            ConnectionRepository.default_connection_name = connection_name
            self._write_file()

        else:
            # TODO should "Default failed be part of this message"?
            raise ValueError('Connection name "{}" does not exist in '
                             'connection repository {}'
                             .format(connection_name, self.connections_file))

    def get_default_connection_name(self):
        """
        Returns the name of the current connection in the connections file.
        This may be the name of a connection in the connections file or
        None if no connection is defined as the current connection.
        """
        return self.default_connection_name
