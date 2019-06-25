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
Click Command definition for the connection command group which includes
cmds to list add, delete, show, and test server definitions in the
connection information.  This also maintains a definition of servers on
disk which is kept in sync with changes made with the add/delete subcommands.
"""
from __future__ import absolute_import

import click
import six
from pywbem import Error, DEFAULT_CA_CERT_PATHS, LOGGER_SIMPLE_NAMES, \
    LOG_DESTINATIONS, DEFAULT_LOG_DESTINATION, LOG_DETAIL_LEVELS, \
    DEFAULT_LOG_DETAIL_LEVEL

from .pywbemcli import cli
from ._common import CMD_OPTS_TXT, pick_one_from_list, format_table, \
    verify_operation
from ._common_options import add_options, verify_option
from ._pywbem_server import PywbemServer
from .config import DEFAULT_NAMESPACE, DEFAULT_CONNECTION_TIMEOUT
from ._connection_repository import ConnectionRepository
from .config import MAX_TIMEOUT
from ._context_obj import ContextObj


@cli.group('connection', options_metavar=CMD_OPTS_TXT)
def connection_group():
    """
    Command group to manage WBEM connections.

    These command allow viewing and setting persistent connection definitions.
    The connections are normally defined in the file pywbemcliconnections.json
    in the current directory.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    command. These are NOT retained after the command is executed.
    """
    pass


@connection_group.command('export', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_export(context):
    """
    Export  the current connection information.

    Creates an export statement for each connection variable and outputs
    the statement to the conole.

    """
    context.execute_cmd(lambda: cmd_connection_export(context))


@connection_group.command('show', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False,)
@click.pass_obj
def connection_show(context, name):
    """
    Show current or NAME connection information.

    This subcommand displays  all the variables that make up the current
    WBEM connection if the optional NAME argument is NOT provided. If NAME not
    supplied, a list of connections from the connections definition file
    is presented with a prompt for the user to select a NAME.

    The information on the     connection named is displayed if that name is in
    the persistent repository.
    """
    context.execute_cmd(lambda: cmd_connection_show(context, name))


@connection_group.command('delete', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False,)
@add_options(verify_option)
@click.pass_obj
def connection_delete(context, name, **options):
    """
    Delete connection information.

    Delete connection information from the persistent store
    for the connection defined by NAME. The NAME argument is optional.

    If NAME not supplied, a select list presents the list of connection
    definitions for selection.

    Example:
      connection delete blah
    """
    context.execute_cmd(lambda: cmd_connection_delete(context, name, options))


@connection_group.command('select', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False,)
@click.pass_obj
def connection_select(context, name):
    """
    Select a connection from defined connections.

    Selects a connection from the persistently stored set of named connections
    if NAME exists in the store. The NAME argument is optional.  If NAME not
    supplied, a list of connections from the connections definition file
    is presented with a prompt for the user to select a NAME.

    Select state is not persistent.

    Examples:

       connection select <name>    # select the defined <name>

       connection select           # presents select list to pick connection
    """

    context.execute_cmd(lambda: cmd_connection_select(context, name))


# TODO Maybe most of these options can be generalized for here and cli

# pylint: disable=bad-continuation
@connection_group.command('add', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True,)
@click.argument('uri', type=str, metavar='uri', required=True)
@click.option('-d', '--default_namespace', type=str,
              default=DEFAULT_NAMESPACE,
              help="Default Namespace to use in the target WBEMServer if no "
                   "namespace is defined in the subcommand"
                   " (Default: {of}).".format(of=DEFAULT_NAMESPACE))
@click.option('-u', '--user', type=str,
              help="User name for the WBEM Server connection. ")
@click.option('-p', '--password', type=str,
              envvar=PywbemServer.password_envvar,
              help="Password for the WBEM Server. Will be requested as part "
                   " of initialization if user name exists and it is not "
                   " provided by this option.")
@click.option('-t', '--timeout', type=click.IntRange(0, MAX_TIMEOUT),
              help="Operation timeout for the WBEM Server in seconds. "
                   "Default: " + "%s" % DEFAULT_CONNECTION_TIMEOUT)
@click.option('-n', '--noverify', is_flag=True,
              help='If set, client does not verify server certificate.')
@click.option('-c', '--certfile', type=str,
              help="Server certfile. Ignored if noverify flag set. ")
@click.option('-k', '--keyfile', type=str,
              help="Client private key file. ")
@click.option('-l', '--log', type=str, metavar='COMP=DEST:DETAIL,...',
              help='Enable logging of CIM Operations and set a component '
                   'to destination, and detail level\n'
                   '(COMP: [{c}], Default: {cd}) '
                   'DEST: [{d}], Default: {dd}) '
                   'DETAIL:[{dl}], Default: {dll})'
                   .format(c='|'.join(LOGGER_SIMPLE_NAMES),
                           cd='all',
                           d='|'.join(LOG_DESTINATIONS),
                           dd=DEFAULT_LOG_DESTINATION,
                           dl='|'.join(LOG_DETAIL_LEVELS),
                           dll=DEFAULT_LOG_DETAIL_LEVEL))
@click.option('-m', '--mock-server', type=str, multiple=True,
              metavar="FILENAME",
              help='If this option is defined, a mock WBEM server is '
                   'constructed as the target WBEM server and the option value '
                   'defines a MOF or Python file to be used to populate the '
                   'mock repository. This option may be used multiple times '
                   'where each use defines a single file or file_path.'
                   'See the pywbemcli documentation for more information.')
@click.option('--ca_certs', type=str,
              help='File or directory containing certificates that will be '
                   'matched against a certificate received from the WBEM '
                   'server. Set the --no-verify-cert option to bypass '
                   'client verification of the WBEM server certificate. '
                   'Default: Searches for matching certificates in the '
                   'following system directories:'
                   ' ' + ("\n".join("%s" % p for p in DEFAULT_CA_CERT_PATHS)))
@add_options(verify_option)
@click.pass_obj
def connection_add(context, name, uri, **options):
    """
    Create a new named WBEM connection.

    This subcommand creates and saves a named connection from the
    input arguments (NAME and URI) and options in the connections file.

    The new connection can be referenced by the name argument in
    the future.  This connection object is capable of managing all of the
    properties defined for WBEMConnections.

    The NAME and URI arguments MUST exist. They define the server uri
    and the unique name under which this server connection information
    will be stored. All other properties are optional.

    Adding a connection does not the new connection as the current connection.
    Use `connection select` to set a particular stored connection definition
    as the current connection.

    A new connection can also be defined by supplying the parameters on the
    command line and using the `connection set` command to put it into the
    connection repository.
    """
    context.execute_cmd(lambda: cmd_connection_add(context, name, uri,
                                                   options))


@connection_group.command('test', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_test(context):
    """
    Execute a predefined wbem request.

    This executes a predefined request against the currente WBEM server to
    confirm that the connection exists and is working.

    It executes getclass on CIM_ManagedElement as the test.
    """
    context.execute_cmd(lambda: cmd_connection_test(context))


@connection_group.command('save', options_metavar=CMD_OPTS_TXT)
@add_options(verify_option)
@click.pass_obj
def connection_save(context, **options):
    """
    Save current connection to repository.

    Saves the current connection to the connections file if
    it does not already exist in that file.

    This is useful when you have defined a connection on the command line and
    want to set it into the connections file.
    """
    context.execute_cmd(lambda: cmd_connection_save(context, options))


@connection_group.command('list', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_list(context):
    """
    List the entries in the connection file.

    This subcommand displays all entries in the connection file as
    a table using the command line output_format to define the
    table format.

    An "*" after the name indicates the currently selected connection.
    """
    context.execute_cmd(lambda: cmd_connection_list(context))


################################################################
#
#   Common methods for The action functions for the connection click group
#
###############################################################


def export_statement(name, value):
    """ Export the name/value provided as:
        export name=value. We do not actually export but output the
        exprot definition.
    """
    if not isinstance(value, six.string_types):
        value = str(value)
    click.echo('export %s=%s' % (name, value))


def if_export_statement(name, value):
    """Export the statement if the value is not None"""
    if value:
        export_statement(name, value)


def show_connection_information(context, svr, separate_line=True):
    """
    Common function to display the connection information.  Note that this
    could also have been part of the context object since this is just the
    info from that object.
    """
    sep = '\n  ' if separate_line else ', '
    context.spinner.stop()

    click.echo('\nName: %s%sWBEMServer uri: %s%sDefault_namespace: %s'
               '%sUser: %s%sPassword: %s%sTimeout: %s%sNoverify: %s%s'
               'Certfile: %s%sKeyfile: %s%suse-pull-ops: %s%spull-max-cnt: %s%s'
               'mock: %s%slog: %s'
               % (svr.name, sep,
                  svr.server_url, sep,
                  svr.default_namespace, sep,
                  svr.user, sep,
                  svr.password, sep,
                  svr.timeout, sep,
                  svr.noverify, sep,
                  svr.certfile, sep,
                  svr.keyfile, sep,
                  svr.use_pull_ops, sep,
                  svr.pull_max_cnt, sep,
                  ", ".join(svr._mock_server), sep,
                  svr.log))

    if svr._mock_server and context.verbose:
        click.echo(context.conn.display_repository())

################################################################
#
#   Common methods for The action functions for the connection click group
#
###############################################################


def cmd_connection_export(context):
    """
        Save the current connection information to env variables using an
        export statement
    """
    context.spinner.stop()
    svr = context.pywbem_server
    if not svr:
        click.ClickException("No server currently defined as current")

    export_statement(PywbemServer.server_envvar, svr.server_url)

    if_export_statement(PywbemServer.defaultnamespace_envvar,
                        svr.default_namespace)
    if_export_statement(PywbemServer.user_envvar, svr.user)
    if_export_statement(PywbemServer.password_envvar, svr.password)
    if_export_statement(PywbemServer.timeout_envvar, svr.timeout)
    if_export_statement(PywbemServer.noverify_envvar, svr.noverify)
    if_export_statement(PywbemServer.certfile_envvar, svr.certfile)
    if_export_statement(PywbemServer.keyfile_envvar, svr.keyfile)
    if_export_statement(PywbemServer.ca_certs_envvar, svr.ca_certs)


def cmd_connection_show(context, name):
    """
    Show the parameters that make up the current connection information
    """
    pywbemcli_servers = ConnectionRepository()

    if name:
        if name in pywbemcli_servers:
            svr = pywbemcli_servers[name]
        else:
            raise click.ClickException("Name %s not in servers repository" %
                                       name)
    else:
        if context.pywbem_server:
            svr = context.pywbem_server
        else:
            raise click.ClickException("No server set as current.")

    show_connection_information(context, svr)


def cmd_connection_test(context):
    """
    Test the current connection with a single command on the default_namespace
    """
    try:
        context.conn.EnumerateClassNames()
        context.spinner.stop()
        click.echo('Connection successful')
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_connection_select(context, name):
    """
    Select an existing connection to use as the current WBEM Server. This
    command accepts the click_context since it updates that context.
    """
    pywbemcli_servers = ConnectionRepository()

    if not name:
        # get all names from dictionary
        conn_names = list(six.viewkeys(pywbemcli_servers))
        conn_names = sorted(conn_names)
        if conn_names:
            name = pick_one_from_list(context, conn_names,
                                      "Select a connection or Ctrl_C to abort.")
        else:
            raise click.ClickException(
                'Connection repository empty' % name)

    if name in pywbemcli_servers:
        pywbem_server = pywbemcli_servers[name]
        new_ctx = ContextObj(pywbem_server,
                             context.output_format,
                             pywbem_server.use_pull_ops,
                             pywbem_server.pull_max_cnt,
                             context.timestats,
                             context.log,
                             context.verbose)
        ctx = click.get_current_context()
        ctx.obj = new_ctx
        # update all contexts with new ContextObj
        parent_ctx = ctx.parent
        while parent_ctx is not None:
            parent_ctx.obj = ctx.obj
            parent_ctx = parent_ctx.parent
    else:
        raise click.ClickException(
            '%s not a defined connection name' % name)


def cmd_connection_delete(context, name, options):
    """
    Delete a connection definition from the set of connections defined.

    This may be either defined by the optional name parameter or if there
    is no name provided, a select list will be presented for the user
    to select the connection to be deleted.
    # TODO make select if name not provided
    """
    pywbemcli_servers = ConnectionRepository()

    if not name:
        # get all names from dictionary
        conn_names = list(six.viewkeys(pywbemcli_servers))
        conn_names = sorted(conn_names)
        if not conn_names:
            raise click.ClickException(
                'No names defined in connection file' % name)

        context.spinner.stop()
        name = pick_one_from_list(context, conn_names,
                                  "Select a connection or CTRL_C to abort.")

    # name defined. Test if in servers.
    if name in pywbemcli_servers:
        # TODO test for same as current connection. Error if it is
        if pywbemcli_servers[name] == context.pywbem_server:
            click.echo('Deleting current connection %s' % name)
        context.spinner.stop()
        if options['verify']:
            click.echo(show_connection_information(context,
                                                   pywbemcli_servers[name],
                                                   separate_line=False))
            if not verify_operation("Execute dete operation", msg=True):
                return
        pywbemcli_servers.delete(name)
    else:
        raise click.ClickException('%s not a defined connection name' % name)


# pylint: disable=unused-argument
def cmd_connection_add(context, name, uri, options):
    """
    Create a new connection object from the input arguments and options and
    put it into the PYWBEMCLI_SERVERS dictionary.
    """
    pywbemcli_servers = ConnectionRepository()
    if name in pywbemcli_servers:
        raise click.ClickException('%s is already defined as a server' % name)

    new_server = PywbemServer(uri, options['default_namespace'], name,
                              user=options['user'],
                              password=options['password'],
                              timeout=options['timeout'],
                              noverify=options['noverify'],
                              certfile=options['certfile'],
                              keyfile=options['keyfile'],
                              ca_certs=options['ca_certs'],
                              mock_server=options['mock_server'],
                              log=options['log'])

    context.spinner.stop()
    if options['verify']:
        click.echo(show_connection_information(context, new_server,
                                               separate_line=False))
        if not verify_operation("Execute add operation", msg=True):
            return

    pywbemcli_servers.add(name, new_server)


def cmd_connection_save(context, options):
    """
    Sets the current connection into the persistent connection repository
    """
    current_svr = context.pywbem_server
    pywbemcli_servers = ConnectionRepository()
    if current_svr.name in pywbemcli_servers:
        raise click.ClickException('%s is already defined as a server' %
                                   current_svr.name)
    context.spinner.stop()
    if options['verify']:
        click.echo(show_connection_information(context, current_svr,
                                               separate_line=False))
        if not verify_operation("Execute add operation", msg=True):
            return

    pywbemcli_servers.add(current_svr.name, current_svr)


def cmd_connection_list(context):
    """
    Dump all of the current servers in the persistent repository line
    by line.  This method displays the information as a table independent
    of the value of the cmd line output_format general option.
    """
    pywbemcli_servers = ConnectionRepository()

    # build the table structure
    headers = ['name', 'server uri', 'namespace', 'user', 'password',
               'timeout', 'noverify', 'certfile', 'keyfile', 'log']
    rows = []

    if context.pywbem_server:
        current_server_name = context.pywbem_server.name
    else:
        current_server_name = None
    for name, svr in pywbemcli_servers.items():
        # if there is a current server, and it is this item in list
        # append * to name
        if context.pywbem_server:
            if name == current_server_name:
                name = name + "*"
        row = [name, svr.server_url, svr.default_namespace, svr.user,
               svr.password, svr.timeout, svr.noverify, svr.certfile,
               svr.keyfile, svr.log]
        rows.append(row)

    context.spinner.stop()
    click.echo(format_table(sorted(rows), headers,
                            title='WBEMServer Connections:',
                            table_format=context.output_format))
