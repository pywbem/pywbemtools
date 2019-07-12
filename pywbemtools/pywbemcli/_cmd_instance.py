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
from pywbem import Error, CIMError, CIM_ERR_NOT_FOUND
from .pywbemcli import cli
from ._common import display_cim_objects, parse_wbemuri_str, \
    pick_instance, sort_cimobjects, resolve_propertylist, create_ciminstance, \
    filter_namelist, CMD_OPTS_TXT, format_table, verify_operation, \
    process_invokemethod
from ._common_options import propertylist_option, names_only_option, \
    sort_option, includeclassorigin_option, namespace_option, add_options, \
    summary_objects_option, verify_option
from .config import DEFAULT_QUERY_LANGUAGE


#
#   Common option definitions for instance group
#


# This is instance-only because the default is False for includequalifiers
# on instances but True on classes
includequalifiers_option = [              # pylint: disable=invalid-name
    click.option('-q', '--includequalifiers', is_flag=True, required=False,
                 help='If set, requests server to include qualifiers in the '
                 'returned instance(s).')]

# specific to instance because deepinheritance differs between class and
# instance operations.
deepinheritance_option = [              # pylint: disable=invalid-name
    click.option('-d', '--deepinheritance', is_flag=True, required=False,
                 help='If set, requests server to return properties in '
                      'subclasses of the target instances class. If option not '
                      'specified only properties from target class are '
                      'returned')]

interactive_option = [              # pylint: disable=invalid-name
    click.option('-i', '--interactive', is_flag=True, required=False,
                 help='If set, `INSTANCENAME` argument must be a class rather '
                      'than an instance and user is presented with a list of '
                      'instances of the class from which the instance to '
                      'process is selected.')]

instance_property_option = [              # pylint: disable=invalid-name
    click.option('-P', '--property', type=str, metavar='name=value',
                 required=False,
                 multiple=True,
                 help='Optional property definitions of the form name=value.'
                 'Multiple definitions allowed, one for each property to be '
                 'included in the createdinstance. Array property values '
                 'defined by comma-separated-values. EmbeddedInstance not '
                 'allowed.')]


@cli.group('instance', options_metavar=CMD_OPTS_TXT)
def instance_group():
    """
    Command group to manage CIM instances.

    This incudes functions to get, enumerate, create, modify, and delete
    instances in a namspace and additional functions to get more general
    information on instances (ex. counts) within the namespace

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
              help='Include class origin attribute in returned instance(s).')
@add_options(propertylist_option)
@add_options(namespace_option)
@add_options(interactive_option)
@click.pass_obj
def instance_get(context, instancename, **options):
    """
    Get a single CIMInstance.

    Gets the instance defined by `INSTANCENAME` where `INSTANCENAME` must
    resolve to the instance name of the desired instance. This may be supplied
    directly as an untyped wbem_uri formatted string or through the
    --interactive option. The wbemuri may contain the namespace or the namespace
    can be supplied with the --namespace option. If no namespace is supplied,
    the connection default namespace is used.  Any host name in the wbem_uri is
    ignored.

    This method may be executed interactively by providing only a classname and
    the interactive option (-i).

    Otherwise the INSTANCENAME must be a CIM instance name in the format
    defined by DMTF `DSP0207`.

    Results are formatted as defined by the output format global option.
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

    Otherwise the INSTANCENAME must be a CIM instance name in the format
    defined by DMTF `DSP0207`.
    """
    context.execute_cmd(lambda: cmd_instance_delete(context, instancename,
                                                    options))


@instance_group.command('create', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@add_options(instance_property_option)
@add_options(verify_option)
@add_options(namespace_option)
@click.pass_obj
def instance_create(context, classname, **options):
    """
    Create a CIM instance of CLASSNAME.

    Creates an instance of the class CLASSNAME with the properties defined
    in the property option.

    Pywbemcli creates the new instance using CLASSNAME retrieved from the
    current WBEM server as a template for property characteristics. Therefore
    pywbemcli will generate an exception if CLASSNAME does not exist in the
    current WBEM Server or if the data definition in the properties options
    does not match the properties characteristics defined the returned class.

    ex. pywbemcli instance create CIM_blah -p id=3 -p strp="bla bla", -p p3=3
    """
    context.execute_cmd(lambda: cmd_instance_create(context, classname,
                                                    options))


@instance_group.command('modify', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@add_options(instance_property_option)
@click.option('-p', '--propertylist', multiple=True, type=str,
              default=None, metavar='<property name>',
              help='Define a propertylist for the request. If option '
                   'not specified a Null property list is created. Multiple '
                   'properties may be defined with either a comma '
                   'separated list defining the option multiple times. '
                   '(ex: -p pn1 -p pn22 or -p pn1,pn2). If defined as '
                   'empty string an empty propertylist is created. The '
                   'server uses the propertylist to limit changes made to '
                   'the instance to properties in the propertylist.')
@add_options(interactive_option)
@add_options(verify_option)
@add_options(namespace_option)
@click.pass_obj
def instance_modify(context, instancename, **options):
    """
    Modify an existing instance.

    Modifies CIM instance defined by INSTANCENAME in the WBEM server using the
    property names and values defined by the property option and the CIM class
    defined by the instance name.  The propertylist option if provided is
    passed to the WBEM server as part of the ModifyInstance operation (normally
    the WBEM server limits modifications) to just those properties defined in
    the property list.

    INSTANCENAME must be a CIM instance name in the format defined by DMTF
    `DSP0207`.

    Pywbemcli builds only the properties defined with the --property option
    into an instance based on the CIMClass and forwards that to the WBEM
    server with the ModifyInstance method.

    ex. pywbemcli instance modify CIM_blah.fred=3 -p id=3 -p strp="bla bla"
    """
    context.execute_cmd(lambda: cmd_instance_modify(context, instancename,
                                                    options))


@instance_group.command('invokemethod', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.argument('methodname', type=str, metavar='METHODNAME', required=True)
@click.option('-p', '--parameter', type=str, metavar='name=value',
              required=False, multiple=True,
              help='Multiple definitions allowed, one for each parameter to be '
                   'included in the new instance. Array parameter values '
                   'defined by comma-separated-values. EmbeddedInstance not '
                   'allowed.')
@add_options(interactive_option)
@add_options(namespace_option)
@click.pass_obj
def instance_invokemethod(context, instancename, methodname, **options):
    """
    Invoke a CIM method on a CIMInstance.

    Invoke the method defined by INSTANCENAME and METHODNAME arguments with
    parameters defined by the --parameter options.

    This issues an instance level invokemethod request and displays the
    results.

    INSTANCENAME must be a CIM instance name in the format defined by  DMTF
    `DSP0207`.

    Pywbemcli creates the method call using the class in INSTANCENAME retrieved
    from the current WBEM server as a template for parameter characteristics.
    Therefore pywbemcli will generate an exception if CLASSNAME does not exist
    in the current WBEM Server or if the data definition in the parameter
    options does not match the parameter characteristics defined the returned
    class.

    A class level invoke method is available as `pywbemcli class invokemethod`.

    Example:

    pywbmcli instance invokemethod  CIM_x.InstanceID='hi" methodx -p id=3
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

    Get CIMInstance or CIMInstanceName (--name_only option) objects from
    the WBEMServer starting either at the top  of the hierarchy (if no
    CLASSNAME provided) or from the CLASSNAME argument if provided.

    Displays the returned instances in mof, xml, or table formats or the
    instance names as a string or XML formats (--names-only option).

    Results are formatted as defined by the output format global option.

    """
    context.execute_cmd(lambda: cmd_instance_enumerate(context, classname,
                                                       options))


@instance_group.command('references', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('-R', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result class name provided. Each returned '
                   'instance (or instance name) should be a member of this '
                   'class or its subclasses. Optional')
@click.option('-r', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided. Each returned instance '
                   '(or instance name) should refer to the target instance '
                   'through a property with aname that matches the value of '
                   'this parameter. Optional.')
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
    target `INSTANCENAME` in the target WBEM server filtered by the
    `role` and `resultclass` options.

    INSTANCENAME must be a CIM instance name in the format defined by DMTF
    `DSP0207`.

    This may be executed interactively by providing only a class name for
    `INSTANCENAME` and the `interactive` option(-i). Pywbemcli presents a list
    of instances names in the class from which you can be chosen as the target.

    Results are formatted as defined by the output format global option.
    """
    context.execute_cmd(lambda: cmd_instance_references(context, instancename,
                                                        options))


@instance_group.command('associators', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('-a', '--assocclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the association class name provided.Each '
                   'returned instance (or instance name) should be associated '
                   'to the source instance through this class or its '
                   'subclasses. Optional.')
@click.option('-c', '--resultclass', type=str, required=False,
              metavar='<class name>',
              help='Filter by the result class name provided. Each '
                   'returned instance (or instance name) should be a member '
                   'of this class or one of its subclasses. Optional')
@click.option('-r', '--role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the role name provided. Each returned instance '
              '(or instance name)should be associated with the source instance '
              '(INSTANCENAME) through an association with this role (property '
              'name in the association that matches this parameter). Optional.')
@click.option('-R', '--resultrole', type=str, required=False,
              metavar='<role name>',
              help='Filter by the result role name provided. Each returned '
              'instance (or instance name)should be associated with the source '
              ' instance name (`INSTANCENAME`) through an association with '
              'returned object having this role (property name in the '
              'association that matches this parameter). Optional.')
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
    `INSTANCENAME` argument filtered by the --assocclass, --resultclass, --role
    and --resultrole options.

    INSTANCENAME must be a CIM instance name in the format defined by DMTF
    `DSP0207`.

    This may be executed interactively by providing only a classname and the
    interactive option. Pywbemcli presents a list of instances in the class
    from which one can be chosen as the target.

    Results are formatted as defined by the output format global option.
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

    Results are formatted as defined by the output format global option.

    """
    context.execute_cmd(lambda: cmd_instance_query(context, query, options))


@instance_group.command('count', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME-GLOB',
                required=False)
@click.option('-s', '--sort', is_flag=True, required=False,
              help='Sort by instance count. Otherwise sorted by classname')
@add_options(namespace_option)
@click.pass_obj
def instance_count(context, classname, **options):
    """
    Get instance count for classes.

    Displays the count of instances for the classes defined by the
    `CLASSNAME-GLOB` argument in one or more namespaces.

    The size of the response may be limited by CLASSNAME-GLOB argument which
    defines a regular expression based on the desired class names so that only
    classes that match the regex are counted. The CLASSNAME-GLOB argument is
    optional.

    The CLASSNAME-GLOB argument may be either a complete classname or a regular
    expression that can be matched to one or more classnames. To limit the
    filter to a single classname, terminate the classname with $.

    The GLOB expression is anchored to the beginning of the CLASSNAME-GLOB, is
    is case insensitive and uses the standard GLOB special characters
    (*(match everything), ?(match single character)).
    Thus, `pywbem_*` returns all classes that begin with
    `PyWBEM_`, `pywbem_`, etc. '.*system*' returns classnames that include
    the case insensitive string `system`.

    This operation can take a long time to execute since it enumerates all
    classes in the namespace.
    """
    context.execute_cmd(lambda: cmd_instance_count(context, classname, options))


####################################################################
#  cmd_instance_<action> processors
####################################################################

def get_instancename(context, instancename, options):
    """
    Common function to get the instancename from either the input or the user.

    Returns:
     CIMInstanceName with namespace retrieved either from the namespace option
     in options dictionary or the connection default_namespace.
    """
    try:
        if options['interactive']:
            if 'namespace' in options:
                ns = options['namespace']
            else:
                ns = None

            if ns is None:
                ns = context.conn.default_namespace
            try:
                instancepath = pick_instance(context, instancename,
                                             namespace=ns)
                return instancepath
            except ValueError:
                click.echo('Function aborted')
                return None

        else:
            instancepath = parse_wbemuri_str(instancename, options['namespace'])
        return instancepath

    except ValueError as ve:
        raise click.ClickException("%s: %s" % (ve.__class__.__name__, ve))


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
    instancepath = get_instancename(context, instancename, options)
    if instancepath is None:
        return

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
    instancepath = get_instancename(context, instancename, options)
    if instancepath is None:
        return

    try:
        context.conn.DeleteInstance(instancepath)

        if context.verbose:
            click.echo('Deleted %s' % instancepath)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_create(context, classname, options):
    """Create an instance and submit to wbemserver.
       If successful, this operation returns the new instance name. Otherwise
       it raises an exception
    """
    try:
        class_ = context.conn.GetClass(
            classname, namespace=options['namespace'], LocalOnly=False)
    except CIMError as ce:
        if ce.status_code == CIM_ERR_NOT_FOUND:
            ns = options['namespace'] if options['namespace'] else \
                context.conn.default_namespace
            raise click.ClickException('CIMClass: "%s" does not exist in '
                                       'namespace "%s" in WEB '
                                       'server: %s.'
                                       % (classname, ns, context.conn))
        else:
            raise click.ClickException('Exception %s' % ce)
    except Error as er:
        raise click.ClickException('Exception %s' % er)

    properties = options['property']

    # properties is a tuple of name,value pairs
    new_inst = create_ciminstance(class_, properties)

    if options['verify']:
        context.spinner.stop()
        click.echo(new_inst.tomof())
        if not verify_operation("Execute CreateInstance operation"):
            return
    try:
        # TODO: Future Possibly create log of instance created.
        name = context.conn.CreateInstance(new_inst,
                                           namespace=options['namespace'])

        context.spinner.stop()
        click.echo("%s" % name)
    except Error as er:
        raise click.ClickException("Server Error creating instance. Exception: "
                                   "%s: %s" % (er.__class__.__name__, er))


def cmd_instance_modify(context, instancename, options):
    """
    Build an instance defined by the options and submit to wbemserver
    as a ModifyInstance method.

    In order to make a correct instance, this method first gets the
    corresponding class and uses that as the template for creating the intance.
    The class provides property names, types, array flags, etc. to assure
    that the instance is correctly built.

    If successful, this operation returns nothing.
    """
    # This function resolves any issues between namespace in instancename and
    # the namespace option.
    instancepath = get_instancename(context, instancename, options)
    if instancepath is None:
        return

    try:
        class_ = context.conn.GetClass(
            instancepath.classname, LocalOnly=False)
    except CIMError as ce:
        if ce.status_code == CIM_ERR_NOT_FOUND:
            raise click.ClickException('CIMClass: %r does not exist in WEB '
                                       'server: %s'
                                       % (instancepath.classname,
                                          context.conn.uri))
        else:
            raise click.ClickException('Exception %s' % ce)
    except Error as er:
        raise click.ClickException('Exception %s' % er)

    property_list = resolve_propertylist(options['propertylist'])

    # properties is a tuple of name,value pairs
    modified_inst = create_ciminstance(class_, options['property'])

    modified_inst.path = instancepath

    if options['verify']:
        context.spinner.stop()
        click.echo(modified_inst.tomof())
        if not verify_operation("Execute ModifyInstance operation", msg=True):
            return

    try:
        # TODO: Future Possibly create log of instance modified.
        context.conn.ModifyInstance(modified_inst,
                                    PropertyList=property_list)
    except Error as er:
        raise click.ClickException("Server Error modifying instance. "
                                   "Exception: %s: %s" %
                                   (er.__class__.__name__, er))


def cmd_instance_invokemethod(context, instancename, methodname,
                              options):
    """Create an instance and submit to wbemserver"""
    instancepath = get_instancename(context, instancename, options)
    if instancepath is None:
        return

    try:
        process_invokemethod(context, instancepath, methodname, options)
    except Exception as ex:
        raise click.ClickException("%s: %s" % (ex.__class__.__name__, ex))


def cmd_instance_enumerate(context, classname, options):
    """
    Enumerate CIM instances or CIM instance names

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
                results = sort_cimobjects(results)

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
    instancepath = get_instancename(context, instancename, options)
    if instancepath is None:
        return

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
            results = sort_cimobjects(results)

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'])

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))


def cmd_instance_associators(context, instancename, options):
    """
    Execute the references request operation to get references for
    the classname defined
    """
    instancepath = get_instancename(context, instancename, options)
    if instancepath is None:
        return

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
        count = sum(1 for inst in inst_names if (inst.classname == classname_))

        if count != 0:
            display_tuple = (classname_, count)
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
                            title='Count of instances per class',
                            table_format=context.output_format))


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
