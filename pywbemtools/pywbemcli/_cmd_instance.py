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
Click Command definition for the class command group  which includes
cmds for get, enumerate, list of classes.
"""
from __future__ import absolute_import, print_function

import click
from pywbem import Error, CIMError, CIM_ERR_NOT_FOUND
from .pywbemcli import cli
from ._common import display_cim_objects, parse_wbemuri_str, \
    pick_instance, resolve_propertylist, create_ciminstance, \
    filter_namelist, CMD_OPTS_TXT, format_table, verify_operation, \
    process_invokemethod
from ._common_options import propertylist_option, names_only_option, \
    includeclassorigin_option, namespace_option, add_options, \
    summary_objects_option, verify_option
from .config import DEFAULT_QUERY_LANGUAGE


#
#   Common option definitions for instance group
#


# This is instance-only because the default is False for include-qualifiers
# on instances but True on classes
includequalifiers_option = [              # pylint: disable=invalid-name
    click.option('-q', '--include-qualifiers', is_flag=True, required=False,
                 help='If set, requests server to include qualifiers in the '
                 'returned instances. Not all servers return qualifiers on '
                 'instances')]

includequalifiersenum_option = [              # pylint: disable=invalid-name
    click.option('-q', '--include-qualifiers', is_flag=True, required=False,
                 help='If set, requests server to include qualifiers in the '
                 'returned instances. This command may use either pull '
                 'or traditional operations depending on the server '
                 'and the "--use-pull" general option. If pull operations '
                 'are used, qualifiers will not be included, even if this '
                 'option is specified. If traditional operations are used, '
                 'inclusion of qualifiers depends on the server.')]

# specific to instance because DeepInheritance differs between class and
# instance operations.
deepinheritance_option = [              # pylint: disable=invalid-name
    click.option('-d', '--deep-inheritance', is_flag=True, required=False,
                 help='If set, requests server to return properties in '
                      'subclasses of the target instances class. If option not '
                      'specified only properties from target class are '
                      'returned')]

localonlyget_option = [              # pylint: disable=invalid-name
    click.option('-l', '--local-only', is_flag=True, required=False,
                 help='Show only local properties of the instance. '
                 'Some servers may not process this parameter.')]

localonlyenum_option = [              # pylint: disable=invalid-name
    click.option('-l', '--local-only', is_flag=True, required=False,
                 help='Show only local properties of the instances. This '
                      'command may use either pull or traditional '
                      'operations depending on the server and the '
                      '--use-pull general option. If pull operations '
                      'are used, this parameters will not be included, even if '
                      'specified. If traditional operations are used, some '
                      'servers do not process the parameter.')]

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
                 help='Optional property names of the form name=value. '
                 'Multiple definitions allowed, one for each property to be '
                 'included in the createdinstance. Array property values '
                 'defined by comma-separated-values. EmbeddedInstance not '
                 'allowed.')]

filterquerylanguage_option = [              # pylint: disable=invalid-name
    click.option('--filter-query-language', type=str, required=False,
                 default=None,
                 help='A filter-query language to be used with a filter query '
                 'defined by --filter-query. (Default: None)')]

filterquery_option = [              # pylint: disable=invalid-name
    click.option('-f', '--filter-query', type=str, required=False,
                 default=None,
                 help='A filter query to be passed to the server if the pull '
                 'operations are used. If this option is defined and the '
                 '--filter-query-language is None, pywbemcli assumes DMTF:FQL. '
                 'If this option is defined and the traditional operations are '
                 'used, the filter is not sent to the server. See the '
                 'documentation for more information. (Default: None)')]


##########################################################################
#
#   Click command group  and command definitions
#
###########################################################################


@cli.group('instance', options_metavar=CMD_OPTS_TXT)
def instance_group():
    """
    Command group for CIM instances.

    This command group  defines commands to inspect instances, to invoke
    methods on instances, and to create and delete instances.

    Modification of instances is not currently supported.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'instance' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@instance_group.command('get', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@add_options(localonlyget_option)
@add_options(includequalifiers_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(namespace_option)
@add_options(interactive_option)
@click.pass_obj
def instance_get(context, instancename, **options):
    """
    Get an instance of a class.

    The instance can be specified in two ways:

    * By specifying an untyped WBEM URI of an instance path in the INSTANCENAME
      argument. The namespace in which the instance is looked up is the
      namespace specified in the WBEM URI, or otherwise the namespace specified
      in the --namespace option, or otherwise the default namespace of the
      connection. Any host name in the WBEM URI will be ignored.

    * By specifying the --interactive option and a class name in the
      INSTANCENAME argument. The instances of the specified class are displayed
      and the user is prompted for an index number to select an instance.
      The namespace in which the instances are looked up is the namespace
      specified in the --namespace option, or otherwise the default namespace
      of the connection.

    In the output, the instance will formatted as defined by the
    --output-format general option.
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
    Delete an instance of a class.

    The CIM instance to be deleted can be specified as follows:

    1. By specifying an untyped WBEM URI of an instance path in the INSTANCENAME
    argument. The CIM namespace in which the instance is looked up is the
    namespace specified in the WBEM URI, or otherwise the namespace specified
    in the --namespace option, or otherwise the default namespace of the
    connection. Any host name in the WBEM URI will be ignored.

    2. By specifying the --interactive option and a CIM class name in the
    INSTANCENAME argument. The instances of the specified class are displayed
    and the user is prompted for an index number to select an instance.
    The CIM namespace in which the instances are looked up is the namespace
    specified in the --namespace option, or otherwise the default namespace
    of the connection.
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
    Create an instance of a class in a namespace.

    Create a CIM instance of the specified creation class (CLASSNAME
    argument) in the specified CIM namespace (--namespace option), with
    the specified properties (--property options) and display the CIM instance
    path of the created instance. If no namespace was specified, the default
    namespace of the connection is used.

    The properties to be initialized and their new values are specified using
    the --property option, which can be specified multiple times.

    Pywbemcli retrieves the class definition from the server in order to
    verify that the specified properties are consistent with the property
    characteristics in the class definition.

    Example:

      pywbemcli instance create CIM_blah -p id=3 -p strp="bla bla"
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
    Modify an instance of a class.

    The CIM instance to be modified can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the INSTANCENAME
    argument. The CIM namespace in which the instance is looked up is the
    namespace specified in the WBEM URI, or otherwise the namespace specified
    in the --namespace option, or otherwise the default namespace of the
    connection. Any host name in the WBEM URI will be ignored.

    2. By specifying the --interactive option and a CIM class name in the
    INSTANCENAME argument. The instances of the specified class are displayed
    and the user is prompted for an index number to select an instance.
    The CIM namespace in which the instances are looked up is the namespace
    specified in the --namespace option, or otherwise the default namespace
    of the connection.

    The properties to be modified and their new values are specified using the
    --property option, which can be specified multiple times.

    Example:

      pywbemcli instance modify CIM_blah.fred=3 -p id=3 -p strp="bla bla"
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
    Invoke a method on an instance.

    Invoke a CIM method (METHODNAME argument) on a CIM instance with the
    specified input parameters (--parameter options), and display the method
    return value and output parameters.

    The CIM instance can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the INSTANCENAME
    argument. The CIM namespace in which the instance is looked up is the
    namespace specified in the WBEM URI, or otherwise the namespace specified
    in the --namespace option, or otherwise the default namespace of the
    connection. Any host name in the WBEM URI will be ignored.

    2. By specifying the --interactive option and a CIM class name in the
    INSTANCENAME argument. The instances of the specified class are displayed
    and the user is prompted for an index number to select an instance.
    The CIM namespace in which the instances are looked up is the namespace
    specified in the --namespace option, or otherwise the default namespace
    of the connection.

    The method input parameters are specified using the --parameter option,
    which can be specified multiple times.

    Pywbemcli retrieves the class definition of the creation class of the
    instance from the server in order to verify that the specified input
    parameters are consistent with the parameter characteristics in the method
    definition.

    Use the 'class invokemethod' command to invoke CIM methods on CIM classes.

    Example:

      pywbemcli -n myconn instance invokemethod CIM_x.id='hi" methodx -p id=3
    """
    context.execute_cmd(lambda: cmd_instance_invokemethod(context,
                                                          instancename,
                                                          methodname,
                                                          options))


@instance_group.command('enumerate', options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@add_options(localonlyenum_option)
@add_options(deepinheritance_option)
@add_options(includequalifiersenum_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(namespace_option)
@add_options(names_only_option)
@add_options(summary_objects_option)
@add_options(filterquery_option)
@add_options(filterquerylanguage_option)
@click.pass_obj
def instance_enumerate(context, classname, **options):
    """
    List the instances of a class.

    Enumerate the CIM instances of the specified class (CLASSNAME argument),
    including instances of subclasses in the specified CIM namespace
    (--namespace option), and display the returned instances, or instance paths
    if --names-only was specified. If no namespace was specified, the default
    namespace of the connection is used.

    The instances to be retrieved can be filtered by the --filter-query option.

    The --local-only, --deep-inheritance, --include-qualifiers,
    --include-classorigin, and --propertylist options determine which parts
    are included in each retrieved instance.

    The --names-only option can be used to show only the instance paths.

    In the output, the instances and instance paths will be formatted as
    defined by the --output-format general option. Table formats on instances
    will be replaced with MOF format.
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
                   'through a property with a name that matches the value of '
                   'this parameter. Optional.')
@add_options(includequalifiersenum_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(interactive_option)
@add_options(summary_objects_option)
@add_options(filterquery_option)
@add_options(filterquerylanguage_option)
@click.pass_obj
def instance_references(context, instancename, **options):
    """
    List the instances referencing an instance.

    List the CIM (association) instances that reference the specified CIM
    instance, and display the returned instances, or instance paths if
    --names-only was specified.

    The CIM instance can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the INSTANCENAME
    argument. The CIM namespace in which the instance is looked up is the
    namespace specified in the WBEM URI, or otherwise the namespace specified
    in the --namespace option, or otherwise the default namespace of the
    connection. Any host name in the WBEM URI will be ignored.

    2. By specifying the --interactive option and a CIM class name in the
    INSTANCENAME argument. The instances of the specified class are displayed
    and the user is prompted for an index number to select an instance.
    The CIM namespace in which the instances are looked up is the namespace
    specified in the --namespace option, or otherwise the default namespace
    of the connection.

    The instances to be retrieved can be filtered by the --filter-query, --role
    and --result-class options.

    The --include-qualifiers, --include-classorigin, and --propertylist options
    determine which parts are included in each retrieved instance.

    The --names-only option can be used to show only the instance paths.

    In the output, the instances and instance paths will be formatted as
    defined by the --output-format general option. Table formats on instances
    will be replaced with MOF format.
    """
    context.execute_cmd(lambda: cmd_instance_references(context, instancename,
                                                        options))


@instance_group.command('associators', options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('-a', '--assoc-class', type=str, required=False,
              metavar='<class name>',
              help='Filter by the association class name provided.Each '
                   'returned instance (or instance name) should be associated '
                   'to the source instance through this class or its '
                   'subclasses. Optional.')
@click.option('-c', '--result-class', type=str, required=False,
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
@click.option('-R', '--result-role', type=str, required=False,
              metavar='<role name>',
              help='Filter by the result role name provided. Each returned '
              'instance (or instance name)should be associated with the source '
              ' instance name (`INSTANCENAME`) through an association with '
              'returned object having this role (property name in the '
              'association that matches this parameter). Optional.')
@add_options(includequalifiersenum_option)
@add_options(includeclassorigin_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(interactive_option)
@add_options(summary_objects_option)
@add_options(filterquery_option)
@add_options(filterquerylanguage_option)
@click.pass_obj
def instance_associators(context, instancename, **options):
    """
    List the instances associated with an instance.

    List the CIM instances that are associated with the specified CIM instance,
    and display the returned instances, or instance paths if --names-only was
    specified.

    The CIM instance can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the INSTANCENAME
    argument. The CIM namespace in which the instance is looked up is the
    namespace specified in the WBEM URI, or otherwise the namespace specified
    in the --namespace option, or otherwise the default namespace of the
    connection. Any host name in the WBEM URI will be ignored.

    2. By specifying the --interactive option and a CIM class name in the
    INSTANCENAME argument. The instances of the specified class are displayed
    and the user is prompted for an index number to select an instance.
    The CIM namespace in which the instances are looked up is the namespace
    specified in the --namespace option, or otherwise the default namespace
    of the connection.

    The instances to be retrieved can be filtered by the --filter-query,
    --role, --result-role, --assoc-class, and --result-class options.

    The --include-qualifiers, --include-classorigin, and --propertylist options
    determine which parts are included in each retrieved instance.

    The --names-only option can be used to show only the instance paths.

    In the output, the instances and instance paths will be formatted as
    defined by the --output-format general option. Table formats on instances
    will be replaced with MOF format.
    """
    context.execute_cmd(lambda: cmd_instance_associators(context, instancename,
                                                         options))


@instance_group.command('query', options_metavar=CMD_OPTS_TXT)
@click.argument('query', type=str, required=True, metavar='QUERY_STRING')
@click.option('-l', '--query-language', type=str, required=False,
              metavar='QUERY LANGUAGE', default=DEFAULT_QUERY_LANGUAGE,
              help='Use the query language defined. '
                   '(Default: {of}.'.format(of=DEFAULT_QUERY_LANGUAGE))
@add_options(namespace_option)
@add_options(summary_objects_option)
@click.pass_obj
def instance_query(context, query, **options):
    """
    Execute a query on instances in a namespace.

    Execute the specified query (QUERY_STRING argument) in the specified CIM
    namespace (--namespace option), and display the returned instances. If no
    namespace was specified, the default namespace of the connection is used.

    In the output, the instances will formatted as defined by the
    --output-format general option.
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
    Count the instances of each class with matching class name.

    Display the count of the instances of each CIM class whose class name
    matches the specified wildcard expression (CLASSNAME-GLOB) in all CIM
    namespaces of the WBEM server, or in the specified namespace
    (--namespace option).

    The CLASSNAME-GLOB argument is a wildcard expression that is matched on
    the class names case insensitively. The special characters known from file
    nme wildcarding are supported: `*` to match zero or more characters, and
    `?` to match a single character. In order to not have the shell expand
    the wildcards, the CLASSNAME-GLOB argument should be put in quotes.

    For example, `pywbem_*` returns classes whose name begins with `PyWBEM_`,
    `pywbem_`, etc. '*system*' returns classes whose names include the case
    insensitive string `system`.

    This operation can take a long time to execute since it potentially
    enumerates all classes in all namespaces.
    """
    context.execute_cmd(lambda: cmd_instance_count(context, classname, options))


####################################################################
#
#  cmd_instance_<action> processors
#
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
            ns = options.get('namespace', context.conn.default_namespace)

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
            LocalOnly=options['local_only'],
            IncludeQualifiers=options['include_qualifiers'],
            IncludeClassOrigin=options['include_classorigin'],
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
            ns = options['namespace'] or context.conn.default_namespace
            raise click.ClickException('CIMClass: "%s" does not exist in '
                                       'namespace "%s" in WEB '
                                       'server: %s.'
                                       % (classname, ns, context.conn))

        raise click.ClickException('Exception %s' % ce)
    except Error as er:
        raise click.ClickException('Exception %s' % er)

    properties = options['property']

    # properties is a tuple of name,value pairs
    new_inst = create_ciminstance(class_, properties)

    if options['verify']:
        context.spinner.stop()
        click.echo(new_inst.tomof())
        if not verify_operation("Execute CreateInstance", msg=True):
            return
    try:
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
                                          context.conn.url))

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
        if not verify_operation("Execute ModifyInstance", msg=True):
            return

    try:
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


def get_filterquerylanguage(options):
    """
    Get the filterquery language based on what is in the filterquery option
    and the filterquerylanguage options.
    If filterquery exists but filterquerylanguage does not, use DMTF as
    the filter query language.
    if filterquery does not exist but filterquerylanguage does, just return it
    """
    if options['filter_query']:
        fql = options['filter_query_language'] or 'DMTF:FQL'
    else:
        fql = options['filter_query_language']
    return fql


def cmd_instance_enumerate(context, classname, options):
    """
    Enumerate CIM instances or CIM instance names

    """
    try:
        if options['names_only']:
            results = context.conn.PyWbemcliEnumerateInstancePaths(
                ClassName=classname,
                namespace=options['namespace'],
                FilterQuery=options['filter_query'],
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pull_max_cnt)
        else:
            results = context.conn.PyWbemcliEnumerateInstances(
                ClassName=classname,
                namespace=options['namespace'],
                LocalOnly=options['local_only'],
                IncludeQualifiers=options['include_qualifiers'],
                DeepInheritance=options['deep_inheritance'],
                IncludeClassOrigin=options['include_classorigin'],
                FilterQuery=options['filter_query'],
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pull_max_cnt,
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=True)

    except (Error) as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
    except ValueError as ve:
        raise click.ClickException('instance enumerate failed because '
                                   'FilterQuery not allowed with traditional '
                                   'EnumerateInstance. --use-pull: '
                                   '%s. Exception: %s: %s' %
                                   (context.use_pull,
                                    ve.__class__.__name__, ve))


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
                Role=options['role'],
                FilterQuery=options['filter_query'],
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pull_max_cnt)
        else:
            results = context.conn.PyWbemcliReferenceInstances(
                instancepath,
                ResultClass=options['resultclass'],
                Role=options['role'],
                IncludeQualifiers=options["include_qualifiers"],
                IncludeClassOrigin=options['include_classorigin'],
                FilterQuery=options['filter_query'],
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pull_max_cnt,
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=True)

    except (Error) as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
    except ValueError as ve:
        raise click.ClickException('instance references failed because '
                                   'FilterQuery not allowed with traditional '
                                   'References. --use-pull: '
                                   '%s. Exception: %s: %s' %
                                   (context.use_pull,
                                    ve.__class__.__name__, ve))


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
                AssocClass=options['assoc_class'],
                Role=options['role'],
                ResultClass=options['result_class'],
                ResultRole=options['result_role'],
                FilterQuery=options['filter_query'],
                MaxObjectCount=context.pull_max_cnt,
                FilterQueryLanguage=get_filterquerylanguage(options))
        else:
            results = context.conn.PyWbemcliAssociatorInstances(
                instancepath,
                AssocClass=options['assoc_class'],
                Role=options['role'],
                ResultClass=options['result_class'],
                ResultRole=options['result_role'],
                IncludeQualifiers=options["include_qualifiers"],
                IncludeClassOrigin=options['include_classorigin'],
                FilterQuery=options['filter_query'],
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pull_max_cnt,
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=True)

    except (Error) as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
    except ValueError as ve:
        raise click.ClickException('instance associators failed because '
                                   'FilterQuery not allowed with traditional '
                                   'Associators. --use-pull: '
                                   '%s. Exception: %s: %s' %
                                   (context.use_pull,
                                    ve.__class__.__name__, ve))


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
        results = context.conn.PyWbemcliQueryInstances(
            options['query_language'],
            query,
            namespace=options['namespace'],
            MaxObjectCount=context.pull_max_cnt)

        display_cim_objects(context, results, context.output_format,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise click.ClickException("%s: %s" % (er.__class__.__name__, er))
