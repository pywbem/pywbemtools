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
pybemcli context object. This is the common object for click command calls for
pywbemcli context information.

It contains data that is set in the top level and used in command calls

This object is attached to the Click Context in pywbemcli.py
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import click
import click_spinner

from ._common import format_table


class ContextObj(object):  # pylint: disable=useless-object-inheritance
    """
        Manage the pywbemcli context that is carried within the Click
        context object in the obj parameter. This is the object that
        communicates between the cli commands and command groups. It contains
        the information that is common to the multiple click commands
    """

    spinner_envvar = 'PYWBEMCLI_SPINNER'

    # pylint: disable=unused-argument
    def __init__(self, pywbem_server, output_format, use_pull,
                 pull_max_cnt, timestats, log, verbose, pdb,
                 deprecation_warnings, connections_repo):

        self._pywbem_server = pywbem_server
        self._output_format = output_format
        self._use_pull = use_pull
        self._pull_max_cnt = pull_max_cnt
        self._timestats = timestats
        self._log = log
        self._verbose = verbose
        self._pdb = pdb
        self._deprecation_warnings = deprecation_warnings
        self._connections_repo = connections_repo

        self._spinner_enabled = None  # Deferred init in getter
        self._spinner_obj = click_spinner.Spinner()
        self._conn = None
        self._wbem_server = None

    def __repr__(self):
        return 'ContextObj(at {:08x}, pywbem_server={!r}, outputformat={}, ' \
               'use_pull={}, pull_max_cnt={}, timestats={}, verbose={}, ' \
               'spinner_enabled={}' \
               .format(id(self), self.pywbem_server, self.output_format,
                       self.use_pull, self.pull_max_cnt, self.timestats,
                       self.verbose, self.spinner_enabled)

    @property
    def output_format(self):
        """
        :term:`string`: String defining the output format requested.  This may
        be None meaning that the default format should be used or may be
        one of the values in the TABLE_FORMATS variable.
        """
        return self._output_format

    @property
    def timestats(self):
        """
        :term:`string`: Output format to be used.
        """
        return self._timestats

    @property
    def use_pull(self):
        """
        :term:`string`: Choice of whether pull, traditional or either type
        of operation is to be used for the instance enumerates, references,
        or associator commands.
        """
        return self._use_pull

    @property
    def pull_max_cnt(self):
        """
        :term:`string`: Maximum number of objects to be returne for pull op.
        """
        return self._pull_max_cnt

    @property
    def log(self):
        """
        :term:`string`: log definition from cmd line
        """
        return self._log

    @property
    def pdb(self):
        """
        bool: Indicates whether to break in the debugger.
        """
        return self._pdb

    @property
    def deprecation_warnings(self):
        """
        bool: Indicates whether to enable deprecation warnings.
        """
        return self._deprecation_warnings

    @property
    def connections_repo(self):
        """
        :class:`ConnectionRepository` instance defining at least the filename
        of the Connections repository. The connections_repo may not be
        loaded at this point.
        """
        return self._connections_repo

    @property
    def conn(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMConnection to be used for requests.
        This property uses the wbem_server property to activate the
        conn and wbem_server. The connection is not activated unless
        a command requiring the webem server is executed.  This allows other
        commands like connection to execute without testing whether or not the
        WBEM server exists.
        """
        # The conn property is created in wbem_server and retained here.
        if self._conn:
            return self._conn

        self._conn = self.wbem_server.conn
        return self._conn

    @property
    def wbem_server(self):
        """
        :class:`~pywbem.WBEMServer` WBEMServer instance to be used for
        requests This is maintained in the pywbem_server object as
        _pywbem_server. This and/or the conn property are executed before
        any operation that is to contact the server.  This property enables any
        server characteristics. This is a passthrough for the wbem_server
        property maintained in self._pywbem_server
        """
        # If no server defined, do not try to connect. This allows
        # commands like help, connection new, list to execute without
        # a target server defined.
        if self._pywbem_server:  # pylint: disable=no-else-return
            # If wbem_server not initialized, initialize it.
            if self._pywbem_server.wbem_server is None:
                # get the password if it is required.  This may involve a
                # prompt.
                # TODO there are two creates and also, since all the inputs
                # are self, why do that here
                self._pywbem_server.get_password(self)
                self._pywbem_server.create_connection(
                    log=self.log,
                    use_pull=self.use_pull,
                    timestats=self.timestats,
                    verbose=self.verbose)
                if self._conn and self.timestats:  # Enable stats gathering
                    self.conn.statistics.enable()
                self._wbem_server = self._pywbem_server.wbem_server
            return self._pywbem_server.wbem_server
        else:
            raise click.ClickException(
                'No server specified for a command that requires a WBEM '
                'server. To specify a server, use the "--server", '
                '"--mock-server", or "--name" general options, or set the '
                'corresponding environment variables, or in interactive mode '
                'use "connection select"')

    @property
    def pywbem_server(self):
        """
        :class:`~pywbem.WBEMServer` WBEMServer instance to be used for
        requests.
        """
        return self._pywbem_server

    @property
    def spinner_enabled(self):
        """
        :class:`py:bool`: Indicates and controls whether the spinner is enabled.

        If the spinner is enabled, subcommands will display a spinning wheel
        while waiting for completion.

        This attribute can be modified.

        The initial state of the spinner is enabled, but it can be disabled by
        setting the {0} environment variable to 'false', '0', or the empty
        value.
        """.format(self.spinner_envvar)

        # Deferred initialization
        if self._spinner_enabled is None:
            value = os.environ.get(self.spinner_envvar, None)
            if value is None:
                # Default if not set
                self._spinner_enabled = True
            elif value == '0' or value == '' or value.lower() == 'false':
                self._spinner_enabled = False
            else:
                self._spinner_enabled = True

        return self._spinner_enabled

    @spinner_enabled.setter
    def spinner_enabled(self, enabled):
        """Setter method; for a description see the getter method."""
        # pylint: disable=attribute-defined-outside-init
        self._spinner_enabled = enabled

    def spinner_start(self):
        """
        Start the spinner, if the spinner is enabled.
        """
        if self.spinner_enabled:
            self._spinner_obj.start()

    def spinner_stop(self):
        """
        Stop the spinner, if the spinner is enabled.
        """
        if self.spinner_enabled:
            self._spinner_obj.stop()

    @property
    def verbose(self):
        """
        :bool:` '~click.verbose.
        """
        return self._verbose

    def set_connection(self, connection):
        """ Set the connection parameter as the current connection object and
            establish the new connection
        """
        self._pywbem_server = connection

    def execute_cmd(self, cmd):
        """
        Call the cmd executor defined by cmd with the spinner. If the
        WBEM server object has not been created it is created so that this wbem
        server can be used for interactive commands.

        This method is called by every command execution to setup and
        execute the command. Thus, each command has the line similar to:

        context.execute_cmd(lambda: cmd_instance_query(context, query, options))
        """
        # Verbose and env var PYWBEMCLI_DIAGNOSTICS displays the click
        # interpetation of the command and parameters from click context
        # This is a diagnostic for developer internal use so the
        # env variable is not documented.
        if self.verbose and os.getenv('PYWBEMCLI_DIAGNOSTICS'):
            ctx = click.get_current_context()
            click.echo('COMMAND="{}", params={!r}'.format(ctx.info_name,
                                                          ctx.params))
            display_click_context_parents(display_attrs=True)

        if not self.pdb:
            self.spinner_start()
        if self.pdb:
            import pdb  # pylint: disable=import-outside-toplevel
            pdb.set_trace()
        try:
            cmd()
        finally:
            if not self.pdb:
                self.spinner_stop()

            # Issue statistics if required. Note that we use _conn in order
            # not to create the connection if not created.
            if self.timestats and self._conn:
                click.echo(self.format_statistics(self.conn.statistics))

    def format_statistics(self, statistics):
        """
        table formatted output of statistics
        """

        def format_float3(avg, min_, max_):
            """Display float statistics with 3 places"""
            if avg == min_ == max_:
                return '{0:.3f}'.format(avg)
            return '{0:.3f}/{1:.3f}/{2:.3f}'.format(avg, min_, max_)

        def format_float0(avg, min_, max_):
            """Display float statistics with 0 places"""
            if avg == min_ == max_:
                return '{0:.0f}'.format(avg)
            return '{0:.0f}/{1:.0f}/{2:.0f}'.format(avg, min_, max_)

        snapshot = sorted(statistics.snapshot(),
                          key=lambda item: item[1].avg_time,
                          reverse=True)

        # Test to see if any server time is non-zero
        include_svr = False
        for name, stats in snapshot:  # pylint: disable=unused-variable
            # TODO: clean up pywbem stats so this is in pywbem, not here
            if stats._server_time_stored:  # pylint: disable=protected-access
                include_svr = True

        # build list of column names
        hdr = ['Count', 'Exc', 'Time']
        if include_svr:
            hdr.append('SvrTime')
        hdr.extend(['ReqLen', 'ReplyLen', 'Operation'])

        # build table rows from snapshot of OperationStatistics
        rows = []
        for name, stats in snapshot:  # pylint: disable=unused-variable
            time = format_float3(stats.avg_time,
                                 stats.min_time,
                                 stats.max_time)
            req_len = format_float0(stats.avg_request_len,
                                    stats.min_request_len,
                                    stats.max_request_len)
            reply_len = format_float0(stats.avg_reply_len,
                                      stats.min_reply_len,
                                      stats.max_reply_len)
            if include_svr:
                svrtime = format_float3(stats.avg_server_time,
                                        stats.min_server_time,
                                        stats.max_server_time)
                row = [stats.count, stats.exception_count, time, svrtime,
                       req_len, reply_len, stats.name]
            else:
                row = [stats.count, stats.exception_count, time,
                       req_len, reply_len, stats.name]
            rows.append(row)

        # only add table description if verbose on.
        if self.verbose:
            title = 'Statistics: Time in sec. Time, ReqLen, etc are single ' \
                    'value if average/min/max are the same'
        else:
            title = None

        click.echo(format_table(rows, hdr, title=title))

    def connect_wbem_server(self):
        """
        If the wbem server has not been connected yet, connect it. The
        wbemserver object is saved both in the context and as a GLOBAL
        This GLOBAL is used to determine that the server has been connected.
        TODO: FUTURE Rather than a global, we should be the wbemserver into the
        parent probably.

        Both the WBEMConnection and WBEMServer objects are established
        at this point since the cost of doing the WBEMServer object is low.
        The existence of the WBEMServer object in the GLOBALS is the flag that
        this server connection has been established already.

        TODO: FUTURE - We should probably move this logic to the first place a
        connection is actually established so that if we have not-password
        commands in the environment they do not force the password request.
        Logical would be the first time the conn or wbem_server property is
        used in pywbem_server.

        """
        # TODO: FUTURE investigate putting this into parent context

        # If no server defined, do not try to connect. This allows
        # commands like help, connection new, select to execute without
        # a target server defined.
        if self._pywbem_server and self._pywbem_server.wbem_server is None:
            # get the password if it is required.  This may involve a
            # prompt.
            self._pywbem_server.get_password(self)
            self._pywbem_server.create_connection(
                log=self.log,
                use_pull=self.use_pull,
                timestats=self.timestats,
                verbose=self.verbose)

    @staticmethod
    def update_root_click_context(ctx_obj):
        """
        Method to update the click root context with a new context
        object.  This makes the values in this context universal for all
        future commands within an interactive session.
        This is a static method and gets the current click context and
        root context from click itself.
        """
        ctx = click.get_current_context()
        root = ctx.find_root()
        root.obj = ctx_obj


#
#   Debug tools to help understandingthe click context.  These are only
#   to help analyzing the click_context (ctx) and primarily in the
#   interactive mode whene several levels of click context can exist
#
def display_click_context(ctx, msg=None, display_attrs=True):
    """
    Debug function displays attributes of click context
    This is a diagnostic for developer use
    """

    attrs = vars(ctx)
    if not msg:
        msg = "CLICK_CONTEXT"
    if not display_attrs:
        click.echo(ctx.obj)
    else:
        click.echo('{0} {1}, attrs: {2}'.format(
            msg, ctx,
            '\n    '.join('{0}: {1}'.format(i, v) for (i, v) in attrs.items())))


def display_click_context_parents(display_attrs=False):
    """
    Display the current click context and its all of its parents.
    This is a diagnostic for developer use
    """
    level = 0
    ctx = click.get_current_context()
    disp_ctx = ctx.parent
    while disp_ctx is not None:
        display_click_context(disp_ctx, msg='level {}'.format(level),
                              display_attrs=display_attrs)
        level += -1
        disp_ctx = disp_ctx.parent
