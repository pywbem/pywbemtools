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
Click Command definition for the qualifer command group which includes
cmds for get and enumerate for CIM qualifier types.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import click

from pywbem import Error, CIMError

from .pywbemcli import cli
from ._common import sort_cimobjects, pywbem_error_exception

from ._common_cmd_functions import ResultsHandler
from ._common_options import namespace_option, summary_option, \
    multiple_namespaces_option_dflt_conn, object_order_option
from .._click_extensions import PywbemtoolsGroup, PywbemtoolsCommand, \
    CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT
from .._options import add_options, help_option
from .._output_formatting import validate_output_format

# Issue 224 - Exception in prompt-toolkit with python 2.7. Caused because
# with prompt-toolkit 2 + the completer requires unicode and click_repl not
# passing help as unicode in options as unicode
# NOTE: Insure that all option help attributes are unicode to get around this
#       issue


@cli.group('qualifier', cls=PywbemtoolsGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def qualifier_group():
    """
    Command group for CIM qualifier declarations.

    This command group defines commands to inspect and delete CIM qualifier
    declarations in the WBEM Server.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'qualifier' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@qualifier_group.command('get', cls=PywbemtoolsCommand,
                         options_metavar=CMD_OPTS_TXT)
@click.argument('qualifiername', type=str, metavar='QUALIFIERNAME',
                required=True,)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(object_order_option)
@add_options(help_option)
@click.pass_obj
def qualifier_get(context, qualifiername, **options):
    """
    Get a qualifier declaration.

    Get a CIM qualifier declaration (QUALIFIERNAME argument) in a CIM
    namespace (--namespace option). If no namespace was specified, the default
    namespace of the connection is used.

    In the output, the qualifier declaration will formatted as defined by the
    --output-format general option.
    """
    context.execute_cmd(
        lambda: cmd_qualifier_get(context, qualifiername, options))


@qualifier_group.command('delete', cls=PywbemtoolsCommand,
                         options_metavar=CMD_OPTS_TXT)
@click.argument('qualifiername', type=str, metavar='QUALIFIERNAME',
                required=True,)
@add_options(namespace_option)
@add_options(help_option)
@click.pass_obj
def qualifier_delete(context, qualifiername, **options):
    """
    Delete a qualifier declaration.

    Delete a CIM qualifier declaration (QUALIFIERNAME argument) in a CIM
    namespace (--namespace option). If no namespace was specified, the default
    namespace of the connection is used.

    This command executes the DeleteQualifier operation against the WBEM server
    and leaves it to the WBEM server to reject the operation if any classes
    in the namespace use the qualifier.

    In the output, the qualifier declaration will formatted as defined by the
    --output-format general option.
    """
    context.execute_cmd(
        lambda: cmd_qualifier_delete(context, qualifiername, options))


@qualifier_group.command('enumerate', cls=PywbemtoolsCommand,
                         options_metavar=CMD_OPTS_TXT)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(object_order_option)
@add_options(summary_option)
@add_options(help_option)
@click.pass_obj
def qualifier_enumerate(context, **options):
    """
    List the qualifier declarations in a namespace.

    Enumerate the CIM qualifier declarations in the specified CIM namespace(s)
    (--namespace option). If no namespace was specified, the default namespace
    of the connection is used.

    In the output, the qualifier declaration will formatted as defined by the
    --output-format general option.
    """
    context.execute_cmd(lambda: cmd_qualifier_enumerate(context, options))


####################################################################
#   Qualifier declaration command processing functions
#####################################################################


def cmd_qualifier_get(context, qualifiername, options):
    """
    Execute the command for get qualifier and display result. Displays the
    instances from single or multiple namespaces based on namespace option.
    """
    conn = context.pywbem_server.conn
    output_format = validate_output_format(context.output_format, ['CIM',
                                                                   'TABLE'])

    results = ResultsHandler(context, options, output_format, "QualDeclName",
                             qualifiername)

    for ns in results:
        try:
            results.add(conn.GetQualifier(qualifiername, namespace=ns))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

    results.display()


def cmd_qualifier_delete(context, qualifiername, options):
    """
    Execute the command for delete qualifier and display result
    """
    conn = context.pywbem_server.conn
    try:
        conn.DeleteQualifier(qualifiername, namespace=options['namespace'])
        if context.verbose:
            context.spinner_stop()
            click.echo('Deleted qualifier type {}.'.format(qualifiername))
    except Error as er:
        raise pywbem_error_exception(er)


def cmd_qualifier_enumerate(context, options):
    """
    Execute the command for enumerate qualifiers and desplay the result.
    """
    conn = context.pywbem_server.conn
    output_format = validate_output_format(context.output_format, ['CIM',
                                                                   'TABLE'])

    results = ResultsHandler(context, options, output_format, "QualDeclName",
                             None)

    for ns in results:
        try:
            results.add(sort_cimobjects(conn.EnumerateQualifiers(namespace=ns)))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

    results.display()
