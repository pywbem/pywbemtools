"""
Test mock script that installs a test method provider for CIM method
method1() in CIM class CIM_Foo, using the old setup approach
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


# Register the provider to the mock environment
# pylint: disable=undefined-variable
_PROV = CIM_FooMethodProvider(CONN.cimrepository)  # noqa: F821
CONN.register_provider(_PROV, CONN.default_namespace,  # noqa: F821
                       verbose=VERBOSE)  # noqa: F821
