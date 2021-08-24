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
try:
    from collections.abc import Sequence
except ImportError:
    # pylint: disable=deprecated-class
    from collections import Sequence

import six
import click
import tabulate
from nocaselist import NocaseList
from toposort import toposort_flatten

from pywbem import CIMInstanceName, CIMInstance, CIMClass, \
    CIMQualifierDeclaration, CIMProperty, CIMClassName, \
    cimvalue, Error
from pywbem._nocasedict import NocaseDict

from ._cimvalueformatter import cimvalue_to_fmtd_string


# Definitions of the components of the help Usage line used
# by pywbemcli
GENERAL_OPTS_TXT = '[GENERAL-OPTIONS]'
CMD_OPTS_TXT = '[COMMAND-OPTIONS]'
SUBCMD_HELP_TXT = "COMMAND [ARGS] " + CMD_OPTS_TXT

DEFAULT_MAX_CELL_WIDTH = 100


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


def output_format_in_groups(output_format, format_groups):
    """
    Return True if output format is in the group defined by format_group

    Parameters:

      output_format (:term:`string`):
         String containing the output_format keyvalue.

      output_groups (:term:`string` or list of :term:`string`):
         String containing the format group ot list of strings representing
         multiple groups. This must be one of the keys in the table
         OUTPUT_FORMAT_GROUPS.  If the

    Returns:
      True: if it is in the group or one of the list of groups
      False: if it is not in any of the the groups.

    Raises:
        KeyError: If format_group parameter is not a valid group
    """
    if isinstance(format_groups, (list, tuple)):
        for group in format_groups:
            if output_format_in_groups(output_format, group):
                return True
        return False

    # test if output_format string is in a group
    return output_format in OUTPUT_FORMAT_GROUPS[format_groups]


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

      title (:term:`string`):
        Title to display before selection

    Retries until either integer within range of options list is input
    or user enter no value. Ctrl-C ends even the REPL.

    Returns:
      Selected item from options_list

    Raises:
      ValueError if Ctrl-c input from console.
    """

    # If there is only a single choice, return that choice.
    if len(options) == 1:
        return options[0]

    # Issue list of choices and prompt for user choice of index
    if context:
        context.spinner_stop()

    click.echo(title)
    for index, str_ in enumerate(options):
        click.echo('{}: {}'.format(index, str_))
    max_option = len(options) - 1
    selection = None
    msg = 'Input integer between 0 and {} or Ctrl-C to exit selection' \
        .format(max_option)

    # Loop for valid user choice until valid choice made or selection aborted
    # by user
    while True:
        try:
            selection_txt = click.prompt(msg)
            selection = int(selection_txt)
            if 0 <= selection <= max_option:
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
    conn = context.pywbem_server.conn
    if not is_classname(objectname):
        raise click.ClickException('{} must be a classname'.format(objectname))
    try:
        instance_names = conn.PyWbemcliEnumerateInstancePaths(
            objectname, namespace)
    except Error as ex:
        raise pywbem_error_exception(ex)

    if not instance_names:
        click.echo('No instance paths found for {}'.format(objectname))
        return None

    try:
        return pick_one_from_list(context, sort_cimobjects(instance_names),
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

    if value_str is None:
        return None

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

      cim_type (:term:`string`):
        CIM type of the property

      is_array (bool):
        Boolean indicating that property is an array

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

    return CIMProperty(name, cim_value, type=cim_type, is_array=is_array)


def create_ciminstance(cim_class, kv_properties):
    """
    Create a CIMInstance object from the input parameters.

    Parameters:

      cim_class (CIMClass):
        The class from which the CIMInstance is to be created

      kv_properties (tuple):
        A tuple of "name=value" strings representing the properties and their
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
    Parse a single "KEY=VALUE" string and return a tuple (key, value).

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


def process_invokemethod(context, objectname, methodname, namespace,
                         parameters):
    # pylint: disable=line-too-long
    """
    Process the parameters for invokemethod at either the class or instance
    level and execute the invokemethod.

    Parameters:

      objectname (:class:`~pywbem.CIMClassName` or :class:`~pywbem.CIMInstanceName`)  # noqa: E501
        The objectname (class or instance) that is the invokemethod
        target. The namespace must have been inserted into the objectname
        before calling this method

      methodname (:term:`string`):
        The name of the method to be executed

      namespace()
      options (:class:`py:dict`):
        The command options dictionary.  Used to get the command namespace
        and parameters.

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

    assert isinstance(objectname, (CIMClassName, CIMInstanceName))
    conn = context.pywbem_server.conn
    classname = objectname.classname

    cim_class = conn.GetClass(
        classname,
        namespace=namespace, LocalOnly=False)

    cim_methods = cim_class.methods
    if methodname not in cim_methods:
        raise click.ClickException(
            "Class {} does not have a method {}"
            .format(classname, methodname))
    cim_method = cim_methods[methodname]

    params = create_params(classname, cim_method, parameters)

    rtn = conn.InvokeMethod(methodname, objectname, params)

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


def sort_cimobjects(cim_objects):
    """
    Return a sorted list of the input objects.

    The returned list is always a new list and its items are the original input
    objects.

    The following input object types are supported, and their sort key is:

    * string: Sorted by string value (case sensitively). This case covers the
      result of 'class enumerate'.

    * CIMClass: Sorted by class name (case sensitively).

    * CIMClassName, CIMInstanceName: Sorted by its canonical WBEM URI string.
      This makes the sort case insensitive.

    * CIMInstance: Must have the path set. Sorted by the canonical WBEM URI
      string of its instance path. This makes the sort case insensitive.

    * CIMQualifierDeclaration: Sorted by qualifier name (case sensitively).

    * tuple(CIMClassName, CIMClass): Sorted by the canonical WBEM URI
      string of the CIMClassName object. This makes the sort case insensitive.
      This case covers the result of 'class references/associators'.

    Parameters:

      cim_objects (Sequence): Objects to be sorted.

    Returns:
        A new list of the original input objects, sorted as defined above.

    Raises:
        TypeError: Invalid type for input parameter 'cim_objects'.
        ValueError: CIMInstance object in sort list has no 'path' set.
    """
    assert isinstance(cim_objects, Sequence)

    if not cim_objects:
        return []

    tst_obj = cim_objects[0]

    # This case covers result of 'class enumerate':
    if isinstance(tst_obj, six.string_types):
        return sorted(cim_objects)

    if isinstance(tst_obj, CIMClass):
        return sorted(cim_objects,
                      key=lambda obj: obj.classname)

    if isinstance(tst_obj, (CIMClassName, CIMInstanceName)):
        return sorted(cim_objects,
                      key=lambda obj: obj.to_wbem_uri(format="canonical"))

    if isinstance(tst_obj, CIMInstance):
        try:
            return sorted(
                cim_objects,
                key=lambda obj: obj.path.to_wbem_uri(format="canonical"))
        except AttributeError as exc:
            new_exc = ValueError(
                "CIMInstance object in sort list has no 'path' set: {}".
                format(exc))
            new_exc.__cause__ = None
            raise new_exc

    if isinstance(tst_obj, CIMQualifierDeclaration):
        return sorted(cim_objects,
                      key=lambda obj: obj.name)

    # This case covers result of 'class references/associators':
    if isinstance(tst_obj, tuple):
        if not isinstance(tst_obj[0], CIMClassName) or \
                not isinstance(tst_obj[1], CIMClass):
            raise TypeError("Items of type tuple ({}, {}) cannot be sorted".
                            format(type(tst_obj[0]), type(tst_obj[1])))
        return sorted(cim_objects,
                      key=lambda tup: tup[0].to_wbem_uri(format="canonical"))

    raise TypeError("Items of type {} cannot be sorted".format(type(tst_obj)))


def get_leafclass_names(classes):
    """
    Get the leaf classes of the classes that are present in the
    input list classes

      Parameters:
        classes: list of :class:`pywbem:CIMClass`

      Returns
        NocaseList of :term:`unicode string` with the names of all classes
        that do not have a subclass

    """
    # Build dictionary of superclassname: classnames. This can be used to
    # find subclasses of any class in the dictionary.
    classname_dict = {}
    for c in classes:
        if c.classname not in classname_dict:
            classname_dict[c.classname] = []
        if c.superclass:
            if c.superclass in classname_dict:
                classname_dict[c.superclass].append(c.classname)
            else:
                classname_dict[c.superclass] = [c.classname]

    # get list of all classnames with no value (i.e. no subclasses)
    rtn_list = [key for key, value in six.iteritems(classname_dict)
                if not value]
    return NocaseList(rtn_list)


def get_subclass_names(classes, classname=None, deep_inheritance=None):
    """
    Get class names that are subclasses of classname, including indirect
    subclasses of the classname input parameter from a list of CIM Classes.

    The input classname is NOT included in the returned list.

    Note: The classes list MUST include all subclasses to any class
    that is the list (i.e what is returned by an enumerate classes) but need
    not include the top level classes(those with with c.superclass == None)

    Parameters:
      classname (:term:`string`):
        The name of the CIM class for which subclass names will
        be retrieved. If None, retrieval starts at the root of
        the class hierarchy. Classes that have superclass None or have
        a superclass not in the list of classes

      classes (:class:`~pywbem_mock.BaseObjectStore):
       A list of CIM classes for which the subclass of a member is to
       be returned.

      deep_inheritance (:class:`py:bool`):
        If True, the complete set of subclasses found in the classes list
        is returned.  If not True, only the direct subclasses list is returned.

    Returns:
      NocaseList of :term:`unicode string` with the names of all subclasses of
      `classname`.  returns empty list if classname is not in the list or their
      are no subclasses.

    Exceptions: ValueError if classname not in classes
    """

    assert isinstance(classname, six.string_types)

    # Build dictionary of superclassname: classnames
    classname_dict = NocaseDict()
    for c in classes:
        if c.classname not in classname_dict:
            classname_dict[c.classname] = []
        if c.superclass:
            if c.superclass in classname_dict:
                classname_dict[c.superclass].append(c.classname)
            else:
                classname_dict[c.superclass] = [c.classname]

    if classname not in classname_dict:
        raise ValueError("Classname {} not found in classes".format(classname))

    # Recurse The classname_dict hierarchy to get subclass names
    rtn_classnames = classname_dict[classname]
    if deep_inheritance:
        if rtn_classnames:
            subclass_names = rtn_classnames
            while True:
                subclass_names_rtn = []
                for cln in subclass_names:
                    subclass_names_rtn.extend(classname_dict[cln])
                if subclass_names_rtn:
                    rtn_classnames.extend(subclass_names_rtn)
                    subclass_names = subclass_names_rtn
                else:
                    break
    return NocaseList(rtn_classnames)


def display_text(text, output_format=None):  # pylint: disable=unused-argument
    """
    Display the text output format. Currently this simply outputs to
    click.echo
    """
    click.echo(text)


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


def hide_empty_columns(headers, rows):
    """
    Removes columns from rows if the colmuns are considered empty.
    The definiton of an empty row is:
    1. All entries for the column in all rows are None or "" if type string.
    2. All entries for the column in all rows are None if number.

    Parameters:
      headers (list of :term:`string`)
        The strings that represent the column titles of an array of rows.

      rows (list of list of TBD):
        The rows of a table where each row is a list of the items that
        represent the columns of the row.

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
            if isinstance(headers, tuple):
                headersl = list(headers)
                del headersl[column]
                headers = tuple(headersl)
            else:
                del headers[column]
            for row in rows:
                del row[column]

    return headers, rows


def format_table(rows, headers, title=None, table_format='simple',
                 sort_columns=None, hide_empty_cols=None, float_fmt=None):
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

    hide_empty_cols (:class:`py:bool`):
        If this flag is True any columns that are completely blank are
        hiddend and the column header is removed from the headers.
        Uses the function hide_empty_columns

    float_fmt (:term:`string` or list of :term:`string`):
        String defining the formating of floating point format, either
        universal for all floating point if a single string or for selected
        columns if a list is provided.
        The string defines the number of decimals after the decimal point as
        ".<number>f". Thus ".4f" tells the formatter to use 4 digits after the
        decimal point

    Returns:
        :term:`string`: Returns the formatted table as a string

    Raises:
        click.ClickException if invalid table format string
    """
    if hide_empty_cols:
        headers, rows = hide_empty_columns(headers, rows)
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

    # Required because tabulate applies an internally defined format
    # when floatfmt not defined.
    if float_fmt:
        result = tabulate.tabulate(rows, headers, tablefmt=table_format,
                                   floatfmt=float_fmt)
    else:
        result = tabulate.tabulate(rows, headers, tablefmt=table_format)

    if title:
        if table_format == 'html':
            # Insert caption element immediatly after table
            assert result.startswith("<table>")
            replacement = "<table>\n<caption>{0}</caption>".format(title)
            result = result.replace("<table>", replacement, 1)
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


def pywbem_error_exception(exc, intro=None):
    """
    Return the standard click exception for a pywbem Error exception.  These
    exceptions do not cause interactive mode failure but display the exception
    class and its str value and return to the repl mode.

    Parameters:

      exc (Exception): The pywbem Error exception.

      intro (string): An additional message used as introduction for the
        resulting click exception message. This message usually states what
        cannot be done due to the error.

    Returns:
        click.ClickException: Click exception for the pywbem Error exception.
    """
    if intro:
        msg = "{}: {}: {}".format(intro, exc.__class__.__name__, exc)
    else:
        msg = "{}: {}".format(exc.__class__.__name__, exc)
    return click.ClickException(msg)


def dependent_classnames(cls_obj):
    """
    Determine the CIM classes the specified CIM class depends upon, based uopn
    the class declaration in the CIMClass object. This function operates solely
    on the provided CIMClass object and does not communicate with the WBEM
    server.

    The following types of dependencies are considered:
    * Superclass
    * Referenced classes (in properties and method parameters)
    * Embedded classes specified with the EmbeddedInstance qualifier (in
      properties, method return values and method parameters)

    The following types of dependencies are not considered:
    * Embedded classes specified with the EmbeddedObject qualifier (in
      properties, method return values and method parameters)
    * Classes specified in the Deprecated qualifier
    * Classes specified in the ModelCorrespondence qualifier

    Note that method return types cannot be references even though this is
    permitted in DSP0004 because DSP0200 does not support the representation of
    such method declarations. Therefore, pywbemtools does not check for them.

    Parameters:

      cls_obj (CIMClass): The specified CIM class.

    Returns:

      NocaseList of string: The unique list of class names of the dependent
      classes, in no particular order. It is guaranteed that the specified class
      itself will not be contained in this list (e.g. when it references itself
      in a method parameter).
    """

    def _add(classnames, new_classname):
        """
        Append new_classname to classnames if not yet contained.

        This provides the add() functionality of a case-insensitive set.
        """
        if new_classname not in classnames:
            classnames.append(new_classname)

    dependent_cln_list = NocaseList()
    if cls_obj.superclass:
        _add(dependent_cln_list, cls_obj.superclass)
    for prop in cls_obj.properties.values():
        embinst_qual = prop.qualifiers.get('EmbeddedInstance', None)
        if embinst_qual:
            _add(dependent_cln_list, embinst_qual.value)
        if prop.reference_class:
            _add(dependent_cln_list, prop.reference_class)
    for meth in cls_obj.methods.values():
        embinst_qual = meth.qualifiers.get('EmbeddedInstance', None)
        if embinst_qual:
            _add(dependent_cln_list, embinst_qual.value)
        # No check for method return values that are references, because that
        # cannot be represented in CIM-XML, even though allowed in DSP0004.
        for parm in meth.parameters.values():
            embinst_qual = parm.qualifiers.get('EmbeddedInstance', None)
            if embinst_qual:
                _add(dependent_cln_list, embinst_qual.value)
            if parm.reference_class:
                _add(dependent_cln_list, parm.reference_class)

    try:
        dependent_cln_list.remove(cls_obj.classname)
    except ValueError:
        pass

    return dependent_cln_list


def depending_classnames(classname, namespace, conn):
    """
    Enumerate all CIM classes in the namespace, determine the classes that
    depend on the specified CIM class and return these depending classes as a
    list of class names.

    This function basically inverts the dependencies determined by
    dependent_classnames(). See there for a description of the class
    dependencies that are considered.

    Parameters:

      classname (string): Class name of the specified CIM class.

      namespace (string): Namespace of the specified CIM class.

      conn (WBEMConnection): WBEM server connection to be used.

    Returns:

      NocaseList of string: The class names of the classes that depend on the
      specified class. It is guaranteed that the specified class itself will
      not be contained in this list (e.g. when it references itself in a method
      parameter).

    Raises:
        click.ClickException: For any WBEM operation errors.
    """
    try:
        all_classes = conn.EnumerateClasses(
            namespace=namespace, ClassName=None,
            IncludeQualifiers=True, DeepInheritance=True, LocalOnly=True)
    except Error as exc:
        raise pywbem_error_exception(
            exc, "Cannot enumerate classes in namespace {}".format(namespace))

    depending_cln_list = NocaseList()
    for cls in all_classes:
        dep_classnames = dependent_classnames(cls)
        if classname in dep_classnames:
            if cls.classname not in depending_cln_list:
                depending_cln_list.append(cls.classname)

    return depending_cln_list


def all_classnames_depsorted(namespace, conn):
    """
    Enumerate all CIM classes in the namespace and return them in a
    dependency-sorted order where the classes that depend on other classes are
    placed before the classes they depend upon.

    This allows for example deleting the classes in the order of the returned
    list without creating or failing due to dangling dependencies.

    The class dependencies that are considered for this purpose are described
    in dependent_classnames().

    Parameters:

      namespace (string): CIM namespace to be used.

      conn (WBEMConnection): WBEM server connection to be used.

    Returns:

      NocaseList of string: The class names of all classes in the namespace
        in dependency-sorted order.

    Raises:
        click.ClickException: For any WBEM operation errors.
    """

    try:
        all_classes = conn.EnumerateClasses(
            namespace=namespace, ClassName=None,
            IncludeQualifiers=True, DeepInheritance=True, LocalOnly=True)
    except Error as exc:
        raise pywbem_error_exception(
            exc, "Cannot enumerate classes in namespace {}".format(namespace))

    all_deps = {}
    for cls in all_classes:
        dep_classnames = dependent_classnames(cls)
        all_deps[cls.classname] = set(dep_classnames)

    # ISSUE #954: Add support for case insensitive sorting.
    flat_cln_iterable = toposort_flatten(all_deps)

    return NocaseList(reversed(flat_cln_iterable))
