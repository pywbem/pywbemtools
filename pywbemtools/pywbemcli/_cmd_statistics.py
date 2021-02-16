# (C) Copyright 2021 IBM Corp.
# (C) Copyright 2021 Inova Development Inc.
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
Click command definition for the statistic command group which includes
cmds for managing the gathering and display of statistics that pywbemcli
and the WBEM server can gather on the WBEM operations

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import click

from pywbem import Error

from .pywbemcli import cli
from ._common import warning_msg, CMD_OPTS_TXT, GENERAL_OPTS_TXT, \
    validate_output_format, output_format_is_table, format_table, \
    SUBCMD_HELP_TXT
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


@cli.group('statistics', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def statistics_group():
    """
    Command group for WBEM server statistics.

    This command group defines commands to control the display of statistical
    data managed by pywbemcli based on the ``--timestats`` general
    option which enables the gathering and display of statistics in pywbemcli.

    Since there may also be capabilities to manage statistics in WBEM servers,
    these commands provide for a) enabling statistics gathering in the WBEM
    server and b) displaying the information gathered.

    One component of the pywbemcli client side statistics depends on the state
    of statistics gathering enabled in the WBEM server, reporting the server
    response time. This appears as the column "Server Time" in the report if
    statistics gathering in the server is enabled.

    Since gathering of statistics in a WBEM server may depend on a server
    setting, pywbemcli provides commands to enable and disable the statistics
    gathering in the server by setting the CIM_ObjectManager
    "GatherStatisticalData" property.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'statistics' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@statistics_group.command('reset', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_reset(context):
    """
    Reset the counts in statistics gathered by pywbemcli.

    This command resets the counts in the statistics gathered by pywbemcli for
    the current connection including the statistics on the server response
    times received from the WBEM server in the ``WBEMServerResponseTime``
    header .

    It does not reset statistics managed by the WBEM server..
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_reset(context))


@statistics_group.command('server-on', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_server_on(context):
    """
    Enable statistics on current server.

    This command  activates the gathering of statistics in the WBEM
    server and the return of server response times for inclusion in
    pywbemcli maintained statistics. The gathering of server statistics and the
    returning of server response times may not be implemented by all WBEM
    servers.

    This may fail if the server does not manage statistics or does not allow
    a client to modify the state of statistics gathering.

    WBEM server statistics gathering state does not impact pywbemcli client
    statistics gathering other than whether the 'Server Time` column is
    included in the report. See the --timestats general option.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_server_on(context))


@statistics_group.command('server-off', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_server_off(context):
    """
    Disable statistics on current server.

    This command turns off the gathering of statistics in the WBEM
    server and the return of server response times for inclusion in
    pywbemcli maintained statistics. The gathering of server statistics and the
    returning of server response times may not be implemented by all WBEM
    servers.

    This may fail if the server does not manage statistics or does not allow
    a client to modify the state of statistics gathering.

    WBEM server statistics gathering state does not impact pywbemcli client
    statistics gathering other than whether the 'Server Time.s` column is
    included in the report. See the --timestats general option.
    """
    # pylint: disable=too-many-function-args

    context.execute_cmd(lambda: cmd_statistics_server_off(context))


@statistics_group.command('server-show', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_server_show(context):
    """
    Display statistics gathered by server.

    Display the current statistics gathered in the WBEM server if statistics
    gathering is implemented and active (see ```statistics server-on```) for
    the current WBEM server.

    These statistics are independent of the statistics gathered by the pywbemcli
    client and displayed for example with the command ``statistics show``.

    Presents a table of the gathered statistical information.

    This command is not implemented. See issue #895
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_server_show(context))


@statistics_group.command('show', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_show(context):
    """
    Display statistics managed by pywbemcli.

    Display the current statistics including client managed statistics on WBEM
    operations and if WBEM server statistics are implemented and enabled, the
    statistics on the returned ``WBEMServerResponseTime`` header.

    Statistics are always displayed as a table independent of output-format
    defined.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_show(context))


@statistics_group.command('status', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_status(context):
    """
    Show statistics enabled status for client and server.

    Show enabled status on statistics gathering for pywbemcli and the
    current WBEM server. Table and text formats are allowed.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_status(context))


###############################################################
#         Server cmds  Common components
###############################################################

OBJMGR_CLN = "CIM_ObjectManager"
OBJMGR_STAT_PROPERTY_NAME = "GatherStatisticalData"


def test_conn_exists(context):
    """
    Test if server defined.

    Returns if server defined

    Exception:
       click.Exception if no current server.
    """
    if not context.conn:
        raise click.ClickException(
            'No server defined in current context.')


def get_objmgr_inst(context):
    """
    Return the state of statistics gathering on the server.
    """
    conn = context.conn
    try:
        interop_ns = context.wbem_server.interop_ns
    except Error as er:
        raise click.ClickException(
            'Cannot access interop namespace. Exception: {}'.format(er))

    try:
        objmanager_insts = conn.EnumerateInstances(OBJMGR_CLN,
                                                   namespace=interop_ns)

        # There must be only one CIM_ObjectManager instance. None causes
        # failure and more than 1 causes warning
        if not objmanager_insts:
            raise click.ClickException(
                'No instances of class {} found on server'.format(OBJMGR_CLN))

        if len(objmanager_insts) > 1:
            warning_msg(
                "Server returned multiple {} instances. Using first.".
                format(objmanager_insts[0].classname))

    except Error as er:
        raise click.ClickException(
            'Failure trying to access object manager instances of class {} '
            'namespace {}. Error: {}'.
            format(OBJMGR_CLN, interop_ns, er))
    objmgr_inst = objmanager_insts[0]

    return objmgr_inst


def to_on_off(state):
    """
    Convert boolean to "on" or "off.

    Return string
        String containing "on" or "off"
    """
    return "on" if state else "off"


def set_server_statistics(context, desired_state):
    """
    Set the server statistics state to on or off, enabling or disabling
    the statistics.

    Parameters:
      desired_state (:class": `boolean)
        Value desired for the GatherStatisticalData property
    """
    conn = context.conn

    interop_ns = context.wbem_server.interop_ns

    objmgr = get_objmgr_inst(context)

    context.spinner_stop()

    try:
        cur_state = objmgr[OBJMGR_STAT_PROPERTY_NAME]
    except KeyError as ke:
        raise click.ClickException(
            'Failure accessing class {} property {}. namespace {}:Error: {}'.
            format(OBJMGR_CLN, OBJMGR_STAT_PROPERTY_NAME, interop_ns, ke))

    if cur_state == desired_state:
        click.echo("Server already in state {}".format(
            to_on_off(desired_state)))
        return

    objmgr[OBJMGR_STAT_PROPERTY_NAME] = desired_state

    # Otherwise modify the property in the server
    try:
        conn.ModifyInstance(objmgr, PropertyList=[OBJMGR_STAT_PROPERTY_NAME],
                            IncludeQualifiers=False)
    except Error as ce:
        raise click.ClickException('Modification of GatherStatisticalData '
                                   'property in instance {} on server failed: '
                                   'Exception {}'.format(objmgr.path, ce))

    modified_objmgr = conn.GetInstance(objmgr.path)

    if modified_objmgr[OBJMGR_STAT_PROPERTY_NAME] != desired_state:
        raise click.ClickException(
            'The WBEM server reported success when changing the {} property '
            'in its {} instance to {} but did not actually change it.'.
            format(OBJMGR_STAT_PROPERTY_NAME, OBJMGR_CLN, interop_ns))

    click.echo("Server GatherStatisticalData set {}".
               format(to_on_off(desired_state)))


###############################################################
#         Statistics cmds action functions
###############################################################


def cmd_statistics_server_on(context):
    """
    Attempt to enable the statistics gathering on the current server if there
    is a current server defined.
    """
    test_conn_exists(context)
    set_server_statistics(context, True)


def cmd_statistics_server_off(context):
    """
    Attempt to disable the statistics gathering on the current server if there
    is a current server defined.
    """
    test_conn_exists(context)
    set_server_statistics(context, False)


def cmd_statistics_status(context):
    """
    Show current status of both client and WBEM server statistics if there
    is a connection.

    It gets the status of the WBEM server statistics from the WBEM server
    and the client statistics from the context and displays either a
    table or text representation of the status.

    If there is an issue with getting statistics information from the server,
    it displays detailed information about the server response.

    """

    # validate output format with default of table
    output_format = validate_output_format(context.output_format, ['TABLE',
                                                                   'TEXT'])

    test_conn_exists(context)

    # Display server status as on/off
    try:
        objmgr = get_objmgr_inst(context)
        try:
            svr_status = objmgr[OBJMGR_STAT_PROPERTY_NAME]
            svr_status = to_on_off(svr_status)
        except KeyError:
            svr_status = "No property {}".format(OBJMGR_STAT_PROPERTY_NAME)
    except Error as er:
        svr_status = "Not settable {}".format(er)

    context.spinner_stop()

    pywbemcli_stats_status = to_on_off(context.timestats)
    if output_format_is_table(output_format):
        headers = ['statistics source', 'status']

        rows = [["client statistics display", pywbemcli_stats_status],
                ['server statistics', svr_status]]
        click.echo(format_table(rows, headers, "Statistics status"))

    else:
        click.echo("Statistics status: client statistics={}; Server "
                   "statistics={}".format(pywbemcli_stats_status,
                                          svr_status))


def cmd_statistics_reset(context):
    """
    Reset the client statistics. This command does not impact the

    statistics retrieved from the server with ``statistics server-show``.
    It does reset the statistics kept in the pywbem client for server
    response time.
    """
    test_conn_exists(context)

    context.conn.statistics.reset()

    context.spinner_stop()
    click.echo("Pywbemcli statistics reset")


def cmd_statistics_show(context):
    """
    If the statistics are enabled for the client and the connection exits,
    display the statistics
    """
    test_conn_exists(context)

    context.spinner_stop()

    click.echo(context.format_statistics(context.conn.statistics, context))


# pylint: disable=unused-argument
def cmd_statistics_server_show(context):
    """
    If server statistics are enabled get them from the server and display.

    This command may fail if the WBEM server has not implemented the
    management of detailed statistics.
    """
    context.spinner_stop()

    raise click.ClickException(
        "This command not implemented. See issue # 895.")
