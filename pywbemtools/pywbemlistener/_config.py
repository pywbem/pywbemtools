# (C) Copyright 2021 Inova Development Inc.
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
Common constants for pywbemlistener.
"""

# Verbosity levels that enable certain types of messages
VERBOSE_SETTINGS = 1
VERBOSE_PROCESSES = 2

# Verbosity help text, by level
VERBOSE_1_HELP = u'Display indication processing settings'
VERBOSE_2_HELP = u'Display interactions between start and run commands'

# Global flag that is set if verbosity >= VERBOSE_PROCESSES
VERBOSE_PROCESSES_ENABLED = False

# Environment variables that influence the behavior of the pywbemlistener
# command, mostly they define defaults that can be overridden by general
# command line options.
PYWBEMLISTENER_KEYFILE_ENVVAR = 'PYWBEMLISTENER_KEYFILE'
PYWBEMLISTENER_CERTFILE_ENVVAR = 'PYWBEMLISTENER_CERTFILE'
PYWBEMLISTENER_LOGDIR_ENVVAR = 'PYWBEMLISTENER_LOGDIR'
PYWBEMLISTENER_PDB_ENVVAR = 'PYWBEMLISTENER_PDB'
