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
Defines click options that are used for multiple scommands and that have
the same definition throughout the environment.  This allows the characteristics
and help to be defined once and used multiple times.
"""

from __future__ import absolute_import, print_function

import click

#
# property_list option - Defined here because the option is used in
# multiple places in the command structure.
#
propertylist_option = [                      # pylint: disable=invalid-name
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
                      'Default: Do not filter properties.')]

names_only_option = [                      # pylint: disable=invalid-name
    click.option('--no', '--names-only', 'names_only', is_flag=True,
                 required=False,
                 help='Retrieve only the object paths (names). '
                      'Default: Retrieve the complete objects including '
                      'object paths.')]

include_classorigin_instance_option = [         # pylint: disable=invalid-name
    click.option('--ico', '--include-classorigin', 'include_classorigin',
                 is_flag=True, required=False,
                 help='Include class origin information in the returned '
                      'instance(s). '
                      'Some servers may ignore this option. '
                      'Default: Do not include class origin information.')]

include_classorigin_class_option = [            # pylint: disable=invalid-name
    click.option('--ico', '--include-classorigin', 'include_classorigin',
                 is_flag=True, required=False,
                 help='Include class origin information in the returned '
                      'class(es). '
                      'Default: Do not include class origin information.')]

namespace_option = [                     # pylint: disable=invalid-name
    click.option('-n', '--namespace', type=str,
                 required=False, metavar='NAMESPACE',
                 help='Namespace to use for this command, instead of the '
                      'default namespace of the connection.')]

summary_option = [              # pylint: disable=invalid-name
    click.option('-s', '--summary', is_flag=True, required=False,
                 help='Show only a summary (count) of the objects.')]

verify_option = [              # pylint: disable=invalid-name
    click.option('-V', '--verify', is_flag=True, required=False,
                 help='Prompt for confirmation before performing a change, '
                      'to allow for verification of parameters. '
                      'Default: Do not prompt for confirmation.')]

multiple_namespaces_option = [              # pylint: disable=invalid-name
    click.option('-n', '--namespace', type=str, multiple=True,
                 required=False, metavar='NAMESPACE',
                 help='Add a namespace to the search scope. '
                      'May be specified multiple times. '
                      'Default: Search in all namespaces of the server.')]

#
#  The following options are implement the filtering of class request
#  operations to filter by selected class qualifiers
#
association_filter_option = [              # pylint: disable=invalid-name
    click.option('--association/--no-association',
                 default=None,
                 help='Filter the returned classes to return only indication '
                      'classes (--association) or classes that are not '
                      'associations(--no-association). If the option is not '
                      'defined no filtering occurs')]

indication_filter_option = [              # pylint: disable=invalid-name
    click.option('--indication/--no-indication',
                 default=None,
                 help='Filter the returned classes to return only indication '
                      'classes (--indication) or classes that are not '
                      'indications (--no-indication). If the option is not '
                      'defined no filtering occurs')]

experimental_filter_option = [              # pylint: disable=invalid-name
    click.option('--experimental/--no-experimental',
                 default=None,
                 help='Filter the returned classes to return only experimental '
                      'classes (--experimental) or classes that are not '
                      'experimental (--no-iexperimental). If the option is not '
                      'defined no filtering occurs')]

help_option = [              # pylint: disable=invalid-name
    click.help_option('-h', '--help', help='Show this help message.')]


def add_options(options):
    """
    Accumulate multiple options into a list. This list can be referenced as
    a click decorator @att_options(name_of_list)

    The list is reversed because of the way click processes options

    Parameters:

      options: list of click.option definitions

    Returns:
        Reversed list

    """
    def _add_options(func):
        """ Reverse options list"""
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options
