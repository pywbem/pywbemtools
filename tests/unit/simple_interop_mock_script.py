"""
Test mock script that installs the pywbem provided namespace provider
CIMNamespaceProvider and the simple Interop and user namespace model
defined in simple_interop_mock_model.mof.
"""

import os
import pywbem_mock

# interop namespace used by this mock environment
INTEROP_NAMESPACE = 'interop'


def setup(conn, server, verbose):
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

    # This MOF file sets pragma namespace to 'interop' and 'root/cimv2'
    mof_file = os.path.join(os.path.dirname(__file__),
                            'simple_interop_mock_model.mof')
    mof_inc1_file = os.path.join(os.path.dirname(__file__),
                                 'mock_interop.mof')
    mof_inc2_file = os.path.join(os.path.dirname(__file__),
                                 'simple_mock_model.mof')
    conn.compile_mof_file(mof_file, namespace=None)
    conn.provider_dependent_registry.add_dependents(__file__, mof_file)
    conn.provider_dependent_registry.add_dependents(__file__, mof_inc1_file)
    conn.provider_dependent_registry.add_dependents(__file__, mof_inc2_file)

    ns_provider = pywbem_mock.CIMNamespaceProvider(conn.cimrepository)
    conn.register_provider(ns_provider, INTEROP_NAMESPACE, verbose=verbose)
