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

# Generally we define common options each as a list to encorage using the
# add_options for each option specified in a command definition rather than
# gathering them together in in the @add_options specification. The only
# exception is the qualifier_filters that are ONLY used as a group.

#
# property_list option - Defined here because the option is used in
# multiple places in the command structure.
#
propertylist_option = [                      # pylint: disable=invalid-name
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
                      u'Default: Do not filter properties.')]

names_only_option = [                      # pylint: disable=invalid-name
    click.option('--no', '--names-only', 'names_only', is_flag=True,
                 required=False,
                 help=u'Retrieve only the object paths (names). '
                      u'Default: Retrieve the complete objects including '
                      u'object paths.')]

include_classorigin_instance_option = [         # pylint: disable=invalid-name
    click.option('--ico', '--include-classorigin', 'include_classorigin',
                 is_flag=True, required=False,
                 help=u'Include class origin information in the returned '
                      u'instance(s). '
                      u'Some servers may ignore this option. '
                      u'Default: Do not include class origin information.')]

include_classorigin_class_option = [            # pylint: disable=invalid-name
    click.option('--ico', '--include-classorigin', 'include_classorigin',
                 is_flag=True, required=False,
                 help=u'Include class origin information in the returned '
                      u'class(es). '
                      u'Default: Do not include class origin information.')]

namespace_option = [                     # pylint: disable=invalid-name
    click.option('-n', '--namespace', type=str,
                 required=False, metavar='NAMESPACE',
                 help=u'Namespace to use for this command, instead of the '
                      u'default namespace of the connection.')]

summary_option = [              # pylint: disable=invalid-name
    click.option('-s', '--summary', is_flag=True, required=False,
                 help=u'Show only a summary (count) of the objects.')]

verify_option = [              # pylint: disable=invalid-name
    click.option('-V', '--verify', is_flag=True, required=False,
                 help=u'Prompt for confirmation before performing a change, '
                      u'to allow for verification of parameters. '
                      u'Default: Do not prompt for confirmation.')]

multiple_namespaces_option = [              # pylint: disable=invalid-name
    click.option('-n', '--namespace', type=str, multiple=True,
                 required=False, metavar='NAMESPACE',
                 help=u'Add a namespace to the search scope. '
                      u'May be specified multiple times. '
                      u'Default: Search in all namespaces of the server.')]

#
#  The following options are implement the filtering of class request
#  operations to filter by selected class qualifiers. Note that these
#  options are NOT defined within a list since they are intended to be
#  used only as a list of all of the items
#
# pylint: disable=invalid-name
association_filter_option = \
    click.option('--association/--no-association',
                 default=None,
                 help=u'Filter the returned classes to return only indication '
                      u'classes (--association) or classes that are not '
                      u'associations(--no-association). If the option is not '
                      u'defined no filtering occurs')

indication_filter_option = \
    click.option('--indication/--no-indication',
                 default=None,
                 help=u'Filter the returned classes to return only indication '
                      u'classes (--indication) or classes that are not '
                      u'indications (--no-indication). If the option is not '
                      u'defined no filtering occurs')

experimental_filter_option = \
    click.option('--experimental/--no-experimental',
                 default=None,
                 help=u'Filter the returned classes to return only '
                      u'experimental classes (--experimental) or classes that '
                      u'are not experimental (--no-iexperimental). If the '
                      u'option is not defined no filtering occurs')

deprecated_filter_option = \
    click.option('--deprecated/--no-deprecated',
                 default=None,
                 help=u'Filter the returned classes to return only deprecated '
                      u'classes (--deprecated) or classes that are not '
                      u'deprecated (--no-deprecated). If the option is not '
                      u'defined no filtering occurs')

since_filter_option = \
    click.option('--since',
                 required=False, metavar='VERSION', type=str,
                 default=None,
                 help=u'Filter the returned classes to return only classes  '
                      u'with a version qualifier ge the supplied string. The '
                      u'string must define a version of the form M.N.V '
                      u'consistent the definitions of the VERSION qualifier.')

schema_filter_option = \
    click.option('--schema',
                 required=False, metavar='SCHEMA', type=str,
                 default=None,
                 help=u'Filter the returned classes to return only classes '
                      u'where the classname scheme component (characters '
                      u'before the "_" match the scheme provided.')


subclassof_filter_option = \
    click.option('--subclass-of',
                 required=False, metavar='CLASSNAME', type=str,
                 default=None,
                 help=u'Filter the returned classes to return only classes '
                      u'that are a subclass of the option value.')


leafclass_filter_option = \
    click.option('--leaf-classes', is_flag=True,
                 default=None,
                 help=u'Filter the returned classes to return only leaf '
                      u'(classes; classes with no subclass.')

# pylint: enable=invalid-name

# List of the class filter options that are common to multiple class commands
# Since the filters are in a list to allow them to be used individually, the
# first item of each list must be used for the combined defintion that can
# be use with add_options
# NOTE: Since these options are only used as a group then do not each need to be
# defined as a list above. However, we are trying to define all individual
# common options the same way (in a list).
class_filter_options = [              # pylint: disable=invalid-name
    association_filter_option,
    indication_filter_option,
    experimental_filter_option,
    deprecated_filter_option,
    since_filter_option,
    schema_filter_option,
    subclassof_filter_option,
    leafclass_filter_option
]

help_option = [              # pylint: disable=invalid-name
    click.help_option('-h', '--help', help=u'Show this help message.')]


def add_options(options):
    """
    Accumulate single or multiple options into a list. This list can be
    referenced as a click decorator @add_options(name_of_list)

    The list is reversed because of the way click processes options

    Since this is used with the click decorator add_options and subject to
    future variations of that decorator implementation.

    This is used by pywbemcli to implement common option definitions outside
    of each command definition and include them with the click decorator.

    Parameters:

      options: List of click.option definitions

    Returns:
        the callable _add_options which used by the decorator to do the
        reversal.

    """
    def _add_options(func):
        """
        Reverse options list, else if single item,
        make into a list.
        """
        for option in reversed(options):
            func = option(func)
        return func

    # Return the callable _add_options
    return _add_options
