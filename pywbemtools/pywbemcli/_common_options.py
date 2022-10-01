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

from __future__ import absolute_import, print_function

import click

# pylint: disable=invalid-name

propertylist_option = [
    click.option('--pl', '--propertylist', 'propertylist', multiple=True,
                 type=str,
                 default=None, metavar='PROPERTYLIST',
                 help=u'Filter the properties included in the returned '
                      u'object(s). '
                      u'Multiple properties may be specified with either a '
                      u'comma-separated list or by using the option multiple '
                      u'times. Properties specified in this option that are '
                      u'not in the object(s) will be ignored. '
                      u'The empty string will include no properties. '
                      u'Default: Do not filter properties.'),
]

names_only_option = [
    click.option('--no', '--names-only', 'names_only', is_flag=True,
                 required=False,
                 help=u'Retrieve only the object paths (names). '
                      u'Default: Retrieve the complete objects including '
                      u'object paths.'),
]

include_classorigin_instance_option = [
    click.option('--ico', '--include-classorigin', 'include_classorigin',
                 is_flag=True, required=False,
                 help=u'Include class origin information in the returned '
                      u'instance(s). '
                      u'Some servers may ignore this option. '
                      u'Default: Do not include class origin information.'),
]

include_classorigin_class_option = [
    click.option('--ico', '--include-classorigin', 'include_classorigin',
                 is_flag=True, required=False,
                 help=u'Include class origin information in the returned '
                      u'class(es). '
                      u'Default: Do not include class origin information.'),
]

namespace_option = [
    click.option('-n', '--namespace', type=str,
                 required=False, metavar='NAMESPACE',
                 help=u'Namespace to use for this command, instead of the '
                      u'default namespace of the connection.'),
]

multiple_namespaces_option_dflt_conn = [
    click.option('-n', '--namespace', type=str, multiple=True,
                 required=False, metavar='NAMESPACE(s)',
                 help=u'Namespace(s) to use for this command, instead of the '
                      u'default connection namespace. May be specified '
                      u'multiple times using either the option multiple times '
                      u'and/or comma separated list. '
                      u'Default: connection default namespace.'),
]

multiple_namespaces_option_dflt_all = [
    click.option('-n', '--namespace', type=str, multiple=True,
                 required=False, metavar='NAMESPACE(s)', default=[],
                 help=u'Namespace(s) for search scope. May be specified '
                      u'multiple times using either the option multiple times '
                      u'and/or comma separated list. '
                      u'Default: Search in all namespaces of the server.'),
]

summary_option = [
    click.option('-s', '--summary', is_flag=True, required=False,
                 help=u'Show only a summary (count) of the objects.'),
]

verify_option = [
    click.option('-V', '--verify', is_flag=True, required=False,
                 help=u'Prompt for confirmation before performing a change, '
                      u'to allow for verification of parameters. '
                      u'Default: Do not prompt for confirmation.'),
]

object_order_option = [
    click.option('--object-order', is_flag=True, required=False,
                 help=u'Order the objects by object before namespace. Only '
                      u'applies when multiple namespaces defined.'),
]

class_filter_options = [
    click.option('--association/--no-association',
                 default=None,
                 help=u'Filter the returned classes to return only indication '
                      u'classes (--association) or classes that are not '
                      u'associations(--no-association). If the option is not '
                      u'defined no filtering occurs'),
    click.option('--indication/--no-indication',
                 default=None,
                 help=u'Filter the returned classes to return only indication '
                      u'classes (--indication) or classes that are not '
                      u'indications (--no-indication). If the option is not '
                      u'defined no filtering occurs'),
    click.option('--experimental/--no-experimental',
                 default=None,
                 help=u'Filter the returned classes to return only '
                      u'experimental classes (--experimental) or classes that '
                      u'are not experimental (--no-iexperimental). If the '
                      u'option is not defined no filtering occurs'),
    click.option('--deprecated/--no-deprecated',
                 default=None,
                 help=u'Filter the returned classes to return only deprecated '
                      u'classes (--deprecated) or classes that are not '
                      u'deprecated (--no-deprecated). If the option is not '
                      u'defined no filtering occurs'),
    click.option('--since',
                 required=False, metavar='VERSION', type=str,
                 default=None,
                 help=u'Filter the returned classes to return only classes  '
                      u'with a version qualifier ge the supplied string. The '
                      u'string must define a version of the form M.N.V '
                      u'consistent the definitions of the VERSION qualifier.'),
    click.option('--schema',
                 required=False, metavar='SCHEMA', type=str,
                 default=None,
                 help=u'Filter the returned classes to return only classes '
                      u'where the classname scheme component (characters '
                      u'before the "_" match the scheme provided.'),
    click.option('--subclass-of',
                 required=False, metavar='CLASSNAME', type=str,
                 default=None,
                 help=u'Filter the returned classes to return only classes '
                      u'that are a subclass of the option value.'),
    click.option('--leaf-classes', is_flag=True,
                 default=None,
                 help=u'Filter the returned classes to return only leaf '
                      u'(classes; classes with no subclass.'),
]

# pylint: enable=invalid-name
