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
"""
from __future__ import absolute_import

import click
from pywbem import ValueMapping, Error
from .pywbemcli import cli
from ._common import CMD_OPTS_TXT, format_table
from ._common_options import add_options, sort_option


@cli.group('server', options_metavar=CMD_OPTS_TXT)
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


@server_group.command('namespaces', options_metavar=CMD_OPTS_TXT)
@add_options(sort_option)
@click.pass_obj
def server_namespaces(context, **options):
    """
    List the namespaces of the server.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_server_namespaces(context, options))


@server_group.command('interop', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def server_interop(context):
    """
    Get the Interop namespace of the server.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_server_interop(context))


@server_group.command('brand', options_metavar=CMD_OPTS_TXT)
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


@server_group.command('info', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def server_info(context):
    """
    Get information about the server.

    The information includes CIM namespaces and server brand.
    """
    context.execute_cmd(lambda: cmd_server_info(context))


@server_group.command('profiles', options_metavar=CMD_OPTS_TXT)
@click.option('-o', '--organization', type=str, required=False,
              metavar='<org name>',
              help='Filter by the defined organization. (ex. -o DMTF')
@click.option('-p', '--profile', type=str, required=False,
              metavar='<profile name>',
              help='Filter by the profile name. (ex. -p Array')
@click.pass_obj
def server_profiles(context, **options):
    """
    List management profiles advertized by the server.

    Retrieve the CIM instances representing the WBEM management profiles
    advertized by the WBEM server, and display information about each profile.
    WBEM management profiles are defined by DMTF and SNIA and define the
    management functionality that is available.

    The retrieved profiles can be filtered using the --organization and
    --profile options.

    The output is formatted as a table showing the organization, name, and
    version for each profile. The --output-format option is ignored unless it
    specifies a table format.
    """
    context.execute_cmd(lambda: cmd_server_profiles(context, options))


@server_group.command('get-centralinsts', options_metavar=CMD_OPTS_TXT)
@click.option('-o', '--organization', type=str, required=False,
              metavar='<org name>',
              help='Filter by the defined organization. (ex. -o DMTF')
@click.option('-p', '--profile', type=str, required=False,
              metavar='<profile name>',
              help='Filter by the profile name. (ex. -p Array')
@click.option('-c', '--central-class', type=str, required=False,
              metavar='<classname>',
              help='Optional. Required only if profiles supports only '
              'scopig methodology')
@click.option('-s', '--scoping-class', type=str, required=False,
              metavar='<classname>',
              help='Optional. Required only if profiles supports only '
              'scopig methodology')
@click.option('-S', '--scoping-path', type=str, required=False,
              multiple=True,
              metavar='<pathname>',
              help='Optional. Required only if profiles supports only '
              'scopig methodology. Multiples allowed')
@click.option('-r', '--reference-direction',
              type=click.Choice(['snia', 'dmtf']),
              default='dmtf',
              show_default=True,
              help='Navigation direction for association.')
@click.pass_obj
def server_centralinsts(context, **options):
    """
    List central instances of mgmt profiles on the server.

    Retrieve the CIM instances that are central instances of the specified
    WBEM management profiles, and display these instances. By default, all
    management profiles advertized on the server are used. The profiles
    can be filtered by using the --organization and --profile options.

    The central instances are determined using all methodologies defined
    in DSP1033 V1.1 in the order of GetCentralInstances, central class,
    and scoping class methodology.

    Profiles that only use the scoping class methodology require the
    specification of the --central-class, --scoping-class, and --scoping-path
    options because additional information is needed to perform the scoping
    class methodology.

    The retrieved central instances are displayed along with the organization,
    name, and version of the profile they belong to, formatted as a table.
    The --output-format general option is ignored unless it specifies a table
    format.
    """
    context.execute_cmd(lambda: cmd_server_centralinsts(context, options))


@server_group.command('connection', options_metavar=CMD_OPTS_TXT)
@click.pass_obj
def server_connection(context):
    """
    Get connection info used by this server.

    Display the information about the connection used to connect to the
    WBEM server.

    This is equivalent to the 'connection show' command.
    """
    context.execute_cmd(lambda: cmd_server_connection(context))


# TODO: reactivate and implement this in version 0.6.0
# @server_group.command('test_pull', options_metavar=CMD_OPTS_TXT)
# @click.pass_obj
# def server_test_pull(context):
#    """
#    Test existence of pull opeations.
#
#    Test whether the pull WBEMConnection methods (ex. OpenEnumerateInstances)
#    exist on the WBEM server.
#
#    This command tests all of the pull operations and reports any that
#    return a NOT_SUPPORTED response.
#    """
#    context.execute_cmd(lambda: cmd_server_test_pull(context))


###############################################################
#         Server cmds
###############################################################

def cmd_server_test_pull(context):
    """
        Test the execution of pull operations against the target server.
        Executes pull operations and reports whether pull is supported.

    """
    raise click.ClickException('test_pull Not implemented')


def cmd_server_namespaces(context, options):
    """
    Display namespaces in the current WBEM server
    """
    try:
        namespaces = context.wbem_server.namespaces
        if options['sort']:
            namespaces.sort()
        context.spinner.stop()

        # create list for each row
        rows = [[ns] for ns in namespaces]

        click.echo(format_table(rows, ['Namespace Name'],
                                title='Server Namespaces:',
                                table_format=context.output_format))

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_server_interop(context):
    """
    Display interop namespace in the current WBEM server
    """
    try:
        interop_ns = context.wbem_server.interop_ns
        context.spinner.stop()

        rows = [[interop_ns]]

        click.echo(format_table(rows, ['Namespace Name'],
                                title='Server Interop Namespace:',
                                table_format=context.output_format))
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_server_brand(context):
    """
    Display product and version info of the current WBEM server
    """
    try:
        brand = context.wbem_server.brand
        context.spinner.stop()

        rows = [[brand]]
        click.echo(format_table(rows, ['WBEM server brand'],
                                title='Server brand:',
                                table_format=context.output_format))
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_server_info(context):
    """
    Display general overview of info from current WBEM server
    """
    try:
        # execute the namespaces to force contact with server before
        # turning off the spinner.
        server = context.wbem_server
        server.namespaces  # pylint: disable=pointless-statement
        context.spinner.stop()

        server = context.wbem_server

        rows = []
        headers = ['Brand', 'Version', 'Interop Namespace', 'Namespaces']
        if len(server.namespaces) > 3:
            namespaces = '\n'.join(server.namespaces)
        else:
            namespaces = ', '.join(server.namespaces)
        rows.append([server.brand, server.version,
                     server.interop_ns,
                     namespaces])
        click.echo(format_table(rows, headers,
                                title='Server General Information',
                                table_format=context.output_format))

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def get_profile_info(org_vm, inst):
    """
    Get the org, name, and version from the profile instance and
    return them as a tuple.
    """
    org = org_vm.tovalues(inst['RegisteredOrganization'])
    name = inst['RegisteredName']
    vers = inst['RegisteredVersion']
    return org, name, vers


def cmd_server_profiles(context, options):
    """
    Display general overview of info from current WBEM server
    """
    server = context.wbem_server
    try:
        found_server_profiles = server.get_selected_profiles(
            registered_org=options['organization'],
            registered_name=options['profile'])

        org_vm = ValueMapping.for_property(server,
                                           server.interop_ns,
                                           'CIM_RegisteredProfile',
                                           'RegisteredOrganization')
        rows = []
        for inst in found_server_profiles:
            row = get_profile_info(org_vm, inst)
            rows.append(row)
        # sort by org
        rows.sort(key=lambda x: (x[0], x[1]))
        headers = ['Organization', 'Registered Name', 'Version']

        click.echo(format_table(rows, headers,
                                title='Advertised management profiles:',
                                table_format=context.output_format))

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


def cmd_server_centralinsts(context, options):
    """
    Display general overview of info from current WBEM server
    """
    server = context.wbem_server
    try:
        found_server_profiles = server.get_selected_profiles(
            registered_org=options['organization'],
            registered_name=options['profile'])

        org_vm = ValueMapping.for_property(server,
                                           server.interop_ns,
                                           'CIM_RegisteredProfile',
                                           'RegisteredOrganization')
        rows = []
        for inst in found_server_profiles:
            pi = get_profile_info(org_vm, inst)
            row = [":".join(pi)]
            try:
                ci = server.get_central_instances(
                    inst.path,
                    central_class=options['central_class'],
                    scoping_class=options['scoping_class'],
                    scoping_path=options['scoping_path'],
                    reference_direction=options['reference_direction'])
                row.append(":".join([str(p) for p in ci]))
            # mark current inst as failed and continue
            except Exception as ex:  # pylint: disable=broad-except
                click.echo('Exception: %s %s' % (row, ex))
                row.append("Failed")
            rows.append(row)

        # sort by org
        rows.sort(key=lambda x: (x[0]))
        headers = ['Profile', 'Central Instances']

        click.echo(format_table(rows,
                                headers,
                                title='Advertised Central Instances:',
                                table_format=context.output_format))
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
