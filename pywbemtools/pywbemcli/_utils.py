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
Utility Functions applicable across multiple components of pywbemcli.
"""

from __future__ import print_function, absolute_import

import os
import six
import click

from .config import USE_TERMINAL_WIDTH, DEFAULT_TABLE_WIDTH

__all__ = []

# Env var for overriding the terminal width
TERMWIDTH_ENVVAR = 'PYWBEMCLI_TERMWIDTH'

# Keep the following connections file definitions in sync with help text of
# the "--connections-file" option in pywbemcli.py and generaloptions.rst, and
# with the use of the base file name in several other .rst and .py files.

# Base file name of the connections file
# The B08_* file name was used before pywbemcli 0.8.
CONNECTIONS_FILENAME = '.pywbemcli_connections.yaml'
B08_CONNECTIONS_FILENAME = 'pywbemcli_connection_definitions.yaml'

# Path name of default connections file directory.
DEFAULT_CONNECTIONS_DIR = os.path.expanduser("~")

# Path name of default connections file
# The B08_* path name was used before pywbemcli 0.8.
DEFAULT_CONNECTIONS_FILE = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                        CONNECTIONS_FILENAME)
B08_DEFAULT_CONNECTIONS_FILE = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                            B08_CONNECTIONS_FILENAME)


def _ensure_bytes(obj):
    """
    If the input object is a string, make sure it is returned as a
    byte string, as follows:

    * If the input object already is a byte string, it is returned unchanged.
    * If the input string is a unicode string, it is encoded using UTF-8.
    * Otherwise, the input object was not a string and is returned unchanged.
    """
    if isinstance(obj, six.text_type):
        return obj.encode("utf-8")
    return obj


def _ensure_unicode(obj):
    """
    If the input object is a string, make sure it is returned as a
    :term:`unicode string`, as follows:

    * If the input object already is a :term:`unicode string`, it is returned
      unchanged.
    * If the input string is a :term:`byte string`, it is decoded using UTF-8.
    * Otherwise, the input object was not a string and is returned unchanged.

    Copied from pywbem
    """
    if isinstance(obj, six.binary_type):
        return obj.decode("utf-8")
    return obj


def _to_unicode(obj):
    """
    Convert the input binary string to a :term:`unicode string`.
    The input object must be a byte string.
    Use this if there is a previous test about the string type.

    Copies from pywbem
    """
    return obj.decode("utf-8")


def _eq_name(name1, name2):
    """
    Test two CIM names for equality.

    The comparison is performed case-insensitively.

    One or both of the names may be `None`; Two names that are `None` are
    considered equal.
    """
    if name1 is None:
        return name2 is None
    if name2 is None:
        return False
    return name1.lower() == name2.lower()


def formatwarning(message, category, filename, lineno, line=None):
    # pylint: disable=unused-argument
    """
    Replacement for warnings.formatwarning() that is patched in.
    """
    return "{}: {}\n".format(category.__name__, message)


def get_terminal_width():
    """
    Return the terminal width to use.

    Note: On Windows, click.get_terminal_size() results in terminal sizes of 0
    in some cases.
    """

    terminal_width = os.getenv(TERMWIDTH_ENVVAR, None)
    if terminal_width:
        try:
            terminal_width = int(terminal_width)
            return terminal_width
        except ValueError:
            pass

    if USE_TERMINAL_WIDTH:
        return click.get_terminal_size()[0]

    return DEFAULT_TABLE_WIDTH
