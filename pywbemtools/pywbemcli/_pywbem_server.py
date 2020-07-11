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
Common Functions applicable across multiple components of pywbemcli
"""

from __future__ import absolute_import, print_function, unicode_literals

import re
from collections import OrderedDict
import six
import click

import pywbem
from pywbem import WBEMServer, configure_loggers_from_string

from .config import DEFAULT_URL_SCHEME, DEFAULT_CONNECTION_TIMEOUT, \
    DEFAULT_NAMESPACE, MAX_TIMEOUT
from ._pywbemcli_operations import PYWBEMCLIConnection, PYWBEMCLIFakedConnection

WBEM_SERVER_OBJ = None

PYWBEMCLI_LOG = 'pywbemcli.log'


def _raise_typeerror(name, value, rqd_type):
    """
    Generate a TypeError for a property in pywbem_server setter that has an
    invalid type
    """
    raise TypeError('Property "{0}" value: {1} must be type: "{2}", not type: '
                    '"{3}"'.format(name, value, rqd_type, type(value)))


def _validate_server_url(server):
    """
    Validate  and possibly complete the wbemserver url provided.

    Parameters:

      server (string):
        url of the WBEMServer to which connection is being made including
        scheme, hostname/IPAddress, and optional port

    Returns:
        The input url or url extended to use DEFAULT_SCHEME as the
        scheme if not is provided

    Raises:
        click.CLICKException if scheme invalid
    """
    if server[0] == '/':
        url = server

    elif re.match(r"^https{0,1}://", server) is not None:
        url = server

    # TODO Future: We are trying to make exceptions in these support classes
    # independent of click so this should become ValueError
    elif re.match(r"^[a-zA-Z0-9]+://", server) is not None:
        raise click.ClickException('Invalid scheme on server argument. {}'
                                   ' Use "http" or "https"'.format(server))
    else:
        url = "{scheme}://{host}".format(
            scheme=DEFAULT_URL_SCHEME,
            host=DEFAULT_URL_SCHEME)

    return url


class PywbemServer(object):
    # pylint: disable=too-many-instance-attributes, useless-object-inheritance
    """
    Envelope for connections with WBEM Server incorporates both the
    pywbem WBEMConnection and pywbem WBEMServer classes.

    The constructor is separated from the connection method to allow the
    object to be contstructed early but actually create the connection and
    WBEMServer objects only when required.  This allows parameters such
    as the password to be requested only when a connection is made.

    This class also holds the variables that determine whether the connection
    will use the pull operations or traditional operations
    """
    # ISSUE: #658 - Reorganize the location for these variable names separate
    # from the PywbemServer class.
    # The following class level variables are the names for the env variables
    # where server connection information are be saved and used as alternate
    # input sources for pywbemcli arguments and options.
    server_envvar = 'PYWBEMCLI_SERVER'
    name_envvar = 'PYWBEMCLI_NAME'
    user_envvar = 'PYWBEMCLI_USER'
    password_envvar = 'PYWBEMCLI_PASSWORD'
    defaultnamespace_envvar = 'PYWBEMCLI_DEFAULT_NAMESPACE'
    timeout_envvar = 'PYWBEMCLI_TIMEOUT'
    keyfile_envvar = 'PYWBEMCLI_KEYFILE'
    certfile_envvar = 'PYWBEMCLI_CERTFILE'
    verify_envvar = 'PYWBEMCLI_VERIFY'
    ca_certs_envvar = 'PYWBEMCLI_CA_CERTS'
    timestats_envvar = 'PYWBEMCLI_TIMESTATS'
    use_pull_envvar = 'PYWBEMCLI_USE_PULL'
    pull_max_cnt_envvar = 'PYWBEMCLI_PULL_MAX_CNT'
    mock_server_envvar = 'PYWBEMCLI_MOCK_SERVER'
    log_envvar = 'PYWBEMCLI_LOG'
    # The following exports are not part of the pywbem_server container
    pdb_envvar = 'PYWBEMCLI_PDB'
    deprecation_warnings_envvar = 'PYWBEMCLI_DEPRECATION_WARNINGS'
    termwidth_envvar = 'PYWBEMCLI_TERMWIDTH'
    connections_file_envvar = 'PYWBEMCLI_CONNECTIONS_FILE'

    def __init__(self, server=None, default_namespace=DEFAULT_NAMESPACE,
                 name='default', user=None, password=None,
                 timeout=DEFAULT_CONNECTION_TIMEOUT, verify=None, use_pull=None,
                 certfile=None, keyfile=None, ca_certs=None, mock_server=None):
        """
        Create  a PywbemServer object. This contains the configuration
        and operation information to create a connection to the server
        and execute cim_operations on the server.
        """

        if server and mock_server:
            raise ValueError('Simultaneous "--server" and '
                             '"--mock-server" not allowed. Server: {}, '
                             'mock_server {}'.format(server, mock_server))
        self.server = server
        self.mock_server = mock_server
        self.name = name
        self.default_namespace = default_namespace
        self.user = user
        self.password = password
        self.timeout = timeout
        self.use_pull = use_pull
        self.verify = verify
        self.certfile = certfile
        self.keyfile = keyfile
        self.ca_certs = ca_certs

        # dynamically created in create_connection
        self._wbem_server = None
        self._conn = None

    def __str__(self):
        return 'PywbemServer(url={} name={})'.format(self.server, self.name)

    def __repr__(self):
        return 'PywbemServer(server={} name={} ns={} user={} ' \
               'password={} timeout={} use_pull={} verify={} certfile={} ' \
               'keyfile={} ca_certs={}  ' \
               'mock_server={!r} wbem_server {!r})' \
               .format(self.server, self.name, self.default_namespace,
                       self.user, self.password, self.timeout, self.use_pull,
                       self.verify, self.certfile, self.keyfile, self.ca_certs,
                       self.mock_server, self.wbem_server)

    @property
    def server(self):
        """
        :term:`string`: Scheme with Hostname or IP address of the WBEM Server.
        """
        return self._server

    @server.setter
    def server(self, server):
        """Setter method; for a description see the getter method."""

        # pylint: disable=attribute-defined-outside-init
        if server:
            self._server = _validate_server_url(server)
        else:
            self._server = server

    @property
    def mock_server(self):
        """
        list of :term:`string`: list of file paths for mock server setup.
        """
        return self._mock_server

    @mock_server.setter
    def mock_server(self, mock_server):
        """Setter method; for a description see the getter method."""
        if mock_server:
            if not isinstance(mock_server, (list, six.string_types)):
                _raise_typeerror("mock_server", mock_server, 'list, string')
            for ms in mock_server:
                if not isinstance(ms, six.string_types):
                    _raise_typeerror("mock_server item", mock_server, 'string')
        # assure this is list type in yaml output
        if mock_server is None:
            mock_server = []
        # pylint: disable=attribute-defined-outside-init
        self._mock_server = mock_server

    @property
    def name(self):
        """
        :term:`string`: Defines a name for this connection object.
        """
        return self._name

    @name.setter
    def name(self, name):
        """Setter method; for a description see the getter method."""
        if name:
            if not isinstance(name, six.string_types):
                _raise_typeerror("name", name, 'string')

        # pylint: disable=attribute-defined-outside-init
        self._name = name

    @property
    def user(self):
        """
        :term:`string`: user name on the WBEM Server.
        """
        return self._user

    @user.setter
    def user(self, user):
        """Setter method; for a description see the getter method."""

        if user and not isinstance(user, six.string_types):
            _raise_typeerror("user", user, 'string')

        # pylint: disable=attribute-defined-outside-init
        self._user = user

    @property
    def password(self):
        """
        :term:`string`: Password for this user on this WBEM Server.
        """
        return self._password

    @password.setter
    def password(self, password):
        """Setter method; for a description see the getter method."""
        if password and not isinstance(password, six.string_types):
            _raise_typeerror("password", password, 'string')
        # pylint: disable=attribute-defined-outside-init
        self._password = password

    @property
    def default_namespace(self):
        """
        :term:`string`: Namespace to be used as default  for requests.
        """
        return self._default_namespace

    @default_namespace.setter
    def default_namespace(self, default_namespace):
        """Setter method; for a description see the getter method."""
        if default_namespace and not isinstance(default_namespace,
                                                six.string_types):
            _raise_typeerror("default-namespace", default_namespace, 'string')
        # pylint: disable=attribute-defined-outside-init
        self._default_namespace = default_namespace

    @property
    def timeout(self):
        """
        :term:`int`: Connection timeout to be used on requests in seconds
        """
        if self._timeout:
            assert isinstance(self._timeout, int)
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Setter method; for a description see the getter method."""
        if timeout is None:   # disallow None
            raise ValueError('timeout option of None not allowed')
        if not isinstance(timeout, int):
            _raise_typeerror("timeout", timeout, 'integer')
        if not 0 < timeout <= MAX_TIMEOUT:
            raise ValueError('Timeout option "{0}" out of range {1} to {2} sec'
                             .format(timeout, 0, MAX_TIMEOUT))
        # pylint: disable=attribute-defined-outside-init
        self._timeout = timeout

    @property
    def use_pull(self):
        """
        :term:`string`: Connection timeout to be used on requests in seconds
        """
        return self._use_pull

    @use_pull.setter
    def use_pull(self, use_pull):
        """Setter method; for a description see the getter method."""

        if use_pull is None or isinstance(use_pull, bool):
            # pylint: disable=attribute-defined-outside-init
            self._use_pull = use_pull
        else:
            _raise_typeerror("use-pull", use_pull, 'boolean')

    @property
    def verify(self):
        """
        :class:`py:bool`: Connection server verfication flag. If True
        server cert verified during connection.
        """
        return self._verify

    @verify.setter
    def verify(self, verify):
        """Setter method; for a description see the getter method."""
        if verify and not isinstance(verify, bool):
            _raise_typeerror("verify", verify, 'boolean')
        # pylint: disable=attribute-defined-outside-init
        self._verify = verify

    @property
    def certfile(self):
        """
        :term:`string`: certificate for server or None if parameter not
        provided on input
        """
        if self._certfile:
            assert isinstance(self._certfile, six.string_types)
        return self._certfile

    @certfile.setter
    def certfile(self, certfile):
        """Setter method; for a description see the getter method."""
        if certfile and not isinstance(certfile, six.string_types):
            _raise_typeerror("certfile", certfile, 'string')
        # pylint: disable=attribute-defined-outside-init
        self._certfile = certfile

    @property
    def keyfile(self):
        """
        :term:`string`: keyfile or None if no keyfile parameter input
        """
        if self._keyfile:
            assert isinstance(self._keyfile, six.string_types)
        return self._keyfile

    @keyfile.setter
    def keyfile(self, keyfile):
        """Setter method; for a description see the getter method."""
        if keyfile and not isinstance(keyfile, six.string_types):
            _raise_typeerror("keyfile", keyfile, 'string')

        # pylint: disable=attribute-defined-outside-init
        self._keyfile = keyfile

    @property
    def ca_certs(self):
        """
        :term:`string`: String that defines certs for server validation"
        """
        if self._ca_certs:
            assert isinstance(self._ca_certs, six.string_types)
        return self._ca_certs

    @ca_certs.setter
    def ca_certs(self, ca_certs):
        """Setter method; for a description see the getter method."""
        if ca_certs and not isinstance(ca_certs, six.string_types):
            _raise_typeerror("ca_certs", ca_certs, 'string')
        # pylint: disable=attribute-defined-outside-init
        self._ca_certs = ca_certs

    @property
    def conn(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMConnection to be used for requests.
        """
        # This is created in wbemserver and retained there.
        return self.wbem_server.conn if self.wbem_server else None

    @property
    def wbem_server(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMServer instance to be used for
        requests.
        """
        return self._wbem_server

    def password_prompt(self, ctx):
        """
        Request password from console.
        """
        if self.user:
            ctx.spinner_stop()
            password = click.prompt(
                "Enter password (user {user})" .format(user=self.user),
                hide_input=True,
                confirmation_prompt=False, type=str, err=True)
            ctx.spinner_start()
            # pylint: disable=attribute-defined-outside-init
            self.password = password
        else:
            # TODO: Again we want to isolate the click excpetions in future
            raise click.ClickException("{cmd} requires user/password, but "
                                       "no password provided."
                                       .format(cmd=ctx.invoked_subcommand))

    def get_password(self, ctx):
        """
        Conditional password prompt function  Prompts for password only if
        there  is a defined user and no password.
        """
        if self.user and not self.password:
            self.password_prompt(ctx)

    def to_dict(self):
        """
        Create dictionary from instance for persisting the connection. All
        key names that include _ are modified to - so that the dictionary
        reflects the general option names.
        """

        return OrderedDict({"name": self.name,
                            "server": self.server,
                            "user": self.user,
                            "password": self.password,
                            "default-namespace": self.default_namespace,
                            "timeout": self.timeout,
                            "use_pull": self.use_pull,
                            "verify": self.verify,
                            "certfile": self.certfile,
                            "keyfile": self.keyfile,
                            "ca-certs": self.ca_certs,
                            "mock-server": self.mock_server})

    @staticmethod
    def create(replace_underscores=False, **kwargs):
        """Create PywbemServer object from kwargs. If replace_underscore is
        True, replace any -  in names with _
        """
        kwargsout = {}
        if replace_underscores:
            kwargsout = {k.replace('-', '_'): v for k, v in kwargs.items()}
        return PywbemServer(**kwargsout)

    def reset(self):
        """ Reset the connection attributes of this pywbem server so that the
        connection must be restablished
        """
        self._conn = None
        self._wbem_server = None

    def create_connection(self, log=None, use_pull=None,
                          verbose=None, timestats=None):
        """
        Initiate a WBEB connection, via PyWBEM api. Arguments for
        the request are the parameters required by the pywbem
        WBEMConnection constructor that are not available within this
        class.

        If self.mock_server is set, a mock connection is created instead
        of a genuine connection to a server.
        See the pywbem.WBEMConnection class for more details on the parameters.

        Return:
            pywbem.WBEMConnection: Connection object that can be used to execute
            other pywbem cim_operation requests

        Raises:
           ValueError: if server paramer is invalid or other issues with
           the input values
        """
        if self._mock_server:
            if self.conn is None:
                conn = PYWBEMCLIFakedConnection(
                    default_namespace=self.default_namespace,
                    use_pull_operations=use_pull,
                    stats_enabled=timestats)
                try:
                    self._wbem_server = WBEMServer(conn)
                    conn.build_repository(conn,
                                          self._wbem_server,
                                          self._mock_server,
                                          verbose)
                except click.Abort:
                    raise
                except Exception as exc:  # pylint: disable=broad-except
                    click.echo(
                        "Building the mock repository failed: {}".format(exc),
                        err=True)

        else:  # mock_server does not exist
            if not self.server:
                raise click.ClickException('No server found. Cannot '
                                           'connect.')
            if self.keyfile is not None and self.certfile is None:
                ValueError('keyfile option requires certfile option')

            creds = (self.user, self.password) if self.user or \
                self.password else None

            # If client cert and key provided, create dictionary for
            # wbem connection certs (WBEMConnection takes dictionary for this
            # info)
            x509_dict = None
            if self.certfile is not None:
                x509_dict = {"cert_file": self.certfile}
                if self.keyfile is not None:
                    x509_dict.update({'key_file': self.keyfile})

            # Create the WBEMConnection object and the _wbem_server object

            # Negate verify to no_verification
            if self.verify is None:
                no_verification = self.verify
            else:
                no_verification = not self.verify

            # Convert ca_certs command line option to ca_certs parameter
            if getattr(pywbem, 'PYWBEM_USES_REQUESTS', False):
                if self.ca_certs == 'certifi':
                    ca_certs = None
                else:
                    ca_certs = self.ca_certs
            else:
                ca_certs = self.ca_certs

            try:
                conn = PYWBEMCLIConnection(
                    self.server, creds,
                    default_namespace=self.default_namespace,
                    no_verification=no_verification,
                    x509=x509_dict, ca_certs=ca_certs,
                    timeout=self.timeout,
                    use_pull_operations=use_pull,
                    stats_enabled=timestats)
            except IOError as exc:
                raise click.ClickException(
                    'Cannot create connection to {}: {}'.
                    format(self.server, exc))

            # Create a WBEMServer object
            self._wbem_server = WBEMServer(conn)

        if log:
            try:
                configure_loggers_from_string(log,
                                              log_filename=PYWBEMCLI_LOG,
                                              connection=conn, propagate=True)
            except ValueError as ve:
                raise click.ClickException('Logger configuration error. input: '
                                           '{}. Exception: {}'.format(log, ve))
