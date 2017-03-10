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
Click command definition for the pywbemcli command, the top level command for
the pywbemcli click tool
"""
from __future__ import absolute_import


from click_repl import register_repl, repl
import click
from ._common import Context
from .config import DEFAULT_OUTPUT_FORMAT, DEFAULT_NAMESPACE

__all__ = ['cli']


# uses -h  and --help rather than just --help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# Display of options in usage line
GENERAL_OPTIONS_METAVAR = '[GENERAL-OPTIONS]'
CMD_OPTS_TXT = '[COMMAND-OPTIONS]'


@click.group(invoke_without_command=True,
             options_metavar=GENERAL_OPTIONS_METAVAR)
@click.option('-s', '--server', type=str, envvar='PYWBEMCLI_SERVER',
              help="Hostname or IP address with scheme of the WBEMServer "
                   "(EnvVar: PYWBEMCLI_SERVER).")
@click.option('-d', '--default_namespace', type=str,
              envvar='PYWBEMCLI_DEFAULT_NAMESPACE',
              help="Default Namespace to use in the target WBEMServer if no "
                   "namespace is defined in the subcommand"
                   "(EnvVar: PYWBEMCLI_DEFAULT_NAMESPACE)."
                   " (Default: {of}).".format(of=DEFAULT_NAMESPACE))
@click.option('-u', '--user', type=str, envvar='PYWBEMCLI_USER',
              help="User name for the WBEM Server connection. "
                   "(EnvVar: PYWBEMCLI_USER).")
@click.option('-p', '--password', type=str, envvar='PYWBEMCLI_PASSWORD',
              help="Password for the WBEM Server "
                   "(EnvVar: PYWBEMCLI_PASSWORD ).")
@click.option('-t', '--timeout', type=str, envvar='PYWBEMCLI_TIMEOUT',
              help="Operation timeout for the WBEM Server. "
                   "(EnvVar: PYWBEMCLI_TIMEOUT).")
@click.option('-n', '--noverify', type=str, is_flag=True,
              envvar='PYWBEMCLI_NOVERIFY',
              help='If set, client does not verify server certificate.')
@click.option('-x', '--certfile', type=str, envvar='PYWBEMCLI_CERTFILE',
              help="Server certfile. Ignored if noverify flag set. "
                   "(EnvVar: PYWBEMCLI_CERTFILE).")
@click.option('-k', '--keyfile', type=str, envvar='PYWBEMCLI_KEYFILE',
              help="Client private key file. "
                   "(EnvVar: PYWBEMCLI_KEYFILE).")
@click.option('-o', '--output-format',
              type=click.Choice(['mof', 'xml', 'table', 'csv', 'text']),
              help='Output format (Default: {of}). pywbemcli may override '
                   'the format choice depending on the operation since not '
                   'all formats apply to all output data types'
              .format(of=DEFAULT_OUTPUT_FORMAT))
@click.option('-v', '--verbose', type=str, is_flag=True,
              help='Display extra information about the processing.')
@click.version_option(help="Show the version of this command and exit.")
@click.pass_context
def cli(ctx, server, default_namespace, user, password, timeout, noverify,
        certfile, keyfile, output_format, verbose, conn=None,
        wbem_server=None):
    """
    Command line browser for WBEM Servers. This cli tool implements the
    CIM/XML client APIs as defined in pywbem to make requests to a WBEM
    server.

    The options shown above that can also be specified on any of the
    (sub-)commands.
    """
    if ctx.obj is None:
        # In command mode or are processing the command line options in
        # interactive mode.
        # Apply the documented option defaults.
        if output_format is None:
            output_format = DEFAULT_OUTPUT_FORMAT
        if default_namespace is None:
            default_namespace = DEFAULT_NAMESPACE
        if noverify is None:
            noverify = True
    else:
        # Processing an interactive command.
        # Apply the option defaults from the command line options.
        if server is None:
            server = ctx.obj.server
        if default_namespace is None:
            default_namespace = ctx.obj.default_namespace
        if user is None:
            user = ctx.obj.user
        if password is None:
            password = ctx.obj.password
        if noverify is None:
            noverify = ctx.obj.noverify
        if keyfile is None:
            keyfile = ctx.obj.keyfile
        if certfile is None:
            certfile = ctx.obj.certfile
        if timeout is None:
            timeout = ctx.obj.timeout
        if output_format is None:
            output_format = ctx.obj.output_format
        if conn is None:
            conn = ctx.obj.conn
        if wbem_server is None:
            wbem_server = ctx.obj.wbem_server

    # Create a command context for each command: An interactive command has
    # its own command context different from the command context for the
    # command line.
    ctx.obj = Context(ctx, server, default_namespace, user, password, timeout,
                      noverify, certfile, keyfile, output_format, verbose,
                      conn, wbem_server)

    # Invoke default command
    if ctx.invoked_subcommand is None:
        repl(ctx)


# register the repl function so it becomes an active component of the
# top level commands
register_repl(cli)
