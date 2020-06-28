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
Utility Functions applicable across multiple components of pywbemcli.
"""

from __future__ import print_function, absolute_import

import six
import click


__all__ = []


def _ensure_unicode(obj):
    """
    If the input object is a string, make sure it is returned as a
    :term:`unicode string`, as follows:

    * If the input object already is a :term:`unicode string`, it is returned
      unchanged.
    * If the input string is a :term:`byte string`, it is decoded using UTF-8.
    * Otherwise, the input object was not a string and is returned unchanged.

    Copied from pywbem
    """
    if isinstance(obj, six.binary_type):
        return obj.decode("utf-8")
    return obj


def _to_unicode(obj):
    """
    Convert the input binary string to a :term:`unicode string`.
    The input object must be a byte string.
    Use this if there is a previous test about the string type.

    Copies from pywbem
    """
    return obj.decode("utf-8")


def _eq_name(name1, name2):
    """
    Test two CIM names for equality.

    The comparison is performed case-insensitively.

    One or both of the names may be `None`; Two names that are `None` are
    considered equal.
    """
    if name1 is None:
        return name2 is None
    if name2 is None:
        return False
    return name1.lower() == name2.lower()


def deprecation_warning(msg, ctx_obj):
    """
    Display a deprecation warning on stderr, unless disabled via
    ctx_obj.deprecation_warnings.
    """
    if ctx_obj.deprecation_warnings:
        click.echo(msg, err=True)
