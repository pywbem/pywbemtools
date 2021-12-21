"""
Test mock script that installs a test method provider for CIM method
method1() in CIM class CIM_Foo, using the new setup approach with a setup()
function.

Note: This script and its method provider perform checks because their purpose
is to test the provider dispatcher. A real mock script with a real method
provider would not need to perform any of these checks.
"""

import os
import pywbem
import pywbem_mock


class CIM_FooMethodProvider(pywbem_mock.MethodProvider):
    """
    Test method provider for CIM_Foo.method1().

    This is basis for testing passing of input parameters correctly and
    generating some exceptions.  It uses only one input parameter where the
    value defines the test and one return parameter that provides data from the
    provider, normally the value of the parameter defined with the input
    parameter. Test for existence of method named method1
    """

    provider_classnames = 'CIM_Foo'

    def __init__(self, cimrepository):
        super(CIM_FooMethodProvider, self).__init__(cimrepository)

    def InvokeMethod(self, methodname, localobject, params):
        """
        Simplistic test method. Validates methodname, localobject, params
        and returns rtn value 0 and one parameter

        The parameters and return for Invoke method are defined in
        :meth:`~pywbem_mock.MethodProvider.InvokeMethod`
        """
        namespace = localobject.namespace
        classname = localobject.classname

        assert classname.lower() == 'cim_foo'

        # Test if class exists.
        if not self.class_exists(namespace, classname):
            raise pywbem.CIMError(
                pywbem.CIM_ERR_NOT_FOUND,
                "class {0} does not exist in CIM repository, "
                "namespace {1}".format(classname, namespace))

        if isinstance(localobject, pywbem.CIMInstanceName):
            instance_store = self.cimrepository.get_instance_store(namespace)
            if not instance_store.object_exists(localobject):
                raise pywbem.CIMError(
                    pywbem.CIM_ERR_NOT_FOUND,
                    "Instance {0} does not exist in CIM repository",
                    format(localobject))

        # This method expects a single parameter input
        return_params = []
        if methodname.lower() in ('fuzzy', 'fuzzystatic'):
            if params:
                if 'TestInOutParameter' in params:
                    return_params.append(params['TestInOutParameter'])

            if 'TestRef' in params:
                return_params.append(params['TestRef'])

            return_value = params.get('OutputRtnValue', 0)

            return (return_value, return_params)

        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE)


def setup(conn, server, verbose):
    # pylint: disable=unused-argument
    """
    Setup for this mock script.

    Parameters:
      conn (FakedWBEMConnection): Connection
      server (PywbemServer): Server
      verbose (bool): Verbose flag
    """

    # Make the mock script standalone by compiling the required MOF file
    # and by registering it as a dependent file.
    mof_file = os.path.join(os.path.dirname(__file__), 'simple_mock_model.mof')
    conn.compile_mof_file(mof_file, namespace=conn.default_namespace,
                          verbose=verbose)
    conn.provider_dependent_registry.add_dependents(__file__, mof_file)

    provider = CIM_FooMethodProvider(conn.cimrepository)
    conn.register_provider(provider, conn.default_namespace, verbose=verbose)
