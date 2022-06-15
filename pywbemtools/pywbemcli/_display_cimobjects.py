# (C) Copyright 2020 IBM Corp.
# (C) Copyright 2020 Inova Development Inc.
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
Common function to display cim objects in multiple formats.
display_cimobjects() is the function that should be used for all CIM
object display in pywbemcli.

It displays a list of CIM objects of a single type in multiple formats
defined by output_format (as CIM objects (mof, etc.) as one or more tables
or as text.
"""

from __future__ import absolute_import, print_function, unicode_literals

import re

import six
import click

from pywbem import CIMInstanceName, CIMInstance, CIMClass, \
    CIMQualifierDeclaration, CIMClassName, ValueMapping, siunit_obj, \
    CIMError, CIM_ERR_NOT_SUPPORTED
from pywbem._nocasedict import NocaseDict

from ._common import sort_cimobjects, to_wbem_uri_folded
from ._cimvalueformatter import cimvalue_to_fmtd_string
from .._utils import get_terminal_width
from .._output_formatting import DEFAULT_MAX_CELL_WIDTH, \
    output_format_is_table, format_table, fold_strings

INT_TYPE_PATTERN = re.compile(r'^[su]int(8|16|32|64)$')

# Minimum width for table view cell size. Below this width the columns become
# unreadable.  Note that this overrides the max_terminal width.
MIN_CELL_WIDTH = 10

####################################################################
#
#  Display of CIM objects in format defined by output_format
#
####################################################################


def display_cim_objects(context, cim_objects, output_format, summary=False,
                        property_list=None, quote_strings=True,
                        ignore_null_properties=True):

    """
    Display CIM objects in form determined by input parameters.

    Input is either a list of cim objects or a single object. It may be
    any of the CIM types.  This is used to display:

      * CIMClass
      * CIMClassName:
      * CIMInstance
      * CIMInstanceName
      * CIMQualifierDeclaration
      * class associatiors (tuple of CIMClassName, CIMClass)
      * list of the above types
      * Dictionary of the above types where the keys are namespaces and the
        values are any of the above types. This is the return from commands
        that handle multiple namespaces in the command option --namespace.

    This function may override output type choice in cases where the output
    choice is not available for the object type.  Thus, for example,
    mof output makes no sense for class names. In that case, the output is
    the str with the name or namespace:name.

    Parameters:

      context (:class:`ContextObj`):
        Click context contained in ContextObj object.

      objects (iterable of :class:`~pywbem.CIMInstance`,
        :class:`~pywbem.CIMInstanceName`, :class:`~pywbem.CIMClass`,
        :class:`~pywbem.CIMClassName`,
        :class:`~pywbem.CIMQualifierDeclaration`, or tuple where the tuple
        consists of (CIMClassName, CIMClass) and is return from class
        associators or class references.
        Iterable of zero or more CIM objects to be displayed.  If the iterable
        is a dictionary it contains the objects for multiple namespaces where
        the keys are namespace names and the values are lists of objects in
        the namespace.

      output_format (:term:`string`):
        String defining the preferred output format. Must not be None since
        the correct output_format must have been selected before this call.
        Note that the output formats allowed may depend on a) whether
        summary is True, b)the specific type because we do not have a table
        output format for CIMClass.

      summary (:class:`py:bool`):
        Boolean that defines whether the data in objects should be displayed
        or just a summary of the objects (ex. count of number of objects).

      property_list (iterable of :term:`string`):
        List of property names to be displayed, in the desired order, when the
        output format is a table, or None to use the default of sorting
        the properties alphabetically within key and non-key groups.

      quote_strings (:class:`py.bool`):
        If False, strings are not encased by quote marks in the table view for
        instance displays. The default is True so that strings are encased in
        quotes in all views.

      ignore_null_properties (:class:`py.bool`):
        If True, cases where a property has Null value or does not exist in all
        of the instances to be displayed will not be included in table output.
        They will be included in CIM object(MOF) output. If False, The
        properties that do not have a value in any instance will be included in
        tables.  This allows table output to ignore properties that do not add
        value to the table display.

      namespace  (:term:`string`):
        The names of a namespace if namespace is to be appended to the
        display.  Used only when the command is processing multiple
        namespaces.
    """

    # Note: In the docstring above, the line for parameter 'objects' was too
    #       long. Since we are not putting it into docmentation, we folded it.
    context.spinner_stop()

    # Assure that there is output format exists, None not allowed.
    assert output_format

    # If dictionary of objects in namespaces and there is only one namespace
    # reduce to list of cim objects. Code deals with single namespace request
    # without identifying it in displays as we do for multiple namespace display
    if isinstance(cim_objects, NocaseDict) and len(cim_objects) == 1:
        ns1 = list(cim_objects.keys())
        ns = ns1[0]
        cim_objects = cim_objects[ns]

    # If summary flag, call the summary display function and return
    if summary:
        _display_cim_objects_summary(context, cim_objects, output_format)
        return

    # Terminate if no actual cim_objects returned for single item and list
    # before any further processing. Simplifies further processing so it
    # can ignore None conditions.
    if cim_objects is None or (isinstance(cim_objects, list) and
                               not cim_objects):
        if context.verbose:
            click.echo("No objects returned")
        return

    if isinstance(cim_objects, NocaseDict) and \
            not any(list(cim_objects.values())):
        if context.verbose:
            click.echo("No objects returned for namespace(s): {}".
                       format(", ".join(cim_objects.keys())))
        return

    # Process by type based on receiving dictionaries of ns:objects or lists
    # of objects or tuples from class associators/references

    if output_format_is_table(output_format):
        # Table format output is processed as a group in a single table both
        # for multiple and single namespaces.
        _display_objects_as_table(cim_objects, output_format, context,
                                  property_list, quote_strings,
                                  ignore_null_properties, namespace=None)
        return

    # CIM Object and text output formats are displayed as single objects.
    # Note: for class associaters/references each object is a tuple of
    # CIMClassName, CIMClass
    if isinstance(cim_objects, NocaseDict):
        for ns, ns_objects in cim_objects.items():
            if not isinstance(ns_objects, list):
                ns_objects = [ns_objects]
            ns_objects = sort_cimobjects(ns_objects)
            for obj in ns_objects:
                _display_one_cim_object(
                    context, obj, output_format, property_list, quote_strings,
                    ignore_null_properties, namespace=ns)
        return

    # If not NocaseDict, it is list or single object. Sort by classname and
    # then call _display_one_cim_objects with each item from list
    if not isinstance(cim_objects, list):
        cim_objects = [cim_objects]
    if isinstance(cim_objects, list):
        # Sort the objects by classname and call to display each object
        cim_objects = sort_cimobjects(cim_objects)
        for obj in cim_objects:
            _display_one_cim_object(
                context, obj, output_format, property_list, quote_strings,
                ignore_null_properties)


############################################################################
#
# Support methods for displaying CIM objects.  This includes multiple
# output formats (ie. MOF, TABLE, TEXT), table display and summary display.
#
############################################################################


def _display_one_cim_object(context, cim_object, output_format, property_list,
                            quote_strings, ignore_null_properties,
                            namespace=None):

    """
    Display a single CIM object.  This creates and outputs the display for one
    CIM object in  the output formats groups CIM object (MOF, XML, Text).
    """
    assert isinstance(
        cim_object, (CIMClass, CIMClassName, CIMInstance, CIMInstanceName,
                     CIMQualifierDeclaration, tuple, six.string_types))

    if output_format_is_table(output_format):
        _display_objects_as_table([cim_object], output_format, context,
                                  property_list, quote_strings,
                                  ignore_null_properties, namespace)

    # Display in the selected CIM object format (mof, xml, repr, txt)
    elif output_format == 'mof':
        try:
            mofstr = cim_object.tomof()
            if namespace:
                click.echo("#pragma namespace (\"{}\")".format(namespace))
            click.echo(mofstr)
        except AttributeError:
            # inserting NL between instance names for readability
            if isinstance(cim_object, CIMInstanceName):
                click.echo("")
                click.echo(cim_object)
            elif isinstance(cim_object, CIMClassName):
                click.echo(cim_object)
            elif isinstance(cim_object, tuple):  # representation of class assoc
                assert isinstance(cim_object[0], CIMClassName)
                assert isinstance(cim_object[1], CIMClass)
                click.echo(cim_object[0])
                click.echo(cim_object[1].tomof())
            elif isinstance(cim_object, six.string_types):
                if namespace:
                    click.echo("{}:{}".format(namespace, cim_object))
                else:
                    click.echo(cim_object)
            else:
                raise click.ClickException('output_format {} invalid for {} '
                                           .format(output_format,
                                                   type(cim_object)))
    elif output_format == 'xml':
        try:
            if isinstance(cim_object,
                          (CIMClass, CIMInstance, CIMQualifierDeclaration,
                           CIMInstanceName, CIMClassName)):
                if namespace:
                    click.echo("<!-- Namespace = {} -->".format(namespace))
                click.echo(cim_object.tocimxmlstr(indent=4))
            elif isinstance(cim_object, tuple):
                if namespace:
                    click.echo("<!-- Namespace = {} -->".format(namespace))
                assert isinstance(cim_object[0], CIMClassName)
                assert isinstance(cim_object[1], CIMClass)
                click.echo(cim_object[0].tocimxmlstr(indent=4))
                click.echo(cim_object[1].tocimxmlstr(indent=4))
            elif isinstance(cim_object, six.string_types):
                if namespace:
                    click.echo("{}:{}".format(namespace, cim_object))
                else:
                    click.echo(cim_object)
            else:
                assert False, "Output_format {} invalid for {}".format(
                    output_format, type(cim_object))

        except AttributeError:
            # no tocimxmlstr functionality
            raise click.ClickException('Output Format {} not supported. '
                                       'Default to\n{!r}'
                                       .format(output_format, cim_object))
    elif output_format == 'repr':
        try:
            click.echo(repr(cim_object))
        except AttributeError:
            raise click.ClickException('"repr" display of {!r} failed'
                                       .format(cim_object))

    elif output_format == 'txt':
        try:
            click.echo(cim_object)
        except AttributeError:
            raise click.ClickException('"txt" display of {!r} failed'
                                       .format(cim_object))
    else:
        raise click.ClickException('Invalid output format {}'
                                   .format(output_format))


def _display_objects_as_table(objects, output_format, context,
                              property_list, quote_strings,
                              ignore_null_properties, namespace=None):
    """
    Call the method for each type of object to print that object type
    information as a table.  This function process objects from multiple
    namespaces in a NocaseDict to produce a single table showing the
    requested output in one row per namespace/class.

    Output format is retrieved from context.

    Parameters:
      objects: list or NocaseDict
        If objects is a list, it is processing a single namespace.  If it is
        a dictionary it is processing multiple namespaces.

      namespace (bool or string containing namespace)
        If bool, indicates that namespace should be included in the output
        for each object.  If string, it is only for class enumerate where we
        do not yet have a table output for class.

    """
    table_width = get_terminal_width()

    if isinstance(objects, NocaseDict):
        # Everything except classes and classnames includes namespace
        # convert back to a single list so a single table can be created
        #
        new_objects = []
        # If the object type is string, it is just a classname.
        # Expand to create list of tuples of (ns, classname)
        # Otherwise, just map the values to a single list
        for ns, values in objects.items():
            if values:
                if not isinstance(values, list):
                    values = [values]
                if isinstance(values[0], six.string_types):
                    new_objects.extend([CIMClassName(v, namespace=ns)
                                        for v in sort_cimobjects(values)])
                else:
                    new_objects.extend(sort_cimobjects(values))

        namespace = True
        objects = new_objects
    if objects:
        # If single object, cvt to list for further processing
        if not isinstance(objects, (list)):
            objects = [objects]
        objects = sort_cimobjects(objects)
        if isinstance(objects[0], CIMInstance):
            _display_instances_as_table(
                objects, table_width, output_format,
                context=context,
                property_list=property_list,
                quote_strings=quote_strings,
                ignore_null_properties=ignore_null_properties,
                namespace=namespace)
        elif isinstance(objects[0], CIMClass):
            _display_classes_as_table(objects, table_width, output_format)
        elif isinstance(objects[0], CIMQualifierDeclaration):
            _display_qual_decls_as_table(objects, table_width, output_format)
        elif isinstance(objects[0], (CIMClassName, CIMInstanceName,
                                     six.string_types, tuple)):
            _display_paths_as_table(objects, table_width, output_format,
                                    namespace=namespace)
        else:
            raise click.ClickException("Cannot print {} as table"
                                       .format(type(objects[0])))


def _get_cimtype(objects):
    """
    Get the cim_type for any returned cim object.  Normally this is the
    name of the class name except that the classname return from
    getclass and enumerate class is just unicode string

    Parameters:
      objects (dict, list, object where object is any CIM object or tuple)

    Returns:
      The CIM type (string) for that object. If the object is a tuple, the
      type comes from the second object in the tuple

      If no objects are in thd dict or list None is returned

    """
    # associators and references return tuple
    if isinstance(objects, list) and objects:
        test_object = objects[0]
    elif objects:
        test_object = object
    else:
        return None

    if isinstance(test_object, tuple):
        # associator or reference class level return is tuple get type
        # from second item, it is the requested object
        cim_type = test_object[1].__class__.__name__
    else:
        cim_type = test_object.__class__.__name__

    # account for fact the enumerate class name operation returns uniicode.
    if isinstance(test_object, six.string_types):
        cim_type = 'CIMClassName'
    return cim_type


def _display_cim_objects_summary(context, objects, output_format):
    """
    Display a summary of the objects received. This displays the
    count of objects.
    """
    context.spinner_stop()

    cim_type = None
    if isinstance(objects, NocaseDict):
        headers = ['Namespace', 'Count', 'CIM Type']
        rows = []
        for ns, objlist in objects.items():
            if not cim_type:
                cim_type = _get_cimtype(objlist)
            rows.append([ns, len(objlist), cim_type])
    else:
        headers = ['Count', 'CIM Type']
        if isinstance(objects, list):
            cim_type = _get_cimtype(objects)
            rows = [[len(objects), cim_type]]
        elif objects is not None:
            cim_type = _get_cimtype(objects)
            rows = [["1", cim_type]]
        else:
            rows = [[0, cim_type]]

    title = 'Summary of {}(s) returned'.format(cim_type)
    if output_format_is_table(output_format):
        click.echo(format_table(rows, headers, title=title,
                                table_format=output_format))
    else:
        for row in rows:  # must be type text
            # The following two are hangover from initial format output
            # "<number <object_name>(s)". Future, redo this whole output format
            cim_type_pos = len(row) - 1
            len_pos = len(row) - 2
            if row[len_pos] == 0:
                row[cim_type_pos] = "objects"
            else:
                row[cim_type_pos] = "{}(s)".format(row[cim_type_pos])
            row[len_pos] = str(row[len_pos])
            click.echo('{} returned'.format(" ".join(row)))


def _display_classes_as_table(classes, table_width, table_format):
    """
    Display classes as a table.
    """
    # pylint: disable=unused-argument

    # ISSUE #249: Display classes as a table or mof rather than just as MOF.
    for class_ in classes:
        click.echo(class_.tomof())


def _display_paths_as_table(objects, table_width, table_format, namespace=None):
    # pylint: disable=unused-argument
    """
    Display paths as a table. This include CIMInstanceName, ClassPath,
    and unicode (the return type for enumerateClasses).
    """
    title = None
    if objects:
        if isinstance(objects[0], six.string_types):
            title = 'Classnames:'
            if namespace:
                title = title + (" namespace: {}".format(namespace))
            headers = ['Class Name']
            if namespace:
                rows = [[namespace, obj] for obj in objects]
            else:
                rows = [[obj] for obj in objects]
        # if obj is tuple, this is a tuple of namespace and classname
        elif isinstance(objects[0], tuple):
            title = 'Classnames:'
            headers = ("namespace", 'class')
            rows = [[obj[0], obj[1]] for obj in objects]

        elif isinstance(objects[0], CIMClassName):
            title = 'Classnames'
            headers = ('host', 'namespace', 'class')
            rows = [[obj.host, obj.namespace, obj.classname] for obj in objects]

        elif isinstance(objects[0], CIMInstanceName):
            # Since there are cases where the list has instances with
            # different keys (i.e. enumerate CIM_ManagedElement), build
            # a dictionary for instances with the same key names.
            # Sort into dictionary for each set of key names.  If all keys are
            # the same, there will be one table.  This allows building
            # a table for each set of keynames
            objs_by_key_set = {}
            original_keys = {}

            for instname in objects:
                # key_names is a tuple of sorted key names in lower case so
                # all instances with the same set of keys ends up in a
                # single dictionary item. NOTE: objects must be tuple to be
                # a dictionary key, the key.
                test_key_names = tuple(
                    sorted(map(lambda x: x.lower(), instname.keys())))
                try:
                    objs_by_key_set[test_key_names].append(instname)
                except KeyError:
                    objs_by_key_set[test_key_names] = [instname]

                # Set the original keys into dict to recover correct key
                # case later
                if test_key_names not in original_keys:
                    original_keys[test_key_names] = instname.keys()

            # If multiple key_names we create multiple tables and add table
            # number to each table title.
            # FUTURE: This was a hack. by forcing classname into the table
            table_number = 0
            for key_names, inst_names in objs_by_key_set.items():
                # Build headers for this table with the common elements and key
                # names for each key in the object. We use inst_names[0] to
                # restore original case to key strings. We sort keys for
                # consistent table output.
                inst_keys = sorted(original_keys[key_names])

                rows = []
                for instname in inst_names:
                    # Build header row for this table
                    row = [instname.host, instname.namespace,
                           instname.classname]
                    for key in inst_keys:
                        if isinstance(instname[key], CIMInstanceName):
                            # If key is CIMInstanceName, fold the value
                            row.append(to_wbem_uri_folded(
                                instname[key], uri_format='standard',
                                max_len=30))
                        else:
                            row.append(instname[key])
                    rows.append(row)

                # If multiple tables, number them as hint to reader that there
                # are multiples.
                if len(objs_by_key_set) > 1:
                    table_number += 1
                    table_number_str = ", (table #{})".format(table_number)
                else:
                    table_number_str = ''

                headers = ['host', 'namespace', 'class'] + \
                    ["key=\n{0}".format(kn) for kn in inst_keys]

                title = 'InstanceNames: {0}{1}'.format(inst_names[0].classname,
                                                       table_number_str)

                # Generate multiple tables, one for each key_name and
                # return local to this scope.
                click.echo(format_table(rows, headers, title=title,
                                        table_format=table_format))

            return  # Return to avoid following table output

        else:
            raise click.ClickException("{0} invalid type ({1})for path display".
                                       format(objects[0], type(objects[0])))

        click.echo(format_table(rows, headers, title=title,
                                table_format=table_format))


def _display_qual_decls_as_table(qual_decls, table_width, table_format):
    """
    Display the elements of qualifier declarations as a table with a
    row for each qualifier declaration and a column for each of the attributes
    of the qualifier declaration (name, type, Value, Array, Scopes, Flavors.

    The function displays all of the qualifier declarations in the
    """
    rows = []
    headers = ['Name', 'Type', 'Value', 'Array', 'Scopes', 'Flavors']
    max_column_width = int(table_width / len(headers)) - 4
    for q in qual_decls:
        scopes = '\n'.join([key for key in q.scopes if q.scopes[key]])
        flavors = []
        flavors.append('EnableOverride' if q.overridable else 'DisableOverride')
        flavors.append('ToSubclass' if q.tosubclass else 'Restricted')
        if q.translatable:
            flavors.append('Translatable')
        if sum(map(len, flavors)) >= max_column_width:
            sep = "\n"
        else:
            sep = ", "
        flavors = sep.join(flavors)

        row = [q.name, q.type, q.value, q.is_array, scopes, flavors]
        rows.append(row)

    click.echo(format_table(rows, headers, title='Qualifier Declarations',
                            table_format=table_format))


def _format_instances_as_rows(insts, max_cell_width, include_classes=False,
                              context=None, prop_names=None,
                              quote_strings=True, namespace=None):
    """
    Format the list of instances properties into a list of the property
    values for each instance(a row of the table) gathered into a list of
    the rows.

    The prop_names parameter is the list of (originally cased) property names
    to be output, in the desired output order. It could be determined from
    the instances, but since it is determined already by the caller, it
    is passed in as an optimization. For test convenience, None is permitted
    and causes the properties to again be determined from the instances.

    Include_classes for each instance if True. Sets the classname as the first
    column.

    max_width if not None folds col entries longer than the defined
    max_cell_width. If max_width is None, the data length is ignored.

    The property values are formatted similar to MOF output. Properties that
    have a ValueMap qualifier (effectively, in the creation class of the
    instance) are shown with both the actual property value and the mapped
    value in parenthesis.

    NOTE: This is a separate function to allow testing of the table formatting
    independently of print output.

    Returns:
        list of strings where each string is a row in the table and each
        item in a row is a cell entry
    """
    conn = context.pywbem_server.conn if context else None

    # Avoid crash deeper in code if max_cell_width is None.
    if max_cell_width is None:
        max_cell_width = DEFAULT_MAX_CELL_WIDTH
    rows = []

    # Build list of properties in any of the instances to display.
    if prop_names is None:
        prop_names = _sorted_prop_names(insts)

    # Cache of ValueMapping objects for integer-typed properties.
    # Key: classname.propertyname, both in lower case.
    # A value of None indicates the property does not have a value mapping.
    valuemappings = {}

    for inst in insts:
        assert isinstance(inst, CIMInstance), \
            "Invalid CIM Type {}".format(type(inst))

        # Setup row list and set namespace if this is multi-namespace
        # Note: We use namespace as a flag here ignoring the actual values.
        row = [inst.path.namespace] if namespace else []

        # Insert classname as before properties if flag set
        if include_classes:
            row.append([inst.classname])

        # Get value for each property in this object
        for name in prop_names:
            # Account for possible instances without all properties
            # Outputs empty  string.  Note that instance with no value
            # results in same output as not instance name.
            if name not in inst.properties:
                val_str = ''
            else:
                value = inst.get(name)
                prop = inst.properties[name]

                # Cache value mappings for integer-typed properties
                if INT_TYPE_PATTERN.match(prop.type) and context:
                    vm_key = '{}.{}'.format(
                        inst.classname.lower(), name.lower())
                    try:
                        valuemapping = valuemappings[vm_key]
                    except KeyError:
                        try:
                            valuemapping = ValueMapping.for_property(
                                conn,
                                inst.path.namespace,
                                inst.classname,
                                name)
                        except ValueError:
                            # Property does not have a value mapping.
                            valuemapping = None
                        valuemappings[vm_key] = valuemapping
                else:
                    valuemapping = None

                if value is None:
                    val_str = u''
                else:
                    val_str, _ = cimvalue_to_fmtd_string(
                        prop.value, prop.type, indent=0, maxline=max_cell_width,
                        line_pos=0, end_space=0, avoid_splits=False,
                        valuemapping=valuemapping, quote_strings=quote_strings)
            row.append(val_str)
        rows.append(row)

    return rows


def _display_instances_as_table(insts, table_width, table_format,
                                include_classes=False, context=None,
                                property_list=None, quote_strings=True,
                                ignore_null_properties=True,
                                namespace=None):
    """
    Print the properties of the instances defined in insts as a table where
    each row is an instance and each column is a property value.

    All properties in the instance are included.

    The header line consists of the property names.

    The property values are formatted similar to MOF output. Properties that
    have a ValueMap qualifier (effectively, in the creation class of the
    instance) are shown with both the actual property value and the mapped
    value in parenthesis.

    """
    conn = context.pywbem_server.conn if context else None

    if table_width is None:
        table_width = get_terminal_width()

    for inst in insts:
        assert isinstance(inst, CIMInstance)

    # Build list of properties, either all properties in a list or all
    # properties in all instances in list of instances
    if property_list:
        prop_names = _propertylist_prop_names(insts, property_list)
    else:
        prop_names = _sorted_prop_names(insts)

    if ignore_null_properties:
        # Get names of properties in any instances that have a value (i.e.
        # not None or empty list)
        props_with_value_dict = NocaseDict()
        for inst in insts:
            for propname, propvalue in inst.properties.items():
                if propvalue.value is not None:
                    props_with_value_dict[propname] = True
        # Rebuild prop names from dict in same order as original list
        prop_names = [pn for pn in prop_names if pn in props_with_value_dict]

    # Try to estimate max cell width from number of cols and properties
    # This allows folding long data. Further, the actual output
    # width of a column involves the tabulate outputter, output_format
    # so this is not deterministic.
    if prop_names:
        max_cell_width = int(table_width / len(prop_names))
    else:
        max_cell_width = table_width

    # Sets a minimum size for cells so they are at least readable.
    # This means we can build tables wider than the terminal width.
    max_cell_width = max(max_cell_width, MIN_CELL_WIDTH)

    # ISSUE #953 Future: Decide whether and how the showing of units should be
    #            controlled. Or are we satisfied with always showing them?
    show_units = True

    # Retrieve all creation classes of the instances in order to get
    # to their PUnit and Units qualifiers.
    if show_units:
        class_objs = NocaseDict()  # CIMClass objects, by classname
        for inst in insts:
            classname = inst.classname
            if classname in class_objs:
                continue
            if inst.path is None:
                # The only operation returning instances without a path is
                # query execution. For now, we simply don't display units in
                # case the inst.path is None.
                # ISSUE #953: Pass the namespace for query execution to allow
                # class retrieval as part of getting  units information.
                show_units = False
                break
            try:
                class_obj = conn.GetClass(
                    classname, namespace=inst.path.namespace,
                    IncludeQualifiers=True, LocalOnly=False)
            except CIMError as exc:
                if exc.status_code == CIM_ERR_NOT_SUPPORTED:
                    # The WBEM Server does not support class operations. We
                    # silently give up showing units in this case.
                    show_units = False
                    break
            class_objs[classname] = class_obj

    # Construct the header line
    headers = []  # list of header strings
    # If we want to include namespace in table as a row
    if namespace:
        headers.append("namespace")
    if include_classes:
        headers.append("classname")
    for pname in prop_names:
        hdr = pname
        if show_units:
            # In theory, two leaf classes from different vendors could have
            # introduced same-named properties with different unit definitions.
            # We account for that by showing a list of units in that case.
            siunits = []
            for class_obj in class_objs.values():
                if pname not in class_obj.properties:
                    # Not all classes may have the property, but one of them
                    # will.
                    continue
                prop_obj = class_obj.properties[pname]
                siunit = siunit_obj(prop_obj)
                if siunit is not None and siunit not in siunits:
                    siunits.append(siunit)
            for siunit in siunits:
                hdr += " [{}]".format(siunit)
        headers.append(hdr)

    rows = _format_instances_as_rows(
        insts, max_cell_width,
        include_classes=include_classes,
        context=context, prop_names=prop_names,
        quote_strings=quote_strings, namespace=namespace)

    # Fold the headers if necessary. Fold on either hypens or single word
    # too long because the headers are all single words
    disp_headers = []
    for header in headers:
        if len(header) > max_cell_width:
            disp_headers.append(fold_strings(header,
                                             max_cell_width,
                                             break_long_words=True,
                                             break_on_hyphens=True))
        else:
            disp_headers.append(header)

    title = 'Instances: {}'.format(insts[0].classname)

    click.echo(format_table(rows, disp_headers, title=title,
                            table_format=table_format))


def _sorted_prop_names(insts):
    """
    Return the list of (originally cased) property names that is the superset
    of all properties in the  any of theinput instances.

    The returned list has the key properties first, followed by the non-key
    properties. Each group is sorted case insensitively.

    The key properties are determined from the instance paths, if present.
    The function tolerates it if only some of the instances have a path,
    and if instances of subclasses have additional keys.
    """

    all_props = NocaseDict()  # key: org prop name, value: lower prop name
    key_props = NocaseDict()  # key: org prop name, value: lower prop name
    for inst in insts:
        for pn in inst.properties:
            all_props[pn] = pn.lower()
            if inst.path and pn in inst.path.keybindings:
                key_props[pn] = pn.lower()

    nonkey_props = NocaseDict()  # key: org prop name, value: lower prop name
    for pn in all_props:
        if pn not in key_props:
            nonkey_props[pn] = all_props[pn]

    key_prop_list = sorted(key_props.keys(), key=lambda pn: key_props[pn])
    nonkey_prop_list = sorted(
        nonkey_props.keys(), key=lambda pn: nonkey_props[pn])
    key_prop_list.extend(nonkey_prop_list)
    return key_prop_list


def _propertylist_prop_names(insts, property_list):
    """
    Return the originally cased property list, based on the lexical case
    in the instances.

    If a property name is not in any instance, it is not returned.
    """
    prop_list = []
    for pname in property_list:
        for inst in insts:
            if pname in inst:
                prop_list.append(inst.properties[pname].name)
                break
    return prop_list
