.. _`Mock WBEM server support`:

Mock WBEM server support
========================

.. _`Mock support overview`:

Mock support overview
---------------------

Pywbemcli has support for mocking a WBEM server with the general option
``--mock-server/-m``. This allows executing pywbemcli against a mock
WBEM server that is automatically created in pywbemcli, rather than a real
WBEM server.

The ``--mock-server`` option is mutually exclusive with the ``--server`` and
``--name`` options, since each defines a WBEM server.

The automatically created mock WBEM server has a in-memory repository for
CIM objects (qualifier declarations, classes, and instances) and supports
CIM namespaces. The operations performed against the mock WBEM server cause
that mock repository to be inspected or manipulated accordingly.

The mock repository can be loaded with CIM objects from files specified as
an argument to the ``--mock-server`` option. Each use of the option specifies
one file path of such a file. The option may be used multiple times and each
specified file is processed sequentially, in the sequence of the options
on the command line.

The following types of files are supported for the ``--mock-server`` option:

* **MOF files**: If the file extension is ``.mof``, the file is considered a
  :term:`MOF` file. Pywbemcli compiles the MOF in the file and adds the
  resulting CIM objects into the mock repository.

  The MOF file may define CIM qualifier declarations, CIM classes and CIM
  instances.

  At this point, these CIM objects can be added to only one
  :term:`CIM namespace` in the repository of the mock WBEM server, namely the
  default namespace of the connection (see ``--default-namespace`` global
  option).

  If a CIM object already exists in the repository, it is updated accordingly.

* **Python files**: If the file extension is ``.py``, the file is considered
  a Python file. The file is executed using Python's ``exec()`` (i.e. with
  module namespace ``__builtin__``), and with the following Python global
  variables made available:

  * ``CONN`` (:class:`pywbem_mock.FakedWBEMConnection`):
    This object provides a connection to the mock WBEM server. The methods
    of this object can be used to create and modify CIM objects in the
    mock repository.

  * ``SERVER`` (:class:`pywbem.WBEMServer`):
    This object is layered on top of the ``CONN`` object and provides access
    to higher level features of the mock WBEM server, such as getting the
    Interop namespace, adding namespaces, or building more complex objects
    for the mock repository.

  * ``VERBOSE`` (bool):
    A flag that contains the value of the boolean ``--verbose`` general
    option of pywbemcli.

  The Python script can for example create Python objects of type
  :class:`~pywbem.CIMQualifierDeclaration`, :class:`~pywbem.CIMClass` and
  :class:`~pywbem.CIMInstance` for representing CIM objects, and add them to
  the mock repository via calls to
  :meth:`pywbem_mock.FakedWBEMConnection.add_cimobjects`.

  The Python script can also extend the capabilities of the mock WBEM server
  by implementing callbacks via :func:`pywbem_mock.method_callback_interface`,
  for handling CIM method invocations against the mock WBEM server.

Pywbemcli logging (``-l`` or ``--log`` general option) can be used together
with the mock support. Since the mock support does not use HTTP(S), only the
"api" component in the log configuration string will generate any log output.


.. _`Creating files for the mock repository`:

Creating files for the mock repository
---------------------------------------

The following is an example MOF file (named ``tst_file.mof``) that defines some
CIM qualifier declarations, a single CIM class, and a single CIM instance of
that class:

.. code-block:: text

    # Define some qualifiers

    Qualifier Description : string = null,
        Scope(any),
        Flavor(EnableOverride, ToSubclass, Translatable);

    Qualifier In : boolean = true,
        Scope(parameter),
        Flavor(DisableOverride, ToSubclass);

    Qualifier Key : boolean = false,
        Scope(property, reference),
        Flavor(DisableOverride, ToSubclass);

    Qualifier Out : boolean = false,
        Scope(parameter),
        Flavor(DisableOverride, ToSubclass);

    # Define a class

       [Description ("Simple CIM Class")]
    class CIM_Foo {

           [Key, Description("This is a key property")]
        string InstanceID;

           [Description("This is a uint32 property")]
        uint32 IntegerProp;

           [Description("Method with one output parameter")]
        uint32 TestMethod(
               [In (false), Out, Description("Output parameter")]
            string OutputParam;
        );
    };

    # Define an instance of the class

    instance of CIM_Foo as $foo1 {
        InstanceID = "CIM_Foo1";
        IntegerProp = 1;
    };

The pywbemcli command to use this MOF file for loading into a mock WBEM server,
and then to enumerate its CIM class names is::

    $ pywbemcli --mock-server tst_file.mof class enumerate --names-only
    CIM_Foo

The following is Python code (in a file ``tst_file.py``) that will add the same
CIM objects as in the MOF file to the mock repository using
:meth:`~pywbem_mock.FakedWBEMConnection.add_cim_objects`. If the ``--verbose``
general option is set on the pywbemcli command line, the mock repository will
be displayed:

.. code-block:: python

    #!/usr/bin/env python

    from pywbem import CIMQualifierDeclaration, CIMQualifier, CIMClass, \
        CIMProperty, CIMMethod, CIMParameter, CIMInstance, CIMInstanceName, Uint32


    def main():

        # Global variables made available by pywbemcli
        global CONN, VERBOSE

        # Define some qualifier declarations
        description_qd = CIMQualifierDeclaration(
            'Description', type='string', value=None,
            scopes=dict(ANY=True),
            overridable=True, tosubclass=True, translatable=True)
        in_qd = CIMQualifierDeclaration(
            'In', type='boolean', value=True,
            scopes=dict(PARAMETER=True),
            overridable=False, tosubclass=True)
        key_qd = CIMQualifierDeclaration(
            'Key', type='boolean', value=False,
            scopes=dict(PROPERTY=True, REFERENCE=True),
            overridable=False, tosubclass=True)
        out_qd = CIMQualifierDeclaration(
            'Out', type='boolean', value=False,
            scopes=dict(PARAMETER=True),
            overridable=False, tosubclass=True)

        # Define a class
        foo_cl = CIMClass(
            'CIM_Foo',
            qualifiers=[
                CIMQualifier('Description', 'Simple CIM Class'),
            ],
            properties=[
                CIMProperty(
                    'InstanceID', type='string', value=None,
                    qualifiers=[
                        CIMQualifier('Key', True),
                        CIMQualifier('Description', 'This is a key property'),
                    ],
                    class_origin='CIM_Foo', propagated=False),
                CIMProperty(
                    'IntegerProp', type='uint32', value=None,
                    qualifiers=[
                        CIMQualifier('Key', True),
                        CIMQualifier('Description', 'This is a uint32 property'),
                    ],
                    class_origin='CIM_Foo', propagated=False),
            ],
            methods=[
                CIMMethod(
                    'TestMethod', return_type='uint32',
                    qualifiers=[
                        CIMQualifier('Description',
                                     'Method with one output parameter'),
                    ],
                    parameters=[
                        CIMParameter(
                            'OutputParam', type='string',
                            qualifiers=[
                                CIMQualifier('In', False),
                                CIMQualifier('Out', True),
                                CIMQualifier('Description', 'Output parameter'),
                            ]),
                    ],
                    class_origin='CIM_Foo', propagated=False),
            ]
        )

        # Define an instance of the class.
        # Note: The mock repository does not add an instance path, so it must be
        # prepared upfront.
        foo1 = CIMInstance(
            'CIM_Foo',
            path=CIMInstanceName(
                'CIM_Foo', keybindings=dict(InstanceID="CIM_Foo1")),
            properties=[
                CIMProperty('InstanceID', value="CIM_Foo1"),
                CIMProperty('IntegerProp', value=Uint32(1)),
            ])

        # Add the CIM objects to the mock repository
        CONN.add_cimobjects([
            description_qd, in_qd, key_qd, out_qd,
            foo_cl,
            foo1,
        ])

        if VERBOSE:
            CONN.display_repository()


    if __name__ == '__builtin__':
        main()

As you can see, adding CIM objects with a MOF file is more compact, but of
course the Python script can contain logic, and it provides for
implementing CIM method calls via callbacks.

It is possible to mix MOF files and Python scripts by specifying the
``--mock-server`` option multiple times.

The pywbemcli command to use this Python file for loading into a mock WBEM
server, and then to enumerate its CIM class names is::

    $ pywbemcli --mock-server tst_file.py class enumerate --names-only
    CIM_Foo
