# (C) Copyright 2020 IBM Corp.
# (C) Copyright 2020 Inova Development Inc.
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
Click Command definition for the 'namespace' command group which includes
commands for create, delete, list, etc. of the CIM namespaces on a WBEM server.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import click

from pywbem import Error
from .pywbemcli import cli
from ._common import CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT, \
    DEFAULT_TABLE_FORMAT, output_format_is_table, format_table, display_text, \
    raise_pywbem_error_exception, validate_output_format
from ._common_options import add_options, help_option
from ._click_extensions import PywbemcliGroup, PywbemcliCommand


##########################################################################
#
#   Click command group and command definitions
#   These decorated functions implement the commands, arguments, and
#   options for the top-level 'namespace' command group
#
###########################################################################

@cli.group('namespace', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def namespace_group():
    """
    Command group for CIM namespaces.

    This command group defines commands to create, delete and list namespaces
    in a WBEM server.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'namespace' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@namespace_group.command('list', cls=PywbemcliCommand,
                         options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def namespace_list(context):
    """
    List the namespaces of the server.

    The Interop namespace must exist on the server.

    Examples:

      pywbemcli -n myconn namespace list
    """
    context.execute_cmd(lambda: cmd_namespace_list(context))


@namespace_group.command('create', cls=PywbemcliCommand,
                         options_metavar=CMD_OPTS_TXT)
@click.argument('namespace', type=str, metavar='NAMESPACE', required=True,)
@add_options(help_option)
@click.pass_obj
def namespace_create(context, namespace):
    """
    Create a namespace on the server.

    Leading and trailing slash (``/``) characters specified in the NAMESPACE
    argument will be stripped.

    The namespace must not yet exist on the server.

    The Interop namespace must exist on the server and cannot be created using
    this command, because that namespace is required to implement client
    requests to manage namespaces.

    WBEM servers may not allow this operation or may severely limit the
    conditions under which a namespace can be created on the server.

    Example:

      pywbemcli -n myconn namespace create root/cimv2
    """
    context.execute_cmd(lambda: cmd_namespace_create(context, namespace))


@namespace_group.command('delete', cls=PywbemcliCommand,
                         options_metavar=CMD_OPTS_TXT)
@click.argument('namespace', type=str, metavar='NAMESPACE', required=True,)
@add_options(help_option)
@click.pass_obj
def namespace_delete(context, namespace):
    """
    Delete a namespace from the server.

    Leading and trailing slash (``/``) characters specified in the NAMESPACE
    argument will be stripped.

    The namespace must exist and must be empty. That is, it must not contain
    any objects (qualifiers, classes or instances).

    The Interop namespace must exist on the server and cannot be deleted using
    this command.

    WBEM servers may not allow this operation or may severely limit the
    conditions under which a namespace can be deleted.

    Example:

      pywbemcli -n myconn namespace delete root/cimv2
    """
    context.execute_cmd(lambda: cmd_namespace_delete(context, namespace))


@namespace_group.command('interop', cls=PywbemcliCommand,
                         options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def namespace_interop(context):
    """
    Get the Interop namespace of the server.

    The Interop namespace must exist on the server.
    """
    context.execute_cmd(lambda: cmd_namespace_interop(context))


#####################################################################
#
#  Command functions for each of the commands in the class group
#
#####################################################################


def cmd_namespace_list(context):
    """
    List the namespaces on the WBEM server.
    """
    output_format = validate_output_format(
        context.output_format,
        ['TABLE', 'TEXT'], default_format=DEFAULT_TABLE_FORMAT)
    try:
        namespaces = context.wbem_server.namespaces
        namespaces.sort()
        context.spinner_stop()
        if output_format_is_table(output_format):
            # create list for each row
            rows = [[ns] for ns in namespaces]
            click.echo(format_table(rows, ['Namespace Name'],
                                    table_format=output_format))
        else:
            display_text("\n".join(namespaces))
    except Error as er:
        raise click.ClickException('{}: {}'.format(er.__class__.__name__, er))


def cmd_namespace_create(context, namespace):
    """
    Create a namespace on the WBEM server.
    """
    try:
        context.wbem_server.create_namespace(namespace)
        context.spinner_stop()
        click.echo('Created namespace {}'.format(namespace))
    except Error as er:
        raise_pywbem_error_exception(er)


def cmd_namespace_delete(context, namespace):
    """
    Delete a namespace on the WBEM server.
    """
    try:
        context.wbem_server.delete_namespace(namespace)
        context.spinner_stop()
        click.echo('Deleted namespace {}'.format(namespace))
    except Error as er:
        raise_pywbem_error_exception(er)


def cmd_namespace_interop(context):
    """
    Display the Interop namespace on the WBEM server.
    """
    output_format = validate_output_format(context.output_format, 'TEXT')
    try:
        interop_ns = context.wbem_server.interop_ns
        context.spinner_stop()
        display_text(interop_ns, output_format)
    except Error as er:
        raise_pywbem_error_exception(er)
