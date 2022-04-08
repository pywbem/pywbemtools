"""
Test mock script that prepares an Interop namespace and namespace provider,
and then compiles namespace-neutral MOF into the default namespace (which may
have been set from the outside).

This mock script uses 'new-style' setup for Python >=3.5 and 'old-style' setup
otherwise, and is therefore useable for all supported Python versions.
On Python <3.5, the tests using this script must be run from the repo main
directory.
"""

import sys
import os
import six
import pywbem_mock

# interop namespace used by this mock environment
INTEROP_NAMESPACE = 'interop'
THIRD_NAMESPACE = "root/cimv3"


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

    if sys.version_info >= (3, 5):
        this_file_path = __file__
    else:
        # Unfortunately, it does not seem to be possible to find the file path
        # of the current script when it is executed using exec(), so we hard
        # code the file path. This requires that the tests are run from the
        # repo main directory.
        this_file_path = 'tests/unit/pywbemcli/simple_interop_mock_script.py'
        assert os.path.exists(this_file_path)

    # Create the third namespace before the interop namespace is created
    # so that it exists when the pywbem server. This namespace creation done
    # before interop created because of pywbem issue #2865
    conn.add_namespace(THIRD_NAMESPACE, verbose=verbose)

    # Prepare an Interop namespace and namespace provider

    interop_mof_file = 'mock_interop.mof'
    if INTEROP_NAMESPACE not in conn.cimrepository.namespaces:
        conn.add_namespace(INTEROP_NAMESPACE, verbose=verbose)

    interop_mof_path = os.path.join(
        os.path.dirname(this_file_path), interop_mof_file)
    conn.compile_mof_file(interop_mof_path, namespace=INTEROP_NAMESPACE,
                          verbose=verbose)
    register_dependents(conn, this_file_path, interop_mof_file)

    ns_provider = pywbem_mock.CIMNamespaceProvider(conn.cimrepository)
    conn.register_provider(ns_provider, INTEROP_NAMESPACE, verbose=verbose)

    # Add namespace-neutral MOF to the default namespace and to the third
    # namespace

    mof_file = 'simple_mock_model.mof'
    mof_path = os.path.join(os.path.dirname(this_file_path), mof_file)
    register_dependents(conn, this_file_path, mof_file)

    conn.compile_mof_file(mof_path, namespace=None, verbose=verbose)

    # Create a third namespace that has same classes and the default
    # namespace but different instances
    # TODO add different class also

    # Add the same classes and instances as in root/cimv2
    conn.compile_mof_file(mof_path, namespace=THIRD_NAMESPACE, verbose=verbose)

    inst_mof = "instance of CIM_Foo{ " \
        "InstanceID = \"CIM_Foo3-third-ns\"; " \
        "IntegerProp = 3; " \
        "};"
    conn.compile_mof_string(inst_mof, namespace=THIRD_NAMESPACE,
                            verbose=verbose)


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
