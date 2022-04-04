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
Utility functions applicable across multiple pywbemtools commands.
"""

from __future__ import print_function, absolute_import

import os
import io
import shutil
import warnings
import inspect
from datetime import datetime
import mock
import six
import click

__all__ = []

# Env var for overriding the terminal width
TERMWIDTH_ENVVAR = 'PYWBEMTOOLS_TERMWIDTH'

# If True, the table formatter uses the terminal width as the maximum width
# of a table. If False it uses the DEFAULT_TABLE_WIDTH config variable. This
# sets the maximum width of table output. The table formatter tries to
# build any table output within this character width.
USE_TERMINAL_WIDTH = True

# Default maximum character width of tables if USE_TERMINAL_WIDTH is NOT set.
# If this variable is an integer, that is the maximum width. If None, tables
# are output with no limit on width.
DEFAULT_TABLE_WIDTH = 150

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


def ensure_bytes(obj):
    """
    If the input object is a string, make sure it is returned as a Byte string,
    as follows:

    * If the input object already is a Byte string, it is returned unchanged.
    * If the input object is a Unicode string, it is converted to a Byte string
      using the UTF-8 encoding.
    * Otherwise, the input object was not a string and is returned unchanged.
    """
    if isinstance(obj, six.text_type):
        return obj.encode("utf-8")
    return obj


def ensure_unicode(obj):
    """
    If the input object is a string, make sure it is returned as a Unicode
    string, as follows:

    * If the input object already is a Unicode string, it is returned unchanged.
    * If the input object is a Byte string, it is converted to a Unicode string
      using the UTF-8 encoding.
    * Otherwise, the input object was not a string and is returned unchanged.
    """
    if isinstance(obj, six.binary_type):
        return obj.decode("utf-8")
    return obj


def to_unicode(obj):
    """
    Convert the input Byte string to a Unicode string.

    The input object must be a Byte string.
    """
    return obj.decode("utf-8")


def _formatwarning(message, category, filename, lineno, line=None):
    # pylint: disable=unused-argument
    """
    Replacement for warnings.formatwarning() that is monkey patched in.
    """
    return "{}: {}\n".format(category.__name__, message)


def pywbemtools_warn(*args, **kwargs):
    """
    Pywbemtools version of the warnings.warn() function,
    with replaced formatting.
    """
    with mock.patch.object(warnings, 'formatwarning', _formatwarning):
        warnings.warn(*args, **kwargs)


def pywbemtools_warn_explicit(*args, **kwargs):
    """
    Pywbemtools version of the warnings.warn_explicit() function,
    with replaced formatting.
    """
    with mock.patch.object(warnings, 'formatwarning', _formatwarning):
        warnings.warn_explicit(*args, **kwargs)


def get_terminal_width():
    """
    Return the terminal width to use, as an integer.
    """

    terminal_width = os.getenv(TERMWIDTH_ENVVAR, None)
    if terminal_width:
        try:
            terminal_width = int(terminal_width)
            return terminal_width
        except ValueError:
            pass

    if USE_TERMINAL_WIDTH:
        # We first try shutil.get_terminal_size() which was added in Python 3.3.
        # Click 8.0 has deprecated click.get_terminal_size() and issues a
        # DeprecationWarning, but on Python 2.7, Click is pinned to <8.0, so we
        # can use click.get_terminal_size() without triggering the
        # DeprecationWarning.
        try:
            ts = shutil.get_terminal_size()
        except AttributeError:
            ts = click.get_terminal_size()  # pylint: disable=no-member
        return ts[0]

    return DEFAULT_TABLE_WIDTH


def debug_log(msg):
    """
    Write a debug log entry for debugging test functions to a file named
    "debug.log".

    The timestamp and name of the calling function are automatically added
    to the message.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    caller = inspect.stack()[1][3]
    with io.open("debug.log", "a", encoding='utf-8') as fp:
        fp.write("{} {}: {}\n".format(timestamp, caller, msg))
