# (C) Copyright 2023 IBM Corp.
# (C) Copyright 2023 Inova Development Inc.
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
Click Command definition for a docs command that calls a web browser with
the uri of the pywbemcli documentation.
"""

from __future__ import absolute_import, print_function

import webbrowser
import click

from .._click_extensions import GENERAL_OPTS_TXT

from .pywbemcli import cli
from .._options import add_options, help_option


@cli.command('docs', options_metavar=GENERAL_OPTS_TXT)
@add_options(help_option)
@click.pass_context
def help_docs(ctx):   # pylint: disable=unused-argument
    """
    Get pywbemtools documentation in web browser.

    EXPERIMENTAL

    Calls the current default web browser to display the current stable
    pywbemtools documentation in a new window.
    """
    docs_uri = "https://pywbemtools.readthedocs.io/en/stable/"
    try:
        webbrowser.open_new(docs_uri)
    except webbrowser.Error as we:
        raise click.ClickException("Web Browser failed {}".format(we))
