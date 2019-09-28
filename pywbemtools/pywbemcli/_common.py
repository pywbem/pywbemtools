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

import fnmatch
import re
from textwrap import fill
from operator import itemgetter
import six
import click
import tabulate

from pywbem import CIMInstanceName, CIMInstance, CIMClass, \
    CIMQualifierDeclaration, CIMProperty, CIMClassName, \
    cimvalue, CIMFloat, CIMInt
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


TABLE_FORMATS = ('table', 'plain', 'simple', 'grid', 'psql', 'rst', 'html')
CIM_OBJECT_OUTPUT_FORMATS = ('mof', 'xml', 'repr', 'txt')

OUTPUT_FORMATS = [TABLE_FORMATS, CIM_OBJECT_OUTPUT_FORMATS]

GENERAL_OPTIONS_METAVAR = '[GENERAL-OPTIONS]'
CMD_OPTS_TXT = '[COMMAND-OPTIONS]'

DEFAULT_MAX_CELL_WIDTH = 100


def output_format_is_table(output_format):
    """ Return True if output format is a table form"""
    return output_format in TABLE_FORMATS


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
    if len(propertylist) == 1 and not propertylist[0]:
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


def warning_msg(msg):
    """Issue the msg param as warning prefixed by WARNING:"""
    click.echo('WARNING: %s' % msg)


def pick_one_from_list(context, options, title):
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
    if context:
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
            selection_txt = click.prompt(msg)
            selection = int(selection_txt)
            if 0 <= selection <= index:
                if context:
                    context.spinner.start()
                return options[selection]
        except ValueError:  # This causes the retry of the request
            pass
        except KeyboardInterrupt:
            raise click.ClickException("Pick Aborted. CTRL-C")
        except Exception as ex:
            raise click.ClickException(
                'Selection exception: %s. Command Aborted' % ex)
        click.echo('"%s" Invalid response %s' % (selection_txt, msg))


def pick_instance(context, objectname, namespace=None):
    """
    Display list of instances names from provided classname to console and user
    selects one. Returns the selected instancename.

      Parameters:
        context:
            Current click context or None

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
        return pick_one_from_list(context, instance_names,
                                  'Pick Instance name to process')
    except Exception as ex:
        raise click.ClickException('Command Aborted. Exception %s' % ex)


def pick_multiple_from_list(context, options, title):
    """
    Interactive component that displays a set of options (strings) and asks
    the user to select multiple entries from that list.  Returns a list of
    the items selected.

    Parameters:
      context:
        If not None, the ContextObj which is used to stop and start the
        spinner.
      options:
        List of strings to select

      title:
        Title to display before selection

    Retries until either integer within range of options list is input
    or user enter no value. Ctrl_C ends even the REPL.

    Returns: list of index of selected items

    Exception: Returns ValueError if Ctrl-c input from console.

    TODO: This could be replaced by the python pick library that would use
    curses for the selection process.
    """
    if context:
        context.spinner.stop()

    click.echo(title)
    index = -1
    for str_ in options:
        index += 1
        click.echo('%s: %s' % (index, str_))
    selection = None
    selection_list = []
    msg = 'Select entry by index or hit enter to end selection>'
    while True:
        try:
            selection_txt = click.prompt(msg)
            if not selection_txt:
                if context:
                    context.spinner.start()
                return selection_list

            selection = int(selection_txt)
            if 0 <= selection <= index:
                selection_list.append(options[selection])
            continue
        except ValueError:
            pass
        except KeyboardInterrupt:
            raise ValueError
        click.echo('%s Invalid. Input integer between 0 and %s hit enter to '
                   'stop selection.' % (selection, index))


def is_classname(str_):
    """
    Test if the str_ input is a classname or contains instance name
    components.  The existence of a period at the end of the name component
    determines if it is a classname or instance name.

    Returns:
        True if classname. Otherwise it returns False
    """
    assert isinstance(str_, six.string_types)
    return not re.match(r'[a-zA_Z0-9_].*\.', str_)


def filter_namelist(pattern, name_list, ignore_case=True):
    """
    Filter out names in name_list that do not match glob pattern compiled
    as regex.

    The regex is defined as IGNORECASE and anchored.

    Note that the regex may define a subset of the name string.  Thus,  regex:
        - CIM* matches any name that starts with CIM
        - CIM_abc* matches any name that starts with CIM_abc
        - CIM_ABC matches only the name CIM_ABC.
        - *ABC matches any name that includes ABC

    Parameters:
      pattern (:term: `String`) Python glob pattern to match.

      name_list: List of strings to be matched.

      ignore_case: bool. If True, do case-insensitive match. Default = True

    Returns:
     List of names that match.

    Raises:
        click.ClickException for regex compile error
    """

    flags = re.IGNORECASE if ignore_case else None
    # compile the regex since it used multiple times
    regex = None
    try:
        # Convert the glob input to regex.
        regex = fnmatch.translate(pattern)
        compiled_regex = re.compile(regex, flags)

    except Exception as ex:
        raise click.ClickException('Regex compile error. '
                                   'Regex=%s. Er: %s: %s' %
                                   (regex, ex.__class__.__name__, ex))

    new_list = [n for n in name_list for m in[compiled_regex.match(n)] if m]

    return new_list


def verify_operation(txt, msg=None):
    """
    Issue click confirm request and return result.  If msg is none and
    confirm response is n, output msg.

      Parameters
        txt(:term:`string`):
        String that is prefixed to the prompt text.

      msg (:class:`py:bool`)
        Optional parameter that if True causes an abort msg on the console.

      Returns:
        (:class:`py:bool`) where true corresponds to 'y' prompt response
    """
    if click.confirm(txt):
        return True
    if msg:
        click.echo('Request aborted')
    return False


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

        if isinstance(value, six.string_types):
            if value.lower() == 'true':
                return True
            if value.lower() == 'false':
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
        if inst1.properties == inst2.properties:
            return True
        if len(inst1.properties) != len(inst2.properties):
            click.echo('Different number of properties %s vs %s\n%s\n%s' %
                       (len(inst1.properties), len(inst2.properties),
                        inst1.keys(), inst2.keys()))
            return False
        keys1 = set(inst1.keys())
        keys2 = set(inst2.keys())
        if keys1 != keys2:
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
    and value components. Assumes that the key component does not
    include = which is valid for CIM names.

    If the value component is empty, returns value None
    """
    name, value = pair.partition("=")[::2]

    # if value has nothing in it, return None.
    if not value:
        value = None

    return name, value


def split_array_value(string, delimiter):
    """Simple split of a string based on a delimiter"""

    rslt = [item for item in split_str_w_esc(string, delimiter)]
    return rslt


def split_str_w_esc(str_, delimiter, escape='\\'):
    """
    Split string based on delimiter defined in call and the escape character \\
    To escape use of the delimiter in the strings. Delimiter may be multi
    character.
    Returns list of elements split from the input str
    """
    ret = []
    current_element = []
    iterator = iter(str_)
    for ch in iterator:
        if ch == escape:
            try:
                next_character = next(iterator)
                # Do not copy escape character if intended to escape either the
                # delimiter or the escape character itself. Copy the escape
                # character if it is not in use to escape one of these
                # characters.
                if next_character not in [delimiter, escape]:
                    current_element.append(escape)
                current_element.append(next_character)
            except StopIteration:
                current_element.append(escape)
        elif ch == delimiter:
            # split! (add current to the list and reset it)
            ret.append(''.join(current_element))
            current_element = []
        else:
            current_element.append(ch)
    ret.append(''.join(current_element))
    return ret


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

    def create_params(classname, cim_method, kv_params):
        """
        Create parameter values from the input arguments and class.

        Parameters:

          cim_method():
            CIM Method that is the template for the parameters.  It is used to
            evaluate the kv_params and generate corresponding CIMParameter
            objects to be passed to the InvokeMethod
        """
        params = []
        for p in kv_params:
            name, value_str = parse_kv_pair(p)
            if name not in cim_method.parameters:
                raise click.ClickException(
                    "Method {} of class {} does not have a parameter {}".
                    format(cim_method.name, classname, name))

            if name in params:
                raise click.ClickException(
                    "Method parameter {} specified multiple times".
                    format(name))

            cl_param = cim_method.parameters[name]
            is_array = cl_param.is_array

            cim_value = create_cimvalue(cl_param.type, value_str, is_array)
            params.append((name, cim_value))
        return params

    classname = objectname.classname \
        if isinstance(objectname, (CIMClassName, CIMInstanceName)) \
        else objectname

    cim_class = context.conn.GetClass(
        classname,
        namespace=options['namespace'], LocalOnly=False)

    cim_methods = cim_class.methods
    if methodname not in cim_methods:
        raise click.ClickException(
            "Class {} does not have a method {}".
            format(classname, methodname))
    cim_method = cim_methods[methodname]

    params = create_params(classname, cim_method, options['parameter'])

    rtn = context.conn.InvokeMethod(methodname, objectname, params)

    # Output results, both ReturnValue and all output parameters
    click.echo("ReturnValue=%s" % rtn[0])

    if rtn[1]:
        cl_params = cim_method.parameters
        rtn_params = rtn[1]
        for pname, pvalue in rtn_params.items():
            ptype = cl_params[pname].type if pname in cl_params else None
            val = _value_tomof(pvalue, ptype, maxline=DEFAULT_MAX_CELL_WIDTH,
                               avoid_splits=False)
            click.echo("%s=%s" % (pname, val[0]))


def sort_cimobjects(cim_objects):
    """
    Sort lists of CIMClass, CIMCLassName, CIMQualifierDecl, CIMInstance or
    CIMInstanceName. Sorts based on name or CIMInstancename. Sorting is based
    on the name value (name, classname, wbemuri(canonical form)
    Returns new list with the sorted objects.  This was defined as a common
    sort mechanism for all of the CIM object responses from WBEM servers.
    """
    if len(cim_objects) < 2:
        return cim_objects

    tst_obj = cim_objects[0]
    # this covers lists of classnames from class enum -o
    if isinstance(tst_obj, six.string_types):
        return sorted(cim_objects)

    if isinstance(tst_obj, CIMClass):
        return sorted(cim_objects, key=lambda class_: class_.classname)

    if isinstance(tst_obj, (CIMClassName, CIMInstanceName)):
        sort_dict = {obj.to_wbem_uri(format="canonical"): obj
                     for obj in cim_objects}
    elif isinstance(tst_obj, CIMInstance):
        sort_dict = {obj.path.to_wbem_uri(format="canonical"): obj
                     for obj in cim_objects}
    elif isinstance(tst_obj, CIMQualifierDeclaration):
        sort_dict = {obj.name: obj for obj in cim_objects}
    # Oddball case. In this case it is a tuple of CIMClassname,
    # CIMClass from class references/associators
    elif isinstance(tst_obj, tuple):
        assert isinstance(tst_obj[0], CIMClassName)
        assert isinstance(tst_obj[1], CIMClass)
        sort_dict = {tup[0].to_wbem_uri(format="canonical"): tup for tup in
                     cim_objects}
    else:
        raise TypeError('%s cannot be sorted' % type(cim_objects[0]))

    return [sort_dict[key] for key in sorted(sort_dict.keys())]


def display_cim_objects_summary(context, objects):
    """
    Display a summary of the objects received. This only displays the
    count.
    """
    context.spinner.stop()

    # default when displaying cim objects is mof
    output_format = context.output_format or 'mof'

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


def display_cim_objects(context, cim_objects, output_format=None, summary=False,
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
    """
    context.spinner.stop()

    if summary:
        display_cim_objects_summary(context, cim_objects)
        return

    if sort:
        cim_objects = sort_cimobjects(cim_objects)

    # default when displaying cim objects is mof
    output_format = context.output_format or 'mof'

    if isinstance(cim_objects, (list, tuple)):
        # Table format output is processed as a group
        if output_format in TABLE_FORMATS:
            _print_objects_as_table(context, cim_objects)
        else:
            # Recursively call to display each object
            for obj in cim_objects:
                display_cim_objects(context, obj,
                                    output_format=context.output_format)
        return

    # Display a single item.
    object_ = cim_objects
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
    # elif output_format == 'tree':
    #    raise click.ClickException('Tree output format not allowed')
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


def format_keys(obj, max_width):
    """
    Format the keys of a dictionary of keybindings as text for display. Formats
    multiple keybindings on each line within the max_width
    """
    def get_wbemurikeys(obj):
        """
        Create wbem_uri from CIMInstanceName and separate out key component
        for return.
        """
        wbem_uri = obj.to_wbem_uri()
        wbem_uri_keys = wbem_uri[wbem_uri.find('.'):]
        wbem_uri_keys = wbem_uri_keys[1:]
        return wbem_uri_keys

    assert isinstance(obj, CIMInstanceName)
    # clear the host and namespace
    myobj = obj.copy()
    myobj.host = None
    myobj.namespace = None
    wbem_uri_keys = get_wbemurikeys(myobj)

    # Too long for width. Fold the keys on multiple lines
    if len(wbem_uri_keys) > max_width:
        wbem_uri_keys = ''
        line_len = 0
        for key, value in myobj.keybindings.items():
            one_key_obj = get_wbemurikeys((CIMInstanceName('x', {key: value})))
            if wbem_uri_keys:
                if line_len + len(one_key_obj) > max_width:
                    wbem_uri_keys += '\n%s' % one_key_obj
                    line_len = 0
                else:
                    wbem_uri_keys += ',%s' % one_key_obj
                    line_len += len(one_key_obj) + 1

            else:  # must put on first line even if too long
                wbem_uri_keys += one_key_obj
                line_len = len(one_key_obj) + 1

    return wbem_uri_keys


def _print_paths_as_table(objects, table_width, table_format):
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
            title = 'InstanceNames: %s' % objects[0].classname
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
            raise ValueError('Only accepts CIMInstance; not type %s' %
                             type(inst))

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

    for inst in insts:
        if not isinstance(inst, CIMInstance):
            raise ValueError('Only CIMInstance display allows table output')

    rows = _format_instances_as_rows(insts, max_cell_width=max_cell_width,
                                     include_classes=include_classes)

    title = 'Instances: %s' % insts[0].classname
    click.echo(format_table(rows, new_header_line, title=title,
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
    if objects:
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
                # Assume comma and space as separator
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


def hide_empty_columns(headers, rows):
    """
    Removes columns from rows if the colmuns are considered empty.
    The definiton of an empty row is:
    1. All entries for the column in all rows are None or "" if type string.
    2. All entries for the column in all rows are None if number.

    Returns new rows and headers
    """
    def column_is_empty(rows, column):
        """
        Determine if entries for defined column in all rows are considered
        empty.
        Returns True if all are empty. Otherwise returns False
        """
        for row in rows:
            if isinstance(row[column], six.integer_types) and \
                    row[column] is not None:
                return False
            if row[column]:
                return False
        return True

    # Remove empty rows
    for row in rows:
        assert len(row) == len(headers)
    for column in range(len(headers) - 1, -1, -1):
        if column_is_empty(rows, column):
            del headers[column]
            for row in rows:
                del row[column]

    return headers, rows


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
        table_format = 'table'
    if table_format == 'table':
        table_format = 'psql'
    if table_format not in TABLE_FORMATS:
        raise click.ClickException('Invalid table format %s.' % table_format)

    result = tabulate.tabulate(rows, headers, tablefmt=table_format)
    if title:
        if table_format == 'html':
            result = '<p>%s</p>\n%s' % (title, result)
        else:
            result = '{0}\n{1}'.format(title, result)
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
