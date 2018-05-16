.. _`Mock WBEM server support`:

Mock WBEM server support
========================

Support for mocking a WBEM server is integrated into pywbemcli using the
pywbem ``pywbem_mock`` subpackage and the pywbemcli ``--mock_server``
global command line option.  This allows executing the pywbemcli subcommands
against a mock WBEM server rather than a real WBEM server.

The pywbem mock support uses :class:`pywbem\pywbem_mock.FakedWBEMConnection`
to define a mock server and build a mock repository that contains data for
responses to the pywbemcli subcommands from the values of the ``--mock_server``
option.

This option constructs an instance of
:class:`~pywbem\pywbem_mock.FakedWBEMConnection` in place of
:class:`~pywbem\pywbem.WBEMConnection` and allows building the mock repository
of CIMQualifierDeclarations, CIMClasses, and CIMInstances in the mock
repository from the files defined with the ``--mock_server``.

Each instance of the ``--mock_server`` option defines a file or file path:

* MOF file (file extension ``mof``) - If the option value is a MOF file,
  pywbemcli compiles the MOF and inserts the CIM objects into the mock
  repository. The file may contain MOF definitions for CIM qualifier
  declarations, CIM classes  and CIM instances.

* Python file (file extension ``py``) - If the option value is a python file,
  that file is executed with the following global variables passed to the
  file:

    * ``CONN`` - an instance object of
                 :class:`~pywbem\pywbem_mock.FakedWBEMConnection`). The methods
                 of this instance object can be used to add data to the
                 mock repository.

    * ``VERBOSE`` - a boolean flag that is based on the pywbemcli option
                    ``--verbose``

  The file can contain any python statements or functions and can insert them
  into the :class:`~pywbem\pywbem_mock.FakedWBEMConnection` using the
  methods in that class

  Generally, the file will contain pywbem CIMQualifierDeclaration, CIMClass,
  and CIMInstance instance objects and a calls to
  :meth:`~pywbem\pywbem_mock.FakedWBEMConnection.add_cimobjects`. to insert the
  objects into the repository.  It may also contain pywbem method callbacks
  (define in pywbem as ``method_callback_interface``) to define server methods
  that will process InvokeMethod calls from pywbemcli.


Defining files for the mock respository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following si a  very simplistic MOF file that defines a single qualifier
declarations a CIMClass and a CIMInstance of that class. These objects will be
compiled into the mock repository in the default namespace::

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

     [Description ("Simple CIM Class")]

    class CIM_Foo {
            [Key, Description ("This is key property.")]
        string InstanceID;

            [Description ("This is Uint32 property.")]
        uint32 IntegerProp;

            [IN ( false ), OUT, Description("TestMethod Param")]
          string OutputParam);

            [ Description("Method with no Parameters") ]
        uint32 DeleteNothing();
    };

    instance of CIM_Foo as $foo1 {
        InstanceID = "CIM_Foo1";
        IntegerProp = 1;
        };

The pywbemcli command to test class enumerate with the pywbem mock and and
these qualifiers, etc. in the repository is::

    pywbemcli --mock-server tst_file.mof class enumerate

The following is a simple python file that will insert objects into
the mock repository in the default namespace. If the VERBOSE
global is passed from pywbemcli it will display the repository and test
that the class is in the repository with GetClass:

.. code-block:: python

    from pywbem import CIMQualifier, CIMClass, CIMProperty, CIMMethod

    def build_class():
        """Builds and returns a single pywbem CIMClass: CIM_Foo"""
        qkey = {'Key': CIMQualifier('Key', True)}
        dkey = {'Description': CIMQualifier('Description', 'blah blah')}

        c = CIMClass(
            'CIM_Foo', qualifiers=dkey,
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

        if VERBOSE:
            CONN.display_repository()
            CONN.GetClass('CIM_Foo')

The pywbemcli command for a test using this mock data is::

    pywbemcli --mock-server <filename>.py class enumerate
