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
Common Functions applicable across multiple components of pywbemcli
"""

from __future__ import absolute_import, unicode_literals

import click_spinner

from ._pywbem_server import PywbemServer

# The current pywbem server object for subcommands.
PYWBEM_SERVER_OBJ = None

# dictionary of defined servers. They key is the names for each
# server.
PYWBEM_SERVERS = {}


class ContextObj(object):
    """
        Manage the click context object. This is the object that communicates
        between the cli commands and command groups. It contains the
        information that is common to the multiple commands
    """
    # pylint: disable=unused-argument
    def __init__(self, ctx, pywbem_server, output_format, verbose):

        self._pywbem_server = pywbem_server
        self._output_format = output_format
        self._verbose = verbose
        self._spinner = click_spinner.Spinner()
        if not isinstance(pywbem_server, PywbemServer):
            print('Error, %s' % pywbem_server)

    def __repr__(self):
        return 'ContextObj(pywbem_server=%s, outputformat=%s, verbose=%s' % \
               (self.pywbem_server, self.output_format, self.verbose)

    @property
    def output_format(self):
        """
        :term:`string`: Output format to be used.
        """
        return self._output_format

    @property
    def conn(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMConnection to be used for requests.
        """
        # This is created in wbemserver and retained there.
        return self._pywbem_server.conn

    @property
    def wbem_server(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMServer instance to be used for
        requests This is maintained in the pywbem_server object.
        """
        return self._pywbem_server.wbem_server

    @property
    def pywbem_server(self):
        """
        :class:`~pywbem.WBEMConnection` WBEMServer instance to be used for
        requests.
        """
        return self._pywbem_server

    @property
    def spinner(self):
        """
        :class:`~click_spinner.Spinner` object.
        """
        return self._spinner

    @property
    def verbose(self):
        """
        :bool:` '~click.verbose.
        """
        return self._verbose

    def set_connection(self, connection):
        """ Set the connection parameter as the current connection object"""
        global PYWBEM_SERVER_OBJ
        PYWBEM_SERVER_OBJ = connection

    def execute_cmd(self, cmd):
        """
        Call the cmd executor defined by cmd with the spinner. If the
        WBEMServer object has not been created it is created and the
        result stored in global storage so that this wbem server can be
        used for interactive commands.
        """
        self.connect_wbem_server()
        self.spinner.start()
        try:
            cmd()
        finally:
            self.spinner.stop()

    def connect_wbem_server(self):
        """
        If the wbem server has not been connected yet, connect it. The
        wbemserver object is saved both in the context and as a GLOBAL
        This global is used to determine that the server has been connected.
        TODO: Rather than a global, we should be the wbemserver into the
        parent probably.

        Both the WBEMConnection and WBEMServer objects are established
        at this point since the cost of doing the WBEMServer object is low.
        The existence of the WBEMSerer object in the global is the flag that
        this server connection has been established already.

        TODO: We should probably move this logic to the first place a
        connection is actually established so that if we have not-password
        commands in the environment they do not force the password request.
        Logical would be the first time the conn or wbem_server property is
        used in pywbem_server.

        """
        # TODO investigate putting this into parent context instead of global

        global PYWBEM_SERVER_OBJ  # pylint: disable=global-statement
        if PYWBEM_SERVER_OBJ is None:
            # get the password if it is required.  This may involve a
            # prompt. Ed delay the password get as long as possible so it
            # does not become part of calls that do not need it.

            self._pywbem_server.get_password(self)

            self._pywbem_server.create_connection()

            PYWBEM_SERVER_OBJ = self._pywbem_server
            if not isinstance(self.pywbem_server, PywbemServer):
                print('Error 3 , %s' % self.pywbem_server)
        else:
            self._pywbem_server = PYWBEM_SERVER_OBJ
            if not isinstance(self.pywbem_server, PywbemServer):
                print('Error 4, %s' % self.pywbem_server)
