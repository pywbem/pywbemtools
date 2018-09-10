"""
mocker test script that installs a callback to be executed. This is based on
the CIM_Foo class in the simple_mock_model.mof test file

"""


def fuzzy_callback(conn, object_name, methodname, **params):
    # pylint: disable=attribute-defined-outside-init, unused-argument
    # pylint: disable=invalid-name
    """
    InvokeMethod callback.  This is a simple callback that just tests
    methodname and then returns returnvalue and params from the
    TestInvokeMethod object attributes.
    """

    if 'TestOutParameter' in params:
        return_params = params['TestOutParameter']
    else:
        return_params = []
    if 'TestRef' in params:
        return_params.append[params['TestRef']]
    return_value = 0
    if 'OutputRtnValue' in params:
        return_value = params['OutputRtnValue']

    return (return_value, return_params)


global CONN
# This method expected to use the global namespace
CONN.add_method_callback('CIM_Foo', 'Fuzzy', fuzzy_callback)  # noqa: F821
