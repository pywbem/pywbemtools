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


from __future__ import absolute_import, unicode_literals

import re
import click
from collections import OrderedDict

from pywbem import WBEMServer, configure_loggers_from_string

from .config import DEFAULT_URL_SCHEME, DEFAULT_CONNECTION_TIMEOUT, \
    DEFAULT_MAXPULLCNT, DEFAULT_NAMESPACE, MAX_TIMEOUT
from ._pywbemcli_operations import PYWBEMCLIConnection, PYWBEMCLIFakedConnection

WBEM_SERVER_OBJ = None

PYWBEMCLI_LOG = 'pywbemcli.log'


def _validate_server(server):
    """
    Validate  and possibly complete the wbemserver url provided.

      Parameters:

        server: (string):
          url of the WBEMServer to which connection is being made including
          scheme, hostname/IPAddress, and optional port
      Returns:
        The input url or url extended to use DEFAULT_SCHEME as the
        scheme if not is provided

      Exceptions:
        click.CLICKException if scheme invalid

    """
    if server[0] == '/':
        url = server

    elif re.match(r"^https{0,1}://", server) is not None:
        url = server

    elif re.match(r"^[a-zA-Z0-9]+://", server) is not None:
        raise click.ClickException('Invalid scheme on server argument. %s'
                                   ' Use "http" or "https"' % server)
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
    no_verify_envvar = 'PYWBEMCLI_NO_VERIFY'
    ca_certs_envvar = 'PYWBEMCLI_CA_CERTS'
    timestats_envvar = 'PYWBEMCLI_TIMESTATS'
    use_pull_envvar = 'PYWBEMCLI_USE_PULL'
    pull_max_cnt_envvar = 'PYWBEMCLI_PULL_MAX_CNT'
    mock_server_envvar = 'PYWBEMCLI_MOCK_SERVER'
    log_envvar = 'PYWBEMCLI_LOG'

    def __init__(self, server=None, default_namespace=DEFAULT_NAMESPACE,
                 name='default',
                 user=None, password=None, timeout=DEFAULT_CONNECTION_TIMEOUT,
                 no_verify=True, certfile=None, keyfile=None, ca_certs=None,
                 use_pull=None, pull_max_cnt=DEFAULT_MAXPULLCNT,
                 stats_enabled=False, verbose=False, mock_server=None,
                 log=None):
        """
            Create a PywbemServer object. This contains the configuration
            and operation information to create a connection to the server
            and execute cim_operations on the server.
        """

        if server and mock_server:
            raise ValueError('Simultaneous "--server" and '
                             '"--mock-server" not allowed. Server: %s, '
                             'mock_server %s' % (server, mock_server))
        self._server = server
        self._mock_server = mock_server

        self._name = name
        self._default_namespace = default_namespace
        self._user = user
        self._password = password
        self._timeout = timeout
        self._no_verify = no_verify
        self._certfile = certfile
        self._keyfile = keyfile
        self._ca_certs = ca_certs
        self._stats_enabled = stats_enabled
        self._verbose = verbose
        self._wbem_server = None
        self._validate_timeout()
        self._use_pull = use_pull
        self._pull_max_cnt = pull_max_cnt

        self._wbem_server = None
        self._verbose = verbose
        self._log = log

    def __str__(self):
        return 'PywbemServer(url=%s name=%s)' % (self.server, self.name)

    def __repr__(self):
        return 'PywbemServer(server=%s name=%s ns=%s user=%s ' \
               'password=%s timeout=%s no_verify=%s certfile=%s ' \
               'keyfile=%s ca_certs=%s use_pull=%s, pull_max_cnt=%s, ' \
               'stats_enabled=%s mock_server=%r, log=%r)' % \
               (self.server, self.name, self.default_namespace,
                self.user, self.password, self.timeout, self.no_verify,
                self.certfile, self.keyfile, self.ca_certs, self.use_pull,
                self.pull_max_cnt, self.stats_enabled, self.mock_server,
                self._log)

    @property
    def server(self):
        """
        :term:`string`: Scheme with Hostname or IP address of the WBEM Server.
        """
        return self._server

    @property
    def name(self):
        """
        :term:`string`: Defines a name for this connection object.
        """
        return self._name

    @property
    def user(self):
        """
        :term:`string`: user name on the WBEM Server.
        """
        return self._user

    @property
    def use_pull(self):
        """
        :term:`bool`: Flag to define if pull operations are to be used.
        True if pull operations are to be use. False if traditional operations
        and None if the system will decide.
        """
        return self._use_pull

    @property
    def pull_max_cnt(self):
        """
        :term:`string`: max object count for pull operations.
        """
        return self._pull_max_cnt

    @property
    def stats_enabled(self):
        """
        :term:`bool`: if set, statistics are enabled for this connection
        """
        return self._stats_enabled

    @property
    def password(self):
        """
        :term:`string`: Password for this user on this WBEM Server.
        """
        return self._password

    @property
    def default_namespace(self):
        """
        :term:`string`: Namespace to be used as default  for requests.
        """
        return self._default_namespace

    @property
    def timeout(self):
        """
        :term: `int`: Connection timeout to be used on requests in seconds
        """
        return self._timeout

    @property
    def no_verify(self):
        """
        :term: `bool`: Connection server verfication flag. If True
        server cert not verified during connection.
        """
        return self._no_verify

    @property
    def certfile(self):
        """
        :term: `string`: certtificate for server or None if parameter not
        provided on input
        """
        return self._certfile

    @property
    def keyfile(self):
        """
        :term: `string`: keyfile or None if no keyfile parameter input
        """
        return self._keyfile

    @property
    def log(self):
        """
        :term: `string`: log config or None if no log parameter input
        """
        return self._log

    @property
    def ca_certs(self):
        """
        :term: `list of strings`: List of ca_certs if provided on cmd line
        """
        return self._ca_certs

    @property
    def conn(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMConnection to be used for requests.
        """
        # This is created in wbemserver and retained there.
        return self._wbem_server.conn

    @property
    def wbem_server(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMServer instance to be used for
        requests.
        """
        return self._wbem_server

    @property
    def mock_server(self):
        """
        :term: `list of strings`: list of file paths for mock server setup.
        """
        return self._mock_server

    def _validate_timeout(self):
        """
        Validate that timeout parameter is in proper range.

        Exception: ValueError in Invalid
        """
        if not self.timeout:   # disallow None
            ValueError('Timout of None not allowed')
        if self.timeout is not None and (self.timeout < 0 or  # noqa: W504
                                         self.timeout > MAX_TIMEOUT):
            ValueError('Timeout option(%s) out of range %s to %s sec' %
                       (self.timeout, 0, MAX_TIMEOUT))

    # TODO ks Can this function can be merged into get_password below?
    def password_prompt(self, ctx):
        """
        Request password from console.
        """
        if self.user:
            ctx.spinner.stop()
            password = click.prompt(
                "Enter password (user {user})" .format(user=self.user),
                hide_input=True,
                confirmation_prompt=False, type=str, err=True)
            ctx.spinner.start()
            self._password = password
        else:
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
                            "no_verify": self.no_verify,
                            "certfile": self.certfile,
                            "keyfile": self.keyfile,
                            "ca-certs": self.ca_certs,
                            "use-pull": self.use_pull,
                            "pull-max_cnt": self.pull_max_cnt,
                            "mock-server": self.mock_server,
                            "log": self.log})

    @staticmethod
    def create(replace_underscores=False, **kwargs):
        """Create PywbemServer object from kwargs. If replace_underscore is
        True, replace any -  in names with _
        """
        if replace_underscores:
            for name, value in kwargs.items():
                if '-' in name:
                    del kwargs[name]
                    name = name.replace('-', '_')
                    kwargs[name] = value

        return PywbemServer(**kwargs)

    def create_connection(self, verbose):
        """
        Initiate a WBEB connection, via PyWBEM api. Arguments for
        the request are the parameters required by the pywbem
        WBEMConnection constructor.

        If self.mock_server is set, a mock connection is created instead
        of a genuine connection to a server.
        See the pywbem WBEMConnection class for more details on the parameters.

           Return:
                pywbem WBEMConnection object that can be used to execute
                other pywbem cim_operation requests

           Exception:
               ValueError: if server paramer is invalid or other issues with
               the input values
        """
        if self._mock_server:
            conn = PYWBEMCLIFakedConnection(
                default_namespace=self.default_namespace,
                use_pull_operations=self.use_pull,
                stats_enabled=self.stats_enabled)
            try:
                self._wbem_server = WBEMServer(conn)
                conn.build_repository(conn,
                                      self._wbem_server,
                                      self._mock_server,
                                      verbose)
            except Exception as ex:
                click.echo('Repository build exception %s.: %s' % (
                    ex.__class__.__name__, ex), err=True)
                raise click.Abort()
        else:
            if not self.server:
                raise click.ClickException('No server found. Cannot '
                                           'connect.')
            self._server = _validate_server(self._server)
            if self.keyfile is not None and self.certfile is None:
                ValueError('keyfile option requires certfile option')

            creds = (self.user, self.password) if self.user or \
                self.password else None

            # If client cert and key provided, create dictionary for
            # wbem connection certs (WBEMConnection takes dictionary for this
            # info)
            x509_dict = None
            if self.certfile is not None:
                x509_dict = {"certfile": self.certfile}
                if self.keyfile is not None:
                    x509_dict.update({'keyfile': self.keyfile})

            # Create the WBEMConnection object and the _wbem_server object

            conn = PYWBEMCLIConnection(
                self.server, creds,
                default_namespace=self.default_namespace,
                no_verification=self.no_verify,
                x509=x509_dict, ca_certs=self.ca_certs,
                timeout=self.timeout,
                use_pull_operations=self.use_pull,
                stats_enabled=self.stats_enabled)
            # Create a WBEMServer object
            self._wbem_server = WBEMServer(conn)

        if self.log:
            try:
                configure_loggers_from_string(self.log,
                                              log_filename=PYWBEMCLI_LOG,
                                              connection=conn, propagate=True)
            except ValueError as ve:
                raise click.ClickException('Logger configuration error. input: '
                                           '%s. Exception: %s' % (self.log, ve))
