# Copyright  2017 IBM Corp. and Inova Development Inc.
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
from ._common import display_cim_objects, parse_cim_namespace_str, \
    pick_instance, objects_sort, resolve_propertylist, create_ciminstance, \
    create_params
from ._common_options import propertylist_option, names_only_option, \
    sort_option, includeclassorigin_option, namespace_option, add_options
from .config import DEFAULT_QUERY_LANGUAGE


#
#   Common option definitions for class group
#


# This is instance-only because the default is False for includequalifiers
# on instances but True on classes
includequalifiers_option = [              # pylint: disable=invalid-name
    click.option('-q', '--includequalifiers', is_flag=True, required=False,
                 help='Include qualifiers in the result.')]

deepinheritance_option = [              # pylint: disable=invalid-name
    click.option('-d', '--deepinheritance', is_flag=True, required=False,
                 help='Return properties in subclasses of defined target. '
                      ' If not specified only properties in target class are '
                      'returned')]

interactive_option = [              # pylint: disable=invalid-name
    click.option('-i', '--interactive', is_flag=True, required=False,
                 help='If set, instancename argument must be a class and '
                      ' user is provided with a list of instances of the '
                      ' class from which the instance to delete is selected.')]


@cli.group('instance', options_metavar=CMD_OPTS_TXT)
def instance_group():
    """
    Command Group to manage CIM instances.

    This incudes functions to get, enumerate,
    create, modify, and delete instances in a namspace and additional functions
    to get more general information on instances (ex. counts) within the
    namespace
    """
    pass


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


@instance_group.command('delete', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@add_options(interactive_option)
@add_options(namespace_option)
@click.pass_obj
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
@click.option('-x', '--property', type=str, metavar='property', required=False,
              multiple=True,
              help='Optional multiple property definitions of form name=value')
@add_options(propertylist_option)
@add_options(namespace_option)
@click.pass_obj
def instance_create(context, classname, **options):
    """
    Create an instance of classname.

    """
    context.execute_cmd(lambda: cmd_instance_create(context, classname,
                                                    options))


@instance_group.command('invokemethod', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='name', required=True)
@click.argument('methodname', type=str, metavar='name', required=True)
@click.option('-p', '--parameter', type=str, metavar='parameter',
              required=False, multiple=True,
              help='Optional multiple method parameters of form name=value')
@add_options(namespace_option)
@click.pass_obj
def instance_invokemethod(context, instancename, methodname, **options):
    """
    Invoke the method defined by instancename and methodname with parameters.

    This issues an instance level invokemethod request and displays the
    results.

    """
    context.execute_cmd(lambda: cmd_instance_invokemethod(context,
                                                          instancename,
                                                          methodname,
                                                          options))


@instance_group.command('names', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', required=False,)
@add_options(namespace_option)
@add_options(sort_option)
@click.pass_obj
def instance_names(context, classname, **options):
    """
    Get and display a list of instance names of the classname argument.

    This is equivalent to pywbemcli instance enumerate -o
    """
    context.execute_cmd(lambda: cmd_instance_names(context, classname, options))


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
    classname argument provided.

    Displays the returned instances or names
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


@instance_group.command('query', options_metavar=CMD_OPTS_TXT)
@click.argument('query', type=str, required=True, metavar='<query string>')
@click.option('-l', '--querylanguage', type=str, required=False,
              metavar='<query language>', default=DEFAULT_QUERY_LANGUAGE,
              help='Use the query language defined. '
                   '(Default: {of}.'.format(of=DEFAULT_QUERY_LANGUAGE))
@add_options(namespace_option)
@add_options(sort_option)
@click.pass_obj
def instance_query(context, query, **options):
    """
    Execute the query defined by the query argument.

    """
    context.execute_cmd(lambda: cmd_instance_query(context, query, options))


# TODO add option for class regex to limit the search
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
            if not instancepath:
                return
        except ValueError as ve:
            raise click.ClickException("%s: %s" % (ve.__class__.__name__, ve))

    else:
        instancepath = parse_cim_namespace_str(instancename,
                                               options['namespace'])

    try:
        instance = context.conn.GetInstance(
            instancepath,
            LocalOnly=options['localonly'],
            IncludeQualifiers=options['includequalifiers'],
            IncludeClassOrigin=options['includeclassorigin'],
            PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, instance, context.output_format)
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
            instancepath = pick_instance(context, instancename,
                                         namespace=options['namespace'])
            if not instancepath:
                return
        except ValueError as ve:
            raise click.ClickException("%s: %s" % (ve.__class__.__name__, ve))
    else:
        instancepath = parse_cim_namespace_str(instancename,
                                               options['namespace'])

    try:
        context.conn.DeleteInstance(instancepath)

        print('Deleted %s', instancepath)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_create(context, classname, options):
    """Create an instance and submit to wbemserver"""

    try:
        class_ = context.conn.GetClass(
            classname, namespace=options['namespace'], LocalOnly=False)

        property_list = resolve_propertylist(options['propertylist'])

        properties = options['property']

        # properties is a tuple of name,value pairs
        new_inst = create_ciminstance(class_, properties, property_list)
        # context.conn.debug = True
        context.conn.CreateInstance(new_inst, namespace=options['namespace'])
        # print('Request as debug shows\n%s' % context.conn.last_request)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_invokemethod(context, instancename, methodname,
                              options):
    """Create an instance and submit to wbemserver"""

    if options['interactive']:
        try:
            instancepath = pick_instance(context, instancename,
                                         options['namespace'])
            if not instancepath:
                return
        except ValueError as er:
            raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
    else:
        instancepath = parse_cim_namespace_str(instancename,
                                               options['namespace'])

    try:
        cim_class = context.conn.GetClass(
            instancepath.classname,
            namespace=options['namespace'], LocalOnly=False)

        cim_methods = cim_class.methods
        if methodname not in cim_methods:
            raise click.ClickException('Error. Method %s not in '
                                       'class %s' %
                                       (methodname, instancepath.classname))
        cim_method = cim_class.methods[methodname]

        params = create_params(cim_method, options['parameter'])

        context.conn.InvokeMethod(instancepath, methodname, params)

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
            namespace=options['namespace'])

        if options['sort']:
            inst_names.sort()
        display_cim_objects(context, inst_names, context.output_format)

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
                PropertyList=resolve_propertylist(options['propertylist']))

            if options['sort']:
                results = objects_sort(results)

        display_cim_objects(context, results, context.output_format)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


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
            if not instancepath:
                return
        except ValueError:
            print('Function aborted')
            return
    else:
        instancepath = parse_cim_namespace_str(instancename,
                                               options['namespace'])

    # TODO the class and instance references and associators can go to a single
    #       client processing function

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
                PropertyList=resolve_propertylist(options['propertylist']))
            if options['sort']:
                results.sort(key=lambda x: x.classname)
        if options['sort']:
            results = objects_sort(results)

        display_cim_objects(context, results, context.output_format)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_associators(context, instancename, options):
    """
    Execute the references request operation to get references for
    the classname defined
    """

    # TODO, this could be common code between assoc and ref
    if options['interactive']:
        try:
            instancepath = pick_instance(context, instancename,
                                         options['namespace'])
            if not instancepath:
                return
        except ValueError as ve:
            raise click.ClickException("%s: %s" % (ve.__class__.__name__, ve))
    else:
        instancepath = parse_cim_namespace_str(instancename,
                                               options['namespace'])

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
                PropertyList=resolve_propertylist(options['propertylist']))
            if options['sort']:
                results.sort(key=lambda x: x.classname)

        display_cim_objects(context, results)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


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

    # TODO Am I handling the namespace correctly? What about default?
    namespace = options['namespace']

    # Get all classes in Namespace
    classlist = context.conn.EnumerateClassNames(
        DeepInheritance=True,
        namespace=namespace)
    if options['sort']:
        classlist.sort()

    maxlen = maxlen(classlist)

    display_data = []
    for classname in classlist:

        # Try block allows issues where enumerate does not properly execute
        # in some cases. The totals may be wrong but at least it gets what
        # it can.
        try:
            insts = context.conn.EnumerateInstanceNames(
                classname,
                namespace=namespace)
        except Error as er:
            print('Server Error %s with %s:%s. Continuing' % (er, namespace,
                                                              classname))
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


def cmd_instance_query(context, query, options):
    """Execute the query defined by the inputs"""

    try:
        results = context.conn.execquery(options['querylanguage'],
                                         query, options['namespace'])

        if options['sort']:
            results.sort(key=lambda x: x.classname)

        display_cim_objects(context, results)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
