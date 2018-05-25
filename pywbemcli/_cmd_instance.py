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
from __future__ import absolute_import, print_function

import click
from pywbem import Error
from .pywbemcli import cli
from ._common import display_cim_objects, parse_cim_namespace_str, \
    pick_instance, objects_sort, resolve_propertylist, create_ciminstance, \
    create_params, filter_namelist, CMD_OPTS_TXT, format_table
from ._common_options import propertylist_option, names_only_option, \
    sort_option, includeclassorigin_option, namespace_option, add_options, \
    summary_objects_option
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
                 help='If set, INSTANCENAME argument must be a class and '
                      ' user is provided with a list of instances of the '
                      ' class from which the instance to delete is selected.')]


@cli.group('instance', options_metavar=CMD_OPTS_TXT)
def instance_group():
    """
    Command group to manage CIM instances.

    This incudes functions to get, enumerate,
    create, modify, and delete instances in a namspace and additional functions
    to get more general information on instances (ex. counts) within the
    namespace

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    command. These are NOT retained after the command is executed.
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

    Gets the instance defined by INSTANCENAME.

    This may be executed interactively by providing only a classname and the
    interactive option (-i).

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
    Delete a single CIM instance.

    Delete the instanced defined by INSTANCENAME from the WBEM server.
    This may be executed interactively by providing only a class name and the
    interactive option.
    """
    context.execute_cmd(lambda: cmd_instance_delete(context, instancename,
                                                    options))


@instance_group.command('create', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('-P', '--property', type=str, metavar='property', required=False,
              multiple=True,
              help='Optional property definitions of form name=value.'
              'Multiple definitions allowed, one for each property')
@add_options(propertylist_option)
@add_options(namespace_option)
@click.pass_obj
def instance_create(context, classname, **options):
    """
    Create an instance of classname.

    Creates an instance of the class `CLASSNAME` with the properties defined
    in the property option.

    The propertylist option limits the created instance to the properties
    in the list. This parameter is NOT passed to the server
    """
    context.execute_cmd(lambda: cmd_instance_create(context, classname,
                                                    options))


@instance_group.command('invokemethod', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.argument('methodname', type=str, metavar='METHODNAME', required=True)
@click.option('-p', '--parameter', type=str, metavar='parameter',
              required=False, multiple=True,
              help='Optional multiple method parameters of form name=value')
@add_options(interactive_option)
@add_options(namespace_option)
@click.pass_obj
def instance_invokemethod(context, instancename, methodname, **options):
    """
    Invoke a CIM method.

    Invoke the method defined by INSTANCENAME and METHODNAME arguments with
    parameters defined by the --parameter options.

    This issues an instance level invokemethod request and displays the
    results.

    A class level invoke method is available as `pywbemcli class invokemethod`.


    """
    context.execute_cmd(lambda: cmd_instance_invokemethod(context,
                                                          instancename,
                                                          methodname,
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
@add_options(summary_objects_option)
@click.pass_obj
def instance_enumerate(context, classname, **options):
    """
    Enumerate instances or names of CLASSNAME.

    Enumerate instances or instance names from the WBEMServer starting either
    at the top  of the hierarchy (if no CLASSNAME provided) or from the
    CLASSNAME argument if provided.

    Displays the returned instances or names
    """
    context.execute_cmd(lambda: cmd_instance_enumerate(context, classname,
                                                       options))


@instance_group.command('references', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('-R', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result class name provided.')
@click.option('-r', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
@add_options(includequalifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(sort_option)
@add_options(interactive_option)
@add_options(summary_objects_option)
@click.pass_obj
def instance_references(context, instancename, **options):
    """
    Get the reference instances or names.

    Gets the reference instances or instance names(--names-only option) for a
    target instance name in the target WBEM server.

    For the INSTANCENAME argument provided return instances or instance
    names filtered by the --role and --resultclass options.

    This may be executed interactively by providing only a class name and the
    interactive option(-i). Pywbemcli presents a list of instances names in the
    class from which one can be chosen as the target.
    """
    context.execute_cmd(lambda: cmd_instance_references(context, instancename,
                                                        options))


@instance_group.command('associators', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('-a', '--assocclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the associated instancename provided.')
@click.option('-c', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result class name provided.')
@click.option('-R', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided.')
@click.option('-R', '--resultrole', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result role name provided.')
@add_options(includequalifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(sort_option)
@add_options(interactive_option)
@add_options(summary_objects_option)
@click.pass_obj
def instance_associators(context, instancename, **options):
    """
    Get associated instances or names.

    Returns the associated instances or names (--names-only option) for the
    INSTANCENAME argument filtered by the --assocclass, --resultclass, --role
    and --resultrole options.

    This may be executed interactively by providing only a classname and the
    interactive option. Pywbemcli presents a list of instances in the class
    from which one can be chosen as the target.
    """
    context.execute_cmd(lambda: cmd_instance_associators(context, instancename,
                                                         options))


@instance_group.command('query', options_metavar=CMD_OPTS_TXT)
@click.argument('query', type=str, required=True, metavar='QUERY_STRING')
@click.option('-l', '--querylanguage', type=str, required=False,
              metavar='QUERY LANGUAGE', default=DEFAULT_QUERY_LANGUAGE,
              help='Use the query language defined. '
                   '(Default: {of}.'.format(of=DEFAULT_QUERY_LANGUAGE))
@add_options(namespace_option)
@add_options(sort_option)
@add_options(summary_objects_option)
@click.pass_obj
def instance_query(context, query, **options):
    """
    Execute an execquery request.

    Executes a query request on the target WBEM Server with the QUERY_STRING
    argument and query language options.

    The results of the query are displayed as mof or xml.

    """
    context.execute_cmd(lambda: cmd_instance_query(context, query, options))


@instance_group.command('count', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME-REGEX',
                required=False)
@click.option('-s', '--sort', is_flag=True, required=False,
              help='Sort by instance count. Otherwise sorted by classname')
@add_options(namespace_option)
@click.pass_obj
def instance_count(context, classname, **options):
    """
    Get instance count for classes.

    Displays the count of instances for the classes defined by the
    `CLASSNAME-REGEX` argument in one or more namespaces.

    The size of the response may be limited by CLASSNAME-REGEX argument which
    defines a regular expression based on the desired class names so that only
    classes that match the regex are counted. The CLASSNAME-regex argument is
    optional.

    The CLASSNAME-regex argument may be either a complete classname or a regular
    expression that can be matched to one or more classnames. To limit the
    filter to a single classname, terminate the classname with $.

    The CLASSNAME-REGEX regular expression is anchored to the beginning of the
    classname and is case insensitive. Thus `pywbem_` returns all classes that
    begin with `PyWBEM_`, `pywbem_`, etc.

    This operation can take a long time to execute.

    """
    context.execute_cmd(lambda: cmd_instance_count(context, classname, options))


####################################################################
#  cmd_instance_<action> processors
####################################################################
def cmd_instance_get(context, instancename, options):
    """
    Get and display an instance of a CIM Class.

    Gets the instance defined by instancename argument and displays in output
    format defined.

    If the interactive flag (-i) is set, only a classname is provided as
    the instancename argument and pywbemcli presents a list of instances
    to the console from which one can be picked to get from the server and
    display.
    """
    try:
        if options['interactive']:
            instancepath = pick_instance(context, instancename,
                                         namespace=options['namespace'])
            if not instancepath:
                return
        else:
            instancepath = parse_cim_namespace_str(instancename,
                                                   options['namespace'])
    except ValueError as ve:
        raise click.ClickException("%s: %s" % (ve.__class__.__name__, ve))

    try:
        instance = context.conn.GetInstance(
            instancepath,
            LocalOnly=options['localonly'],
            IncludeQualifiers=options['includequalifiers'],
            IncludeClassOrigin=options['includeclassorigin'],
            PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, instance, context.output_format,
                            summary=options['summary'])

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_delete(context, instancename, options):
    """
        If option interactive is set, get instances of the class defined
        by instance name and allow the user to select the instance to
        delete.
        Otherwise attempt to delete the instance defined by instancename
    """
    try:
        if options['interactive']:
            instancepath = pick_instance(context, instancename,
                                         namespace=options['namespace'])
            if not instancepath:
                return
        else:
            instancepath = parse_cim_namespace_str(instancename,
                                                   options['namespace'])
    except ValueError as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))

    try:
        context.conn.DeleteInstance(instancepath)

        click.echo('Deleted %s', instancepath)

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
        # TODO create log of instance created.
        context.conn.CreateInstance(new_inst, namespace=options['namespace'])

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_invokemethod(context, instancename, methodname,
                              options):
    """Create an instance and submit to wbemserver"""

    try:
        if options['interactive']:
            instancepath = pick_instance(context, instancename,
                                         options['namespace'])
            if not instancepath:
                return
        else:
            instancepath = parse_cim_namespace_str(instancename,
                                                   options['namespace'])
    except ValueError as ve:
        raise click.ClickException("%s: %s" % (ve.__class__.__name__, ve))

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
            results = context.conn.PyWbemcliEnumerateInstances(
                ClassName=classname,
                namespace=options['namespace'],
                LocalOnly=options['localonly'],
                DeepInheritance=options['deepinheritance'],
                IncludeQualifiers=options['includequalifiers'],
                IncludeClassOrigin=options['includeclassorigin'],
                PropertyList=resolve_propertylist(options['propertylist']))

            if options['sort']:
                results = objects_sort(results)

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'])

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

    try:
        if options['names_only']:
            results = context.conn.PyWbemcliReferenceInstancePaths(
                instancepath,
                ResultClass=options['resultclass'],
                Role=options['role'])
            if options['sort']:
                results.sort()
        else:
            results = context.conn.PyWbemcliReferenceInstances(
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

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'])

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
            results = context.conn.PyWbemcliAssociatorInstancePaths(
                instancepath,
                AssocClass=options['assocclass'],
                Role=options['role'],
                ResultClass=options['resultclass'],
                ResultRole=options['resultrole'])
            if options['sort']:
                results.sort()
        else:
            results = context.conn.PyWbemcliAssociatorInstances(
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

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'])

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_count(context, classname, options):
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
    try:
        classlist = context.conn.EnumerateClassNames(
            DeepInheritance=True,
            namespace=namespace)
    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))

    if classname:
        classlist = filter_namelist(classname, classlist, ignore_case=True)

    # sort  since normal output for this command is by class alphabetic order.
    classlist.sort()

    maxlen = maxlen(classlist)    # get max classname size for display

    display_data = []
    for classname_ in classlist:

        # Try block allows issues where enumerate does not properly execute
        # in some cases. The totals may be wrong but at least it gets what
        # it can.  This accounts for issues with some servers where there
        # are providers that return errors from the enumerate.
        try:
            inst_names = context.conn.EnumerateInstanceNames(
                classname_,
                namespace=namespace)
        except Error as er:
            click.echo('Server Error %s with %s:%s. Continuing' %
                       (er, namespace, classname))

        # Sum the number of instances with the defined classname.
        # this counts only classes with that specific classname and not
        # subclasses
        count = sum(1 for inst in inst_names if (inst.classname == classname))

        if count != 0:
            display_tuple = (classname, count)
            display_data.append(display_tuple)

    # If sort set, resort by count size
    if options['sort']:
        display_data.sort(key=lambda x: x[1])

    headers = ['Class', 'count']
    rows = []
    if display_data:
        for item in display_data:
            rows.append([item[0], item[1]])
    context.spinner.stop()
    click.echo(format_table(rows, headers,
                            table_format=context.output_format,
                            title='Count of instances per class'))


def cmd_instance_query(context, query, options):
    """Execute the query defined by the inputs"""

    try:
        results = context.conn.pyWbemcliQueryInstances(options['querylanguage'],
                                                       query,
                                                       options['namespace'])

        if options['sort']:
            results.sort(key=lambda x: x.classname)

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'])

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
