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
#

"""
This module implements a user-defined provider that rejects the deletion
of instances, for test purposes.
"""

from pywbem import CIMError, CIM_ERR_FAILED
from pywbem_mock import InstanceWriteProvider


class CIM_Foo_sub_sub_RejectDeleteProvider(InstanceWriteProvider):
    """
    Implements a user defined provider for the class CIM_Foo_sub_sub where
    DeleteInstance is rejected with CIM_ERR_FAILED.
    """

    provider_classnames = 'CIM_Foo_sub_sub'

    def DeleteInstance(self, InstanceName):
        """
        Reject the deletion of an instance of the class.
        """
        raise CIMError(
            CIM_ERR_FAILED,
            "Deletion of {} instances is rejected".
            format(self.provider_classnames))


def setup(conn, server, verbose):
    # pylint: disable=unused-argument
    """
    Setup for this mock script.

    Parameters:
      conn (FakedWBEMConnection): Connection
      server (PywbemServer): Server
      verbose (bool): Verbose flag
    """
    provider = CIM_Foo_sub_sub_RejectDeleteProvider(conn.cimrepository)
    conn.register_provider(provider, 'root/cimv2', verbose=verbose)
