#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

"""
The following warnings are pywbemcli specific warnings that can be issued by
the pywbemcli.
"""

from pywbem import Warning as pywbemwarning


class InvalidConnectionFile(pywbemwarning):
    """
    Indicates that invalid connection file in startup of interactive mode.
    Warning to user that they cannot use some commands because of the
    lack of connection file.
    """
    pass


class TabCompletionError(pywbemwarning):
    """
    Indicates that invalid connection file in a tab completion.
    This warning is used in place of an exception for cmd line tab completion
    errors because exceptions should never be issued in tab-completion
    handling
    """
    pass
