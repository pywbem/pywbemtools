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
"""

from __future__ import absolute_import, print_function, unicode_literals

import re

from pydicti import odicti
import six
import click
from nocaselist import NocaseList
from nocasedict import NocaseDict

from pywbem import CIMInstanceName, CIMInstance, CIMClass, \
    CIMQualifierDeclaration, CIMClassName, ValueMapping, siunit_obj, \
    CIMError, CIM_ERR_NOT_SUPPORTED

from ._common import format_table, fold_strings, DEFAULT_MAX_CELL_WIDTH, \
    output_format_is_table, sort_cimobjects, format_keys, \
    hide_empty_columns

from .config import DEFAULT_TABLE_WIDTH, USE_TERMINAL_WIDTH

from ._cimvalueformatter import cimvalue_to_fmtd_string

INT_TYPE_PATTERN = re.compile(r'^[su]int(8|16|32|64)$')


####################################################################
#
#  Display of CIM objects.
#
####################################################################


def display_cim_objects(context, cim_objects, output_format, summary=False,
                        sort=False):
    """
    Display CIM objects in form determined by input parameters.

    Input is either a list of cim objects or a single object. It may be
    any of the CIM types.  This is used to display:

      * CIMClass

      * CIMClassName:

      * CIMInstance

      * CIMInstanceName

      * CIMQualifierDeclaration

      * Or list of the above

    This function may override output type choice in cases where the output
    choice is not available for the object type.  Thus, for example,
    mof output makes no sense for class names. In that case, the output is
    the str of the type.

    Parameters:

      context (:class:`ContextObj`):
        Click context contained in ContextObj object.

      objects (iterable of :class:`~pywbem.CIMInstance`,
        :class:`~pywbem.CIMInstanceName`, :class:`~pywbem.CIMClass`,
        :class:`~pywbem.CIMClassName`,
        or :class:`~pywbem.CIMQualifierDeclaration`):
        Iterable of zero or more CIM objects to be displayed.

      output_format (:term:`string`):
        String defining the preferred output format. Must not be None since
        the correct output_format must have been selected before this call.
        Note that the output formats allowed may depend on a) whether
        summary is True, b)the specific type because we do not have a table
        output format for CIMClass.

      summary (:class:`py:bool`):
        Boolean that defines whether the data in objects should be displayed
        or just a summary of the objects (ex. count of number of objects).
    """
    # Note: In the docstring above, the line for parameter 'objects' was way too
    #       long. Since we are not putting it into docmentation, we folded it.

    context.spinner_stop()

    if summary:
        display_cim_objects_summary(context, cim_objects, output_format)
        return

    if not cim_objects and context.verbose:
        click.echo("No objects returned")
        return

    if sort:
        cim_objects = sort_cimobjects(cim_objects)

    # default when displaying cim objects is mof
    assert output_format

    if isinstance(cim_objects, (list, tuple)):
        # Table format output is processed as a group
        if output_format_is_table(output_format):
            _display_objects_as_table(cim_objects, output_format,
                                      context=context)
        else:
            # Call to display each object
            for obj in cim_objects:
                display_cim_objects(context, obj, output_format=output_format)
        return

    # Display a single item.
    object_ = cim_objects
    # This allows passing single objects to the table formatter (i.e. not lists)
    if output_format_is_table(output_format):
        _display_objects_as_table([object_], output_format, context=context)
    elif output_format == 'mof':
        try:
            click.echo(object_.tomof())
        except AttributeError:
            # insert NL between instance names for readability
            if isinstance(object_, CIMInstanceName):
                click.echo("")
                click.echo(object_)
            elif isinstance(object_, (CIMClassName, six.string_types)):
                click.echo(object_)
            else:
                raise click.ClickException('output_format {} invalid for {} '
                                           .format(output_format,
                                                   type(object_)))
    elif output_format == 'xml':
        try:
            click.echo(object_.tocimxmlstr(indent=4))
        except AttributeError:
            # no tocimxmlstr functionality
            raise click.ClickException('Output Format {} not supported. '
                                       'Default to\n{!r}'
                                       .format(output_format, object_))
    elif output_format == 'repr':
        try:
            click.echo(repr(object_))
        except AttributeError:
            raise click.ClickException('"repr" display of {!r} failed'
                                       .format(object_))

    elif output_format == 'txt':
        try:
            click.echo(object_)
        except AttributeError:
            raise click.ClickException('"txt" display of {!r} failed'
                                       .format(object_))
    # elif output_format == 'tree':
    #    raise click.ClickException('Tree output format not allowed')
    else:
        raise click.ClickException('Invalid output format {}'
                                   .format(output_format))


def _display_objects_as_table(objects, output_format, context=None):
    """
    Call the method for each type of object to print that object type
    information as a table.

    Output format is retrieved from context.
    """
    if USE_TERMINAL_WIDTH:
        table_width = click.get_terminal_size()[0]
    else:
        table_width = DEFAULT_TABLE_WIDTH

    if objects:
        if isinstance(objects[0], CIMInstance):
            _display_instances_as_table(objects, table_width, output_format,
                                        context=context)
        elif isinstance(objects[0], CIMClass):
            _display_classes_as_table(objects, table_width, output_format,
                                      context=context)
        elif isinstance(objects[0], CIMQualifierDeclaration):
            _display_qual_decls_as_table(objects, table_width, output_format)
        elif isinstance(objects[0], (CIMClassName, CIMInstanceName,
                                     six.string_types)):
            _display_paths_as_table(objects, table_width, output_format)
        else:
            raise click.ClickException("Cannot print {} as table"
                                       .format(type(objects[0])))


############################################################################
#
# Support methods for displaying CIM objects.  This includes multiple
# output formats (ie.e MOF, TABLE, TEXT)
#
############################################################################


def get_cimtype(objects):
    """
    Get the cim_type for any returned cim object.  Normally this is the
    name of the class name except that the classname return from
    getclass and enumerate class is just unicode string
    """
    # associators and references return tuple
    if isinstance(objects, list):
        test_object = objects[0]
    elif objects:
        test_object = object
    else:
        cim_type = 'unknown'
        return None

    if isinstance(test_object, tuple):
        # associator or reference class level return is tuple
        cim_type = test_object[0].__class__.__name__
    else:
        cim_type = test_object.__class__.__name__

    # account for fact the enumerate class name operation returns uniicode.
    if isinstance(test_object, six.string_types):
        cim_type = 'CIMClassName'
    return cim_type


def display_cim_objects_summary(context, objects, output_format):
    """
    Display a summary of the objects received. This displays the
    count of objects.
    """
    context.spinner_stop()

    if objects:
        cim_type = get_cimtype(objects)

        if output_format_is_table(output_format):
            rows = [[len(objects), cim_type]]
            click.echo(format_table(rows, ['Count', 'CIM Type'],
                                    title='Summary of {} returned'
                                    .format(cim_type),
                                    table_format=output_format))
            return
        click.echo('{} {}(s) returned'.format(len(objects), cim_type))

    else:
        click.echo('0 objects returned')


class TableCell(object):
    """
    Defines a single cell of data for a table. This data may be of any
    python type.
    The data can be manipulated including folding it as a string into multiple
    lines and computing the length and width of the data.
    """
    def __init__(self, data, max_width=None, break_long_words=False,
                 break_on_hyphens=False, fold_list_items=False, separator=', ',
                 initial_indent='', subsequent_indent=''):
        """
        Capture the data for the cell and optionally fold it immediatly if
        the max_width parameter is defined.
        """
        self._data = data
        # TODO: Handle lists including cvt to strings.
        # optional. If max_width on constructor fold  immediatly
        if data and max_width:
            self.fold(max_width, break_long_words, break_on_hyphens,
                      fold_list_items, initial_indent, subsequent_indent)

    @property
    def data(self):
        """
        Returns the string representation of the data including any folding
        """
        return self._data

    @property
    def width(self):
        """
        Get the maximum length between EOL characters which is the the maximum
        display width of this cell. That is the cell width. If the cell data is
        not a string, return the length of the string representation of the
        cell.

        Parameters:
          cell (:term:`string` or int or bool or float):
            String that may contain EOL characters.  The width is defined as the
            maximum number of characters on a single line in the string

        Returns:
            Integer defining the width of the cell where width is the maximum
            number of characters on a single line
        """
        if self._data is None:
            return 0
        #if isinstance(self._data, (list, tuple))
        #    return ','.join(str(item) for item in self._data)
        # The following are all one line per cell.
        if isinstance(self._data, (six.integer_types, float, bool)):
            return len(str(self._data))

        assert isinstance(self._data, six.string_types)
        lines = self._data.split("\n")
        return len(max(lines, key=len))

    @property
    def length(self):
        """
        Return the length of the string value of the item
        """
        if self._data is None:
            return 0
        if isinstance(self.data, six.string_types):
            return len(self._data)
        else:
            return len(str(self._data))

    def __str__(self):
        return self.data

    def __repr__(self):
        return "TableCell {}".self.format(self.data)

    def fold(self, max_width, break_long_words=False,
             break_on_hyphens=False, fold_list_items=False, separator=', ',
             initial_indent='', subsequent_indent=''):
        """
        Fold the data based on the max_length attribute.
        """
        if isinstance(self._data, (six.string_types, list, tuple)):
            self._data = fold_strings(self._data, max_width,
                                      break_long_words=break_long_words,
                                      break_on_hyphens=break_on_hyphens,
                                      fold_list_items=fold_list_items,
                                      separator=separator,
                                      initial_indent=initial_indent,
                                      subsequent_indent=subsequent_indent)
        else:
            assert False, "Fold failed bad type {}".format(type(self._data))


class TableColumn(object):
    """
    Represents a single column in a table.  Made up of 0 or more
    TableCell objects
    """
    def __init__(self, cells):
        """
        """
        if isinstance(cells, (tuple, list)):
            self._column = cells
        else:
            self._column = [cells]
        for item in cells:
            assert isinstance(item, TableCell)

    #def __str__(self):
    #    return ", ".format(self._column)

    @property
    def data(self):
        """
        Returns the cells of the row possibly modified by fold, etc.
        """
        return [cell.data for cell in self._column]

    def __repr__(self):
        return ", ".join([str(item) for item in self._column])

    def widths(self):
        """
        Returns a list of the width of each cell entry in the column
        """
        return [cell.width for cell in self._column]

    def max_width(self):
        """
        Return the maximum cell width in a column
        Parameters:
            col (list/tuple of ints, floats, strings)

        Returns:
            integer defining the maximum with of a cell in the column
        """

        assert isinstance(self._column, (list, tuple))

        return max([cell.width for cell in self._column])

    def fold(self, max_width, break_long_words=False,
             break_on_hyphens=False, fold_list_items=False, separator=', ',
             initial_indent='', subsequent_indent=''):
        """
        Fold the cells in the column
        """
        for cell in self._column:
            fold_strings(self, max_width, break_long_words=break_long_words,
                         break_on_hyphens=break_on_hyphens,
                         fold_list_items=fold_list_items, separator=separator,
                         initial_indent=initial_indent,
                         subsequent_indent=subsequent_indent)


def _build_class_as_table(klass, table_width, table_format, context):
    """

    Parameters:

      klass ():
      table_width
      table_format

    Returns:

    Raises: TODO
    """
    def build_qualifiers_cell(obj, width, exclude=[]):
        """
        Build a multiline string for the names and values of the qualifiers
        defined in qualifiers. Each qualifier name and value is in mof format
        on one or more lines.

        Parameters:

          obj :
            The CIM object from which the qualifiers are to be extracted

          width TODO

          exclude (NocaseList)
        """
        qualifiers = obj.qualifiers.values()
        qualifier_entries = []
        if not qualifiers:
            return None
        for qualifier in qualifiers:
            #if qualifier.name in exclude:
            #    continue
            if 'description' == qualifier.name.lower():
                continue
            qualifier_entries.append(
                qualifier.tomof(indent=0, maxline=width))

        return TableCell("\n".join(qualifier_entries))

    def get_classorigin(obj, classname):
        """
        Return the class origin classname if class)origin exists
        """
        # TODO: We need option to show all classnames
        if obj.class_origin != classname:
            return obj.class_origin

        return None

    def build_description_cell(obj, max_width):
        """
        Get the description from the qualifiers attached to obj.  Returns
        the description value or None if there  is no description
        """
        if 'Description' in obj.qualifiers:
            description = TableCell(obj.qualifiers['Description'].value)
            description.fold(max_width)
            return description
        return TableCell(None)

    def build_type_cell(obj):
        """
        Build a string that defines the object type, arrayness and if it
        is a reference type, the Reference class. The object type string is the
        actual pywbem string for that type except for reference which returns
        "REF".

        If embedded_data is set, this is added to the type string as
        EMB(<embedded object type>)

        Returns "<type>", or  "<type>[]" or "<type>[int]" and if reference
        type "reference_class"

        """
        if obj.is_array:
            array_size = str(obj.array_size) if obj.array_size else ""
            array = "[{0}]".format(array_size)
        else:
            array = ''
        if obj.embedded_object:
            embed_object = "\nEMB(object.embedded_object)"
        else:
            embed_object = ""
        if obj.type == 'reference':
            return TableCell("{}{}({}{})".format('REF', array,
                                                 obj.reference_class,
                                                 embed_object))
        return TableCell("{}{}{}".format(obj.type, array, embed_object))

    def build_parameters_subtable(parameters, width, table_format):
        """
        Build a subtable of the parameters for a method
        """
        qualifier_exclude_list = NocaseList(["Description"])
        rows = []
        if not parameters:
            return None
        headers = ["Name", "Type", "Value", "Description", "Qualifiers"]

        for param in parameters:
            name_cell = TableCell(param.name)
            type_and_array_cell = build_type_cell(param)
            # TODO format value
            value_cell = TableCell(param.value)
            description_cell = build_description_cell(param, 40)
            param_qualifiers_cell = build_qualifiers_cell(
                param, width, exclude=qualifier_exclude_list)

            row = [name_cell.data, type_and_array_cell.data,
                   value_cell.data, description_cell.data,
                   param_qualifiers_cell.data]
            rows.append(row)

        hide_empty_columns(headers, rows)
        return format_table(rows, headers, table_format=table_format)
    subtable_width = table_width - 12

    # Build class subtable
    subclasses_cell_width = 30
    subclasses = context.conn.EnumerateClassNames(ClassName=klass.path)
    subclasses_cell = TableCell(subclasses,
                                max_width=subclasses_cell_width,
                                break_long_words=False,
                                break_on_hyphens=False,
                                fold_list_items=True)

    # Create class qualifiers subtable
    qualifier_exclude_list = NocaseList([])
    qual_cell_width = subtable_width - 16 if subtable_width > 90 else 12
    qualifiers_cell = build_qualifiers_cell(klass,
                                            qual_cell_width,
                                            exclude=qualifier_exclude_list)

    class_header = ['Superclass', 'Subclasses', 'Description', 'Qualifiers']

    superclass_cell = TableCell(klass.superclass)
    other_cells_width = superclass_cell.width + qualifiers_cell.width + \
        subclasses_cell.width + 12
    description_width = max([subtable_width - other_cells_width, 34])
    description_cell = build_description_cell(klass, description_width)
    class_row = [superclass_cell.data, subclasses_cell.data,
                 description_cell.data, qualifiers_cell.data]

    class_subtable = format_table([class_row], class_header,
                                  table_format=table_format,
                                  hide_empty_cols=True)

    # Build property subtable
    property_rows = []
    headers = ["Property\nName", "Type", "Default\nValue", "Description",
               "Class Origin", "Embedded Obj", "Qualifiers"]
    for property in klass.properties.values():
        qualifier_width = subtable_width - (8 + 50)
        qualifiers_cell = build_qualifiers_cell(
            property, qualifier_width, exclude=qualifier_exclude_list)

        type_and_array_cell = build_type_cell(property)

        class_origin_cell = TableCell(get_classorigin(property,
                                                      klass.classname))
        description_cell = build_description_cell(property, 50)

        row = [property.name, type_and_array_cell.data, property.value,
               description_cell.data, class_origin_cell.data,
               property.embedded_object, qualifiers_cell.data]
        property_rows.append(row)

    property_subtable = format_table(property_rows, headers,
                                     table_format=table_format,
                                     hide_empty_cols=True)

    # Build method subtable and parameter subtable for each method
    # Format methods and a subtable for parameters.
    method_rows = []
    headers = ["MethodName\nRtnType", "Class\nOrigin", "Description",
               "Qualifiers", "Parameters"]
    for method in klass.methods.values():
        method_name = "{}({})".format(method.name, method.return_type)
        name_cell = TableCell(method_name)

        method_qualifiers_cell = build_qualifiers_cell(
            method, 12, exclude=qualifier_exclude_list)

        class_origin_cell = TableCell(get_classorigin(method, klass.classname))
        description_cell = build_description_cell(method, 30)

        parameters_subtable_width = max(subtable_width - 80, 40)
        parameters_subtable = build_parameters_subtable(
            method.parameters.values(), parameters_subtable_width, table_format)



        row = [name_cell.data, class_origin_cell.data,
               description_cell.data,
               method_qualifiers_cell.data,
               parameters_subtable]

        method_rows.append(row)
    methods_subtable = format_table(method_rows, headers,
                                    table_format=table_format,
                                    hide_empty_cols=True)

    overall_rows = [[class_subtable], [property_subtable], [methods_subtable]]

    overall_headers = [klass.classname]
    table = format_table(overall_rows, overall_headers,
                         table_format=table_format,
                         hide_empty_cols=True)
    return table


# TODO: We are inconsistent with context as optional or required
def _display_classes_as_table(classes, table_width, table_format, context=None):
    """
    Display one or more CIM class objects as a table.
    """
    # pylint: disable=unused-argument
    for klass in classes:
        class_table = _build_class_as_table(klass,
                                            table_width,
                                            table_format,
                                            context)
        click.echo(class_table)


def _display_paths_as_table(objects, table_width, table_format):
    # pylint: disable=unused-argument
    """
    Display paths as a table. This include CIMInstanceName, ClassPath,
    and unicode (the return type for enumerateClasses).
    """
    title = None
    if objects:
        if isinstance(objects[0], six.string_types):
            title = 'Classnames:'
            headers = ['Class Name']
            rows = [[obj] for obj in objects]
        elif isinstance(objects[0], CIMClassName):
            title = 'Classnames'
            headers = ('host', 'namespace', 'class')
            rows = [[obj.host, obj.namespace, obj.classname] for obj in objects]
        elif isinstance(objects[0], CIMInstanceName):
            title = 'InstanceNames: {}'.format(objects[0].classname)
            host_hdr = 'host'
            ns_hdr = 'namespace'
            class_hdr = 'class'
            host_hdr_len = len(host_hdr) + 4
            ns_hdr_len = len(ns_hdr) + 3
            class_hdr_len = len(class_hdr) + 3
            headers = (host_hdr, ns_hdr, class_hdr, 'keysbindings')

            host_lens = [len(obj.host) for obj in objects if obj.host]
            host_max = max(host_lens) if host_lens else host_hdr_len
            ns_lens = [len(obj.namespace) for obj in objects if obj.namespace]
            ns_max = max(ns_lens) if ns_lens else ns_hdr_len
            class_lens = [len(obj.classname) for obj in objects]
            class_max = max(class_lens) if class_lens else class_hdr_len

            max_key_len = (table_width) - (host_max + ns_max + class_max + 3)
            rows = [[obj.host, obj.namespace, obj.classname,
                     format_keys(obj, max_key_len)] for obj in objects]
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
        if sum([len(i) for i in flavors]) >= max_column_width:
            sep = "\n"
        else:
            sep = ", "
        flavors = sep.join(flavors)

        row = [q.name, q.type, q.value, q.is_array, scopes, flavors]
        rows.append(row)

    click.echo(format_table(rows, headers, title='Qualifier Declarations',
                            table_format=table_format))


def _format_instances_as_rows(insts, max_cell_width=DEFAULT_MAX_CELL_WIDTH,
                              include_classes=False, context=None,
                              prop_names=None):
    """
    Format the list of instances properties into as a list of the property
    values for each instance( a row of the table) gathered into a list of
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
    # Avoid crash deeper in code if max_cell_width is None.
    if max_cell_width is None:
        max_cell_width = DEFAULT_MAX_CELL_WIDTH
    lines = []

    if prop_names is None:
        prop_names = sorted_prop_names(insts)

    # Cache of ValueMapping objects for integer-typed properties.
    # Key: classname.propertyname, both in lower case.
    # A value of None indicates the property does not have a value mapping.
    valuemappings = {}

    for inst in insts:
        if not isinstance(inst, CIMInstance):
            raise ValueError('Only accepts CIMInstance; not type {}'
                             .format(type(inst)))

        # Insert classname as first col if flag set
        line = [inst.classname] if include_classes else []

        # get value for each property in this object
        for name in prop_names:

            # Account for possible instances without all properties
            # Outputs empty  string.  Note that instance with no value
            # results in same output as not instance name.
            if name not in inst.properties:
                val_str = ''
            else:
                value = inst.get(name)
                p = inst.properties[name]

                # Cache value mappings for integer-typed properties
                if INT_TYPE_PATTERN.match(p.type) and context:
                    vm_key = '{}.{}'.format(
                        inst.classname.lower(), name.lower())
                    try:
                        valuemapping = valuemappings[vm_key]
                    except KeyError:
                        try:
                            valuemapping = ValueMapping.for_property(
                                context.conn,
                                context.conn.default_namespace,
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
                        p.value, p.type, indent=0, maxline=max_cell_width,
                        line_pos=0, end_space=0, avoid_splits=False,
                        valuemapping=valuemapping)

            line.append(val_str)
        lines.append(line)

    return lines


def _display_instances_as_table(insts, table_width, table_format,
                                include_classes=False, context=None):
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

    if table_width is None:
        table_width = DEFAULT_TABLE_WIDTH

    for inst in insts:
        assert isinstance(inst, CIMInstance)

    prop_names = sorted_prop_names(insts)

    # Try to estimate max cell width from number of cols
    # This allows folding long data.  However it is incomplete in
    # that we do not fold the property name.  Further, the actual output
    # width of a column involves the tabulate outputter, output_format
    # so this is not deterministic.
    if prop_names:
        num_cols = len(prop_names)
        max_cell_width = int(table_width / num_cols) - 2
    else:
        max_cell_width = table_width

    # TODO: Decide whether and how the showing of units should be controlled.
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
                # that case.
                # TODO: Pass a namespace for query execution to display units
                show_units = False
                break
            namespace = inst.path.namespace
            try:
                class_obj = context.conn.GetClass(
                    classname, namespace=namespace,
                    IncludeQualifiers=True, LocalOnly=False)
            except CIMError as exc:
                if exc.status_code == CIM_ERR_NOT_SUPPORTED:
                    # The WBEM Server does not support class operations. We
                    # silently give up showing units in this case.
                    show_units = False
                    break
            class_objs[classname] = class_obj

    # Construct the header line
    header_line = []  # list of header strings
    if include_classes:
        header_line.append("classname")
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
        header_line.append(hdr)

    # Fold long property names
    new_header_line = []
    for header in header_line:
        if len(header) > max_cell_width:
            new_header_line.append(fold_strings(header, max_cell_width))
        else:
            new_header_line.append(header)

    rows = _format_instances_as_rows(insts, max_cell_width=max_cell_width,
                                     include_classes=include_classes,
                                     context=context, prop_names=prop_names)

    title = 'Instances: {}'.format(insts[0].classname)
    click.echo(format_table(rows, new_header_line, title=title,
                            table_format=table_format))


def sorted_prop_names(insts):
    """
    Return the list of (originally cased) property names that is the superset
    of all properties in the input instances.

    The returned list has the key properties first, followed by the non-key
    properties. Each group is sorted case insensitively.

    The key properties are determined from the instance paths, if present.
    The function tolerates it if only some of the instances have a path,
    and if instances of subclasses have additional keys.
    """

    all_props = odicti()  # key: org prop name, value: lower cased prop name
    key_props = odicti()  # key: org prop name, value: lower cased prop name
    for inst in insts:
        inst_props = inst.keys()
        for pn in inst_props:
            all_props[pn] = pn.lower()
        if inst.path:
            key_prop_names = inst.path.keys()
            for pn in inst_props:
                if pn in key_prop_names:
                    key_props[pn] = pn.lower()

    nonkey_props = odicti()  # key: org prop name, value: lower cased prop name
    for pn in all_props:
        if pn not in key_props:
            nonkey_props[pn] = all_props[pn]

    key_prop_list = sorted(key_props.keys(), key=lambda p: p.lower())
    nonkey_prop_list = sorted(nonkey_props.keys(), key=lambda p: p.lower())
    key_prop_list.extend(nonkey_prop_list)
    return key_prop_list
