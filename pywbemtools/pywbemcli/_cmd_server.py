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

import os
import sys
import click

from pywbem import Error, MOFCompiler
from pywbem._mof_compiler import MOFWBEMConnection, MOFCompileError

from .pywbemcli import cli
from ._common import format_table, pywbem_error_exception, \
    validate_output_format, display_text, \
    CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT
from ._common_options import add_options, help_option, namespace_option
from ._click_extensions import PywbemcliGroup, PywbemcliCommand
from ._cmd_namespace import cmd_namespace_list, cmd_namespace_interop
from ._utils import pywbemcliwarn

# NOTE: A number of the options use double-dash as the short form.  In those
# cases, a third definition of the options without the double-dash defines
# the corresponding option name, ex. 'include_qualifiers'. It should be
# defined with underscore and not dash

# Issue 224 - Exception in prompt-toolkit with python 2.7. Caused because
# with prompt-toolkit 2 + the completer requires unicode and click_repl not
# passing help as unicode in options as unicode
# NOTE: Insure that all option help attributes are unicode to get around this
#       issue

#
#   Common option definitions for server group
#

mof_include_option = [              # pylint: disable=invalid-name
    click.option('--include', '-I', metavar='INCLUDEDIR', multiple=True,
                 help=u'Path name of a MOF include directory. '
                 'May be specified multiple times.')]

mof_dry_run_option = [              # pylint: disable=invalid-name
    click.option('--dry-run', '-d', is_flag=True, default=False,
                 help=u'Enable dry-run mode: Don\'t actually modify the '
                 'server. Connection to the server is still required for '
                 'reading.')]


@cli.group('server', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def server_group():
    """
    Command group for WBEM servers.

    This command group defines commands to inspect and manage core components
    of a WBEM server including server attributes, namespaces, compiling MOF,
    the Interop namespace, management profiles, and access to profile central
    instances.

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
    List the namespaces of the server (deprecated).

    The Interop namespace must exist on the server.

    Deprecated: The 'server namespaces' command is deprecated and will be
    removed in a future version. Use the 'namespace list' command instead.
    """
    pywbemcliwarn(
        "The 'server namespaces' command is deprecated and will be removed in "
        "a future version. Use the 'namespace list' command instead.",
        DeprecationWarning)
    context.execute_cmd(lambda: cmd_namespace_list(context))


@server_group.command('interop', cls=PywbemcliCommand,
                      options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def server_interop(context):
    """
    Get the Interop namespace of the server (deprecated).

    The Interop namespace must exist on the server.

    Deprecated: The 'server interop' command is deprecated and will be removed
    in a future version. Use the 'namespace interop' command instead.
    """
    pywbemcliwarn(
        "The 'server interop' command is deprecated and will be removed in "
        "a future version. Use the 'namespace interop' command instead.",
        DeprecationWarning)
    context.execute_cmd(lambda: cmd_namespace_interop(context))


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


@server_group.command('add-mof', cls=PywbemcliCommand,
                      options_metavar=CMD_OPTS_TXT)
@click.argument('moffiles', metavar='MOFFILE', type=click.Path(),
                nargs=-1, required=True)
@add_options(namespace_option)
@add_options(mof_include_option)
@add_options(mof_dry_run_option)
@add_options(help_option)
@click.pass_obj
def server_add_mof(context, **options):
    """
    Compile MOF and add/update CIM objects in the server.

    The MOF files are specified with the MOFFILE argument, which may be
    specified multiple times. The minus sign ('-') specifies the standard
    input.

    Initially, the target namespace is the namespace specified with the
    --namespace option or if not specified the default namespace of the
    connection. If the MOF contains '#pragma namespace' directives, the target
    namespace will be changed accordingly.

    MOF include files (specified with the '#pragma include' directive) are
    searched first in the directory of the including MOF file, and then in
    the directories specified with the --include option.

    Any CIM objects (instances, classes and qualifiers) specified in the MOF
    files are created in the server, or modified if they already exist in the
    server.

    The global --verbose option will show the CIM objects that are created or
    modified.
    """
    context.execute_cmd(lambda: cmd_server_add_mof(context, options))


@server_group.command('remove-mof', cls=PywbemcliCommand,
                      options_metavar=CMD_OPTS_TXT)
@click.argument('moffiles', metavar='MOFFILE', type=click.Path(),
                nargs=-1, required=True)
@add_options(namespace_option)
@add_options(mof_include_option)
@add_options(mof_dry_run_option)
@add_options(help_option)
@click.pass_obj
def server_remove_mof(context, **options):
    """
    Compile MOF and remove CIM objects from the server.

    The MOF files are specified with the MOFFILE argument, which may be
    specified multiple times. The minus sign ('-') specifies the standard
    input.

    Initially, the target namespace is the namespace specified with the
    --namespace option or if not specified the default namespace of the
    connection. If the MOF contains '#pragma namespace' directives, the target
    namespace will be changed accordingly.

    MOF include files (specified with the '#pragma include' directive) are
    searched first in the directory of the including MOF file, and then in
    the directories specified with the --include option.

    Any CIM objects (instances, classes and qualifiers) specified in the MOF
    files are deleted from the server.

    The global --verbose option will show the CIM objects that are removed.
    """
    context.execute_cmd(lambda: cmd_server_remove_mof(context, options))


###############################################################
#         Server cmds
###############################################################


def cmd_server_brand(context):
    """
    Display product and version info of the current WBEM server
    """
    wbem_server = context.pywbem_server.wbem_server
    output_format = validate_output_format(context.output_format, 'TEXT')

    try:
        brand = wbem_server.brand
        context.spinner_stop()

        display_text(brand, output_format)

    except Error as er:
        raise pywbem_error_exception(er)


def cmd_server_info(context):
    """
    Display general overview of info from current WBEM server
    """
    wbem_server = context.pywbem_server.wbem_server
    output_format = validate_output_format(context.output_format, 'TABLE')

    try:
        # Execute the namespaces to force contact with server before
        # turning off the spinner.
        namespaces = sorted(wbem_server.namespaces)
        context.spinner_stop()

        rows = []
        headers = ['Brand', 'Version', 'Interop Namespace', 'Namespaces']
        sep = '\n' if namespaces and len(namespaces) > 3 else ', '
        namespaces = sep.join(namespaces)

        rows.append([wbem_server.brand, wbem_server.version,
                     wbem_server.interop_ns,
                     namespaces])
        click.echo(format_table(rows, headers,
                                title='Server General Information',
                                table_format=output_format))

    except Error as er:
        raise pywbem_error_exception(er)


def cmd_server_add_mof(context, options):
    """
    Compile MOF and add/update CIM objects in the server.
    """
    conn = context.pywbem_server.conn

    try:

        context.spinner_stop()

        # Define the connection to be used by the MOF compiler.
        # MOFWBEMConnection writes resulting CIM objects to a local store
        # but reads from the connection.
        if options['dry_run']:
            comp_handle = MOFWBEMConnection(conn=conn)
        else:
            comp_handle = conn

        if options['dry_run']:
            print('Executing in dry-run mode')

        include_dirs = []
        for idir in options['include']:
            if not os.path.isabs(idir):
                idir = os.path.abspath(idir)
            include_dirs.append(idir)
        for moffile in options['moffiles']:
            if moffile != '-':
                mofdir = os.path.dirname(moffile)
                if not os.path.isabs(mofdir):
                    mofdir = os.path.abspath(mofdir)
                for idir in include_dirs:
                    if mofdir.startswith(idir):
                        break
                else:
                    include_dirs.append(mofdir)

        mofcomp = MOFCompiler(handle=comp_handle, search_paths=include_dirs,
                              verbose=context.verbose)

        for moffile in options['moffiles']:
            if moffile == '-':
                mofstr = sys.stdin.read()  # bytes in py2 / text in py3
                if context.verbose:
                    print('Compiling MOF from standard input')
                # The defaulting to the connection default namespace is handled
                # inside of the MOF compiler.
                mofcomp.compile_string(mofstr, options['namespace'])
            else:
                if not os.path.isabs(moffile):
                    moffile = os.path.abspath(moffile)
                if context.verbose:
                    print('Compiling MOF file {0}'.format(moffile))
                # The defaulting to the connection default namespace is handled
                # inside of the MOF compiler.
                mofcomp.compile_file(moffile, options['namespace'])

    # If MOFCompileError, exception already logged by compile_string().
    except MOFCompileError:
        raise click.ClickException("Compile failed.")

    # Otherwise display the exception itself
    except Error as exc:
        raise pywbem_error_exception(exc)


def cmd_server_remove_mof(context, options):
    """
    Compile MOF and remove CIM objects from the server.
    """
    conn = context.pywbem_server.conn

    try:

        context.spinner_stop()

        # Define the connection to be used by the MOF compiler.
        # MOFWBEMConnection writes resulting CIM objects to a local store
        # but reads from the connection.
        comp_handle = MOFWBEMConnection(conn=conn)

        if options['dry_run']:
            print('Executing in dry-run mode')

        include_dirs = []
        for idir in options['include']:
            if not os.path.isabs(idir):
                idir = os.path.abspath(idir)
            include_dirs.append(idir)
        for moffile in options['moffiles']:
            if moffile != '-':
                mofdir = os.path.dirname(moffile)
                if not os.path.isabs(mofdir):
                    mofdir = os.path.abspath(mofdir)
                for idir in include_dirs:
                    if mofdir.startswith(idir):
                        break
                else:
                    include_dirs.append(mofdir)

        # verbose messages are displayed by rollback()
        mofcomp = MOFCompiler(handle=comp_handle, search_paths=include_dirs,
                              verbose=False)

        for moffile in options['moffiles']:
            if moffile == '-':
                mofstr = sys.stdin.read()  # bytes in py2 / text in py3
                if context.verbose:
                    print('Compiling MOF from standard input into cache')
                # The defaulting to the connection default namespace is handled
                # inside of the MOF compiler.
                mofcomp.compile_string(mofstr, options['namespace'])
            else:
                if not os.path.isabs(moffile):
                    moffile = os.path.abspath(moffile)
                if context.verbose:
                    print('Compiling MOF file {0} into cache'.format(moffile))
                # The defaulting to the connection default namespace is handled
                # inside of the MOF compiler.
                mofcomp.compile_file(moffile, options['namespace'])

        # rollback the compiled objects to remove them from the target.
        if not options['dry_run']:
            if context.verbose:
                print('Deleting CIM objects found in MOF...')
            comp_handle.rollback(verbose=context.verbose)
        else:
            if context.verbose:
                print('No deletions will be shown in dry-run mode')
    # If MOFCompileError, exception already logged by compile_string().
    except MOFCompileError:
        raise click.ClickException("Compile failed.")
    except Error as exc:
        raise pywbem_error_exception(exc)
