.. _`Mock WBEM server support`:

Mock WBEM server support
========================

Support for mocking a WBEM server is integrated into pywbemcli using  the
pywbemcli ``--mock-server`` global command line option.  This allows executing
the pywbemcli against a mock WBEM server rather than a real WBEM
server.

The pywbem mock support uses :class:`pywbem\pywbem_mock.FakedWBEMConnection`
to define a mock server and build a mock repository that contains data for
responses to pywbemcli from the values of the ``--mock-server`` option.

This command line option constructs an instance of
:class:`~pywbem\pywbem_mock.FakedWBEMConnection` in place of
:class:`~pywbem\pywbem.WBEMConnection` and allows building the mock repository
of CIMQualifierDeclarations, CIM classes, and CIM instances in the mock
repository from the files defined with the ``--mock-server``.

Each instance of the ``--mock-server`` option defines a single file or file
path:

* `MOF` file (file extension ``mof``) - If the option value is a `MOF` file,
  pywbemcli compiles the MOF and inserts the CIM objects into the mock
  repository. The file may contain MOF definitions for CIM qualifier
  declarations, CIM classes  and CIM instances.

* Python file (file extension ``py``) - If the option value is a Python file,
  that file is executed with the following global variables passed to the
  file:

    * ``CONN`` - an instance object of
                 :class:`~pywbem\pywbem_mock.FakedWBEMConnection`). The methods
                 of this instance object can be used to add data to the
                 mock repository.

    * ``SERVER`` - an instance object of :class:`~pywbem\WBEMServer`). The
                   methods of this instance object can be used to add data to
                   them mock repository. This instance can be useful to get
                   namespace information or build more complex objects
                   for the mock repository.

    * ``VERBOSE`` - a boolean flag that is based on the pywbemcli option
                    ``--verbose``

  The file can contain any Python statements or functions and can insert them
  into the :class:`~pywbem\pywbem_mock.FakedWBEMConnection` using the
  methods in that class

  Generally, the Python file will contain pywbem CIMQualifierDeclaration,
  CIMClass, and CIMInstance instance objects and a calls to
  :meth:`~pywbem\pywbem_mock.FakedWBEMConnection.add_cim objects` to insert
  objects into the repository.  It may also contain pywbem method callbacks
  (define in pywbem as ``method_callback_interface``) to define server methods
  that will process InvokeMethod calls from pywbemcli.

Pywbemcli logging (``--log``) can be enabled when the `--mock-server` option is
enabled. However, since the mock support does not use HTTP, the `http`  of the
log option will generate no output.

Defining files for the mock respository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is a  simplistic MOF file that defines somee qualifier
declarations, a CIMClass, and a CIMInstance of that class:

.. code-block:: text

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

The pywbemcli command to test class enumerate with the pywbem mock MOF above in
the file ``test_file.mof`` and in the mock repository is::

    pywbemcli --mock-server tst_file.mof

The following is a simple Python file that will insert CIM objects  defined
using the pywbem APIs into the mock repository in the default namespace. If the
``--verbose`` general option is set on the pywbemcli command line, the global
variable ``VERBOSE`` will be set True and the code below  will display the
repository and test that the class is in the repository with GetClass:

.. code-block:: python

    from pywbem import CIMQualifier, CIMClass, CIMProperty, CIMMethod

    def build_class():
        """Builds and returns a single pywbem CIMClass: CIM_Foo"""

        # Define the qualifier declarations for Key and Description
        qkey = {'Key': CIMQualifier('Key', True)}
        dkey = {'Description': CIMQualifier('Description', 'blah blah')}

        # create the CIMClass with one property and two methods
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
        # Add the objects to the repository
        global CONN
        CONN.add_cimobjects(c)

        # if verbose, show repository and test if class in repository
        if VERBOSE:
            CONN.display_repository()
            CONN.GetClass('CIM_Foo')

The pywbemcli command for a test using this mock data is::

    pywbemcli --mock-server tst_file.mof.py class enumerate
