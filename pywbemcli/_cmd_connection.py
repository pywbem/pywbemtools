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
Click Command definition for the class command group which includes
cmds for get, enumerate, list of classes.
"""
from __future__ import absolute_import

import click
from pywbem import Error
from .pywbemcli import cli
from ._common import CMD_OPTS_TXT


@cli.group('connection', options_metavar=CMD_OPTS_TXT)
def connection_group():
    """
    Command group to manage WBEM connections These command allow viewing
    and setting connection information.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    command. These are NOT retained after the command is executed.
    """
    pass


@connection_group.command('save', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_save(context):
    """
    Call the funciton to save the current connection information by
    exporting it
    """
    context.execute_cmd(lambda: cmd_connection_save(context))


@connection_group.command('show', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_show(context):
    """
    Show the current connection information, i.e. all the variables that
    make up the current connection
    """
    context.execute_cmd(lambda: cmd_connection_show(context))


@connection_group.command('set', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_set(context):
    """
    Show the current connection information, i.e. all the variables that
    make up the current connection
    """
    context.execute_cmd(lambda: cmd_connection_set(context))


@connection_group.command('test', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_test(context):
    """
    Execute a simple wbem request to test that the connection exists
    and is working.
    """
    context.execute_cmd(lambda: cmd_connection_test(context))


################################################################
#
#   The following are the action functions for the connection click group
#
###############################################################

def show_connection_information(context, separate_line=True):
    """
    Common function to display the connection information.  Note that this
    could also have been part of the context object since this is just the
    info from that object.
    """
    sep = '\n' if separate_line else ', '

    # pylint: disable=protected-access
    click.echo('\nWBEMServer uri: %s%sDefault_namespace: %s%sUser: %s%s'
               'Password: %s%sTimeout: %s%sNoverify: %s%s'
               'Certfile: %s%sKeyfile: %s'
               % (context.server, sep, context.default_namespace, sep,
                  context.user, sep, context.password, sep, context.timeout,
                  sep, context.noverify, sep, context._certfile, sep,
                  context._keyfile))  # pylint: disable=protected-access


def cmd_connection_save(context):
    """
        Save the current connection information to env variables
    """
    # pylint: disable=protected-access
    click.echo("export PYWBEMCLI_SERVER=%s" % context.server)
    click.echo("export PYWBEMCLI_DEFAULT_NAMESPACE=%s" %
               context.default_namespace)
    click.echo("export PYWBEMCLI_USER=%s" % context.user)
    click.echo("export PYWBEMCLI_PASSWORD=%s" % context.password)
    click.echo("export PYWBEMCLI_TIMEOUT=%s" % context.timeout)
    click.echo("export PYWBEMCLI_NOVERIFY=%s" % context.noverify)
    click.echo("export PYWBEMCLI_CERTFILE'=%s" % context._certfile)
    click.echo("export PYWBEMCLI_KEYFILE=%s" % context._keyfile)


def cmd_connection_show(context):
    """
    Show the parameters that make up the current connection information
    """
    show_connection_information(context)


def cmd_connection_set(context):
    """
    Test the current connection by executing a predefined WBEM request.
    Currently this request is a get class CIM_ManagedElement on the
    default namespace
    """
    click.echo('NOT IMPLEMENTED. This will set the parameters.')
    show_connection_information(context)


def cmd_connection_test(context):
    """
    Show the parameters that make up the current connection information
    """
    try:
        context.conn.GetClass('CIM_ManagedElement')
        click.echo('Connection successful')
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
