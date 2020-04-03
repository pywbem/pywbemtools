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
Click Command definition for the instance command group which includes
cmds for get, enumerate, list of instance.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

import re
import click

from pywbem import Error, CIMError, CIM_ERR_NOT_FOUND

from .pywbemcli import cli
from ._common import display_cim_objects, parse_wbemuri_str, \
    pick_instance, resolve_propertylist, create_ciminstance, \
    filter_namelist, format_table, verify_operation, \
    process_invokemethod, raise_pywbem_error_exception, \
    create_ciminstancename, warning_msg, validate_output_format, \
    CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT

from ._common_options import add_options, propertylist_option, \
    names_only_option, include_classorigin_instance_option, namespace_option, \
    summary_option, verify_option, multiple_namespaces_option, \
    association_filter_option, indication_filter_option, \
    experimental_filter_option

from ._association_shrub import AssociationShrub

from .config import DEFAULT_QUERY_LANGUAGE
from ._click_extensions import PywbemcliGroup, PywbemcliCommand
from ._cmd_class import get_namespaces, enumerate_classes_filtered

#
#   Common option definitions for instance group
#

# NOTE: A number of the options use double-dash as the short form.  In those
# cases, a third definition of the options without the double-dash defines
# the corresponding option name, ex. 'include_qualifiers'. It should be
# defined with underscore and not dash


# This is instance-only because the default is False for include-qualifiers
# on instances but True on classes
include_qualifiers_get_option = [              # pylint: disable=invalid-name
    click.option('--iq', '--include-qualifiers', 'include_qualifiers',
                 is_flag=True, required=False,
                 help='Include qualifiers in the returned instance. '
                      'Not all servers return qualifiers on instances. '
                      'Default: Do not include qualifiers.')]

include_qualifiers_list_option = [              # pylint: disable=invalid-name
    click.option('--iq', '--include-qualifiers', 'include_qualifiers',
                 is_flag=True, required=False,
                 help='When traditional operations are used, include '
                      'qualifiers in the returned instances. '
                      'Some servers may ignore this option. '
                      'By default, and when pull operations are used, '
                      'qualifiers will never be included.')]

# specific to instance because DeepInheritance differs between class and
# instance operations.
deep_inheritance_enum_option = [              # pylint: disable=invalid-name
    click.option('--di', '--deep-inheritance', 'deep_inheritance',
                 is_flag=True, required=False,
                 help='Include subclass properties in the returned '
                      'instances. '
                      'Default: Do not include subclass properties.')]

local_only_get_option = [              # pylint: disable=invalid-name
    click.option('--lo', '--local-only', 'local_only', is_flag=True,
                 required=False,
                 help='Do not include superclass properties in the returned '
                      'instance. '
                      'Some servers may ignore this option. '
                      'Default: Include superclass properties.')]

local_only_list_option = [              # pylint: disable=invalid-name
    click.option('--lo', '--local-only', 'local_only', is_flag=True,
                 required=False,
                 help='When traditional operations are used, do not include '
                      'superclass properties in the returned instances. '
                      'Some servers may ignore this option. '
                      'By default, and when pull operations are used, '
                      'superclass properties will always be included.')]

property_create_option = [              # pylint: disable=invalid-name
    click.option('-p', '--property', type=str, metavar='PROPERTYNAME=VALUE',
                 required=False, multiple=True,
                 help='Initial property value for the new instance. '
                      'May be specified multiple times. '
                      'Array property values are specified as a '
                      'comma-separated list; embedded instances are not '
                      'supported. '
                      'Default: No initial properties provided.')]

property_modify_option = [              # pylint: disable=invalid-name
    click.option('-p', '--property', type=str, metavar='PROPERTYNAME=VALUE',
                 required=False, multiple=True,
                 help='Property to be modified, with its new value. '
                      'May be specified once for each property to be '
                      'modified. '
                      'Array property values are specified as a '
                      'comma-separated list; embedded instances are not '
                      'supported. '
                      'Default: No properties modified.')]

keybinding_key_option = [              # pylint: disable=invalid-name
    click.option('-k', '--key', type=str, metavar='KEYNAME=VALUE',
                 required=False, multiple=True,
                 help='Value for a key in keybinding of CIM instance name. '
                      'May be specified multiple times. '
                      'Allows defining keys without the issues of quotes. '
                      'Default: No keybindings provided.')]

filter_query_language_option = [              # pylint: disable=invalid-name
    click.option('--fql', '--filter-query-language', 'filter_query_language',
                 type=str, metavar='QUERY-LANGUAGE', default=None,
                 help='The filter query language to be used with '
                      '--filter-query. '
                      'Default: DMTF:FQL.')]

filter_query_option = [              # pylint: disable=invalid-name
    click.option('--fq', '--filter-query', 'filter_query', type=str,
                 metavar='QUERY-STRING', default=None,
                 help='When pull operations are used, filter the instances in '
                      'the result via a filter query. '
                      'By default, and when traditional operations are used, '
                      'no such filtering takes place.')]


##########################################################################
#
#   Click command group and command definitions
#   These decorated functions implement the commands, arguments, and
#
###########################################################################


@cli.group('instance', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
def instance_group():
    """
    Command group for CIM instances.

    This command group defines commands to inspect instances, to invoke
    methods on instances, and to create and delete instances.

    Modification of instances is not currently supported.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'instance' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@instance_group.command('enumerate', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@add_options(local_only_list_option)
@add_options(deep_inheritance_enum_option)
@add_options(include_qualifiers_list_option)
@add_options(include_classorigin_instance_option)
@add_options(propertylist_option)
@add_options(namespace_option)
@add_options(names_only_option)
@add_options(summary_option)
@add_options(filter_query_option)
@add_options(filter_query_language_option)
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


@instance_group.command('get', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@add_options(local_only_get_option)
@add_options(include_qualifiers_get_option)
@add_options(include_classorigin_instance_option)
@add_options(propertylist_option)
@add_options(keybinding_key_option)
@add_options(namespace_option)
@click.pass_obj
def instance_get(context, instancename, **options):
    """
    Get an instance of a class.

    The instance can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the
    INSTANCENAME argument. The CIM namespace in which the instance is looked up
    is the namespace specified in the WBEM URI, or otherwise the namespace
    specified in the --namespace option, or otherwise the default namespace of
    the connection. Any host name in the WBEM URI will be ignored.

    2. By specifying a class name with wildcard for the keys in the
    INSTANCENAME argument, i.e. "CLASSNAME.?". The instances of the specified
    class are displayed and the user is prompted for an index number to select
    an instance. The namespace in which the instances are looked up is the
    namespace specified in the --namespace option, or otherwise the default
    namespace of the connection.

    The --local-only, --include-qualifiers, --include-classorigin, and
    --propertylist options determine which parts are included in the retrieved
    instance.

    In the output, the instance will formatted as defined by the
    --output-format general option.
    """
    context.execute_cmd(lambda: cmd_instance_get(context, instancename,
                                                 options))


@instance_group.command('delete', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@add_options(keybinding_key_option)
@add_options(namespace_option)
@click.pass_obj
def instance_delete(context, instancename, **options):
    """
    Delete an instance of a class.

    The CIM instance to be deleted can be specified as follows:

    1. By specifying an untyped WBEM URI of an instance path in the
    INSTANCENAME argument. The CIM namespace in which the instance is looked up
    is the namespace specified in the WBEM URI, or otherwise the namespace
    specified in the --namespace option, or otherwise the default namespace of
    the connection. Any host name in the WBEM URI will be ignored.

    2. By specifying a class name with wildcard for the keys in the
    INSTANCENAME argument, i.e. "CLASSNAME.?". The instances of the specified
    class are displayed and the user is prompted for an index number to select
    an instance. The namespace in which the instances are looked up is the
    namespace specified in the --namespace option, or otherwise the default
    namespace of the connection.
    """
    context.execute_cmd(lambda: cmd_instance_delete(context, instancename,
                                                    options))


@instance_group.command('create', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@add_options(property_create_option)
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
    the --property option, which may be specified multiple times.

    Pywbemcli retrieves the class definition from the server in order to
    verify that the specified properties are consistent with the property
    characteristics in the class definition.

    Example:

      pywbemcli instance create CIM_blah -P id=3 -P arr="bla bla",foo
    """
    context.execute_cmd(lambda: cmd_instance_create(context, classname,
                                                    options))


@instance_group.command('modify', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@add_options(property_modify_option)
@click.option('--pl', '--propertylist', 'propertylist', multiple=True, type=str,
              default=None, required=False, metavar='PROPERTYLIST',
              help='Reduce the properties to be modified (as per '
              '--property) to a specific property list. '
              'Multiple properties may be specified with either a '
              'comma-separated list or by using the option multiple '
              'times. The empty string will cause no properties to '
              'be modified. '
              'Default: Do not reduce the properties to be modified.')
@add_options(verify_option)
@add_options(keybinding_key_option)
@add_options(namespace_option)
@click.pass_obj
def instance_modify(context, instancename, **options):
    """
    Modify properties of an instance.

    The CIM instance to be modified can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the
    INSTANCENAME argument. The CIM namespace in which the instance is looked up
    is the namespace specified in the WBEM URI, or otherwise the namespace
    specified in the --namespace option, or otherwise the default namespace of
    the connection. Any host name in the WBEM URI will be ignored.

    2. By specifying a class name with wildcard for the keys in the
    INSTANCENAME argument, i.e. "CLASSNAME.?". The instances of the specified
    class are displayed and the user is prompted for an index number to select
    an instance. The namespace in which the instances are looked up is the
    namespace specified in the --namespace option, or otherwise the default
    namespace of the connection.

    The properties to be modified and their new values are specified using the
    --property option, which may be specified multiple times.

    The --propertylist option allows restricting the set of properties to be
    modified. Given that the set of properties to be modified is already
    determined by the specified --property options, it does not need to be
    specified.

    Example:

      pywbemcli instance modify CIM_blah.fred=3 -P id=3 -P arr="bla bla",foo
    """
    context.execute_cmd(lambda: cmd_instance_modify(context, instancename,
                                                    options))


@instance_group.command('associators', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('--ac', '--assoc-class', 'assoc_class', type=str, required=False,
              metavar='CLASSNAME',
              help='Filter the result set by association class name. '
                   'Subclasses of the specified class also match.')
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help='Filter the result set by result class name. '
                   'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False,
              metavar='PROPERTYNAME',
              help='Filter the result set by source end role name.')
@click.option('--rr', '--result-role', 'result_role', type=str, required=False,
              metavar='PROPERTYNAME',
              help='Filter the result set by far end role name.')
@add_options(include_qualifiers_list_option)
@add_options(include_classorigin_instance_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(keybinding_key_option)
@add_options(namespace_option)
@add_options(summary_option)
@add_options(filter_query_option)
@add_options(filter_query_language_option)
@click.pass_obj
def instance_associators(context, instancename, **options):
    """
    List the instances associated with an instance.

    List the CIM instances that are associated with the specified CIM instance,
    and display the returned instances, or instance paths if --names-only was
    specified.

    The CIM instance can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the
    INSTANCENAME argument. The CIM namespace in which the instance is looked up
    is the namespace specified in the WBEM URI, or otherwise the namespace
    specified in the --namespace option, or otherwise the default namespace of
    the connection. Any host name in the WBEM URI will be ignored.

    2. By specifying a class name with wildcard for the keys in the
    INSTANCENAME argument, i.e. "CLASSNAME.?". The instances of the specified
    class are displayed and the user is prompted for an index number to select
    an instance. The namespace in which the instances are looked up is the
    namespace specified in the --namespace option, or otherwise the default
    namespace of the connection.

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


@instance_group.command('references', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help='Filter the result set by result class name. '
                   'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False, metavar='PROPERTYNAME',
              help='Filter the result set by source end role name.')
@add_options(include_qualifiers_list_option)
@add_options(include_classorigin_instance_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(keybinding_key_option)
@add_options(namespace_option)
@add_options(summary_option)
@add_options(filter_query_option)
@add_options(filter_query_language_option)
@click.pass_obj
def instance_references(context, instancename, **options):
    """
    List the instances referencing an instance.

    List the CIM (association) instances that reference the specified CIM
    instance, and display the returned instances, or instance paths if
    --names-only was specified.

    The CIM instance can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the
    INSTANCENAME argument. The CIM namespace in which the instance is looked up
    is the namespace specified in the WBEM URI, or otherwise the namespace
    specified in the --namespace option, or otherwise the default namespace of
    the connection. Any host name in the WBEM URI will be ignored.

    2. By specifying a class name with wildcard for the keys in the
    INSTANCENAME argument, i.e. "CLASSNAME.?". The instances of the specified
    class are displayed and the user is prompted for an index number to select
    an instance. The namespace in which the instances are looked up is the
    namespace specified in the --namespace option, or otherwise the default
    namespace of the connection.

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


@instance_group.command('invokemethod', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.argument('methodname', type=str, metavar='METHODNAME', required=True)
@click.option('-p', '--parameter', type=str, metavar='PARAMETERNAME=VALUE',
              required=False, multiple=True,
              help='Specify a method input parameter with its value. '
                   'May be specified multiple times. '
                   'Array property values are specified as a comma-separated '
                   'list; embedded instances are not supported. '
                   'Default: No input parameters.')
@add_options(keybinding_key_option)
@add_options(namespace_option)
@click.pass_obj
def instance_invokemethod(context, instancename, methodname, **options):
    """
    Invoke a method on an instance.

    Invoke a CIM method (METHODNAME argument) on a CIM instance with the
    specified input parameters (--parameter options), and display the method
    return value and output parameters.

    The CIM instance can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the
    INSTANCENAME argument. The CIM namespace in which the instance is looked up
    is the namespace specified in the WBEM URI, or otherwise the namespace
    specified in the --namespace option, or otherwise the default namespace of
    the connection. Any host name in the WBEM URI will be ignored.

    2. By specifying a class name with wildcard for the keys in the
    INSTANCENAME argument, i.e. "CLASSNAME.?". The instances of the specified
    class are displayed and the user is prompted for an index number to select
    an instance. The namespace in which the instances are looked up is the
    namespace specified in the --namespace option, or otherwise the default
    namespace of the connection.

    The method input parameters are specified using the --parameter option,
    which may be specified multiple times.

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


@instance_group.command('query', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('query', type=str, required=True, metavar='QUERY-STRING')
@click.option('--ql', '--query-language', 'query_language', type=str,
              metavar='QUERY-LANGUAGE', default=DEFAULT_QUERY_LANGUAGE,
              help='The query language to be used with --query. '
              'Default: {default}.'.
              format(default=DEFAULT_QUERY_LANGUAGE))
@add_options(namespace_option)
@add_options(summary_option)
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


@instance_group.command('count', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME-GLOB',
                required=False)
@add_options(multiple_namespaces_option)
@add_options(association_filter_option)
@add_options(indication_filter_option)
@add_options(experimental_filter_option)
@click.option('-s', '--sort', is_flag=True, required=False,
              help='Sort by instance count. Otherwise sorted by class name.')
@click.pass_obj
def instance_count(context, classname, **options):
    """
    Count the instances of each class with matching class name.

    Display the count of instances of each CIM class whose class name
    matches the specified wildcard expression (CLASSNAME-GLOB) in all CIM
    namespaces of the WBEM server, or in the specified namespaces
    (--namespace option).  This differs from instance enumerate, etc. in that
    it counts the instances specifically for the classname of each instance
    returned, not including subclasses.

    The CLASSNAME-GLOB argument is a wildcard expression that is matched on
    class names case insensitively.
    The special characters from Unix file name wildcarding are supported
    ('*' to match zero or more characters, '?' to match a single character,
    and '[]' to match character ranges). To avoid shell expansion of wildcard
    characters, the CLASSNAME-GLOB argument should be put in quotes.

    If CLASSNAME-GLOB is not specified, then all classes in the specified
    namespaces are counted (same as when specifying CLASSNAME-GLOB as "*").

    For example, "pywbem_*" returns classes whose name begins with "PyWBEM_",
    "pywbem_", etc. "*system*" returns classes whose names include the case
    insensitive string "system".

    This command can take a long time to execute since it potentially
    enumerates all instance names for all classes in all namespaces.
    """
    context.execute_cmd(lambda: cmd_instance_count(context, classname, options))


@instance_group.command('shrub', cls=PywbemcliCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME', required=True)
@click.option('--ac', '--assoc-class', 'assoc_class', type=str, required=False,
              metavar='CLASSNAME',
              help='Filter the result set by association class name. '
                   'Subclasses of the specified class also match.')
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help='Filter the result set by result class name. '
                   'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False,
              metavar='PROPERTYNAME',
              help='Filter the result set by source end role name.')
@click.option('--rr', '--result-role', 'result_role', type=str, required=False,
              metavar='PROPERTYNAME',
              help='Filter the result set by far end role name.')
@add_options(keybinding_key_option)
@add_options(namespace_option)
@add_options(summary_option)
@click.option('-f', '--fullpath', default=False, is_flag=True,
              help='Normally the instance paths in the tree views are '
                   'by hiding some keys with ~ to make the tree simpler '
                   'to read. This includes keys that have the same value '
                   'for all instances and the "CreationClassName" key.  When'
                   'this option is used the full instance paths are displayed.')
@click.pass_obj
def instance_shrub(context, instancename, **options):
    """
    Show the association shrub for INSTANCENAME.

    The shrub is a view of all of the instance association relationships for
    a defined INSTANCENAME showing the various components that are part of
    the association including Role, AssocClasse,ResultRole, And ResultClas

    The default view is a tree view from the INSTANCENAME to associated
    instances.

    Displays the shrub of association components for the association source
    instance defined by INSTANCENAME.

    The INSTANCENAME can be specified in two ways:

    1. By specifying an untyped WBEM URI of an instance path in the
    INSTANCENAME argument. The CIM namespace in which the instance is looked up
    is the namespace specified in the WBEM URI, or otherwise the namespace
    specified in the --namespace option, or otherwise the default namespace of
    the connection. Any host name in the WBEM URI will be ignored.

    2. By specifying a class name with wildcard for the keys in the
    INSTANCENAME argument, i.e. "CLASSNAME.?". The instances of the specified
    class are displayed and the user is prompted for an index number to select
    an instance. The namespace in which the instances are looked up is the
    namespace specified in the --namespace option, or otherwise the default
    namespace of the connection.

    Normally the association information is displayed as a tree but it
    may also be displayed as a table or as one of the object formats (ex. MOF)
    of all instances that are part of the shrub if one of the cim object
    formats is selected with the global output_format parameter.

    Results are formatted as defined by the output format global option.
    """
    context.execute_cmd(lambda: cmd_instance_shrub(context, instancename,
                                                   options))


####################################################################
#
#  Common functions for cmd_instance processing
#
####################################################################


WBEM_URI_INSTANCEPATH_REGEXP = re.compile(
    r'^(?:([\w\-]+):)?'  # namespace type (URI scheme)
    r'(?://([\w.:@\[\]]*))?'  # authority (host)
    r'(?:/|^/?)(\w+(?:/\w+)*)?'  # namespace name (leading slash optional)
    r'(?::|^:?)(\w+)'  # class name (leading colon optional)
    r'$',  # String end withou key bindings
    flags=re.UNICODE)

# Valid namespace types (URI schemes) for WBEM URI parsing
WBEM_URI_NAMESPACE_TYPES = [
    'http', 'https',
    'cimxml-wbem', 'cimxml-wbems',
]


def get_instancename(context, instancename, options):
    """
    Common function to get the instancename from the input defined as a
    WBEM_URL, the user with a console prompt call, or from one or more
    key options.

    If the instance name replaces the keys with ".?" execute the console
    prompt to select the instance name.

    If there is data in the key element in the options dict, usees that data to
    build the instance name.  The data ins in the form name=value.

    Otherwise assume that the instancename is a WBEM_URI and parse it.

    Parameters:

      Context: :class:`~pywbem.CIMInstanceName`
        The click context

      instancename: (:term:`string`):

      The WBEM URI string must be a CIM instance path in untyped WBEM URI
      format as documented in the pywbem CIMInstanceName.from_wbem_uri except
      that if the --keys option exists the keybindings compoment must not
      exist or if the keybindings may be defined as ".?'

    Returns:

     CIMInstanceName with namespace retrieved either from the namespace option
     in options dictionary or the connection default_namespace.

      :class:`~pywbem.CIMInstanceName`: The instance path created from the
      specified input with namespace retrieved either the namespace option
      in options dictionary, the instancename,  or the connection
      default_namespace.

    Raises:

      ClickException: Invalid WBEM URI format for an instance path. This
        includes typed WBEM URIs.
    """
    # TODO: Future - Could we  make usable if no class can be acquired because
    # GetClass not implemented in server. That would probably require
    # getting at least an instance of the class and using the properties
    # in that instance and the corresponding instancename to determine
    # which properties are keys and the property types.

    # If the keybindings is the character ? execute select
    if instancename.endswith(".?"):
        if options['key']:
            raise click.ClickException('Key option conflicts with '
                                       'namespace wildcard "?"')
        cln = instancename[:-2]
        ns = options.get('namespace', context.conn.default_namespace)

        try:
            instancepath = pick_instance(context, cln, namespace=ns)
        except ValueError:
            click.echo('Request aborted')
            return None

    # If the --key option contains data use that to build CIMInstanceName
    elif options['key']:
        # parse the prolog and classname from WBEM_URI to get classname
        m = WBEM_URI_INSTANCEPATH_REGEXP.match(instancename)
        if m is None:
            raise click.ClickException("Invalid format for instance path {}".
                                       format(instancename))

        ns_type = m.group(1) or None
        if ns_type and ns_type.lower() not in WBEM_URI_NAMESPACE_TYPES:
            warning_msg("Tolerating unknown namespace type {} in WBEM URI: {}".
                        format(ns_type, instancename))

        namespace = m.group(3) or None
        classname = m.group(4) or None
        assert classname is not None  # should be ensured by regexp

        try:
            cim_class = context.conn.GetClass(classname, LocalOnly=False,
                                              IncludeQualifiers=True)
            instancepath = create_ciminstancename(cim_class, options['key'])
            instancepath.namespace = namespace

        except CIMError as ce:
            if ce.status_code == CIM_ERR_NOT_FOUND:
                raise click.ClickException('Class "{}" not found'.
                                           format(classname))
        except ValueError as ve:
            raise click.ClickException('{}: {}'.format(
                ve.__class__.__name__, ve))

    else:
        try:
            instancepath = parse_wbemuri_str(instancename,
                                             options['namespace'])
        except ValueError as ve:
            raise click.ClickException('{}: {}'.format(
                ve.__class__.__name__, ve))

    return instancepath


####################################################################
#
#  cmd_instance_<action> processors
#
####################################################################


def cmd_instance_get(context, instancename, options):
    """
    Get and display an instance of a CIM Class.

    Gets the instance defined by instancename argument and displays in output
    format defined.

    If the wildcard key is used (CLASSNAME.?), pywbemcli presents a list of
    instances to the console from which one can be picked to get from the
    server and display.
    """

    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

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

        display_cim_objects(context, instance, output_fmt)

    except Error as er:
        raise_pywbem_error_exception(er)


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
            context.spinner_stop()
            click.echo('Deleted instance {}'.format(instancepath))

    except Error as er:
        raise_pywbem_error_exception(er)


def cmd_instance_create(context, classname, options):
    """
       Create an instance and submit to wbemserver.
       If successful, this operation returns the new instance name. Otherwise
       it raises an exception
    """
    ns = options['namespace'] or context.conn.default_namespace
    try:
        class_ = context.conn.GetClass(
            classname, namespace=ns, LocalOnly=False)
    except CIMError as ce:
        if ce.status_code == CIM_ERR_NOT_FOUND:
            raise click.ClickException('CIMClass: "{}" does not exist in '
                                       'namespace "{}" in WEB '
                                       'server: {}.'.format(classname, ns,
                                                            context.conn))
        raise_pywbem_error_exception(ce)

    except Error as er:
        raise_pywbem_error_exception(er)

    properties = options['property']

    # properties is a tuple of name,value pairs
    new_inst = create_ciminstance(class_, properties)

    if options['verify']:
        context.spinner_stop()
        click.echo(new_inst.tomof())
        if not verify_operation("Execute CreateInstance", msg=True):
            return
    try:
        name = context.conn.CreateInstance(new_inst,
                                           namespace=ns)

        context.spinner_stop()
        click.echo('{}'.format(name))
    except Error as er:
        raise click.ClickException('Server Error creating instance in '
                                   'namespace {}. Exception: '
                                   '{}: {}'.format(ns, er.__class__.__name__,
                                                   er))


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

    ns = options['namespace'] or context.conn.default_namespace

    try:
        class_ = context.conn.GetClass(
            instancepath.classname, namespace=ns, LocalOnly=False)
    except CIMError as ce:
        if ce.status_code == CIM_ERR_NOT_FOUND:
            raise click.ClickException(
                'CIMClass: {!r} does not exist in WEB server: {}'
                .format(instancepath.classname, context.conn.url))

        raise_pywbem_error_exception(ce)
    except Error as er:
        raise_pywbem_error_exception(er)

    property_list = resolve_propertylist(options['propertylist'])

    # properties is a tuple of name,value pairs
    modified_inst = create_ciminstance(class_, options['property'])

    modified_inst.path = instancepath

    if options['verify']:
        context.spinner_stop()
        click.echo(modified_inst.tomof())
        if not verify_operation("Execute ModifyInstance", msg=True):
            return

    try:
        context.conn.ModifyInstance(modified_inst,
                                    PropertyList=property_list)
        if context.verbose:
            context.spinner_stop()
            click.echo('Modified instance {}'.format(instancepath))
    except Error as er:
        raise click.ClickException('Server Error modifying instance {} '
                                   'in namespace {}. Exception: {}: {}'.format
                                   (instancepath, ns, er.__class__.__name__,
                                    er))


def cmd_instance_invokemethod(context, instancename, methodname,
                              options):
    """Create an instance and submit to wbemserver"""
    instancepath = get_instancename(context, instancename, options)
    if instancepath is None:
        return

    try:
        process_invokemethod(context, instancepath, methodname, options)
    except Error as er:
        raise_pywbem_error_exception(er)


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
    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

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

        display_cim_objects(context, results, output_fmt,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise_pywbem_error_exception(er)
    except ValueError as ve:
        raise click.ClickException('instance enumerate failed because '
                                   'FilterQuery not allowed with traditional '
                                   'EnumerateInstance. --use-pull: '
                                   '{}. Exception: {}: {}'
                                   .format(context.use_pull,
                                           ve.__class__.__name__, ve))


def cmd_instance_references(context, instancename, options):
    """Execute the references request operation to get references for
       the classname defined. This may be either interactive or if the
       interactive option is set or use the instancename directly.

       If the interactive option is selected, the instancename MUST BE
       a classname.
    """
    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

    instancepath = get_instancename(context, instancename, options)
    if instancepath is None:
        return

    try:
        if options['names_only']:
            results = context.conn.PyWbemcliReferenceInstancePaths(
                instancepath,
                ResultClass=options['result_class'],
                Role=options['role'],
                FilterQuery=options['filter_query'],
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pull_max_cnt)
        else:
            results = context.conn.PyWbemcliReferenceInstances(
                instancepath,
                ResultClass=options['result_class'],
                Role=options['role'],
                IncludeQualifiers=options['include_qualifiers'],
                IncludeClassOrigin=options['include_classorigin'],
                FilterQuery=options['filter_query'],
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pull_max_cnt,
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, output_fmt,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise_pywbem_error_exception(er)
    except ValueError as ve:
        raise click.ClickException('instance references failed because '
                                   'FilterQuery not allowed with traditional '
                                   'References. --use-pull: '
                                   '{}. Exception: {}: {}'
                                   .format(context.use_pull,
                                           ve.__class__.__name__, ve))


def cmd_instance_associators(context, instancename, options):
    """
    Execute the references request operation to get references for
    the classname defined
    """
    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

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
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pull_max_cnt)
        else:
            results = context.conn.PyWbemcliAssociatorInstances(
                instancepath,
                AssocClass=options['assoc_class'],
                Role=options['role'],
                ResultClass=options['result_class'],
                ResultRole=options['result_role'],
                IncludeQualifiers=options['include_qualifiers'],
                IncludeClassOrigin=options['include_classorigin'],
                FilterQuery=options['filter_query'],
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pull_max_cnt,
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, output_fmt,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise_pywbem_error_exception(er)

    except ValueError as ve:
        raise click.ClickException('instance associators failed because '
                                   'FilterQuery not allowed with traditional '
                                   'Associators. --use-pull: '
                                   '{}. Exception: {}: {}'
                                   .format(context.use_pull,
                                           ve.__class__.__name__, ve))


def cmd_instance_count(context, classname, options):
    """
    Get the number of instances of each class in the namespace
    """
    output_fmt = validate_output_format(context.output_format, 'TABLE')

    # Differs from class find because it classname is optional.
    # If None, select all
    if classname is None:
        classname = '*'

    # Create list of namespaces from the option or from all namespaces
    ns_names = get_namespaces(context, options['namespace'])

    ns_cln_tuples = []  # a list of tuples of namespace, classname
    for namespace in ns_names:
        # Get all classes in Namespace
        try:
            # Set cmd options that are required for this command.
            # 1. Always use deep_inheritance
            # 2. Set namespace to each namespace in loop
            options['deep_inheritance'] = True
            options['namespace'] = namespace
            options['names_only'] = True

            classnames = enumerate_classes_filtered(context, None, options)
        except Error as er:
            raise_pywbem_error_exception(er)

        if classnames:
            classlist = filter_namelist(classname, classnames, ignore_case=True)
            cl_tup = [(namespace, cln) for cln in classlist]
            ns_cln_tuples.extend(cl_tup)

    # sort since normal output for this command is  namespace, classname
    # alphabetic order.
    ns_cln_tuples.sort(key=lambda tup: (tup[0], tup[1]))

    display_data = []
    for tup in ns_cln_tuples:
        ns = tup[0]
        cln = tup[1]
        # Try block allows issues where enumerate does not properly execute
        # The totals may be wrong but at least it gets what it can.
        # This accounts for issues with some servers where there
        # are providers that return errors from the enumerate.
        try:
            inst_names = context.conn.EnumerateInstanceNames(cln, namespace=ns)
        except CIMError as ce:
            warning_msg('Server Error {} with {}:{}. Continuing.'
                        .format(ce, ns, cln))

        # Sum the number of instances with the defined classname.
        # this counts only classes with that specific classname and not
        # subclasses
        clnl = cln.lower()
        count = sum(1 for inst_name in inst_names
                    if (inst_name.classname.lower() == clnl))

        if count != 0:
            display_tuple = (ns, cln, count)
            display_data.append(display_tuple)

    # If sort set, resort by count size
    if options['sort']:
        display_data.sort(key=lambda x: x[2])

    headers = ['Namespace', 'Class', 'count']
    rows = []
    if display_data:
        for item in display_data:
            rows.append([item[0], item[1], item[2]])

    context.spinner_stop()
    click.echo(format_table(rows, headers,
                            title='Count of instances per class',
                            table_format=output_fmt))


def cmd_instance_query(context, query, options):
    """Execute the query defined by the inputs"""
    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

    try:
        results = context.conn.PyWbemcliQueryInstances(
            options['query_language'],
            query,
            namespace=options['namespace'],
            MaxObjectCount=context.pull_max_cnt)

        display_cim_objects(context, results, output_fmt,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise_pywbem_error_exception(er)


def cmd_instance_shrub(context, instancename, options):
    """
    Display the association information defined by instancename as a tree
    showing the various steps to get through the roles, references, etc. to
    return the names of associated instances.
    """

    try:
        instancepath = get_instancename(context, instancename, options)
        if instancepath is None:
            return

        # Collect the data for the shrub
        shrub = AssociationShrub(context, instancepath,
                                 Role=options['role'],
                                 AssocClass=options['assoc_class'],
                                 ResultRole=options['result_role'],
                                 ResultClass=options['result_class'],
                                 verbose=context.verbose,
                                 fullpath=options['fullpath'])

        # display the shrub
        context.spinner_stop()
        shrub.display_shrub(context.output_format, options['summary'])
    except Error as er:
        raise_pywbem_error_exception(er)
