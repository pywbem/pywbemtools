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
Test some errors with real servers.
"""

from __future__ import absolute_import, print_function

import re

# pylint: disable=unused-import
from .utils import server_url  # noqa: F401
# pylint: enable=unused-import
from ..unit.utils import execute_command


def test_resourcewarning_interactive(server_url):  # noqa: F811
    # pylint: disable=redefined-outer-name
    """
    Test that ending an interactive session to a real WBEM server does not
    cause any ResourceWarnings (e.g. about unclosed sockets).
    """

    def details(what, expected=None):
        "Return a string with details about the unexpected command result"
        msg = """
Unexpected {} (expected: {}):
rc={}
stdout:
{}
stderr:
{}
""".format(what, expected, rc, stdout, stderr)
        return msg

    # Note: We want to see ResourceWarning but not other warnings, particularly
    # not DeprecationWarning which is issued on Python 2.7. Using the 'env'
    # parameter to set PYTHONWARNINGS does not work because PYTHONWARNINGS is
    # disabled in execute_command(). So we use '--warn' and manually process
    # the warnings that are issued.
    rc, stdout, stderr = execute_command(
        'pywbemcli',
        ['-s', server_url, '--no-verify', '--warn'],
        stdin='server brand')

    out_lines = stdout.strip('\n')
    out_lines = [] if out_lines == '' else out_lines.split('\n')
    err_lines = stderr.strip('\n')
    err_lines = [] if err_lines == '' else err_lines.split('\n')
    reswarn_lines = []
    for line in err_lines:
        if 'ResourceWarning:' in line:
            reswarn_lines.append(line)

    assert rc == 0, details('rc')
    assert len(reswarn_lines) == 0, details('stderr', '0 ResourceWarning lines')
    assert len(out_lines) == 2, details('stdout', '2 stdout lines')
    assert re.match(r"Enter 'help repl' for help", out_lines[0]), \
        details('stdout')
    assert re.match(r"OpenPegasus", out_lines[1]), details('stdout')
