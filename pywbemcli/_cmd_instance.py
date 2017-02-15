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
from __future__ import absolute_import, print_function

import click
from pywbem import Error
from .pywbemcli import cli, CMD_OPTS_TXT
from ._common import display_cim_objects, parse_wbem_uri, pick_instance, \
    objects_sort, fix_propertylist
from ._common_options import propertylist_option, names_only_option, \
    sort_option, includeclassorigin_option, namespace_option, add_options

#
#   Common option definitions for class group
#


# TODO This should default to use qualifiers for class commands.
includequalifiers_option = [              # pylint: disable=invalid-name
    click.option('-i', '--includequalifiers', is_flag=True, required=False,
                 help='Include qualifiers in the result.')]

deepinheritance_option = [              # pylint: disable=invalid-name
    click.option('-d', '--deepinheritance', is_flag=True, required=False,
                 help='Return properties in subclasses of defined target. '
                      ' If not specified only properties in target class are '
                      'returned')]
interactive_option = [              # pylint: disable=invalid-name
    click.option('-i', '--interactive', is_flag=True, required=False,
                 help='instancename is classname. Gets list of all instances '
                      'namesand the user selects the instance to be returned.')]


@cli.group('instance', options_metavar=CMD_OPTS_TXT)
def instance_group():
    """
    Command Group to manage CIM instances.

    This incudes functions to get, enumerate,
    create, modify, and delete instances in a namspace and additional functions
    to get more general information on instances (ex. counts) within the
    namespace
    """


@instance_group.command('get', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('-l', '--localonly', is_flag=True, required=False,
              help='Show only local properties of the returned instance.')
@add_options(includequalifiers_option)
@click.option('-c', '--includeclassorigin', is_flag=True, required=False,
              help='Include Class Origin in the returned instance.')
@add_options(propertylist_option)
@add_options(namespace_option)
@add_options(interactive_option)
@click.pass_obj
def instance_get(context, instancename, **options):
    """
    Get a single CIMInstance.

    Gets the instance defined by instancename.

    This may be executed interactively by providing only a classname and the
    interactive option.

    """
    context.execute_cmd(lambda: cmd_instance_get(context, instancename,
                                                 options))


@instance_group.command('names', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', required=False,)
@add_options(namespace_option)
@click.pass_obj
def instance_names(context, classname, **options):
    """
    Get and display a list of instance names of the classname argument.
    """
    context.execute_cmd(lambda: cmd_instance_names(context, classname, options))


@instance_group.command('delete', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('-i', '--interactive', is_flag=True, required=False,
              help='If set, instancename argument must be a class and '
                   ' user is provided with a list of instances of the '
                   ' class from which the instance to delete is selected.')
@add_options(namespace_option)
def instance_delete(context, instancename, **options):
    """
    Delete a single instance defined by instancename from the WBEM server.
    This may be executed interactively by providing only a classname and the
    interactive option.

    """
    context.execute_cmd(lambda: cmd_instance_delete(context, instancename,
                                                    options))


@instance_group.command('create', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='classname', required=True)
@click.option('-p', 'property', type=str, metavar='property', required=False,
              multiple=True,
              help='optional multipleproperties of form name=value')
@add_options(namespace_option)
def instance_create(context, classname, **options):
    """
    Create an instance of classname.

    """
    context.execute_cmd(lambda: cmd_instance_delete(context, classname,
                                                    options))


@instance_group.command('invokemethod', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='name', required=True)
@click.argument('methodname', type=str, metavar='name', required=True)
@click.option('-p', 'parameter', type=str, metavar='parameter', required=False,
              multiple=True,
              help='optionsl multiple parameters of form name=value')
@add_options(namespace_option)
def instance_invokemethod(context, classname, **options):
    """
    Create an instance of classname.

    """
    context.execute_cmd(lambda: cmd_instance_invokemethod(context, classname,
                                                          options))


@instance_group.command('enumerate', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('-l', '--localonly', is_flag=True, required=False,
              help='Show only local properties of the class.')
@add_options(deepinheritance_option)
@add_options(includequalifiers_option)
@click.option('-c', '--includeclassorigin', is_flag=True, required=False,
              help='Include ClassOrigin in the result.')
@add_options(propertylist_option)
@add_options(namespace_option)
@add_options(names_only_option)
@add_options(sort_option)
@click.pass_obj
def instance_enumerate(context, classname, **options):
    """
    Enumerate instances or instance names from the WBEMServer starting either
    at the top  of the hiearchy (if no classname provided) or from the
    classname argument.
    """
    context.execute_cmd(lambda: cmd_instance_enumerate(context, classname,
                                                       options))


@instance_group.command('references', options_metavar=CMD_OPTS_TXT)
@click.argument('INSTANCENAME', type=str, metavar='INSTANCENAME', required=True)
@click.option('-r', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result class name provided.')
@click.option('-o', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
@add_options(includequalifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(sort_option)
@add_options(interactive_option)
@click.pass_obj
def instance_references(context, instancename, **options):
    """
    Get the reference instances or instance names.

    For the INSTANCENAME argument provided return instances or instance
    names (names-only option) filtered by the role and result class options.
    This may be executed interactively by providing only a classname and the
    interactive option.
    """
    context.execute_cmd(lambda: cmd_instance_references(context, instancename,
                                                        options))


@instance_group.command('associators', options_metavar=CMD_OPTS_TXT)
@click.argument('INSTANCENAME', type=str, metavar='INSTANCENAME', required=True)
@click.option('-a', '--assocclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the associated instancename provided.')
@click.option('-r', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result class name provided.')
@click.option('-x', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
@click.option('-o', '--resultrole', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result role name provided.')
@add_options(includequalifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(sort_option)
@add_options(interactive_option)
@click.pass_obj
def instance_associators(context, instancename, **options):
    """
    Get the associated instances or instance names.

    Returns the associated instances or names (names-only option) for the
    INSTANCENAME argument filtered by the assocclass, resultclass, role and
    resultrole arguments.
    This may be executed interactively by providing only a classname and the
    interactive option.
    """
    context.execute_cmd(lambda: cmd_instance_associators(context, instancename,
                                                         options))


# TODO option for class regex
@instance_group.command('count', options_metavar=CMD_OPTS_TXT)
@add_options(namespace_option)
@add_options(sort_option)
@click.pass_obj
def instance_count(context, **options):
    """
    Get number of instances for each class in namespace.

    """
    context.execute_cmd(lambda: cmd_instance_count(context, options))


####################################################################
#  cmd_instance_<action> processors
####################################################################
def cmd_instance_get(context, instancename, options):
    """
    get and display an instance defined either by the instancename provided
    or by the classname provided in instancename if the interactive flag
    is provided
    """
    if options['interactive']:
        try:
            instancepath = pick_instance(context, instancename,
                                         namespace=options['namespace'])
        except ValueError:
            print('Function aborted')
            return
    else:
        instancepath = parse_wbem_uri(instancename, options['namespace'])

    try:
        instance = context.conn.GetInstance(
            instancepath,
            LocalOnly=options['localonly'],
            IncludeQualifiers=options['includequalifiers'],
            IncludeClassOrigin=options['includeclassorigin'],
            PropertyList=fix_propertylist(options['propertylist']))

        display_cim_objects(instance, context.output_format)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_names(context, classname, options):
    """
    get and display a the instancenames of the instances of the class
    classname
    """
    try:
        inst_names = context.conn.EnumerateInstanceNames(
            classname,
            namespace=options['namespace'],
            DeepInheritance=options['deepinheritance'])

        if options['sort']:
            inst_names.sort()
        display_cim_objects(inst_names, context.output_format)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_enumerate(context, classname, options):
    """
    Enumerate instances or instance names (names_only option)

    """
    try:
        if options['names_only']:
            results = context.conn.EnumerateInstanceNames(
                ClassName=classname,
                namespace=options['namespace'])
            if options['sort']:
                results.sort()
        else:
            results = context.conn.EnumerateInstances(
                ClassName=classname,
                namespace=options['namespace'],
                LocalOnly=options['localonly'],
                Deepinheritance=options['deepinheritance'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['includeclassorigin'],
                PropertyList=fix_propertylist(options['propertylist']))

            if options['sort']:
                results = objects_sort(results)

        display_cim_objects(results, context.output_format)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


# TODO the class and instance references and associators can go to a single
#       client processing module I believe
def cmd_instance_references(context, instancename, options):
    """Execute the references request operation to get references for
       the classname defined. This may be either interactive or if the
       interactive option is set or use the instancename directly.

       If the interactive option is selected, the instancename MUST BE
       a classname.
    """
    if options['interactive']:
        try:
            instancepath = pick_instance(context, instancename,
                                         options['namespace'])
        except ValueError:
            print('Function aborted')
            return
    else:
        instancepath = parse_wbem_uri(instancename, options['namespace'])

    try:
        if options['names_only']:
            results = context.conn.ReferenceNames(
                instancepath,
                ResultClass=options['resultclass'],
                Role=options['role'])
            if options['sort']:
                results.sort()
        else:
            results = context.conn.References(
                instancepath,
                ResultClass=options['resultclass'],
                Role=options['role'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['includeclassorigin'],
                PropertyList=fix_propertylist(options['propertylist']))
            if options['sort']:
                results.sort(key=lambda x: x.classname)
        if options['sort']:
            results = objects_sort(results)

        display_cim_objects(results, context.output_format)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_associators(context, instancename, options):
    """Execute the references request operation to get references for
       the classname defined
    """

    # TODO, this could be common between assoc and ref
    if options['interactive']:
        try:
            instancepath = pick_instance(context, instancename,
                                         options['namespace'])
        except ValueError:
            print('Function aborted')
            return
    else:
        instancepath = parse_wbem_uri(instancename, options['namespace'])

    try:
        if options['names_only']:
            results = context.conn.AssociatorNames(
                instancepath,
                AssocClass=options['assocclass'],
                Role=options['role'],
                ResultClass=options['resultclass'],
                ResultRole=options['resultrole'])
            if options['sort']:
                results.sort()
        else:
            results = context.conn.Associators(
                instancepath,
                AssocClass=options['assocclass'],
                Role=options['role'],
                ResultClass=options['resultclass'],
                ResultRole=options['resultrole'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['includeclassorigin'],
                PropertyList=fix_propertylist(options['propertylist']))
            if options['sort']:
                results.sort(key=lambda x: x.classname)

        display_cim_objects(results)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_delete(context, instancename, options):
    """
        If option interactive is set, get instances of the class defined
        by instance name and allow the user to select the instance to
        delete.
        Otherwise attempt to delete the instance defined by instancename
    """
    if options['interactive']:
        try:
            instancename = pick_instance(context, instancename)
        except ValueError:
            print('Function aborted')
            return

    try:
        instancepath = parse_wbem_uri(instancename)
        context.conn.DeleteInstance(instancepath,
                                    namespace=options['namespace'])

        print('%s deleted')

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_create(context, classname, property, options):
    """Create an instance and submit to wbemserver"""
    print('create_instance %s\n%s\n%s' % (classname, property, options))
    print('NOT IMPLEMENTED')
    # TODO: Finish this function


def cmd_instance_invokemethod(context, instancename, methodname, parameter,
                              options):
    """Create an instance and submit to wbemserver"""
    print('create_instance %s\n%s\n%s' % (instancename, methodname,
                                          parameter, options))
    print('NOT IMPLEMENTED')

    # TODO: Finish this function


# TODO account for errors in the process and continue if found
def cmd_instance_count(context, options):
    """
    Get the number of instances of each class in the namespace
    """
    def maxlen(str_list):
        """ get the maximum length of the elements in a list of strings"""
        maxlen = 0
        for item in str_list:
            if len(item) > maxlen:
                maxlen = len(item)
        return maxlen

    # Get all classes in Namespace
    classlist = context.conn.EnumerateClassNames(
        DeepInheritance=True,
        namespace=options['namespace'])
    if options['sort']:
        classlist.sort()

    maxlen = maxlen(classlist)

    display_data = []
    for classname in classlist:
        insts = context.conn.EnumerateInstanceNames(
            classname,
            namespace=options['namespace'])
        count = 0
        # get only for the defined classname, not subclasses
        for inst in insts:
            if inst.classname == classname:
                count += 1

        if count != 0:
            tx = (classname, count)
            display_data.append(tx)

    # finally display the results
    if display_data:
        print('')
        for item in display_data:
            print('{0:<{width}}: {1}'.format(item[0], item[1], width=maxlen))
