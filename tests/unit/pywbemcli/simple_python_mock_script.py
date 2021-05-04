"""
    Test script to be loaded with pywbemcli --mock-server general option to test
    capability to execute python code as part of startup.
    This script loads a single class into the repository.
    This script includes  asserts to confirm that the class is loaded into
    the repositoryand to verify that the GLOBALS are passed to this code from
    pywbemcli.
"""
from pywbem import CIMQualifier, CIMClass, CIMProperty, CIMMethod

# test that GLOBALS exist
assert "CONN" in globals()
assert 'SERVER' in globals()
assert 'VERBOSE' in globals()
global CONN  # pylint: disable=global-at-module-level


def build_classes():
    """
    Function that builds and returns a single class: CIM_Foo that will to be
     used as a test class for the mock class tests.
    """
    # build the key properties
    qkey = {'Key': CIMQualifier('Key', True)}
    dkey = {'Description': CIMQualifier('Description', 'blah blah')}

    # build the CIMClass with properties and methods.
    c = CIMClass(
        'CIM_FooDirLoad', qualifiers=dkey,
        properties={'InstanceID':
                    CIMProperty('InstanceID', None, qualifiers=qkey,
                                type='string', class_origin='CIM_Foo',
                                propagated=False)},
        methods={'Delete': CIMMethod('Delete', 'uint32', qualifiers=dkey,
                                     class_origin='CIM_Foo',
                                     propagated=False),
                 'Fuzzy': CIMMethod('Fuzzy', 'string', qualifiers=dkey,
                                    class_origin='CIM_Foo',
                                    propagated=False)})
    # add the objects to the mock repository
    CONN.add_cimobjects(c)  # noqa: F821 pylint: disable=undefined-variable


def main():
    """Main routine when called as script"""

    build_classes()

    # pylint: disable=undefined-variable
    cls = CONN.GetClass('CIM_FooDirLoad')  # noqa: F821
    assert cls


if __name__ == '__main__':
    main()
