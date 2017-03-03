# Copyright  2017 IBM Corp. and Inova Development Inc.
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

# There are submodules, but clients shouldn't need to know about them.
# Importing just this module is enough.
# These are explicitly safe for 'import *'

"""
Version of the pywbemcli package.
"""

#: Version of the pywbemcli package, as a :term:`string`.
#:
#: Possible formats for the version string are:
#:
#: * "M.N.U.dev0": During development of future M.N.U release (not released to
#:   PyPI)
#: * "M.N.U.rcX": Release candidate X of future M.N.U release (not released to
#:   PyPI)
#: * "M.N.U": The final M.N.U release
__version__ = '0.5.0.dev0'
