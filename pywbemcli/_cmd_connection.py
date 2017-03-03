# Copyright  2017 IBM Corp. and Inova Development Inc.
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
from .pywbemcli import cli, CMD_OPTS_TXT


@cli.group('connection', options_metavar=CMD_OPTS_TXT)
def connection_group():
    """
    Command group to manage WBEM connections.
    This should include subcommands for:
        - save - save the current connection definition to env variables
    """
    pass


@connection_group.command('save', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def connection_save(context):
    """
    get and display a single class from the WBEM Server
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
    Show the parameters that make up the current connection information
    """
    click.echo('NOT IMPLEMENTED. This will set the parameters.')
    show_connection_information(context)
