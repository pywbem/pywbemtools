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
Click context object for the pybemlistener command.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import click_spinner


class ContextObj(object):
    # pylint: disable=useless-object-inheritance, too-many-instance-attributes
    """
    Click context object for the pybemlistener command.

    This object is attached to the Click context, and is used as follows:
    - Contains all general options for use by command functions.
    - Serves as the central object for executing command functions.
    - Has support for starting and stopping the Click spinner.
    """

    spinner_envvar = 'PYWBEMLISTENER_SPINNER'

    def __init__(self, output_format, logdir, verbose, pdb, warn):
        """
        Parameters:

          output_format (:term:`string` or `None`):
            Value of --output-format general option, or `None` if not specified.

          logdir (:term:`string` or `None`):
            Value of --logdir general option, or `None` if not specified.

          verbose (int):
            Verbosity. See VERBOSE_* constants for a definition.

          pdb (:class:`py:bool`):
            Indicates whether the --pdb general option was specified.

          warn (:class:`py:bool`):
            Indicates whether the --warn general option was specified.
        """

        self._output_format = output_format
        self._logdir = logdir
        self._verbose = verbose
        self._pdb = pdb
        self._warn = warn

        self._spinner_enabled = None  # Deferred init in getter
        self._spinner_obj = click_spinner.Spinner()

    def __repr__(self):
        return 'ContextObj(at {:08x}, output_format={s.output_format}, ' \
               'logdir={s.logdir}, verbose={s.verbose}, pdb={s.pdb}, ' \
               'warn={s.warn}, spinner_enabled={s.spinner_enabled}' \
               .format(id(self), s=self)

    @property
    def output_format(self):
        """
        :term:`string`: String defining the output format requested.  This may
        be `None` meaning that the default format should be used or may be
        one of the values in the TABLE_FORMATS variable.
        """
        return self._output_format

    @property
    def logdir(self):
        """
        :term:`string`: Path name of log directory for the 'run' command,
        or `None` for no logging.
        """
        return self._logdir

    @property
    def verbose(self):
        """
        int: Verbosity. See VERBOSE_* constants for a definition.
        """
        return self._verbose

    @property
    def pdb(self):
        """
        bool: Indicates whether to break in the debugger.
        """
        return self._pdb

    @property
    def warn(self):
        """
        bool: Indicates whether to enable Python warnings.
        """
        return self._warn

    @property
    def spinner_enabled(self):
        """
        :class:`py:bool`: Indicates and controls whether the spinner is enabled.

        If the spinner is enabled, subcommands will display a spinning wheel
        while waiting for completion.

        This attribute can be modified.

        The initial state of the spinner is enabled, but it can be disabled by
        setting the {0} environment variable to 'false', '0', or the empty
        value.
        """.format(self.spinner_envvar)

        # Deferred initialization
        if self._spinner_enabled is None:
            value = os.environ.get(self.spinner_envvar, None)
            if value is None:
                # Default if not set
                self._spinner_enabled = True
            elif value == '0' or value == '' or value.lower() == 'false':
                self._spinner_enabled = False
            else:
                self._spinner_enabled = True

        return self._spinner_enabled

    @spinner_enabled.setter
    def spinner_enabled(self, enabled):
        """Setter method; for a description see the getter method."""
        self._spinner_enabled = enabled

    def spinner_start(self):
        """
        Start the spinner, if the spinner is enabled.
        """
        if self.spinner_enabled:
            self._spinner_obj.start()

    def spinner_stop(self):
        """
        Stop the spinner, if the spinner is enabled.
        """
        if self.spinner_enabled:
            self._spinner_obj.stop()

    def execute_cmd(self, cmd):
        """
        Call the command function for a command, after enabling the spinner
        (except when in debug mode) and after entering debug mode if desired.
        """
        if not self.pdb:
            self.spinner_start()
        try:
            if self.pdb:
                import pdb  # pylint: disable=import-outside-toplevel
                pdb.set_trace()  # pylint: disable=forgotten-debug-statement

            cmd()  # The command function for the pywbemlistener command

        finally:
            if not self.pdb:
                self.spinner_stop()
