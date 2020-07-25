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

from pywbem import ValueMapping, Error

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


@server_group.command('profiles', cls=PywbemcliCommand,
                      options_metavar=CMD_OPTS_TXT)
@click.option('-o', '--organization', type=str, metavar='ORG-NAME',
              required=False,
              help='Filter by the defined organization. (ex. -o DMTF')
@click.option('-p', '--profile', type=str, metavar='PROFILE-NAME',
              required=False,
              help='Filter by the profile name. (ex. -p Array')
@add_options(help_option)
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


@server_group.command('centralinsts', cls=PywbemcliCommand,
                      options_metavar=CMD_OPTS_TXT)
@click.option('-o', '--organization', type=str, metavar='ORG-NAME',
              required=False,
              help='Filter by the defined organization. (ex. -o DMTF')
@click.option('-p', '--profile', type=str, metavar='PROFILE-NAME',
              required=False,
              help='Filter by the profile name. (ex. -p Array')
@click.option('--cc', '--central-class', 'central_class', type=str,
              metavar='CLASSNAME', required=False,
              help='Optional. Required only if profiles supports only '
              'scopig methodology')
@click.option('--sc', '--scoping-class', 'scoping_class', type=str,
              metavar='CLASSNAME', required=False,
              help='Optional. Required only if profiles supports only '
              'scopig methodology')
@click.option('--sp', '--scoping-path', 'scoping_path', type=str,
              metavar='CLASSLIST', required=False, multiple=True,
              help='Optional. Required only if profiles supports only '
              'scopig methodology. Multiples allowed')
@click.option('--rd', '--reference-direction', 'reference_direction',
              type=click.Choice(['snia', 'dmtf']),
              default='dmtf',
              show_default=True,
              help='Navigation direction for association.')
@add_options(help_option)
@click.pass_obj
def centralinsts(context, **options):
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
        server.namespaces  # pylint: disable=pointless-statement
        context.spinner_stop()

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
                                table_format=output_format))

    except Error as er:
        raise_pywbem_error_exception(er)


def get_profile_info(org_vm, inst):
    """
    Get the org, name, and version from the profile instance and
    return them as a tuple.
    """
    org = org_vm.tovalues(inst['RegisteredOrganization'])
    name = inst['RegisteredName']
    vers = inst['RegisteredVersion']
    return org, name, vers


def profile_row_sortkey(row):
    """
    Return a sort key for profiles that sorts by org name, profile name, and
    profile version (numeric).

    row is a tuple(org, name, version) where version is a version string such
    as "1.2.3" or "1.2.3a".
    """
    version_parts = []
    for v_str in row[2].split('.'):
        try:
            v_int = int(v_str)
        except ValueError:
            v_int = v_str
        version_parts.append(v_int)
    return row[0], row[1], tuple(version_parts)


def cmd_server_profiles(context, options):
    """
    Display general overview of info from current WBEM server
    """
    output_format = validate_output_format(context.output_format, 'TABLE')

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
        rows.sort(key=profile_row_sortkey)
        headers = ['Organization', 'Registered Name', 'Version']

        click.echo(format_table(rows, headers,
                                title='Advertised management profiles:',
                                table_format=output_format))

    except Error as er:
        raise_pywbem_error_exception(er)


def cmd_server_centralinsts(context, options):
    """
    Display general information on the central instances of one or more
    profiles.
    """
    output_format = validate_output_format(context.output_format, ['CIM',
                                                                   'TABLE'])

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
                row.append("\n".join([str(p) for p in ci]))
            # mark current inst as failed and continue
            except Exception as ex:  # pylint: disable=broad-except
                click.echo('Exception: {} {}'.format(row, ex))
                row.append("Failed")
            rows.append(row)

        # sort by org
        rows.sort(key=lambda x: (x[0]))
        headers = ['Profile', 'Central Instance paths']

        click.echo(format_table(rows,
                                headers,
                                title='Advertised Central Instances:',
                                table_format=output_format))
    except Error as er:
        raise_pywbem_error_exception(er)
