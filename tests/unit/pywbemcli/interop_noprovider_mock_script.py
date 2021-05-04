"""
Test mock script that attempts to compile MOF into a user namespace
when the Interop namespace exists, but the CIMNamespaceProvider is not
registered.

This is expected to fail because no CIM_ObjectManager class and instance
exists, i.e. the interop namespace is set up incompletely.
"""


def setup(conn, server, verbose):
    # pylint: disable=unused-argument
    """
    Setup function of mock script.
    """

    mof = """
    #pragma namespace ("root/blah")
    #pragma locale ("en_US")
    Qualifier Association : boolean = false,
        Scope(association),
        Flavor(DisableOverride, ToSubclass);
    """

    # Enable the following line to provoke a programming error.
    # raise ValueError("test")

    conn.add_namespace('interop')
    conn.compile_mof_string(mof, verbose=True)
