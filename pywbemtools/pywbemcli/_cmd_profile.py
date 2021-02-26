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
Click command definition for the profile command group which includes
cmds for inspection and management of the registered profiles that are
maintained in the WBEM Server and used by the client to determine what
WBEM management functionality the server supports.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import click

from pywbem import ValueMapping, Error

from .pywbemcli import cli
from ._common import format_table, pywbem_error_exception, \
    validate_output_format, CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT
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


@cli.group('profile', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def profile_group():
    """
    Command group for WBEM management profiles.

    This command group defines commands to inspect and manage the WBEM
    management profiles maintained by the WBEM server.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'server' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@profile_group.command('list', cls=PywbemcliCommand,
                       options_metavar=CMD_OPTS_TXT)
@click.option('-o', '--organization', type=str, metavar='ORG-NAME',
              required=False,
              help=u'Filter by the defined organization. (ex. -o DMTF')
@click.option('-p', '--profile', type=str, metavar='PROFILE-NAME',
              required=False,
              help=u'Filter by the profile name. (ex. -p Array')
@add_options(help_option)
@click.pass_obj
def profile_list(context, **options):
    """
    List WBEM management profiles advertised by the server.

    Retrieve  the WBEM management profiles advertised by the WBEM server, and
    display information about each profile. WBEM management profiles are
    defined by DMTF and SNIA and define the management functionality that is
    available.

    The retrieved profiles can be filtered using the --organization and
    --profile options.

    The output is formatted as a table showing the organization, name, and
    version for each profile. The --output-format option is ignored unless it
    specifies a table format.
    """
    context.execute_cmd(lambda: cmd_profile_list(context, options))


@profile_group.command('centralinsts', cls=PywbemcliCommand,
                       options_metavar=CMD_OPTS_TXT)
@click.option('-o', '--organization', type=str, metavar='ORG-NAME',
              required=False,
              help=u'Filter by the defined organization. (ex. -o DMTF')
@click.option('-p', '--profile', type=str, metavar='PROFILE-NAME',
              required=False,
              help=u'Filter by the profile name. (ex. -p Array')
@click.option('--cc', '--central-class', 'central_class', type=str,
              metavar='CLASSNAME', required=False,
              help=u'Optional. Required only if profiles supports only '
              u'scoping methodology')
@click.option('--sc', '--scoping-class', 'scoping_class', type=str,
              metavar='CLASSNAME', required=False,
              help=u'Optional. Required only if profiles supports only '
              u'scoping methodology')
@click.option('--sp', '--scoping-path', 'scoping_path', type=str,
              metavar='CLASSLIST', required=False, multiple=True,
              help=u'Optional. Required only if profiles supports only '
              u'scoping methodology. Multiples allowed')
@click.option('--rd', '--reference-direction', 'reference_direction',
              type=click.Choice(['snia', 'dmtf']),
              default='dmtf',
              show_default=True,
              help=u'Navigation direction for association.')
@add_options(help_option)
@click.pass_obj
def centralinsts(context, **options):
    """
    List WBEM management profile central instances on the server.

    Retrieve the CIM instances that are central instances of the specified
    WBEM management profiles, and display these instances. By default, all
    management profiles advertized on the server are included. The profiles
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
    context.execute_cmd(lambda: cmd_profile_centralinsts(context, options))


###############################################################
#         Server cmds
###############################################################


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


def cmd_profile_list(context, options):
    """
    Display a list of the profiles registered for the server and filtered
    by the command options.
    """
    output_format = validate_output_format(context.output_format, 'TABLE')

    wbem_server = context.pywbem_server.wbem_server

    organization = options['organization']
    profile_name = options['profile']
    try:
        found_server_profiles = wbem_server.get_selected_profiles(
            registered_org=organization,
            registered_name=profile_name)

        org_vm = ValueMapping.for_property(wbem_server,
                                           wbem_server.interop_ns,
                                           'CIM_RegisteredProfile',
                                           'RegisteredOrganization')
        rows = []
        for inst in found_server_profiles:
            row = get_profile_info(org_vm, inst)
            rows.append(row)
        rows.sort(key=profile_row_sortkey)
        headers = ['Organization', 'Registered Name', 'Version']

        title = 'Advertised management profiles:'

        if organization:
            title += " org={}".format(organization)
        if profile_name:
            title += " name={}".format(profile_name)

        click.echo(format_table(rows, headers,
                                title=title,
                                table_format=output_format))

    except Error as er:
        raise pywbem_error_exception(er)


def cmd_profile_centralinsts(context, options):
    """
    Display general information on the central instances of one or more
    profiles.
    """
    output_format = validate_output_format(context.output_format, ['CIM',
                                                                   'TABLE'])

    wbem_server = context.pywbem_server.wbem_server
    organization = options['organization']
    profile_name = options['profile']
    try:
        found_server_profiles = wbem_server.get_selected_profiles(
            registered_org=organization,
            registered_name=profile_name)

        org_vm = ValueMapping.for_property(wbem_server,
                                           wbem_server.interop_ns,
                                           'CIM_RegisteredProfile',
                                           'RegisteredOrganization')
        rows = []
        for inst in found_server_profiles:
            pi = get_profile_info(org_vm, inst)
            row = [":".join(pi)]
            try:
                ci = wbem_server.get_central_instances(
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

        headers = ['Profile', 'Central Instance paths']

        # sort by profile
        rows.sort(key=lambda x: (x[0]))

        click.echo(format_table(rows,
                                headers,
                                title='Advertised Central Instances:',
                                table_format=output_format))
    except Error as er:
        raise pywbem_error_exception(er)
