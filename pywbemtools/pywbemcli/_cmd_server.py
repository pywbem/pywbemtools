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
Click command definition for the server command group which includes
cmds for inspection and management of the objects defined by the pywbem
server class including namespaces, WBEMServer information, and profile
information.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import click

from pywbem import Error

from .pywbemcli import cli
from ._common import format_table, raise_pywbem_error_exception, \
    validate_output_format, display_text, output_format_is_table, \
    CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT, DEFAULT_TABLE_FORMAT
from ._common_options import add_options, help_option
from ._click_extensions import PywbemcliGroup, PywbemcliCommand

# NOTE: A number of the options use double-dash as the short form.  In those
# cases, a third definition of the options without the double-dash defines
# the corresponding option name, ex. 'include_qualifiers'. It should be
# defined with underscore and not dash

# Issue 224 - Exception in prompt-toolkit with python 2.7. Caused because
# with prompt-toolkit 2 + the completer requires unicode and click_repl not
# passing help as unicode in options as unicode
# NOTE: Insure that all option help attributes are unicode to get around this
#       issue


@cli.group('server', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def server_group():
    """
    Command group for WBEM servers.

    This command group defines commands to inspect and manage core components
    of a WBEM server including server attributes, namespaces, the Interop
    namespace, management profiles, and access to profile central instances.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'server' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@server_group.command('namespaces', cls=PywbemcliCommand,
                      options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def server_namespaces(context):
    """
    List the namespaces of the server.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_server_namespaces(context))


@server_group.command('interop', cls=PywbemcliCommand,
                      options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def server_interop(context):
    """
    Get the Interop namespace of the server.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_server_interop(context))


@server_group.command('brand', cls=PywbemcliCommand,
                      options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def server_brand(context):
    """
    Get the brand of the server.

    Brand information is defined by the server implementor and may or may
    not be available. Pywbem attempts to collect the brand information from
    multiple sources.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_server_brand(context))


@server_group.command('info', cls=PywbemcliCommand,
                      options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def server_info(context):
    """
    Get information about the server.

    The information includes CIM namespaces and server brand.
    """
    context.execute_cmd(lambda: cmd_server_info(context))


###############################################################
#         Server cmds
###############################################################


def cmd_server_namespaces(context):
    """
    Display namespaces in the current WBEM server
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
                                    title='Server Namespaces:',
                                    table_format=output_format))
        else:
            display_text(", ".join(namespaces))

    except Error as er:
        raise click.ClickException('{}: {}'.format(er.__class__.__name__, er))


def cmd_server_interop(context):
    """
    Display interop namespace in the current WBEM server
    """

    output_format = validate_output_format(context.output_format, 'TEXT')

    try:
        interop_ns = context.wbem_server.interop_ns
        context.spinner_stop()

        display_text(interop_ns, output_format)

    except Error as er:
        raise_pywbem_error_exception(er)


def cmd_server_brand(context):
    """
    Display product and version info of the current WBEM server
    """
    output_format = validate_output_format(context.output_format, 'TEXT')

    try:
        brand = context.wbem_server.brand
        context.spinner_stop()

        display_text(brand, output_format)

    except Error as er:
        raise_pywbem_error_exception(er)


def cmd_server_info(context):
    """
    Display general overview of info from current WBEM server
    """
    output_format = validate_output_format(context.output_format, 'TABLE')

    try:
        # execute the namespaces to force contact with server before
        # turning off the spinner.
        server = context.wbem_server
        namespaces = sorted(server.namespaces)
        context.spinner_stop()

        rows = []
        headers = ['Brand', 'Version', 'Interop Namespace', 'Namespaces']
        sep = '\n' if namespaces and len(namespaces) > 3 else ', '
        namespaces = sep.join(namespaces)

        rows.append([server.brand, server.version,
                     server.interop_ns,
                     namespaces])
        click.echo(format_table(rows, headers,
                                title='Server General Information',
                                table_format=output_format))

    except Error as er:
        raise_pywbem_error_exception(er)
