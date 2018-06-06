"""
mocker test script that install a callback to be executed. This is based on
the CIM_Foo class in the simple_mock_model.mof test file

"""

RETURN_VALUE = 0
RETURN_PARAMS = None


def fuzzy_callback(self, conn, methodname, object_name, **params):
    # pylint: disable=attribute-defined-outside-init, unused-argument
    # pylint: disable=invalid-name
    """
    InvokeMethod callback.  This is a simple callback that just tests
    methodname and then returns returnvalue and params from the
    TestInvokeMethod object attributes.
    """
    print('fuzzy_callback conn=%s, methodname=%s, object_name=%s, params=%r'
          (conn, methodname, object_name, params))

    global RETURN_VALUE
    global RETURN_PARAMS
    return (RETURN_VALUE, RETURN_PARAMS)


global CONN
# This method expected to use the global namespace
CONN.add_method_callback('CIM_Foo', 'Fuzzy', fuzzy_callback)  # noqa: F821
