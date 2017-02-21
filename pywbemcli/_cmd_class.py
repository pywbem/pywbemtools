# Copyright TODO
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
from .pywbemcli import cli, CMD_OPTS_TXT
from ._common import display_cim_objects, filter_namelist, fix_propertylist, \
    parse_kv_pair
from ._common_options import propertylist_option, names_only_option, \
    sort_option, includeclassorigin_option, namespace_option, add_options
from ._displaytree import display_class_tree

#
#   Common option definitions for class group
#

# TODO This should default to use qualifiers for class commands.
includeclassqualifiers_option = [              # pylint: disable=invalid-name
    click.option('--includequalifiers/--no_includequalifiers',
                 is_flag=True, required=False, default=True,
                 help='Include qualifiers in the result. Default is to'
                      ' include qualifiers')]

deepinheritance_option = [              # pylint: disable=invalid-name
    click.option('-d', '--deepinheritance', is_flag=True, required=False,
                 help='Return complete subclass hiearchy for this class.')]

# TODO add a case sensitive option and make the sort an option group.


@cli.group('class', options_metavar=CMD_OPTS_TXT)
def class_group():
    """
    Command group to manage CIM Classes.
    """
    pass


# Reverse includequalifiers so the default is true
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
    get and display a single class from the WBEM Server
    """
    context.execute_cmd(lambda: cmd_class_get(context, classname, options))


@class_group.command('invokemethod', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='classname', required=True)
@click.argument('methodname', type=str, metavar='name', required=True)
@click.option('-p', '--parameter', type=str, metavar='parameter',
              required=False, multiple=True,
              help='Optionall multiple method parameters of form name=value')
@add_options(namespace_option)
@click.pass_obj
def class_invokemethod(context, classname, methodname, **options):
    """
    Invoke the class method named methodname in the class classname

    """
    context.execute_cmd(lambda: cmd_class_invokemethod(context,
                                                       classname,
                                                       methodname,
                                                       options))


@class_group.command('names', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=False,)
@click.option('-d', '--deepinheritance', is_flag=True, required=False,
              help='Return complete subclass hiearchy for this class.')
@add_options(deepinheritance_option)
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(sort_option)
@add_options(namespace_option)
@click.pass_obj
def class_names(context, classname, **options):
    """
    get and display a list of classnames from the WBEM Server.
    """
    context.execute_cmd(lambda: cmd_class_names(context, classname, options))


@class_group.command('enumerate', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=False)
@click.option('-d', '--deepinheritance', is_flag=True, required=False,
              help='Return complete subclass hiearchy for this class.')
@click.option('-l', '--localonly', is_flag=True, required=False,
              help='Show only local properties of the class.')
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(names_only_option)
@add_options(sort_option)
@add_options(namespace_option)
@click.pass_obj
def class_enumerate(context, classname, **options):
    """
    Enumerate classes from the WBEMServer starting either at the top or from
    the classname argument if provided
    """
    context.execute_cmd(lambda: cmd_class_enumerate(context, classname,
                                                    options))


@class_group.command('references', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=True)
@click.option('-r', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the classname provided.')
@click.option('-o', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(sort_option)
@add_options(namespace_option)
@click.pass_obj
def class_references(context, classname, **options):
    """
    Get the reference classes for the CLASSNAME argument filtered by the
    role and result class options.
    """
    context.execute_cmd(lambda: cmd_class_references(context, classname,
                                                     options))


@class_group.command('associators', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=True)
@click.option('-a', '--assocclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the associated class name provided.')
@click.option('-r', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result class name provided.')
@click.option('-x', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
@click.option('-o', '--resultrole', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
@add_options(includeclassqualifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(sort_option)
@add_options(namespace_option)
@click.pass_obj
def class_associators(context, classname, **options):
    """
    Get the associated classes for the CLASSNAME argument filtered by the
    assocclass, resultclass, role and resultrole arguments.
    """
    context.execute_cmd(lambda: cmd_class_associators(context, classname,
                                                      options))


# TODO we can make optional namespace option the limit search
@class_group.command('find', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=True)
@add_options(sort_option)
@click.pass_obj
def class_find(context, classname, **options):
    """
    Find all classes that match the CLASSNAME argument in the namespaces of
    the defined WBEMserver. The CLASSNAME argument may be either a
    classname or a regular expression that can be matched to one or more
    classnames.
    """
    context.execute_cmd(lambda: cmd_class_find(context, classname, options))


@class_group.command('tree', options_metavar=CMD_OPTS_TXT)
@click.argument('CLASSNAME', type=str, metavar='CLASSNAME', required=False)
@click.option('-s', '--superclasses', is_flag=True, required=False,
              default=False,
              help='Display the superclasses to CLASSNAME.  In this case '
              'CLASSNAME is required')
@add_options(namespace_option)
@click.pass_obj
def class_tree(context, classname, **options):
    """
    Display the classnames as a tree on the console.

    The classname option, if it exists defines the topmost  class of the tree
    to include in the display. This is a separate subcommand because it
    is tied specifically to this one output_format.
    """
    context.execute_cmd(lambda: cmd_class_tree(context, classname,
                                               options))

#
#  Command functions for each of the subcommands in the class group
#


def cmd_class_get(context, classname, options):
    """
    Execute the command for get class and display the result
    """
    try:
        result_class = context.conn.GetClass(
            classname,
            namespace=options['namespace'],
            LocalOnly=options['localonly'],
            IncludeQualifiers=options['includequalifiers'],
            IncludeClassOrigin=options['includeclassorigin'],
            PropertyList=fix_propertylist(options['propertylist']))
        display_cim_objects(context, result_class, context.output_format)
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
                raise click.ClickException('Error. Parameter %s not in method' %
                                           (name, methodname))

            cl_param = work_class.parameters[name]

            # isarray = cl_param.is_array
            # TODO account for arrays of parameters

            value_ = tocimobj(cl_param.type, value_str)
            params[name] = (name, value_)

        context.conn.InvokeMethod(classname, methodname, params)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_names(context, classname, options):
    """ Execute the EnumerateClassNames operation."""
    try:
        result_classnames = context.conn.EnumerateClassNames(
            ClassName=classname,
            namespace=options['namespace'],
            DeepInheritance=options['deepinheritance'])
        if options['sort']:
            result_classnames.sort()
        display_cim_objects(context, result_classnames, context.output_format)
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

        display_cim_objects(context, results, context.output_format)

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
                PropertyList=fix_propertylist(options['propertylist']))
            if options['sort']:
                results.sort(key=lambda x: x.classname)

        display_cim_objects(context, results, context.output_format)

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
                PropertyList=fix_propertylist(options['propertylist']))
            if options['sort']:
                results.sort(key=lambda x: x.classname)
        display_cim_objects(context, results, context.output_format)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_find(context, classname, options):
    """
    Execute the command for get class and display the result. The result is
    a list of classes/namespaces
    """
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

        # Display function to display classnames returned with
        # their namespaces in the form <namespace>:<classname>
        for ns_name in names_dict:
            for classname in names_dict[ns_name]:
                print('  %s:%s' % (ns_name, classname))

        # ##display_result(result)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_class_tree(context, classname, options):
    """
    Execute the command to enumerate classes from the top or starting at the
    classname argument. Then format the results to be displayed as a
    left-justified tree using the asciitree library
    """

    if options['superclasses']:
        if classname is None:
            raise click.ClickException('Classname required for superclasses '
                                       'option')

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
        classes = context.conn.EnumerateClasses(ClassName=classname,
                                                namespace=options['namespace'],
                                                DeepInheritance=True)

    display_class_tree(classes, classname)
