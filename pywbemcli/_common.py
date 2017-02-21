# Copyright TODO
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
from six.moves import input
import click

from pywbem import WBEMConnection, CIMInstanceName

from .config import DEFAULT_CONNECTION_TIMEOUT


# TODO This should become a special click option type rather than a
# separate function.
def fix_propertylist(propertylist):
    """
    Correct property list received from options.  Click options produces an
    empty list when there is no property list.  Pywbem requires None
    when there is no propertylist
    """
    if not propertylist:
        rtn = None
    else:
        rtn = propertylist
    return rtn


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
        instancename selected
      Exception:
        ValueError Exception if user elects to abort the selection
    """
    if not is_classname(objectname):
        raise click.ClickException('%s must be a classname' % objectname)
    instance_names = context.conn.EnumerateInstanceNames(objectname,
                                                         namespace)

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


def create_connection(server, namespace, user=None, password=None,
                      cert_file=None, key_file=None, ca_certs=None,
                      no_verify_cert=False):
    """
    Initiate a remote connection, via PyWBEM. Arguments for
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

    conn.debug = True
    return conn


def objects_sort(objects):
    """
    Sort CIMInstances or instance names
    """
    # TODO: Not implemented
    return objects


# TODO if namespace element, it should go back to context. I think.
# TODO: I do not like the name.  This is really cimnamespacename parser
def parse_wbem_uri(uri, namespace=None):
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


def parse_kv_pair(pair):
    """
    Parse a single key value pair separated by = and return the key
    and value components.
    The value may be empty
    """
    name, value = pair.partition("=")[::2]

    return name, value


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
    # TODO this is very simplistic and needs refinement.
    if isinstance(objects, (list, tuple)):
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
