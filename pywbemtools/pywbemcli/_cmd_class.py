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
Click Command definition for the class command group which includes
commands for get, enumerate, associators, references, find, etc. of the objects
CIMClass on a WBEM server.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import copy
import click

from pywbem import Error, CIMClassName, CIMError


from pywbem._nocasedict import NocaseDict

from .pywbemcli import cli
from ._common import filter_namelist, resolve_propertylist, \
    process_invokemethod, pywbem_error_exception,  \
    depending_classnames

from ._common_cmd_functions import get_namespaces, enumerate_classes_filtered, \
    ResultsHandler

from ._common_options import propertylist_option, names_only_option, \
    include_classorigin_class_option, namespace_option, summary_option, \
    multiple_namespaces_option_dflt_conn, multiple_namespaces_option_dflt_all, \
    class_filter_options, object_order_option
from ._displaytree import display_class_tree
from .._click_extensions import PywbemtoolsGroup, PywbemtoolsCommand, \
    CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT
from .._options import add_options, help_option
from .._output_formatting import output_format_is_table, \
    validate_output_format, format_table

#
#   Common option definitions for class group
#

# NOTE: A number of the options use double-dash as the short form.  In those
# cases, a third definition of the options without the double-dash defines
# the corresponding option name, ex. 'include_qualifiers'. It should be
# defined with underscore and not dash

no_qualifiers_class_option = [              # pylint: disable=invalid-name
    click.option('--nq', '--no-qualifiers', 'no_qualifiers', is_flag=True,
                 default=True,
                 help=u'Do not include qualifiers in the returned class(es). '
                      'Default: Include qualifiers.')]

deep_inheritance_class_option = [              # pylint: disable=invalid-name
    click.option('--di', '--deep-inheritance', 'deep_inheritance', is_flag=True,
                 default=False,
                 help=u'Include the complete subclass hierarchy of the '
                      'requested classes in the result set. '
                      'Default: Do not include subclasses.')]

local_only_class_option = [              # pylint: disable=invalid-name
    click.option('--lo', '--local-only', 'local_only', is_flag=True,
                 default=False,
                 help=u'Do not include superclass properties and methods in '
                      u'the returned class(es). '
                      u'Default: Include superclass properties and methods.')]


##########################################################################
#
#   Click command group and command definitions
#   These decorated functions implement the commands, arguments, and
#   options for the top-level class command group
#
###########################################################################

@cli.group('class', cls=PywbemtoolsGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def class_group():
    """
    Command group for CIM classes.

    This command group defines commands to inspect classes, invoke
    methods on classes, delete classes.

    Creation and modification of classes is not currently supported.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'class' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@class_group.command('enumerate', cls=PywbemtoolsCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=False)
@add_options(deep_inheritance_class_option)
@add_options(local_only_class_option)
@add_options(no_qualifiers_class_option)
@add_options(include_classorigin_class_option)
@add_options(names_only_option)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(summary_option)
@add_options(class_filter_options)
@add_options(object_order_option)
@add_options(help_option)
@click.pass_obj
def class_enumerate(context, classname, **options):
    """
    List top classes or subclasses of a class in namespace(s).

    Enumerate CIM classes starting either at the top of the class hierarchy
    in the specified CIM namespace (--namespace option), or at the specified
    class (CLASSNAME argument) in the specified namespace. If no namespace was
    specified, the default namespace of the connection is used.

    The --local-only, --include-classorigin, and --no-qualifiers options
    determine which parts are included in each retrieved class.

    The --deep-inheritance option defines whether or not the complete subclass
    hierarchy of the classes is retrieved.

    The --names-only option can be used to show only the class paths.

    In the output, the classes and class paths will be formatted as defined
    by the --output-format general option. Table formats on classes will be
    replaced with MOF format.

    Examples:

      pywbemcli -n myconn class enumerate -n interop

      pywbemcli -n myconn class enumerate CIM_Foo -n interop
    """
    context.execute_cmd(
        lambda: cmd_class_enumerate(context, classname, options))


@class_group.command('get', cls=PywbemtoolsCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@add_options(local_only_class_option)
@add_options(no_qualifiers_class_option)
@add_options(include_classorigin_class_option)
@add_options(propertylist_option)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(help_option)
@click.pass_obj
def class_get(context, classname, **options):
    """
    Get a class.

    Get a CIM class (CLASSNAME argument) in a CIM namespace (--namespace
    option). If no namespace was specified, the default namespace of the
    connection is used.

    The --local-only, --include-classorigin, --no-qualifiers, and
    --propertylist options determine which parts are included in each retrieved
    class.

    In the output, the class will be formatted as defined by the
    --output-format general option. Table formats are replaced with MOF
    format.

    Example:

      pywbemcli -n myconn class get CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_get(context, classname, options))


@class_group.command('delete', cls=PywbemtoolsCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@click.option('--include-instances', is_flag=True, default=False,
              help=u'Delete any instances of the class as well. '
                   'WARNING: Deletion of instances will cause the removal '
                   'of corresponding resources in the managed environment '
                   '(i.e. in the real world).'
                   'Default: Reject command if the class has any instances.')
@click.option('--dry-run', is_flag=True, required=False,
              help=u'Enable dry-run mode: Do not actually delete the objects, '
                   'but display what would be done.')
@add_options(namespace_option)
@add_options(help_option)
@click.pass_obj
def class_delete(context, classname, **options):
    """
    Delete a class.

    Delete a CIM class (CLASSNAME argument) in a CIM namespace (--namespace
    option). If no namespace was specified, the default namespace of the
    connection is used.

    If the class has instances, the command is rejected, unless the
    --include-instances option is specified, in which case the instances
    are also deleted.

    If other classes in that namespace depend on the class to be deleted, the
    command is rejected. Dependencies considered for this purpose are
    subclasses, referencing classes and embedding classes (EmbeddedInstance
    qualifier only).

    WARNING: Deletion of instances will cause the removal of corresponding
    resources in the managed environment (i.e. in the real world). Some
    instances may not be deletable.

    WARNING: Deleting classes can cause damage to the server: It can impact
    instance providers and other components in the server. Use this
    command with caution.

    Many WBEM servers may not allow this operation or may severely limit the
    conditions under which a class can be deleted from the server.

    Example:

      pywbemcli -n myconn class delete CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_delete(context, classname, options))


@class_group.command('invokemethod', cls=PywbemtoolsCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@click.argument('methodname', type=str, metavar='METHODNAME', required=True)
@click.option('-p', '--parameter', type=str, metavar='PARAMETERNAME=VALUE',
              required=False, multiple=True,
              help=u'Specify a method input parameter with its value. '
                   'May be specified multiple times. '
                   'Default: No input parameters.')
@add_options(namespace_option)
@add_options(help_option)
@click.pass_obj
def class_invokemethod(context, classname, methodname, **options):
    """
    Invoke a method on a class.

    Invoke a static CIM method (METHODNAME argument) on a CIM class (CLASSNAME
    argument) in a CIM namespace (--namespace option), and display the method
    return value and output parameters. If no namespace was specified, the
    default namespace of the connection is used.

    The method input parameters are specified using the --parameter option,
    which may be specified multiple times.

    Pywbemcli retrieves the class definition from the server in order to
    verify that the specified input parameters are consistent with the
    parameter characteristics in the method definition.

    Use the 'instance invokemethod' command to invoke CIM methods on CIM
    instances.

    Example:

      pywbemcli -n myconn class invokemethod CIM_Foo methodx -p p1=9 -p p2=Fred
    """
    context.execute_cmd(
        lambda: cmd_class_invokemethod(context, classname, methodname, options))


@class_group.command('references', cls=PywbemtoolsCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help=u'Filter the result set by result class name. '
                   'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by source end role name.')
@add_options(no_qualifiers_class_option)
@add_options(include_classorigin_class_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(object_order_option)
@add_options(summary_option)
@add_options(help_option)
@click.pass_obj
def class_references(context, classname, **options):
    """
    List the classes referencing a class.

    List the CIM (association) classes that reference the specified class
    (CLASSNAME argument) in the specified CIM namespace
    (--namespace option). If no namespace was specified, the default namespace
    of the connection is used.

    The classes to be retrieved can be filtered by the --role and
    --result-class options.

    The --include-classorigin, --no-qualifiers, and --propertylist options
    determine which parts are included in each retrieved class.

    The --names-only option can be used to show only the class paths.

    In the output, the classes and class paths will be formatted as defined
    by the --output-format general option. Table formats on classes will be
    replaced with MOF format.

    Examples:

      pywbemcli -n myconn class references CIM_Foo -n interop
    """
    context.execute_cmd(
        lambda: cmd_class_references(context, classname, options))


@class_group.command('associators', cls=PywbemtoolsCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('--ac', '--assoc-class', 'assoc_class', type=str, required=False,
              metavar='CLASSNAME',
              help=u'Filter the result set by association class name. '
                   'Subclasses of the specified class also match.')
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help=u'Filter the result set by result class name. '
                   'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by source end role name.')
@click.option('--rr', '--result-role', 'result_role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by far end role name.')
@add_options(no_qualifiers_class_option)
@add_options(include_classorigin_class_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(object_order_option)
@add_options(summary_option)
@add_options(help_option)
@click.pass_obj
def class_associators(context, classname, **options):
    """
    List the classes associated with a class.

    List the CIM classes that are associated with the specified class
    (CLASSNAME argument) in the specified CIM namespace
    (--namespace option). If no namespace was specified, the default namespace
    of the connection is used.

    The classes to be retrieved can be filtered by the --role, --result-role,
    --assoc-class, and --result-class options.

    The --include-classorigin, --no-qualifiers, and --propertylist options
    determine which parts are included in each retrieved class.

    The --names-only option can be used to show only the class paths.

    In the output, the classes and class paths will be formatted as defined
    by the --output-format general option. Table formats on classes will be
    replaced with MOF format.

    Examples:

      pywbemcli -n myconn class associators CIM_Foo -n interop
    """
    context.execute_cmd(
        lambda: cmd_class_associators(context, classname, options))


@class_group.command('find', cls=PywbemtoolsCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname-glob', type=str, metavar='CLASSNAME-GLOB',
                required=True)
@add_options(multiple_namespaces_option_dflt_all)
@click.option('-s', '--sort', is_flag=True, required=False,
              help=u'Sort by namespace. Default is to sort by classname')
@add_options(class_filter_options)
@add_options(help_option)
@click.pass_obj
def class_find(context, classname_glob, **options):
    """
    List the classes with matching class names on the server.

    Find the CIM classes whose class name matches the specified wildcard
    expression (CLASSNAME-GLOB argument) in all CIM namespaces of the
    WBEM server, or in the specified namespace (--namespace option).

    The CLASSNAME-GLOB argument is a wildcard expression that is matched on
    class names case insensitively.
    The special characters from Unix file name wildcarding are supported
    ('*' to match zero or more characters, '?' to match a single character,
    and '[]' to match character ranges). To avoid shell expansion of wildcard
    characters, the CLASSNAME-GLOB argument should be put in quotes.

    For example, "pywbem_*" returns classes whose name begins with "PyWBEM_",
    "pywbem_", etc. "*system*" returns classes whose names include the case
    insensitive string "system".

    In the output, the classes will be formatted as defined by the
    --output-format general option if it specifies table output. Otherwise
    the classes will be in the form "NAMESPACE:CLASSNAME".

    Examples:

      pywbemcli -n myconn class find "CIM_*System*" -n interop

      pywbemcli -n myconn class find *Foo*
    """

    context.execute_cmd(
        lambda: cmd_class_find(context, classname_glob, options))


@class_group.command('tree', cls=PywbemtoolsCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=False)
@click.option('-s', '--superclasses', is_flag=True, default=False,
              help=u'Show the superclass hierarchy. '
                   'Default: Show the subclass hierarchy.')
@click.option('-d', '--detail', is_flag=True, default=False,
              help=u'Show details about the class: the Version, '
                   ' Association, Indication, and Abstact qualifiers.')
@add_options(namespace_option)
@add_options(help_option)
@click.pass_obj
def class_tree(context, classname, **options):
    """
    Show the subclass or superclass hierarchy for a class.

    List the subclass or superclass hierarchy of a CIM class (CLASSNAME
    argument) or CIM namespace (--namespace option):

    - If CLASSNAME is omitted, the complete class hierarchy of the specified
      namespace is retrieved.

    - If CLASSNAME is specified but not --superclasses, the class and its
      subclass hierarchy in the specified namespace are retrieved.

    - If CLASSNAME and --superclasses are specified, the class and its
      superclass ancestry up to the top-level class in the specified namespace
      are retrieved.

    If no namespace was specified, the default namespace of the connection is
    used.

    The class hierarchy will formatted as a ASCII graphical tree; the
    --output-format general option is ignored.

    The --detail options to display extra information about each class
    including:

    -  The Version qualifier value if the class includes a version
       qualifier. This is normally a string with 3 integers

    -  Information about each class type (Association, Indication, Abstract)

    Examples:

      # Display the complete class hierarchy from the interop namespace
      pywbemcli -n myconn class tree -n interop

      # Display CIM_Foo an its subclasses from the namespace interop
      pywbemcli -n myconn class tree CIM_Foo -n interop

      # Display CIM_Foo and its superclasses from interop
      pywbemcli -n myconn class tree CIM_Foo -s -n interop

    """
    context.execute_cmd(lambda: cmd_class_tree(context, classname, options))


####################################################################
#
#  Common functions for cmd_class processing
#  This includes functions used by the command action functions
#  in this module and possibly other modules
#
#  get_namespaces, enumerate_classes_filtered, and handle_multi_ns_exc
#  are called from the instance and qualifier command processors.
#
####################################################################


def get_classnames_in_namespaces(context, options, namespaces, classname_glob):
    """
    Get the classnames of all classes in the namespaces parameter that
    matches the classname_glob pattern.

    Parameters:

      context :
        Context object for the command

      options (python dictionary)
        Options dictionary for the command executiong

      namespaces (list of strings):
        List of the namespaces from which namespace names are to be retrieved.

      classname_glob ((:term: `string`))
        A string that may contain GLOB characters which serves as the
        filter

    Returns:
        NocaseDict where the keys are namespace names and the value for
        each key is the list of classnames that match the glob patter  in
        each namespace in namespaces

    """

    # Dictionary key is namespaces, value is list of classes
    names_dict = NocaseDict()
    if namespaces:
        # Use di True, and names_only build options to get all names
        # Create deep copy to insure no changes to original dict
        options_tmp = copy.deepcopy(options)
        options_tmp['deep_inheritance'] = True
        options_tmp['names_only'] = True
        try:
            for ns in namespaces:
                # Enumerate filtered for classnames and add to dictionary
                # of returns for each namespace
                classnames = enumerate_classes_filtered(context, ns, None,
                                                        options_tmp)
                names_dict[ns] = filter_namelist(classname_glob, classnames)
        except Error as er:
            raise pywbem_error_exception(er)

    return names_dict


def get_format_group(context, options):
    """
    Define the format groups allowed based on the options. This is particular
    to the class commands, largely because we do not have a table format
    for enumerate, get, associators, or references unless options such as
    summary, or names_only are set.
    """

    # Summary always output as TABLE
    if 'summary' in options and options['summary']:

        # This accounts for the fact that the results of a summary can be
        # either table or simply a string output
        if context.output_format and \
                output_format_is_table(context.output_format):
            return ['TABLE']

        # Temporary hack. We need another format group, i.e. txt or str
        # That displays in non-structured manner. Or drop this output
        # completely.
        return ['CIM']

    # Names_only may be output as Table or as CIM Object.
    if 'names_only' in options and options['names_only']:
        return ['CIM', 'TABLE']

    # otherwise only CIM allowed today.
    return ['CIM']


#####################################################################
#
#  Command functions for each of the commands in the class group
#
#####################################################################


def cmd_class_get(context, classname, options):
    """
    Get the class defined by the argument.

    Gets the class defined by CLASSNAME from the WBEM server and displays
    the class. If the class cannot be found, the server returns a CIMError
    exception.
    """
    conn = context.pywbem_server.conn
    format_group = get_format_group(context, options)
    output_format = validate_output_format(context.output_format, format_group)

    results = ResultsHandler(context, options, output_format, "class",
                             classname)

    for ns in results:
        try:
            results.add(conn.GetClass(
                classname,
                namespace=ns,
                LocalOnly=options['local_only'],
                IncludeQualifiers=options['no_qualifiers'],
                IncludeClassOrigin=options['include_classorigin'],
                PropertyList=resolve_propertylist(options['propertylist'])))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

    results.display()


def cmd_class_invokemethod(context, classname, methodname, options):
    """
    Create an instance and submit to a WBEM server
    """

    try:
        cln = CIMClassName(classname, namespace=options['namespace'])
        process_invokemethod(context, cln, methodname, options['namespace'],
                             options['parameter'])
    except Error as er:
        raise pywbem_error_exception(er)


def cmd_class_enumerate(context, classname, options):
    """
        Enumerate the classes returning a list of classes from the WBEM server.
        That match the qualifier filter options
    """
    format_group = get_format_group(context, options)
    output_format = validate_output_format(context.output_format, format_group)

    results = ResultsHandler(context, options, output_format, "class",
                             classname)

    for ns in results:
        try:
            results.add(enumerate_classes_filtered(
                context, ns, classname, options))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

    results.display()


def cmd_class_references(context, classname, options):
    """
    Execute the references request operation to get references for
    the classname defined
    """
    conn = context.pywbem_server.conn
    format_group = get_format_group(context, options)
    output_format = validate_output_format(context.output_format, format_group)

    results = ResultsHandler(context, options, output_format, "class",
                             classname)

    for ns in results:
        try:
            cln = CIMClassName(classname, namespace=ns)
            if options['names_only']:
                results.add(conn.ReferenceNames(
                    cln,
                    ResultClass=options['result_class'],
                    Role=options['role']))
            else:
                results.add(conn.References(
                    cln,
                    ResultClass=options['result_class'],
                    Role=options['role'],
                    IncludeQualifiers=options['no_qualifiers'],
                    IncludeClassOrigin=options['include_classorigin'],
                    PropertyList=resolve_propertylist(options['propertylist'])))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

    results.display()


def cmd_class_associators(context, classname, options):
    """
    Execute the references request operation to get references for
    the classname defined
    """
    conn = context.pywbem_server.conn

    format_group = get_format_group(context, options)
    output_format = validate_output_format(context.output_format, format_group)

    results = ResultsHandler(context, options, output_format, "class",
                             classname)

    for ns in results:
        try:
            cln = CIMClassName(classname, namespace=ns)
            if options['names_only']:
                results.add(conn.AssociatorNames(
                    cln,
                    AssocClass=options['assoc_class'],
                    Role=options['role'],
                    ResultClass=options['result_class'],
                    ResultRole=options['result_role']))
            else:
                results.add(conn.Associators(
                    cln,
                    AssocClass=options['assoc_class'],
                    Role=options['role'],
                    ResultClass=options['result_class'],
                    ResultRole=options['result_role'],
                    IncludeQualifiers=options['no_qualifiers'],
                    IncludeClassOrigin=options['include_classorigin'],
                    PropertyList=resolve_propertylist(options['propertylist'])))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

    results.display()


def cmd_class_find(context, classname_glob, options):
    """
    Execute the command for enumerate classes, filter the results based on the
    option and display the result. The result is a list of classes/namespaces
    """

    output_format = validate_output_format(context.output_format, 'TABLE')

    context.spinner_stop()
    namespaces = get_namespaces(context, options['namespace'],
                                default_all_ns=True)

    try:
        # Define sort by namespace name if --sort, or  othersise by count
        sort_col = 0 if options['sort'] else 1

        names_dict = get_classnames_in_namespaces(context, options, namespaces,
                                                  classname_glob)

        context.spinner_stop()

        # If summary set, generate output of only count of classes for
        # each namespace
        if 'summary' in options and options['summary']:
            rows = [[ns, len(names_dict[ns])] for ns in names_dict]
            rows.sort(key=lambda x: x[sort_col])

            if output_format_is_table(context.output_format):
                headers = ['Namespace', 'Class count']
                click.echo(format_table(rows,
                                        headers,
                                        title='Find class counts {}'.
                                        format(classname_glob),
                                        table_format=output_format))
            else:
                for ns, count in rows:
                    click.echo('  {}: {}'. format(ns, count))
            return

        # Not summary. Build rows of namespace, classname for each namespace
        # and sort by names if --sort set
        rows = []
        for ns_name in names_dict:
            ns_rows = [[ns_name, name] for name in names_dict[ns_name]]
            # sort by classname if sort option defined, else by namespace
            ns_rows.sort(key=lambda x: x[sort_col])
            rows.extend(ns_rows)

        context.spinner_stop()

        if output_format_is_table(context.output_format):
            headers = ['Namespace', 'Classname']
            click.echo(
                format_table(rows, headers,
                             title='Find class {}'.format(classname_glob),
                             table_format=output_format))
        else:
            # Display function to display classnames returned with
            # their namespaces in the form <namespace>:<classname>
            for row in rows:
                click.echo('  {}: {}'.format(row[0], row[1]))

    except Error as er:
        raise pywbem_error_exception(er)


def get_class_hierarchy(conn, classname, namespace, superclasses=None):
    """
    Get the class hierarchy from the server, either the superclasses
    associated or subclasses with classname .  If getting subclasses
    the classname parameter may be None which requests that the complete
    class hiearchy be retrieved.

      Parameters:
        conn (:class:`~pywbem.WBEMConnection` or subclass):
            Current connection to a WBEM server.

        classname(:term:`string):
            classname if the tree is to be initiated from
            within the class hiearchy. May be None

        namespace(:term:`string):
          Namespace to use to acquire classes from WBEM server

        superclasses (:class:`py:bool`):
            If `True` display the superclasses of classname. If not True
            display the subclasses. The default is None (display subclasses).

      Returns:
        tuple of  classes, classnames where
          classes (list of :class:`~pywbem.CIMClass`): that are either the
          superclasses or the subclasses of classname.

      Raises:
        CIM_Error:
    """

    try:
        if superclasses:
            # classname must exist for superclass tree
            assert classname is not None

            # get the superclasses into a list
            klass = conn.GetClass(classname, namespace=namespace)
            classes = []
            classes.append(klass)
            while klass.superclass:
                klass = conn.GetClass(klass.superclass, namespace=namespace)
                classes.append(klass)
        else:
            # get the subclass hierarchy either complete or starting at the
            # optional CLASSNAME. Gets minimum data from server to define
            # class, superclass data
            classes = conn.EnumerateClasses(ClassName=classname,
                                            namespace=namespace,
                                            LocalOnly=True,
                                            IncludeQualifiers=True,
                                            DeepInheritance=True)

    except Error as er:
        raise pywbem_error_exception(er)

    return classes


def cmd_class_tree(context, classname, options):
    """
    Execute the command to display graphical tree of either superclasses or
    subclasses of classname. If classname is None, display tree starting from
    the class hierarchy root.
    Tree is displayed on the console as a left-justified tree using the
    asciitree library.
    The --superclasses option determines if the superclass tree or the
    subclass tree is displayed.
    """
    conn = context.pywbem_server.conn

    superclasses = options['superclasses']

    # Classname must exist as starting point for superclass tree.
    if superclasses and classname is None:
        raise click.ClickException('CLASSNAME argument required for '
                                   '--superclasses option')

    classes = get_class_hierarchy(conn, classname, options['namespace'],
                                  superclasses)

    # If showing superclasses, set classname to None for the display
    # to add the 'root' as top class.
    if superclasses:
        classname = None

    # Display the list of classes as a tree. The classname is the top
    # of the tree.
    context.spinner_stop()
    display_class_tree(classes, classname, show_detail=options['detail'])


def cmd_class_delete(context, classname, options):
    """Delete a class from the WBEM server repository"""
    conn = context.pywbem_server.conn

    include_instances = options['include_instances']
    dry_run = options['dry_run']
    dry_run_prefix = "Dry run: " if dry_run else ""

    namespace = options['namespace'] or conn.default_namespace

    try:
        instnames = conn.EnumerateInstanceNames(
            ClassName=classname, namespace=namespace)
    except Error as exc:
        raise pywbem_error_exception(
            exc, "Cannot enumerate instance names of class {} in "
            "namespace {}".format(classname, namespace))

    if instnames and not include_instances:
        raise click.ClickException(
            "Cannot delete class {} because it has {} instances".
            format(classname, len(instnames)))

    depending_cln_list = depending_classnames(
        classname, namespace, conn)

    if depending_cln_list:
        raise click.ClickException(
            "Cannot delete class {} because these classes depend on it: {}".
            format(classname, ', '.join(depending_cln_list)))

    context.spinner_stop()
    if include_instances:
        for instname in instnames:
            if not dry_run:
                try:
                    conn.DeleteInstance(instname)
                except Error as exc:
                    raise pywbem_error_exception(
                        exc, "Cannot delete instance {}".format(instname))
            click.echo('{}Deleted instance {}'.format(dry_run_prefix, instname))

    if not dry_run:
        try:
            conn.DeleteClass(classname)
        except Error as exc:
            raise pywbem_error_exception(
                exc, "Cannot delete class {} in namespace {}".
                format(classname, namespace))
    click.echo('{}Deleted class {}'.format(dry_run_prefix, classname))
