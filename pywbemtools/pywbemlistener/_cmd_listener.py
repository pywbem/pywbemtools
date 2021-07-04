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
Click definitions for the pywbemlistener commands.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import sys
import os
import subprocess
import signal
import atexit
import threading
import argparse
import importlib
from time import sleep
from datetime import datetime
import click
import psutil
import six
from nocasedict import NocaseDict

from pywbem import WBEMListener, ListenerError

from .._click_extensions import PywbemtoolsCommand, CMD_OPTS_TXT
from .._options import add_options, help_option, validate_required_arg
from .._output_formatting import format_table

from . import _config
from .pywbemlistener import cli

# Signals used for having the 'run' command signal startup completion
# back to its parent 'start' process.
# The default handlers for these signals are replaced.
# The success signal can be any signal that can be handled.
# In order to handle keyboard interrupts during password prompt correctly,
# the failure signal must be SIGINT.
try:
    # Unix/Linux/macOS
    # pylint: disable=no-member
    SIGNAL_RUN_STARTUP_SUCCESS = signal.SIGUSR1
except AttributeError:
    # native Windows
    # pylint: disable=no-member
    SIGNAL_RUN_STARTUP_SUCCESS = signal.SIGBREAK
SIGNAL_RUN_STARTUP_FAILURE = signal.SIGINT

# Status and condition used to communicate the startup completion status of the
# 'run' process between the signal handlers and other functions in the
# 'start' process.
RUN_STARTUP_STATUS = None
RUN_STARTUP_COND = threading.Condition()

# Timeout in seconds for the 'run' command starting up. This timeout
# also ends a possible prompt for the password of the private key file.
RUN_STARTUP_TIMEOUT = 60

DEFAULT_LISTENER_PORT = 25989
DEFAULT_LISTENER_SCHEME = 'https'
DEFAULT_INDI_FORMAT = '{dt} {h} {c} {p}'

LISTEN_OPTIONS = [
    click.option('-p', '--port', type=int, metavar='PORT',
                 required=False, default=DEFAULT_LISTENER_PORT,
                 help=u'The port number the listener will open to receive '
                 'indications. This can be any available port. '
                 'Default: {}'.format(DEFAULT_LISTENER_PORT)),
    click.option('-s', '--scheme', type=click.Choice(['http', 'https']),
                 metavar='SCHEME',
                 required=False, default=DEFAULT_LISTENER_SCHEME,
                 help=u'The scheme used by the listener (http, https). '
                 'Default: {}'.format(DEFAULT_LISTENER_SCHEME)),
    click.option('-c', '--certfile', type=str, metavar='FILE',
                 required=False, default=None,
                 envvar=_config.PYWBEMLISTENER_CERTFILE_ENVVAR,
                 help=u'Path name of a PEM file containing the certificate '
                 'that will be presented as a server certificate during '
                 'SSL/TLS handshake. Required when using https. '
                 'The file may in addition contain the private key of the '
                 'certificate. '
                 'Default: EnvVar {ev}, or no certificate file.'.
                 format(ev=_config.PYWBEMLISTENER_CERTFILE_ENVVAR)),
    click.option('-k', '--keyfile', type=str, metavar='FILE',
                 required=False, default=None,
                 envvar=_config.PYWBEMLISTENER_KEYFILE_ENVVAR,
                 help=u'Path name of a PEM file containing the private key '
                 'of the server certificate. '
                 'Required when using https and when the certificate file '
                 'does not contain the private key. '
                 'Default: EnvVar {ev}, or no key file.'.
                 format(ev=_config.PYWBEMLISTENER_KEYFILE_ENVVAR)),
    click.option('--indi-call', type=str, metavar='MODULE.FUNCTION',
                 required=False, default=None,
                 help=u'Call a Python function for each received indication. '
                 'Invoke with --help-call for details on the function '
                 'interface. '
                 'Default: No function is called.'),
    click.option('-d', '--indi-display', is_flag=True,
                 required=False, default=False,
                 help=u'Display received indications on stdout. '
                 'The format can be modified using the --indi-format option. '
                 'Default: Not displayed.'),
    click.option('--indi-file', type=str, metavar='FILE',
                 required=False, default=None,
                 help=u'Append received indications to a file. '
                 'The format can be modified using the --indi-format option. '
                 'Default: Not appended.'),
    click.option('--indi-format', type=str, metavar='FORMAT',
                 required=False, default=DEFAULT_INDI_FORMAT,
                 help=u'Sets the format to be used when displaying received '
                 'indications. '
                 'Invoke with --help-format for details on the format '
                 'specification. '
                 'Default: "{dif}".'.format(dif=DEFAULT_INDI_FORMAT)),
    click.option('--help-format', is_flag=True,
                 required=False, default=False, is_eager=True,
                 help=u'Show help message for the format specification used '
                 'with the --indi-format option and exit.'),
    click.option('--help-call', is_flag=True,
                 required=False, default=False, is_eager=True,
                 help=u'Show help message for calling a Python function for '
                 'each received indication when using the --indi-call option '
                 'and exit.'),
]


class ListenerProperties(object):
    """
    The properties of a running named listener.
    """

    def __init__(self, name, port, scheme, certfile, keyfile,
                 indi_call, indi_display, indi_file, indi_format,
                 logfile, pid, created):
        self._name = name
        self._port = port
        self._scheme = scheme
        self._certfile = certfile
        self._keyfile = keyfile
        self._indi_call = indi_call
        self._indi_display = indi_display
        self._indi_file = indi_file
        self._indi_format = indi_format
        self._logfile = logfile
        self._pid = pid
        self._created = created

    def show_row(self):
        """Return a tuple of the properties for 'show' command"""
        return (
            self.name,
            str(self.port),
            self.scheme,
            self.certfile,
            self.keyfile,
            self.indi_call,
            self.indi_display,
            self.indi_file,
            self.logfile,
            str(self.pid),
            self.created.strftime("%Y-%m-%d %H:%M:%S"),
        )

    @staticmethod
    def show_headers():
        """Return a tuple of the header labels for 'show' command"""
        return (
            'Name',
            'Port',
            'Scheme',
            'Certificate file',
            'Key file',
            'Indication call',
            'Indication display',
            'Indication file',
            'Log file',
            'PID',
            'Created',
        )

    def list_row(self):
        """Return a tuple of the properties for 'list' command"""
        return (
            self.name,
            str(self.port),
            self.scheme,
            str(self.pid),
            self.created.strftime("%Y-%m-%d %H:%M:%S"),
        )

    @staticmethod
    def list_headers():
        """Return a tuple of the header labels for 'list' command"""
        return (
            'Name',
            'Port',
            'Scheme',
            'PID',
            'Created',
        )

    @property
    def name(self):
        """string: Name of the listener"""
        return self._name

    @property
    def port(self):
        """int: Port number of the listener"""
        return self._port

    @property
    def scheme(self):
        """string: Scheme of the listener"""
        return self._scheme

    @property
    def certfile(self):
        """string: Path name of certificate file of the listener"""
        return self._certfile

    @property
    def keyfile(self):
        """string: Path name of key file of the listener"""
        return self._keyfile

    @property
    def indi_call(self):
        """string: Call function MODULE.FUNCTION for each received indication"""
        return self._indi_call

    @property
    def indi_display(self):
        """bool: Display each received indication in a format"""
        return self._indi_display

    @property
    def indi_file(self):
        """string: Append each received indication to a file in a format"""
        return self._indi_file

    @property
    def indi_format(self):
        """string: Set format of indication"""
        return self._indi_format

    @property
    def logfile(self):
        """string: Path name of log file"""
        return self._logfile

    @property
    def pid(self):
        """int: Process ID of the listener"""
        return self._pid

    @property
    def created(self):
        """datetime: Point in time when the listener process was created"""
        return self._created


@cli.command('run', cls=PywbemtoolsCommand, options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False)
@add_options(LISTEN_OPTIONS)
@add_options(help_option)
@click.pass_obj
def listener_run(context, name, **options):
    """
    Run as a named WBEM indication listener.

    Run this command as a named WBEM indication listener until it gets
    terminated, e.g. by a keyboard interrupt, break signal (e.g. kill), or the
    `pywbemlistener stop` command.

    A listener with that name must not be running, otherwise the command fails.

    Examples:

      pywbemlistener run lis1
    """
    if show_help_options(options):
        return
    validate_required_arg(name, 'NAME')
    context.execute_cmd(lambda: cmd_listener_run(context, name, options))


@cli.command('start', cls=PywbemtoolsCommand, options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=False)
@add_options(LISTEN_OPTIONS)
@add_options(help_option)
@click.pass_obj
def listener_start(context, name, **options):
    """
    Start a named WBEM indication listener in the background.

    A listener with that name must not be running, otherwise the command fails.

    A listener is identified by its hostname or IP address and a port number.
    It can be started with any free port.

    Examples:

      pywbemlistener start lis1
    """
    if show_help_options(options):
        return
    validate_required_arg(name, 'NAME')
    context.execute_cmd(lambda: cmd_listener_start(context, name, options))


@cli.command('stop', cls=PywbemtoolsCommand, options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True)
@add_options(help_option)
@click.pass_obj
def listener_stop(context, name):
    """
    Stop a named WBEM indication listener.

    The listener will shut down gracefully.

    A listener with that name must be running, otherwise the command fails.

    Examples:

      pywbemlistener stop lis1
    """
    context.execute_cmd(lambda: cmd_listener_stop(context, name))


@cli.command('show', cls=PywbemtoolsCommand, options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True)
@add_options(help_option)
@click.pass_obj
def listener_show(context, name):
    """
    Show a named WBEM indication listener.

    A listener with that name must be running, otherwise the command fails.

    Examples:

      pywbemlistener stop lis1
    """
    context.execute_cmd(lambda: cmd_listener_show(context, name))


@cli.command('list', cls=PywbemtoolsCommand, options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def listener_list(context):
    """
    List the currently running named WBEM indication listeners.

    This is done by listing the currently running `pywbemlistener run`
    commands.
    """
    context.execute_cmd(lambda: cmd_listener_list(context))


################################################################
#
#   Common methods for The action functions for the listener click group
#
###############################################################


def get_logfile(logdir, name):
    """
    Return path name of run log file, or None if no log directory is specified.

    Parameters:
      logdir (string): Path name of log directors, or None.
      name (string): Listener name.
    """
    if logdir is None:
        return None
    return os.path.join(logdir, 'pywbemlistener_{}.log'.format(name))


def get_listeners(name=None):
    """
    List the running listener processes, or the running listener process(es)
    with the specified name.

    Note that in case of the 'run' command, it is possible that this
    function is called with a name and finds two listener processes with that
    name: A previosly started one, and the one that is about to run now.
    Both will be returned so this situation can be handled by the caller.

    Returns:
      list of ListenerProperties
    """
    ret = []
    for p in psutil.process_iter():
        try:
            cmdline = p.cmdline()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            # Ignore processes we cannot access
            continue
        for i, item in enumerate(cmdline):
            if item.endswith('pywbemlistener'):
                listener_index = i
                break
        else:
            # Ignore processes that are not 'pywbemlistener'
            continue
        listener_args = cmdline[listener_index + 1:]  # After 'pywbemlistener'
        args = parse_listener_args(listener_args)
        if args:
            if name is None or args.name == name:
                # pylint: disable=no-member
                # Note: This is a workaround for Pylint raising no-member on
                # Python 3.9 (see issue #1001)
                logfile = get_logfile(args.logdir, args.name)
                lis = ListenerProperties(
                    name=args.name, port=args.port, scheme=args.scheme,
                    certfile=args.certfile, keyfile=args.keyfile,
                    indi_call=args.indi_call, indi_display=args.indi_display,
                    indi_file=args.indi_file, indi_format=args.indi_format,
                    logfile=logfile,
                    pid=p.pid, created=datetime.fromtimestamp(p.create_time()))
                # pylint: enable=no-member
                # Note: End of workaround
                ret.append(lis)
    return ret


def is_parent_start():
    """
    Determine whether the parent process is a 'start' command, and
    return its PID if so. Otherwise, return None.

    This is used by the 'run' command to find out whether it is
    executed directly by a user, vs. launched by the 'start' command,
    so it can signal startup completion to the 'start' command.

    Returns:
      int: PID of parent process, if it is 'start', otherwise None.
    """
    ppid = os.getppid()
    pps = psutil.Process(ppid)

    try:
        cmdline = pps.cmdline()
    except (psutil.AccessDenied, psutil.ZombieProcess):
        # Ignore processes we cannot access
        return None

    seen_pywbemlistener = False
    for item in cmdline:
        if item.endswith('pywbemlistener'):
            seen_pywbemlistener = True
            continue
        if seen_pywbemlistener and item == 'start':
            break
    else:
        # Ignore processes that are not 'pywbemlistener [opts] start'
        return None

    return ppid


def prepare_startup_completion():
    """
    In the 'start' command, prepare for a later use of
    wait_startup_completion() by setting up the necessary signal handlers.
    """
    signal.signal(SIGNAL_RUN_STARTUP_SUCCESS, success_signal_handler)
    signal.signal(SIGNAL_RUN_STARTUP_FAILURE, failure_signal_handler)


def success_signal_handler(sig, frame):
    # pylint: disable=unused-argument
    """
    Signal handler in 'start' process for the signal indicating
    success of startup completion of the 'run' child process.
    """
    # pylint: disable=global-statement
    global RUN_STARTUP_STATUS, RUN_STARTUP_COND

    if _config.VERBOSE_PROCESSES_ENABLED:
        print("Start process: Handling success signal ({}) from run process".
              format(sig))

    RUN_STARTUP_STATUS = 'success'
    with RUN_STARTUP_COND:
        RUN_STARTUP_COND.notify()


def failure_signal_handler(sig, frame):
    # pylint: disable=unused-argument
    """
    Signal handler in 'start' process for the signal indicating
    failure of startup completion of the 'run' child process.
    """
    # pylint: disable=global-statement
    global RUN_STARTUP_STATUS, RUN_STARTUP_COND

    if _config.VERBOSE_PROCESSES_ENABLED:
        print("Start process: Handling failure signal ({}) from run process".
              format(sig))

    RUN_STARTUP_STATUS = 'failure'
    with RUN_STARTUP_COND:
        RUN_STARTUP_COND.notify()


def wait_startup_completion(child_pid):
    """
    In the 'start' command, wait for the 'run' child process
    to either successfully complete its startup or to fail its startup.

    Returns:
      int: Return code indicating whether the child started up successfully (0)
        or failed its startup (1).
    """
    # pylint: disable=global-statement
    global RUN_STARTUP_STATUS, RUN_STARTUP_COND

    if _config.VERBOSE_PROCESSES_ENABLED:
        print("Start process: Waiting for run process {} to complete startup".
              format(child_pid))

    RUN_STARTUP_STATUS = 'failure'
    with RUN_STARTUP_COND:
        rc = RUN_STARTUP_COND.wait(RUN_STARTUP_TIMEOUT)

    # Before Python 3.2, wait() always returns None. Since 3.2, it returns
    # a boolean indicating whether the timeout expired (False) or the
    # condition was triggered (True).
    if rc is None or rc is True:
        status = RUN_STARTUP_STATUS
    else:
        # Only since Python 3.2
        status = 'timeout'

    if status == 'success':
        if _config.VERBOSE_PROCESSES_ENABLED:
            print("Start process: Startup of run process {} succeeded".
                  format(child_pid))
        return 0

    if status == 'timeout':
        click.echo("Timeout")

    # The 'run' child process may still be running, or already a
    # zombie, or no longer exist. If it still is running, the likely cause is
    # that it was in a password prompt for the keyfile password that was not
    # entered.

    sleep(0.5)  # Give it some time to finish by itself before we clean it up

    if _config.VERBOSE_PROCESSES_ENABLED:
        print("Start process: Startup of run process {} failed".
              format(child_pid))
    child_exists = False
    try:
        child_ps = psutil.Process(child_pid)
        child_status = child_ps.status()
        if child_status != psutil.STATUS_ZOMBIE:
            child_exists = True
    except (psutil.NoSuchProcess, psutil.ZombieProcess):
        # No need to clean up anything in these cases.
        pass

    if child_exists:
        if _config.VERBOSE_PROCESSES_ENABLED:
            print("Start process: Cleaning up run process {} and status {}".
                  format(child_pid, child_status))
        try:
            child_ps.terminate()
            child_ps.wait()
        except (IOError, OSError) as exc:
            raise click.ClickException(
                "Cannot clean up 'run' child process with PID {}: {}: {}".
                format(child_pid, type(exc), exc))
    return 1


def run_exit_handler(start_pid, log_fp):
    """
    Exit handler that gets etablished for the 'run' command.

    This exit handler signals a failed startup of the 'run' command
    to the 'start' process, if it still exists. If the 'start'
    process no longer exists, this means that the startup of the 'run'
    command succeeded earlier, and it is now terminated by some means.

    In addition, it closes the log_fp log file.
    """
    if _config.VERBOSE_PROCESSES_ENABLED:
        print("Run process: Exit handler sends failure signal ({}) to start "
              "process {}".
              format(SIGNAL_RUN_STARTUP_FAILURE, start_pid))
    try:
        os.kill(start_pid, SIGNAL_RUN_STARTUP_FAILURE)  # Sends the signal
    except OSError:
        # The original start parent no longer exists -> the earlier startup
        # succeeded.
        pass

    if log_fp:
        print("Closing 'run' output log file at {}".format(datetime.now()))
        log_fp.close()


class DisplayDict(NocaseDict):
    # pylint: disable=too-many-ancestors
    """
    Dictionary with a string representation that uses name=value format.
    """

    def __str__(self):
        items = ['{}={!r}'.format(k, v) for k, v in self.items()]
        return ' '.join(items)


def format_indication(indication, host, indi_format=None):
    """
    Return a string that contains the indication formatted according to the
    given format.
    """
    dt = datetime.now()
    try:
        dt = dt.astimezone()
    except TypeError:
        # Below Python 3.6, it cannot determine the local timezone, and its
        # tzinfo argument is required.
        pass
    p_dict = DisplayDict()
    for pn, p in indication.properties.items():
        p_dict[pn] = p.value
    format_kwargs = dict(
        dt=dt,
        dt_tzname=dt.tzname() or '',
        h=host,
        i=indication,
        c=indication.classname,
        p=p_dict,
    )
    if indi_format is None:
        indi_format = DEFAULT_INDI_FORMAT
    indi_str = indi_format.format(**format_kwargs)
    return indi_str


def show_help_format():
    """
    Display help for the format specification used with the --indi-format
    option.
    """
    print("""
Help for the format specification with option:  --indi-format FORMAT

FORMAT is a new-style format string that can use the following keyword args:

* 'dt' - datetime object of the time the listener received the indication, in
  local time. The object is timezone-aware on Python 3.6 or higher.
* 'dt_tzname' - timezone name of the datetime object if timezone-aware, else
  the empty string.
* 'h' - Host name or IP address of the host that sent the indication
* 'i' - pywbem.CIMInstance object with the indication instance
* 'c' - CIM classname of the indication instance
* 'p' - Case-insensitive dictionary of the indication properties, displayed
  as blank-separated name=value items

Examples:

--indi-format '{dt} {c} {p}'
2021-05-13 17:51:05.831117+02:00 CIM_AlertIndication Severity='high' \
SequenceNumber='0'

--indi-format '{dt} {h} {c}: Severity={p[severity]}'
2021-05-13 17:51:05.831117+02:00 127.0.0.1 CIM_AlertIndication: Severity=high
""")


def show_help_call():
    """
    Display help for calling a Python function for each received indication
    when using the --indi-call option.
    """
    print("""
Help for calling a Python function with option:  --indi-call MODULE.FUNCTION

MODULE must be a module name or a dotted package name in the module search
path, e.g. 'mymodule' or 'mypackage.mymodule'.

The current directory is added to the front of the Python module search path,
if needed. Thus, the module can be a single module file in the current
directory, for example:

    ./mymodule.py

or a module in a package in the current directory, for example:

    ./mypackage/__init__.py
    ./mypackage/mymodule.py

FUNCTION must be a function in that module with the following interface:

    def func(indication, host)

Parameters:

* 'indication' is a 'pywbem.CIMInstance' object representing the CIM indication
  that has been received. Its 'path' attribute is None.

* 'host' is a string with the host name or IP address of the indication sender
  (typically a WBEM server).

The return value of the function will be ignored.

Exceptions raised when importing the module cause the 'pywbemlistener run'
command to terminate with an error. Exceptions raised by the function when
it is called cause an error message to be displayed.
""")


def show_help_options(options):
    """
    Show the help messages for the --help-... options, if specified.

    Returns:
      bool: Indicates whether help was shown.
    """
    ret = False
    if options['help_call']:
        show_help_call()
        ret = True
    if options['help_format']:
        show_help_format()
        ret = True
    return ret


class SilentArgumentParser(argparse.ArgumentParser):
    """
    argparse.ArgumentParser subclass that silences any errors and exit and
    just raises them as SystemExit.
    """

    def error(self, message=None):
        """Called for usage errors detected by the parser"""
        raise SystemExit(2)

    def exit(self, status=0, message=None):
        """Not sure when this is called"""
        raise SystemExit(status)


def parse_listener_args(listener_args):
    """
    Parse the command line arguments of a process. If it is a listener process
    return its parsed arguments (after the 'pywbemlistener' command); otherwise
    return None.
    """

    parser = SilentArgumentParser()

    # Note: The following options must ne in sync with the Click general options
    parser.add_argument('--output-format', '-o', type=str, default=None)
    parser.add_argument('--logdir', '-l', type=str, default=None)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--pdb', action='store_true', default=False)
    parser.add_argument('--warn', default=False, action='store_true')

    parser.add_argument('run', type=str, default=None)
    parser.add_argument('name', type=str, default=None)

    # Note: The following options must ne in sync with the Click command options
    parser.add_argument('--port', '-p', type=int,
                        default=DEFAULT_LISTENER_PORT)
    parser.add_argument('--scheme', '-s', type=str,
                        default=DEFAULT_LISTENER_SCHEME)
    parser.add_argument('--certfile', type=str, default=None)
    parser.add_argument('--keyfile', type=str, default=None)
    parser.add_argument('--indi-call', type=str, default=None)
    parser.add_argument('--indi-display', '-d', action='store_true',
                        default=False)
    parser.add_argument('--indi-file', type=str, default=None)
    parser.add_argument('--indi-format', type=str, default=None)

    try:
        parsed_args = parser.parse_args(listener_args)
    except SystemExit:
        # Invalid arguments
        return None

    if parsed_args.run != 'run':
        return None

    return parsed_args


def run_term_signal_handler(sig, frame):
    # pylint: disable=unused-argument
    """
    Signal handler for the 'run' command that gets called for the
    SIGTERM signal, i.e. when the 'run' process gets terminated by
    some means.

    Ths handler ensures that the main loop of the the 'run' command
    gets control and can gracefully stop the listener.
    """
    if _config.VERBOSE_PROCESSES_ENABLED:
        print("Run process: Received termination signal ({})".format(sig))
    raise SystemExit(1)


def transpose(headers, rows):
    """
    Return transposed headers and rows (i.e. switch columns and rows).
    """
    ret_headers = ['Attribute', 'Value']
    ret_rows = []
    for header in headers:
        ret_row = [header]
        ret_rows.append(ret_row)
    for row in rows:
        assert len(headers) == len(row)
        for i, col in enumerate(row):
            ret_rows[i].append(col)
    return ret_headers, ret_rows


def display_show_listener(listener, table_format):
    """
    Display a listener for the 'show' command.
    """
    headers = ListenerProperties.show_headers()
    rows = [listener.show_row()]
    headers, rows = transpose(headers, rows)
    table = format_table(
        rows, headers, table_format=table_format,
        sort_columns=None, hide_empty_cols=None, float_fmt=None)
    click.echo(table)


def display_list_listeners(listeners, table_format):
    """
    Display listeners for the 'list' command.
    """
    headers = ListenerProperties.list_headers()
    rows = []
    for lis in listeners:
        rows.append(lis.list_row())
    table = format_table(
        rows, headers, table_format=table_format,
        sort_columns=None, hide_empty_cols=None, float_fmt=None)
    click.echo(table)


################################################################
#
#   Common methods for The action functions for the listener click group
#
###############################################################


def cmd_listener_run(context, name, options):
    """
    Run as a listener.
    """
    port = options['port']
    scheme = options['scheme']
    host = 'localhost'

    logfile = get_logfile(context.logdir, name)
    if logfile:
        print("Logging 'run' output to: {}".format(logfile))
        log_fp = open(logfile, 'a')  # pylint: disable=consider-using-with
        # The log file will be closed in run_exit_handler()
        sys.stdout = log_fp
        sys.stderr = log_fp
        print("Opening 'run' output log file at {}".format(datetime.now()))
    else:
        log_fp = None

    # Register a termination signal handler that causes the loop further down
    # to get control via SystemExit.
    signal.signal(signal.SIGTERM, run_term_signal_handler)

    # If this run process is started from a start process, register a Python
    # atexit handler to make sure we get control when Click exceptions terminate
    # the process. The exit handler signals a failed startup to the start
    # process.
    start_pid = is_parent_start()
    if start_pid:
        atexit.register(run_exit_handler, start_pid, log_fp)

    listeners = get_listeners(name)
    if len(listeners) > 1:  # This upcoming listener and a previous one
        lis = listeners[0]
        url = '{}://{}:{}'.format(lis.scheme, host, lis.port)
        raise click.ClickException(
            "Listener {} already running at {}".format(name, url))

    if scheme == 'http':
        http_port = port
        https_port = None
        certfile = None
        keyfile = None
    else:
        assert scheme == 'https'
        https_port = port
        http_port = None
        certfile = options['certfile']
        keyfile = options['keyfile'] or certfile
    url = '{}://{}:{}'.format(scheme, host, port)

    context.spinner_stop()

    try:
        listener = WBEMListener(
            host=host, http_port=http_port, https_port=https_port,
            certfile=certfile, keyfile=keyfile)
    except ValueError as exc:
        raise click.ClickException(
            "Cannot create listener {}: {}".format(name, exc))
    try:
        listener.start()
    except (IOError, OSError, ListenerError) as exc:
        raise click.ClickException(
            "Cannot start listener {}: {}".format(name, exc))

    indi_call = options['indi_call']
    indi_file = options['indi_file']
    indi_display = options['indi_display']
    indi_format = options['indi_format'] or DEFAULT_INDI_FORMAT

    def display_func(indication, host):
        """
        Indication callback function that displays the indication on stdout
        using the specified format.
        """
        try:
            display_str = format_indication(indication, host, indi_format)
        except Exception as exc:  # pylint: disable=broad-except
            display_str = ("Error: Cannot format indication using format "
                           "\"{}\": {}: {}".
                           format(indi_format, exc.__class__.__name__, exc))
        print(display_str)
        sys.stdout.flush()

    def file_func(indication, host):
        """
        Indication callback function that appends the indication to a file
        using the specified format.
        """
        try:
            display_str = format_indication(indication, host, indi_format)
        except Exception as exc:  # pylint: disable=broad-except
            display_str = ("Error: Cannot format indication using format "
                           "\"{}\": {}: {}".
                           format(indi_format, exc.__class__.__name__, exc))
        with open(indi_file, 'a') as fp:
            fp.write(display_str)
            fp.write('\n')

    if indi_call:
        mod_func = indi_call.rsplit('.', 1)
        if len(mod_func) < 2:
            raise click.ClickException(
                "The --indi-call option does not specify MODULE.FUNCTION: {}".
                format(indi_call))
        mod_name = mod_func[0]
        func_name = mod_func[1]

        curdir = os.getcwd()
        if sys.path[0] != curdir:
            if context.verbose >= _config.VERBOSE_SETTINGS:
                click.echo("Inserting current directory into front of Python "
                           "module search path: {}".format(curdir))
            sys.path.insert(0, curdir)

        try:
            module = importlib.import_module(mod_name)
        except ImportError as exc:
            raise click.ClickException(
                "Cannot import module {}: {}".
                format(mod_name, exc))
        except SyntaxError as exc:
            raise click.ClickException(
                "Cannot import module {}: SyntaxError: {}".
                format(mod_name, exc))
        try:
            func = getattr(module, func_name)
        except AttributeError:
            raise click.ClickException(
                "Function {}() not found in module {}".
                format(func_name, mod_name))
        listener.add_callback(func)
        if context.verbose >= _config.VERBOSE_SETTINGS:
            click.echo("Added indication handler for calling function {}() "
                       "in module {}".format(func_name, mod_name))

    if indi_display:
        listener.add_callback(display_func)
        if context.verbose >= _config.VERBOSE_SETTINGS:
            click.echo("Added indication handler for displaying on stdout "
                       "with format \"{}\"".format(indi_format))

    if indi_file:
        listener.add_callback(file_func)
        if context.verbose >= _config.VERBOSE_SETTINGS:
            click.echo("Added indication handler for appending to file {} "
                       "with format \"{}\"".format(indi_file, indi_format))

    click.echo("Running listener {} at {}".format(name, url))

    # Signal successful startup completion to the parent 'start'
    # process.
    start_pid = is_parent_start()
    if start_pid:
        if _config.VERBOSE_PROCESSES_ENABLED:
            print("Run process: Sending success signal ({}) to "
                  "start process {}".
                  format(SIGNAL_RUN_STARTUP_SUCCESS, start_pid))
        os.kill(start_pid, SIGNAL_RUN_STARTUP_SUCCESS)  # Sends the signal

    try:
        while True:
            sleep(60)
    except (KeyboardInterrupt, SystemExit) as exc:
        if _config.VERBOSE_PROCESSES_ENABLED:
            print("Run process: Caught exception {}: {}".
                  format(type(exc), exc))
        # SystemExit occurs only due to being raised in the signal handler
        # that was registered.
        listener.stop()
        click.echo("Shut down listener {} running at {}".format(name, url))

        # Signal failure to the parent 'start' process if it still
        # exists.
        start_pid = is_parent_start()
        if start_pid:
            if _config.VERBOSE_PROCESSES_ENABLED:
                print("Run process: Sending failure signal ({}) to start "
                      "process {}".
                      format(SIGNAL_RUN_STARTUP_FAILURE, start_pid))
            os.kill(start_pid, SIGNAL_RUN_STARTUP_FAILURE)  # Sends the signal


def cmd_listener_start(context, name, options):
    """
    Start a named listener.
    """
    port = options['port']
    scheme = options['scheme']
    certfile = options['certfile']
    keyfile = options['keyfile']
    indi_call = options['indi_call']
    indi_display = options['indi_display']
    indi_file = options['indi_file']
    indi_format = options['indi_format']
    host = 'localhost'

    listeners = get_listeners(name)
    if listeners:
        lis = listeners[0]
        url = '{}://{}:{}'.format(lis.scheme, host, lis.port)
        raise click.ClickException(
            "Listener {} already running at {}".format(name, url))

    run_args = [
        'pywbemlistener',
    ]
    if context.verbose:
        run_args.append('-{}'.format('v' * context.verbose))
    if context.logdir:
        run_args.extend(['--logdir', context.logdir])
    run_args.extend([
        'run', name,
        '--port', str(port),
        '--scheme', scheme,
    ])
    if certfile:
        run_args.extend(['--certfile', certfile])
    if keyfile:
        run_args.extend(['--keyfile', keyfile])
    if indi_call:
        run_args.extend(['--indi-call', indi_call])
    if indi_display:
        run_args.extend(['--indi-display'])
    if indi_file:
        run_args.extend(['--indi-file', indi_file])
    if indi_format:
        run_args.extend(['--indi-format', indi_format])

    # While we stop the spinner of this 'start' command, the spinner of the
    # invoked 'run' command will still be spinning until its startup/exit
    # completion is detected. When the output of the 'start'command is
    # redirected, the spinner of the child process will also be suppressed,
    # so this behavior is consistent and should be fine.
    context.spinner_stop()

    prepare_startup_completion()

    if six.PY2:
        popen_kwargs = {}
    else:
        popen_kwargs = dict(start_new_session=True)

    if _config.VERBOSE_PROCESSES_ENABLED:
        print("Start process: Starting run process as: {}".format(run_args))

    # pylint: disable=consider-using-with
    p = subprocess.Popen(run_args, **popen_kwargs)

    # Wait for startup completion or for error exit
    try:
        rc = wait_startup_completion(p.pid)
    except KeyboardInterrupt:
        raise click.ClickException(
            "Keyboard interrupt while waiting for listener to start up")
    if rc != 0:
        # Error has already been displayed
        raise SystemExit(rc)

    # A message about the successful startup has already been displayed by
    # the child process.


def cmd_listener_stop(context, name):
    """
    Stop a named listener.
    """
    listeners = get_listeners(name)
    if not listeners:
        raise click.ClickException(
            "No running listener found with name {}".format(name))
    listener = listeners[0]

    context.spinner_stop()

    p = psutil.Process(listener.pid)
    p.terminate()
    p.wait()

    # A message about the successful shutdown has already been displayed by
    # the child process.


def cmd_listener_show(context, name):
    """
    Show a named listener.
    """
    listeners = get_listeners(name)
    if not listeners:
        raise click.ClickException(
            "No running listener found with name {}".format(name))

    context.spinner_stop()
    display_show_listener(listeners[0], table_format=context.output_format)


def cmd_listener_list(context):
    """
    List all named listeners.
    """
    listeners = get_listeners()
    context.spinner_stop()
    if not listeners:
        click.echo("No running listeners")
    else:
        display_list_listeners(listeners, table_format=context.output_format)
