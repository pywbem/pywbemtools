"""
mock_pywbem test script that installs a method callback to be executed. This is
based on the CIM_Foo class in the simple_mock_model.mof test file

"""
# test that GLOBALS exist
assert "CONN" in globals()
assert 'SERVER' in globals()
assert 'VERBOSE' in globals()
global CONN  # pylint: disable=global-at-module-level


def alltypes_callback(conn, object_name, methodname, **params):
    # pylint: disable=attribute-defined-outside-init, unused-argument
    # pylint: disable=invalid-name
    """
    InvokeMethod callback defined in accord with pywbem
    method_callback_interface which defines the input parameters and returns
    all parameters received.
    """
    return_params = list(params.values())
    return_value = 0

    return (return_value, return_params)


# Add the the callback to the mock repository
# pylint: disable=undefined-variable
CONN.add_method_callback(  # noqa: F821
    'PyWBEM_AllTypes', 'AllTypesMethod', alltypes_callback)
