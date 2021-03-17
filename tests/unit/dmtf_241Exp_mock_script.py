# Copyright 2021 IBM Corp. All Rights Reserved.
# (C) Copyright 2021 Inova Development Inc.
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
 Build and install a specific complete DMTF schema defined DMTF_TEST_SCHEMA
 into the default namespace and a minimal set of interop classes into the
 interop namespace defined by INTEROP_NAMESPACE
"""
import sys
import os
import pywbem_mock

DMTF_TEST_SCHEMA_VER = (2, 41, 0)
INTEROP_NAMESPACE = 'interop'
EXPERIMENTAL = True


def _setup(conn, server, verbose):  # pylint: disable=unused-argument
    """
    Compile the complete DMTF schema defined.
    """
    schema = pywbem_mock.DMTFCIMSchema(
        DMTF_TEST_SCHEMA_VER,
        'tests/schemas',
        use_experimental=EXPERIMENTAL,
        verbose=verbose)

    if sys.version_info >= (3, 5):
        this_file_path = __file__
    else:
        # Unfortunately, it does not seem to be possible to find the file path
        # of the current script when it is executed using exec(), so we hard
        # code the file path. This requires that the tests are run from the
        # repo main directory.
        this_file_path = 'tests/unit/simple_interop_mock_script.py'
        assert os.path.exists(this_file_path)

    # Build minimal interop namespace (CIMObjectManager, CIM_Namespace)

    if INTEROP_NAMESPACE not in conn.cimrepository.namespaces:
        conn.add_namespace(INTEROP_NAMESPACE)

    interop_classes = ['CIM_Namespace',
                       'CIM_ObjectManager',
                       'CIM_RegisteredProfile',
                       'CIM_ElementConformsToProfile',
                       'CIM_ReferencedProfile',
                       'CIM_ComputerSystem',
                       'CIM_CIMOMStatisticalData']

    conn.compile_schema_classes(
        interop_classes,
        schema.schema_pragma_file,
        namespace=INTEROP_NAMESPACE,
        verbose=verbose)

    # Register only the pragma file as the provider dependent files
    conn.provider_dependent_registry.add_dependents(
        this_file_path, schema.schema_pragma_file)

    ns_provider = pywbem_mock.CIMNamespaceProvider(conn.cimrepository)
    conn.register_provider(ns_provider, INTEROP_NAMESPACE, verbose=verbose)
    obj_mgr_instance = """
    instance of CIM_ObjectManager {
        SystemCreationClassName = "CIM_ComputerSystem";
        SystemName = "MockSystem_WBEMServerTest";
        CreationClassName = "CIM_ObjectManager";
        Name = "FakeObjectManager";
        ElementName = "DMTF_241Exp";
        Description = "Testing build of DMTF schema Experimental version 2.4.1";
        };
       """

    conn.compile_mof_string(obj_mgr_instance, namespace=INTEROP_NAMESPACE)

    if verbose:
        print('Interop schema installed in namespace: {} based on leaf '
              'classes: {}'.format(INTEROP_NAMESPACE,
                                   ", ".join(interop_classes)))

    conn.compile_mof_file(schema.schema_pragma_file, namespace=None)
    print("DMTF Schema: {} installed in namespace: {}".format(
        schema.schema_version_str, conn.default_namespace))


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
