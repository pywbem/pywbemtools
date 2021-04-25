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
from contextlib import contextmanager
import yaml
import six
import yamlloader
import click

from ._pywbem_server import PywbemServer
from ._pywbemcli_operations import delete_mock_cache
from ._utils import DEFAULT_CONNECTIONS_FILE, B08_DEFAULT_CONNECTIONS_FILE

if six.PY2:
    import codecs  # pylint: disable=wrong-import-order

BAK_FILE_SUFFIX = 'bak'


class ConnectionsFileError(Exception):
    """
    Base class for connections file related exceptions. Exceptions are not
    raised using this class, but this class can be used to catch all of its
    derived exceptions.
    """
    def __init__(self, message):
        """
        Parameters:

          message (:term:`string`): Message text for the exception.
        """
        # pylint: disable=useless-super-delegation
        super(ConnectionsFileError, self).__init__(message)


class ConnectionsFileWriteError(ConnectionsFileError):
    """
    Exception indicating an error when writing the connections file.

    This includes I/O and OS errors during writing of the file or during
    renaming of temporary or backup files.
    """
    def __init__(self, connections_file, message):
        """
        Parameters:

          connections_file (:term:`string`): Path name of connections file.

          message (:term:`string`): Text describing just the error
            (without text like 'Cannot write connection file {file}').
        """
        msg = 'Cannot write connections file "{0}": {1}'. \
            format(connections_file, message)
        super(ConnectionsFileWriteError, self).__init__(msg)


class ConnectionsFileLoadError(ConnectionsFileError):
    """
    Exception indicating an error when loading the connections file.

    This includes errors due to invalid YAML format at the syntax or logical
    level, missing required properties, I/O and OS errors during loading of the
    file or during renaming of the file when migrating an old file.
    """
    def __init__(self, connections_file, message):
        """
        Parameters:

          connections_file (:term:`string`): Path name of connections file.

          message (:term:`string`): Text describing just the error
            (without text like 'Cannot load connection file {file}').
        """
        msg = 'Cannot load connections file "{0}": {1}'.format(connections_file,
                                                               message)
        super(ConnectionsFileLoadError, self).__init__(msg)


@contextmanager
def open_text_file(filename, file_mode):
    """
    Context manager that opens the specified file in text mode with UTF-8
    encoding and closes it upon exit.

    This method encapsulates a difference between Python 2 and Python 3
    when opening files in text mode with UTF-8 encoding.

    Parameters:

      filename (:term:`string`):
        Path name of the file to be opened.

      file_mode (:term:`string`):
        File mode, for example:
        - 'r' opens the file for reading.
        - 'w' opens the file for writing and truncates an existing file.
        Must be a text mode, i.e. 'b' is not permitted in the file mode.

    Returns:

      File-like object.

    Raises:
      OSError
      IOError (on Python 2, and possibly for lower level errors)
    """
    assert 'b' not in file_mode
    if six.PY2:
        # pylint: disable=consider-using-with
        fp = codecs.open(filename, mode=file_mode, encoding='utf-8')
    else:
        # pylint: disable=consider-using-with
        fp = open(filename, file_mode, encoding='utf8')
    yield fp
    fp.close()


class ConnectionRepository(object):
    # pylint: disable=useless-object-inheritance
    """
    A connection repository that contains the named connection definitions
    and provides methods to manage these connection definitions.

    The connection definitions are automatically persisted in a
    :term:`connections file`.

    This class loads the connections file in a lazy manner upon access by one
    of the methods that need it to be loaded. When modifications are made,
    the connections file is immediately written back, creating a backup file
    of the current connections file.

    Each connection definition is represented as a PywbemServer object.

    This class supports the dictionary interface for accessing the connection
    definitions, using the connection name as a key, and the PywbemServer object
    as a value. The dictionary interface supports a subset of read-only
    operations.

    The connections file is a YAML file, with a format as shown in the following
    example that defines a mock connection named 'mock1', a server connection
    named 'server1', and defines 'mock1' as the default connection. The
    properties of each connection definition are the attributes of PywbemServer
    objects:

        connection_definitions:
            mock1:
                name: mock1
                server: null
                user: null
                password: null
                default-namespace: root/cimv2
                timeout: 30
                use_pull: null
                pull_max_cnt: null
                verify: true
                certfile: null
                keyfile: null
                ca-certs: null
                mock-server:
                - tests/unit/simple_mock_model.mof
                - tests/unit/simple_mock_invokemethod_v1old.py
            server1:
                name: server1
                server: https://woot.com
                user: foo
                password: pass
                default-namespace: root/cimv2
                timeout: 30
                use_pull: null
                pull_max_cnt: null
                verify: false
                certfile: null
                keyfile: null
                ca-certs: null
                mock-server: []
        default_connection_name: mock1
    """

    # Name of YAML property in the connections file that contains the
    # named connection definitions
    connections_group_name = 'connection_definitions'

    # Name of YAML property in the connections file that contains the
    # default connection name
    default_connection_grp_name = 'default_connection_name'

    def __init__(self, connections_file, verbose=None):
        """
        Initialize the object. The connections file is not yet loaded.

        Parameters:

          connections_file (:term:`string`):
            Path name of the connections file. Must not be `None`.

          verbose (:class:`py:bool`):
            If `True` enables progress console displays.
        """

        # Dictionary of connection definitions.
        # Key: Name of the connection definition.
        # Value: PywbemServer object representing the connection definition.
        self._pywbemcli_servers = {}

        # Flag indicating whether the connections file has been loaded.
        self._loaded = False

        # Path name of the connections file.
        self._connections_file = connections_file

        # Name of the default connection definition.
        # `None`, if there is no default connection definition.
        self._default_connection_name = None
        self._verbose = verbose

    @property
    def connections_file(self):
        """
        :term:`string`: Path name of the connections file. Will not be `None`.
        """
        return self._connections_file

    @property
    def default_connection_name(self):
        """
        :term:`string`: Name of the default connection definition. If `None`,
        there is no default connection definition.

        Loads the connections file, if not yet loaded.

        The default connection is selected on pywbemcli startup if no
        connection is specified.

        Raises:
          ConnectionsFileLoadError
        """
        self._load_connections_file()
        return self._default_connection_name

    @default_connection_name.setter
    def default_connection_name(self, name):
        """
        Set the default connection definition.

        Loads the connections file, if not yet loaded, and updates it.

        Parameters:

          name (:term:`string` or `None`):
            The name of an existing connection definition to be set as the
            default connection definition.
            `None` will unset the default connection definition.

        Raises:
          ConnectionsFileLoadError
          ConnectionsFileWriteError
          KeyError: Connection definition not found
        """
        self._load_connections_file()
        if name is None or name in self._pywbemcli_servers:
            self._default_connection_name = name
            self._write_connections_file()
        else:
            raise KeyError('Connection definition {!r} not found'.
                           format(name))

    def file_exists(self):
        """
        Test if the connections file exists.

        Returns:
            :class:`py:bool`: `True` if the connections file exists and `False`
            if it does not exist.
        """
        return os.path.isfile(self._connections_file)

    def __str__(self):
        """
        Return a one-line human readable string that contains path name and
        existence status of the connections file, and count of connection
        definitions in this object.

        Loads the connections file, if not yet loaded.

        Raises:
          ConnectionsFileLoadError
        """
        exists = 'exists' if self.file_exists() else "does not exist"
        self._load_connections_file()
        count = len(self)
        return ('Connection repository with {0} connection definitions and '
                'connections file "{1}" ({2})'.
                format(count, self._connections_file, exists))

    def __repr__(self):
        """
        Return a string representation of the connections dictionary in this
        object that is suitable for debugging and other key parameters.

        Loads the connections file, if not yet loaded.

        Raises:
          ConnectionsFileLoadError
        """
        exists = 'exists' if self.file_exists() else "does not exist"
        self._load_connections_file()
        items = ["{0!r}: {1}".format(k, v)
                 for k, v in six.iteritems(self._pywbemcli_servers)]
        items_str = ', '.join(items)
        return ("{0}({{{1}}}, connections_file={2!r} ({3}), loaded={4!r})".
                format(self.__class__.__name__, items_str,
                       self._connections_file, exists, self._loaded))

    def __contains__(self, name):
        """
        Return a boolean indicating whether the specified connection definition
        exists.

        Loads the connections file, if not yet loaded.

        Parameters:

          name (:term:`string`): Name of the connection definition.

        Raises:
          ConnectionsFileLoadError
        """
        self._load_connections_file()
        return name in self._pywbemcli_servers

    def __getitem__(self, name):
        """
        Return the PywbemServer object for the specified connection definition.

        Loads the connections file, if not yet loaded.

        Parameters:

          name (:term:`string`): Name of the connection definition.

        Raises:
          ConnectionsFileLoadError
          KeyError: Connection definition not found
        """
        self._load_connections_file()
        return self._pywbemcli_servers[name]

    def __len__(self):
        """
        Return the count of connection definitions.

        Loads the connections file, if not yet loaded.

        Raises:
          ConnectionsFileLoadError
        """
        self._load_connections_file()
        return len(self._pywbemcli_servers)

    def __iter__(self):
        """
        Return an iterator through the names of the connection definitions.

        Loads the connections file, if not yet loaded.

        Raises:
          ConnectionsFileLoadError
        """
        self._load_connections_file()
        return six.iterkeys(self._pywbemcli_servers)

    def items(self):
        """
        Return a list of the connection definitions, as tuple(name, conn)
        where conn is a PywbemServer object.

        Loads the connections file, if not yet loaded.

        Raises:
          ConnectionsFileLoadError
        """
        self._load_connections_file()
        return list(self.iteritems())

    def keys(self):
        """
        Return a list of the connection names.

        Loads the connections file, if not yet loaded.

        Raises:
          ConnectionsFileLoadError
        """
        self._load_connections_file()
        return list(self.iterkeys())

    def iteritems(self):
        """
        Return an iterator through the connection definitions, as
        tuple(name, conn) where conn is a PywbemServer object.

        Loads the connections file, if not yet loaded.

        Raises:
          ConnectionsFileLoadError
        """
        self._load_connections_file()
        return six.iteritems(self._pywbemcli_servers)

    def iterkeys(self):
        """
        Return an iterator through the connection names.

        Loads the connections file, if not yet loaded.

        Raises:
          ConnectionsFileLoadError
        """
        self._load_connections_file()
        return six.iterkeys(self._pywbemcli_servers)

    def _load_connections_file(self):
        """
        Load the connections file into the connection repository, if not yet
        loaded.

        Repeated calls to this method will load the file only once.

        Old connections files are migrated if needed, and a message about that
        is issued to stdout.

        Raises:
          ConnectionsFileLoadError
        """
        if self._loaded:
            return

        # Migrate an old connections file
        if self._connections_file == DEFAULT_CONNECTIONS_FILE and \
                not os.path.isfile(self._connections_file) and \
                os.path.isfile(B08_DEFAULT_CONNECTIONS_FILE):

            try:
                os.rename(B08_DEFAULT_CONNECTIONS_FILE,
                          DEFAULT_CONNECTIONS_FILE)
            except (OSError, IOError) as exc:
                raise ConnectionsFileLoadError(
                    self._connections_file,
                    'Error migrating old connections file "{0}": {1}'.
                    format(B08_DEFAULT_CONNECTIONS_FILE, exc))

            click.echo("Migrated old connections file {0!r} to {1!r}".
                       format(B08_DEFAULT_CONNECTIONS_FILE,
                              DEFAULT_CONNECTIONS_FILE))

        # If the file does not exist, the connection repo still has the
        # initial state at this point, and it remains empty.
        if not os.path.isfile(self._connections_file):
            return

        # Load the existing file.
        try:
            with open_text_file(self._connections_file, 'r') as _fp:
                try:
                    dict_ = yaml.safe_load(_fp)
                except (TypeError, yaml.YAMLError) as exc:
                    raise ConnectionsFileLoadError(
                        self._connections_file,
                        'Invalid YAML syntax: {0}'.format(exc))

                # Try building dictionary of server definitions
                try:
                    connections_dict = \
                        dict_[ConnectionRepository.connections_group_name]
                except TypeError as te:
                    raise ConnectionsFileLoadError(
                        self._connections_file,
                        'Invalid type of YAML property {0}: {1}'.
                        format(ConnectionRepository.connections_group_name, te))
                except KeyError:
                    raise ConnectionsFileLoadError(
                        self._connections_file,
                        'Missing YAML property {0}'.
                        format(ConnectionRepository.connections_group_name))

                # Try getting the default connection name
                try:
                    self._default_connection_name = dict_[
                        ConnectionRepository.default_connection_grp_name]
                except KeyError:
                    raise ConnectionsFileLoadError(
                        self._connections_file,
                        'Missing YAML property {0}'.
                        format(
                            ConnectionRepository.default_connection_grp_name))

                # Build the PywbemServer object for each connection definition
                for name, svr in six.iteritems(connections_dict):
                    try:
                        server = PywbemServer.create(
                            replace_underscores=True,
                            connections_file=self._connections_file,
                            **svr)
                    except TypeError as te:
                        raise ConnectionsFileLoadError(
                            self._connections_file,
                            'Invalid attribute type in connection '
                            'definition "{0}": {1}'.format(name, te))
                    except ValueError as ve:
                        raise ConnectionsFileLoadError(
                            self._connections_file,
                            'Invalid attribute value in connection '
                            'definition "{0}": {1}'.format(name, ve))
                    self._pywbemcli_servers[name] = server
                self._loaded = True
                if self._verbose:
                    click.echo("Connections file loaded: {}".
                               format(self._connections_file))

        except (OSError, IOError) as exc:
            raise ConnectionsFileLoadError(
                self._connections_file,
                'Error opening the file: {0}'.format(exc))

    def add(self, svr_definition):
        """
        Add a connection definition to the connections repository.

        If the connection definition already exists, it is replaced. If that is
        undesired, the existence of the connection definition can be checked
        before calling this method.

        Loads the connections file, if not yet loaded, and updates it.

        Parameters:

          svr_definition (:class:`PywbemServer`):
            An instance of PywbemServer representing the connection definition.
            The PywbemServer object must have set its `name` attribute.

        Raises:
          ConnectionsFileLoadError
          ConnectionsFileWriteError
        """
        assert isinstance(svr_definition.name, six.string_types)

        # If the file exists load it. Otherwise the write will create it
        if os.path.isfile(self._connections_file):
            self._load_connections_file()

        self._pywbemcli_servers[svr_definition.name] = svr_definition
        self._write_connections_file()

    def delete(self, name):
        """
        Delete a connection definition from the connections repository.

        Loads the connections file, if not yet loaded, and updates it.

        Parameters:

          name (:term:`string`):
            Name of the connection definition to delete.

        Raises:
          ConnectionsFileLoadError
          ConnectionsFileWriteError
          KeyError: Connection definition not found
        """
        self._load_connections_file()

        # Delete mock cache if it exists
        delete_mock_cache(self._connections_file, name)

        # Delete connection definition
        del self._pywbemcli_servers[name]

        # Unset default connection if it is the one being deleted
        if name == self._default_connection_name:
            self._default_connection_name = None

        self._write_connections_file()

    def _write_connections_file(self):
        """
        Write the connection repository state to the connections file.

        If there is an existing connections file, it is backed up with a suffix
        of '.bak' before writing the connections file.

        Raises:
          ConnectionsFileWriteError
        """
        conn_dict = {}
        if self._pywbemcli_servers:
            conn_dict = {name: value.to_dict() for name, value in
                         self._pywbemcli_servers.items()}

            # build dictionary for YAML output
            yaml_dict = {
                ConnectionRepository.connections_group_name: conn_dict,
                ConnectionRepository.default_connection_grp_name:
                self._default_connection_name
            }

            # Write to tmpfile and if successful create backup file and
            # move the tmpfile to be the new connections file contents.
            tmpfile = '{}.tmp'.format(self._connections_file)

            try:
                with open_text_file(tmpfile, 'w') as _fp:
                    data = yaml.dump(yaml_dict,
                                     encoding=None,
                                     allow_unicode=True,
                                     default_flow_style=False,
                                     indent=4,
                                     Dumper=yamlloader.ordereddict.CSafeDumper)
                    data = data.replace('\n\n', '\n')  # YAML dump dups newlines
                    _fp.write(data)
                    # Data gets flushed to disk when closing the file upon exit
                    # from the 'with' clause.
            except (OSError, IOError) as exc:
                raise ConnectionsFileWriteError(
                    self._connections_file,
                    'Error writing temporary file "{0}": {1}'.
                    format(tmpfile, exc))

        # Create bak file and then rename tmp file
        try:
            if os.path.isfile(self._connections_file):
                bakfile = '{0}.{1}'.format(self._connections_file,
                                           BAK_FILE_SUFFIX)
                if os.path.isfile(bakfile):
                    os.remove(bakfile)
                if os.path.isfile(self._connections_file):
                    os.rename(self._connections_file, bakfile)
        except (OSError, IOError) as exc:
            raise ConnectionsFileWriteError(
                self._connections_file,
                'Error renaming connections file "{0}" to backup file "{1}": '
                '{2}'.format(tmpfile, bakfile, exc))

        try:
            if self._pywbemcli_servers:
                os.rename(tmpfile, self._connections_file)
        except (OSError, IOError) as exc:
            raise ConnectionsFileWriteError(
                self._connections_file,
                'Error renaming temporary file "{0}" to connections file '
                '"{1}": {2}'.format(tmpfile, self._connections_file, exc))
        if self._verbose:
            click.echo("Connections file saved: {}".
                       format(self._connections_file))
