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
cmds for get, enumerate, associators, references, find, etc. of the objects
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
    sort_option, includeclassorigin_option, namespace_option, add_options, \
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
    click.option('-d', '--deepinheritance', is_flag=True, required=False,
                 help='If set, request server to return complete subclass '
                      'hiearchy for this class. The default is False which '
                      'requests only one level of subclasses.')]


@cli.group('class', options_metavar=CMD_OPTS_TXT)
def class_group():
    """
    Command group to manage CIM classes.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    command. These are NOT retained after the command is executed.
    """
    pass  # pylint: disable=unnecessary-pass


@class_group.command('get', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@click.option('-l', '--localonly', is_flag=True, required=False,
              help='Show only local properties of the class.')
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(namespace_option)
@click.pass_obj
def class_get(context, classname, **options):
    """
    Get and display a single CIM class.

    Get a single CIM class defined by the CLASSNAME argument from the WBEM
    server and display it. Normally it is retrieved from the default namespace
    in the server.

    If the class is not found in the WBEM server, the server returns an
    exception.

    The --includeclassorigin, --includeclassqualifiers, and --propertylist
    options determine what parts of the class definition are retrieved.

    Results are formatted as defined by the output format general option.

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
    Delete a single CIM class.

    Deletes the CIM class defined by CLASSNAME from the WBEM server.

    If the class has instances, the command is refused unless the
    --force option is used. If --force is used, instances are also
    deleted.

    If the class has subclasses, the command is rejected.

    WARNING: Removing classes from a WBEM server can cause damage to the
    server. Use this with caution.  It can impact instance providers and
    other components in the server.

    Some servers may refuse the operation.
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
    Invoke the class method named methodname.

    This invokes the method named METHODNAME on the class named CLASSNAME.

    This is the class level invokemethod and uses only the class name on the
    invoke.The subcommand `instance invokemethod` invokes methods based on
    class name.

    Examples:

      pywbemcli invokemethod CIM_Foo methodx -p param1=9 -p param2=Fred
    """
    context.execute_cmd(lambda: cmd_class_invokemethod(context,
                                                       classname,
                                                       methodname,
                                                       options))


@class_group.command('enumerate', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=False)
@click.option('-d', '--deepinheritance', is_flag=True, required=False,
              help='Return complete subclass hierarchy for this class if '
                   'set. Otherwise retrieve only the next hierarchy level.')
@click.option('-l', '--localonly', is_flag=True, required=False,
              help='Show only local properties of the class.')
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(names_only_option)
@add_options(sort_option)
@add_options(namespace_option)
@add_options(summary_objects_option)
@click.pass_obj
def class_enumerate(context, classname, **options):
    """
    Enumerate classes from the WBEM server.

    Enumerates the classes (or classnames) from the WBEM server starting
    either at the top of the class hierarchy or from  the position in the
    class hierarchy defined by `CLASSNAME` argument if provided.

    The output format is defined by the output-format general option.

    The includeclassqualifiers, includeclassorigin options define optional
    information to be included in the output.

    The deepinheritance option defines whether the complete hiearchy is
    retrieved or just the next level in the hiearchy.

    Results are formatted as defined by the output format general option.
    """
    context.execute_cmd(lambda: cmd_class_enumerate(context, classname,
                                                    options))


@class_group.command('references', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('-R', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result classname provided. Each returned '
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
@add_options(sort_option)
@add_options(namespace_option)
@add_options(summary_objects_option)
@click.pass_obj
def class_references(context, classname, **options):
    """
    Get the reference classes for CLASSNAME.

    Get the reference classes (or class names) for the CLASSNAME argument
    filtered by the role and result class options and modified by the
    other options.

    Results are displayed as defined by the output format general option.
    """
    context.execute_cmd(lambda: cmd_class_references(context, classname,
                                                     options))


@class_group.command('associators', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('-a', '--assocclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the association class name provided. Each '
                   'returned class (or class name) should be associated to the '
                   'source class through this class or its subclasses. '
                   'Optional.')
@click.option('-C', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the association result class name provided. Each '
                   'returned class (or class name) should be this class or one '
                   'of its subclasses. Optional')
@click.option('-r', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided. Each returned class '
              '(or class name)should be associated with the source class '
              '(CLASSNAME) through an association with this role (property '
              'name in the association that matches this parameter). Optional.')
@click.option('-R', '--resultrole', type=str, required=False,
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
@add_options(sort_option)
@add_options(namespace_option)
@add_options(summary_objects_option)
@click.pass_obj
def class_associators(context, classname, **options):
    """
    Get the associated classes for CLASSNAME.

    Get the classes(or class names) that are associated with the CLASSNAME
    argument filtered by the --assocclass, --resultclass, --role and
    --resultrole options and modified by the other options.

    Results are formatted as defined by the output format general option.
    """
    context.execute_cmd(lambda: cmd_class_associators(context, classname,
                                                      options))


@class_group.command('find', options_metavar=CMD_OPTS_TXT)
@click.argument('classname-glob', type=str, metavar='CLASSNAME-GLOB',
                required=True)
@add_options(sort_option)
@click.option('-n', '--namespace', type=str, multiple=True,
              required=False, metavar='<name>',
              help='Namespace(s) to use for this operation. If defined only '
              'those namespaces are searched rather than all available '
              'namespaces. ex: -n root/interop -n root/cimv2')
@click.pass_obj
def class_find(context, classname_glob, **options):
    """
    Find all classes that match CLASSNAME-GLOB.

    Find all classes in the namespace(s) of the target WBEM server that
    match the CLASSNAME-GLOB regular expression argument and return the
    classnames. The CLASSNAME-GLOB argument is required.

    The CLASSNAME-GLOB argument may be either a complete classname or a regular
    expression that can be matched to one or more classnames. To limit the
    filter to a single classname, terminate the classname with $.

    The GLOB expression is anchored to the beginning of the CLASSNAME-GLOB, is
    is case insensitive and uses the standard GLOB special characters
    (*(match everything), ?(match single character)).
    Thus, `pywbem_*` returns all classes that begin with
    `PyWBEM_`, `pywbem_`, etc. '.*system*' returns classnames that include
    the case insensitive string `system`.

    The namespace option limits the search to the defined namespaces. Otherwise
    all namespaces in the target server are searched.

    Output is in table format if table output specified. Otherwise it is in the
    form <namespace>:<classname>
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
    Display CIM class inheritance hierarchy tree.

    Displays a tree of the class hiearchy to show superclasses and subclasses.

    CLASSNAMe is an optional argument that defines the starting point for the
    hiearchy display

    If the --superclasses option not specified the hiearchy starting either
    at the top most classes of the class hiearchy or at the class defined by
    CLASSNAME is displayed.

    if the --superclasses options is specified and a CLASSNAME is defined
    the class hiearchy of superclasses leading to CLASSNAME is displayed.

    This is a separate subcommand because it is tied specifically to displaying
    in a tree format.so that the --output-format general option is ignored.
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

    Gets the class defined by CLASSNAME from thw wbem server and displays
    the class. If the class cannot be found, the server returns a CIMError
    exception.

    """
    try:
        result_class = context.conn.GetClass(
            classname,
            namespace=options['namespace'],
            LocalOnly=options['localonly'],
            IncludeQualifiers=options['includequalifiers'],
            IncludeClassOrigin=options['includeclassorigin'],
            PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, result_class,
                            output_format=context.output_format)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_invokemethod(context, classname, methodname, options):
    """
    Create an instance and submit to wbemserver
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
                DeepInheritance=options['deepinheritance'])
        else:
            results = context.conn.EnumerateClasses(
                ClassName=classname,
                namespace=options['namespace'],
                LocalOnly=options['localonly'],
                DeepInheritance=options['deepinheritance'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['includeclassorigin'])

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=options['sort'])

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_references(context, classname, options):
    """Execute the references request operation to get references for
       the classname defined
    """
    if options['namespace']:
        classname = CIMClassName(classname, namespace=options['namespace'])

    try:
        if options['names_only']:
            results = context.conn.ReferenceNames(
                classname,
                ResultClass=options['resultclass'],
                Role=options['role'])
        else:
            results = context.conn.References(
                classname,
                ResultClass=options['resultclass'],
                Role=options['role'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['includeclassorigin'],
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=options['sort'])

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_associators(context, classname, options):
    """Execute the references request operation to get references for
       the classname defined
    """
    if options['namespace']:
        classname = CIMClassName(classname, namespace=options['namespace'])

    try:
        if options['names_only']:
            results = context.conn.AssociatorNames(
                classname,
                AssocClass=options['assocclass'],
                Role=options['role'],
                ResultClass=options['resultclass'],
                ResultRole=options['resultrole'])
        else:
            results = context.conn.Associators(
                classname,
                AssocClass=options['assocclass'],
                Role=options['role'],
                ResultClass=options['resultclass'],
                ResultRole=options['resultrole'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['includeclassorigin'],
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=options['sort'])

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
        except CIMError as ce:
            # allow processing to continue if no interop namespace
            if ce.status_code == CIM_ERR_NOT_FOUND:
                click.echo('WARNING: %s' % ce)
                ns_names = [context.conn.default_namespace]
        if options['sort']:
            ns_names.sort()

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
    """Delete a class from the wbemserver repository"""
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
