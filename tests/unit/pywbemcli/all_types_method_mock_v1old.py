"""
Test mock script that installs a test method provider for CIM method
AllTypesMethod() in CIM class PyWBEM_AllTypes, using the old setup approach
with global variables.

Note: This script and its method provider perform checks because their purpose
is to test the provider dispatcher. A real mock script with a real method
provider would not need to perform any of these checks.
"""

import pywbem
import pywbem_mock

assert "CONN" in globals()
assert 'SERVER' in globals()
assert 'VERBOSE' in globals()
global CONN  # pylint: disable=global-at-module-level


class CIM_AllTypesMethodProvider(pywbem_mock.MethodProvider):
    """
    User test provider for InvokeMethod using CIM_Foo and method1.
    This is basis for testing passing of input parameters correctly and
    generating some exceptions.  It uses only one input parameter where the
    value defines the test and one return parameter that provides data from the
    provider, normally the value of the parameter defined with the input
    parameter. Test for existence of method named method1
    """

    provider_classnames = 'PyWBEM_AllTypes'

    def __init__(self, cimrepository):
        super().__init__(cimrepository)

    def InvokeMethod(self, methodname, localobject, params):
        """
        Simplistic test method. Validates methodname, localobject,
        and returns return value 0 and the input parameters.

        The parameters and return for Invoke method are defined in
        :meth:`~pywbem_mock.MethodProvider.InvokeMethod`
        """
        namespace = localobject.namespace

        # get classname and validate. This provider uses only one class
        classname = localobject.classname
        assert classname.lower() == self.provider_classnames.lower()

        if methodname != 'AllTypesMethod':
            raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE)

        # Test if class exists.
        if not self.class_exists(namespace, classname):
            raise pywbem.CIMError(
                pywbem.CIM_ERR_NOT_FOUND,
                "class {} does not exist in CIM repository, "
                "namespace {}".format(classname, namespace))

        # Return the input parameters as output parameters
        out_params = params

        return_value = 0

        return (return_value, out_params)


# Register the provider to the mock environment
# pylint: disable=undefined-variable
_PROV = CIM_AllTypesMethodProvider(CONN.cimrepository)  # noqa: F821
CONN.register_provider(_PROV, CONN.default_namespace,  # noqa: F821
                       verbose=VERBOSE)  # noqa: F821
