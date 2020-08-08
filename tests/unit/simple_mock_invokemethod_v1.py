"""
mock_pywbem test script that installs a a method provider for the class
CIM_Foo
"""

from pywbem_mock import MethodProvider

from pywbem import CIM_ERR_METHOD_NOT_AVAILABLE, CIMError, CIM_ERR_NOT_FOUND, \
    CIMInstanceName

# test that GLOBALS exist
assert "CONN" in globals()
assert 'SERVER' in globals()
assert 'VERBOSE' in globals()
global CONN  # pylint: disable=global-at-module-level


class CIM_FooMethodProvider(MethodProvider):
    """
    User test provider for InvokeMethod using CIM_Foo and method1.
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
            raise CIMError(
                CIM_ERR_NOT_FOUND,
                "class {0} does not exist in CIM repository, "
                "namespace {1}".format(classname, namespace))

        if isinstance(localobject, CIMInstanceName):
            instance_store = self.cimrepository.get_instance_store(namespace)
            if not instance_store.object_exists(localobject):
                raise CIMError(
                    CIM_ERR_NOT_FOUND,
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

        raise CIMError(CIM_ERR_METHOD_NOT_AVAILABLE)


# Add the the callback to the mock repository
# pylint: disable=undefined-variable
CONN.register_provider(CIM_FooMethodProvider(CONN.cimrepository),  # noqa: F821
                       CONN.default_namespace,  # noqa: F821
                       verbose=False)
