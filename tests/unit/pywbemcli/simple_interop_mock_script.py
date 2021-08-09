"""
Test mock script that installs the pywbem provided namespace provider
CIMNamespaceProvider and the simple Interop and user namespace model
defined in simple_interop_mock_model.mof.

This mock script uses 'new-style' setup for Python >=3.5 and 'old-style' setup
otherwise, and is therefore useable for all supported Python versions.
On Python <3.5, the tests using this script must be run from the repo main
directory.
"""

import sys
import os
import six
import pywbem_mock

# Namespaces set up by this mock environment.
# Must be consistent with the namespace pragmas in the main MOF file, because
# the pywbem MOF compiler does not create any namespaces.
INTEROP_NAMESPACE = 'interop'
MODEL_NAMESPACE = 'root/cimv2'


def register_dependents(conn, this_file_path, dependent_file_names):
    """
    Register a dependent file name with the pywbemcli dependent file api.
    This insures that any change to a dependent file will cause the
    script to be recompiled.
    """
    if isinstance(dependent_file_names, six.string_types):
        dependent_file_names = [dependent_file_names]

    for fn in dependent_file_names:
        dep_path = os.path.join(os.path.dirname(this_file_path), fn)
        conn.provider_dependent_registry.add_dependents(this_file_path,
                                                        dep_path)


def _setup(conn, server, verbose):
    # pylint: disable=unused-argument
    """
    Setup for this mock script.

    Parameters:
      conn (FakedWBEMConnection): Connection
      server (PywbemServer): Server
      verbose (bool): Verbose flag
    """

    if INTEROP_NAMESPACE not in conn.cimrepository.namespaces:
        conn.add_namespace(INTEROP_NAMESPACE)
    if MODEL_NAMESPACE not in conn.cimrepository.namespaces:
        conn.add_namespace(MODEL_NAMESPACE)

    if sys.version_info >= (3, 5):
        this_file_path = __file__
    else:
        # Unfortunately, it does not seem to be possible to find the file path
        # of the current script when it is executed using exec(), so we hard
        # code the file path. This requires that the tests are run from the
        # repo main directory.
        this_file_path = 'tests/unit/pywbemcli/simple_interop_mock_script.py'
        assert os.path.exists(this_file_path)

    mof_file = 'simple_interop_mock_model.mof'
    dependent_files = [mof_file,
                       'mock_interop.mof',
                       'simple_mock_model.mof']
    mof_path = os.path.join(os.path.dirname(this_file_path), mof_file)
    conn.compile_mof_file(mof_path, namespace=MODEL_NAMESPACE)

    register_dependents(conn, this_file_path, dependent_files)
    ns_provider = pywbem_mock.CIMNamespaceProvider(conn.cimrepository)
    conn.register_provider(ns_provider, INTEROP_NAMESPACE, verbose=verbose)


if sys.version_info >= (3, 5):
    # New-style setup

    # If the function is defined directly, it will be detected and refused
    # by the check for setup() functions on Python <3.5, despite being defined
    # only conditionally. The indirect approach with exec() addresses that.
    # pylint: disable=exec-used
    exec("""
def setup(conn, server, verbose):
    _setup(conn, server, verbose)
""")

else:
    # Old-style setup

    global CONN  # pylint: disable=global-at-module-level
    global SERVER  # pylint: disable=global-at-module-level
    global VERBOSE  # pylint: disable=global-at-module-level

    # pylint: disable=undefined-variable
    _setup(CONN, SERVER, VERBOSE)  # noqa: F821
