# (C) Copyright 2024 IBM Corp.
# (C) Copyright 2024 Inova Development Inc.
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
Path for the directory containing the connections file and
mock cache directory.  This is setup dynamically using an environment
variable for the name of the toplevel directory for these files or the
user home directory.
"""

import os
from click import Abort

# file suffix to be used for backup files for connection files when they
# are updated.
BAK_FILE_SUFFIX = '.bak'

# Env var that defines an alternate directory in which will be the home
# directory for the default connection file and mock cache directory.
# If env var PYWBEMCLI_ALT_HOME_DIR_ENVVAR is empty
# or does not exist user home directory (i.e. '~') is used
PYWBEMCLI_ALT_HOME_DIR_ENVVAR = 'PYWBEMCLI_ALT_HOME_DIR'

# Keep the following connections file definitions in sync with help text of
# the "--connections-file" option in pywbemcli.py and generaloptions.rst, and
# with the use of the base file name in several other .rst and .py files.

# Base file name of the default connections file
# The B08_* file name was used before pywbemcli 0.8.
CONNECTIONS_FILENAME = '.pywbemcli_connections.yaml'
B08_CONNECTIONS_FILENAME = 'pywbemcli_connection_definitions.yaml'

# Path name of default connections file directory.
# Dynamically builds the directory name for the directory that contains the
# default connections file and the mockcache directory based on an environment
# variable. Savea the result in variable DEFAULT_CONNECTIONS_DIR.
# Directory name is from the environment variable value or if the env var
# does not exist, the user home directory.
#
# This environment variable provides a tool to define an alternate
# location for the directory containing the default connection file and
# connection mockcache directory and is used in pywbemcli unit test.
# If no directory exists it builds an empty directory.
DEFAULT_CONNECTIONS_DIR = None

if os.getenv(PYWBEMCLI_ALT_HOME_DIR_ENVVAR):
    alt_home_dir_path = os.path.normpath(
        os.getenv(PYWBEMCLI_ALT_HOME_DIR_ENVVAR))
    # Windows makefile pads end of env var string.
    while alt_home_dir_path[-1] == " ":
        alt_home_dir_path = alt_home_dir_path[:-1]
    if os.path.exists(alt_home_dir_path):
        if os.path.isfile(alt_home_dir_path):
            raise Abort(
                f'Alternate files home path create: {alt_home_dir_path} '
                f'defined by envvar: {PYWBEMCLI_ALT_HOME_DIR_ENVVAR} failed. '
                "File with same name exists")
        DEFAULT_CONNECTIONS_DIR = alt_home_dir_path
    else:
        try:
            os.mkdir(alt_home_dir_path)
            DEFAULT_CONNECTIONS_DIR = alt_home_dir_path
        except OSError as oe:
            raise Abort(
                f'Alternate files home path create: {alt_home_dir_path} '
                f'defined by envvar: {PYWBEMCLI_ALT_HOME_DIR_ENVVAR} failed. '
                f'Exception: {oe}')
else:
    DEFAULT_CONNECTIONS_DIR = os.path.expanduser("~")

assert DEFAULT_CONNECTIONS_DIR is not None  # Future rmve after testing complete


# Path name of default connections file
# The B08_* path name was used before pywbemcli 0.8.
DEFAULT_CONNECTIONS_FILE = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                        CONNECTIONS_FILENAME)
B08_DEFAULT_CONNECTIONS_FILE = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                            B08_CONNECTIONS_FILENAME)

# Directory where mock cache files for named connections defined in the
# default connection file as mock connections (--mock-server general
# argument) are saved. In the same directory as default connection file.
MOCKCACHE_ROOT_DIR = os.path.join(DEFAULT_CONNECTIONS_DIR,
                                  '.pywbemcli_mockcache')
