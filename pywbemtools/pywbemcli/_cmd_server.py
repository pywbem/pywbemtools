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
import six

from pywbem import Error, MOFCompiler, ModelError
from pywbem._mof_compiler import MOFWBEMConnection, MOFCompileError
from pywbem._nocasedict import NocaseDict
from nocaselist import NocaseList

from .pywbemcli import cli
from ._common import pywbem_error_exception, parse_version_value, \
    is_experimental_class
from ._common_options import namespace_option
from .._click_extensions import PywbemtoolsGroup, PywbemtoolsCommand, \
    CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT
from .._options import add_options, help_option
from .._output_formatting import validate_output_format, format_table, \
    display_text, fold_strings

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


@cli.group('server', cls=PywbemtoolsGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def server_group():
    """
    Command group for WBEM servers.

    This command group defines commands to inspect and manage core components
    of a WBEM server including server attributes, namespaces, compiling MOF,
    the Interop namespace and schema information.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'server' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@server_group.command('brand', cls=PywbemtoolsCommand,
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


@server_group.command('info', cls=PywbemtoolsCommand,
                      options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def server_info(context):
    """
    Get information about the server.

    The information includes CIM namespaces and server brand.
    """
    context.execute_cmd(lambda: cmd_server_info(context))


@server_group.command('add-mof', cls=PywbemtoolsCommand,
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


@server_group.command('remove-mof', cls=PywbemtoolsCommand,
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


@server_group.command('schema', cls=PywbemtoolsCommand,
                      options_metavar=CMD_OPTS_TXT)
@add_options(namespace_option)
@click.option('-d', '--detail', is_flag=True, default=False,
              help=u'Display details about each schema in the namespace rather '
                   u'than accumulated for the namespace.')
@add_options(help_option)
@click.pass_obj
def server_schema(context, **options):
    """
    Get information about the server schemas.

    Gets information about the schemas and CIM schemas that define the classes
    in each namespace. The information provided includes:
      * The released DMTF CIM schema version that was the source for the
        qualifier declarations and classes for the namespace.
      * Experimental vs. final elements in the schema
      * Schema name (defined by the prefix on each class before the first '_')
      * Class count

    """
    context.execute_cmd(lambda: cmd_server_schema(context, options))


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

        interop_ns = wbem_server.interop_ns  # Determines the Interop namespace
        rows.append([wbem_server.brand, wbem_server.version,
                     interop_ns, namespaces])
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


def cmd_server_schema(context, options):
    """
    The schema command provides information on the CIM model in each namespace
    including the CIM Schema's defined, the DMTF Release schema version, whether
    the namespace/schema includes classes with the experimental qualifier, and
    the count of classes for the namespace and for each schema..
    """
    # The schema names that can be considered DMTF schemas and are part of
    # the dmtf_cim_schema
    possible_dmtf_schemas = NocaseList(['CIM', 'PRS'])

    def experimental_display(value):
        """Return string Experimental or empty sting"""
        return 'Experimental' if value else ''

    def schema_display(schema):
        """Replace dummy name for no-schema with real text"""
        if schema == "~~~":
            return "(no-schema)"
        return schema

    def version_str(version_tuple):
        """Convert 3 integer tuple to string  (1.2.3) or empty strig"""
        if all(i == version_tuple[0] for i in version_tuple):
            return ""
        return ".".join([str(i) for i in version_tuple])

    conn = context.pywbem_server.conn
    wbem_server = context.pywbem_server.wbem_server

    output_format = validate_output_format(context.output_format, 'TABLE')
    namespace_opt = options['namespace']

    # Get namespaces. This bypasses the issue whene there is no interop
    # namespace
    try:
        namespaces = [namespace_opt] if namespace_opt else \
            wbem_server.namespaces
    except ModelError:
        namespaces = [wbem_server.conn.default_namespace]

    detail = options['detail']

    rows = []
    for ns in sorted(namespaces):
        klasses = conn.EnumerateClasses(namespace=ns, DeepInheritance=True,
                                        LocalOnly=True)
        classes_count = len(klasses)
        # namespace level variables for experimental status and max version
        ns_experimental = False
        ns_max_dmtf_version = [0, 0, 0]

        # Dictionaries for schemas, schema_max_version and experimental status
        # per schema found in the namespaces
        schemas = NocaseDict()  # Schema names are case independent
        schema_max_ver = NocaseDict()
        schema_experimental = NocaseDict()
        no_schema = []

        for klass in klasses:
            schema_elements = klass.classname.split('_', 1)
            schema = schema_elements[0] if len(schema_elements) > 1 \
                else "~~~"  # this is dummy for sort that is replaced later.

            schemas[schema] = schemas.get(schema, 0) + 1
            if len(schema_elements) < 2:
                no_schema.append(klass.classname)
            if schema not in schema_max_ver:
                schema_max_ver[schema] = [0, 0, 0]

            this_class_experimental = False
            # Determine if experimental qualifier exists and set namespace
            # level experimental flag.
            if ns_experimental is False:
                if is_experimental_class(klass):
                    ns_experimental = True
                    this_class_experimental = True
            # If detail, set the schema level experimental flag
            if detail:
                if schema not in schema_experimental:
                    schema_experimental[schema] = False

                if this_class_experimental:
                    schema_experimental[schema] = True
                elif ns_experimental:
                    if schema_experimental[schema] is False:
                        if is_experimental_class(klass):
                            schema_experimental[schema] = True

            # Get the version qualifier for this class
            if 'Version' in klass.qualifiers:
                version = klass.qualifiers['Version'].value
                version = parse_version_value(version, klass.classname)

                # update the namespace max version if this schema is a
                # DMTF schema and not previously found
                if schema in possible_dmtf_schemas:
                    if version > ns_max_dmtf_version:
                        ns_max_dmtf_version = version

                # update the version in the schema_max_ver dictionary
                if schema not in schema_max_ver or \
                        version > schema_max_ver[schema]:
                    schema_max_ver[schema] = version

        # Build the table formatted output
        prev_namespace = None
        ns_version_str = version_str(ns_max_dmtf_version) \
            if classes_count else ""

        if detail:
            headers = ['Namespace', 'schemas', 'classes\ncount',
                       'schema\nversion', 'experimental']
            # Display with a line for each namespace and one for each
            # schema in the namespace
            # replace the dummy "~~~" with the output text
            for schema in sorted(schemas.keys()):
                schema_max_ver_str = version_str(schema_max_ver[schema])
                # Set the namespace in first row for each new namespace found
                if ns != prev_namespace:
                    prev_namespace = ns
                    ns_display = ns
                else:
                    ns_display = ""
                # Append the row for each schema in the namespace
                rows.append([ns_display,              # namespace. don't repeat
                             schema_display(schema),  # CIM schema
                             schemas[schema],         #
                             schema_max_ver_str,      # schema version
                             experimental_display(schema_experimental[schema])])
        else:  # display non-detail report
            # Display one line for each namespace with list of schemas in the
            # namespace
            headers = ['Namespace', 'schemas', 'classes\ncount',
                       'CIM schema\nversion', 'experimental']
            schemas_str = ", ".join(sorted(list(six.iterkeys(schemas))))
            schemas_str = schemas_str.replace('~~~', '(no-schema)')
            folded_schemas = fold_strings(schemas_str, 45,
                                          fold_list_items=False)

            rows.append([ns,
                         folded_schemas,
                         classes_count,
                         ns_version_str,
                         experimental_display(ns_experimental)
                         ])

    # if output_format_is_table(context.output_format):
    title = "Schema information{0} namespaces: {1};".format(
        '; detail;' if detail else ";", namespace_opt or "all")

    context.spinner_stop()
    click.echo(format_table(rows,
                            headers,
                            title=title,
                            table_format=output_format))
