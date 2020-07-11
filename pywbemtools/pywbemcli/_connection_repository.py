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
loaded at startup and available through an interactive session.  Methods
are provided to create, delete, and view existing connections. A set method
allows setting the current active connection into the repository.
"""

from __future__ import absolute_import, print_function

import os
import yaml
import six
import yamlloader
import click

from ._pywbem_server import PywbemServer

if six.PY2:
    import codecs  # pylint: disable=wrong-import-order


# Normal definition for location of connection file
DEFAULT_CONNECTIONS_FILE = 'pywbemcli_connection_definitions.yaml'

LOCAL_CONNECTIONS_PATH = os.path.join(os.getcwd(), DEFAULT_CONNECTIONS_FILE)
HOME_CONNECTIONS_PATH = os.path.join(os.path.expanduser("~"),
                                     DEFAULT_CONNECTIONS_FILE)

BAK_FILE_SUFFIX = 'bak'


class ConnectionRepository(object):
    # pylint: disable=useless-object-inheritance
    """
    Manage the set of connections defined.  The data for the predefined
    connection exists on disk between pywbemcli sessions and within an
    instance of ConnectionRepository while pywbemcli is running.

    ConnectionRepository lazy load  gets the repository from the disk so that
    the repository is not in memory until one of the access methods is
    executed or a write is executed.  This also allows creation of new
    connections files using the connection save command.
    """
    # Class variables
    # The YAML section names in the connection yaml file
    # Name of the YAML group that contains named connection definitions.
    connections_group_name = 'connection_definitions'
    # Name of the YAML group that contains the default connection name
    default_connection_grp_name = 'default_connection_name'

    def __init__(self, connections_file):
        """
        Initialize the object instance if it has not already been initialized
        (class level variable is not None)by reading the connection file.

        The __init__ does not load the connections file. That is done for each
        method that accesses the file to read or write.

        Parameters:

          connections_file (:term:`string`):
            File path defining the location of the connections file.  This
            is optional and must define the location of an existing file.
        """

        # Dictionary of named connections if the connection file is loaded
        # where each value is an instance of the class PywbemServer
        self._pywbemcli_servers = {}

        # Flag indicating whether the connections file has been loaded
        self._loaded = False
        self._connections_file = connections_file

        # default connection name Must be the name of a
        # connection in the connections file or None.
        self._default_connection_name = None

    @property
    def connections_file(self):
        """
        Get the current connections file

        Returns:
            :term:`string` containing the file path of the connections file
        """
        return self._connections_file

    @property
    def default_connection_name(self):
        """
        Return the name of connection defined in the connections file that
        is the default connection, the connection that is selected on
        pywbemcli startup if no connection name or other connection definition
        is specified.

        If None, there is no current default connection name

        Returns:
            :term:`string` containing the name of the default connection
            defined in the connections file.
        """
        return self._default_connection_name

    def file_exists(self):
        """
        Test if the connection file exists

        Returns:
            (:class:`py:bool`) True if the connections_file exists and False if
            it does not exist
        """
        return os.path.isfile(self.connections_file)

    def __str__(self):
        """
        Return  a string containing connections file name and count of items in
        connections file
        """
        if self.file_exists():
            status = 'exists'
            self._load_connections_file()
            length = len(self)
        else:
            status = "does not exist"
            length = 0

        return('connections_file: {0} {1}. {2} servers defined.'.format(
            self.connections_file, status, length))

    def __repr__(self):
        """
        Return a string representation of the
        servers dictionary that is suitable for debugging and other key
        parameters. Always tries to load connection file before displaying.
        """
        self._load_connections_file()
        # Fails if connection file does not exist.
        items = ["{0}: {1}".format(k, v)
                 for k, v in six.iteritems(self._pywbemcli_servers)]
        items_str = ', '.join(items)
        return "{0.__class__.__name__}({{{1}}}, connections_file {2})]". \
            format(self, items_str, self._connections_file)

    def __contains__(self, key):
        """Load the repository if necessary and return True if key found"""
        self._load_connections_file()
        return key in self._pywbemcli_servers

    def __getitem__(self, key):
        self._load_connections_file()
        return self._pywbemcli_servers[key]

    def __len__(self):
        self._load_connections_file()
        return len(self._pywbemcli_servers)

    def __iter__(self):
        self._load_connections_file()
        return six.iterkeys(self._pywbemcli_servers)

    def items(self):
        """
        Return a list of the items in the server repo
        """
        self._load_connections_file()
        return list(self.__iteritems__())

    def keys(self):
        """
        Return a list of the dictionary keys.
        """
        self._load_connections_file()
        return list(self.iterkeys())

    def __iteritems__(self):  # pylint: disable=no-self-use
        """"""
        self._load_connections_file()
        return six.iteritems(self._pywbemcli_servers)

    def iterkeys(self):
        """
        Return an iterator through the dictionary keys in their original
        case, preserving the original order of items.
        """
        self._load_connections_file()
        for item in six.iterkeys(self._pywbemcli_servers):
            yield item

    def _load_connections_file(self):
        """
        If there is a file, read it in and install into the dictionary.
        This file is read only once.

        Raises:
          IOError: repository does not exist

          ValueError: Error in reading repository
        """
        if self._loaded:
            return

        if os.path.isfile(self._connections_file):
            with self._open_file(self._connections_file, 'r') as _fp:
                try:
                    dict_ = yaml.safe_load(_fp)
                    # put all the connection definitions into a group
                    # in the connection file
                    connections_dict = dict_[
                        ConnectionRepository.connections_group_name]

                    self._default_connection_name = dict_[
                        ConnectionRepository.default_connection_grp_name]
                    try:
                        for name, svr in six.iteritems(connections_dict):
                            self._pywbemcli_servers[name] = \
                                PywbemServer.create(
                                    replace_underscores=True, **svr)
                            self._loaded = True
                    except KeyError as ke:
                        raise KeyError("Items missing from record {0} in "
                                       "connections file. Exception {1}".format
                                       (ke, self._connections_file))
                    except TypeError as te:
                        raise TypeError('Invalid object type in connections '
                                        'file: "{0}"; server name: "{1}". '
                                        'Item: {2}'.
                                        format(self._connections_file, name,
                                               te))
                except ValueError as ve:
                    raise ValueError("Invalid YAML in connections file {0}. "
                                     "Exception {1}".format
                                     (self._connections_file, ve))
        # Apply IO error for non-existent file
        # TODO. IOError can also mean disk full in general
        else:
            raise IOError("Connections file {} does not exist.".
                          format(self.connections_file))

    def add(self, name, svr_definition):
        """
        Add a new connection to the connections repository or replace an
        existing connection.  Users of this method should check before add if
        they do not want to replace an existing entry.

        Parameter:

          svr_definition (:class:`ServerDefinition`):
            An instance of ServerDefinition that contains the data that will be
            added to the connections file.

        Raises:
            click.Abort if the load of the connections file returns an
            exception
        """

        # If the file does exists get it. Otherwise the write will create it
        # TODO: we process errors here differently than in read mode because
        # de use click and abort. Should we do this in common.
        # Also, why not make abort_click a common function with message.
        if os.path.isfile(self._connections_file):
            try:
                self._load_connections_file()
            # All other errors cases abort.
            except Exception as e:
                click.echo("Fatal error loading YAML file {0}. "
                           "Exception: {1}: {2}".
                           format(self.connections_file, e.__class__.__name__,
                                  e),
                           err=True)
                raise click.Abort()

        self._pywbemcli_servers[name] = svr_definition
        self._write_file()

    def delete(self, name):
        """
        Delete a definition from the connections repository.

        Parameters:

          name (:term:`string):
            Name of the connection to delete

        Raises:
            KeyError: No server definition exists in the connections file
            with this name

            ValueError: Connection file is not valid YAML

            IOError: The connections file does not exist.

        """
        self._load_connections_file()
        del self._pywbemcli_servers[name]

        # Remove default_name if it is the name being deleted
        if name == self.default_connection_name:
            self._default_connection_name = None
        self._write_file()

    @staticmethod
    def _open_file(filename, file_mode='w'):
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
        If the dictionary is empty, it deletes the file.

        If there is an existing file it is moved to filename.bak and a new
        current file written.
        """
        conn_dict = {}
        if self._pywbemcli_servers:
            if self._pywbemcli_servers:
                conn_dict = \
                    {name: value.to_dict() for name, value in
                     self._pywbemcli_servers.items()}

            # build dictionary for yaml output
            yaml_dict = {ConnectionRepository.connections_group_name: conn_dict,
                         ConnectionRepository.default_connection_grp_name:
                             self.default_connection_name}

            # Write to tmpfile and if successful create backup file and
            # move the tmpfile to be the new connections file contents.
            tmpfile = '{}.tmp'.format(self._connections_file)

            with self._open_file(tmpfile, 'w') as _fp:
                data = yaml.dump(yaml_dict,
                                 encoding=None,
                                 allow_unicode=True,
                                 default_flow_style=False,
                                 indent=4,
                                 Dumper=yamlloader.ordereddict.CSafeDumper)
                data = data.replace('\n\n', '\n')  # YAML dump dups newlines
                _fp.write(data)
                _fp.flush()

        # create bak file and then rename tmp file
        if os.path.isfile(self._connections_file):
            bakfile = '{0}.{1}'.format(self._connections_file, BAK_FILE_SUFFIX)
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

        Parameters:

          connection_name (:term:`string`):
            The name of an existing connection in the connection file.

        Raises:
          ValueError: if connection_name does not exist in the connection file.
        """
        self._load_connections_file()
        if connection_name in self._pywbemcli_servers:
            self._default_connection_name = connection_name
            self._write_file()

        else:
            raise ValueError('Connection name "{}" does not exist in '
                             'connection repository {}'
                             .format(connection_name, self.connections_file))

    def get_default_connection_name(self):
        """
        Returns the name of the current connection in the connections file.
        This may be the name of a connection in the connections file or
        None if no connection is defined as the current connection.

        Returns:
          :term:`string`: Name of the default connection if one
          exists in the file; otherwise None

        Raises:
            ValueError: Connection file is not valid YAML

            IOError: The connections file does not exist.

        """
        if self.file_exists():
            self._load_connections_file()
            return self.default_connection_name
        return None
