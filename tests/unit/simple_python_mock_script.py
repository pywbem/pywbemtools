"""
    Test script to be loaded with pywbemcli _mock_server global option to test
    capability to execute python code as part of startup.
    This script loads a single class into the repository and displays
    the resulting repository.
    This script includes an assert to confirm that the class is loaded into
    the repository.
"""
from pywbem import CIMQualifier, CIMClass, CIMProperty, CIMMethod


def build_classes():
    """
    Builds and returns a single class: CIM_Foo that to be used as a
    test class for the mock class tests.
    """
    qkey = {'Key': CIMQualifier('Key', True)}
    dkey = {'Description': CIMQualifier('Description', 'blah blah')}

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
    global CONN
    CONN.add_cimobjects(c)


build_classes()
assert(CONN.GetClass('CIM_FooDirLoad'))
