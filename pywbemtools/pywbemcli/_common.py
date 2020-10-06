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

from __future__ import absolute_import, print_function, unicode_literals

import fnmatch
import re
from textwrap import fill
from operator import itemgetter
from collections import namedtuple
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict  # pylint: disable=import-error

from pydicti import odicti
import six
import click
import tabulate

from pywbem import CIMInstanceName, CIMInstance, CIMClass, \
    CIMQualifierDeclaration, CIMProperty, CIMClassName, \
    cimvalue, ValueMapping

from .config import USE_TERMINAL_WIDTH, DEFAULT_TABLE_WIDTH

from ._cimvalueformatter import cimvalue_to_fmtd_string


# Definitions of the components of the help Usage line used
# by pywbemcli
GENERAL_OPTS_TXT = '[GENERAL-OPTIONS]'
CMD_OPTS_TXT = '[COMMAND-OPTIONS]'
SUBCMD_HELP_TXT = "COMMAND [ARGS] " + CMD_OPTS_TXT

DEFAULT_MAX_CELL_WIDTH = 100

INT_TYPE_PATTERN = re.compile(r'^[su]int(8|16|32|64)$')

##############################################################
#
#     General option output format definitions and support for
#     validating output formats
#
##############################################################

# Definition of the format keywords within each format group
TABLE_FORMATS = ('table', 'plain', 'simple', 'grid', 'psql', 'rst', 'html')
CIM_OBJECT_FORMATS = ('mof', 'xml', 'repr', 'txt')
TEXT_FORMATS = ('text',)

# Definition of the default format for each format group
DEFAULT_CIM_FORMAT = CIM_OBJECT_FORMATS[0]
DEFAULT_TABLE_FORMAT = TABLE_FORMATS[2]
DEFAULT_TEXT_FORMAT = TEXT_FORMATS[0]

# Dictionary that relates group names to list of formats keywords for that
# group and the default format for that group.  The order of the dictionary
# entry determines the priority of selecting formats.
GROUPVALUES = namedtuple('GROUPVALUES', 'keywords default')
OUTPUT_FORMAT_GROUPS = OrderedDict(
    [('CIM', GROUPVALUES(CIM_OBJECT_FORMATS, DEFAULT_CIM_FORMAT)),
     ('TABLE', GROUPVALUES(TABLE_FORMATS, DEFAULT_TABLE_FORMAT)),
     ('TEXT', GROUPVALUES(TEXT_FORMATS, DEFAULT_TEXT_FORMAT))])

# All of the format strings
OUTPUT_FORMATS = tuple(item for fmts in OUTPUT_FORMAT_GROUPS.values()
                       for item in fmts.keywords)


def output_format_is_table(output_format):
    """
    Return True if output format is a table form.

    Parameters:

      output_format (:term:`string`):
         String containing the output_format keyvalue.

    Returns:
      True: if `output_format` is one of the Table format keyword choises
      False: if `output_format` is not a Table format.
    """
    return output_format in TABLE_FORMATS


def validate_output_format(output_format, valid_format_groups,
                           default_format=None):
    """
    Tests for valid format groups and provides a default format if the
    context.output_format is None.

    Parameters:

      output_format (:term:`string` or None):
        The output format string to be validated (normally provided by input
        (i.e. ContextObj)) or None if there is no defined format for this
        command execution.

      valid_format_groups (list of :term:`string` or :term:`string`):
        One or more strings in a list where the allowed strings are: 'TABLE',
        'CIM', or 'TEXT'. An empty list implies any output group if valid. A
        single string may be used to designate a single group

      default_format (:term:`string` or None):
        One of the valid format definitions or None.  The format must be in the
        OUTPUT_FORMATS list. If None, the default format for the first group in
        `valid_format_groups` is returned. This format keyword is returned if
        `output_format` is None.

    Returns:
       :term:`string` containing output format keyword to be used.

    Raises:
        click.ClickException if format invalid for command
    """

    # These are asserts because they are coding errors in the input parameters
    # for this function
    if isinstance(valid_format_groups, six.string_types):
        valid_format_groups = [valid_format_groups]

    # Code error if this assert fails
    assert all(element in OUTPUT_FORMAT_GROUPS for element in
               valid_format_groups)

    if default_format:
        assert default_format in OUTPUT_FORMATS

    # Confirm default matches group.
    # CIM object type has priority over Table
    if output_format:
        # Do invalid message here but really should be assert because this
        # is a error in the data defined for the validate call.
        for group, value in OUTPUT_FORMAT_GROUPS.items():
            if group in valid_format_groups:
                if output_format in value.keywords:
                    return output_format
        if not valid_format_groups:
            return output_format

    else:   # output_format is None
        if default_format:
            return default_format
        if valid_format_groups:
            for group, value in OUTPUT_FORMAT_GROUPS.items():
                if valid_format_groups[0] == group:
                    return value.default
            return OUTPUT_FORMAT_GROUPS['CIM'].default
        return OUTPUT_FORMAT_GROUPS['CIM'].default

    valid_formats = ""
    for name, value in OUTPUT_FORMAT_GROUPS.items():
        fmt_list = value.keywords
        if name in valid_format_groups:
            if valid_formats:
                valid_formats += "; "
            valid_formats += '{0} formats: "({1})"'.format(
                name, '", "'.join(fmt_list))

    raise click.ClickException('Output format "{}" not allowed for this '
                               'command. Only {} allowed.'.
                               format(output_format, valid_formats))


######################################################################
#
#  General common functions
#
######################################################################


def resolve_propertylist(propertylist):
    """
    Resolve property list received from click options.  Click options produces
    an empty list when there is no property list.

    Pywbem requires None when there is no propertylist

    Further, property lists can be input as a comma separated list so this
    function also splits any string with embedded commas.

    Parameters:

      propertylist (list of :term:`string` or None):
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
    """Issue the msg param as warning prefixed by WARNING: to stderr"""
    click.echo('WARNING: {}'.format(msg), err=True)


######################################################################
#
#  Functions to select from console
#
######################################################################


def pick_one_from_list(context, options, title):
    """
    Interactive component that displays a set of options (strings) and asks
    the user to select one.  Returns the item and index of the selected string.

    If there is only a single item in the options, simply return that choice
    without user intervention.

    Parameters:
      options:
        List of strings from which one will is to be selected

      title:
        Title to display before selection

    Retries until either integer within range of options list is input
    or user enter no value. Ctrl-C ends even the REPL.

    Returns:
      Selected item from options_list

    Raises:
      ValueError if Ctrl-c input from console.

    TODO: Possible Future This could be replaced by the python pick library
    that would use curses for the selection process.
    """

    # If there is only a single choice, return that choice.
    if len(options) == 1:
        return options[0]

    # Issue list of choices and prompt for user choice of index
    if context:
        context.spinner_stop()

    click.echo(title)
    index = -1
    for str_ in options:
        index += 1
        click.echo('{}: {}'.format(index, str_))
    selection = None
    msg = 'Input integer between 0 and {} or Ctrl-C to exit selection' \
        .format(index)

    # Loop for valid user choice until valid choice made or selection aborted
    # by user
    while True:
        try:
            selection_txt = click.prompt(msg)
            selection = int(selection_txt)
            if 0 <= selection <= index:
                if context:
                    context.spinner_start()
                return options[selection]
        except ValueError:  # This causes the retry of the request
            pass
        except KeyboardInterrupt:
            raise click.ClickException("Pick Aborted. CTRL-C")
        except Exception as ex:
            raise click.ClickException(
                'Selection exception: {} Command Aborted'.format(ex))
        click.echo('"{}" Invalid response {}'.format(selection_txt, msg))


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

    Raises:
        ClickException if user choses to terminate the selection process
    """
    if not is_classname(objectname):
        raise click.ClickException('{} must be a classname'.format(objectname))
    instance_names = context.conn.PyWbemcliEnumerateInstancePaths(objectname,
                                                                  namespace)

    if not instance_names:
        click.echo('No instance paths found for {}'.format(objectname))
        return None

    try:
        return pick_one_from_list(context, instance_names,
                                  'Pick Instance name to process')
    except Exception as ex:
        raise click.ClickException('Command Aborted. Exception {}'.format(ex))


def pick_multiple_from_list(context, options, title):
    """
    Interactive component that displays a set of options (strings) and asks
    the user to select multiple entries from that list.  Returns a list of
    the items selected.

    Retries until either integer within range of options list is input
    or user enter no value. Ctrl-C ends even the REPL.

    Parameters:
      context:
        If not None, the ContextObj which is used to stop and start the
        spinner.
      options:
        List of strings to select

      title:
        Title to display before selection

    Returns:
      list of index of selected items

    Raises:
      ValueError if Ctrl-c input from console.

    TODO: This could be replaced by the python pick library that would use
    curses for the selection process.
    """
    if context:
        context.spinner_stop()

    click.echo(title)
    index = -1
    for str_ in options:
        index += 1
        click.echo('{}: {}'.format(index, str_))
    selection = None
    selection_list = []
    msg = 'Select entry by index or hit enter to end selection>'
    while True:
        try:
            selection_txt = click.prompt(msg)
            if not selection_txt:
                if context:
                    context.spinner_start()
                return selection_list

            selection = int(selection_txt)
            if 0 <= selection <= index:
                selection_list.append(options[selection])
            continue
        except ValueError:
            pass
        except KeyboardInterrupt:
            raise ValueError
        click.echo('{} Invalid. Input integer between 0 and {}; hit enter to '
                   'stop selection.'.format(selection, index))


def is_classname(astring):
    """
    Test if the astring input is a classname or contains instance name
    components.  The existence of a period at the end of the name component
    determines if it is a classname or instance name.

    Returns:
        True if classname. Otherwise it returns False
    """
    assert isinstance(astring, six.string_types)
    return not re.match(r'[a-zA_Z0-9_].*\.', astring)


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

      pattern (:term:`string`):
        Python glob pattern to match.

      name_list:
        List of strings to be matched.

      ignore_case (bool):
        If True, do case-insensitive match. Default = True

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
        raise click.ClickException('Regex compile error. Regex={}. Er: {}: {}'
                                   .format(regex, ex.__class__.__name__, ex))

    new_list = [n for n in name_list for m in [compiled_regex.match(n)] if m]

    return new_list


def verify_operation(txt, msg=None):
    """
    Issue click confirm request and return result.  If msg is none and
    confirm response is n, output msg.

    Parameters:

      txt (:term:`string`):
        String that is prefixed to the prompt text and defines the
        verification request.

      msg (:class:`py:bool`):
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
    try:
        instance_name = CIMInstanceName.from_wbem_uri(wbemuri_str)
        if instance_name.namespace and namespace:
            if instance_name.namespace != namespace:
                raise click.ClickException('Conflicting namespaces between '
                                           'wbemuri {} and option {}'
                                           .format(instance_name.namespace,
                                                   namespace))
        elif instance_name.namespace is None and namespace:
            instance_name.namespace = namespace

        return instance_name
    except ValueError as ve:
        raise click.ClickException('Invalid wbem uri input {}. Error {}'
                                   .format(wbemuri_str, ve))


def create_cimvalue(cim_type, value_str, is_array):
    """
    Build a cim value of the type in cim_type and the information in value_str
    or fail with an exception if the value_str cannot be parsed into a
    CIMValue or list of CIMValue elements.

    Parameters:
      cim_type (:term:`string`):
        CIMType for this value. The CIM data type name for the CIM object.
        See :ref:`CIM data types` for valid type names.

      value_str (:term:`string`):
        String defining the input to be parsed.

      is_array (:class:`py:bool`):
        The value_str is to be treated as a comma separated set of values.

    Return:
        is_array == False. Returns a single CIMValue
        is_array == True. Returns a list of CIMValues

    Raises:
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
        raise ValueError('Invalid boolean value: "{}"'.format(value))

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

      cim_class (:class:`~pywbem.CIMClass`):
        CIM Class that includes the property defined by name

      name (:term:`string`):
        Name of the property to be constructed

      value_str (:term:`string`):
        String form for the value to be inserted.

    Returns:
        CIMProperty with name defined by name and CIMValue corresponding to
        value_str and property information from the class

    Raises:
        ValueError if value_str, cim_type and is_array mismatch.
    """
    cim_value = create_cimvalue(cim_type, value_str, is_array)

    return CIMProperty(name, cim_value, cim_type)


def create_ciminstancename(cim_class, kv_keys):
    """
    Create a CIMInstanceName object from the input parameters.

    The provided key values are verified against the properties of the class.

    Parameters:

      cim_class (:class:`~pywbem.CIMClass`):
        The class from which the CIMInstanceName is to be created.
        The provided keys are validated against the properties of that class.

      kv_keys (tuple):
        A tuple of name/value pairs representing the keys and their
        values that are to be constructed for the instance name. Required

    Returns:
        CIMInstanceName: with namespace = None and host = None

    Raises:
        click.ClickException if Property name not found in class or if mismatch
          of property type in class vs value component of kv pair
    """
    # TODO: Avoid the CIMClass object as input, because GetClass is not
    # implemented by all WBEM servers. That is not easy however, because the
    # name=value syntax used in the --key option does not allow distinguishing
    # the string/numeric/boolean types sufficiently well. For example, one
    # would need to find a way to resolve the ambiguity between numeric/boolean
    # values and strings with that same string value. One option might be to
    # have optional single or double quotes around string values, that normally
    # would not be needed, but when the string value is a numeric or boolean
    # string, then they would be used to turn the value into a string. For
    # example: name=42 -> numeric, name="42" -> string.
    keys = []
    for kv_property in kv_keys:
        name, value_str = parse_kv_pair(kv_property)
        try:
            cl_prop = cim_class.properties[name]
        except KeyError:
            raise click.ClickException('Property name "{}" not in class "{}".'
                                       .format(name, cim_class.classname))

        if value_str and value_str.startswith('"') and value_str.endswith('"'):
            value_str = value_str[1:-1]
        try:
            value = create_cimvalue(cl_prop.type, value_str, False)
            keys.append((name, value))
        except ValueError as ex:
            raise click.ClickException("Type mismatch property '{}' between "
                                       "expected type='{}', array={} and input "
                                       "value='{}'. Exception: {}"
                                       .format(name, cl_prop.type,
                                               cl_prop.is_array,
                                               value_str, ex))

    try:
        instance_path = CIMInstanceName(cim_class.classname, keybindings=keys)
    except ValueError as exc:
        raise click.ClickException(str(exc))

    return instance_path


def create_ciminstance(cim_class, kv_properties):
    """
    Create a CIMInstance object from the input parameters.

    Parameters:

      cim_class (CIMClass):
        The class from which the CIMInstance is to be created

      kv_properties (tuple):
        A tuple of name/value pairs representing the properties and their
        values that are to be constructed for the instance. Required

    Returns:
        CIMInstance

    Raises:
        click.ClickException if Property name not found in class or if mismatch
          of property type in class vs value component of kv pair
    """
    properties = []
    for kv_property in kv_properties:
        name, value_str = parse_kv_pair(kv_property)
        try:
            cl_prop = cim_class.properties[name]
        except KeyError:
            raise click.ClickException('Property name "{}" not in class "{}".'
                                       .format(name, cim_class.classname))

        try:
            prop = create_cimproperty(cl_prop.type,
                                      cl_prop.is_array,
                                      name,
                                      value_str)
            properties.append((name, prop))
        except ValueError as ex:
            raise click.ClickException("Type mismatch property '{}' between "
                                       "expected type='{}', array={} and input "
                                       "value='{}'. Exception: {}"
                                       .format(name, cl_prop.type,
                                               cl_prop.is_array,
                                               value_str, ex))

    new_inst = CIMInstance(cim_class.classname, properties=properties)

    return new_inst


def compare_obj(obj1, obj2, msg):
    """
    Compare two objects and display error if different.  Returns True if
    match or False if different
    """
    if obj1 != obj2:
        click.echo('Obj Compare {}: compare mismatch:\n{!r}\n{!r}'
                   .format(msg, obj1, obj2))
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
            click.echo('Different number of properties {} vs {}\n{}\n{}'
                       .format(len(inst1.properties), len(inst2.properties),
                               inst1.keys(), inst2.keys()))
            return False
        keys1 = set(inst1.keys())
        keys2 = set(inst2.keys())
        if keys1 != keys2:
            diff = keys1.symmetric_difference(keys2)
            click.echo('Property Name differences {}'.format(diff))
            return False

        for n1, v1 in six.iteritems(inst1):
            if v1 != inst2[n1]:
                msg = 'property ' + n1
                if not compare_obj(inst1.get(n1), inst2.get(n1), msg):
                    return False
    return True


def parse_kv_pair(pair):
    """
    Parse a single key/value pair string in 'KEY=VALUE' syntax, and return a
    tuple (key, value).

    The parsing assumes that KEY does not include '=', which is always the case
    for CIM names. VALUE may contain '=' characters, which are retained.

    If 'VALUE' or '=VALUE' are missing, value is returned as None.
    """
    name, value = pair.partition("=")[::2]

    # if VALUE is missing, return it as None.
    if not value:
        value = None

    return name, value


def split_array_value(astring, delimiter):
    """Simple split of a string based on a delimiter"""

    rslt = split_str_w_esc(astring, delimiter)
    return rslt


def split_str_w_esc(astring, delimiter, escape='\\'):
    """
    Split string based on delimiter defined in call and the escape character \\
    To escape use of the delimiter in the strings. Delimiter may be multi
    character.
    Returns list of elements split from the input str
    """
    ret = []
    current_element = []
    iterator = iter(astring)
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

          cim_method (CIMMethod):
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
            "Class {} does not have a method {}"
            .format(classname, methodname))
    cim_method = cim_methods[methodname]

    params = create_params(classname, cim_method, options['parameter'])

    rtn = context.conn.InvokeMethod(methodname, objectname, params)

    # Output results, both ReturnValue and all output parameters
    click.echo('ReturnValue={}'.format(rtn[0]))

    if rtn[1]:
        cl_params = cim_method.parameters
        rtn_params = rtn[1]
        for pname, pvalue in rtn_params.items():
            ptype = cl_params[pname].type if pname in cl_params else None
            val = cimvalue_to_fmtd_string(
                pvalue, ptype, maxline=DEFAULT_MAX_CELL_WIDTH,
                avoid_splits=False)
            click.echo('{}={}'.format(pname, val[0]))


####################################################################
#
#  Display of CIM objects.
#
####################################################################


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
        raise TypeError('{} cannot be sorted'.format(type(cim_objects[0])))

    return [sort_dict[key] for key in sorted(sort_dict.keys())]


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
            _print_objects_as_table(cim_objects, output_format, context=context)
        else:
            # Call to display each object
            for obj in cim_objects:
                display_cim_objects(context, obj, output_format=output_format)
        return

    # Display a single item.
    object_ = cim_objects
    # This allows passing single objects to the table formatter (i.e. not lists)
    if output_format_is_table(output_format):
        _print_objects_as_table([object_], output_format, context=context)
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

    Parameters:

      obj (:class:`pwbem.CIMInstanceName`):
        Instance name from which keybindings are to be extracted for
        formatting.

    Returns:
        :term:`string` containing the keys from the input obj formatted for
        display at within the defined width.
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
                    wbem_uri_keys += '\n{}'.format(one_key_obj)
                    line_len = 0
                else:
                    wbem_uri_keys += ',{}'.format(one_key_obj)
                    line_len += len(one_key_obj) + 1

            else:  # must put on first line even if too long
                wbem_uri_keys += one_key_obj
                line_len = len(one_key_obj) + 1

    return wbem_uri_keys


def display_text(text, output_format=None):  # pylint: disable=unused-argument
    """
    Display the text output format. Currently this simply outputs to
    click.echo
    """
    click.echo(text)


class NoCaseList(object):
    """
    This class simplifies working with lists of strings that are to be tested
    case-insenstive. This simplifies working with  the CIM object attributes
    that are case insensitive such as class names, roles, etc.

    NOTE: This code does not handle None either for items in the list or for
    the str parameter in __contains__

    Example:

        roles = NoCaseList(roles)
        # the following does case insensitive test
        if role in roles:
            do something
    """

    def __init__(self, strs):
        """
        Constructor requires list of strings input

        Parameters:

          strs (list of :term:`string`):
            The strings that will make up the list
        """

        assert isinstance(strs, list)
        self.str_list = strs

    def __contains__(self, astring):
        """
        Implement Python 'in' functionality.

        Parameters:

          astring (:term:`string`):
            String to test against the instance of NocaseList

        Returns:
          True if string in list (case insensitive compare)
        """

        assert astring is not None
        return astring.lower() in (n.lower() for n in self.str_list)

    def add(self, strs):
        """
        Add string or list of strings to the list

        Parameters:

          strs (:term:`string` or list, tuple of :term:`string`):
            String to test against the instance of NocaseList.
      """
        if not strs:
            return
        if isinstance(strs, list):
            self.str_list.extend(strs)
        else:
            self.str_list.append(strs)

    def get(self, astring):
        """
        Get the string that matches astring case insensitive

        Parameters:

          astring (:term:`string` or list, tuple of :term:`string`):
            String to test against the instance of NocaseList.

        Returns:
            String in list that matches No case the input string, or None
            if the input string was empty or None.

        Raises:
            KeyError: If no match
        """
        if not astring:
            return None
        tstr = astring.lower()
        for s in self.str_list:
            if tstr == s.lower():
                return s
        raise KeyError('{} not found in list'.format(astring))


def shorten_path_str(path, replacements, fullpath):
    """
    Create a short-form path str from the input CIMInstanceName with selected
    components shortened to just a single known character.  This allows
    modifying the path string to replace selected key/value paris with a single
    character. Thus where the original string is very long and contains
    repeated key bindings (ex. CreationClassName) we can shorten the path
    string by reducing selected key/value pairs to just ~

    Parameters:

      path (:class:`CIMInstanceName`):
        CIMInstanceName object defining instance name to shorten

      replacements:
        Dictionary of the replacements containing a key names and key
        values to be replaced. If the key value is None, they name alone
        causes the replacement. Otherwise, both the name and value must
        match.

      fullpath (:class:`py:bool`):
        If True Return complete path using to_wbem_rul. Otherwise, shorten
        the path by replacing keys defined by the replacements dictionary.
        shorten the path, otherwise simply convert to string. Othewise

    Returns:
        String representation of the path.
    """

    if fullpath:
        # Just build the full path string
        name_str = path.to_wbem_uri()

    else:
        # Shorten path based on key definitons in replacements
        kbs = path.keybindings
        repl_list = []
        magicvalue = 9999123999918
        for k, v in kbs.items():
            for key, value in replacements.items():
                if k.lower() == key.lower():
                    if value is None or v == value:
                        repl_list.append((key, value))
                        # Set the value to a known value for the replacement
                        kbs[key] = magicvalue
        path.keybindings = kbs
        name_str = path.to_wbem_uri()
        # replace each key binding in repl_list with ~ char
        for key, value in repl_list:
            name_str = name_str.replace("{}={}".format(key, magicvalue), "~", 1)

    return name_str


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


def _print_instances_as_table(insts, table_width, table_format,
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

    header_line = []
    if include_classes:
        header_line.append("classname")
    header_line.extend(prop_names)

    # Fold long property names
    new_header_line = []
    for header in header_line:
        if len(header) > max_cell_width:
            new_header_line.append(fold_strings(header, max_cell_width))
        else:
            new_header_line.append(header)

    for inst in insts:
        if not isinstance(inst, CIMInstance):
            raise ValueError('Only CIMInstance display allows table output')

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
        for pn in inst.properties:
            all_props[pn] = pn.lower()
            if inst.path and pn in inst.path.keybindings:
                key_props[pn] = pn.lower()

    nonkey_props = odicti()  # key: org prop name, value: lower cased prop name
    for pn in all_props:
        if pn not in key_props:
            nonkey_props[pn] = all_props[pn]

    key_prop_list = sorted(key_props.keys(), key=lambda pn: key_props[pn])
    nonkey_prop_list = sorted(
        nonkey_props.keys(), key=lambda pn: nonkey_props[pn])
    key_prop_list.extend(nonkey_prop_list)
    return key_prop_list


def _print_objects_as_table(objects, output_format, context=None):
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
            _print_instances_as_table(objects, table_width, output_format,
                                      context=context)
        elif isinstance(objects[0], CIMClass):
            _print_classes_as_table(objects, table_width, output_format)
        elif isinstance(objects[0], CIMQualifierDeclaration):
            _print_qual_decls_as_table(objects, table_width, output_format)
        elif isinstance(objects[0], (CIMClassName, CIMInstanceName,
                                     six.string_types)):
            _print_paths_as_table(objects, table_width, output_format)
        else:
            raise click.ClickException("Cannot print {} as table"
                                       .format(type(objects[0])))


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
    len_hdr = len(headers)
    for row in rows:
        assert len(row) == len_hdr, "row: {}\nhdrs: {}". \
            format(row, headers)
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

      headers (list strings):
        where each string is a table column name or None if no header is to be
        attached

      table_data (list of lists):
        where each the top level iterables represents the list of rows
        and each row is an iterable of strings for the data in that row.

      title (:term:`string`):
         Optional title to be places io the output above the table.
         No title is output if this parameter is None

      table_format (:term:`string`):
        Output format defined by the string and limited to one of the
        choice of table formats defined in TABLE_FORMATS list

      output_file (:term:`string`):
        If not None, a file name to which the output formatted data is sent.

      sort_columns (int or list of int that defines sort):
        Defines the cols that will be sorted. If int, it defines the column
        that will be sorted. If list of int, the sort is in sort order of
        cols in the list (i.e. minor sorts to the left, major sorts to the
        right). Note that entries in each row of the columns to be sorted
        must be of the same type (int, str, etc.) to be sortable.

    Returns:
        :term:`string`: Returns the formatted table as a string

    Raises:
        click.ClickException if invalid table format string
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
    if not output_format_is_table(table_format):
        raise click.ClickException('Invalid table format {}.'
                                   .format(table_format))

    result = tabulate.tabulate(rows, headers, tablefmt=table_format)
    if title:
        if table_format == 'html':
            result = '<p>{0}</p>\n{1}'.format(title, result)
        else:
            result = '{0}\n{1}'.format(title, result)
    return result


def fold_strings(input_strings, max_width, break_long_words=False,
                 break_on_hyphens=False, fold_list_items=False, separator=', ',
                 initial_indent='', subsequent_indent=''):
    """
    Fold a string or a list/tuple of strings within a maximum width and return
    a folded string that fits within the width defined by max_width. If input
    is a list of strings, the fold_list_itmes defines whether they create
    separate lines in the output or are concatenated into a single string
    before folding the string. This implementation refolds strings that already
    contain EOL characters and removes any existing folds that do not match the
    max_width criteria.  Lists of strings may be folded with one string per
    line or concatenated and then folded.

    Parameters:

      input_strings (:term:`string` or list of :term:`string`):
        The string that will be contents of into the cell. This string may
        already include multiple lines.

      max_width (:term:`integer`):
        Maximum width of cell containing the resulting string.  Data is
        folded into multiple lines to fit into this width.

      break_long_words (:class:`py:bool`):
        Boolean that forces long words to be broken if True
        If False, long words will not break at the max width

      break_on_hyphens (:class:`py:bool`):
        If True use hypens as word separator.

      fold_list_items (:class:`py:bool`):
        If True, force fold for each item in list/tupe of input strings if
        single line concatenation is longer than max_width. Otherwise list is
        contatenated and the result folded.

      separator (:term:`string`):
        String that is separator between list items when folded into
        string.

      initial_indent (:term:`integer` or :term:`string`):
        Integer  or string defining the number of characters of indent for
        the first line if single string or the first line of each string in
        the list if input_strings is a list and fold_list_items is True.

      subsequent_indent (:term:`integer`):
        Integer or string, defining the number of characters of indent for
        the all but the first lineif single string or the first line of
        each string in the list if input_strings is a list and
        fold_list_items is True.

    Returns:
        String representing the folded input_strings
    """
    def indent_str(indent):
        """
        Maps indent to string of indent characters if necessary.
        If None, return None
        If integer, map to indent characters
        """
        if indent is None:
            return ""
        if isinstance(indent, six.string_types):
            return indent
        return ' ' * indent

    initial_indent = indent_str(initial_indent)
    subsequent_indent = indent_str(subsequent_indent)

    if isinstance(input_strings, (list, tuple)):
        if separator is None:
            separator = ', '
        build_str = separator.join(input_strings)
        # Return contatentated list if within cell width
        if len(build_str) <= max_width:
            return build_str

        if fold_list_items:
            folded_strings = []
            for str_item in input_strings:
                folded_strings.append(
                    fold_strings(str_item, max_width,
                                 break_long_words=break_long_words,
                                 break_on_hyphens=break_on_hyphens,
                                 initial_indent=initial_indent,
                                 subsequent_indent=subsequent_indent))
            return "\n".join(folded_strings)
        input_strings = build_str

    # process single string
    input_string = input_strings
    assert isinstance(input_string, six.string_types)

    if len(input_string) <= max_width:
        return input_string

    # use textwrap fill to fold the string
    folded_string = fill(input_string, max_width,
                         break_long_words=break_long_words,
                         break_on_hyphens=break_on_hyphens,
                         initial_indent=initial_indent,
                         subsequent_indent=subsequent_indent)

    return folded_string


def raise_pywbem_error_exception(er):
    """
    Raise the standard click exception for a pywbem Error exception.  These
    exceptions do not cause interactive mode failure but display the exception
    class and its str value and return to the repl mode.
    """
    raise click.ClickException('{}: {}'.format(er.__class__.__name__, er))
