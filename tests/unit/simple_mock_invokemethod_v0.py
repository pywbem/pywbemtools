"""
mock_pywbem test script that installs a method callback to be executed. This is
based on the CIM_Foo class in the simple_mock_model.mof test file

"""
# test that GLOBALS exist
assert "CONN" in globals()
assert 'SERVER' in globals()
assert 'VERBOSE' in globals()
global CONN  # pylint: disable=global-at-module-level


def fuzzy_callback(conn, object_name, methodname, **params):
    # pylint: disable=attribute-defined-outside-init, unused-argument
    # pylint: disable=invalid-name
    """
    InvokeMethod callback defined in accord with pywbem
    method_callback_interface which defines the input parameters and return
    values for a mock of a CIMMethod execution in a WBEM server.  This is a
    simple callback that just tests methodname and then returns returnvalue and
    params from the TestInvokeMethod object attributes.
    """
    return_params = params.get('TestOutParameter', [])

    if 'TestInOutParameter' in params:
        return_params.append(params['TestInOutParameter'])

    if 'TestRef' in params:
        return_params.append(params['TestRef'])

    return_value = params.get('OutputRtnValue', 0)

    return (return_value, return_params)


# Add the the callback to the mock repository
# pylint: disable=undefined-variable
CONN.add_method_callback('CIM_Foo', 'Fuzzy', fuzzy_callback)  # noqa: F821
CONN.add_method_callback('CIM_Foo', 'FuzzyStatic', fuzzy_callback)  # noqa: F821
