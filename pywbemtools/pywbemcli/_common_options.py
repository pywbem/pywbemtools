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
from __future__ import absolute_import

import click

#
# property_list option - Defined here because the option is used in
# multiple places in the command structure.
#
propertylist_option = [                      # pylint: disable=invalid-name
    click.option('--pl', '--propertylist', multiple=True, type=str,
                 default=None, metavar='<property name>',
                 help='Define a propertylist for the request. If option '
                      'not specified a Null property list is created and the '
                      'server returns all properties. Multiple properties may '
                      'be defined with either a comma separated list or by '
                      'using the option multiple times. '
                      '(ex: -p pn1 -p pn22 or -p pn1,pn2). '
                      'If defined as empty string the server should return no '
                      'properties.')]

names_only_option = [                      # pylint: disable=invalid-name
    click.option('--no', '--names-only', is_flag=True, required=False,
                 help='Retrieve only the returned object names.')]

sort_option = [                            # pylint: disable=invalid-name
    click.option('--so', '--sort', is_flag=True, required=False,
                 help='Sort into alphabetical order by classname.')]

includeclassorigin_option = [            # pylint: disable=invalid-name
    click.option('--ico', '--include-classorigin', is_flag=True,
                 required=False,
                 help='Include class origin information in the returned '
                      'class(es). '
                      'Default: Do not include class origin information.')]

namespace_option = [                     # pylint: disable=invalid-name
    click.option('-n', '--namespace', type=str,
                 required=False, metavar='NAMESPACE',
                 help='Namespace to use for this command, instead of the '
                      'default namespace of the connection.')]

summary_objects_option = [              # pylint: disable=invalid-name
    click.option('-s', '--summary', is_flag=True, required=False,
                 help='Return only summary of objects (count).')]

verify_option = [              # pylint: disable=invalid-name
    click.option('-V', '--verify', is_flag=True, required=False,
                 help='Prompt for confirmation before performing a change, '
                      'to allow for verification of parameters. '
                      'Default: Do not prompt for confirmation.')]


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
