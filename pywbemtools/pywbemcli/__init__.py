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
Pywbemcli is a command line WBEM client that uses pywbem as its communication
interface with WBEM Servers. It is written in pure Python and supports Python 2
and Python 3.
"""

from __future__ import absolute_import

import sys

from ._cmd_class import *       # noqa: F403,F401
from ._cmd_instance import *       # noqa: F403,F401
from ._cmd_qualifier import *       # noqa: F403,F401
from ._cmd_server import *       # noqa: F403,F401
from ._cmd_connection import *   # noqa: F403,F401
from ._common import *   # noqa: F403,F401
from ._pywbem_server import *   # noqa: F403,F401
from ._context_obj import *   # noqa: F403,F401
from ._connection_repository import *   # noqa: F403,F401
from .pywbemcli import *       # noqa: F403,F401
from .config import *  # noqa: F403,F401
from ._pywbemcli_operations import *  # noqa: F403,F401

from ._version import __version__  # noqa: F401

_python_m = sys.version_info[0]  # pylint: disable=invalid-name
_python_n = sys.version_info[1]  # pylint: disable=invalid-name
if _python_m == 2 and _python_n < 7:
    raise RuntimeError('On Python 2, pywbem requires Python 2.7 or higher')
if _python_m == 3 and _python_n < 4:
    raise RuntimeError('On Python 3, pywbem requires Python 3.4 or higher')
