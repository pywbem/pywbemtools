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
Pywbemtools command action functions that are common across multiple
tools.  The action method is called by the command processor defined by
a click command decorator.  These methods processing the parsed command.

"""

from __future__ import print_function, absolute_import

import webbrowser
import click


def docs_cmd_action(docs_url):
    """
    Action processor for docs command.  This function just calls a web browser
    with the docs_url provided. It is common because it is used by multiple
    pywbemtools.
    """
    try:
        webbrowser.open_new(docs_url)
    except webbrowser.Error as we:
        raise click.ClickException("Web Browser failed {}".format(we))
