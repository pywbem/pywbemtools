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

import six

import click

from pywbem import CIMInstanceName, CIMClassName, Error, CIMError, \
    CIM_ERR_NOT_FOUND

from .pywbemcli import cli
from ._common import pick_instance, resolve_propertylist, create_ciminstance, \
    filter_namelist, verify_operation, process_invokemethod, \
    pywbem_error_exception, parse_kv_pair

from ._display_cimobjects import display_cim_objects

from ._common_options import propertylist_option, names_only_option, \
    include_classorigin_instance_option, namespace_option, summary_option, \
    verify_option, multiple_namespaces_option_dflt_all, \
    multiple_namespaces_option_dflt_conn, class_filter_options, \
    object_order_option

from ._cimvalueformatter import mof_escaped

from ._association_shrub import AssociationShrub

from .config import DEFAULT_QUERY_LANGUAGE
from ._common_cmd_functions import get_namespaces, enumerate_classes_filtered, \
    ResultsHandler
from .._click_extensions import PywbemtoolsGroup, PywbemtoolsCommand, \
    CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT
from .._options import add_options, help_option, validate_required_arg
from .._output_formatting import validate_output_format, format_table, \
    warning_msg

#
#   Common option definitions for instance group
#

# NOTE: A number of the options use double-dash as the short form.  In those
# cases, a third definition of the options without the double-dash defines
# the corresponding option name, ex. 'include_qualifiers'. It should be
# defined with underscore and not dash

# Issue 224 - Exception in prompt-toolkit with python 2.7. Caused because
# with prompt-toolkit 2 + the completer requires unicode and click_repl not
# passing help as unicode in options as unicode
# NOTE: Insure that all option help attributes are unicode to get around this
#       issue


# This is instance-only because the default is False for include-qualifiers
# on instances but True on classes
include_qualifiers_get_option = [              # pylint: disable=invalid-name
    click.option('--iq', '--include-qualifiers', 'include_qualifiers',
                 is_flag=True, required=False,
                 help=u'Include qualifiers in the returned instance. '
                      u'Not all servers return qualifiers on instances. '
                      u'Default: Do not include qualifiers.')]

include_qualifiers_list_option = [              # pylint: disable=invalid-name
    click.option('--iq', '--include-qualifiers', 'include_qualifiers',
                 is_flag=True, required=False,
                 help=u'When traditional operations are used, include '
                      u'qualifiers in the returned instances. '
                      u'Some servers may ignore this option. '
                      u'By default, and when pull operations are used, '
                      u'qualifiers will never be included.')]

# specific to instance because DeepInheritance differs between class and
# instance operations.
deep_inheritance_enum_option = [              # pylint: disable=invalid-name
    click.option('--di', '--deep-inheritance', 'deep_inheritance',
                 is_flag=True, required=False,
                 help=u'Include subclass properties in the returned '
                      u'instances. '
                      u'Default: Do not include subclass properties.')]

local_only_get_option = [              # pylint: disable=invalid-name
    click.option('--lo', '--local-only', 'local_only', is_flag=True,
                 required=False,
                 help=u'Do not include superclass properties in the returned '
                      u'instance. '
                      u'Some servers may ignore this option. '
                      u'Default: Include superclass properties.')]

local_only_list_option = [              # pylint: disable=invalid-name
    click.option('--lo', '--local-only', 'local_only', is_flag=True,
                 required=False,
                 help=u'When traditional operations are used, do not include '
                      u'superclass properties in the returned instances. '
                      u'Some servers may ignore this option. '
                      u'By default, and when pull operations are used, '
                      u'superclass properties will always be included.')]

property_create_option = [              # pylint: disable=invalid-name
    click.option('-p', '--property', type=str, metavar='PROPERTYNAME=VALUE',
                 required=False, multiple=True,
                 help=u'Initial property value for the new instance. '
                      u'May be specified multiple times. '
                      u'Array property values are specified as a '
                      u'comma-separated list; embedded instances are not '
                      u'supported. '
                      u'Default: No initial properties provided.')]

property_modify_option = [              # pylint: disable=invalid-name
    click.option('-p', '--property', type=str, metavar='PROPERTYNAME=VALUE',
                 required=False, multiple=True,
                 help=u'Property to be modified, with its new value. '
                      u'May be specified once for each property to be '
                      u'modified. '
                      u'Array property values are specified as a '
                      u'comma-separated list; embedded instances are not '
                      u'supported. '
                      u'Default: No properties modified.')]

keybinding_key_option = [              # pylint: disable=invalid-name
    click.option('-k', '--key', type=str, metavar='KEYNAME=VALUE',
                 required=False, multiple=True,
                 help=u'Value for a key in keybinding of CIM instance name. '
                      u'May be specified multiple times. '
                      u'Allows defining keys without the issues of quotes. '
                      u'Default: No keybindings provided.')]

filter_query_language_option = [              # pylint: disable=invalid-name
    click.option('--fql', '--filter-query-language', 'filter_query_language',
                 type=str, metavar='QUERY-LANGUAGE', default=None,
                 help=u'The filter query language to be used with '
                      u'--filter-query. '
                      u'Default: DMTF:FQL.')]

filter_query_option = [              # pylint: disable=invalid-name
    click.option('--fq', '--filter-query', 'filter_query', type=str,
                 metavar='QUERY-STRING', default=None,
                 help=u'When pull operations are used, filter the instances in '
                      u'the result via a filter query. '
                      u'By default, and when traditional operations are used, '
                      u'no such filtering takes place.')]

help_instancename_option = [              # pylint: disable=invalid-name
    click.option('--hi', '--help-instancename', 'help_instancename',
                 is_flag=True, required=False, is_eager=True,
                 help=u'Show help message for specifying INSTANCENAME '
                      u'including use of the --key and --namespace options.')]

show_null_option = [              # pylint: disable=invalid-name
    click.option('--show-null', 'show_null', is_flag=True, required=False,
                 help=u'In the TABLE output formats, show properties with no '
                      u'value (i.e. Null) in all of the instances to be '
                      u'displayed. Otherwise only properties at least '
                      u'one instance has a non-Null property are displayed')]


##########################################################################
#
#   Click command group and command definitions
#   These decorated functions implement the commands, arguments, and
#
###########################################################################


@cli.group('instance', cls=PywbemtoolsGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
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


@instance_group.command('enumerate', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@add_options(local_only_list_option)
@add_options(deep_inheritance_enum_option)
@add_options(include_qualifiers_list_option)
@add_options(include_classorigin_instance_option)
@add_options(propertylist_option)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(names_only_option)
@add_options(summary_option)
@add_options(filter_query_option)
@add_options(filter_query_language_option)
@add_options(show_null_option)
@add_options(object_order_option)
@add_options(help_option)
@click.pass_obj
def instance_enumerate(context, classname, **options):
    """
    List the instances of a class.

    Enumerate the CIM instances of the specified class (CLASSNAME argument),
    including instances of subclasses in the specified CIM namespace(s)
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
    context.execute_cmd(
        lambda: cmd_instance_enumerate(context, classname, options))


@instance_group.command('get', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME',
                required=False)
@add_options(local_only_get_option)
@add_options(include_qualifiers_get_option)
@add_options(include_classorigin_instance_option)
@add_options(propertylist_option)
@add_options(keybinding_key_option)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(object_order_option)
@add_options(help_instancename_option)
@add_options(show_null_option)
@add_options(help_option)
@click.pass_obj
def instance_get(context, instancename, **options):
    """
    Get an instance of a class.

    For information on how to specify the instance using INSTANCENAME and the
    --key and --namespace options, invoke with --help-instancename.

    The --local-only, --include-qualifiers, --include-classorigin, and
    --propertylist options determine which parts are included in the retrieved
    instance.

    In the output, the instance will formatted as defined by the
    --output-format general option.
    """
    if options['help_instancename']:
        show_help_instancename()
        return
    validate_required_arg(instancename, 'INSTANCENAME')
    context.execute_cmd(
        lambda: cmd_instance_get(context, instancename, options))


@instance_group.command('delete', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME',
                required=False)
@add_options(keybinding_key_option)
@add_options(namespace_option)
@add_options(help_instancename_option)
@add_options(help_option)
@click.pass_obj
def instance_delete(context, instancename, **options):
    """
    Delete an instance of a class.

    WARNING: Deletion of instances will cause the removal of corresponding
    resources in the managed environment (i.e. in the real world). Some
    instances may not be deletable.

    For information on how to specify the instance using INSTANCENAME and the
    --key and --namespace options, invoke with --help-instancename.
    """
    if options['help_instancename']:
        show_help_instancename()
        return
    validate_required_arg(instancename, 'INSTANCENAME')
    context.execute_cmd(
        lambda: cmd_instance_delete(context, instancename, options))


@instance_group.command('create', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@add_options(property_create_option)
@add_options(verify_option)
@add_options(namespace_option)
@add_options(help_option)
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
    context.execute_cmd(
        lambda: cmd_instance_create(context, classname, options))


@instance_group.command('modify', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME',
                required=False)
@add_options(property_modify_option)
@click.option('--pl', '--propertylist', 'propertylist', multiple=True, type=str,
              default=None, required=False, metavar='PROPERTYLIST',
              help=u'Reduce the properties to be modified (as per '
              u'--property) to a specific property list. '
              u'Multiple properties may be specified with either a '
              u'comma-separated list or by using the option multiple '
              u'times. The empty string will cause no properties to '
              u'be modified. '
              u'Default: Do not reduce the properties to be modified.')
@add_options(verify_option)
@add_options(keybinding_key_option)
@add_options(namespace_option)
@add_options(help_instancename_option)
@add_options(help_option)
@click.pass_obj
def instance_modify(context, instancename, **options):
    """
    Modify properties of an instance.

    For information on how to specify the instance using INSTANCENAME and the
    --key and --namespace options, invoke with --help-instancename.

    The properties to be modified and their new values are specified using the
    --property option, which may be specified multiple times.

    The --propertylist option allows restricting the set of properties to be
    modified. Given that the set of properties to be modified is already
    determined by the specified --property options, it does not need to be
    specified.

    Example:

      pywbemcli instance modify CIM_blah.fred=3 -P id=3 -P arr="bla bla",foo
    """
    if options['help_instancename']:
        show_help_instancename()
        return
    validate_required_arg(instancename, 'INSTANCENAME')
    context.execute_cmd(
        lambda: cmd_instance_modify(context, instancename, options))


@instance_group.command('associators', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME',
                required=False)
@click.option('--ac', '--assoc-class', 'assoc_class', type=str, required=False,
              metavar='CLASSNAME',
              help=u'Filter the result set by association class name. '
                   u'Subclasses of the specified class also match.')
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help=u'Filter the result set by result class name. '
                   u'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by source end role name.')
@click.option('--rr', '--result-role', 'result_role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by far end role name.')
@add_options(include_qualifiers_list_option)
@add_options(include_classorigin_instance_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(keybinding_key_option)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(summary_option)
@add_options(filter_query_option)
@add_options(filter_query_language_option)
@add_options(show_null_option)
@add_options(help_instancename_option)
@add_options(object_order_option)
@add_options(help_option)
@click.pass_obj
def instance_associators(context, instancename, **options):
    """
    List the instances associated with an instance.

    List the CIM instances that are associated with the specified CIM instance,
    and display the returned instances, or instance paths if --names-only was
    specified.

    For information on how to specify the instance using INSTANCENAME and the
    --key and --namespace options, invoke with --help-instancename.

    The instances to be retrieved can be filtered by the --filter-query,
    --role, --result-role, --assoc-class, and --result-class options.

    The --include-qualifiers, --include-classorigin, and --propertylist options
    determine which parts are included in each retrieved instance.

    The --names-only option can be used to show only the instance paths.

    In the output, the instances and instance paths will be formatted as
    defined by the --output-format general option. Table formats on instances
    will be replaced with MOF format.
    """
    if options['help_instancename']:
        show_help_instancename()
        return
    validate_required_arg(instancename, 'INSTANCENAME')
    context.execute_cmd(
        lambda: cmd_instance_associators(context, instancename, options))


@instance_group.command('references', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME',
                required=False)
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help=u'Filter the result set by result class name. '
                   u'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False, metavar='PROPERTYNAME',
              help=u'Filter the result set by source end role name.')
@add_options(include_qualifiers_list_option)
@add_options(include_classorigin_instance_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(keybinding_key_option)
@add_options(multiple_namespaces_option_dflt_conn)
@add_options(summary_option)
@add_options(filter_query_option)
@add_options(show_null_option)
@add_options(filter_query_language_option)
@add_options(help_instancename_option)
@add_options(object_order_option)
@add_options(help_option)
@click.pass_obj
def instance_references(context, instancename, **options):
    """
    List the instances referencing an instance.

    List the CIM (association) instances that reference the specified CIM
    instance, and display the returned instances, or instance paths if
    --names-only was specified.

    For information on how to specify the instance using INSTANCENAME and the
    --key and --namespace options, invoke with --help-instancename.

    The instances to be retrieved can be filtered by the --filter-query, --role
    and --result-class options.

    The --include-qualifiers, --include-classorigin, and --propertylist options
    determine which parts are included in each retrieved instance.

    The --names-only option can be used to show only the instance paths.

    In the output, the instances and instance paths will be formatted as
    defined by the --output-format general option. Table formats on instances
    will be replaced with MOF format.
    """
    if options['help_instancename']:
        show_help_instancename()
        return
    validate_required_arg(instancename, 'INSTANCENAME')
    # pylint: disable=line-too-long
    context.execute_cmd(lambda: cmd_instance_references(context, instancename, options))  # noqa: E501


@instance_group.command('invokemethod', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME',
                required=False)
@click.argument('methodname', type=str, metavar='METHODNAME', required=False)
@click.option('-p', '--parameter', type=str, metavar='PARAMETERNAME=VALUE',
              required=False, multiple=True,
              help=u'Specify a method input parameter with its value. '
                   u'May be specified multiple times. '
                   u'Array property values are specified as a comma-separated '
                   u'list; embedded instances are not supported. '
                   u'Default: No input parameters.')
@add_options(keybinding_key_option)
@add_options(namespace_option)
@add_options(help_instancename_option)
@add_options(help_option)
@click.pass_obj
def instance_invokemethod(context, instancename, methodname, **options):
    """
    Invoke a method on an instance.

    Invoke a CIM method (METHODNAME argument) on a CIM instance with the
    specified input parameters (--parameter options), and display the method
    return value and output parameters.

    For information on how to specify the instance using INSTANCENAME and the
    --key and --namespace options, invoke with --help-instancename.

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
    if options['help_instancename']:
        show_help_instancename()
        return
    validate_required_arg(instancename, 'INSTANCENAME')
    validate_required_arg(methodname, 'METHODNAME')
    # pylint: disable=line-too-long
    context.execute_cmd(lambda: cmd_instance_invokemethod(context, instancename, methodname, options))  # noqa: E501


@instance_group.command('query', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('query', type=str, required=True, metavar='QUERY-STRING')
@click.option('--ql', '--query-language', 'query_language', type=str,
              metavar='QUERY-LANGUAGE', default=DEFAULT_QUERY_LANGUAGE,
              help=u'The query language to be used with --query. '
              u'Default: {default}.'.
              format(default=DEFAULT_QUERY_LANGUAGE))
@add_options(namespace_option)
@add_options(summary_option)
@add_options(help_option)
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


@instance_group.command('count', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME-GLOB',
                required=False)
@add_options(multiple_namespaces_option_dflt_all)
@click.option('-s', '--sort', is_flag=True, required=False,
              help=u'Sort by instance count. Otherwise sorted by class name.')
@click.option('--ignore-class', type=str,
              multiple=True,
              metavar='CLASSNAME',
              help=u"Class names of classes to be ignored (not counted). "
                   u"Allows counting instances in servers where instance "
                   u"retrieval may cause a CIMError or Error exception "
                   u"on some classes. CIM errors on particular "
                   u"classes are ignored. Error exceptions cause scan to stop "
                   u"and remaining classes status shown as 'not scanned'. "
                   u"Multiple class names are allowed (one per option or "
                   u"comma-separated).")
@add_options(class_filter_options)
@add_options(help_option)
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

    If a CIMError occurs on any enumerate, it is flagged with a warning message
    and the search for instances continues.  If an Error exception occurs
    (ex. Connection error) the scan is terminated under the assumption
    that the server may have failed and the remaining items are shown as
    "Not scanned".

    This command can take a long time to execute since it potentially
    enumerates all instance names for all classes in all namespaces.
    """
    context.execute_cmd(lambda: cmd_instance_count(context, classname, options))


@instance_group.command('shrub', cls=PywbemtoolsCommand,
                        options_metavar=CMD_OPTS_TXT)
@click.argument('instancename', type=str, metavar='INSTANCENAME',
                required=False)
@click.option('--ac', '--assoc-class', 'assoc_class', type=str, required=False,
              metavar='CLASSNAME',
              help=u'Filter the result set by association class name. '
                   'Subclasses of the specified class also match.')
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help=u'Filter the result set by result class name. '
                   u'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by source end role name.')
@click.option('--rr', '--result-role', 'result_role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by far end role name.')
@add_options(keybinding_key_option)
@add_options(namespace_option)
@add_options(summary_option)
@click.option('-f', '--fullpath', default=False, is_flag=True,
              help=u'Normally the instance paths in the tree views are '
                   u'by hiding some keys with ~ to make the tree simpler '
                   u'to read. This includes keys that have the same value '
                   u'for all instances and the "CreationClassName" key.  When'
                   'this option is used the full instance paths are displayed.')
@add_options(help_instancename_option)
@add_options(help_option)
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

    For information on how to specify the instance using INSTANCENAME and the
    --key and --namespace options, invoke with --help-instancename.

    Normally the association information is displayed as a tree but it
    may also be displayed as a table or as one of the object formats (ex. MOF)
    of all instances that are part of the shrub if one of the cim object
    formats is selected with the global output_format parameter.

    Results are formatted as defined by the output format global option.
    """
    if options['help_instancename']:
        show_help_instancename()
        return
    validate_required_arg(instancename, 'INSTANCENAME')
    # pylint: disable=line-too-long
    context.execute_cmd(lambda: cmd_instance_shrub(context, instancename, options))  # noqa: E501


####################################################################
#
#  Common functions for cmd_instance processing
#
####################################################################


def show_help_instancename():
    """
    Show the help message on how to specify an instance using INSTANCENAME
    and the --key and --namespace options.
    """
    # Note: This help text has a fixed width since it is too complex to
    # dynamically render it to a given width.
    click.echo("""
An instance path is specified using the INSTANCENAME argument and optionally the
--key and --namespace options. It can be specified in three ways:

1. By specifying the instance path as an untyped WBEM URI in the INSTANCENAME
   argument. In this case, the keybindings of the instance are specified in the
   WBEM URI, and the --key option must not be used.

   String typed keybindings in WBEM URIs are using double quotes, so the
   processing of special characters by the shell (such as backslashes and
   quotes) needs to be considered.

   The CIM namespace of the instance can be specified in the WBEM URI, or using
   the --namespace option, or otherwise the default namespace of the connection
   will be used.

   If present, the scheme and host components in the WBEM URI will be ignored.

   Examples (for a shell such as 'bash'):

     cimv2/test:TST_Person.FirstName=\\"Albert\\",LastName=\\"Einstein\\"
     TST_Foo.ID=42 --namespace cimv2/test
     TST_Foo.ID=42                     # default namespace of connection is used
     TST_Foo.IntegerKey=42
     TST_Foo.BooleanKey=true
     TST_Foo.StringKey=\\"text\\"        # shell processes escapes
     'TST_Foo.StringKey="text"'        # shell processes outer squotes
     'TST_Foo.StringKey="42"'          # shell processes outer squotes
     'TST_Foo.StringKey="true"'        # shell processes outer squotes
     "TST_Foo.StringKey=\\"it's\\""      # shell proc. outer dquotes and escapes
     'TST_Foo.StringKey="1.75\\""'      # shell processes outer squotes
     'TST_Foo.StringKey="a b"'         # shell processes outer squotes
     'CIM_SubProfile.Main="CIM_RegisteredProfile.InstanceID=\\"acme.1\\"",
       Sub="CIM_RegisteredProfile.InstanceID=\\"acme.2\\""'

2. By specifying the class path of the creation class of the instance as an
   untyped WBEM URI in the INSTANCENAME argument and by using the --key option
   to specify the keybindings of the instance.

   This approach reduces the use of double quotes compared to the first
   approach and eliminates it for the most common cases, but the processing of
   special characters by the shell still needs to be considered.

   The --key option can be specified multiple times, once for each key of the
   instance name. The argument of the --key option has a NAME=VALUE format,
   where NAME is the name of the key property and VALUE is its value. The
   string/numeric/boolean type needed for creating a keybinding is determined
   automatically from VALUE. Valid integer numbers are interpreted as a numeric
   type, the strings "true" and "false" in any lexical case are interpreted as
   a boolean type, and anything else is interpreted as a string type. Starting
   and ending VALUE with double quotes forces interpretation as a string type;
   in that case double quotes and backslashes inside of the double quotes need
   to be backslash-escaped. This is useful for strings that have a numeric
   value, or the string values "true" or "false".

   The CIM namespace of the instance can be specified in the WBEM URI, or using
   the --namespace option, or otherwise the default namespace of the connection
   will be used.

   If present, the scheme and host components in the WBEM URI will be ignored.

   Examples (for a shell such as 'bash'):

     cimv2/test:TST_Person --key FirstName=Albert --key LastName=Einstein
     TST_Foo --namespace cimv2/test --key ID=42
     TST_Foo --key ID=42               # default namespace of connection is used
     TST_Foo --key IntegerKey=42
     TST_Foo --key BooleanKey=true
     TST_Foo --key StringKey=text
     TST_Foo --key StringKey=\\"42\\"    # shell processes escapes
     TST_Foo --key StringKey=\\"true\\"  # shell processes escapes
     TST_Foo --key "StringKey=it's"    # shell processes outer dquotes
     TST_Foo --key 'StringKey=1.75"'   # shell processes outer squotes
     TST_Foo --key "StringKey=a b"     # shell processes outer dquotes
     TST_Foo --key StringKey="a b"     # shell processes outer dquotes
     TST_Foo --key StringKey=a\\ b      # shell processes escapes
     CIM_SubProfile --key Main='CIM_RegisteredProfile.InstanceID="acme.1"'
       --key Sub='CIM_RegisteredProfile.InstanceID="acme.2"'

3. By specifying the class path of the creation class of the instance as an
   untyped WBEM URI in the INSTANCENAME argument, followed by a wildcard
   indicator ".?". In this case, the --key option must not be used. The
   instances of the specified class are displayed and the user is prompted for
   an index number to select an instance.

   The CIM namespace of the instance can be specified in the WBEM URI, or using
   the --namespace option, or otherwise the default namespace of the connection
   will be used.

   If present, the scheme and host components in the WBEM URI will be ignored.

   Example command:

     $ pywbemcli instance get cimv2/test:TST_Person.?
     Pick Instance name to process
     0: cimv2/test:TST_Person.FirstName="Albert",LastName="Einstein"
     1: cimv2/test:TST_Person.FirstName="Marie",LastName="Curie"
     Input integer between 0 and 1 or Ctrl-C to exit selection: _
""")


def get_instancename(context, instancename, options, default_all_ns=False):
    """
    Common function to construct a CIMInstanceName object from the
    INSTANCENAME argument and the --key and --namespace options specified
    in the command line.

    The keybindings of the returned CIM instance path(s) must be specified in
    exactly one of these ways:

    * If the keybindings component in the instance name string is "?"
      (e.g. "CIM_Foo.?"), the instances of that class are listed and the user
      is prompted to pick instance name. If multiple namespaces are specified
      in the "--namespaces" option the instances in all requested namespaces
      are listed for the user to pick one.

    * If the "key" option is non-empty, the so specified key values are used as
      keybindings for the returned instance path, and the instancename string
      is interpreted as a class WBEM URI.

    * If the instance name string specifies keybindings, these keybindings
      are used to define the instance name to return.

    The namespace of the returned CIM instance path must be specified in
    exactly one of these ways:

    * If the instance name string specifies a namespace, it is used.

    * If the "--namespace" option is non-empty, it is used. If the "--namespace"
      option is a list, the request is to return instance names in any of the
      namespaces.

    * Otherwise, the default namespace of the connection in the context is used.

    Parameters:

      context (:class:`'~pywbemtools._context_obj.ContextObj`):
        The Click context object.

      instancename (:term:`string`):
        The INSTANCENAME argument from the command line.

      options (dict):
        Command-specific options from the command line (including "-key" and
        "--namespace" if specified).

      default_all_ns (:class:`py:bool`)
        If True, the default is to return all namespaces.  Otherwise the
        default is to return None.

    Returns:

      :class:`~pywbem.CIMInstanceName`: CIM instance path. It is never None.
      Namespace included in instance name ONLY if it is in the parameter
      instance name or multiple namespaces were specified with "--namespace".

    Raises:

      ClickException: Various reasons.
    """
    conn = context.pywbem_server.conn

    def validate_namespace_option(class_path):
        """Validate either namespace in instance or --namespace but not both"""
        if class_path.namespace:
            if options['namespace']:
                raise click.ClickException(
                    "Using --namespace option: {} conflicts with specifying "
                    "namespace in INSTANCENAME: {}".format(options['namespace'],
                                                           instancename))

    # If option is a tuple, expand option to get list of all namespaces
    # defined. Option may be multiple uses of the option and/or comma-separated
    # string for any option value
    if isinstance(options['namespace'], tuple):
        ns_names = get_namespaces(context, options['namespace'],
                                  default_all_ns=default_all_ns)
    else:
        ns_names = options['namespace']

    # Process the 3 exclusive cmd option (".?", --key option, instance name )
    if instancename.endswith(".?"):
        if options['key']:
            raise click.ClickException(
                "Using the --key option conflicts with specifying a "
                "wildcard keybinding in INSTANCENAME: {}".
                format(instancename))

        class_uri = instancename[:-2]
        try:
            class_path = CIMClassName.from_wbem_uri(class_uri)
        except ValueError as exc:
            raise click.ClickException(str(exc))

        validate_namespace_option(class_path)

        try:
            # User picks one instance.  returned instance path includes
            # namespace.
            instance_path = pick_instance(
                context, class_path.classname, ns_names)
            # Reset the namespace in instance name if multiple namespaces
            if instance_path:
                if ns_names:
                    instance_path.namespace = None
        except ValueError as exc:
            raise click.ClickException(str(exc))

    # if --key option exists.
    elif options['key']:
        # Transform the --key option values into WBEM URI keybinding strings
        kb_strs = []
        for kv in options['key']:
            key, value = parse_kv_pair(kv)
            if value is None:
                raise click.ClickException(
                    "VALUE in --key option argument is missing: {}".format(kv))
            try:
                int(value)
                is_int = True
            except (ValueError, TypeError):
                is_int = False
            if value is None:
                # There is no official NULL representation in WBEM URI
                kb_value = ''
            elif is_int:
                # integer - use without quotes
                kb_value = value
            elif value.upper() in ('TRUE', 'FALSE'):
                # boolean - use the upper cased string without quotes
                kb_value = value.upper()
            elif value.startswith('"') and value.endswith('"'):
                # string - the value between the double quotes is assumed to
                # already be backslash-escaped, at the minimum for double
                # quotes and backslashes.
                kb_value = value
            else:
                # string - double quotes and escaping is added
                # Note that a keybinding value in a WBEM URI only requires
                # the minimal escaping for MOF string literals, i.e. double
                # quotes and backslashes. However, we escape all control chars,
                # double quotes, and single quotes, to ensure that there are no
                # unprintable characters, and no quotes that might interfere
                # with the shell.
                kb_value = '"{}"'.format(mof_escaped(value))

            kb_strs.append("{}={}".format(key, kb_value))

        # We perform an extra verification that instance name was a class
        # path to get a more understandable error message if it is not,
        # compared to leaving that to CIMInstanceName.from_wbem_uri().
        try:
            CIMClassName.from_wbem_uri(instancename)
        except ValueError as exc:
            raise click.ClickException(str(exc))

        instancename_kb = "{}.{}".format(instancename, ','.join(kb_strs))

        try:
            instance_path = CIMInstanceName.from_wbem_uri(instancename_kb)
            validate_namespace_option(instance_path)
        except ValueError as exc:
            raise click.ClickException(str(exc))

    else:  # else for not options['key']] or ".?", i.e. full key in inst path
        try:
            instance_path = CIMInstanceName.from_wbem_uri(instancename)
            validate_namespace_option(instance_path)
        except ValueError as exc:
            raise click.ClickException(str(exc))

    if instance_path is None:
        raise click.ClickException(
            "No instance paths found for instancename {0}".format(instancename))

    # Set namespace into path if ns_names not set
    if not instance_path.namespace:
        if not ns_names:
            instance_path.namespace = options.get('namespace') or \
                conn.default_namespace
        if isinstance(ns_names, six.string_types):
            instance_path.namespace = ns_names

    return instance_path


####################################################################
#
#  cmd_instance_<action> processors
#
####################################################################


def cmd_instance_get(context, instancename, options):
    """
    Get and display an instance of a CIM Class.

    Gets the instance defined by instancename argument in the namespaces defined
    and displays in output format defined.  If multiple namespaces are defined
    this method may get multiple instances.

    If the wildcard key is used (CLASSNAME.?), pywbemcli presents a list of
    instances to the console from which one can be picked to get from the
    server and display.
    """
    conn = context.pywbem_server.conn
    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

    # Returns list of namespaces from namespace option
    instancepath = get_instancename(context, instancename, options)

    property_list = resolve_propertylist(options['propertylist'])

    results = ResultsHandler(context, options, output_fmt, "instance",
                             instancepath, instpath=instancepath)

    for ns in results:
        try:
            instancepath.namespace = ns
            results.add(conn.GetInstance(
                instancepath,
                LocalOnly=options['local_only'],
                IncludeQualifiers=options['include_qualifiers'],
                IncludeClassOrigin=options['include_classorigin'],
                PropertyList=property_list))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

    results.display()


def cmd_instance_delete(context, instancename, options):
    """
        If option interactive is set, get instances of the class defined
        by instance name and allow the user to select the instance to
        delete. This method allows only a single namespace.

        Otherwise attempt to delete the instance defined by instancename
    """
    conn = context.pywbem_server.conn

    instancepath = get_instancename(context, instancename, options)

    try:
        conn.DeleteInstance(instancepath)

        if context.verbose:
            context.spinner_stop()
            click.echo('Deleted instance {}'.format(instancepath))

    except Error as er:
        raise pywbem_error_exception(er)


def cmd_instance_create(context, classname, options):
    """
       Create an instance and submit to wbemserver.
       If successful, this operation returns the new instance name. Otherwise
       it raises an exception
    """
    conn = context.pywbem_server.conn
    ns = options['namespace'] or conn.default_namespace
    try:
        class_ = conn.GetClass(
            classname, namespace=ns, LocalOnly=False)
    except CIMError as ce:
        if ce.status_code == CIM_ERR_NOT_FOUND:
            raise click.ClickException(
                'CIMClass: "{}" does not exist in namespace "{}" in WEB '
                'server: {}.'.
                format(classname, ns, conn))
        raise pywbem_error_exception(ce)

    except Error as er:
        raise pywbem_error_exception(er)

    properties = options['property']

    # properties is a tuple of name,value pairs
    new_inst = create_ciminstance(class_, properties)

    if options['verify']:
        context.spinner_stop()
        click.echo(new_inst.tomof())
        if not verify_operation("Execute CreateInstance", msg=True):
            return
    try:
        name = conn.CreateInstance(new_inst, namespace=ns)

        context.spinner_stop()
        click.echo('{}'.format(name))
    except Error as er:
        raise click.ClickException(
            'Server Error creating instance in namespace {}. Exception: '
            '{}: {}'.
            format(ns, er.__class__.__name__, er))


def cmd_instance_modify(context, instancename, options):
    """
    Build an instance defined by the options and submit to wbemserver
    as a ModifyInstance method.

    This method allows only a single namespace.

    In order to make a correct instance, this method first gets the
    corresponding class and uses that as the template for creating the intance.
    The class provides property names, types, array flags, etc. to assure
    that the instance is correctly built.

    If successful, this operation returns nothing.
    """
    conn = context.pywbem_server.conn
    instancepath = get_instancename(context, instancename, options)

    ns = options['namespace'] or conn.default_namespace

    try:
        class_ = conn.GetClass(
            instancepath.classname, namespace=ns, LocalOnly=False)
    except CIMError as ce:
        if ce.status_code == CIM_ERR_NOT_FOUND:
            raise click.ClickException(
                'CIMClass: {!r} does not exist in WEB server: {}'
                .format(instancepath.classname, conn.url))

        raise pywbem_error_exception(ce)
    except Error as er:
        raise pywbem_error_exception(er)

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
        conn.ModifyInstance(modified_inst, PropertyList=property_list)
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
    """
    Create an instance and submit to wbemserver
    """
    instancepath = get_instancename(context, instancename, options)

    try:
        process_invokemethod(context, instancepath, methodname,
                             options['namespace'], options['parameter'])
    except Error as er:
        raise pywbem_error_exception(er)


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


def enumerate_instances(conn, context, options, namespace, classname,
                        property_list, return_original_err=False):
    """
    Internal method.

    Issue the command to enumerate either the paths or instances for the
    namespace defined by the namespace parameter.

    If the return_original_err is True, reraise any  Error or CIMError
    exception.
    """
    try:
        if options['names_only']:
            return conn.PyWbemcliEnumerateInstancePaths(
                ClassName=classname,
                namespace=namespace,
                FilterQuery=options['filter_query'],
                FilterQueryLanguage=get_filterquerylanguage(options),
                MaxObjectCount=context.pywbem_server.pull_max_cnt)

        return conn.PyWbemcliEnumerateInstances(
            ClassName=classname,
            namespace=namespace,
            LocalOnly=options['local_only'],
            IncludeQualifiers=options['include_qualifiers'],
            DeepInheritance=options['deep_inheritance'],
            IncludeClassOrigin=options['include_classorigin'],
            FilterQuery=options['filter_query'],
            FilterQueryLanguage=get_filterquerylanguage(options),
            MaxObjectCount=context.pywbem_server.pull_max_cnt,
            PropertyList=property_list)

    except Error as er:
        # Return either the original exception or the ClickException.
        if return_original_err:
            raise er
        raise pywbem_error_exception(er)

    # Exception from Enumerate and the FilterQuery.  This exception would
    # apply  to all namespaces so just terminate.
    except ValueError as ve:
        raise click.ClickException(
            'Instance enumerate failed because FilterQuery not allowed with '
            'traditional EnumerateInstance. --use-pull: {}. Exception: {}: {}'
            .format(context.pywbem_server.use_pull, ve.__class__.__name__, ve))


def cmd_instance_enumerate(context, classname, options):
    """
    Enumerate CIM instances or CIM instance names

    Returns:
        list of objects retrieved.

    """
    conn = context.pywbem_server.conn
    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

    property_list = resolve_propertylist(options['propertylist'])

    results = ResultsHandler(context, options, output_fmt, "class", classname,
                             property_list=property_list)

    for ns in results:
        try:
            results.add(enumerate_instances(conn, context, options, ns,
                                            classname, property_list,
                                            return_original_err=True))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

    results.display()


def cmd_instance_references(context, instancename, options):
    """Execute the references request operation to get references for
       the classname defined. This may be either interactive or if the
       interactive option is set or use the instancename directly.

       This method allows multiple namespaces

       If the interactive option is selected, the instancename MUST BE
       a classname.
    """
    conn = context.pywbem_server.conn
    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

    instancepath = get_instancename(context, instancename, options)

    property_list = resolve_propertylist(options['propertylist'])

    results = ResultsHandler(context, options, output_fmt, "instance",
                             instancepath, instpath=instancepath,
                             property_list=property_list)

    for ns in results:
        try:
            instancepath.namespace = ns
            if options['names_only']:
                results.add(conn.PyWbemcliReferenceInstancePaths(
                    instancepath,
                    ResultClass=options['result_class'],
                    Role=options['role'],
                    FilterQuery=options['filter_query'],
                    FilterQueryLanguage=get_filterquerylanguage(options),
                    MaxObjectCount=context.pywbem_server.pull_max_cnt))
            else:
                results.add(conn.PyWbemcliReferenceInstances(
                    instancepath,
                    ResultClass=options['result_class'],
                    Role=options['role'],
                    IncludeQualifiers=options['include_qualifiers'],
                    IncludeClassOrigin=options['include_classorigin'],
                    FilterQuery=options['filter_query'],
                    FilterQueryLanguage=get_filterquerylanguage(options),
                    MaxObjectCount=context.pywbem_server.pull_max_cnt,
                    PropertyList=property_list))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

        except ValueError as ve:
            raise click.ClickException(
                'Instance references failed because FilterQuery not allowed '
                'with traditional References. --use-pull {}. Exception: {}: {}'
                .format(context.pywbem_server.use_pull, ve.__class__.__name__,
                        ve))
    results.display()


def cmd_instance_associators(context, instancename, options):
    """
    Execute the references request operation to get references for
    the classname defined.

    This method allows multiple namespaces.
    """
    conn = context.pywbem_server.conn
    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

    instancepath = get_instancename(context, instancename, options)

    property_list = resolve_propertylist(options['propertylist'])

    results = ResultsHandler(context, options, output_fmt, "class",
                             instancepath, instpath=instancepath,
                             property_list=property_list)

    for ns in results:
        try:
            instancepath.namespace = ns
            if options['names_only']:
                results.add(conn.PyWbemcliAssociatorInstancePaths(
                    instancepath,
                    AssocClass=options['assoc_class'],
                    Role=options['role'],
                    ResultClass=options['result_class'],
                    ResultRole=options['result_role'],
                    FilterQuery=options['filter_query'],
                    FilterQueryLanguage=get_filterquerylanguage(options),
                    MaxObjectCount=context.pywbem_server.pull_max_cnt))
            else:
                results.add(conn.PyWbemcliAssociatorInstances(
                    instancepath,
                    AssocClass=options['assoc_class'],
                    Role=options['role'],
                    ResultClass=options['result_class'],
                    ResultRole=options['result_role'],
                    IncludeQualifiers=options['include_qualifiers'],
                    IncludeClassOrigin=options['include_classorigin'],
                    FilterQuery=options['filter_query'],
                    FilterQueryLanguage=get_filterquerylanguage(options),
                    MaxObjectCount=context.pywbem_server.pull_max_cnt,
                    PropertyList=property_list))

        except CIMError as ce:
            # Process error and continue or generate exception
            results.handle_exception(ns, ce)
            continue

        except Error as er:
            raise pywbem_error_exception(er)

        except ValueError as ve:
            raise click.ClickException(
                'Instance associators failed because FilterQuery not allowed '
                'with traditional Associators. --use-pull: {}. Exception: {}: '
                '{}'
                .format(context.pywbem_server.use_pull, ve.__class__.__name__,
                        ve))

    results.display()


def cmd_instance_count(context, classname, options):
    """
    Get the number of instances of each class in the namespace
    """
    conn = context.pywbem_server.conn
    output_fmt = validate_output_format(context.output_format, 'TABLE')

    class_ignore_list = []
    for cls in options['ignore_class']:
        if ',' in cls:
            class_ignore_list.extend(cls.split(','))
        else:
            class_ignore_list.append(cls)

    # Differs from class find because the classname is optional.
    # If None, select all
    if classname is None:
        classname = '*'

    # Create list of namespaces from the option or from all namespaces
    # default_rtn forces
    ns_names = get_namespaces(context, options['namespace'],
                              default_all_ns=True)

    ns_cln_tuples = []  # a list of tuples of namespace, classname
    for namespace in ns_names:
        # Get all classes in Namespace
        try:
            # Set cmd options that are required for this command.
            # 1. Always use deep_inheritance
            # 2. Set namespace to each namespace in loop
            options['deep_inheritance'] = True
            options['names_only'] = True

            classnames = enumerate_classes_filtered(context, namespace, None,
                                                    options)
        except Error as er:
            raise pywbem_error_exception(er)

        if classnames:
            classlist = filter_namelist(classname, classnames, ignore_case=True)
            cl_tup = [(namespace, cln) for cln in classlist]
            ns_cln_tuples.extend(cl_tup)

    # Sort since normal output for this command is  namespace, classname
    # alphabetic order.
    ns_cln_tuples.sort(key=lambda tup: (tup[0], tup[1]))

    display_data = []
    error = 0
    # Scan all of the class/namespace tuples to get count of instances
    # of each class.
    for tup in ns_cln_tuples:
        ns = tup[0]
        cln = tup[1]
        if cln in class_ignore_list:
            display_tuple = (ns, cln, "ignored")
            display_data.append(display_tuple)
            continue
        # If an error has occurred, just display the remaining items with
        # Not scanned msg.
        if error:
            display_tuple = (ns, cln, "Not scanned")
            display_data.append(display_tuple)
            continue
        # Try block allows issues where enumerate does not properly execute
        # The totals may be wrong but at least it gets what it can.
        # This accounts for issues with some servers where there
        # are providers that return errors from the enumerate.
        inst_names = None
        try:
            inst_names = conn.EnumerateInstanceNames(cln, namespace=ns)
        except CIMError as ce:
            warning_msg("Server CIMError {0} with namepace={1}, class={2}. "
                        "Continuing scan."
                        .format(ce, ns, cln))
            display_tuple = (ns, cln, "CIMError {}".format(ce.status_code))
            display_data.append(display_tuple)
            continue
        # Error exception cause termination of the connection. Add this
        # item to the display with Server Fail message instead of count
        except Error as er:
            error = er
            warning_msg("Server Error {0} with namepace={1}, class={2}. "
                        "Terminating scan."
                        .format(er, ns, cln))
            display_tuple = (ns, cln, "Server Fail")
            display_data.append(display_tuple)
            continue

        # Sum the number of instances with the defined classname.
        # this counts only classes with that specific classname and not
        # subclasses
        if inst_names:
            count = sum(1 for inst_name in inst_names
                        if (inst_name.classname.lower() == cln.lower()))
            # Display only non-zero elements
            if count:
                display_tuple = (ns, cln, count)
                display_data.append(display_tuple)

    # Post scan processing
    # If sort set, re-sort by count size
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
    if error:
        raise click.ClickException(
            "Server Error {0} at namespace={1}, class:{2}. Scan incomplete."
            .format(error, ns, cln))


def cmd_instance_query(context, query, options):
    """
    Execute the query defined by the inputs.

    This commands creates a Query request based on the command input variables
    and options and outputs the result in either CIM or TABLE format.
    """
    conn = context.pywbem_server.conn
    output_fmt = validate_output_format(context.output_format, ['CIM', 'TABLE'])

    try:
        results = conn.PyWbemcliQueryInstances(
            options['query_language'],
            query,
            namespace=options['namespace'],
            MaxObjectCount=context.pywbem_server.pull_max_cnt)

        display_cim_objects(
            context, results, output_fmt, summary=options['summary'])

    except Error as er:
        raise pywbem_error_exception(er)


def cmd_instance_shrub(context, instancename, options):
    """
    Display the association information defined by instancename as a tree
    showing the various steps to get through the roles, references, etc. to
    return the names of associated instances.
    """
    conn = context.pywbem_server.conn

    # ns_names = get_namespaces(context, options['namespace'], default_rtn=None)
    instancepath = get_instancename(context, instancename, options)

    try:

        # Collect the data for the shrub
        shrub = AssociationShrub(conn, instancepath,
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
        raise pywbem_error_exception(er)
