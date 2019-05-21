.. _`Mock WBEM server support`:

Mock WBEM server support
========================

.. _`Mock support overview`:

Mock support overview
---------------------

Support for mocking a WBEM server is integrated into pywbemcli using  the
pywbemcli  general command line option (``-m``or ``--mock-server``).  This
allows executing pywbemcli against a mock WBEM server integrated into the
pywbemcli process rather than a real WBEM server.

When the --mock-server option is used on the pywbemcli command line it
replaces the --server option

The ``--mock-server`` option constructs an instance of the pywbem class
:class:`~pywbem.pywbem_mock.FakedWBEMConnection` in place of the pywbem class
:class:`~pywbem.pywbem.WBEMConnection` and allows building the mock repository
of CIM qualifier declarations, CIM classes, and CIM instances in the mock
repository from the file specified with the ``--mock-server`` option.

The ``--mock-server`` option defines a single file path that pywbemcli will
pass to the repository building tools in pywbem when pywbemcli is started. This
option may be used multiple times and each use of the option specifies the file
path of one of the following types of files:

* ``MOF`` file (file extension ``mof``) - If the option value is the file path of
  a `MOF` file, pywbemcli compiles the MOF and inserts the CIM objects into the
  mock repository. The file may contain MOF definitions for CIM qualifier
  declarations, CIM classes  and CIM instances when pywbemcli is started.  The
  CIM objects will be inserted into the default namespace defined for the
  current connection.

* Python file (file extension ``py``) - If the option value is the file path of
  a Python file, that file is executed with the following Python GLOBAL
  variables passed to the file when pywbemcli is started:

    * ``CONN`` - an instance of
                 :class:`~pywbem.pywbem_mock.FakedWBEMConnection`). The methods
                 of this instance object can be used to add data to the
                 mock repository.

    * ``SERVER`` - an instance of :class:`~pywbem.WBEMServer`). The
                   methods of this instance object can be used to add data to
                   them mock repository. This instance can be useful to get
                   namespace information or build more complex objects
                   for the mock repository.

    * ``VERBOSE`` - a boolean flag that is based on the pywbemcli option
                    ``--verbose``.

  The file can contain any Python statements or functions and can insert them

  into the :class:`~pywbem.pywbem_mock.FakedWBEMConnection` using the
  methods in that class

  The  Python file may contain pywbem CIMQualifierDeclaration,
  CIMClass, and CIMInstance instance objects and calls to
  :meth:`~pywbem.pywbem_mock.FakedWBEMConnection.add_cim objects` to insert
  objects into the repository.

  It may also implement pywbem CIM method callbacks (defined in pywbem as
  ``method_callback_interface``) for handling InvokeMethod operations requested
  from pywbemcli.

Pywbemcli logging (`` -l`` or ``--log``) can be enabled when the `--mock-server` option is
enabled. However, since the mock support does not use HTTP, the `http`  of the
log option will generate no output.


.. _`Creating files for the mock respository`:

Creating files for the mock respository
---------------------------------------

The following is a MOF file (tst_file.mof) that defines some qualifier
declarations, a single CIMClass, and a single CIMInstance of that class:

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

    # define the instance of CIM_Foo in MOF
    # NOTE that the alias $foo1 creates the instance name
    instance of CIM_Foo as $foo1 {
        InstanceID = "CIM_Foo1";
        IntegerProp = 1;
        };

The pywbemcli command to insert these CIM objects into the mock repository
(where the file containing the above MOF is tst_file.mof)  and then to
enumerate its CIM classes is::

    $ pywbemcli --mock-server tst_file.mof class enumerate

           [Description ( "Simple CIM Class" )]
        class CIM_Foo {

              [Key ( true ),
               Description ( "This is key property." )]
           string InstanceID;

              [Description ( "This is Uint32 property." )]
           uint32 IntegerProp;

              [Description ( "Method with in and out parameters" )]
           uint32 Fuzzy(
                 [IN ( true ),
                  OUT ( true ),
                  Description ( "Define data to be returned in output parameter" )]
              string TestInOutParameter,
                 [IN ( true ),
                  OUT ( true ),
                  Description ( "Test of ref in/out parameter" )]
              CIM_Foo REF TestRef,
                 [IN ( false ),
                  OUT ( true ),
                  Description ( "Rtns method name if exists on input" )]
              string OutputParam,
                 [IN ( true ),
                  Description ( "Defines return value if provided." )]
              uint32 OutputRtnValue);

              [Description ( "Method with no Parameters" )]
           uint32 DeleteNothing();

        };
      $

The following is a  Python code (in a file tst_file.py)) that will insert CIM
objects defined using the pywbem APIs into the mock repository in the default
namespace. If the ``--verbose`` general option is set on the pywbemcli command
line, the global variable ``VERBOSE`` will be set True and the code below  will
display the repository and test that the class is in the repository with
GetClass:

.. code-block:: python

    # CONN and VERBOSE are GLOBAL available to this code when executed in
    # during pywbemcli startup

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


    $ pywbemcli --mock-server tst_file.mof.py class enumerate

