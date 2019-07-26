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
"""

from __future__ import absolute_import

import click
from pywbem import Error
from .pywbemcli import cli
from ._common import display_cim_objects, CMD_OPTS_TXT, \
    output_format_is_table, sort_cimobjects
from ._common_options import namespace_option, add_options, \
    summary_objects_option


@cli.group('qualifier', options_metavar=CMD_OPTS_TXT)
def qualifier_group():
    """
    Command group to view QualifierDeclarations.

    Includes the capability to get and enumerate CIM qualifier declarations
    defined in the WBEM Server.

    pywbemcli does not provide the capability to create or delete CIM
    QualifierDeclarations

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    command. These are NOT retained after the command is executed.
    """
    pass  # pylint: disable=unnecessary-pass


@qualifier_group.command('get', options_metavar=CMD_OPTS_TXT)
@click.argument('qualifiername', type=str, metavar='QUALIFIERNAME',
                required=True,)
@add_options(namespace_option)
@click.pass_obj
def qualifier_get(context, qualifiername, **options):
    """
    Display CIMQualifierDeclaration.

    Displays CIMQualifierDeclaration QUALIFIERNAME for the defined namespace in
    the current WBEMServer
    """
    context.execute_cmd(lambda: cmd_qualifier_get(context, qualifiername,
                                                  options))


@qualifier_group.command('enumerate', options_metavar=CMD_OPTS_TXT)
@add_options(namespace_option)
@add_options(summary_objects_option)
@click.pass_obj
def qualifier_enumerate(context, **options):
    """
    Enumerate CIMQualifierDeclaractions.

    Displays all of the CIMQualifierDeclaration objects in the defined
    namespace in the current WBEM Server
    """
    context.execute_cmd(lambda: cmd_qualifier_enumerate(context, options))


####################################################################
#   Qualifier declaration command processing functions
#####################################################################


def qual_outputformat(output_format):
    """ If output format is table type, force to mof"""

    return 'mof' if output_format_is_table(output_format) else output_format


def cmd_qualifier_get(context, qualifiername, options):
    """
    Execute the command for get qualifier and display result
    """
    try:
        qual_decl = context.conn.GetQualifier(qualifiername,
                                              namespace=options['namespace'])

        display_cim_objects(context, qual_decl,
                            qual_outputformat(context.output_format))

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_qualifier_enumerate(context, options):
    """
    Execute the command for enumerate qualifiers and desplay the result.
    """
    try:
        qual_decls = sort_cimobjects(context.conn.EnumerateQualifiers(
            namespace=options['namespace']))

        display_cim_objects(context, qual_decls, context.output_format,
                            summary=options['summary'])

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
