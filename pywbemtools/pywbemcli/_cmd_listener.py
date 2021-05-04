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
Click Command definition for the listener command group which includes
cmds to manage indication listeners that are separate invocations of
pywbemcli representing a listener.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import os
import subprocess
import signal
import atexit
import threading
import argparse
from time import sleep
from datetime import datetime
import click
import psutil
import six

from pywbem import WBEMListener, ListenerError

from .pywbemcli import cli
from ._common import CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT, \
    format_table
from ._common_options import add_options, help_option
from ._click_extensions import PywbemcliGroup, PywbemcliCommand

# Print debug messages related to process handling
DEBUG_PROCESS = False

# Signals used for having the 'listener run' command signal startup completion
# back to its parent 'listener start' process.
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
# 'listener run' process between the signal handlers and other functions in the
# 'listener start' process.
RUN_STARTUP_STATUS = None
RUN_STARTUP_COND = threading.Condition()

# Timeout in seconds for the 'listener run' command starting up. This timeout
# also ends a possible prompt for the password of the private key file.
RUN_STARTUP_TIMEOUT = 60

DEFAULT_LISTENER_PORT = 25989
DEFAULT_LISTENER_PROTOCOL = 'https'

LISTEN_OPTIONS = [
    click.option('--port', type=int, metavar='PORT',
                 required=False, default=DEFAULT_LISTENER_PORT,
                 help=u'The port number the listener will open to receive '
                 'indications. This can be any available port. '
                 'Default: {}'.format(DEFAULT_LISTENER_PORT)),
    click.option('--protocol', type=click.Choice(['http', 'https']),
                 metavar='PROTOCOL',
                 required=False, default=DEFAULT_LISTENER_PROTOCOL,
                 help=u'The protocol used by the listener (http, https). '
                 'Default: {}'.format(DEFAULT_LISTENER_PROTOCOL)),
    click.option('--certfile', type=str, metavar='FILE',
                 required=False, default=None,
                 help=u'Path name of a PEM file containing the certificate '
                 'that will be presented as a server certificate during '
                 'SSL/TLS handshake. Required when using https. '
                 'The file may in addition contain the private key of the '
                 'certificate.'),
    click.option('--keyfile', type=str, metavar='FILE',
                 required=False, default=None,
                 help=u'Path name of a PEM file containing the private key '
                 'of the server certificate. '
                 'Required when using https and when the certificate file '
                 'does not contain the private key. '
                 'Default: Certificate file.'),
]


class ListenerProperties(object):
    """
    The properties of a running named listener.
    """

    def __init__(self, name, port, protocol, certfile, keyfile, pid, created):
        self._name = name
        self._port = port
        self._protocol = protocol
        self._certfile = certfile
        self._keyfile = keyfile
        self._pid = pid
        self._created = created

    def show_row(self):
        """Return a tuple of the properties for 'listener show' command"""
        return (
            self.name,
            str(self.port),
            self.protocol,
            self.certfile,
            self.keyfile,
            str(self.pid),
            self.created.strftime("%Y-%m-%d %H:%M:%S"),
        )

    @staticmethod
    def show_headers():
        """Return a tuple of the header labels for 'listener show' command"""
        return (
            'Name',
            'Port',
            'Protocol',
            'Certificate file',
            'Key file',
            'PID',
            'Created',
        )

    def list_row(self):
        """Return a tuple of the properties for 'listener list' command"""
        return (
            self.name,
            str(self.port),
            self.protocol,
            str(self.pid),
            self.created.strftime("%Y-%m-%d %H:%M:%S"),
        )

    @staticmethod
    def list_headers():
        """Return a tuple of the header labels for 'listener list' command"""
        return (
            'Name',
            'Port',
            'Protocol',
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
    def protocol(self):
        """string: Protocol of the listener"""
        return self._protocol

    @property
    def certfile(self):
        """string: Path name of certificate file of the listener"""
        return self._certfile

    @property
    def keyfile(self):
        """string: Path name of key file of the listener"""
        return self._keyfile

    @property
    def pid(self):
        """int: Process ID of the listener"""
        return self._pid

    @property
    def created(self):
        """datetime: Point in time when the listener process was created"""
        return self._created


@cli.group('listener', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def listener_group():
    """
    Command group for WBEM indication listeners.

    This command group defines commands to manage WBEM indication listeners.
    Each listener is a process that executes the `pywbemcli listener run`
    command to receive WBEM indications sent from a WBEM server.

    A listener process can be started with the `pywbemcli listener start`
    command and stopped with the `pywbemcli listener stop` command.

    There is no central registration of the currently running listeners.
    Instead, the currently running processes executing the
    `pywbemcli listener run` command are by definition the currently running
    listeners. Because of this, there is no notion of a stopped listener nor
    does a listener have an operational status.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'connection' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@listener_group.command('run', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True)
@add_options(LISTEN_OPTIONS)
@add_options(help_option)
@click.pass_obj
def listener_run(context, **options):
    """
    Run as a named WBEM indication listener.

    Run this command as a named WBEM indication listener until it gets
    terminated, e.g. by a keyboard interrupt, break signal (e.g. kill), or the
    `pywbemcli listener stop` command.

    A listener with that name must not be running, otherwise the command fails.

    Examples:

      pywbemcli listener run lis1
    """
    context.execute_cmd(lambda: cmd_listener_run(context, options))


@listener_group.command('start', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True)
@add_options(LISTEN_OPTIONS)
@add_options(help_option)
@click.pass_obj
def listener_start(context, **options):
    """
    Start a named WBEM indication listener in the background.

    A listener with that name must not be running, otherwise the command fails.

    A listener is identified by its hostname or IP address and a port number.
    It can be started with any free port.

    Examples:

      pywbemcli listener start lis1
    """
    context.execute_cmd(lambda: cmd_listener_start(context, options))


@listener_group.command('stop', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True)
@add_options(help_option)
@click.pass_obj
def listener_stop(context, name):
    """
    Stop a named WBEM indication listener.

    The listener will shut down gracefully.

    A listener with that name must be running, otherwise the command fails.

    Examples:

      pywbemcli listener stop lis1
    """
    context.execute_cmd(lambda: cmd_listener_stop(context, name))


@listener_group.command('show', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('name', type=str, metavar='NAME', required=True)
@add_options(help_option)
@click.pass_obj
def listener_show(context, name):
    """
    Show a named WBEM indication listener.

    A listener with that name must be running, otherwise the command fails.

    Examples:

      pywbemcli listener stop lis1
    """
    context.execute_cmd(lambda: cmd_listener_show(context, name))


@listener_group.command('list', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def listener_list(context):
    """
    List the currently running named WBEM indication listeners.

    This is done by listing the currently running `pywbemcli listener run`
    commands.
    """
    context.execute_cmd(lambda: cmd_listener_list(context))


################################################################
#
#   Common methods for The action functions for the listener click group
#
###############################################################

def get_listeners(name=None):
    """
    List the running listener processes, or the running listener process(es)
    with the specified name.

    Note that in case of the 'listener run' command, it is possible that this
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
        seen_pywbemcli = False
        for i, item in enumerate(cmdline):
            if item.endswith('pywbemcli'):
                seen_pywbemcli = True
                continue
            if seen_pywbemcli and item == 'listener':
                listener_index = i
                break
        else:
            # Ignore processes that are not 'pywbemcli [opts] listener'
            continue
        listener_args = cmdline[listener_index + 1:]  # After 'listener'
        args = parse_listener_args(listener_args)
        if args:
            if name is None or args.name == name:
                listener = ListenerProperties(
                    name=args.name, port=args.port, protocol=args.protocol,
                    certfile=args.certfile, keyfile=args.keyfile,
                    pid=p.pid, created=datetime.fromtimestamp(p.create_time()))
                ret.append(listener)
    return ret


def is_parent_start():
    """
    Determine whether the parent process is a 'listener start' command, and
    return its PID if so. Otherwise, return None.

    This is used by the 'listener run' command to find out whether it is
    executed directly by a user, vs. launched by the 'listener start' command,
    so it can signal startup completion to the 'listener start' command.

    Returns:
      int: PID of parent process, if it is 'listener start', otherwise None.
    """
    ppid = os.getppid()
    pps = psutil.Process(ppid)

    try:
        cmdline = pps.cmdline()
    except (psutil.AccessDenied, psutil.ZombieProcess):
        # Ignore processes we cannot access
        return None

    seen_pywbemcli = False
    seen_listener = False
    for item in cmdline:
        if item.endswith('pywbemcli'):
            seen_pywbemcli = True
            continue
        if seen_pywbemcli and item == 'listener':
            seen_listener = True
            continue
        if seen_listener and item == 'start':
            break
    else:
        # Ignore processes that are not 'pywbemcli [opts] listener [opts] start'
        return None

    return ppid


def prepare_startup_completion():
    """
    In the 'listener start' command, prepare for a later use of
    wait_startup_completion() by setting up the necessary signal handlers.
    """
    signal.signal(SIGNAL_RUN_STARTUP_SUCCESS, success_signal_handler)
    signal.signal(SIGNAL_RUN_STARTUP_FAILURE, failure_signal_handler)


def success_signal_handler(sig, frame):
    # pylint: disable=unused-argument
    """
    Signal handler in 'listener start' process for the signal indicating
    success of startup completion of the 'listener run' child process.
    """
    # pylint: disable=global-statement
    global RUN_STARTUP_STATUS, RUN_STARTUP_COND

    if DEBUG_PROCESS:
        print("Debug: start: Handling success signal {}".format(sig))

    RUN_STARTUP_STATUS = 'success'
    with RUN_STARTUP_COND:
        RUN_STARTUP_COND.notify()


def failure_signal_handler(sig, frame):
    # pylint: disable=unused-argument
    """
    Signal handler in 'listener start' process for the signal indicating
    failure of startup completion of the 'listener run' child process.
    """
    # pylint: disable=global-statement
    global RUN_STARTUP_STATUS, RUN_STARTUP_COND

    if DEBUG_PROCESS:
        print("Debug: start: Handling failure signal {}".format(sig))

    RUN_STARTUP_STATUS = 'failure'
    with RUN_STARTUP_COND:
        RUN_STARTUP_COND.notify()


def wait_startup_completion(child_pid):
    """
    In the 'listener start' command, wait for the 'listener run' child process
    to either successfully complete its startup or to fail its startup.

    Returns:
      int: Return code indicating whether the child started up successfully (0)
        or failed its startup (1).
    """
    # pylint: disable=global-statement
    global RUN_STARTUP_STATUS, RUN_STARTUP_COND

    if DEBUG_PROCESS:
        print("Debug: start: Waiting for run process {} to "
              "complete startup".format(child_pid))

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
        if DEBUG_PROCESS:
            print("Debug: start: Startup of run process {} succeeded".
                  format(child_pid))
        return 0

    if status == 'timeout':
        click.echo("Timeout")

    # The 'listener run' child process may still be running, or already a
    # zombie, or no longer exist. If it still is running, the likely cause is
    # that it was in a password prompt for the keyfile password that was not
    # entered.

    sleep(0.5)  # Give it some time to finish by itself before we clean it up

    if DEBUG_PROCESS:
        print("Debug: start: Startup of run process {} failed".
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
        if DEBUG_PROCESS:
            print("Debug: start: Cleaning up run process {} and status {}".
                  format(child_pid, child_status))
        try:
            child_ps.terminate()
            child_ps.wait()
        except (IOError, OSError) as exc:
            raise click.ClickException(
                "Cannot clean up 'listener run' child process with PID {}: "
                "{}: {}".format(child_pid, type(exc), exc))
    return 1


def run_exit_handler(start_pid):
    """
    Exit handler that gets etablished for the 'listener run' command.

    This exit handler signals a failed startup of the 'listener run' command
    to the 'listener start' process, if it still exists. If the 'listener start'
    process no longer exists, this means that the startup of the 'listener run'
    command succeeded earlier, and it is now terminated by some means.
    """
    if DEBUG_PROCESS:
        print("Debug: run: Exit handler sends failure signal {} to "
              "start process {}".
              format(SIGNAL_RUN_STARTUP_FAILURE, start_pid))
    try:
        os.kill(start_pid, SIGNAL_RUN_STARTUP_FAILURE)  # Sends the signal
    except OSError:
        # The original start parent no longer exists -> the earlier startup
        # succeeded.
        pass


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
    return its parsed arguments (after the 'listener' command); otherwise
    return None.
    """

    parser = SilentArgumentParser()
    parser.add_argument('run', type=str, default=None)
    parser.add_argument('name', type=str, default=None)
    parser.add_argument('--port', type=int, default=DEFAULT_LISTENER_PORT)
    parser.add_argument('--protocol', type=str,
                        default=DEFAULT_LISTENER_PROTOCOL)
    parser.add_argument('--certfile', type=str, default=None)
    parser.add_argument('--keyfile', type=str, default=None)

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
    Signal handler for the 'listener run' command that gets called for the
    SIGTERM signal, i.e. when the 'listener run' process gets terminated by
    some means.

    Ths handler ensures that the main loop of the the 'listener run' command
    gets control and can gracefully stop the listener.
    """
    if DEBUG_PROCESS:
        print("Debug: run: Received SIGTERM signal {}".format(sig))
    raise SystemExit(1)


def display_show_listener(listener, table_format):
    """
    Display a listener for the 'listener show' command.
    """
    headers = ListenerProperties.show_headers()
    rows = [listener.show_row()]
    table = format_table(
        rows, headers, table_format=table_format,
        sort_columns=None, hide_empty_cols=None, float_fmt=None)
    click.echo(table)


def display_list_listeners(listeners, table_format):
    """
    Display listeners for the 'listener list' command.
    """
    headers = ListenerProperties.list_headers()
    rows = []
    for listener in listeners:
        rows.append(listener.list_row())
    table = format_table(
        rows, headers, table_format=table_format,
        sort_columns=None, hide_empty_cols=None, float_fmt=None)
    click.echo(table)


################################################################
#
#   Common methods for The action functions for the listener click group
#
###############################################################


def cmd_listener_run(context, options):
    """
    Run as a listener.
    """
    name = options['name']
    port = options['port']
    protocol = options['protocol']
    host = 'localhost'

    # Register a termination signal handler that causes the loop further down
    # to get control via SystemExit.
    signal.signal(signal.SIGTERM, run_term_signal_handler)

    # If this run process is started from a start process, register a Python
    # atexit handler to make sure we get control when Click exceptions terminate
    # the process. The exit handler signals a failed startup to the start
    # process.
    start_pid = is_parent_start()
    if start_pid:
        atexit.register(run_exit_handler, start_pid)

    listeners = get_listeners(name)
    if len(listeners) > 1:  # This upcoming listener and a previous one
        lis = listeners[0]
        url = '{}://{}:{}'.format(lis.protocol, host, lis.port)
        raise click.ClickException(
            "Listener {} already runs at {}".format(name, url))

    if protocol == 'http':
        http_port = port
        https_port = None
        certfile = None
        keyfile = None
    else:
        assert protocol == 'https'
        https_port = port
        http_port = None
        certfile = options['certfile']
        keyfile = options['keyfile'] or certfile
    url = '{}://{}:{}'.format(protocol, host, port)

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

    click.echo("Running listener {} at {}".format(name, url))

    # Signal successful startup completion to the parent 'listener start'
    # process.
    start_pid = is_parent_start()
    if start_pid:
        if DEBUG_PROCESS:
            print("Debug: run: Sending success signal {} to start "
                  "process {}".
                  format(SIGNAL_RUN_STARTUP_SUCCESS, start_pid))
        os.kill(start_pid, SIGNAL_RUN_STARTUP_SUCCESS)  # Sends the signal

    try:
        while True:
            sleep(60)
    except (KeyboardInterrupt, SystemExit) as exc:
        if DEBUG_PROCESS:
            print("Debug: run: Caught exception {}: {}".
                  format(type(exc), exc))
        # SystemExit occurs only due to being raised in the signal handler
        # that was registered.
        listener.stop()
        click.echo("Shut down listener {} running at {}".format(name, url))

        # Signal failure to the parent 'listener start' process if it still
        # exists.
        start_pid = is_parent_start()
        if start_pid:
            if DEBUG_PROCESS:
                print("Debug: run: Sending failure signal {} to start "
                      "process {}".
                      format(SIGNAL_RUN_STARTUP_FAILURE, start_pid))
            os.kill(start_pid, SIGNAL_RUN_STARTUP_FAILURE)  # Sends the signal


def cmd_listener_start(context, options):
    """
    Start a named listener.
    """
    name = options['name']
    port = options['port']
    protocol = options['protocol']
    certfile = options['certfile']
    keyfile = options['keyfile']
    host = 'localhost'

    listeners = get_listeners(name)
    if listeners:
        lis = listeners[0]
        url = '{}://{}:{}'.format(lis.protocol, host, lis.port)
        raise click.ClickException(
            "Listener {} already runs at {}".format(name, url))

    run_args = [
        'pywbemcli', 'listener', 'run', name,
        '--port', str(port),
        '--protocol', protocol,
    ]
    if certfile:
        run_args.extend(['--certfile', certfile])
    if keyfile:
        run_args.extend(['--keyfile', keyfile])

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
