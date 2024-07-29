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
Defines Click options that are used for multiple pywbemcli subcommands.

The options are defined as a list to be suitable for the add_options decorator.
"""


import click

# pylint: disable=invalid-name

propertylist_option = [
    click.option('--pl', '--propertylist', 'propertylist', multiple=True,
                 type=str,
                 default=None, metavar='PROPERTYLIST',
                 help='Filter the properties included in the returned '
                      'object(s). '
                      'Multiple properties may be specified with either a '
                      'comma-separated list or by using the option multiple '
                      'times. Properties specified in this option that are '
                      'not in the object(s) will be ignored. '
                      'The empty string will include no properties. '
                      'Default: Do not filter properties.'),
]

names_only_option = [
    click.option('--no', '--names-only', 'names_only', is_flag=True,
                 required=False,
                 help='Retrieve only the object paths (names). '
                      'Default: Retrieve the complete objects including '
                      'object paths.'),
]

include_classorigin_instance_option = [
    click.option('--ico', '--include-classorigin', 'include_classorigin',
                 is_flag=True, required=False,
                 help='Include class origin information in the returned '
                      'instance(s). '
                      'Some servers may ignore this option. '
                      'Default: Do not include class origin information.'),
]

include_classorigin_class_option = [
    click.option('--ico', '--include-classorigin', 'include_classorigin',
                 is_flag=True, required=False,
                 help='Include class origin information in the returned '
                      'class(es). '
                      'Default: Do not include class origin information.'),
]

namespace_option = [
    click.option('-n', '--namespace', type=str,
                 required=False, metavar='NAMESPACE',
                 help='Namespace to use for this command, instead of the '
                      'default namespace of the connection.'),
]

multiple_namespaces_option_dflt_conn = [
    click.option('-n', '--namespace', type=str, multiple=True,
                 required=False, metavar='NAMESPACE(s)',
                 help='Namespace(s) to use for this command, instead of the '
                      'default connection namespace. May be specified '
                      'multiple times using either the option multiple times '
                      'and/or comma separated list. '
                      'Default: connection default namespace.'),
]

multiple_namespaces_option_dflt_all = [
    click.option('-n', '--namespace', type=str, multiple=True,
                 required=False, metavar='NAMESPACE(s)', default=[],
                 help='Namespace(s) for search scope. May be specified '
                      'multiple times using either the option multiple times '
                      'and/or comma separated list. '
                      'Default: Search in all namespaces of the server.'),
]

summary_option = [
    click.option('-s', '--summary', is_flag=True, required=False,
                 help='Show only a summary (count) of the objects.'),
]

verify_option = [
    click.option('-V', '--verify', is_flag=True, required=False,
                 help='Prompt for confirmation before performing a change, '
                      'to allow for verification of parameters. '
                      'Default: Do not prompt for confirmation.'),
]

object_order_option = [
    click.option('--object-order', is_flag=True, required=False,
                 help='Order the objects by object before namespace. Only '
                      'applies when multiple namespaces defined.'),
]

class_filter_options = [
    click.option('--association/--no-association',
                 default=None,
                 help='Filter the returned classes to return only indication '
                      'classes (--association) or classes that are not '
                      'associations(--no-association). If the option is not '
                      'defined no filtering occurs'),
    click.option('--indication/--no-indication',
                 default=None,
                 help='Filter the returned classes to return only indication '
                      'classes (--indication) or classes that are not '
                      'indications (--no-indication). If the option is not '
                      'defined no filtering occurs'),
    click.option('--experimental/--no-experimental',
                 default=None,
                 help='Filter the returned classes to return only '
                      'experimental classes (--experimental) or classes that '
                      'are not experimental (--no-iexperimental). If the '
                      'option is not defined no filtering occurs'),
    click.option('--deprecated/--no-deprecated',
                 default=None,
                 help='Filter the returned classes to return only deprecated '
                      'classes (--deprecated) or classes that are not '
                      'deprecated (--no-deprecated). If the option is not '
                      'defined no filtering occurs'),
    click.option('--since',
                 required=False, metavar='VERSION', type=str,
                 default=None,
                 help='Filter the returned classes to return only classes  '
                      'with a version qualifier ge the supplied string. The '
                      'string must define a version of the form M.N.V '
                      'consistent the definitions of the VERSION qualifier.'),
    click.option('--schema',
                 required=False, metavar='SCHEMA', type=str,
                 default=None,
                 help='Filter the returned classes to return only classes '
                      'where the classname scheme component (characters '
                      'before the "_" match the scheme provided.'),
    click.option('--subclass-of',
                 required=False, metavar='CLASSNAME', type=str,
                 default=None,
                 help='Filter the returned classes to return only classes '
                      'that are a subclass of the option value.'),
    click.option('--leaf-classes', is_flag=True,
                 default=None,
                 help='Filter the returned classes to return only leaf '
                      '(classes; classes with no subclass.'),
]

# pylint: enable=invalid-name
