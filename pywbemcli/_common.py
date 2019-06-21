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
from operator import itemgetter
from prompt_toolkit import prompt
import six
import click
import tabulate

from pywbem import CIMInstanceName, CIMInstance, CIMClass, \
    CIMQualifierDeclaration, CIMProperty, CIMClassName, cimvalue, \
    CIM_ERR_METHOD_NOT_FOUND, CIMError, CIMFloat, CIMInt
from pywbem.cim_obj import mofstr
from pywbem.cim_obj import NocaseDict

from .config import USE_TERMINAL_WIDTH, DEFAULT_TABLE_WIDTH

# Same as in pywbem.cimobj.py
try:
    from builtins import type as builtin_type
except ImportError:  # py2
    from __builtin__ import type as builtin_type

# Same as in pwbem.cimtypes.py
if six.PY2:
    # pylint: disable=invalid-name,undefined-variable
    _Longint = long  # noqa: F821
else:
    # pylint: disable=invalid-name
    _Longint = int


TABLE_FORMATS = ['table', 'plain', 'simple', 'grid', 'rst']
CIM_OBJECT_OUTPUT_FORMATS = ['mof', 'xml', 'txt', 'tree']


# TODO: ks for some reason extending one list with another causes a problem
# in click with the help.
OUTPUT_FORMATS = ['table', 'plain', 'simple', 'grid', 'rst', 'mof', 'xml',
                  'txt', 'repr', 'tree']
GENERAL_OPTIONS_METAVAR = '[GENERAL-OPTIONS]'
CMD_OPTS_TXT = '[COMMAND-OPTIONS]'

DEFAULT_MAX_CELL_WIDTH = 100


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


def pywbemcli_prompt(msg):
    """
    This function isolates the prompt call so that it can be mocked for
    pywbemcli tests.
    """
    return prompt(msg)


def pick_from_list(context, options, title):
    """
    Interactive component that displays a set of options (strings) and asks
    the user to select one.  Returns the item and index of the selected string.

    Parameters:
      options:
        List of strings from which one will is to be selected

      title:
        Title to display before selection

    Retries until either integer within range of options list is input
    or user enter no value. Ctrl_C ends even the REPL.

    Returns: Selected item from options_list

    Exception: Returns ValueError if Ctrl-c input from console.

    TODO: Possible Future This could be replaced by the python pick library
    that would use curses for the selection process.
    """
    try:
        context.spinner.stop()

        click.echo(title)
        index = -1
        for str_ in options:
            index += 1
            click.echo('%s: %s' % (index, str_))
        selection = None
        msg = 'Input integer between 0 and %s or Ctrl-C to exit selection: ' \
            % index
        while True:
            try:
                selection_txt = pywbemcli_prompt(msg)
                selection = int(selection_txt)
                if 0 <= selection <= index:
                    context.spinner.start()
                    return options[selection]
            except ValueError:  # This causes the retry of the request
                pass
            except KeyboardInterrupt:
                raise click.ClickException("Pick Aborted.")
            click.echo('"%s" Invalid response %s' % (selection_txt, msg))
    except Exception:
        raise click.ClickException('Selection exception %s. Command Aborted')


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
        return pick_from_list(context, instance_names,
                              'Pick Instance name to process')
    except Exception as ex:
        raise click.ClickException('Command Aborted. Exception %s' % ex)


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
    if wbemuri_str and wbemuri_str[0] != ":":
        if re.match(r"^[a-zA-Z0-9_]+\.", wbemuri_str):
            wbemuri_str = ':%s' % wbemuri_str

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

    new_inst = CIMInstance(cim_class.classname,
                           properties=properties,
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
        return None

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
    if context.output_format:
        output_format = context.output_format
    else:
        output_format = 'mof'

    if objects:
        cim_type = get_cimtype(objects)

        if output_format_is_table(output_format):
            rows = [[len(objects), cim_type]]
            click.echo(format_table(rows, ['Count', 'CIM Type'],
                                    title='Summary of %s returned' % cim_type,
                                    table_format=output_format))
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
    output_format = context.output_format or 'mof'

    if isinstance(objects, (list, tuple)):
        # Table format output is processed as a group
        if output_format in TABLE_FORMATS:
            _print_objects_as_table(context, objects)
        else:
            # Recursively call to display each object
            for obj in objects:
                display_cim_objects(context, obj,
                                    output_format=context.output_format)
        return

    # Display a single item.
    object_ = objects
    # This allows passing single objects to the table formatter (i.e. not lists)
    if output_format in TABLE_FORMATS:
        _print_objects_as_table(context, [object_])
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
    elif output_format == 'repr':
        try:
            click.echo(repr(object_))
        except AttributeError:
            raise click.ClickException('"repr" display of %r failed' % object_)
    elif output_format == 'txt':
        try:
            click.echo(object_)
        except AttributeError:
            raise click.ClickException('"txt" display of %r failed' % object_)
    elif output_format == 'tree':
        raise click.ClickException('Tree output format not allowed')
    else:
        raise click.ClickException('Invalid output format %s' %
                                   output_format)


#######################################################################
#
#  The following code formats and outputs CIM Objects in table format
#
#######################################################################
def _print_classes_as_table(classes, table_width, table_format):
    """
    TODO: Future extend to display classes as a table, showing the
    properties for each class. This will display the properties that exist in
    subclasses. The temp output
    so we could create the function is to just output as mof
    """
    # pylint: disable=unused-argument

    for class_ in classes:
        click.echo(class_.tomof())


def _print_paths_as_table(objects, table_width, table_format):
    # pylint: disable=unused-argument
    """
    Display paths as a table. This include CIMInstanceName, ClassPath,
    and unicode (the return type for enumerateClasses).
    """
    cim_type = get_cimtype(objects)
    if objects:
        if isinstance(cim_type, six.stringtypes):
            headers = ['path']
            rows = [obj for obj in objects]
        elif isinstance(cim_type, CIMClass, CIMInstanceName):
            headers = ['host', 'namespace', 'keybindings']
            rows = [[obj.host, obj.namespace, obj.keybindings]
                    for obj in objects]
        else:
            raise click.ClickException("{0} invalid type ({1})for path display".
                                       format(objects[0], cim_type))

    title = '{} paths'.format(cim_type)
    click.echo(format_table(rows, headers, title=title,
                            table_format=table_format))


def _print_qual_decls_as_table(qual_decls, table_width, table_format):
    """
    Display the elements of qualifier declarations as a table with a
    row for each qualifier declaration and a column for each of the attributes
    of the qualifier declaration (name, type, Value, Array, Scopes, Flavors.

    The function displays all of the qualifier declarations in the
    """
    rows = []
    headers = ['Name', 'Type', 'Value', 'Array', 'Scopes', 'Flavors']
    max_column_width = (table_width / len(headers)) - 4
    for q in qual_decls:
        scopes = '\n'.join([key for key in q.scopes if q.scopes[key]])
        flavors = []
        flavors.append('EnableOverride' if q.overridable else 'DisableOverride')
        # flavors = q.overridable and 'EnableOverride' or 'DisableOverride'
        # flavors += ','
        flavors.append('ToSubclass' if q.tosubclass else 'Restricted')
        if q.translatable:
            flavors.append('Translatable')
        if sum([len(i) for i in flavors]) > max_column_width:
            sep = "\n"
        else:
            sep = ", "
        flavors = sep.join(flavors)

        row = [q.name, q.type, q.value, q.is_array, scopes, flavors]
        rows.append(row)

    click.echo(format_table(rows, headers, title='Qualifier Declarations',
                            table_format=table_format))


def _format_instances_as_rows(insts, max_cell_width=DEFAULT_MAX_CELL_WIDTH,
                              include_classes=False):
    """
    Format the list of instances properties into as a list of the property
    values for each instance( a row of the table) gathered into a list of
    the rows.

    Include_classes for each instance if True. Sets the classname as the first
    column.

    max_width if not None folds col entries longer than the defined
    max_cell_width. If max_width is None, the data length is ignored.

    Formatting is consistent with mof output for each value.

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
    prop_names = []

    # find instance with max number of properties
    for inst in insts:
        pn = inst.keys()
        if len(pn) > len(prop_names):
            prop_names = pn

    for inst in insts:
        if not isinstance(inst, CIMInstance):
            raise ValueError('Only  Accepts CIMInstance. not type %s' %
                             type(inst))

        # Insert classname as first col if flag set
        line = [inst.classname] if include_classes else []

        # get value for each property in this object
        for name in prop_names:
            # Account for possible instances without all properties
            if name not in inst.properties:
                val_str = ''
            else:
                value = inst.get(name)
                p = inst.properties[name]
                if value is None:
                    val_str = u''
                else:
                    val_str, _ = _value_tomof(p.value, p.type, indent=0,
                                              maxline=max_cell_width,
                                              line_pos=0, end_space=0,
                                              avoid_splits=False)
            line.append(val_str)
        lines.append(line)

    return lines


def _print_instances_as_table(insts, table_width, table_format,
                              include_classes=False):
    """
    Print the properties of the instances defined in insts as a table where
    each row is an instance and each column is a property value.  The properties
    are formatted similar to mof output. All properties in the instance are
    included.

    The header line consists of property names.
    """

    if table_width is None:
        table_width = DEFAULT_TABLE_WIDTH

    # Find instance with max number of prop names to determine number
    # of columns
    prop_names = []
    for inst in insts:
        pn = inst.keys()
        if len(pn) > len(prop_names):
            prop_names = pn

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

    header_line = []
    if include_classes:
        header_line.append("classname")
    header_line.extend(prop_names)

    # Fold long property names
    new_header_line = []
    for header in header_line:
        if len(header) > max_cell_width:
            new_header_line.append(fold_string(header, max_cell_width))
        else:
            new_header_line.append(header)

    title = insts[0].classname

    for inst in insts:
        if not isinstance(inst, CIMInstance):
            raise ValueError('Only CIMInstance display allows table output')

    lines = _format_instances_as_rows(insts, max_cell_width=max_cell_width,
                                      include_classes=include_classes)

    click.echo(format_table(lines, new_header_line, title=title,
                            table_format=table_format))


def _print_objects_as_table(context, objects):
    """
    Call the method for each type of object to print that object type
    information as a table.

    Output format is retrieved from context.
    """
    if USE_TERMINAL_WIDTH:
        table_width = click.get_terminal_size()[0]
    else:
        table_width = DEFAULT_TABLE_WIDTH

    output_format = context.output_format
    if isinstance(objects[0], CIMInstance):
        _print_instances_as_table(objects, table_width, output_format)
    elif isinstance(objects[0], CIMClass):
        _print_classes_as_table(objects, table_width, output_format)
    elif isinstance(objects[0], CIMQualifierDeclaration):
        _print_qual_decls_as_table(objects, table_width, output_format)
    elif isinstance(objects[0], (CIMClassName, CIMInstanceName,
                                 six.string_types)):
        _print_paths_as_table(objects, table_width, output_format)
    else:
        raise click.ClickException("Cannot print %s as table" %
                                   type(objects[0]))


def _indent_str(indent):
    """
    Return a MOF indent pad unicode string from the indent integer variable
    that defines number of spaces to indent. Used to format MOF output.
    """
    return u''.ljust(indent, u' ')


def mofval(value, indent=0, maxline=DEFAULT_MAX_CELL_WIDTH, line_pos=0,
           end_space=0):
    """
    Low level function that returns the MOF representation of a non-string
    value (i.e. a value that cannot not be split into multiple parts, for
    example a numeric or boolean value).

    If the MOF representation of the value does not fit into the remaining
    space of the current line, it is put into a new line, considering the
    specified indentation.

    NOTE: This method is derived from pywbem mofval but differs in that we
    want to output even if we violate the maxline limit on the new line. This
    method favors outputing data over exceptions.

    Parameters:

      value (:term:`unicode string`): The non-string value. Must not be `None`.

      indent (:term:`integer`): Number of spaces to indent any new lines that
        are generated.

      maxline (:term:`integer`): Maximum line length for the generated MOF.

      line_pos (:term:`integer`): Length of content already on the current
        line.

      end_space (:term:`integer`): Length of space to be left free on the last
        line.

    Returns:

      tuple of
        * :term:`unicode string`: MOF string.
        * new line_pos
    """

    assert isinstance(value, six.text_type)

    # Check for output on current line
    # if fits or this is first entry on the line
    avl_len = maxline - line_pos - end_space
    if len(value) <= avl_len or line_pos == 0:
        line_pos += len(value)
        return value, line_pos

    mof_str = u'\n' + _indent_str(indent) + value
    line_pos = indent + len(value)
    return mof_str, line_pos


def _scalar_value_tomof(value, type, indent=0, maxline=DEFAULT_MAX_CELL_WIDTH,
                        line_pos=0, end_space=0, avoid_splits=False):
    # pylint: disable=line-too-long,redefined-builtin
    """
    Return a MOF string representing a scalar CIM-typed value.

    `None` is returned as 'NULL'.

    NOTE: This code taken from pywbem 0.14.0

    Parameters:

      value (:term:`CIM data type`, :term:`number`, :class:`~pywbem.CIMInstance`, :class:`~pywbem.CIMClass`):
        The scalar CIM-typed value. May be `None`.

        Must not be an array/list/tuple. Must not be a :ref:`CIM object` other
        than those listed.

      type (string): CIM data type name.

      indent (:term:`integer`): Number of spaces to indent any new lines that
        are generated.

      maxline (:term:`integer`): Maximum line length for the generated MOF.

      line_pos (:term:`integer`): Length of content already on the current
        line.

      end_space (:term:`integer`): Length of space to be left free on the last
        line.

      avoid_splits (bool): Avoid splits at the price of starting a new line
        instead of using the current line.

    Returns:

      tuple of
        * :term:`unicode string`: MOF string.
        * new line_pos
    """  # noqa: E501

    if value is None:
        return mofval(u'NULL', indent, maxline, line_pos, end_space)

    if type == 'string':  # pylint: disable=no-else-raise
        if isinstance(value, six.string_types):
            return mofstr(value, indent, maxline, line_pos, end_space,
                          avoid_splits)

        if isinstance(value, (CIMInstance, CIMClass)):
            # embedded instance or class
            return mofstr(value.tomof(), indent, maxline, line_pos, end_space,
                          avoid_splits)
        raise TypeError("Scalar value of CIM type {0} has invalid Python type "
                        "type {1} for conversion to a MOF string".format
                        (type, builtin_type(value)))

        # TODO Integrate _format into pywbemcli
        #  _format("Scalar value of CIM type {0} has invalid Python type "
        #        "type {1} for conversion to a MOF string",
        #        type, builtin_type(value)))

    elif type == 'char16':
        return mofstr(value, indent, maxline, line_pos, end_space, avoid_splits,
                      quote_char=u"'")
    elif type == 'boolean':
        val = u'true' if value else u'false'
        return mofval(val, indent, maxline, line_pos, end_space)
    elif type == 'datetime':
        val = six.text_type(value)
        return mofstr(val, indent, maxline, line_pos, end_space, avoid_splits)
    elif type == 'reference':
        val = value.to_wbem_uri()
        return mofstr(val, indent, maxline, line_pos, end_space, avoid_splits)
    elif isinstance(value, (CIMFloat, CIMInt, int, _Longint)):
        val = six.text_type(value)
        return mofval(val, indent, maxline, line_pos, end_space)
    else:
        assert isinstance(value, float), \
            "Scalar value of CIM type {0} has invalid Python type {1} " \
            "for conversion to a MOF string".format(type, builtin_type(value))
        val = repr(value)
        return mofval(val, indent, maxline, line_pos, end_space)


def _value_tomof(value, type, indent=0, maxline=DEFAULT_MAX_CELL_WIDTH,
                 line_pos=0, end_space=0, avoid_splits=False):
    # pylint: disable=redefined-builtin
    """
    Return a MOF string representing a CIM-typed value (scalar or array).

    In case of an array, the array items are separated by comma, but the
    surrounding curly braces are not added.

    Parameters:

      value (CIM-typed value or list of CIM-typed values): The value.

      indent (:term:`integer`): Number of spaces to indent any new lines that
        are generated.

      maxline (:term:`integer`): Maximum line length for the generated MOF.

      line_pos (:term:`integer`): Length of content already on the current
        line.

      end_space (:term:`integer`): Length of space to be left free on the last
        line.

      avoid_splits (bool): Avoid splits at the price of starting a new line
        instead of using the current line.

    Returns:

      tuple of
        * :term:`unicode string`: MOF string.
        * new line_pos
    """

    if isinstance(value, list):

        mof = []

        for i, v in enumerate(value):

            if i > 0:
                # Assume we would add comma and space as separator
                line_pos += 2

            val_str, line_pos = _scalar_value_tomof(
                v, type, indent, maxline, line_pos, end_space + 2, avoid_splits)

            if i > 0:
                # Add the actual separator
                mof.append(u',')
                if val_str[0] != '\n':
                    mof.append(u' ')
                else:
                    # Adjust by the space we did not need
                    line_pos -= 1

            mof.append(val_str)

        mof_str = u''.join(mof)

    else:
        mof_str, line_pos = _scalar_value_tomof(
            value, type, indent, maxline, line_pos, end_space, avoid_splits)

    return mof_str, line_pos


def format_table(rows, headers, title=None, table_format='simple',
                 sort_columns=None):
    """
    General print table function.  Prints a list of lists in a
    table format where each inner list is a row.
    This code is temporary while the tabulate package is updated

      Parameters:
          headers (list strings) where each string is a
           table column name or None if no header is to be attached

          table_data - list of lists where:
             each the top level iterables represents the list of rows
             and each row is an iterable of strings for the data in that
             row.

          title (:term: `string`):
             Optional title to be places io the output above the table.
             No title is output if this parameter is None

          table_format (:term: 'string'):
            Output format defined by the string and limited to one of the
            choice of table formats defined in TABLE_FORMATS list

          output_file (:term: 'string'):
            If not None, a file name to which the output formatted data
            is sent.

          sort_columns (int or list of int that defines sort):
            Defines the cols that will be sorted. If int, it defines the column
            that will be sorted. If list of int, the sort is in sort order of
            cols in the list (i.e. minor sorts to the left, major sorts to the
            right). Note that entries in each row of the columns to be sorted
            must be of the same type (int, str, etc.) to be sortable.

      Returns: (:term:`string`)
        Returns the formatted table as a string

      Exceptions:
        Raises click.ClickException if invalid table format string
    """
    if sort_columns is not None:
        if isinstance(sort_columns, int):
            rows = sorted(rows, key=itemgetter(sort_columns))
        elif isinstance(sort_columns, (list, tuple)):
            rows = sorted(rows, key=itemgetter(*sort_columns))
        else:
            assert False, "Sort_columns must be int or list/tuple of int"

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
