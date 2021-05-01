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
import six

from pywbem import Error, ValueMapping, CIMDateTime

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
    Command group for WBEM operation statistics.

    This command group defines commands to control the gathering and display of
    statistical data about the WBEM operations issued by pywbemcli or processed
    by a WBEM server.

    Pywbemcli maintains statistics about the WBEM operations it has issued. This
    includes the Client Time measured on the client side and the Server Time
    measured by the WBEM server and reported in the 'WBEMServerResponseTime'
    header field in the CIM-XML response (if supported by the WBEM server).

    The WBEM server may also support maintaining statistics about the WBEM
    operations it has processed (possibly by multiple clients). Pywbemcli
    supports enabling or disabling the statistics gathering on the WBEM server
    via the 'GatherStatisticalData' property in the 'CIM_ObjectManager'
    instance for the WBEM server and supports retrieving and displaying the
    server maintained statistics.

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
    Reset client maintained statistics.

    This command resets the counts in the statistics maintained by pywbemcli.
    This includes the server response times received from the WBEM server in
    the 'WBEMServerResponseTime' header field of the CIM-XML response,
    if supported and enabled.

    This command does not reset the server maintained statistics.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_reset(context))


@statistics_group.command('server-on', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_server_on(context):
    """
    Enable server maintained statistics.

    This command activates the gathering of statistics in the current
    WBEM server and also activates the returning of server response times in
    the CIM-XML response for inclusion in the client maintained statistics,
    by setting the 'GatherStatisticalData' property to True in the
    'CIM_ObjectManager' instance for the WBEM server.

    This command fails if the server does not support gathering statistics
    or does not allow a client to modify the state of statistics gathering.

    This command does not affect the state of the client maintained statistics
    other than whether the server response times are included. See the
    '--timestats' general option for controlling the displaying of client
    maintained statistics.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_server_on(context))


@statistics_group.command('server-off', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_server_off(context):
    """
    Disable server maintained statistics.

    This command deactivates the gathering of statistics in the current
    WBEM server and also deactivates the returning of server response times in
    the CIM-XML response for inclusion in the client maintained statistics,
    by setting the 'GatherStatisticalData' property to False in the
    'CIM_ObjectManager' instance for the WBEM server.

    This command fails if the server does not support gathering statistics
    or does not allow a client to modify the state of statistics gathering.

    This command does not affect the state of the client maintained statistics
    other than whether the server response times are included. See the
    '--timestats' general option for controlling the displaying of client
    maintained statistics.
    """
    # pylint: disable=too-many-function-args

    context.execute_cmd(lambda: cmd_statistics_server_off(context))


@statistics_group.command('server-show', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_server_show(context):
    """
    Display server maintained statistics.

    Retrieve and display the statistics gathered by the current WBEM server.
    This requires statistics gathering to be enabled on the server (see
    'statistics server-on' command).

    This command fails if the server does not support gathering statistics.

    These statistics are independent of the client maintained statistics which
    can be displayed with the command 'statistics show'.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_server_show(context))


@statistics_group.command('show', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_show(context):
    """
    Display client maintained statistics.

    Display the statistics gathered by pywbemcli.
    This includes the server response times received from the WBEM server in
    the 'WBEMServerResponseTime' header field of the CIM-XML response,
    if supported and enabled.

    These statistics are independent of the server maintained statistics which
    can be displayed with the command 'statistics server-show'.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_show(context))


@statistics_group.command('status', cls=PywbemcliCommand,
                          options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def statistics_status(context):
    """
    Show enabled status of client and server maintained statistics.

    Show the enabled status for displaying the statistics gathered by
    pywbemcli, and for gathering the statistics on the current WBEM server.
    """
    # pylint: disable=too-many-function-args
    context.execute_cmd(lambda: cmd_statistics_status(context))


###############################################################
#         Server cmds  Common components
###############################################################

OBJMGR_CLN = "CIM_ObjectManager"
OBJMGR_STAT_PROPERTY_NAME = "GatherStatisticalData"
CIMOM_STATISTICAL_DATA_CLASS = "CIM_CIMOMStatisticalData"


def get_objmgr_inst(context):
    """
    Return the state of statistics gathering on the server.
    """
    conn = context.pywbem_server.conn
    wbem_server = context.pywbem_server.wbem_server
    try:
        interop_ns = wbem_server.interop_ns
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
    conn = context.pywbem_server.conn
    wbem_server = context.pywbem_server.wbem_server

    interop_ns = wbem_server.interop_ns

    objmgr = get_objmgr_inst(context)

    context.spinner_stop()

    try:
        cur_state = objmgr[OBJMGR_STAT_PROPERTY_NAME]
    except KeyError as ke:
        raise click.ClickException(
            'Failure accessing class {} property {}. namespace {}:Error: {}'.
            format(OBJMGR_CLN, OBJMGR_STAT_PROPERTY_NAME, interop_ns, ke))

    if cur_state == desired_state:
        click.echo("Server statistics gathering was already {}".
                   format(to_on_off(desired_state)))
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

    click.echo("Server statistics gathering set to {}".
               format(to_on_off(desired_state)))


###############################################################
#         Statistics cmds action functions
###############################################################


def cmd_statistics_server_on(context):
    """
    Attempt to enable the statistics gathering on the current server if there
    is a current server defined.
    """
    set_server_statistics(context, True)


def cmd_statistics_server_off(context):
    """
    Attempt to disable the statistics gathering on the current server if there
    is a current server defined.
    """
    set_server_statistics(context, False)


def cmd_statistics_status(context):
    """
    Show current status of both client and server statistics if there
    is a connection.

    It gets the status of the server statistics from the WBEM server
    and the client statistics from the context and displays either a
    table or text representation of the status.

    If there is an issue with getting statistics information from the server,
    it displays detailed information about the server response.

    """

    # validate output format with default of table
    output_format = validate_output_format(context.output_format,
                                           ['TABLE', 'TEXT'])

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
        headers = ['Item', 'Status']
        rows = [['client statistics display', pywbemcli_stats_status],
                ['server statistics gathering', svr_status]]
        click.echo(format_table(rows, headers, "Statistics status"))
    else:
        click.echo("Statistics status: client={}; server={}".
                   format(pywbemcli_stats_status, svr_status))


def cmd_statistics_reset(context):
    """
    Reset the client statistics. This command does not impact the
    statistics retrieved from the server with ``statistics server-show``.
    It does reset the statistics kept in the pywbem client for server
    response time.
    """

    conn = context.pywbem_server.conn
    conn.statistics.reset()

    context.spinner_stop()
    click.echo("Pywbemcli statistics reset")


def cmd_statistics_show(context):
    """
    If the statistics are enabled for the client and the connection exits,
    display the statistics
    """

    conn = context.pywbem_server.conn

    context.spinner_stop()
    click.echo(context.format_statistics(conn.statistics, context))


def cmd_statistics_server_show(context):
    """
    If server statistics are enabled get them from the server and display.

    This command may fail if the WBEM server has not implemented the
    management of detailed statistics.
    """
    conn = context.pywbem_server.conn

    def avg_value(value_, num_ops):
        """
        Compute the average value from the value_ input and the number of
        operations.
        If the number of operations is 0, return 0

        Parameters:
          value_ (:class:`int` or :class:`py:float`):

          num_ops (:class:`int`):
            The number of operations executed

        Returns:
          Numeric containing the value / num_ops or
          0 if num_ops is 0.
        """
        if num_ops:
            return value_ / num_ops

        assert value_ == 0
        return 0

    def avg_time_ms(total_time, num_ops):
        """
        Return the average elapsed time of the operations in milliseconds.

        Parameters:
          total_time (:class:`CIMDateTime`):
            The total elapsed time of the operations, as an interval.

          num_ops (:class:`int`):
            The number of operations executed.

          Returns:
            :class:`int`: The average elapsed time of the operations in
            milliseconds.
        """
        assert isinstance(total_time, CIMDateTime)
        assert total_time.is_interval
        milliseconds = total_time.timedelta.total_seconds() * 1000
        avg = avg_value(milliseconds, num_ops)
        return avg

    conn = context.pywbem_server.conn
    wbem_server = context.pywbem_server.wbem_server
    output_fmt = validate_output_format(context.output_format, 'TABLE')

    objmgr = get_objmgr_inst(context)
    try:
        svr_status = objmgr[OBJMGR_STAT_PROPERTY_NAME]
    except KeyError:
        svr_status = "No property {}".format(OBJMGR_STAT_PROPERTY_NAME)
    except Error as er:
        svr_status = "Not settable {}".format(er)

    if isinstance(svr_status, six.string_types):
        raise click.ClickException("ObjectManager config setting not found {}".
                                   format(svr_status))

    if not svr_status:
        raise click.ClickException("WBEM server CIM_ObjectManager "
                                   "statistics off")

    # We must find the
    # namespace containing statistical data since apparently not clearly
    # documented in specs. Ex. Pegasus has in in root/cimv2 in test build
    namespaces = wbem_server.namespaces
    results = None
    stats_namespace = None
    for ns in namespaces:
        try:
            _ = conn.GetClass(CIMOM_STATISTICAL_DATA_CLASS, namespace=ns)
        except Error:
            continue
        try:
            results = conn.PyWbemcliEnumerateInstances(
                ClassName=CIMOM_STATISTICAL_DATA_CLASS,
                namespace=ns,
                LocalOnly=False,
                IncludeQualifiers=False,
                DeepInheritance=True,
                IncludeClassOrigin=False)
            stats_namespace = ns
            if results:
                break
        except Error:
            continue

    if not results:
        raise click.ClickException(
            "No WBEM server class {} or class returns no data on "
            "WBEM Server".
            format(CIMOM_STATISTICAL_DATA_CLASS))

    if context.verbose:
        click.echo("{} returns instances in namespace {}".
                   format(CIMOM_STATISTICAL_DATA_CLASS, stats_namespace))

    try:
        op_type_vm = ValueMapping.for_property(conn, stats_namespace,
                                               CIMOM_STATISTICAL_DATA_CLASS,
                                               'OperationType')

        results = conn.PyWbemcliEnumerateInstances(
            ClassName=CIMOM_STATISTICAL_DATA_CLASS,
            namespace=stats_namespace,
            LocalOnly=False,
            IncludeQualifiers=False,
            DeepInheritance=True,
            IncludeClassOrigin=False)
        if not results:
            raise click.ClickException(
                "WBEM server Class {} returns no data".
                format(CIMOM_STATISTICAL_DATA_CLASS))

        row_tuples = []
        for inst in results:
            # Only show lines that have a non-zero number of operations
            if inst['NumberOfOperations'] == 0:
                continue
            op_type_name = op_type_vm.tovalues(inst['OperationType'])
            # If op_type_name is other, get op_type_name from other property
            if op_type_name.lower() == 'other':
                op_type_name = inst['OtherOperationType']
            number_of_operations = inst['NumberOfOperations']

            avg_provider_time_ms = avg_time_ms(
                inst['ProviderElapsedTime'], number_of_operations)
            avg_cimom_time_ms = avg_time_ms(
                inst['CimomElapsedTime'], number_of_operations)
            # Note: The CimomElapsedTime property is explicitly described
            #       to be the time just in the CIMOM without provider time.
            #       Since we want to be able to relate that to the server time
            #       in the client statistics, we calculate the server time
            #       as CIMOM time plus provider time.
            avg_server_time_ms = avg_cimom_time_ms + avg_provider_time_ms

            avg_request_size = avg_value(inst['RequestSize'],
                                         number_of_operations)
            avg_response_size = avg_value(inst['ResponseSize'],
                                          number_of_operations)

            row_tuples.append(
                (op_type_name, number_of_operations, avg_server_time_ms,
                 avg_provider_time_ms, avg_request_size, avg_response_size))

        # Index of the items in the row tuples
        operation_idx = 0
        count_idx = 1
        server_time_idx = 2
        provider_time_idx = 3
        request_size_idx = 4
        response_size_idx = 5

        # Sort the rows by descending server time.
        # Note: Because the server time first needs to be calculated which may
        #       be WBEM server dependent, the sorting is performed as a
        #       separate step.
        rows = []
        for row_tuple in sorted(row_tuples,
                                key=lambda tup: tup[server_time_idx],
                                reverse=True):
            rows.append(
                (row_tuple[operation_idx], row_tuple[count_idx],
                 "{:.3f}".format(row_tuple[server_time_idx]),
                 "{:.3f}".format(row_tuple[provider_time_idx]),
                 "{:.0f}".format(row_tuple[request_size_idx]),
                 "{:.0f}".format(row_tuple[response_size_idx])))

        headers = ['Operation', 'Count', 'Server Time\n[ms]',
                   'Provider Time\n[ms]', 'Request Size\n[B]',
                   'Response Size\n[B]']

        context.spinner_stop()
        click.echo(format_table(
            rows, headers,
            title='Server statistics',
            table_format=output_fmt))
    except Error as er:
        raise click.ClickException("Statistics retrieval from WBEM server "
                                   "failed. Exception {}".
                                   format(er))
