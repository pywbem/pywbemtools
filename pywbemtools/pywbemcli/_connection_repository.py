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

# Keep the following connections file definitions in sync with help text of
# the "--connections-file" option in pywbemcli.py and generaloptions.rst, and
# with the use of the base file name in several other .rst and .py files.

# Base file name of the connections file
# The B08_* file name was used before pywbemcli 0.8.
CONNECTIONS_FILENAME = '.pywbemcli_connections.yaml'
B08_CONNECTIONS_FILENAME = 'pywbemcli_connection_definitions.yaml'

# Path name of default connections file directory.
DEFAULT_CONNECTIONS_DIR = os.path.expanduser("~")

# Path name of default connections file
# The B08_* path name was used before pywbemcli 0.8.
DEFAULT_CONNECTIONS_FILE = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                        CONNECTIONS_FILENAME)
B08_DEFAULT_CONNECTIONS_FILE = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                            B08_CONNECTIONS_FILENAME)

BAK_FILE_SUFFIX = 'bak'


class ConnectionsFileError(Exception):
    """
    Top level exception for the Connections file errors.  This is not abstact
    and generally errors can be caught by just catching this error and
    reporting the class and error message found.
    """
    def __init__(self, message):
        """
        Parameters:
          msg (:term:`string`):
            Message text for the exception.
        """
        # pylint: disable=useless-super-delegation
        super(ConnectionsFileError, self).__init__(message)


class ConnectionsFileWriteError(ConnectionsFileError):
    """
    Exception to be used for connection file write errors.

    """
    def __init__(self, connections_file_name, ioerrtext, message=None):
        """
        Parameters:
          connection_file_name (:term:`string`):
            Path of the connections file

          ioerrtext (:term:`string`): Text from io error exception.

          message (:term:`string`): Further text for the exception
        """
        assert message is None or isinstance(message, six.string_types), \
            str(type(message))

        msg = 'Cannon write connection file: "{0}" write error. {1}. {2}.'. \
            format(connections_file_name, ioerrtext, message)
        super(ConnectionsFileWriteError, self).__init__(msg)


class ConnectionsFileLoadError(ConnectionsFileError):
    """
    Exception that defines errors in loading the connection file. These
    errors are due to invalid YAML or YAML key names that are required
    but missing from the file being loaded.
    Also, physical IO errors in file load..

    """
    def __init__(self, connections_file_name, message):
        """
        Parameters:
          connection_file_name (:term:`string`):
            Path of the connections file

          message (:term:`string`): Error message.
        """
        assert message is None or isinstance(message, six.string_types), \
            str(type(message))
        msg = 'Cannot load connections file: "{0}"; {1}'.format(
            connections_file_name, message)
        super(ConnectionsFileLoadError, self).__init__(msg)


class ConnectionsFileNotFoundError(ConnectionsFileError):
    """
    Excepton when file not found.
    """
    def __init__(self, connections_file_name):
        """
        Parameters:
          connection_file_name (:term:`string`):
            Path of the connections file
        """
        super(ConnectionsFileNotFoundError, self).__init__(
            'Connections file: "{0}" does not exist'.format(
                connections_file_name))


class ConnectionRepository(object):
    # pylint: disable=useless-object-inheritance
    """
    Manage the set of connections defined.  The data for the predefined
    connection exists on disk between pywbemcli sessions and within an
    instance of ConnectionRepository while pywbemcli is running.

    ConnectionRepository._load_connections_file() is a lazy load when the data
    is neeeded  rather than when the ConnectionRepository object is created
    gets the repository from the disk so that the repository is not in memory
    until one of the access methods is executed or a write is executed.  This
    also allows creation of new connections files using the connection save
    command.
    """
    # Class variables
    # The YAML section names (YAMO keys) in the connection yaml file

    # YAML group name that contains named connection definitions.
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
        Name of connection defined in the connections file that
        is the default connection; the connection that is selected on
        pywbemcli startup if no connection name or other connection definition
        is specified.

        None, if there is no current default connection name

        Returns:
            :term:`string` containing the name of the default connection
            defined in the connections file.

        Raises:
            Exceptions from _load_connections_file
        """
        if self.file_exists():
            self._load_connections_file()
            return self._default_connection_name
        return None

    @default_connection_name.setter
    def default_connection_name(self, connection_name):
        """
        Set the connection defined by connection_name to be the current
        connection in the connections file.

        Parameters:

          connection_name (:term:`string` or None):
            The name of an existing connection in the connection file that
            will become the default or None to remove any existing
            default connection name.

        Raises:
          ValueError: if connection_name does not exist in the connection file.
        """
        self._load_connections_file()
        if connection_name is None or connection_name in \
                self._pywbemcli_servers:
            self._default_connection_name = connection_name
            self._write_connections_file()
        else:
            raise ValueError('Connection name: "{}" does not exist in '
                             'connection file: "{}:'
                             .format(connection_name, self.connections_file))

    def file_exists(self):
        """
        Test if the connection file exists.The connections file is loaded as
        part of the test.

        Returns:
            (:class:`py:bool`) True if the connections_file exists and False if
            it does not exist

        Raises:
            ConnectionLoadFileError if the file is invalid and cannot be
            loaded
        """
        try:
            self._load_connections_file()
            return True
        except ConnectionsFileNotFoundError:
            return False

    def __str__(self):
        """
        Return  a string containing connections file name and count of items in
        connections file
        """
        if self.file_exists():
            # Has loaded the file
            status = 'exists'
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
        return "{0.__class__.__name__}({{{1}}}, connections_file: {2})], " \
               "loaded={3}". format(self, items_str, self._connections_file,
                                    self._loaded)

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
        If the connections file exists, read it in and install into the
        dictionary.

        An old connections file is migrated, if needed.
        Repeated calls to this method will load the file only once.

        Raises:
          ConnectionsFileNotFoundError: Connections file not found
          ConnectionsFileLoaderror: File in invalid YAML or invalid structure
          of YAML data.
        """
        if self._loaded:
            return

        # Migrate an old connections file
        if self._connections_file == DEFAULT_CONNECTIONS_FILE and \
                not os.path.isfile(self._connections_file) and \
                os.path.isfile(B08_DEFAULT_CONNECTIONS_FILE):

            # May raise IOError:
            os.rename(B08_DEFAULT_CONNECTIONS_FILE, DEFAULT_CONNECTIONS_FILE)

            click.echo("Migrated old connections file {!r} to {!r}".
                       format(B08_DEFAULT_CONNECTIONS_FILE,
                              DEFAULT_CONNECTIONS_FILE))

        # load the existing file
        if not os.path.isfile(self._connections_file):
            raise ConnectionsFileNotFoundError(self.connections_file)

        try:
            with self._open_file(self._connections_file, 'r') as _fp:
                try:
                    dict_ = yaml.safe_load(_fp)
                except (TypeError, yaml.YAMLError) as exc:
                    raise ConnectionsFileLoadError(
                        self._connections_file,
                        'Invalid YAML. Exception: {0}'.format(exc))

                # Try building dictionary of server definitions
                try:
                    connections_dict = dict_[
                        ConnectionRepository.connections_group_name]
                except TypeError as te:
                    raise ConnectionsFileLoadError(
                        self._connections_file,
                        'Invalid or no YAML in file. Exception {0}'.format(
                            str(te)))
                except KeyError:
                    raise ConnectionsFileLoadError(
                        self._connections_file,
                        'Missing YAML key name: "{0}"'.format(
                            ConnectionRepository.connections_group_name))

                # Try getting the default_connection name
                try:
                    self._default_connection_name = dict_[
                        ConnectionRepository.default_connection_grp_name]
                except KeyError:
                    gn = ConnectionRepository.default_connection_grp_name
                    raise ConnectionsFileLoadError(
                        self._connections_file,
                        'Missing YAML key name: "{0}"'.format(gn))

                # Try to rebuild the PywbemcliServer object for each
                # server definition
                for name, svr in six.iteritems(connections_dict):
                    try:
                        self._pywbemcli_servers[name] = \
                            PywbemServer.create(
                                replace_underscores=True, **svr)
                    except KeyError as ke:
                        raise ConnectionsFileLoadError(
                            self._connections_file,
                            "Element: {} missing from server named: {}".format(
                                ke, name))
                    except TypeError as te:
                        raise ConnectionsFileLoadError(
                            self._connections_file,
                            'Invalid type of item in connection definition '
                            ': "{0}". Item: "{1}"'.format(name, te))
                    except ValueError as ve:
                        raise ConnectionsFileLoadError(
                            self._connections_file,
                            'Invalid item value in connection definition '
                            ': "{0}". Item: "{1}"'.format(name, ve))

                self._loaded = True
        except IOError as io:
            raise ConnectionsFileLoadError(
                self._connections_file,
                'load failed with IO error'
                ': "{0}". Item: "{1}"'.format(name, str(io)))

    def add(self, svr_definition):
        """
        Add a new connection to the connections repository or replace an
        existing connection.  Users of this method should check before add if
        they do not want to replace an existing entry.

        Parameter:

          svr_definition (:class:`PywbemServer`):
            An instance of PywbemServer that contains the data that will be
            added to the connections file. The server definition must contain
            a name attribute.

        Raises:
            ConnectionsFileLoadError: if the file is invalid
            ConnectionsFileWriteError: if it cannot write the modified file.
        """
        assert isinstance(svr_definition.name, six.string_types)

        # If the file exists load it. Otherwise the write will create it
        if os.path.isfile(self._connections_file):
            self._load_connections_file()

        self._pywbemcli_servers[svr_definition.name] = svr_definition
        self._write_connections_file()

    def delete(self, name):
        """
        Delete a definition from the connections repository.

        Parameters:

          name (:term:`string):
            Name of the connection to delete

        Raises:
            ConnectionsFileLoadError: if it loads the file and the file is
            invalid.
            KeyError: if name does not exist in the file
            ConnectionsFileWriteError: If the file cannot be written

        """
        self._load_connections_file()
        del self._pywbemcli_servers[name]

        # Remove default_name if it is the name being deleted
        if name == self.default_connection_name:
            self._default_connection_name = None
        self._write_connections_file()

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

    def _write_connections_file(self):  # pylint: disable=no-self-use
        """
        Write the connections file if one has been loaded.
        If the dictionary is empty, it deletes the file.

        If there is an existing file it is moved to the same name with the
        suffix .bak and a new current file written.

        Raises:
            ConnectionsFileWriteError: If the file cannot be written.
        """
        conn_dict = {}
        if self._pywbemcli_servers:
            conn_dict = {name: value.to_dict() for name, value in
                         self._pywbemcli_servers.items()}

            # build dictionary for YAML output
            yaml_dict = {ConnectionRepository.connections_group_name: conn_dict,
                         ConnectionRepository.default_connection_grp_name:
                             self.default_connection_name}

            # Write to tmpfile and if successful create backup file and
            # move the tmpfile to be the new connections file contents.
            tmpfile = '{}.tmp'.format(self._connections_file)

            try:
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
            except IOError as io:
                raise ConnectionsFileWriteError(tmpfile, str(io),
                                                message="Error writing tmpfile")

        # Create bak file and then rename tmp file
        try:
            if os.path.isfile(self._connections_file):
                bakfile = '{0}.{1}'.format(self._connections_file,
                                           BAK_FILE_SUFFIX)
                if os.path.isfile(bakfile):
                    os.remove(bakfile)
                if os.path.isfile(self._connections_file):
                    os.rename(self._connections_file, bakfile)

            if self._pywbemcli_servers:
                os.rename(tmpfile, self._connections_file)
        except OSError as ose:
            raise ConnectionsFileWriteError(
                tmpfile, str(ose),
                message="Error in rename bakfile{0} to {1}".
                format(tmpfile, self._connections_file))
