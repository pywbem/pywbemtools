# (C) Copyright 2020 IBM Corp.
# (C) Copyright 2020 Inova Development Inc.
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
Click Command definition for the 'namespace' command group which includes
commands for create, delete, list, etc. of the CIM namespaces on a WBEM server.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import click

from pywbem import Error
from .pywbemcli import cli
from ._common import CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT, \
    DEFAULT_TABLE_FORMAT, output_format_is_table, format_table, display_text, \
    pywbem_error_exception, validate_output_format, all_classnames_depsorted
from ._common_options import add_options, help_option
from ._click_extensions import PywbemcliGroup, PywbemcliCommand


##########################################################################
#
#   Click command group and command definitions
#   These decorated functions implement the commands, arguments, and
#   options for the top-level 'namespace' command group
#
###########################################################################

@cli.group('namespace', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def namespace_group():
    """
    Command group for CIM namespaces.

    This command group defines commands to create, delete and list namespaces
    in a WBEM server.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'namespace' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@namespace_group.command('list', cls=PywbemcliCommand,
                         options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def namespace_list(context):
    """
    List the namespaces of the server.

    The Interop namespace must exist on the server.

    Examples:

      pywbemcli -n myconn namespace list
    """
    context.execute_cmd(lambda: cmd_namespace_list(context))


@namespace_group.command('create', cls=PywbemcliCommand,
                         options_metavar=CMD_OPTS_TXT)
@click.argument('namespace', type=str, metavar='NAMESPACE', required=True,)
@add_options(help_option)
@click.pass_obj
def namespace_create(context, namespace):
    """
    Create a namespace on the server.

    Leading and trailing slash (``/``) characters specified in the NAMESPACE
    argument will be stripped.

    The namespace must not yet exist on the server.

    The Interop namespace must exist on the server and cannot be created using
    this command, because that namespace is required to implement client
    requests to manage namespaces.

    WBEM servers may not allow this operation or may severely limit the
    conditions under which a namespace can be created on the server.

    Example:

      pywbemcli -n myconn namespace create root/cimv2
    """
    context.execute_cmd(lambda: cmd_namespace_create(context, namespace))


@namespace_group.command('delete', cls=PywbemcliCommand,
                         options_metavar=CMD_OPTS_TXT)
@click.argument('namespace', type=str, metavar='NAMESPACE', required=True,)
@click.option('--include-objects', is_flag=True, default=False,
              help=u'Delete any objects in the namespace as well. '
                   'WARNING: Deletion of instances will cause the removal of '
                   'corresponding resources in the managed environment (i.e. '
                   'in the real world). '
                   'Default: Reject command if the namespace has any objects.')
@click.option('--dry-run', is_flag=True, required=False,
              help=u'Enable dry-run mode: Do not actually delete the objects, '
                   'but display what would be done.')
@add_options(help_option)
@click.pass_obj
def namespace_delete(context, namespace, **options):
    """
    Delete a namespace from the server.

    Leading and trailing slash (``/``) characters specified in the NAMESPACE
    argument will be stripped.

    The Interop namespace must exist on the server and cannot be deleted using
    this command.

    The targeted namespace must exist on the server. If the namespace contains
    any objects (qualifier types, classes or instances), the command is
    rejected unless the --include-objects option is specified.

    If the --include-objects option is specified, the dependency order of
    classes is determined, and the instances are deleted first in that order,
    then the classes in that order, and at last the qualifier types.
    This ensures that no dangling dependencies remain at any point in the
    operation. Dependencies that are considered for this purpose are subclasses,
    referencing classes and embedding classes (EmbeddedInstance qualifier
    only). Cross-namespace associations are deleted in the targeted namespace
    and are assumed to be properly handled by the server in the other namespace.
    (i.e. to be cleaned up there as well without requiring a deletion by the
    client).

    WARNING: Deletion of instances will cause the removal of corresponding
    resources in the managed environment (i.e. in the real world). Some
    instances may not be deletable.

    WARNING: Deletion of classes or qualifier types can cause damage to
    the server: It can impact instance providers and other components in the
    server. WBEM servers may not allow the deletion of classes or qualifier
    declarations.

    WBEM servers may not allow deletion of namespaces or may severely limit the
    conditions under which a namespace can be deleted.

    Example:

      pywbemcli -n myconn namespace delete root/cimv2
    """
    context.execute_cmd(
        lambda: cmd_namespace_delete(context, namespace, options))


@namespace_group.command('interop', cls=PywbemcliCommand,
                         options_metavar=CMD_OPTS_TXT)
@add_options(help_option)
@click.pass_obj
def namespace_interop(context):
    """
    Get the Interop namespace of the server.

    The Interop namespace must exist on the server.
    """
    context.execute_cmd(lambda: cmd_namespace_interop(context))


#####################################################################
#
#  Command functions for each of the commands in the class group
#
#####################################################################


def cmd_namespace_list(context):
    """
    List the namespaces on the WBEM server.
    """
    wbem_server = context.pywbem_server.wbem_server
    output_format = validate_output_format(
        context.output_format,
        ['TABLE', 'TEXT'], default_format=DEFAULT_TABLE_FORMAT)
    try:
        namespaces = wbem_server.namespaces
        namespaces.sort()
        context.spinner_stop()
        if output_format_is_table(output_format):
            # create list for each row
            rows = [[ns] for ns in namespaces]
            click.echo(format_table(rows, ['Namespace Name'],
                                    table_format=output_format))
        else:
            display_text("\n".join(namespaces))
    except Error as er:
        raise click.ClickException('{}: {}'.format(er.__class__.__name__, er))


def cmd_namespace_create(context, namespace):
    """
    Create a namespace on the WBEM server.
    """
    wbem_server = context.pywbem_server.wbem_server
    try:
        wbem_server.create_namespace(namespace)
        context.spinner_stop()
        click.echo('Created namespace {}'.format(namespace))
    except Error as er:
        raise pywbem_error_exception(er)


def cmd_namespace_delete(context, namespace, options):
    """
    Delete a namespace on the WBEM server.
    """
    include_objects = options['include_objects']
    dry_run = options['dry_run']
    dry_run_prefix = "Dry run: " if dry_run else ""

    wbem_server = context.pywbem_server.wbem_server
    conn = context.pywbem_server.conn

    if namespace == wbem_server.interop_ns:
        raise click.ClickException(
            "Cannot delete namespace {} because it is the Interop "
            "namespace".format(namespace))

    # Check whether the namespace is empty.
    # We do not check for instances, because classes are a prerequisite for
    # instances, so if no classes exist, no instances will exist.
    # WBEM servers that do not support class operations (e.g. SFCB) will
    # raise a CIMError with status CIM_ERR_NOT_SUPPORTED.
    try:
        top_class_paths = conn.EnumerateClassNames(
            namespace=namespace, ClassName=None, DeepInheritance=False)
    except Error as exc:
        raise pywbem_error_exception(
            exc, "Cannot enumerate top-level class names in namespace {}".
            format(namespace))
    try:
        qualifiers = conn.EnumerateQualifiers(namespace=namespace)
    except Error as exc:
        raise pywbem_error_exception(
            exc, "Cannot enumerate qualifier types in namespace {}".
            format(namespace))
    non_empty = top_class_paths or qualifiers

    if non_empty and not include_objects:
        raise click.ClickException(
            "Cannot delete namespace {} because it has {} qualifier types "
            "and {} top-level classes (and possibly instances)".
            format(namespace, len(top_class_paths), len(qualifiers)))

    if top_class_paths:

        # The following is rather long-running, so we do not want it to be used
        # before the previous checks, and we want the spinner to be running
        # while it is being executed.
        classnames_depsorted = all_classnames_depsorted(namespace, conn)

        context.spinner_stop()
        for classname in classnames_depsorted:
            try:
                inst_paths = conn.EnumerateInstanceNames(
                    namespace=namespace, ClassName=classname)
            except Error as exc:
                raise pywbem_error_exception(
                    exc, "Cannot enumerate instance names of class {} in "
                    "namespace {}".format(classname, namespace))
            for inst_path in inst_paths:
                # Skip instances of subclasses. This only happens in dry-run
                # mode, but we execute it always to minimize differences
                # between dry-run mode and real mode.
                if inst_path.classname != classname:
                    assert dry_run
                    continue
                if not dry_run:
                    try:
                        conn.DeleteInstance(inst_path)
                    except Error as exc:
                        raise pywbem_error_exception(
                            exc, "Cannot delete instance {}".format(inst_path))
                click.echo('{}Deleted instance {}'.
                           format(dry_run_prefix, inst_path))
        for classname in classnames_depsorted:
            if not dry_run:
                try:
                    conn.DeleteClass(
                        namespace=namespace, ClassName=classname)
                except Error as exc:
                    raise pywbem_error_exception(
                        exc, "Cannot delete class {} in namespace {}".
                        format(classname, namespace))
            click.echo('{}Deleted class {}'.
                       format(dry_run_prefix, classname))

    if qualifiers:
        context.spinner_stop()
        for qualifier in qualifiers:
            qualifiername = qualifier.name
            if not dry_run:
                try:
                    conn.DeleteQualifier(
                        namespace=namespace, QualifierName=qualifiername)
                except Error as exc:
                    raise pywbem_error_exception(
                        exc, "Cannot delete qualifier type {} in namespace {}".
                        format(qualifiername, namespace))
            click.echo('{}Deleted qualifier type {}'.
                       format(dry_run_prefix, qualifiername))

    context.spinner_stop()
    if not dry_run:
        try:
            wbem_server.delete_namespace(namespace)
        except Error as exc:
            raise pywbem_error_exception(
                exc, "Cannot delete namespace {}".format(namespace))
    click.echo('{}Deleted namespace {}'.format(dry_run_prefix, namespace))


def cmd_namespace_interop(context):
    """
    Display the Interop namespace on the WBEM server.
    """
    wbem_server = context.pywbem_server.wbem_server
    output_format = validate_output_format(context.output_format, 'TEXT')
    try:
        interop_ns = wbem_server.interop_ns
        context.spinner_stop()
        display_text(interop_ns, output_format)
    except Error as er:
        raise pywbem_error_exception(er)
