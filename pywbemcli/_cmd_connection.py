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
cmds to view, save, etc. connection information.
"""
from __future__ import absolute_import

import click
from pywbem import Error, DEFAULT_CA_CERT_PATHS

from .pywbemcli import cli
from ._common import CMD_OPTS_TXT, pick_from_list
from ._pywbem_server import PywbemServer
from .config import DEFAULT_NAMESPACE, DEFAULT_CONNECTION_TIMEOUT
from ._asciitable import print_ascii_table
from ._connection_repository import get_pywbemcli_servers, \
    server_definitions_file_save


@cli.group('connection', options_metavar=CMD_OPTS_TXT)
def connection_group():
    """
    Command group to manage WBEM connections.

    These command allow viewing and setting connection information.

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
@click.argument('name', type=str, metavar='name', required=False,)
@click.pass_obj
def connection_show(context, name):
    """
    Show the current connection information, i.e. all the variables that
    make up the current connection
    """
    context.execute_cmd(lambda: cmd_connection_show(context, name))


@connection_group.command('delete', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='name', required=True,)
@click.pass_obj
def connection_delete(context, name):
    """
    Show the current connection information, i.e. all the variables that
    make up the current connection
    """
    context.execute_cmd(lambda: cmd_connection_delete(context, name))


@connection_group.command('select', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='name', required=False,)
@click.pass_obj
def connection_select(context, name):
    """
    Select a connection from the current defined connections
    """

    context.execute_cmd(lambda: cmd_connection_select(context, name))


@connection_group.command('set', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='name', required=False,)
@click.pass_obj
def connection_set(context, name):
    """
    Set current connection into repository.

    Sets the current wbem connection information into the repository of
    connections. If the name does not already exist in the connection
    information, the provided name is used.
    """
    context.execute_cmd(lambda: cmd_connection_set(context, name))


# TODO Maybe most of these options can be generalized for here and cli
@connection_group.command('create', options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='name', required=True,)
@click.argument('server', type=str, envvar=PywbemServer.server_envvar,
                required=True)
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
@click.option('-t', '--timeout', type=str,
              help="Operation timeout for the WBEM Server in seconds. "
                   "Default: " + "%s" % DEFAULT_CONNECTION_TIMEOUT)
@click.option('-n', '--noverify', type=str, is_flag=True,
              help='If set, client does not verify server certificate.')
@click.option('-c', '--certfile', type=str,
              help="Server certfile. Ignored if noverify flag set. ")
@click.option('-k', '--keyfile', type=str,
              help="Client private key file. ")
@click.option('--ca_certs', type=str,
              help='File or directory containing certificates that will be '
                   'matched against a certificate received from the WBEM '
                   'server. Set the --no-verify-cert option to bypass '
                   'client verification of the WBEM server certificate. '
                   'Default: Searches for matching certificates in the '
                   'following system directories: ' +
                   ("\n".join("%s" % p for p in DEFAULT_CA_CERT_PATHS)))
@click.pass_obj
def connection_create(context, name, server, **options):
    """
    Create a new named connection from the input parameters.

    This subcommand creates and saves a new named connection from the
    input parameters.

    The name and server arguments MUST exist. They define the server uri
    and the unique name under which this server connection information
    will be stored. All other properties are optional.

    It does NOT automatically set the pywbemcli to use that connection.
    Use `connection select` to set a particular stored connection definition
    as the current connection.

    This is the alternative means of defining a new WBEM server to be accessed
    to supplying the parameters on the command line. and using the
    connection set command to put it into the connection repository.

    Defines a new connection that can be referenced by the name argument in
    the future.  This connection object is capable of managing all of the
    properties defined for WBEMConnections.
    """
    context.execute_cmd(lambda: cmd_connection_create(context, name, server,
                                                      options))


@connection_group.command('test', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_test(context):
    """
    Execute a simple wbem request to test that the connection exists
    and is working.
    """
    context.execute_cmd(lambda: cmd_connection_test(context))


@connection_group.command('list', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_list(context):
    """
    Execute a simple wbem request to test that the connection exists
    and is working.
    """
    context.execute_cmd(lambda: cmd_connection_list(context))


################################################################
#
#   The following are the action functions for the connection click group
#
###############################################################


def export_statement(name, value):
    """ Export the name/value provided as:
        export name=value
    """
    click.echo('export %s=%s' % (name, value))


def if_export_statement(name, value):
    """Export the statement if the value is not None"""
    if value:
        export_statement(name, value)


def cmd_connection_export(context):
    """
        Save the current connection information to env variables using an
        export statement
    """
    context.spinner.stop()
    svr = context.pywbem_server

    export_statement(PywbemServer.server_envvar, svr.server_uri)

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
    pywbemcli_servers = get_pywbemcli_servers()

    if name in pywbemcli_servers:
        svr = pywbemcli_servers[name]
    else:
        svr = context.pywbem_server

    show_connection_information(context, svr)


def cmd_connection_set(context, name):
    """
    Set the current connection information into the dictionary of
    servers.
    """
    svr = context.pywbem_server
    if svr.name and name:
        svr._name = name
    elif not svr.name and not name:
        raise click.ClickException('No name definition' % name)
        # TODO we can ask for name in this case in interactive mode
    elif svr.name:
        name = svr.name
    pywbemcli_servers = get_pywbemcli_servers()
    pywbemcli_servers[name] = svr
    server_definitions_file_save()

    show_connection_information(context, context.pywbem_server)


def cmd_connection_test(context):
    """
    Show the parameters that make up the current connection information
    """
    try:
        context.conn.GetClass('CIM_ManagedElement')
        context.spinner.stop()
        click.echo('Connection successful')
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def show_connection_information(context, svr, separate_line=True):
    """
    Common function to display the connection information.  Note that this
    could also have been part of the context object since this is just the
    info from that object.
    """
    sep = '\n' if separate_line else ', '
    context.spinner.stop()

    click.echo('\nWBEMServer uri: %s%sDefault_namespace: %s%sUser: %s%s'
               'Password: %s%sTimeout: %s%sNoverify: %s%s'
               'Certfile: %s%sKeyfile: %s%sName: %s'
               % (svr.server_uri, sep,
                  svr.default_namespace, sep,
                  svr.user, sep,
                  svr.password, sep,
                  svr.timeout,
                  sep, svr.noverify,
                  sep, svr.certfile, sep,
                  svr.keyfile, sep,
                  svr.name))


def cmd_connection_select(context, name):
    """
    Select and existing connection to use as the current WBEM Server
    """
    pywbemcli_servers = get_pywbemcli_servers()
    if not name:
        # get all names from dictionary
        conn_names = pywbemcli_servers.keys()
        if conn_names:
            name = pick_from_list(context, conn_names, "Select a connection")
        else:
            raise click.ClickException(
                'Connection repository empty' % name)

    else:
        if name in pywbemcli_servers:
            connection = pywbemcli_servers[name]
            context.set_connection(connection)
        else:
            raise click.ClickException(
                '%s not a defined connection name' % name)


def cmd_connection_delete(context, name):
    """
    Delete a connection definition from the set of connections defined.

    This may be either defined by the optional name parameter or if there
    is no name provided, a select list will be presented for the user
    to select the connection to be deleted.
    # TODO make select if name not provided
    """
    pywbemcli_servers = get_pywbemcli_servers()

    if name in pywbemcli_servers:
        # TODO test for same as current connection. Error if it is
        if pywbemcli_servers[name] == context.pywbem_server:
            raise click.ClickException(
                'Please do not delete current connection %s' % name)
        del pywbemcli_servers[name]
        server_definitions_file_save()
    else:
        raise click.ClickException(
            '%s not a defined connection name' % name)


def cmd_connection_create(context, name, server, options):
    """
    Create a new connection object from the input arguments and options and
    put it into the PYWBEMCLI_SERVERS dictionary.
    """
    pywbemcli_servers = get_pywbemcli_servers()
    if name in pywbemcli_servers:
        raise click.ClickException('%s is already defined as a server' % name)

    pywbem_server = PywbemServer(server, options['default_namespace'], name,
                                 user=options['user'],
                                 password=options['password'],
                                 timeout=options['timeout'],
                                 noverify=options['noverify'],
                                 certfile=options['certfile'],
                                 keyfile=options['keyfile'],
                                 ca_certs=options['ca_certs'])
    pywbemcli_servers[name] = pywbem_server

    server_definitions_file_save()


def cmd_connection_list(context):
    """
    Dump all of the current servers in the persistent repository line
    by line.  This is a raw dump
    """
    pywbemcli_servers = get_pywbemcli_servers()

    # build the table structure
    hdr = ['name', 'server uri', 'namespace', 'user', 'password',
           'timeout', 'noverify', 'certfile', 'keyfile']
    lines = []

    for name, svr in pywbemcli_servers.iteritems():
        line = [svr.name, svr.server_uri, svr.default_namespace, svr.user,
                svr.password, svr.timeout, svr.noverify, svr.certfile,
                svr.keyfile]
        lines.append(line)

    context.spinner.stop()
    print_ascii_table(lines, header=hdr, title='WBEMServer Connections',
                      inner=False, outer=False)
