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
commands for get, enumerate, associators, references, find, etc. of the objects
CIMClass on a WBEM server.

NOTE: Commands are ordered in help display by their order in this file.
"""

from __future__ import absolute_import, print_function

from collections import namedtuple
import click

from pywbem._nocasedict import NocaseDict

from pywbem import Error, CIMClassName, CIMError, ModelError, CIM_ERR_NOT_FOUND

from .pywbemcli import cli
from ._common import filter_namelist, \
    resolve_propertylist, CMD_OPTS_TXT, GENERAL_OPTS_TXT, SUBCMD_HELP_TXT, \
    output_format_is_table, format_table, process_invokemethod, \
    pywbem_error_exception, warning_msg, validate_output_format, \
    get_subclass_names, depending_classnames, get_leafclass_names

from ._display_cimobjects import display_cim_objects

from ._common_options import add_options, propertylist_option, \
    names_only_option, include_classorigin_class_option, namespace_option,  \
    summary_option, multiple_namespaces_option, class_filter_options, \
    help_option
from ._displaytree import display_class_tree
from ._click_extensions import PywbemcliGroup, PywbemcliCommand
from ._utils import pywbemcliwarn

#
#   Common option definitions for class group
#

# NOTE: A number of the options use double-dash as the short form.  In those
# cases, a third definition of the options without the double-dash defines
# the corresponding option name, ex. 'include_qualifiers'. It should be
# defined with underscore and not dash

no_qualifiers_class_option = [              # pylint: disable=invalid-name
    click.option('--nq', '--no-qualifiers', 'no_qualifiers', is_flag=True,
                 default=True,
                 help=u'Do not include qualifiers in the returned class(es). '
                      'Default: Include qualifiers.')]

deep_inheritance_class_option = [              # pylint: disable=invalid-name
    click.option('--di', '--deep-inheritance', 'deep_inheritance', is_flag=True,
                 default=False,
                 help=u'Include the complete subclass hierarchy of the '
                      'requested classes in the result set. '
                      'Default: Do not include subclasses.')]

local_only_class_option = [              # pylint: disable=invalid-name
    click.option('--lo', '--local-only', 'local_only', is_flag=True,
                 default=False,
                 help=u'Do not include superclass properties and methods in '
                      u'the returned class(es). '
                      u'Default: Include superclass properties and methods.')]


##########################################################################
#
#   Click command group and command definitions
#   These decorated functions implement the commands, arguments, and
#   options for the top-level class command group
#
###########################################################################

@cli.group('class', cls=PywbemcliGroup, options_metavar=GENERAL_OPTS_TXT,
           subcommand_metavar=SUBCMD_HELP_TXT)
@add_options(help_option)
def class_group():
    """
    Command group for CIM classes.

    This command group defines commands to inspect classes, invoke
    methods on classes, delete classes.

    Creation and modification of classes is not currently supported.

    In addition to the command-specific options shown in this help text, the
    general options (see 'pywbemcli --help') can also be specified before the
    'class' keyword.
    """
    pass  # pylint: disable=unnecessary-pass


@class_group.command('enumerate', cls=PywbemcliCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=False)
@add_options(deep_inheritance_class_option)
@add_options(local_only_class_option)
@add_options(no_qualifiers_class_option)
@add_options(include_classorigin_class_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(summary_option)
@add_options(class_filter_options)
@add_options(help_option)
@click.pass_obj
def class_enumerate(context, classname, **options):
    """
    List top classes or subclasses of a class in a namespace.

    Enumerate CIM classes starting either at the top of the class hierarchy
    in the specified CIM namespace (--namespace option), or at the specified
    class (CLASSNAME argument) in the specified namespace. If no namespace was
    specified, the default namespace of the connection is used.

    The --local-only, --include-classorigin, and --no-qualifiers options
    determine which parts are included in each retrieved class.

    The --deep-inheritance option defines whether or not the complete subclass
    hierarchy of the classes is retrieved.

    The --names-only option can be used to show only the class paths.

    In the output, the classes and class paths will be formatted as defined
    by the --output-format general option. Table formats on classes will be
    replaced with MOF format.

    Examples:

      pywbemcli -n myconn class enumerate -n interop

      pywbemcli -n myconn class enumerate CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_enumerate(context, classname,
                                                    options))


@class_group.command('get', cls=PywbemcliCommand, options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@add_options(local_only_class_option)
@add_options(no_qualifiers_class_option)
@add_options(include_classorigin_class_option)
@add_options(propertylist_option)
@add_options(namespace_option)
@add_options(help_option)
@click.pass_obj
def class_get(context, classname, **options):
    """
    Get a class.

    Get a CIM class (CLASSNAME argument) in a CIM namespace (--namespace
    option). If no namespace was specified, the default namespace of the
    connection is used.

    The --local-only, --include-classorigin, --no-qualifiers, and
    --propertylist options determine which parts are included in each retrieved
    class.

    In the output, the class will be formatted as defined by the
    --output-format general option. Table formats are replaced with MOF
    format.

    Example:

      pywbemcli -n myconn class get CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_get(context, classname, options))


@class_group.command('delete', cls=PywbemcliCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@click.option('-f', '--force', is_flag=True, default=False,
              help=u'Same as --include-instances. The -f / --force option has '
                   'been deprecated and will be removed in a future version.')
@click.option('--include-instances', is_flag=True, default=False,
              help=u'Delete any instances of the class as well. '
                   'WARNING: Deletion of instances will cause the removal '
                   'of corresponding resources in the managed environment '
                   '(i.e. in the real world).'
                   'Default: Reject command if the class has any instances.')
@click.option('--dry-run', is_flag=True, required=False,
              help=u'Enable dry-run mode: Do not actually delete the objects, '
                   'but display what would be done.')
@add_options(namespace_option)
@add_options(help_option)
@click.pass_obj
def class_delete(context, classname, **options):
    """
    Delete a class.

    Delete a CIM class (CLASSNAME argument) in a CIM namespace (--namespace
    option). If no namespace was specified, the default namespace of the
    connection is used.

    If the class has instances, the command is rejected, unless the
    --include-instances option is specified, in which case the instances
    are also deleted.

    If other classes in that namespace depend on the class to be deleted, the
    command is rejected. Dependencies considered for this purpose are
    subclasses, referencing classes and embedding classes (EmbeddedInstance
    qualifier only).

    WARNING: Deletion of instances will cause the removal of corresponding
    resources in the managed environment (i.e. in the real world). Some
    instances may not be deletable.

    WARNING: Deleting classes can cause damage to the server: It can impact
    instance providers and other components in the server. Use this
    command with caution.

    Many WBEM servers may not allow this operation or may severely limit the
    conditions under which a class can be deleted from the server.

    Example:

      pywbemcli -n myconn class delete CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_delete(context, classname, options))


@class_group.command('invokemethod', cls=PywbemcliCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True,)
@click.argument('methodname', type=str, metavar='METHODNAME', required=True)
@click.option('-p', '--parameter', type=str, metavar='PARAMETERNAME=VALUE',
              required=False, multiple=True,
              help=u'Specify a method input parameter with its value. '
                   'May be specified multiple times. '
                   'Default: No input parameters.')
@add_options(namespace_option)
@add_options(help_option)
@click.pass_obj
def class_invokemethod(context, classname, methodname, **options):
    """
    Invoke a method on a class.

    Invoke a static CIM method (METHODNAME argument) on a CIM class (CLASSNAME
    argument) in a CIM namespace (--namespace option), and display the method
    return value and output parameters. If no namespace was specified, the
    default namespace of the connection is used.

    The method input parameters are specified using the --parameter option,
    which may be specified multiple times.

    Pywbemcli retrieves the class definition from the server in order to
    verify that the specified input parameters are consistent with the
    parameter characteristics in the method definition.

    Use the 'instance invokemethod' command to invoke CIM methods on CIM
    instances.

    Example:

      pywbemcli -n myconn class invokemethod CIM_Foo methodx -p p1=9 -p p2=Fred
    """
    context.execute_cmd(lambda: cmd_class_invokemethod(context, classname,
                                                       methodname, options))


@class_group.command('references', cls=PywbemcliCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help=u'Filter the result set by result class name. '
                   'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by source end role name.')
@add_options(no_qualifiers_class_option)
@add_options(include_classorigin_class_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(summary_option)
@add_options(help_option)
@click.pass_obj
def class_references(context, classname, **options):
    """
    List the classes referencing a class.

    List the CIM (association) classes that reference the specified class
    (CLASSNAME argument) in the specified CIM namespace
    (--namespace option). If no namespace was specified, the default namespace
    of the connection is used.

    The classes to be retrieved can be filtered by the --role and
    --result-class options.

    The --include-classorigin, --no-qualifiers, and --propertylist options
    determine which parts are included in each retrieved class.

    The --names-only option can be used to show only the class paths.

    In the output, the classes and class paths will be formatted as defined
    by the --output-format general option. Table formats on classes will be
    replaced with MOF format.

    Examples:

      pywbemcli -n myconn class references CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_references(context, classname,
                                                     options))


@class_group.command('associators', cls=PywbemcliCommand,
                     options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=True)
@click.option('--ac', '--assoc-class', 'assoc_class', type=str, required=False,
              metavar='CLASSNAME',
              help=u'Filter the result set by association class name. '
                   'Subclasses of the specified class also match.')
@click.option('--rc', '--result-class', 'result_class', type=str,
              required=False, metavar='CLASSNAME',
              help=u'Filter the result set by result class name. '
                   'Subclasses of the specified class also match.')
@click.option('-r', '--role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by source end role name.')
@click.option('--rr', '--result-role', 'result_role', type=str, required=False,
              metavar='PROPERTYNAME',
              help=u'Filter the result set by far end role name.')
@add_options(no_qualifiers_class_option)
@add_options(include_classorigin_class_option)
@add_options(propertylist_option)
@add_options(names_only_option)
@add_options(namespace_option)
@add_options(summary_option)
@add_options(help_option)
@click.pass_obj
def class_associators(context, classname, **options):
    """
    List the classes associated with a class.

    List the CIM classes that are associated with the specified class
    (CLASSNAME argument) in the specified CIM namespace
    (--namespace option). If no namespace was specified, the default namespace
    of the connection is used.

    The classes to be retrieved can be filtered by the --role, --result-role,
    --assoc-class, and --result-class options.

    The --include-classorigin, --no-qualifiers, and --propertylist options
    determine which parts are included in each retrieved class.

    The --names-only option can be used to show only the class paths.

    In the output, the classes and class paths will be formatted as defined
    by the --output-format general option. Table formats on classes will be
    replaced with MOF format.

    Examples:

      pywbemcli -n myconn class associators CIM_Foo -n interop
    """
    context.execute_cmd(lambda: cmd_class_associators(context, classname,
                                                      options))


@class_group.command('find', cls=PywbemcliCommand, options_metavar=CMD_OPTS_TXT)
@click.argument('classname-glob', type=str, metavar='CLASSNAME-GLOB',
                required=True)
@add_options(multiple_namespaces_option)
@click.option('-s', '--sort', is_flag=True, required=False,
              help=u'Sort by namespace. Default is to sort by classname')
@add_options(class_filter_options)
@add_options(help_option)
@click.pass_obj
def class_find(context, classname_glob, **options):
    """
    List the classes with matching class names on the server.

    Find the CIM classes whose class name matches the specified wildcard
    expression (CLASSNAME-GLOB argument) in all CIM namespaces of the
    WBEM server, or in the specified namespace (--namespace option).

    The CLASSNAME-GLOB argument is a wildcard expression that is matched on
    class names case insensitively.
    The special characters from Unix file name wildcarding are supported
    ('*' to match zero or more characters, '?' to match a single character,
    and '[]' to match character ranges). To avoid shell expansion of wildcard
    characters, the CLASSNAME-GLOB argument should be put in quotes.

    For example, "pywbem_*" returns classes whose name begins with "PyWBEM_",
    "pywbem_", etc. "*system*" returns classes whose names include the case
    insensitive string "system".

    In the output, the classes will be formatted as defined by the
    --output-format general option if it specifies table output. Otherwise
    the classes will be in the form "NAMESPACE:CLASSNAME".

    Examples:

      pywbemcli -n myconn class find "CIM_*System*" -n interop

      pywbemcli -n myconn class find *Foo*
    """
    context.execute_cmd(lambda: cmd_class_find(context, classname_glob,
                                               options))


@class_group.command('tree', cls=PywbemcliCommand, options_metavar=CMD_OPTS_TXT)
@click.argument('classname', type=str, metavar='CLASSNAME', required=False)
@click.option('-s', '--superclasses', is_flag=True, default=False,
              help=u'Show the superclass hierarchy. '
                   'Default: Show the subclass hierarchy.')
@click.option('-d', '--detail', is_flag=True, default=False,
              help=u'Show details about the class: the Version, '
                   ' Association, Indication, and Abstact qualifiers.')
@add_options(namespace_option)
@add_options(help_option)
@click.pass_obj
def class_tree(context, classname, **options):
    """
    Show the subclass or superclass hierarchy for a class.

    List the subclass or superclass hierarchy of a CIM class (CLASSNAME
    argument) or CIM namespace (--namespace option):

    - If CLASSNAME is omitted, the complete class hierarchy of the specified
      namespace is retrieved.

    - If CLASSNAME is specified but not --superclasses, the class and its
      subclass hierarchy in the specified namespace are retrieved.

    - If CLASSNAME and --superclasses are specified, the class and its
      superclass ancestry up to the top-level class in the specified namespace
      are retrieved.

    If no namespace was specified, the default namespace of the connection is
    used.

    The class hierarchy will formatted as a ASCII graphical tree; the
    --output-format general option is ignored.

    The --detail options to display extra information about each class
    including:

    -  The Version qualifier value if the class includes a version
       qualifier. This is normally a string with 3 integers

    -  Information about each class type (Association, Indication, Abstract)

    Examples:

      # Display the complete class hierarchy from the interop namespace
      pywbemcli -n myconn class tree -n interop

      # Display CIM_Foo an its subclasses from the namespace interop
      pywbemcli -n myconn class tree CIM_Foo -n interop

      # Display CIM_Foo and its superclasses from interop
      pywbemcli -n myconn class tree CIM_Foo -s -n interop

    """
    context.execute_cmd(lambda: cmd_class_tree(context, classname, options))


####################################################################
#
#  Common functions for cmd_class processing
#  This includes functions used by the command action functions
#  in this fmodule and possibly other modules
#
####################################################################

def parse_version_str(version_str):
    """
    Parse a string with 3 positive integers seperated by period (CIM version
    string) into a 3 integer tuple and return the tuole

    Parameters:
        version_str (:term: str):
            String defining 3 components of a CIM version

    Returns:
        tuple containing 3 integers
    """
    try:
        version_tuple = [int(x) for x in version_str.split('.')]
    except ValueError:
        raise click.ClickException('--since option value invalid. '
                                   'Must contain 3 integer elements: '
                                   'int.int.int". {} received'.
                                   format(version_str))
    if len(version_tuple) != 3:
        raise click.ClickException('Version value must contain 3 integer '
                                   'elements (int.int.int). '
                                   '{} received'.format(version_str))
    return version_tuple


# Namedtupe defining each entry in the filters dictionary values
FILTERDEF = namedtuple('FILTERDEF', 'optionvalue qualifiername scopes')


def _build_filters_dict(conn, ns, options):
    """
    Build a dictionary defining the filters to be processed against list
    of classes from
    the filter definitons in the Click options dictionary. There is an entry
    in the dictionary for each filter to be applied to filter a list of
    classes.

    Returns:
      Dict of filters where the names are the  filtersthemselves , the types
      are the type of test (i.e. qualifier, superclass)
      and the value for each is a tuple:
      * Name of the qualifier (:term:`string`)
      * The value of the qualifier filter option (True or False which
        determines whether to display the existence or non-existence of the
        qualifier
      * A tuple containing Booleans for the value of each of the possible
        element scopes (class, property, method, parameter) indicating whether
        the qualifier is allowed in that element.
    """
    filters = {}

    def set_qualifier_option(qname, option_value):
        qualdecl = conn.GetQualifier(qname, ns)
        # Note: qualdecl.scopes performs test case-insensitively
        if qualdecl.scopes['any']:
            scopes_map = [True, True, True, True]
        else:
            scopes_map = [False, False, False, False]
            scopes_map[0] = any([qualdecl.scopes['class'],
                                 qualdecl.scopes['association'],
                                 qualdecl.scopes['indication']])
            scopes_map[1] = qualdecl.scopes['property']
            scopes_map[2] = qualdecl.scopes['method']
            scopes_map[3] = qualdecl.scopes['parameter']
        filters['qualifier'] = FILTERDEF(option_value, qname,
                                         tuple(scopes_map))

    # Qualifier options
    if options['association'] is not None:
        set_qualifier_option('association', options['association'])
    if options['indication'] is not None:
        set_qualifier_option('indication', options['indication'])
    if options['experimental'] is not None:
        set_qualifier_option('experimental', options['experimental'])
    # If set, the entity is deprecated
    if options['deprecated'] is not None:
        set_qualifier_option('deprecated', options['deprecated'])
    if options['since'] is not None:
        version_tuple = parse_version_str(options['since'])
        set_qualifier_option('version', version_tuple)

    if options['schema'] is not None:
        test_str = "{}_".format(options['schema'].lower())
        filters['schema'] = FILTERDEF(test_str, None, None)

    if options['subclass_of'] is not None:
        filters['subclass_of'] = FILTERDEF(options['subclass_of'], None, None)
    if options['leaf_classes'] is not None:
        filters['leaf_classes'] = FILTERDEF(options['leaf_classes'], None, None)
    return filters


def _filter_classes(classes, filters, names_only, iq):
    """
    Filter a list of classes for the qualifiers defined by  the
    qualifier_filter parameter where this parameter is a list of tuples.
    each tuple contains the qualifier name and a dictionary with qualifier
     name as key and tuple containing the option_value(True or False) and
    a list of booleans where each boolean represents one of the scope types
    ()
    whether to display or not display if it exists.

    This method only works for boolean qualifiers

    Parameters:

      classes (list of :class:`~pywbem.CIMClass`):
        list of classes to be filtered

      qualifier_filters (dict):
        Dictionary defining the filtering to be performed. It contains an entry
        for each qualifier filter that is defined. See _build_qualifier_filters
        for a definition of this list.

      names_only (:class:`py:bool`):
        If True, return only the classnames. Otherwise returns the filtered
        classes. This is because we must get the classes from the server to
        perform the filtering

      iq (:class:`py:bool`):
        If not True, remove any qualifiers from the classes.  This is because
        we must get the classes from the server with qualifiers to
        perform the filtering.
    """

    def class_has_qualifier(cls, qname, scopes):
        """
        Determine if the qualifier defined by qname exists in the elements
        of the class where the elements are defined by the scopes parameter
        for this filter.

        Parameters:

          cls (:class:`~pywbem.CIMClass`):
            The class to be inspected for the qualifier defined by qname

          qname (:term:`string`):
            The qualifier for which we are searching

          scopes (tuple of booleans):
            A tuple containing a boolean value for each of the possible scopes
            (class, property, method, parameter)

        Returns:
          True if the qualifier with name quname is found in the elements where
          the scope is True. Otherwise, False is returned

        """
        # Test class scope
        if scopes[0] and qname in cls.qualifiers:
            return True

        # if property scope, test properties
        if scopes[1]:
            for prop in cls.properties.values():
                if qname in prop.qualifiers:
                    return True
        # If method scope, test methods and if parameter scope, test parameters
        if scopes[2]:
            for method in cls.methods.values():
                if qname in method.qualifiers:
                    return True
                if scopes[3]:
                    params = method.parameters
                    for param in params.values():
                        if qname in param.qualifiers:
                            return True
        return False

    # Test all classes in the input property for the defined filters.
    filtered_classes = []
    subclass_names = []
    # Build list of subclass names that will be used later as a filter on the
    # classes to be returned
    if 'subclass_of' in filters:
        try:
            subclass_names = get_subclass_names(
                classes,
                classname=filters['subclass_of'].optionvalue,
                deep_inheritance=True)
        except ValueError:
            raise click.ClickException(
                'Classname {} for "subclass-of" not found in returned classes.'
                .format(filters['subclass_of'].optionvalue))

    # Build a list of leaf class names that will be used later as a filter on
    # the classes to be returned.
    if 'leaf_classes' in filters:
        try:
            if subclass_names:
                clsx = [cls for cls in classes if cls.classname in
                        subclass_names]
                leafclass_names = get_leafclass_names(clsx)
            else:
                leafclass_names = get_leafclass_names(classes)

        except ValueError:
            raise click.ClickException(
                'Classname {} for "leaf_classes-of" not found in returned '
                'classes.'.format(filters['leaf_classes'].optionvalue))

    for cls in classes:
        show_class_list = []
        for filter_name, filter_ in filters.items():
            if filter_name == 'qualifier':
                option_value = filter_.optionvalue
                if class_has_qualifier(cls, filter_.qualifiername,
                                       filter_.scopes):
                    if filter_.qualifiername == 'version':
                        if filter_.qualifiername in cls.qualifiers:
                            cls_version = \
                                cls.qualifiers[filter_.qualifiername].value
                            version_val = parse_version_str(cls_version)
                            option_value = version_val >= filter_.optionvalue

                    show_class_list.append(option_value)
                else:
                    show_class_list.append(not option_value)

            elif filter_name == 'schema':
                show_class_list.append(
                    cls.classname.lower().startswith(filter_.optionvalue))
            elif filter_name == 'subclass_of':
                show_class_list.append(cls.classname in subclass_names)
            elif filter_name == 'leaf_classes':
                show_class_list.append(cls.classname in leafclass_names)

            else:
                assert False  # Future for other test_types

        # Show if all options are True for this class
        show_this_class = all(show_class_list)

        if show_this_class:
            # If returning instances, honor the names_only option
            if not names_only and not iq:
                cls.qualifiers = []
                for p in cls.properties.values():
                    p.qualifiers = []
                for m in cls.methods.values():
                    m.qualifiers = []
                    for p in m.parameters.values():
                        p.qualifiers = []
            filtered_classes.append(cls)

    # If names_only parameter create list of classnames
    if names_only:
        filtered_classes = [cls.classname for cls in filtered_classes]
    return filtered_classes


def enumerate_classes_filtered(context, classname, options):
    """
    Execute EnumerateClasses or EnumerateClassNames in a single namespace
    defined in options['namespace'] and return results.

    If any of the class qualifier filters are defined in the options parameter,
    enumerate the classes, filter the result for those parameters, and return
    only class names if --names-only set.

    This function may be executed by multiple command action functions with
    varying options in the options. Each option must be tested to validate
    that it exists in the options dictionary

    Parameters:

      context:  Click context

      classname:
        classname for the enumerate or None if all classes to be enumerated.

      options:Click options dictionary
        Options that form basis for this Enumerate and filter processing.

    Returns:
        List of classes or classnames that satisfy the criteria

    Raises:
        pywbem Error exceptions generated by EnumerateClassNames and
        enumerateClasses
    """
    namespace = options['namespace']
    conn = context.pywbem_server.conn
    filters = _build_filters_dict(conn, namespace, options)

    names_only = options.get('names_only', False)

    iq = options.get('no_qualifiers', True)

    # Force IncludeQualifier true if results are to be filtered since
    # the filter requires that qualifiers exist.
    request_iq = True if filters else iq

    local_only = options.get('local_only', False)
    deep_inheritance = options.get('deep_inheritance', True)
    include_classorigin = options.get('include_classorigin', True)

    if names_only and not filters:
        results = conn.EnumerateClassNames(
            ClassName=classname,
            namespace=namespace,
            DeepInheritance=deep_inheritance)
    else:
        results = conn.EnumerateClasses(
            ClassName=classname,
            namespace=namespace,
            LocalOnly=local_only,
            DeepInheritance=deep_inheritance,
            IncludeQualifiers=request_iq,
            IncludeClassOrigin=include_classorigin)
        if filters:
            results = _filter_classes(results, filters,
                                      names_only, iq)
    return results


def get_format_group(context, options):
    """
    Define the format groups allowed based on the options. This is particular
    to the class commands, largely because we do not have a table format
    for enumerate, get, associators, or references unless options such as
    summary, or names_only are set.
    """

    # Summary always output as TABLE
    if 'summary' in options and options['summary']:

        # This accounts for the fact that the results of a summary can be
        # either table or simply a string output
        if context.output_format and \
                output_format_is_table(context.output_format):
            return ['TABLE']

        # Temporary hack. We need another format group, i.e. txt or str
        # That displays in non-structured manner. Or drop this output
        # completely.
        return ['CIM']

    # Names_only may be output as Table or as CIM Object.
    if 'names_only' in options and options['names_only']:
        return ['CIM', 'TABLE']

    # otherwise only CIM allowed today.
    return ['CIM']


#####################################################################
#
#  Command functions for each of the commands in the class group
#
#####################################################################


def cmd_class_get(context, classname, options):
    """
    Get the class defined by the argument.

    Gets the class defined by CLASSNAME from the WBEM server and displays
    the class. If the class cannot be found, the server returns a CIMError
    exception.
    """
    conn = context.pywbem_server.conn
    format_group = get_format_group(context, options)
    output_format = validate_output_format(context.output_format, format_group)

    try:
        result_class = conn.GetClass(
            classname,
            namespace=options['namespace'],
            LocalOnly=options['local_only'],
            IncludeQualifiers=options['no_qualifiers'],
            IncludeClassOrigin=options['include_classorigin'],
            PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, result_class,
                            output_format=output_format)
    except Error as er:
        raise pywbem_error_exception(er)


def cmd_class_invokemethod(context, classname, methodname, options):
    """
    Create an instance and submit to a WBEM server
    """

    try:
        cln = CIMClassName(classname, namespace=options['namespace'])
        process_invokemethod(context, cln, methodname, options['namespace'],
                             options['parameter'])
    except Error as er:
        raise pywbem_error_exception(er)


def cmd_class_enumerate(context, classname, options):
    """
        Enumerate the classes returning a list of classes from the WBEM server.
        That match the qualifier filter options
    """
    format_group = get_format_group(context, options)
    output_format = validate_output_format(context.output_format, format_group)

    try:
        results = enumerate_classes_filtered(context, classname, options)

        display_cim_objects(context, results, output_format,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise pywbem_error_exception(er)


def cmd_class_references(context, classname, options):
    """
    Execute the references request operation to get references for
    the classname defined
    """
    conn = context.pywbem_server.conn
    if options['namespace']:
        classname = CIMClassName(classname, namespace=options['namespace'])

    format_group = get_format_group(context, options)
    output_format = validate_output_format(context.output_format, format_group)

    try:
        if options['names_only']:
            results = conn.ReferenceNames(
                classname,
                ResultClass=options['result_class'],
                Role=options['role'])
        else:
            results = conn.References(
                classname,
                ResultClass=options['result_class'],
                Role=options['role'],
                IncludeQualifiers=options['no_qualifiers'],
                IncludeClassOrigin=options['include_classorigin'],
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, output_format,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise pywbem_error_exception(er)


def cmd_class_associators(context, classname, options):
    """
    Execute the references request operation to get references for
    the classname defined
    """
    conn = context.pywbem_server.conn

    if options['namespace']:
        classname = CIMClassName(classname, namespace=options['namespace'])

    format_group = get_format_group(context, options)
    output_format = validate_output_format(context.output_format, format_group)

    try:
        if options['names_only']:
            results = conn.AssociatorNames(
                classname,
                AssocClass=options['assoc_class'],
                Role=options['role'],
                ResultClass=options['result_class'],
                ResultRole=options['result_role'])
        else:
            results = conn.Associators(
                classname,
                AssocClass=options['assoc_class'],
                Role=options['role'],
                ResultClass=options['result_class'],
                ResultRole=options['result_role'],
                IncludeQualifiers=options['no_qualifiers'],
                IncludeClassOrigin=options['include_classorigin'],
                PropertyList=resolve_propertylist(options['propertylist']))

        display_cim_objects(context, results, output_format,
                            summary=options['summary'], sort=True)

    except Error as er:
        raise pywbem_error_exception(er)


def get_namespaces(context, namespaces):
    """
    Returns either the namespaces provided or if that is None, the set of
    namespaces that are defined in the wbem server as a list

    Raises:
        CIMError if status code not CIM_ERR_NOT_FOUND
    """
    conn = context.pywbem_server.conn
    wbem_server = context.pywbem_server.wbem_server

    ns_names = []

    # Return the provided namespace(s)
    if namespaces:
        return namespaces

    # Otherwise get all namespaces from server
    try:
        ns_names = wbem_server.namespaces
        ns_names.sort()
        return ns_names

    except ModelError:
        return [conn.default_namespace]
    except CIMError as ce:
        # allow processing to continue if no interop namespace
        if ce.status_code == CIM_ERR_NOT_FOUND:
            warning_msg('{}. Using default_namespace {}.'
                        .format(ce, conn.default_namespace))
            ns_names = [conn.default_namespace]
        return ns_names
    except Error as er:
        raise pywbem_error_exception(er)


def cmd_class_find(context, classname_glob, options):
    """
    Execute the command for enumerate classes, filter the results based on the
    option and display the result. The result is a list of classes/namespaces
    """

    output_format = validate_output_format(context.output_format, 'TABLE')

    context.spinner_stop()
    namespaces = get_namespaces(context, options['namespace'])

    try:
        # Define sort by namespace name if --sort, or  othersise by count
        sort_col = 0 if options['sort'] else 1

        # Dictionary key is namespaces, value is list of classes
        names_dict = NocaseDict()
        if namespaces:
            for ns in namespaces:
                # Uses di True, and names_only. Build options for enumerate
                options['deep_inheritance'] = True
                options['namespace'] = ns
                options['names_only'] = True

                # enumerate filtered for classnames and add to namespace in
                # dictionary
                classnames = enumerate_classes_filtered(context, None, options)
                names_dict[ns] = filter_namelist(classname_glob, classnames)

        context.spinner_stop()

        # If summary set, generate output of only count of classes for
        # each namespace
        if 'summary' in options and options['summary']:
            rows = [[ns, len(names_dict[ns])] for ns in names_dict]
            rows.sort(key=lambda x: x[sort_col])

            if output_format_is_table(context.output_format):
                headers = ['Namespace', 'Class count']
                click.echo(format_table(rows,
                                        headers,
                                        title='Find class counts {}'.
                                        format(classname_glob),
                                        table_format=output_format))
            else:
                for ns, count in rows:
                    click.echo('  {}: {}'. format(ns, count))
            return

        # Not summary. Build rows of namespace, classname for each namespace
        # and sort by names if --sort set
        rows = []
        for ns_name in names_dict:
            ns_rows = [[ns_name, name] for name in names_dict[ns_name]]
            # sort by classname if sort option defined, else by namespace
            ns_rows.sort(key=lambda x: x[sort_col])
            rows.extend(ns_rows)

        context.spinner_stop()

        if output_format_is_table(context.output_format):
            headers = ['Namespace', 'Classname']
            click.echo(
                format_table(rows, headers,
                             title='Find class {}'.format(classname_glob),
                             table_format=output_format))
        else:
            # Display function to display classnames returned with
            # their namespaces in the form <namespace>:<classname>
            for row in rows:
                click.echo('  {}: {}'.format(row[0], row[1]))

    except Error as er:
        raise pywbem_error_exception(er)


def get_class_hierarchy(conn, classname, namespace, superclasses=None):
    """
    Get the class hierarchy from the server, either the superclasses
    associated or subclasses with classname .  If getting subclasses
    the classname parameter may be None which requests that the complete
    class hiearchy be retrieved.

      Parameters:
        conn (:class:`~pywbem.WBEMConnection` or subclass):
            Current connection to a WBEM server.

        classname(:term:`string):
            classname if the tree is to be initiated from
            within the class hiearchy. May be None

        namespace(:term:`string):
          Namespace to use to acquire classes from WBEM server

        superclasses (:class:`py:bool`):
            If `True` display the superclasses of classname. If not True
            display the subclasses. The default is None (display subclasses).

      Returns:
        tuple of  classes, classnames where
          classes (list of :class:`~pywbem.CIMClass`): that are either the
          superclasses or the subclasses of classname.

      Raises:
        CIM_Error:
    """

    try:
        if superclasses:
            # classname must exist for superclass tree
            assert classname is not None

            # get the superclasses into a list
            klass = conn.GetClass(classname, namespace=namespace)
            classes = []
            classes.append(klass)
            while klass.superclass:
                klass = conn.GetClass(klass.superclass, namespace=namespace)
                classes.append(klass)
        else:
            # get the subclass hierarchy either complete or starting at the
            # optional CLASSNAME. Gets minimum data from server to define
            # class, superclass data
            classes = conn.EnumerateClasses(ClassName=classname,
                                            namespace=namespace,
                                            LocalOnly=True,
                                            IncludeQualifiers=True,
                                            DeepInheritance=True)

    except Error as er:
        raise pywbem_error_exception(er)

    return classes


def cmd_class_tree(context, classname, options):
    """
    Execute the command to display graphical tree of either superclasses or
    subclasses of classname. If classname is None, display tree starting from
    the class hierarchy root.
    Tree is displayed on the console as a left-justified tree using the
    asciitree library.
    The --superclasses option determines if the superclass tree or the
    subclass tree is displayed.
    """
    conn = context.pywbem_server.conn

    superclasses = options['superclasses']

    # Classname must exist as starting point for superclass tree.
    if superclasses and classname is None:
        raise click.ClickException('CLASSNAME argument required for '
                                   '--superclasses option')

    classes = get_class_hierarchy(conn, classname, options['namespace'],
                                  superclasses)

    # If showing superclasses, set classname to None for the display
    # to add the 'root' as top class.
    if superclasses:
        classname = None

    # Display the list of classes as a tree. The classname is the top
    # of the tree.
    context.spinner_stop()
    display_class_tree(classes, classname, show_detail=options['detail'])


def cmd_class_delete(context, classname, options):
    """Delete a class from the WBEM server repository"""
    conn = context.pywbem_server.conn

    include_instances = options['include_instances']
    if options['force']:
        include_instances = options['force']
        pywbemcliwarn("The --force / -f option has been deprecated and "
                      "will be removed in a future version. Use "
                      "--include-instances instead.", DeprecationWarning)
    dry_run = options['dry_run']
    dry_run_prefix = "Dry run: " if dry_run else ""

    namespace = options['namespace'] or conn.default_namespace

    try:
        instnames = conn.EnumerateInstanceNames(
            ClassName=classname, namespace=namespace)
    except Error as exc:
        raise pywbem_error_exception(
            exc, "Cannot enumerate instance names of class {} in "
            "namespace {}".format(classname, namespace))

    if instnames and not include_instances:
        raise click.ClickException(
            "Cannot delete class {} because it has {} instances".
            format(classname, len(instnames)))

    depending_cln_list = depending_classnames(
        classname, namespace, conn)

    if depending_cln_list:
        raise click.ClickException(
            "Cannot delete class {} because these classes depend on it: {}".
            format(classname, ', '.join(depending_cln_list)))

    context.spinner_stop()
    if include_instances:
        for instname in instnames:
            if not dry_run:
                try:
                    conn.DeleteInstance(instname)
                except Error as exc:
                    raise pywbem_error_exception(
                        exc, "Cannot delete instance {}".format(instname))
            click.echo('{}Deleted instance {}'.format(dry_run_prefix, instname))

    if not dry_run:
        try:
            conn.DeleteClass(classname)
        except Error as exc:
            raise pywbem_error_exception(
                exc, "Cannot delete class {} in namespace {}".
                format(classname, namespace))
    click.echo('{}Deleted class {}'.format(dry_run_prefix, classname))
