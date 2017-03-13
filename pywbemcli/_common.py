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

from __future__ import absolute_import

import re
from six.moves import input  # pylint: disable=redefined-builtin
import click
import click_spinner

from pywbem import WBEMConnection, WBEMServer, CIMInstanceName, CIMInstance, \
    CIMClass, CIMQualifierDeclaration, tocimobj, CIMProperty
from pywbem.cim_obj import mofstr
from pywbem.cim_obj import NocaseDict

from .config import DEFAULT_CONNECTION_TIMEOUT
from ._asciitable import print_ascii_table, fold_line

# from ._debugtools import DumpArgs


# TODO Could this become a special click option type rather than a
# separate function.
def resolve_propertylist(propertylist):
    """
    Correct property list received from options.  Click options produces an
    empty list when there is no property list.  Pywbem requires None
    when there is no propertylist

    Further, property lists can be input as a comma separated list so this
    function also splits these.
    """
    # If no property list, return None which means all properties
    if not propertylist:
        propertylist = None

    # if cmdline was a single empty string, we set to empty list
    # This means send no propertylist and is a special case for the
    # cim/xml and pywbem interface.
    elif len(propertylist) == 1 and len(propertylist[0]) == 0:
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
        ValueError Exception if user elects to abort the selection
    """
    if not is_classname(objectname):
        raise click.ClickException('%s must be a classname' % objectname)
    instance_names = context.conn.EnumerateInstanceNames(objectname,
                                                         namespace)

    if not instance_names:
        click.echo('No instance paths found for %s', objectname)
        return None

    try:
        instancename, _ = pick_from_list(context, instance_names,
                                         'Pick Instance name to process')
        return instancename
    except Exception:
        raise ValueError('Invalid pick')


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
    or user enter ctrl-c.

    Returns: Tuple of option selected, index of selected item

    Exception: Returns ValueError if Ctrl-c input from console.

    TODO: This could be replaced by the python pick library that would use
    curses for the selection process.
    """
    context.spinner.stop()
    print(title)
    index = -1
    for str_ in options:
        index += 1
        print('%s: %s' % (index, str_))
    while True:
        n = input('Index of selection or Ctrl-C to exit> ')
        try:
            n = int(n)
            if n >= 0 and n <= index:
                return options[index], index
        except ValueError:
            pass
        # TODO make this one our own exception.
        except KeyboardInterrupt:
            raise ValueError
        print('%s Invalid. Must be integer between 0 and %s. Ctrl-C to '
              ' terminate selection' % (n, index))
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
    Filter out names in name_list that match compiled_regex.

    Note that the regex may define a subset of the name string.  Thus,  regex:
        - CIM matches any name that starts with CIM
        - CIM_abc matches any name that starts with CIM_abc
        - CIM_ABC$ matches only the name CIM_ABC.

    Parameters:
      regex (:term: `String`) Python regular expression to match

      name_list: List of strings to be matched.

      ignore_case: bool. If True, do case-insensitive match. Default = True

    Returns the list of names that match.

    """
    flags = re.IGNORECASE if ignore_case else None

    compiled_regex = re.compile(regex, flags) if flags else re.compile(regex)

    nl = [n for n in name_list for m in[compiled_regex.match(n)] if m]

    return nl


def _create_connection(server, namespace, user=None, password=None,
                       cert_file=None, key_file=None, ca_certs=None,
                       no_verify_cert=False, debug=False):
    """
    Initiate a WBEB connection, via PyWBEM api. Arguments for
    the request are the parameters required by the pywbem
    WBEMConnection constructor.
    See the pywbem WBEMConnection class for more details on the parameters.

      Parameters:

        server: (string):
          uri of the WBEMServer to which connection is being made including
          scheme, hostname/IPAddress, and optional port

        namespace: (string):
          Namespace which will be the default namespace for the connection.

        user: (string):
            Optional user name(credential) for the connection.

        password: (string):
            Optional password for the connection

        cert_file: (string):
            Optional cert_file path and name for the connection.

        key_file: (string):
            Optional key_file for the connection.

        ca_certs: (string):
            Optional ca_certs for the connection

        no_verify_certs: (bool):
            Optional boolean that determines if client verifys server
            certificate.  If None or False, No verification is performed.

        debug: (bool)
            Optional boolean that is passed to connection. This attribute
            defines whether the server saves output and input packets.
            This functionality is NOT a feature of the WBEMConnection
            constructor but is set after the connection is created.

       Return:
            pywbem WBEMConnection object that can be used to execute
            other pywbem cim_operation requests

       Exception:
           ValueError: if server paramer is invalid or other issues with
           the input values
    """

    if server[0] == '/':
        url = server

    elif re.match(r"^https{0,1}://", server) is not None:
        url = server

    elif re.match(r"^[a-zA-Z0-9]+://", server) is not None:
        ValueError('Invalid scheme on server argument. %s'
                   ' Use "http" or "https"' % server)

    else:
        url = '%s://%s' % ('https', server)

    creds = None

    if key_file is not None and cert_file is None:
        ValueError('keyfile option requires certfile option')

    if user is not None or password is not None:
        creds = (user, password)

    timeout = DEFAULT_CONNECTION_TIMEOUT
    if timeout is not None and (timeout < 0 or timeout > 300):
        ValueError('timeout option(%s) out of range %s to %s sec' %
                   (timeout, 0, 300))

    # if client cert and key provided, create dictionary for wbem connection
    x509_dict = None
    if cert_file is not None:
        x509_dict = {"cert_file": cert_file}
        if key_file is not None:
            x509_dict.update({'key_file': key_file})
    no_verify_cert = True
    ca_certs = None
    conn = WBEMConnection(url, creds, default_namespace=namespace,
                          no_verification=no_verify_cert,
                          x509=x509_dict, ca_certs=ca_certs,
                          timeout=timeout)

    conn.debug = debug
    return conn


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

# TODO if namespace element, it should go back to context. I think.
# TODO: I do not like the name.  This is really cimnamespacename parser


def parse_cim_namespace_str(uri, namespace=None):
    """
    Create and return a CIMObjectPath from a string input.
    For now we do not allow the host element.  The uri is of the form
    namespace:className.<name=value>*

    This differs from wbemuri in that it does not require quotes around
    value elements unless they include commas or quotation marks
    """
    # print('parse uri %s' % uri)
    host = None
    # if matches re.match(r"^//(.*)/".uri,re.I):
    #    # host =  matches.group(1))
    #    # span = matches.span())

    # namespace = None
    key_bindings = {}
    classname = None
    # if not uri.startswith('//'):
    #     host = None
    # TODO implement host component of parse.
    uri_pattern = r'''(?x)
              ([a-zA-Z0-9_]*).      # classname
'''
    match = re.match(uri_pattern, uri, re.VERBOSE)
    # print('uri match %s' % match)
    if match:
        # namespace = match.group(1)
        classname = match.group(1)
        if host and not namespace:
            raise ValueError('HostName with no namespace is invalid')
        next_char = match.end()

        kb_pattern = r'([a-zA-Z0-9_]*=[^",][^,]*)'

        for pmatch in re.finditer(kb_pattern, uri[next_char:]):
            # print('pmatch %s' % pmatch)
            pair = pmatch.group(1).split('=', 1)
            # print('pair %s' % pair)
            if len(pair[0]):
                if pair[1][0] == '"':
                    # if pair[1][:-1] != '"'
                    #    ValueError('Mismatched quotes %s' % pmatch.group(1))
                    key_bindings[pair[0]] = pair[1][1:-1]
                else:
                    try:
                        key_bindings[pair[0]] = int(pair[1])
                    except ValueError:
                        key_bindings[pair[0]] = pair[1]
                    except TypeError:
                        key_bindings[pair[0]] = pair[1]
            else:
                # Value Error when name component empty
                ValueError('Cannot parse keybinding %s' % pair)
    else:
        ValueError('Cannot parse wbemuri %s' % uri)

    inst_name = CIMInstanceName(classname, keybindings=key_bindings, host=host,
                                namespace=namespace)
    # print('CIMInstanceName %s' % inst_name)

    return inst_name


def create_params(cim_method, kv_params):
    """
    Create a parameter values from the input arguments and class.
    """
    params = NocaseDict()
    for p in kv_params:
        name, value_str = parse_kv_pair(p)
        if name not in cim_method.parameters:
            raise click.ClickException('Error. Parameter %s not in method '
                                       ' %s' % (name, cim_method.name))

        cl_param = cim_method.parameters[name]
        is_array = cl_param.is_array

        cim_value = create_cimvalue(cl_param.type, value_str, is_array)

        params[name] = (name, cim_value)
    return params


def create_cimvalue(cim_type, value_str, is_array):
    """
    Build a cim value of the type in cim_type and the information in value_str
    or fail with an exception if the value_str cannot be parsed into a
    CIMValue or list of CIMValue elements.

    Parameters:
      CIM_Type: TODO
        CIMType for this value.

      Value_str (:term: `string`):
        String defining the input to be parsed.
        TODO cover escapes

      is_array (:class:`py:bool`):
        The value_str is to be treated as a comma separated set of values.

    Return:
        is_array == False. Returns a single CIMValue
        is_array == True. Returns a list of CIMValues

    Exceptions:
        ValueError if the value_str cannot be parsed consistent with
        the cim_type and is_array attributes of the call.
    """
    cim_value = None

    if not is_array:
        cim_value = tocimobj(cim_type, value_str)
    else:
        cim_value = []
        values_list = split_array_value(value_str, ',')
        for value_str in values_list:
            cim_value.append(tocimobj(cim_type, value_str))
    return cim_value


def create_cim_property(cim_class, name, value_str):
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
        KeyError if name not in class or ValueError if the value in
        value_str cannot be mapped to a CIMValue
    """

    cl_prop = cim_class.properties[name]

    cim_value = create_cimvalue(cl_prop.type, value_str, cl_prop.is_array)

    return CIMProperty(name, cim_value, cl_prop.type)


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

      Exceptions: KeyError if Property name not found in class.
    """
    properties = NocaseDict()
    for kv_property in kv_properties:
        name, value_str = parse_kv_pair(kv_property)
        try:
            properties[name] = create_cim_property(cim_class, name, value_str)
        except KeyError as ke:
            raise click.ClickException('Error: property name %s not in class %s'
                                       '. Exception %s' %
                                       (cim_class.classname, name, ke))

        except ValueError as ve:
            raise click.ClickException('Error: property  %s value %s cannot be'
                                       ' parsed. Exception %s' %
                                       (name, value_str, ve))

    new_inst = CIMInstance(cim_class.classname, properties=properties,
                           property_list=property_list)

    return new_inst


def compare_obj(obj1, obj2, msg):
    """
    Compare two objects and display error if different.  Returns True if
    match or False if different
    """
    if obj1 != obj2:
        print('OOPS %s: compare mismatch:\n%r\n%r' % (msg, obj1, obj2))
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
            print('Different number of properties %s vs %s' %
                  (len(inst1.properties, len(inst2.properties))))
            keys1 = set(inst1.keys())
            keys2 = set(inst2.keys())
            diff = keys1.symmetric_difference(keys2)
            print('Property Name differences %s' % diff)
            return False
        for n1, v1 in inst1.iteritems():
            if v1 != inst2[n1]:
                msg = 'property ' + n1
                if not compare_obj(inst1.get(n1), inst2.get(n1), msg):
                    return False
    return True


def parse_kv_pair(pair):
    """
    Parse a single key value pair separated by = and return the key
    and value components.

    If the value component is empty, returns None
    """
    name, value = pair.partition("=")[::2]

    # if value has nothing in it, return None.
    if len(value) == 0:
        value = None

    return name, value


def split_array_value(string, delimiter):
    """Simple split of a string based on a delimiter"""

    rslt = [item for item in split_value_str(string, delimiter)]
    return rslt


def split_value_str(string, delimiter):
    """Spit a string based on a delimiter character bypassing escaped
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


def display_cim_objects(context, objects, output_format='mof'):
    """
    Input is either a list of cim objects or a single object. It may be
    any of the CIM types.  This is used to display:
      classes
      instances
      qualifiertypes

      Or list of the names of the above

    output_format defines the proposed format for output of the objects.

    Note: This function may override that choice in the case where the output
    choice is not avialable for the object type.  Thus, for example,
    mof output makes no sense for class names. In that case, the output is
    in the str of the type.
    """
    context.spinner.stop()
    if output_format == 'csv' or output_format == 'txt':
        click.echo("Csv and txt formats not implemented. Using MOF.")
        output_format = 'mof'
    # TODO this is very simplistic formatter and needs refinement.
    if isinstance(objects, (list, tuple)):
        if output_format == 'table':
            display_table(objects)
        else:
            for item in objects:
                display_cim_objects(context, item, output_format=output_format)

    # display the item
    else:
        object_ = objects
        if output_format == 'mof':
            try:
                click.echo(object_.tomof())
            except AttributeError:
                # no tomof functionality
                click.echo(object_)
        elif output_format == 'xml':
            try:
                click.echo(object_.toxmlstr())
            except AttributeError:
                # no toxmlstr functionality
                click.echo(object)
        elif output_format == 'txt':
            try:
                click.echo(object)
            except AttributeError:
                click.echo('%r' % object)

        elif output_format == 'tree':
            raise click.ClickException("tree output format not allowed")


# TODO how can we build the include_classes into the format requirements
# TODO how can we set up the max_cell_width
def display_table(objects, include_classes=False,
                  max_cell_width=20):
    """If possible display the list of object as a table.
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
    lines.append(header_line)

    title = objects[0].classname

    for inst in objects:
        if not isinstance(inst, CIMInstance):
            raise ValueError('Only CIMInstance display allows table output')
        # Look for not allowed property types
        for name in prop_names:
            if name in inst.properties:
                p = inst.properties[name]
                if p.embedded_object:
                    raise ValueError('Cannot process embeddedObject')

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
                    val_str = fold_line(val_str, max_cell_width)
            line.append(val_str)

        lines.append(line)
    print_ascii_table(lines, title=title, inner=True, outer=True)


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
            _str = fold_line(_str, max_width)
    return _str


# TODO We do not know how to handle the fold mechanism
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


class Context(object):
    """
        Manage the click context object. This is the object that communicates
        between the cli commands and command groups. It contains the
        information that is common to the multiple commands
    """

    def __init__(self, ctx, server, default_namespace, user, password, timeout,
                 noverify, certfile, keyfile, output_format, verbose, debug,
                 conn, wbem_server):
        self._server = server
        self._default_namespace = default_namespace
        self._user = user
        self._password = password
        self._timeout = timeout
        self._noverify = noverify
        self._certfile = certfile
        self._keyfile = keyfile
        self._output_format = output_format
        self._verbose = verbose
        self._debug = debug
        self._conn = conn
        self._wbem_server = wbem_server
        self._spinner = click_spinner.Spinner()

    @property
    def server(self):
        """
        :term:`string`: Scheme with Hostname or IP address of the WBEM Server.
        """
        return self._server

    @property
    def user(self):
        """
        :term:`string`: Username on the WBEM Server.
        """
        return self._user

    @property
    def output_format(self):
        """
        :term:`string`: Output format to be used.
        """
        return self._output_format

    @property
    def default_namespace(self):
        """
        :term:`string`: Namespace to be used as default  or requests.
        """
        return self._default_namespace

    @property
    def timeout(self):
        """
        :term: `int`: Connection timeout to be used on requests in seconds
        """
        return self._timeout

    @property
    def certfile(self):
        """
        :term: `int`: Connection timeout to be used on requests in seconds
        """
        return self._certfile

    @property
    def keyfile(self):
        """
        :term: `int`: Connection timeout to be used on requests in seconds
        """
        return self._keyfile

    @property
    def noverify(self):
        """
        :term: `bool`: Connection server verfication flag. If True
        server cert not verified during connection.
        """
        return self._noverify

    @property
    def conn(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMConnection to be used for requests.
        """
        # TODO. We always create wbemserver so not need wbemconnection
        # object in context
        return self._conn

    @property
    def wbem_server(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMServer instance to be used for
        requests.
        """
        return self._wbem_server

    @property
    def password(self):
        """
        :term:`string`: password to be used instead of logging on, or `None`.
        """
        return self._password

    @property
    def spinner(self):
        """
        :class:`~click_spinner.Spinner` object.
        """
        return self._spinner

    @property
    def verbose(self):
        """
        :bool:` '~click.verbose.
        """
        return self._verbose

    @property
    def debug(self):
        """
        :bool:` '~click.debug.
        """
        return self._debug

    def execute_cmd(self, cmd):
        """
        Call the cmd executor defined by cmd with the spinner
        """
        if self._conn is None:
            if self._server is None:
                raise click.ClickException("No WBEM Server defined")
            # TODO We do not cover the ca_certs parameter of wbemconnection
            self._conn = _create_connection(self.server, self.default_namespace,
                                            user=self.user,
                                            password=self.password,
                                            cert_file=self.certfile,
                                            key_file=self.keyfile,
                                            no_verify_cert=self.noverify)
            self._wbem_server = WBEMServer(self.conn)
        self.spinner.start()
        try:
            cmd()
        finally:
            self.spinner.stop()
