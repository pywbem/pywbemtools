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
import io
import importlib
import traceback
import pywbem

from .._utils import pywbemcliwarn_explicit


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
    """
    modpath = get_modpath(file_path)
    if sys.version_info[0:2] >= (3, 5):
        spec = importlib.util.spec_from_file_location(modpath, file_path)
        module = importlib.util.module_from_spec(spec)

        # We cannot find out whether the script has a setup() function before
        # executing it, so we have to set the global variables for the old
        # setup approach in any case.
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
            pywbemcliwarn_explicit(
                "The support of mock scripts without setup() function is "
                "deprecated and will be removed in a future version.",
                DeprecatedSetupWarning, file_path, 0)

    else:  # Python 2.7 + 3.4
        with io.open(file_path, 'r', encoding='utf-8') as fp:
            file_source = fp.read()

        # Using compile+exec instead of just exec allows specifying the file
        # name, causing it to appear in any tracebacks.
        try:
            file_code = compile(file_source, file_path, 'exec')
        except Exception as exc:
            raise script_error(file_path, exc)

        # Poor man's approach to determining whether the mock script has a
        # setup() function:
        if 'setup' in file_code.co_names:
            raise SetupNotSupportedError(
                "On Python <3.5, mock scripts with setup() function are not "
                "supported")

        pywbemcliwarn_explicit(
            "The support of mock scripts without setup() function is "
            "deprecated and will be removed in a future version.",
            DeprecatedSetupWarning, file_path, 0)

        globalparams = {
            'CONN': conn,
            'SERVER': server,
            'VERBOSE': verbose,
            '__name__': modpath,
        }
        try:
            exec(file_code, globalparams, None)  # pylint: disable=exec-used
        except Exception as exc:
            raise script_error(file_path, exc)
        raise NotCacheable(
            "On Python <3.5, mock scripts cannot be cached")


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
    if sys.version_info[0:2] < (3, 5):
        raise NotCacheable(
            "On Python <3.5, mock scripts cannot be cached")

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
            "Mock script {} implements old setup approach with global "
            "variables".format(file_path))

    # This is just checked for additional safety - normally the execution
    # of mock script has failed due to missing global variables.
    # Note that variables from the mock script are set only after exec_module()
    if not hasattr(module, 'setup'):
        raise NotCacheable(
            "Mock script {} does not have a setup() function".format(file_path))


def script_error(file_path, exc):
    """
    Return a MockScriptError exception object with the current traceback in its
    exception message, ready to be displayed.
    """
    if isinstance(exc, pywbem.Error):
        new_exc = MockScriptError(
            "Mock script {} failed: {}".
            format(file_path, exc))
    else:
        tb = traceback.format_exception(*sys.exc_info())
        new_exc = MockScriptError(
            "Mock script {} failed:\n{}".
            format(file_path, "\n".join(tb)))
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
