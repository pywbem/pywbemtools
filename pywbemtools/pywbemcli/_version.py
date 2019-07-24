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
#


"""
Version of the pywbemcli package and check for valid python versions.

The actual package version is deterrmined through pbr package through
git tag information  and is only referenced here to create the __version__
variable.
"""
import sys
import pbr.version

__all__ = ['__version__']


#: Version of the pywbemcli package, as a :term:`string`.
#:
#: Possible formats for the version string are:
#:
#: * "M.N.U.dev0": During development of future M.N.U release (not released to
#:   PyPI)
#: * "M.N.U.rcX": Release candidate X of future M.N.U release (not released to
#:   PyPI)
#: * "M.N.U": The final M.N.U release
__version__ = pbr.version.VersionInfo('pywbemtools').release_string()


# Check supported Python versions
_PYTHON_M = sys.version_info[0]
_PYTHON_N = sys.version_info[1]
if _PYTHON_M == 2 and _PYTHON_N < 7:
    raise RuntimeError('On Python 2, pywbemtools requires Python 2.7')
if _PYTHON_M == 3 and _PYTHON_N < 4:
    raise RuntimeError('On Python 3, pywbemtools requires Python 3.4 or higher')
