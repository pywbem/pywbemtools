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
CIMClass on a WBEM server
"""
from __future__ import absolute_import

import click

from pywbem import Error, CIMClassName, CIMError, CIM_ERR_NOT_FOUND

from .pywbemcli import cli
from ._common import display_cim_objects, filter_namelist, \
    resolve_propertylist, CMD_OPTS_TXT, TABLE_FORMATS, \
    format_table, process_invokemethod
from ._common_options import propertylist_option, names_only_option, \
    includeclassorigin_option, namespace_option, add_options, \
    summary_objects_option

from ._displaytree import display_class_tree


#
#   Common option definitions for class group
#

includeclassqualifiers_option = [              # pylint: disable=invalid-name
    click.option('--no-qualifiers', 'includequalifiers', is_flag=True,
                 required=False, default=True,
                 help='If set, request server to not include qualifiers in '
                      'the returned class(s). The default behavior is to '
                      'request qualifiers in returned class(s).')]

deepinheritance_option = [              # pylint: disable=invalid-name
    click.option('-d', '--deep-inheritance', is_flag=True, required=False,
                 help='If set, request server to return complete subclass '
                      'hiearchy for this class. The default is False which '
                      'requests only one level of subclasses.')]

localonly_option = [              # pylint: disable=invalid-name
    click.option('-l', '--local-only', is_flag=True, required=False,
                 help='Show only local properties of the class(s).')]


@cli.group('class', options_metavar=CMD_OPTS_TXT)
def class_group():
    """
    Command group for CIM classes.

    This command group defines commands to inspect classes, to invoke
    methods on classes, and to delete classes.

    Creation and modification of classes is not currently supported.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'class' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@class_group.command('get', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@add_options(localonly_option)
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(namespace_option)
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

    In the output, the class will formatted as defined by the --output-format
    general option.

    Example:

      pywbemcli -n myconn class get CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_get(context, classname, options))


@class_group.command('delete', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@click.option('-f', '--force', is_flag=True, required=False,
              help='Force the delete request to be issued even if '
              'there are instances in the server or subclasses to this class. '
              'The WBEM server may still refuse the request.')
@add_options(namespace_option)
@click.pass_obj
def class_delete(context, classname, **options):
    """
    Delete a class.

    Delete a CIM class (CLASSNAME argument) in a CIM namespace (--namespace
    option). If no namespace was specified, the default namespace of the
    connection is used.

    If the class has subclasses, the command is rejected.

    If the class has instances, the command is rejected, unless the --force
    option was specified, in which case the instances are also deleted.

    WARNING: Deleting classes can cause damage to the server: It can impact
    instance providers and other components in the server. Use this with
    command with caution.

    Some servers may refuse the operation altogether.

    Example:

      pywbemcli -n myconn class delete CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_delete(context, classname, options))


@class_group.command('invokemethod', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@click.argument('methodname', type=str, metavar='METHODNAME', required=True)
@click.option('-p', '--parameter', type=str, metavar='parameter',
              required=False, multiple=True,
              help='Optional multiple method parameters of form name=value')
@add_options(namespace_option)
@click.pass_obj
def class_invokemethod(context, classname, methodname, **options):
    """
    Invoke a method on a class.

    Invoke a static CIM method (METHODNAME argument) on a CIM class (CLASSNAME
    argument) in a CIM namespace (--namespace option), and display the method
    return value and output parameters. If no namespace was specified, the
    default namespace of the connection is used.

    The method input parameters are specified using the --parameter option,
    which can be specified multiple times.

    Pywbemcli retrieves the class definition from the server in order to
    verify that the specified input parameters are consistent with the
    parameter characteristics in the method definition.

    Use the 'instance invokemethod' command to invoke CIM methods on CIM
    instances.

    Example:

      pywbemcli -n myconn class invokemethod CIM_Foo methodx -p p1=9 -p p2=Fred
    """
    context.execute_cmd(lambda: cmd_class_invokemethod(context,
                                                       classname,
                                                       methodname,
                                                       options))


@class_group.command('enumerate', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=False)
@add_options(deepinheritance_option)
@add_options(localonly_option)
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(summary_objects_option)
@click.pass_obj
def class_enumerate(context, classname, **options):
    """
    Get the top classes or subclasses of a class in a namespace.

    Enumerate CIM classes starting either at the top of the class hierarchy
    in the specified CIM namespace (--namespace option), or at the specified
    class (CLASSNAME argument) in the specified namespace. If no namespace was
    specified, the default namespace of the connection is used.

    The --local-only, --include-classorigin, --no-qualifiers, and
    --propertylist options determine which parts are included in each retrieved
    class.

    The --deep-inheritance option defines whether or not the complete subclass
    hierarchy of the classes is retrieved.

    In the output, the classes will formatted as defined by the --output-format
    general option.

    Examples:

      pywbemcli -n myconn class enumerate -n interop
      pywbemcli -n myconn class enumerate CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_enumerate(context, classname,
                                                    options))


@class_group.command('references', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('-R', '--result-class', type=str, required=False,
              metavar='<class name>',
              help='Filter by the classname provided. Each returned '
                   'class (or classname) should be this class or its '
                   'subclasses. Optional.')
@click.option('-r', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided. Each returned class '
                   '(or classname) should refer to the target class through '
                   'a property with a name that matches the value of this '
                   'parameter. Optional.')
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(summary_objects_option)
@click.pass_obj
def class_references(context, classname, **options):
    """
    Get the classes referencing a class.

    List the CIM (association) classes that reference the specified class
    (CLASSNAME argument) or subclasses thereof in the specified CIM namespace
    (--namespace option). If no namespace was specified, the default namespace
    of the connection is used.

    The classes to be retrieved can be filtered by the --role and
    --result-class options.

    The --include-classorigin, --no-qualifiers, and --propertylist options
    determine which parts are included in each retrieved class.

    In the output, the classes will formatted as defined by the --output-format
    general option.

    Examples:

      pywbemcli -n myconn class references CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_references(context, classname,
                                                     options))


@class_group.command('associators', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('-a', '--assoc-class', type=str, required=False,
              metavar='<class name>',
              help='Filter by the association class name provided. Each '
                   'returned class (or class name) should be associated to the '
                   'source class through this class or its subclasses. '
                   'Optional.')
@click.option('-C', '--result-class', type=str, required=False,
              metavar='<class name>',
              help='Filter the returned objects by the class name provided. '
                   'Each returned class (or class name) should be this class '
                   'or one of its subclasses. Optional')
@click.option('-r', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided. Each returned class '
              '(or class name)should be associated with the source class '
              '(CLASSNAME) through an association with this role (property '
              'name in the association that matches this parameter). Optional.')
@click.option('-R', '--result-role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the result role name provided. Each returned '
              'class (or class name)should be associated with the source class '
              '(CLASSNAME) through an association with returned object having '
              'this role (property name in the association that matches this '
              'parameter). Optional.')
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(summary_objects_option)
@click.pass_obj
def class_associators(context, classname, **options):
    """
    Get the classes associated with a class.

    List the CIM classes that are associated with the specified class
    (CLASSNAME argument) or subclasses thereof in the specified CIM namespace
    (--namespace option). If no namespace was specified, the default namespace
    of the connection is used.

    The classes to be retrieved can be filtered by the --role, --result-role,
    --assoc-class, and --result-class options.

    The --include-classorigin, --no-qualifiers, and --propertylist options
    determine which parts are included in each retrieved class.

    In the output, the classes will formatted as defined by the --output-format
    general option.

    Examples:

      pywbemcli -n myconn class associators CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_associators(context, classname,
                                                      options))


@class_group.command('find', options_metavar=CMD_OPTS_TXT)
@click.argument('classname-glob', type=str, metavar='CLASSNAME-GLOB',
                required=True)
@click.option('-n', '--namespace', type=str, multiple=True,
              required=False, metavar='<name>',
              help='Namespace to use for this operation. If defined only '
              'those namespaces are searched rather than all available '
              'namespaces. ex: -n root/interop -n root/cimv2')
@click.pass_obj
def class_find(context, classname_glob, **options):
    """
    Get the classes with matching class names on the WBEM server.

    Find the CIM classes whose class name matches the specified wildcard
    expression (CLASSNAME-GLOB argument) in all CIM namespaces of the
    WBEM server, or in the specified namespace (--namespace option).

    The CLASSNAME-GLOB argument is a wildcard expression that is matched on
    the class names case insensitively. The special characters known from file
    nme wildcarding are supported: `*` to match zero or more characters, and
    `?` to match a single character. In order to not have the shell expand
    the wildcards, the CLASSNAME-GLOB argument should be put in quotes.

    For example, `pywbem_*` returns classes whose name begins with `PyWBEM_`,
    `pywbem_`, etc. '*system*' returns classes whose names include the case
    insensitive string `system`.

    Output is in table format if table output specified. Otherwise it is in the
    form <namespace>:<classname>

    In the output, the classes will formatted as defined by the --output-format
    general option if it specifies table output. Otherwise the classes will
    be in the form `<namespace>:<classname>`.

    Examples:

      pywbemcli -n myconn class find "CIM_*" -n interop
      pywbemcli -n myconn class find CIM_Foo
    """
    context.execute_cmd(lambda: cmd_class_find(context, classname_glob,
                                               options))


@class_group.command('tree', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=False)
@click.option('-s', '--superclasses', is_flag=True, required=False,
              default=False,
              help='Display the superclasses to CLASSNAME as a tree.  When '
                   'this option is set, the CLASSNAME argument is required')
@add_options(namespace_option)
@click.pass_obj
def class_tree(context, classname, **options):
    """
    Get the subclass or superclass inheritance tree of a class.

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

    In the output, the classes will formatted as a ASCII graphical tree; the
    --output-format general option is ignored.

    Examples:

      pywbemcli -n myconn class tree -n interop
      pywbemcli -n myconn class tree CIM_Foo -n interop
      pywbemcli -n myconn class tree CIM_Foo --superclasses -n interop
    """
    context.execute_cmd(lambda: cmd_class_tree(context, classname, options))

#####################################################################
#
#  Command functions for each of the subcommands in the class group
#
#####################################################################


def cmd_class_get(context, classname, options):
    """
    Get the class defined by the argument.

    Gets the class defined by CLASSNAME from the WBEM server and displays
    the class. If the class cannot be found, the server returns a CIMError
    exception.

    """
    try:
        result_class = context.conn.GetClass(
            classname,
            namespace=options['namespace'],
            LocalOnly=options['local_only'],
            IncludeQualifiers=options['includequalifiers'],
            IncludeClassOrigin=options['include_classorigin'],
            PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, result_class,
                            output_format=context.output_format)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_invokemethod(context, classname, methodname, options):
    """
    Create an instance and submit to a WBEM server
    """
    try:
        process_invokemethod(context, classname, methodname, options)
    except Exception as ex:
        raise click.ClickException("%s: %s" % (ex.__class__.__name__, ex))


def cmd_class_enumerate(context, classname, options):
    """
        Enumerate the classes returning a list of classes from the WBEM server.
    """
    # results may be either classes or classnames
    try:
        if options['names_only']:
            results = context.conn.EnumerateClassNames(
                ClassName=classname,
                namespace=options['namespace'],
                DeepInheritance=options['deep_inheritance'])
        else:
            results = context.conn.EnumerateClasses(
                ClassName=classname,
                namespace=options['namespace'],
                LocalOnly=options['local_only'],
                DeepInheritance=options['deep_inheritance'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['include_classorigin'])

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_references(context, classname, options):
    """
    Execute the references request operation to get references for
    the classname defined
    """
    if options['namespace']:
        classname = CIMClassName(classname, namespace=options['namespace'])

    try:
        if options['names_only']:
            results = context.conn.ReferenceNames(
                classname,
                ResultClass=options['result_class'],
                Role=options['role'])
        else:
            results = context.conn.References(
                classname,
                ResultClass=options['result_class'],
                Role=options['role'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['include_classorigin'],
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_associators(context, classname, options):
    """
    Execute the references request operation to get references for
    the classname defined
    """
    if options['namespace']:
        classname = CIMClassName(classname, namespace=options['namespace'])

    try:
        if options['names_only']:
            results = context.conn.AssociatorNames(
                classname,
                AssocClass=options['assoc_class'],
                Role=options['role'],
                ResultClass=options['result_class'],
                ResultRole=options['result_role'])
        else:
            results = context.conn.Associators(
                classname,
                AssocClass=options['assoc_class'],
                Role=options['role'],
                ResultClass=options['result_class'],
                ResultRole=options['result_role'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['include_classorigin'],
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_find(context, classname_glob, options):
    """
    Execute the command for get class and display the result. The result is
    a list of classes/namespaces
    """
    if options['namespace']:
        ns_names = options['namespace']
    else:
        try:
            ns_names = context.wbem_server.namespaces
            ns_names.sort()
        except CIMError as ce:
            # allow processing to continue if no interop namespace
            if ce.status_code == CIM_ERR_NOT_FOUND:
                click.echo('WARNING: %s' % ce)
                ns_names = [context.conn.default_namespace]

    try:
        names_dict = {}
        for ns in ns_names:
            classnames = context.conn.EnumerateClassNames(
                namespace=ns, DeepInheritance=True)
            filtered_classnames = filter_namelist(classname_glob, classnames)
            names_dict[ns] = filtered_classnames

        rows = []
        for ns_name in names_dict:
            ns_rows = [[ns_name, name] for name in names_dict[ns_name]]
            # sort the result by classname
            ns_rows.sort(key=lambda x: x[1])
            rows.extend(ns_rows)

        context.spinner.stop()
        if context.output_format in TABLE_FORMATS:
            headers = ['Namespace', 'Classname']
            click.echo(format_table(rows, headers,
                                    title='Find class %s' % classname_glob,
                                    table_format=context.output_format))
        else:
            # Display function to display classnames returned with
            # their namespaces in the form <namespace>:<classname>
            context.spinner.stop()
            for row in rows:
                click.echo('  %s:%s' % (row[0], row[1]))

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_tree(context, classname, options):
    """
    Execute the command to enumerate classes from the top or starting at the
    classname argument. Then format the results to be displayed as a
    left-justified tree using the asciitree library.
    The superclasses option determines if the superclass tree or the
    subclass tree is displayed.
    """
    try:
        if options['superclasses']:
            if classname is None:
                raise click.ClickException('Classname argument required for '
                                           'superclasses option')

            # get the superclasses into a list
            class_ = context.conn.GetClass(classname,
                                           namespace=options['namespace'])
            classes = []
            classes.append(class_)
            while class_.superclass:
                class_ = context.conn.GetClass(class_.superclass,
                                               namespace=options['namespace'])
                classes.append(class_)
            classname = None

        else:
            # get the subclass hierarchy either complete or starting at the
            # optional CLASSNAME
            classes = context.conn.EnumerateClasses(
                ClassName=classname,
                namespace=options['namespace'],
                DeepInheritance=True)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))

    # display the list of classes as a tree. The classname is the top
    # of the tree.
    context.spinner.stop()
    display_class_tree(classes, classname)


def cmd_class_delete(context, classname, options):
    """Delete a class from the WBEM server repository"""
    if options['namespace']:
        classname = CIMClassName(classname, namespace=options['namespace'])

    instnames = context.conn.EnumerateInstanceNames(classname)
    subclassnames = context.conn.EnumerateClassNames(ClassName=classname,
                                                     DeepInheritance=True)

    if subclassnames:
        raise click.ClickException('Delete rejected; subclasses exist')

    if not options['force']:
        if instnames:
            raise click.ClickException('Delete rejected; instances exist')
    else:
        for instname in instnames:
            context.conn.DeleteInstance(instname)

    instnames = context.conn.EnumerateInstanceNames(classname)
    if instnames:
        raise click.ClickException('Delete rejected; instance delete failed')

    try:
        context.conn.DeleteClass(classname)
        click.echo('%s delete successful' % classname)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
