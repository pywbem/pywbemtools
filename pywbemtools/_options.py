# (C) Copyright 2017 IBM Corp.
# (C) Copyright 2017-2021 Inova Development Inc.
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
Functions that help defining command line options with Click, and options that
are common across pywbemtools commands.
"""

from __future__ import absolute_import, print_function

import click


help_option = [  # pylint: disable=invalid-name
    click.help_option('-h', '--help', help=u'Show this help message.'),
]


def add_options(options):
    """
    Decorator that adds a list of command line options to a Click command or
    group.

    The list is processed in reversed order because of the way Click processes
    options.

    Parameters:

      options (list): List of click.option objects defining the options to add.
    """

    def _add_options(func):
        """
        Reverse options list, else if single item,
        make into a list.
        """
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def validate_required_arg(value, metavar):
    """
    Validate that a required CLI argument is present, and raise a usage error
    otherwise.

    This function is used for required arguments in cases where the command
    has a --help-... option, so that the option can be used without specifying
    the required arguments. Just using is_eager on the option is not sufficient
    for that.
    """
    if not value:
        raise click.UsageError(
            "Missing argument '{}'.".format(metavar),
            click.get_current_context())
