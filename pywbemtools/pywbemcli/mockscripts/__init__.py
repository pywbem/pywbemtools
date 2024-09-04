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
Module for holding mock scripts.

This module provides its namespace as the parent namespace for any mock scripts.
The main objects in mock scripts are provider classes, and they need to exist
in a module namespace for pickle to be able to load the corresponding objects.
"""

import sys
import os
import importlib
import traceback
import pywbem

from ..._utils import pywbemtools_warn_explicit


class MockError(Exception):
    """
    Base class for all exceptions related to issues with the mock environment.
    """
    pass


class NotCacheable(MockError):
    """
    Indicates that the mock environment is not cacheable.
    """
    pass


class MockFileError(MockError):
    """
    Indicates an issue with a mock file.
    """
    pass


class MockScriptError(MockFileError):
    """
    Indicates that the mock script raised an exception. The exception message
    contains the traceback from the script.
    """
    pass


class MockMOFCompileError(MockFileError):
    """
    Indicates that a mock MOF file could not be compiled.
    """
    pass


class SetupNotSupportedError(MockError):
    """
    Indicates that a mock script with the setup() function was used on Python
    <3.5.

    On Python <3.5, only the old setup approach with global variables is
    supported.
    """
    pass


class DeprecatedSetupWarning(Warning):
    """
    Indicates the use of deprecated mock script setup.
    """
    pass


def setup_script(file_path, conn, server, verbose):
    """
    Import a mock script and perform its setup.

    Both types of mock script setup are supported:
    * The setup via calling setup(conn, server, verbose)
    * The deprecated setup via global variables CONN, SERVER, VERBOSE

    Raises:
      MockScriptError:
      SetupNotSupportedError (py<3.5): New-style setup in mock script not
        supported.
      NotCacheable (py<3.5): Mock environment is not cacheable.
      DeprecatedSetupWarning: Old-style setup mock script. This is a
        warning that this style is deprecated and will be removed in a
        future version of pywbemtools
    """
    modpath = get_modpath(file_path)
    spec = importlib.util.spec_from_file_location(modpath, file_path)
    module = importlib.util.module_from_spec(spec)

    # We cannot find out whether the script has a setup() function before
    # executing it, so we have to set the global variables for the old
    # setup approach in any case.
    # Deprecated: These global variables have been deprecated will be removed
    # in a future version of pywbemtools, They are retained because users may
    # have defined scripts that use this old-style interface.
    module.CONN = conn
    module.SERVER = server
    module.VERBOSE = verbose

    sys.modules[modpath] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise script_error(file_path, exc)

    if hasattr(module, 'setup'):
        try:
            module.setup(conn=conn, server=server, verbose=verbose)
        except Exception as exc:
            raise script_error(file_path, exc)
    else:
        pywbemtools_warn_explicit(
            "The support of mock scripts without setup() function is "
            "deprecated and will be removed in a future version.",
            DeprecatedSetupWarning, file_path, 0)


def import_script(file_path):
    """
    Import a mock script causing it to define the provider class(es), without
    performing setup activities such as registering its provider(s) or adding
    objects to the CIM repository of the mock connection.

    There are multiple reasons this function can raise NotCacheable. If
    that happens, the logic of the caller is to perform a complete build
    of the mock environment. During that build, script errors or the
    deprecation of the old setup approach will surface.

    Raises:
      NotCacheable
    """
    modpath = get_modpath(file_path)
    spec = importlib.util.spec_from_file_location(modpath, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[modpath] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        # Possible reasons:
        # - Error in mock script
        # - Mock script implements old setup approach with global variables,
        #   (but we intentionally did not set them in order not to perform
        #   the setup)
        # We report the reason was the old setup approach. If it was en error,
        # this will surface during rebuild.
        raise NotCacheable(
            f"Mock script {file_path} implements old setup approach with "
            "global variables")

    # This is just checked for additional safety - normally the execution
    # of mock script has failed due to missing global variables.
    # Note that variables from the mock script are set only after exec_module()
    if not hasattr(module, 'setup'):
        raise NotCacheable(
            f"Mock script {file_path} does not have a setup() function")


def script_error(file_path, exc):
    """
    Return a MockScriptError exception object with the current traceback in its
    exception message, ready to be displayed.
    """
    if isinstance(exc, pywbem.Error):
        new_exc = MockScriptError(f"Mock script {file_path} failed: {exc}")
    else:
        tb = traceback.format_exception(*sys.exc_info())
        fail_list = "\n".join(tb)
        new_exc = MockScriptError(
            f"Mock script {file_path} failed:\n{fail_list}")
    new_exc.__cause__ = None
    return new_exc


def get_modpath(file_path):
    """
    Return the dotted module path to be used for a mock script.
    """
    this_modpath = __name__  # Dotted module path of this module
    file_base = os.path.splitext(os.path.basename(file_path))[0]
    modpath = this_modpath + '.' + file_base
    return modpath
