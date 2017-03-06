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
from .pywbemcli import cli, CMD_OPTS_TXT
from ._common import display_cim_objects
from ._common_options import sort_option, namespace_option, add_options


@cli.group('qualifier', options_metavar=CMD_OPTS_TXT)
def qualifier_group():
    """
    Command Group to manage CIM QualifierDeclarations.

    Includes the capability to get and enumerate qualifier declarations.

    This does not provide the capability to create or delete CIM
    QualifierDeclarations
    """
    pass


@qualifier_group.command('get', options_metavar=CMD_OPTS_TXT)
@click.argument('NAME', type=str, metavar='NAME', required=True,)
@add_options(namespace_option)
@click.pass_obj
def qualifier_get(context, name, **options):
    """
    Display CIMQualifierDeclaration.

    Displays a single CIMQualifierDeclaration for the defined namespace in
    the current WBEMServer
    """
    context.execute_cmd(lambda: cmd_qualifier_get(context, name, options))


@qualifier_group.command('enumerate', options_metavar=CMD_OPTS_TXT)
@add_options(namespace_option)
@add_options(sort_option)
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
def cmd_qualifier_get(context, name, options):
    """
    Execute the command for get qualifier and display result
    """
    try:
        if context.verbose:
            print('get qualifier name: %s ' % (name))

        qual_decl = context.conn.GetQualifier(name,
                                              namespace=options['namespace'])

        display_cim_objects(context, qual_decl, context.ouput_format)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_qualifier_enumerate(context, options):
    """
    Execute the command for enumerate qualifiers and desplay the result.
    """
    try:
        qual_decls = context.conn.EnumerateQualifiers(
            namespace=options['namespace'])

        if options['sort']:
            qual_decls.sort(key=lambda x: x.name)

        display_cim_objects(context, qual_decls, context.ouput_format)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
