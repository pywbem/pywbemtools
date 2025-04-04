# (C) Copyright 2020 IBM Corp.
# (C) Copyright 2020 Inova Development Inc.
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
Version of the pywbemtools package.
"""

try:
    from ._version_scm import version, version_tuple
except ImportError:
    version = "unknown"
    version_tuple = ("unknown")

__all__ = ['__version__', '__version_tuple__']

#: The full version of this package including any development levels, as a
#: string.
#:
#: Possible formats for this version string are:
#:
#: * "M.N.Pa1.dev7+g1234567": A not yet released version M.N.P
#: * "M.N.P": A released version M.N.P
__version__ = version

#: The full version of this package including any development levels, as a
#: tuple of version items, converted to integer where possible.
#:
#: Possible formats for this version string are:
#:
#: * (M, N, P, 'a1', 'dev7', 'g1234567'): A not yet released version M.N.P
#: * (M, N, P): A released version M.N.P
__version_tuple__ = version_tuple
