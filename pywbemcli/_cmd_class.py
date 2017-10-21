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
cmds for get, enumerate, list of classes.
"""
from __future__ import absolute_import

import click

from pywbem import Error, CIMClassName, tocimobj
from pywbem.cim_obj import NocaseDict

from .pywbemcli import cli
from ._common import display_cim_objects, filter_namelist, \
    resolve_propertylist, parse_kv_pair, CMD_OPTS_TXT, TABLE_FORMATS, \
    format_table
from ._common_options import propertylist_option, names_only_option, \
    sort_option, includeclassorigin_option, namespace_option, add_options, \
    summary_objects_option

from ._displaytree import display_class_tree


#
#   Common option definitions for class group
#

# TODO This is an awkward form for a boolean. Should we change. Note that
# the default is True which is what we want.
# One alternative might be -i --ignorequalifiers
includeclassqualifiers_option = [              # pylint: disable=invalid-name
    click.option('--includequalifiers/--no_includequalifiers',
                 is_flag=True, required=False, default=True,
                 help='Include qualifiers in the result. Default is to'
                      ' include qualifiers')]

deepinheritance_option = [              # pylint: disable=invalid-name
    click.option('-d', '--deepinheritance', is_flag=True, required=False,
                 help='Return complete subclass hiearchy for this class.')]

# TODO add a case sensitive option for those things that use regex


@cli.group('class', options_metavar=CMD_OPTS_TXT)
def class_group():
    """
    Command group to manage CIM Classes.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    command. These are NOT retained after the command is executed.
    """
    pass


@class_group.command('get', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=True,)
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
    """
    context.execute_cmd(lambda: cmd_class_get(context, classname, options))


@class_group.command('delete', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=True,)
@click.option('-f', '--force', is_flag=True, required=False,
              help='Force the delete request to be issued even if '
              'there are instances in the server or subclasses to this class. '
              ' The WBEM Server may still refuse the request.')
@add_options(namespace_option)
@click.pass_obj
def class_delete(context, classname, **options):
    """
    Delete the class defined by CLASSNAME.

    Deletes the class from the  WBEM Server completely.

    If the class has instances, the command is refused unless the
    --force option is used. If --force is used, instances are also
    deleted.

    WARNING: Removing classes from a WBEM Server can cause damage to the
    server. Use this with caution.  It can impact instance providers and
    other components in the server.

    Some server may refuse the operation.
    """
    context.execute_cmd(lambda: cmd_class_delete(context, classname, options))


@class_group.command('invokemethod', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='classname', required=True)
@click.argument('methodname', type=str, metavar='name', required=True)
@click.option('-p', '--parameter', type=str, metavar='parameter',
              required=False, multiple=True,
              help='Optional multiple method parameters of form name=value')
@add_options(namespace_option)
@click.pass_obj
def class_invokemethod(context, classname, methodname, **options):
    """
    Invoke the class method named methodname.

    This invokes the method named `methodname` on the class named `classname`.

    This is the class level invokemethod and uses only the class name on the
    invoke. The subcommand `instance invokemethod` invokes methods based
    on instance name.

    """
    context.execute_cmd(lambda: cmd_class_invokemethod(context,
                                                       classname,
                                                       methodname,
                                                       options))


@class_group.command('enumerate', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=False)
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
    Enumerate classes from the WBEMServer.

    Enumerates the classes (or classnames) from the WBEMServer starting
    either at the top of the class hierarchy or from  the position in the
    class hierarch defined by `classname` argument if provided.

    The output format is defined by the output_format global option.

    The includeclassqualifiers, includeclassorigin options define optional
    information to be included in the output.

    The deepinheritance option defines whether the complete hiearchy is
    retrieved or just the next level in the hiearchy.
    """
    context.execute_cmd(lambda: cmd_class_enumerate(context, classname,
                                                    options))


@class_group.command('references', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=True)
@click.option('-R', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the classname provided.')
@click.option('-r', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
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
    Get the reference classes for the CLASSNAME.

    Get the reference classes (or their classnames) for the CLASSNAME argument
    filtered by the role and result class options and modified  by the
    other options.
    """
    context.execute_cmd(lambda: cmd_class_references(context, classname,
                                                     options))


@class_group.command('associators', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=True)
@click.option('-a', '--assocclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the associated class name provided.')
@click.option('-c', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result class name provided.')
@click.option('-r', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
@click.option('-R', '--resultrole', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
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
    Get the associated classes for the CLASSNAME.

    Get the classes(or classnames) that are associated with the CLASSNAME
    argument filtered by the --assocclass, --resultclass, --role and
    --resultrole options.

    Results are displayed as defined by the output format global option.
    """
    context.execute_cmd(lambda: cmd_class_associators(context, classname,
                                                      options))


@class_group.command('find', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME-regex', required=True)
@add_options(sort_option)
@add_options(namespace_option)
@click.pass_obj
def class_find(context, classname, **options):
    """
    Find all classes that match CLASSNAME-regex

    Find all classes in the namespace(s) of the target WBEMServer that
    match the CLASSNAME-regex regular expression argument. The CLASSNAME-regex
    argument is required.

    The CLASSNAME argument may be either a complete classname or a regular
    expression that can be matched to one or more classnames. To limit the
    filter to a single classname, terminate the classname with $.

    The regular expression is anchored to the beginning of the classname and
    is case insensitive. Thus, `pywbem_` returns all classes that begin with
    `PyWBEM_`, `pywbem_`, etc.

    The namespace option limits the search to the defined namespace. Otherwise
    all namespaces in the target server are searched.

    Output is in table format if table output specified. Otherwise it is in the
    form <namespace>:<classname>
    """
    context.execute_cmd(lambda: cmd_class_find(context, classname, options))


@class_group.command('tree', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=False)
@click.option('-s', '--superclasses', is_flag=True, required=False,
              default=False,
              help='Display the superclasses to CLASSNAME as a tree.  In this '
                   'case CLASSNAME is required')
@add_options(namespace_option)
@click.pass_obj
def class_tree(context, classname, **options):
    """
    Display CIM class inheritance hierarchy tree.

    The classname option, if it exists defines the topmost class of the
    hierarchy to include in the display. This is a separate subcommand because
    it is tied specifically to displaying in a tree format.

    Output is displayed as a tree to the console independent of the
    output_format type.
    """
    context.execute_cmd(lambda: cmd_class_tree(context, classname, options))

#####################################################################
#
#  Command functions for each of the subcommands in the class group
#
#####################################################################


def cmd_class_get(context, classname, options):
    """
    Get the class defined by the argument and display.
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
    """Create an instance and submit to wbemserver"""

    try:
        work_class = context.conn.GetClass(
            classname,
            namespace=options['namespace'], LocalOnly=False)

        methods = work_class.methods
        if methodname not in methods:
            raise click.ClickException('Error. Method %s not in '
                                       'class %s' %
                                       (methodname, classname))
        method = work_class.methods[methodname]

        params = NocaseDict()
        for p in options['parameter']:
            name, value_str = parse_kv_pair(p)
            if name not in method.parameters:
                raise click.ClickException('Error. Parameter %s not in '
                                           'method %s' %
                                           (name, methodname))

            cl_param = work_class.parameters[name]

            # isarray = cl_param.is_array
            # TODO account for arrays of parameters

            value_ = tocimobj(cl_param.type, value_str)
            params[name] = (name, value_)

        context.conn.InvokeMethod(classname, methodname, params)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


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
            if options['sort']:
                results.sort()
        else:
            results = context.conn.EnumerateClasses(
                ClassName=classname,
                namespace=options['namespace'],
                LocalOnly=options['localonly'],
                Deepinheritance=options['deepinheritance'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['includeclassorigin'])
            if options['sort']:
                results.sort(key=lambda x: x.classname)

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'])

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
            if options['sort']:
                results.sort()
        else:
            results = context.conn.References(
                classname,
                ResultClass=options['resultclass'],
                Role=options['role'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['includeclassorigin'],
                PropertyList=resolve_propertylist(options['propertylist']))
            if options['sort']:
                results.sort(key=lambda x: x[1].classname)

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'])

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
            if options['sort']:
                results.sort()
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
            if options['sort']:
                results.sort(key=lambda x: x[1].classname)

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'])

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_find(context, classname, options):
    """
    Execute the command for get class and display the result. The result is
    a list of classes/namespaces
    """
    if options['namespace']:
        ns_names = options['namespace']
    else:
        ns_names = context.wbem_server.namespaces
        if options['sort']:
            ns_names.sort()

    try:
        names_dict = {}
        for ns in ns_names:
            classnames = context.conn.EnumerateClassNames(
                namespace=ns, DeepInheritance=True)
            filtered_classnames = filter_namelist(classname, classnames)
            if options['sort']:
                filtered_classnames.sort()
            names_dict[ns] = filtered_classnames

        # TODO we sort twice (above and below)

        rows = []
        for ns_name in names_dict:
            ns_rows = [[ns_name, name] for name in names_dict[ns_name]]
            # sort the result by classname
            ns_rows.sort(key=lambda x: x[1])
            rows.extend(ns_rows)

        if context.output_format in TABLE_FORMATS:
            headers = ['Namespace', 'Classname']
            click.echo(format_table(rows, headers,
                                    table_format=context.output_format,
                                    title='Find class %s' % classname))
        else:
            # Display function to display classnames returned with
            # their namespaces in the form <namespace>:<classname>
            for row in rows:
                print('  %s:%s' % (row[0], row[1]))

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
            # get the complete subclass hierarchy
            classes = context.conn.EnumerateClasses(
                ClassName=classname,
                namespace=options['namespace'],
                DeepInheritance=True)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))

    # display the list of classes as a tree. The classname is the top
    # of the tree.
    display_class_tree(classes, classname)


def cmd_class_delete(context, classname, options):
    """Delete a class from the wbemserver repository"""

    if options['namespace']:
        classname = CIMClassName(classname, namespace=options['namespace'])

    if not options['force']:
        insts = context.conn.PyWbemCLIEnumerateInstancePaths(classname)
        if insts:
            raise click.ClickException('Ignored; instances exist')
        # TODO test for subclasses

    try:
        context.conn.DeleteClass(classname)
        click.echo('%s delete successful' % classname)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
