# Copyright TODO
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
"""
from __future__ import absolute_import

import click
from pywbem import ValueMapping, Error
from .pywbemcli import cli, CMD_OPTS_TXT
from ._common import display_cim_objects
from ._common_options import sort_option, add_options


def print_profile_info(org_vm, inst):
    """Print the registered org, name, version for the profile defined by
       inst
    """
    org = org_vm.tovalues(inst['RegisteredOrganization'])
    name = inst['RegisteredName']
    vers = inst['RegisteredVersion']
    print("  %s %s %s" % (org, name, vers))


@cli.group('server', options_metavar=CMD_OPTS_TXT)
def class_group():
    """
    Command group for server operations.
    """
    pass


@class_group.command('namespaces', options_metavar=CMD_OPTS_TXT)
@add_options(sort_option)
@click.pass_obj
def server_namespaces(context, **options):
    """
    Display the set of namespaces in the current WBEM server
    """
    context.execute_cmd(lambda: cmd_server_namespaces(context, options))


@class_group.command('interop', options_metavar=CMD_OPTS_TXT)
@add_options(sort_option)
@click.pass_obj
def server_interop(context, **options):
    """
    Display the interop namespace name in the WBEM Server.
    """
    context.execute_cmd(lambda: cmd_server_interop(context, options))


@class_group.command('brand', options_metavar=CMD_OPTS_TXT)
@add_options(sort_option)
@click.pass_obj
def server_brand(context, **options):
    """
    Display the interop namespace name in the WBEM Server.
    """
    context.execute_cmd(lambda: cmd_server_brand(context, options))


@class_group.command('info', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def server_info(context):
    """
    Display the brand information on the current WBEM Server.
    """
    context.execute_cmd(lambda: cmd_server_info(context))


@class_group.command('profiles', options_metavar=CMD_OPTS_TXT)
@click.option('-o', '--organization', type=str, required=False,
              metavar='<org name>',
              help='Filter by the defined organization. (ex. -o DMTF')
@click.option('-n', '--profilename', type=str, required=False,
              metavar='<profile name>',
              help='Filter by the profile name. (ex. -n Array')
@click.pass_obj
def server_profiles(context, **options):
    """
    Display profiles on the current WBEM Server.

    This display may be filtered by the optional organization and profile
    name options
    """
    context.execute_cmd(lambda: cmd_server_profiles(context, options))


@class_group.command('connection', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def server_connection(context):
    """
    Display information on the connection used by this server.
    """
    context.execute_cmd(lambda: cmd_server_connection(context))


###############################################################
#         Server cmds
###############################################################
def cmd_server_namespaces(context, options):
    """
    Display namespaces in the current WBEMServer
    """
    try:
        ns = context.wbem_server.namespaces
        display_cim_objects(context, ns, context.output_format)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_server_interop(context, options):
    """
    Display interop namespace in the current WBEMServer
    """
    try:
        display_cim_objects(context, context.wbem_server.interop_ns,
                            context.output_format)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_server_brand(context, options):
    """
    Display product and version info of the current WBEMServer
    """
    try:
        click.echo(context.wbem_server.brand)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_server_info(context):
    """
    Display general overview of info from current WBEMServer
    """
    try:
        context.spinner.stop()
        click.echo("Brand:\n  %s" % context.wbem_server.brand)
        click.echo("Version:\n  %s" % context.wbem_server.version)
        click.echo("Interop namespace:\n  %s" % context.wbem_server.interop_ns)

        click.echo("All namespaces:")
        for ns in context.wbem_server.namespaces:
            click.echo("  %s" % ns)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_server_profiles(context, options):
    """
    Display general overview of info from current WBEMServer
    """
    try:
        found_server_profiles = context.wbem_server.get_selected_profiles(
            registered_org=options['organization'],
            registered_name=options['profilename'])

        org_vm = ValueMapping.for_property(context.wbem_server,
                                           context.wbem_server.interop_ns,
                                           'CIM_RegisteredProfile',
                                           'RegisteredOrganization')

        print('Profiles for %s:%s' % (options['organization'],
                                      options['profilename']))

        context.spinner.stop()
        for inst in found_server_profiles:
            print_profile_info(org_vm, inst)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_server_connection(context):
    """Display information on the current WBEM Connection"""
    try:
        conn = context.conn
        click.echo('\nurl: %s\ncreds: %s\n.x509: %s\ndefault_namespace: %s\n'
                   'timeout: %s sec.\nca_certs: %s' %
                   (conn.url, conn.creds, conn.x509, conn.default_namespace,
                    conn.timeout, conn.ca_certs))
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
