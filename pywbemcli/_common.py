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
Common Functions applicable across multiple components of pywbemcli
"""

from __future__ import absolute_import, unicode_literals

import re
from textwrap import fill
from prompt_toolkit import prompt
import six
import click
import tabulate

from pywbem import CIMInstanceName, CIMInstance, CIMClass, \
    CIMQualifierDeclaration, CIMProperty, CIMClassName, cimvalue, \
    CIM_ERR_METHOD_NOT_FOUND, CIMError
from pywbem.cim_obj import mofstr
from pywbem.cim_obj import NocaseDict

TABLE_FORMATS = ['table', 'plain', 'simple', 'grid', 'rst']
CIM_OBJECT_OUTPUT_FORMATS = ['mof', 'xml', 'txt', 'tree']

# TODO: ks for some reason extending one list with another causes a problem
# in click with the help.
OUTPUT_FORMATS = ['table', 'plain', 'simple', 'grid', 'rst', 'mof', 'xml',
                  'txt', 'tree']
GENERAL_OPTIONS_METAVAR = '[GENERAL-OPTIONS]'
CMD_OPTS_TXT = '[COMMAND-OPTIONS]'


def output_format_is_table(output_format):
    """ Return True if output format is a table form"""
    return True if output_format in TABLE_FORMATS else False


def resolve_propertylist(propertylist):
    """
    Resolve property list received from click options.  Click options produces
    an empty list when there is no property list.

    Pywbem requires None when there is no propertylist

    Further, property lists can be input as a comma separated list so this
    function also splits any string with embedded commas.

    Parameters (list of :term:`string` or None):
        Each item in list may be a single property name or a collection of
        property names separated by commas.

    Returns:
        list of property names resulting from parsing input or empty list
        or None

    """
    # If no property list, return None which means all properties
    if not propertylist:
        return None

    # If propertylist is a single empty string, set to empty list.
    elif len(propertylist) == 1 and not propertylist[0]:
        propertylist = []

    # expand any comma separated entries in the list
    else:
        pl = []
        for item in propertylist:
            if ',' in item:
                pl.extend(item.split(','))
            else:
                pl.append(item)
        propertylist = pl

    return propertylist


def pick_instance(context, objectname, namespace=None):
    """
    Display list of instances names from provided classname to console and user
    selects one. Returns the selected instancename.

      Parameters:
        context:
            Current click context

        classname:
            Classname to use to get instance names from server

      Returns:
        instancename selected or None if there are no instances to pick
      Exception:
        ClickException if user choses to terminate the selection process
    """
    if not is_classname(objectname):
        raise click.ClickException('%s must be a classname' % objectname)
    instance_names = context.conn.PyWbemcliEnumerateInstancePaths(objectname,
                                                                  namespace)

    if not instance_names:
        click.echo('No instance paths found for %s' % objectname)
        return None

    try:
        index = pick_from_list(context, instance_names,
                               'Pick Instance name to process')
        return instance_names[index]
    except Exception:
        raise click.ClickException('Command Aborted')


def pick_from_list(context, options, title):
    """
    Interactive component that displays a set of options (strings) and asks
    the user to select one.  Returns the item and index of the selected string.

    Parameters:
      options:
        List of strings to select

      title:
        Title to display before selection

    Retries until either integer within range of options list is input
    or user enter no value. Ctrl_C ends even the REPL.

    Returns: Index of selected item

    Exception: Returns ValueError if Ctrl-c input from console.

    TODO: This could be replaced by the python pick library that would use
    curses for the selection process.
    """
    context.spinner.stop()

    click.echo(title)
    index = -1
    for str_ in options:
        index += 1
        click.echo('%s: %s' % (index, str_))
    selection = None
    msg = 'Input integer between 0 and %s or Ctrl-C to exit selection: ' % index
    while True:
        try:
            selection = int(prompt(msg))
            if selection >= 0 and selection <= index:
                return selection
        except ValueError:  # This causes the retry of the request
            pass
        except KeyboardInterrupt:
            raise click.ClickException("Pick Aborted.")
        click.echo('%s Invalid. %s' % (selection, msg))
    context.spinner.start()


def is_classname(str_):
    """
    Test if the str_ input is a classname or contains instance name
    components.  The existence of a period at the end of the name component

    Returns:
        True if classname. Otherwise it returns False
    """
    match = re.match(r'[a-zA_Z0-9_].*\.', str_)
    return False if match else True


def filter_namelist(regex, name_list, ignore_case=True):
    """
    Filter out names in name_list that do not match compiled_regex.

    The regex is defines as IGNORECASE and anchored.

    Note that the regex may define a subset of the name string.  Thus,  regex:
        - CIM matches any name that starts with CIM
        - CIM_abc matches any name that starts with CIM_abc
        - CIM_ABC$ matches only the name CIM_ABC.
        - .*ABC matches any name that includes ABC

    Parameters:
      regex (:term: `String`) Python regular expression to match.

      name_list: List of strings to be matched.

      ignore_case: bool. If True, do case-insensitive match. Default = True

    Returns:
     List of names that match.

    Raises:
        click.ClickException for regex compile error
    """

    flags = re.IGNORECASE if ignore_case else None
    try:
        cmpiled_regex = re.compile(regex, flags) if flags else re.compile(regex)
    except re.error as er:
        raise click.ClickException("Regex Compile Error: %s: %s" %
                                   (er.__class__.__name__, er))

    new_list = [n for n in name_list for m in[cmpiled_regex.match(n)] if m]

    return new_list


def verify_operation(txt, msg=None):
    """
    Issue prompt to verify the execution of the request and test the response
    for y or n.  Repeat until one of them is received.

      Parameters
        txt(:term:`string`):
        String that it prefixed to the prompt text.

      msg (:class:`py:bool`)
        Optional parameter that if True causes an abort msg on the console.

      Returns:
        (:class:`py:bool`) where true corresponds to 'y' prompt response
    """
    value = 'x'
    while value not in ('y', 'n'):
        value = click.prompt('%s Verify y/n ' % txt, default='n').lower()
    if value == 'y':
        if msg:
            click.echo('Request aborted')
        return True
    return False


def objects_sort(objects):
    """
    Sort CIMClasses, CIMQualifierDecls, CIMInstances or instance names.
    Returns new list with the sorted objects.
    """
    if len(objects) < 2:
        return objects
    if isinstance(objects[0], CIMClass):
        return sorted(objects, key=lambda class_: class_.classname)

    sort_dict = {}
    rtn_objs = []
    if isinstance(objects[0], CIMInstanceName):
        for instname in objects:
            key = "%s" % instname
            sort_dict[key] = instname
    elif isinstance(objects[0], CIMInstance):
        for inst in objects:
            key = "%s" % inst.path
            sort_dict[key] = inst
    elif isinstance(objects[0], CIMQualifierDeclaration):
        for qd in objects:
            key = "%s" % qd.name
            sort_dict[key] = qd
    else:
        raise TypeError('%s cannot be sorted' % type(objects[0]))

    for key in sorted(sort_dict):
        rtn_objs.append(sort_dict[key])
    return rtn_objs


def parse_wbemuri_str(wbemuri_str, namespace=None):
    """
    Parse a string that is a wbemuri into a CIMInstanceName object.  This method
    parses a string consistent with a wbemuri into a CIMInstanceName object.

    If the wbem_uri includes a namespace that is parsed also.  If both
    the namespace optional parameter exists and the wbemuri_str parameter
    includes a namespace (and they are not the same), an exception is returned.

    Returns:
        CIMInstanceName instance object

    Raises:
        ClickException: if the input wbemuri_str is an invalid wbemuri.

    """
    # TODO documented in issue #131
    # TODO remove this code when we resolve issue with pywbem issue #1359
    # Issue is that 0.13.0 does not allow the form classname.keybindings
    # without the : before the classname
    # print('PARSE_WBEMURI_STR1 %s' % wbemuri_str)
    if wbemuri_str and wbemuri_str[0] != ":":
        if re.match(r"^[a-zA-Z0-9_]+\.", wbemuri_str):
            wbemuri_str = ':%s' % wbemuri_str
    # print('PARSE_WBEMURI_STR2 %s' % wbemuri_str)

    try:
        instance_name = CIMInstanceName.from_wbem_uri(wbemuri_str)
        if instance_name.namespace and namespace:
            if instance_name.namespace != namespace:
                raise click.ClickException('Conflicting namespaces between '
                                           'wbemuri %s and option %s' %
                                           (instance_name.namespace, namespace))
        elif instance_name.namespace is None and namespace:
            instance_name.namespace = namespace

        return instance_name
    except ValueError as ve:
        raise click.ClickException('Invalid wbem uri input %s. Error %s' %
                                   (wbemuri_str, ve))


def create_params(cim_method, kv_params):
    """
    Create a parameter values from the input arguments and class.

    Parameters:

      cim_method():
        CIM Method that is the template for the parameters.  It is used to
        evaluate the kv_params and generate corresponding CIM_Parameter
        objects to be passed to the InvokeMethod
    """
    params = NocaseDict()
    for p in kv_params:
        name, value_str = parse_kv_pair(p)
        if name not in cim_method.parameters:
            raise click.ClickException('Parameter: %s not in method: '
                                       ' %s' % (name, cim_method.name))

        cl_param = cim_method.parameters[name]
        is_array = cl_param.is_array

        cim_value = create_cimvalue(cl_param.type, value_str, is_array)
        params = []
        params.append((name, cim_value))
    return params


def create_cimvalue(cim_type, value_str, is_array):
    """
    Build a cim value of the type in cim_type and the information in value_str
    or fail with an exception if the value_str cannot be parsed into a
    CIMValue or list of CIMValue elements.

    Parameters:
      cim_type: (:term: `string`)
        CIMType for this value. The CIM data type name for the CIM object.
        See :ref:`CIM data types` for valid type names.

      value_str (:term: `string`):
        String defining the input to be parsed.

      is_array (:class:`py:bool`):
        The value_str is to be treated as a comma separated set of values.

    Return:
        is_array == False. Returns a single CIMValue
        is_array == True. Returns a list of CIMValues

    Exceptions:
        ValueError if the value_str cannot be parsed consistent with
        the cim_type and is_array attributes of the call.
    """
    def str_2_bool(value):
        """
        Convert the value input to boolean based on text or
        raise ValueError if strings are not 'true' or 'false'.
        """
        if isinstance(value, bool):
            return value
        elif isinstance(value, six.string_types):
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
        raise ValueError('Invalid boolean value: "%s"' % value)

    cim_value = None

    if not is_array:
        # cimvalue does not handle strings for bool
        if cim_type == 'boolean':
            value_str = str_2_bool(value_str)
        cim_value = cimvalue(value_str, cim_type)
    else:
        cim_value = []
        values_list = split_array_value(value_str, ',')
        for val in values_list:
            if cim_type == 'boolean':
                val = str_2_bool(val)
            cim_value.append(cimvalue(val, cim_type))
    return cim_value


def create_cimproperty(cim_type, is_array, name, value_str):
    """
    Create and return a CIMProperty from the input parameters and the
    information in cim_class.

      Parameters:
        cim_class (:class:`~pywbem.CIMClass`)
          CIM Class that includes the property defined by name

        name (:term: `string`)
            Name of the property to be constructed

        value_str (:term: `string`)
            String form for the value to be inserted.

      Return:
        CIMProperty with name defined by name and CIMValue corresponding to
        value_str and property information from the class

      Exception:
        ValueError if value_str, cim_type and is_array mismatch.
    """
    cim_value = create_cimvalue(cim_type, value_str, is_array)

    return CIMProperty(name, cim_value, cim_type)


def create_ciminstance(cim_class, kv_properties, property_list=None):
    """
    Create a cim instance from the input parameters.

      Parameters:

        class_: (CIMClass)
            The class from which the CIMInstance is to be created

        properties ():
            A tuple of name/value pairs representing the properties and their
            values that are to be constructed for the instance. Required

        property_list ():
            a list of properties that is to be the list that is supplied
            when the instance is created. Optional

      Returns: CIMInstance

      Exceptions:
        click.ClickException if Property name not found in class or if mismatch
          of property type in class vs value component of kv pair
    """
    properties = NocaseDict()
    for kv_property in kv_properties:
        name, value_str = parse_kv_pair(kv_property)
        try:
            cl_prop = cim_class.properties[name]
        except KeyError:
            raise click.ClickException('Property name "%s" not in class "%s".'
                                       % (name, cim_class.classname))

        try:
            properties[name] = create_cimproperty(cl_prop.type,
                                                  cl_prop.is_array,
                                                  name,
                                                  value_str)
        except ValueError as ex:
            raise click.ClickException("Type mismatch property '%s' between "
                                       "expected type='%s', array=%s and input "
                                       "value='%s'. Exception: %s" %
                                       (name, cl_prop.type, cl_prop.is_array,
                                        value_str, ex))

    new_inst = CIMInstance(cim_class.classname, properties=properties,
                           property_list=property_list)

    return new_inst


def compare_obj(obj1, obj2, msg):
    """
    Compare two objects and display error if different.  Returns True if
    match or False if different
    """
    if obj1 != obj2:
        click.echo('Obj Compare %s: compare mismatch:\n%r\n%r' %
                   (msg, obj1, obj2))
        return False
    return True


def compare_instances(inst1, inst2):
    """
    Compare two instances. If they do not match, compare the details to
    find differnes and report the differences. Report the differences
    """
    if inst1 != inst2:
        if not compare_obj(inst1.classname, inst2.classname, "classname"):
            return False
        if not compare_obj(inst1.path, inst2.path, "path"):
            return False
        if not compare_obj(inst1.qualifiers, inst2.qualifiers, "qualifiers"):
            return False
        if len(inst1.properties) != len(inst2.properties):
            click.echo('Different number of properties %s vs %s' %
                       (len(inst1.properties, len(inst2.properties))))
            keys1 = set(inst1.keys())
            keys2 = set(inst2.keys())
            diff = keys1.symmetric_difference(keys2)
            click.echo('Property Name differences %s' % diff)
            return False
        for n1, v1 in six.iteritems(inst1):
            if v1 != inst2[n1]:
                msg = 'property ' + n1
                if not compare_obj(inst1.get(n1), inst2.get(n1), msg):
                    return False
    return True


def parse_kv_pair(pair):
    """
    Parse a single key/value pair separated by = and return the key
    and value components.

    If the value component is empty, returns None
    """
    name, value = pair.partition("=")[::2]

    # if value has nothing in it, return None.
    if not value:
        value = None

    return name, value


def split_array_value(string, delimiter):
    """Simple split of a string based on a delimiter"""

    rslt = [item for item in split_value_str(string, delimiter)]
    return rslt


def split_value_str(string, delimiter):
    """
    Split a string based on a delimiter character bypassing escaped
    instances of the delimiter.  This is a generator function in that
    it yields each time it separates a value.

    Delimiter must be single character.
    """
    if len(delimiter) != 1:
        raise ValueError('Invalid delimiter: ' + delimiter)
    ln = len(string)
    i = 0
    j = 0
    while j < ln:
        if string[j] == '\\':
            if j + 1 >= ln:
                yield string[i:j]
                return
            j += 1
        elif string[j] == delimiter:
            yield string[i:j]
            i = j + 1
        j += 1
    yield string[i:j]


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
        return

    if isinstance(test_object, tuple):
        # associator or reference class level return is tuple
        cim_type = test_object[1].__class__.__name__
    else:
        cim_type = test_object.__class__.__name__

    # account for fact the enumerate class name operation returns uniicode.
    if isinstance(test_object, six.string_types):
        cim_type = 'CIMClassName'
    return cim_type


def process_invokemethod(context, objectname, methodname, options):
    # pylint: disable=line-too-long
    """
    Process the parameters for invokemethod at either the class or instance
    level and execute the invokemethod.

    Parameters:

      objectname (:term:`string` or :class:`~pywbem.CIMInstanceName` or :class:`~pywbem.CIMInstanceName`)  # noqa: E501

      methodname (:term:`string`):
        The name of the method to be executed

    """  # pylint: enable=line-too-long

    classname = objectname.classname \
        if isinstance(objectname, (CIMClassName, CIMInstanceName)) \
        else objectname

    cim_class = context.conn.GetClass(
        classname,
        namespace=options['namespace'], LocalOnly=False)

    cim_methods = cim_class.methods
    if methodname not in cim_methods:
        # TODO: This really is a client error and probably should not use
        # CIMError
        raise CIMError(CIM_ERR_METHOD_NOT_FOUND, 'Method %s not in class %s '
                       'in server' % (methodname, classname))
    cim_method = cim_methods[methodname]

    params = create_params(cim_method, options['parameter'])

    rtn = context.conn.InvokeMethod(methodname, objectname, params)

    click.echo("ReturnValue=%s" % rtn[0])
    if rtn[1]:
        params = rtn[1]
        for param in params:
            click.echo("%s=%s" % (param, params[param]))


def display_cim_objects_summary(context, objects):
    """
    Display a summary of the objects received. This only displays the
    count.
    """
    context.spinner.stop()

    output_format = 'table' if context.output_format is 'None' else \
        context.output_format

    if objects:
        cim_type = get_cimtype(objects)

        if output_format_is_table(output_format):
            rows = [[len(objects), cim_type]]
            click.echo(format_table(rows, ['Count', 'CIM Type'],
                                    table_format=context.output_format,
                                    title='Summary of %s returned'))
            return
        click.echo('%s %s(s) returned' % (len(objects), cim_type))
    else:
        click.echo('0 objects returned')


def display_cim_objects(context, objects, output_format=None, summary=False):
    # pylint: disable=line-too-long
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

      TODO This is not correct form for this doc.
      objects(iterable of CIMInstance, CIMInstanceName, CIMClass, CIMClassName,
      or CIMQualifierDeclaration):
        Iterable of CIM objects to be displayed or a single object.

      output_format(:term:`strng`):
        String defining the preferred output format. This may be overridden
        if the output format cannot be used for the object type

      summary(:class:`py:bool`):
        Boolean that defines whether the data in objects should be displayed
        or just a summary of the objects (ex. count of number of objects).
    """    # noqa: E501
    # pylint: enable=line-too-long
    context.spinner.stop()

    if summary:
        display_cim_objects_summary(context, objects)
        return
    # default when displaying cim objects is mof
    if output_format is None:
        output_format = 'mof'

    if isinstance(objects, (list, tuple)):
        if output_format in TABLE_FORMATS:
            if isinstance(objects[0], CIMInstance):
                print_insts_as_table(context, objects)
            elif isinstance(objects[0], CIMClass):
                print_classes_as_table(context, objects)
            elif isinstance(objects[0], CIMQualifierDeclaration):
                print_qual_decls_as_table(context, objects)
            elif isinstance(objects[0], (CIMClassName, CIMInstanceName,
                                         six.string_types)):
                print_paths_as_table(context, objects)
            else:
                raise click.ClickException("Cannot print %s as table" %
                                           type(objects[0]))
        else:
            for obj in objects:
                display_cim_objects(context, obj, output_format=output_format)
        return

    # display a single item.
    object_ = objects
    if output_format in TABLE_FORMATS:
        if isinstance(object_, CIMInstance):
            print_insts_as_table(context, object_)
        elif isinstance(object_, CIMClass):
            print_classes_as_table(context, [object_])
        else:
            raise click.ClickException('No table formatter for %s' %
                                       type(object_))
    elif output_format == 'mof':
        try:
            click.echo(object_.tomof())
        except AttributeError:
            if isinstance(object_, (CIMInstanceName, CIMClassName,
                                    six.string_types)):
                click.echo(object_)
            else:
                raise click.ClickException('output_format %s invalid for %s '
                                           % (output_format, type(object_)))
    elif output_format == 'xml':
        try:
            click.echo(object_.tocimxmlstr(indent=4))
        except AttributeError:
            # no tocimxmlstr functionality
            raise click.ClickException('Output Format %s not supported. '
                                       'Default to\n%r' %
                                       (output_format, object_))
    elif output_format == 'txt':
        try:
            click.echo(object_)
        except AttributeError:
            raise click.ClickException('"xt" display of %r failed' % object_)
    elif output_format == 'tree':
        raise click.ClickException('Tree output format not allowed')
    else:
        raise click.ClickException('Invalid output format %s' %
                                   output_format)


def print_class_as_table(context, class_, max_cell_width=20):
    """
    TODO: Future add code here to display a class as a table.  The temp output
    so we could create the function is to just output as mof
    """
    click.echo(class_.tomof())


def print_classes_as_table(context, classes, max_cell_width=20):
    """
    TODO: Future extend to display classes as a table, showing the
    properties for each class. This will display the properties that exist in
    subclasses
    """
    # pylint: disable=unused-argument

    for class_ in classes:
        print_class_as_table(context, class_, max_cell_width=20)


def print_paths_as_table(context, objects, max_cell_width=20):
    """
    Display paths as a table. This include CIMInstanceName, ClassPath,
    and unicode (the return type for enumerateClasses).
    """
    headers = ['path']

    rows = [[obj] for obj in objects]

    title = '%s paths' % get_cimtype(objects)
    click.echo(format_table(rows, headers, title=title,
                            table_format=context.output_format))


def print_qual_decls_as_table(context, qual_decls, max_cell_width=20):
    """
    Display the elements of qualifier declarations as a table
    """
    rows = []
    headers = ['Name', 'Type', 'Value', 'Array', 'Scopes', 'Flavors']
    for q in qual_decls:
        scopes = '\n'.join([key for key in q.scopes if q.scopes[key]])
        # TODO this is messy code.  Should we use something like:
        flavors = 'EnableOverride' if q.overridable else 'DisableOverride'
        flavors = q.overridable and 'EnableOverride' or 'DisableOverride'
        flavors += '\n'
        flavors += q.tosubclass and 'ToSubclass' or 'Restricted'
        if q.translatable:
            flavors += '\nTranslatable'

        row = [q.name, q.type, q.value, q.is_array, scopes, flavors]
        rows.append(row)

    click.echo(format_table(rows, headers, title='Qualifier Declarations',
                            table_format=context.output_format))


# TODO: Future provide way to set up max table and cell width more logically
def print_insts_as_table(context, objects, include_classes=False,
                         max_cell_width=20):
    """
    If possible display the list of instances as a table.
    Currently this only works for instances where the table is a column
    per property.

    This cannot display properties with embedded instances. They are ignored

    include_classes if True sets the classname as the first column.

    max_width if not None folds col entries longer than the defined length.
    If max_width is None, the data length is ignored. The property names used
    as the col headers are ignored.
    """
    lines = []
    title = None
    prop_names = []

    # find instance with max number of properties
    for inst in objects:
        pn = inst.keys()
        if len(pn) > len(prop_names):
            prop_names = pn

    header_line = []
    if include_classes:
        header_line.append("classname")
    header_line.extend(prop_names)

    title = objects[0].classname

    for inst in objects:
        if not isinstance(inst, CIMInstance):
            raise ValueError('Only CIMInstance display allows table output')
        # Look for not allowed property types
        for name in prop_names:
            if name in inst.properties:
                p = inst.properties[name]
                if p.embedded_object:
                    raise ValueError('Cannot process embeddedObject property '
                                     ' %s' % name)

        line = [inst.classname] if include_classes else []
        # get value for each property in this object
        # TODO: account for possible non-existence of name
        for name in prop_names:
            # Account for possible instances without all properties
            if name not in inst.properties:
                val_str = '?no_name?'
            else:
                value = inst.get(name)
                p = inst.properties[name]
                if not value:
                    val_str = ''
                else:
                    if p.is_array:
                        val_str = _array_value(p.type, value)
                    else:
                        val_str = _scalar_value(p.type, value)
            if max_cell_width:
                if len(val_str) > max_cell_width:
                    val_str = fold_string(val_str, max_cell_width)
            line.append(val_str)
        lines.append(line)

    click.echo(format_table(lines, header_line, title=title,
                            table_format=context.output_format))


def _scalar_value(type_, value_, max_width=None):
    """
    Private function to map provided value to string for output.
    Used by :meth:`tomof`.

    Parameters:

      value_ (:term:`CIM data type`): Value to be mapped to string for MOF
        output.

      max_wdith (:term:`integer`): If not None causes any result string
      longer than the integer value of max_width to be folded.

    Return:
        The string value of value_ based on type_
    """

    if type_ == 'string':
        _str = mofstr(value_, indent=0)
    elif type_ == 'datetime':
        _str = '"%s"' % str(value_)
    else:
        _str = str(value_)
    if max_width:
        if len(str) > max_width:
            _str = fold_string(_str, max_width)
    return _str


# TODO We do not know how to handle the fold mechanism here
def _array_value(type_, value_, fold=False, max_cell_width=None):
    """
    Output array of values either on single line or one line per value.

    Parameters:

      fold (bool): If True, fold the output string for each entry.

    """
    def enum_value(type_, value_, sep, max_cell_width):
        """ Convert the array values and return resulting string"""
        str_ = ""
        for i, val_ in enumerate(value_):
            if i > 0:
                str_ += sep
            str_ += _scalar_value(type_, val_, max_width=max_cell_width)
        return str_

    sep = ', ' if not fold else ',\n'
    str_ = enum_value(type_, value_, sep, max_cell_width)

    return str_


def format_table(rows, headers, table_format='simple', title=None):
    """
    General print table function.  Prints a list of lists in a
    table format where each inner list is a row.
    This code is temporary while the tabulate package is updated
    to being  capable of supporting multiline cells.

      Parameters:
          headers (list strings) where each string is a
           table column name or None if no header is to be attached

          table_data - list of lists where:
             each the top level iterables represents the list of rows
             and each row is an iterable of strings for the data in that
             row.

          title (:term: `string`)
             Optional title to be places io the output above the table.
             No title is output if this parameter is None

          table_format (:term: 'string')
            Output format defined by the string and limited to one of the
            choice of table formats defined in TABLE_FORMATS list

          output_file (:term: 'string')
            If not None, a file name to which the output formatted data
            is sent.

      Returns: (:term:`string`)
        Returns the formatted table as a string

      Exceptions:
        Raises click.ClickException if invalid table format string
    """

    if table_format is None:
        table_format = 'simple'
    if table_format not in TABLE_FORMATS:
        raise click.ClickException('Invalid table format %s.' % table_format)

    result = tabulate.tabulate(rows, headers, tablefmt=table_format)

    if title:
        result = '%s\n%s' % (title, result)
    return result


def fold_string(input_string, max_width):
    """
    Fold a string within a maximum width.

      Parameters:

        input_string:
          The string of data to go into the cell
        max_width:
          Maximum width of cell.  Data is folded into multiple lines to
          fit into this width.

      Return:
          String representing the folded string
    """
    new_string = input_string
    if isinstance(input_string, six.string_types):
        if max_width < len(input_string):
            # use textwrap to fold the string
            new_string = fill(input_string, max_width)

    return new_string
