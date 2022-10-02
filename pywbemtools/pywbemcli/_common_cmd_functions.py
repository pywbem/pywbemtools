# (C) Copyright 2022 IBM Corp.
# (C) Copyright 2022 Inova Development Inc.
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
Functions and classes used by the _cmd_xxxx.py command implementations but that
apply across multiple command groups (ex. they are used by both _cmd_class
and _cmd_instance).
"""

from __future__ import absolute_import, print_function

from collections import namedtuple
import click

from pywbem._nocasedict import NocaseDict

from pywbem import Error, CIMError, ModelError, \
    CIM_ERR_NOT_FOUND, CIM_ERR_INVALID_CLASS, CIM_ERR_INVALID_PARAMETER, \
    CIM_ERR_INVALID_NAMESPACE

from ._common import pywbem_error_exception, get_subclass_names, \
    get_leafclass_names, parse_version_value

from ._display_cimobjects import display_cim_objects

from .._output_formatting import output_format_is_table, \
    format_table, warning_msg, output_format_is_cimobject, \
    output_format_is_textgroup


class ResultsHandler(object):
    """
    Class that manages the handling of the namespaces, interim results, and
    errors in those request action methods that use multiple namespaces.

    This class:
      - Initializes the structures that gather data from pywbem server requests
        when multiple requests are to be executed because the command
        defines multiple namespaces for the requests,
      - Manages determination of the namespaces to be processed.
      - Provides methods (add(...) and handle_exception() to capture the
        command results
      - Manages continuation of execution of requests if a CIMError is
        encountered
      - Provides a method (display(...) that calls the display_cimobjects to
        display the request results
      - Displays any error results in a form compatible with the requested
        display format and data format.

    The pattern for this class is:

      results = ResultsHandler(...)
      for namespace in results:
         # execute server request and append results to any previous results
         results.add(<request method>)
      exception CIMError as ce:
        # Capture the CIMError exception and either terminate if not one of the
        # ones for which continuing would be logical or return
        results.handle_exception(ns, ce)
        continue
      # terminate because an Error exception is going to apply to all requests
      exception Error as er:
            raise pywbem_error_exception(er)

      results.display()
    """
    def __init__(self, context, options, output_format, obj_type,
                 target_object, instpath=None, property_list=None):
        """
          context (:class:`py:dict`):
            click command context dictionary
          options (:class:`py:dict`):
            click command options dictionary
          output_format (:term:`string`)
            Output format string that is passed to display_cimobjects())
          obj_type ((:term:`string`)):
            String defining type of object "class", "instance", etc.
          target_object

          instpath (:term:`string` or :class:`~pywbem.CIMInstanceName`):
            Identification of the request target object to be included in
            error display

          property_list (list of :term:`string, :term:`string` or None)
            Resolved property list passed to display_cimobjects
        """

        self.context = context
        self.obj_type = obj_type
        self.target_object = target_object
        self.output_format = output_format
        self.options = options
        self.property_list = property_list

        # If namespace returned from get_instancename in path, put it into
        # ns_names. path on the instance overrides the use of --namespace and
        # therefore return from get_namespaces()
        if instpath and instpath.namespace:
            self.ns_names = [instpath.namespace]
        else:
            self.ns_names = get_namespaces(context, options['namespace'])

        self.results = NocaseDict()

        # Set the requested namespaces into the results dictionary
        for ns in self.ns_names:
            self.results[ns] = None

        self.result_errors = {}
        self.results_to_date = 0

    def __contains__(self, key):
        return key in self.results

    def keys(self):
        """
        Return result dictionary keys
        """
        return self.results.keys()

    def __iter__(self):
        """
        Used to iterate the namespaces for which requests are to be made
        """
        return iter(self.results)

    def add(self, request_result):
        """
        Adds reguest_result to results dictionary
        """
        self.results[self.ns_names[self.results_to_date]] = request_result
        self.results_to_date += 1

    def handle_exception(self, ns, exc):
        """
        Handle CIM_Error exceptions from multi-namespace requests.  This method
        processes an exception from a server request methods and determines if
        the processing will continue for other namespaces or terminate with an
        exception. If one of the listed CIMError status codes in being
        processed, it allows the processing to continue but issues a warning
        message.

        If all namespaces in the ns_names list have been processed and there
        are no valid responses in the ns_names list, it raises the error shown
        by exc.

        Parameters:
          exc (Exception):
            The exception caught and  being processed.

          target_object (:term:`string` or CIMInstanceName,):
            The request target object that caused the exception or None
        """
        # If not one of the following CIMError status codes, terminate with
        # Click exception
        if exc.status_code not in (CIM_ERR_NOT_FOUND,
                                   CIM_ERR_INVALID_CLASS,
                                   CIM_ERR_INVALID_NAMESPACE,
                                   CIM_ERR_INVALID_PARAMETER):
            raise pywbem_error_exception(exc)

        # If all returns were in error, terminate with last exception but show
        # the errors as part of the errors display
        self.results_to_date += 1
        self.result_errors[ns] = (exc)
        if self.results_to_date == len(self.results):
            if not any(self.results.values()):
                if self.result_errors:
                    self.display_errors(terminate=False)
                raise pywbem_error_exception(exc)

    def display(self):
        """
        Execute the displays. This will cause the display of both the
        results and result_errors.  Note that this method gets specifiec
        options from self.options that are required by display_cimobjects
        """
        summary = self.options.get('summary', None)
        ignore_null = not self.options.get('show_null', None)
        object_order = self.options.get("object_order", None)

        display_cim_objects(self.context, self.results, self.output_format,
                            summary=summary,
                            ignore_null_properties=ignore_null,
                            property_list=self.property_list,
                            object_order=object_order,
                            ctx_options=self.options)

        if self.result_errors:
            if any(self.result_errors.values()):
                self.display_errors(terminate=True)

    def display_errors(self, terminate=False):
        """
        Display any errors in an appropriate format consistent with the
        output format but to stderr.
        """
        rows = []
        # values are (exception, self.obj_type, target_object)
        for ns, exc in self.result_errors.items():
            rows.append([ns, exc.status_code_name, exc.status_description])

        title = "Request Response Errors for Target: ({}) {}". \
            format(self.obj_type, self.target_object)

        if output_format_is_table(self.output_format):
            headers = ['namespace', 'CIMError', "Description"]

            click.echo(format_table(rows, headers,
                                    title=title,
                                    table_format=self.output_format))

        elif output_format_is_cimobject(self.output_format):
            click.echo("\n{}".format(title))
            for row in rows:
                click.echo(
                    "namespace:{} CIMError:{} Description:{}".
                    format(row[0], row[1], row[2]), err=True)

        elif output_format_is_textgroup(self.output_format):
            click.echo("\n{}".format(title))
            for row in rows:
                click.echo(
                    "namespace:{} CIMError:{} Description:{}".
                    format(row[0], row[1], row[2]), err=True)

        # Close with an exception so exception code is raised.
        if terminate:
            raise click.ClickException(
                "Errors encountered on {} server request(s)".
                format(len(self.result_errors)))


def get_namespaces(context, namespaces, default_all_ns=False):
    """
    Returns either the namespaces defined in --namespaces parameter or if
    namespaces is empty, either all of the namespaces available in the server or
    the value None depending on the value of the parameter default_all_ns.

    Processes either single namespace string, single string containing
    multiple comma-separated,namespace definitions  or combination of string
    and tuple.

    This allows a single processor for the namespace option that returns
    namespace or default in a form that matches the type of namespaces
    (tuple, list) or (string, string)

    Parameters:

      context context (:class:`ContextObj` provided with command)

      namespaces (tuple of :term:`string` or :term:`string`)
        tuple of strings where each string is one or more namespace names.
        Any single string can contain one or multiple namespaces by
        comma-separating the namespace names.

      default_all_ns (:class:`py:bool`):
        Boolean that determines return value if namespaces is None or []:
          True: Return all namespaces in server
          False: Return default namespace for current conn (default)

    Returns:
        If namespaces is a tuple, returns list of namespaces with
        comma-separated strings separated into single items in the list
        If namespaces is string, returns the single namespace string
        if namespaces is None, returns None if default_all_ns is False
        or all namespaces in environment if default_all_ns is True

    Raises:
        CIMError if status code not CIM_ERR_NOT_FOUND
    """
    def get_default_ns(default_ns):
        return default_ns if not isinstance(namespaces, tuple) else [default_ns]

    # Return the provided namespace(s) by expanding each entry that has
    # comma-separated values add adding those without comma
    ns_names = []
    if namespaces:
        if isinstance(namespaces, tuple):
            for ns in namespaces:
                ns_names.extend(ns.split(','))
            return ns_names
        return namespaces

    # If default input param is None, return the default namespace.
    # We set the default namespace here rather than None (where the request
    # would get the default namespace) because the find command
    # attempts to build a dict with namespace and None fails
    conn = context.pywbem_server.conn
    default_ns = conn.default_namespace
    assert default_all_ns is not None
    if default_all_ns is False:
        return get_default_ns(default_ns)

    # Otherwise get all namespaces from server
    wbem_server = context.pywbem_server.wbem_server
    try:
        assert isinstance(namespaces, tuple)
        ns_names = wbem_server.namespaces
        ns_names.sort()
        return ns_names

    except ModelError:
        return get_default_ns(default_ns)

    except CIMError as ce:
        # Allow processing to continue if no interop namespace
        if ce.status_code == CIM_ERR_NOT_FOUND:
            warning_msg('{}. Using default_namespace {}.'
                        .format(ce, conn.default_namespace))
            return get_default_ns(default_ns)
        raise click.ClickException('Failed to find namespaces. Exception: {} '
                                   .format(ce))

    except Error as er:
        raise pywbem_error_exception(er)


def enumerate_classes_filtered(context, namespace, classname, options):
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

      context:  (instance of :class:`ContextObj`):
        Used to retrieve conn parameter

      classname (:term:`string`):
        classname for the enumerate or None if all classes to be enumerated.

      options: Click options dictionary
        Options that form basis for this Enumerate and filter processing.

    Returns:
        List of classes or classnames that satisfy the criteria

    Raises:
        pywbem Error exceptions generated by EnumerateClassNames and
        enumerateClasses
    """
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


def parse_version_str(version_str):
    """
    Parse a string with 3 positive integers seperated by period (CIM version
    string) into a 3 integer tuple and return the tuple. Used to parse the
    version value of the DMTF Version qualifier.

    Parameters:
        version_str (:term: str):
            String defining 3 components of a CIM version

    Returns:
        tuple containing 3 integers

    Raises:
        click.ClickException if the version_str is invalid (not integers,
        not seperated by ".", not 3 values)
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
                            val = parse_version_value(cls_version,
                                                      cls.classname)
                            option_value = bool(val >= filter_.optionvalue)

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
