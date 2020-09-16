.. index:: pair: Mock WBEM server support; server mock

.. _`Mock WBEM server support`:

Mock WBEM server support
========================

.. _`Mock support overview`:

Mock support overview
---------------------

Pywbemcli supports mocking a WBEM server with the
:ref:`--mock-server general option`. This allows executing pywbemcli against a
mock WBEM server that is automatically created in pywbemcli, rather than a real
WBEM server.

The ``--mock-server`` option is mutually exclusive with the
:ref:`--server general option` and :ref:`--name general option`, since each
defines a WBEM server.

The automatically created mock WBEM server has a in-memory repository for
CIM objects (qualifier declarations, classes, and instances) and supports
CIM namespaces. The operations performed against the mock WBEM server cause
that mock repository to be inspected or manipulated accordingly.

The mock repository can be loaded with CIM objects from files specified as an
argument to the ``--mock-server`` option. Each use of the option
specifies one file path of such a file. The option may be used multiple times
and each specified file is processed sequentially, in the sequence of the
options on the command line.

The following types of files are supported for the ``--mock-server`` option:

.. index:: pair: MOF; server mock
.. index:: pair: compile_string(); mock setup methods

* **MOF files**: If the file extension is ``.mof``, the file is considered a
  :term:`MOF` file. Pywbemcli compiles the MOF in the file and adds the
  resulting CIM objects to the mock repository.

  The MOF file may define CIM qualifier declarations, CIM classes and CIM
  instances.

  At this point, these CIM objects can be added to only one
  :term:`CIM namespace` in the repository of the mock WBEM server, namely the
  default namespace of the connection (see
  :ref:`--default-namespace general option`).

  If a CIM object already exists in the repository, it is updated accordingly.

.. index:: triple: Python files; server mock; add_cimobjects()

* **Mock scripts**: If the file extension is ``.py``, the file is considered
  a Python mock script.

  Mock scripts can be used for any kind of setup of the mock WBEM server, for
  example for creating namespaces, implementing and registering providers, or
  adding CIM objects either from the corresponding Python objects or by
  compiling MOF files or MOF strings.

  Mock scripts support two approaches for passing the mock WBEM server they
  should operate on:

  * New-style: The mock script has a ``setup()`` function. This is the
    recommended approach, but it is supported only on Python >=3.5. It enables
    the mock environment of a connection definition to be cached.

    New-style mock scripts are imported as a Python module into Python namespace
    ``pywbemtools.pywbemcli.mockscripts.<mock-script-name>`` and their
    ``setup()`` function is called. That function has the following interface:

    .. code-block:: python

        def setup(conn, server, verbose):
            . . .

    * ``conn`` (:class:`pywbem_mock.FakedWBEMConnection`):
      This object provides a connection to the mock WBEM server. The methods
      of this object can be used to create and modify CIM objects in the
      mock repository and to register providers.

    * ``server`` (:class:`pywbem.WBEMServer`):
      This object is layered on top of the ``CONN`` object and provides access
      to higher level features of the mock WBEM server, such as getting the
      Interop namespace, adding namespaces, or building more complex objects
      for the mock repository.

    * ``verbose`` (bool):
      A flag that contains the value of the boolean
      :ref:`--verbose general option` of pywbemcli.

  * Old-style: The mock script does not have a ``setup()`` function. This
    approach is not recommended, but it is supported on all supported Python
    versions. Using old-style mock scripts in a connection definition prevents
    caching of its mock environment.

    Old-style mock scripts are executed as Python scripts in Python namespace
    ``__builtin__``, with the following Python global variables made available:

    * ``CONN`` (:class:`pywbem_mock.FakedWBEMConnection`):
      This object provides a connection to the mock WBEM server. The methods
      of this object can be used to create and modify CIM objects in the
      mock repository and to register providers.

    * ``SERVER`` (:class:`pywbem.WBEMServer`):
      This object is layered on top of the ``CONN`` object and provides access
      to higher level features of the mock WBEM server, such as getting the
      Interop namespace, adding namespaces, or building more complex objects
      for the mock repository.

    * ``VERBOSE`` (bool):
      A flag that contains the value of the boolean
      :ref:`--verbose general option` of pywbemcli.

  Mock scripts can for example create Python objects of type
  :class:`~pywbem.CIMQualifierDeclaration`, :class:`~pywbem.CIMClass` and
  :class:`~pywbem.CIMInstance` for representing CIM objects, and add them to
  the mock repository via calls to
  :meth:`pywbem_mock.FakedWBEMConnection.add_cimobjects`.

  Mock scripts can also implement user-defined providers
  (see :ref:`pywbem:User-defined providers` in the pywbem documentation)
  and register these providers with the mock WBEM server.

  Finally, mock scripts can be used to add or update CIM objects in the
  CIM repository of the mock WBEM server. This is an alternative to
  specifying MOF files, and can be used for example to parse files defining
  the CIM objects for entire WBEM management profiles.

It is possible to mix MOF files and mock scripts by specifying the
:ref:`--mock-server general option` multiple times.

Pywbemcli logging (see :ref:`--log general option`) can be used together
with the mock support. Since the mock support does not use HTTP(S), only the
"api" component in the log configuration string will generate any log output.


.. index::
    pair: Creating files for mock repository; server mock
    pair: Setting up the mock WBEM server; server mock
    pair: MOF; server mock

.. _`Creating files for the mock repository`:
.. _`Setting up the mock WBEM server`:

Setting up the mock WBEM server
-------------------------------

The following is an example MOF file named ``tst_file.mof`` that defines some
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


.. index:: pair: add_cimobjects(); mock setup methods

The following is an old-style mock script named ``tst_script.py`` that will add
the same CIM objects as MOF file ``tst_file.mof`` to the mock repository using
:meth:`~pywbem_mock.FakedWBEMConnection.add_cimobjects`. If the
:ref:`--verbose general option` is set on the pywbemcli command line, the
mock repository will be displayed:

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

The following is the new-style version of mock script ``tst_script.py``:

.. code-block:: python

    from pywbem import CIMQualifierDeclaration, CIMQualifier, CIMClass, \
        CIMProperty, CIMMethod, CIMParameter, CIMInstance, CIMInstanceName, Uint32


    def setup(conn, server, verbose):

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
        conn.add_cimobjects([
            description_qd, in_qd, key_qd, out_qd,
            foo_cl,
            foo1,
        ])

        if verbose:
            conn.display_repository()

The pywbemcli command to use this mock script, and then to enumerate its
CIM class names is::

    $ pywbemcli --mock-server tst_script.py class enumerate --names-only
    CIM_Foo

As you can see, adding CIM objects with a MOF file is more compact than
doing that in a mock script, but of course the mock script can contain logic,
and it allows defining providers.

The following new-style mock script defines and registers a method provider
for CIM method "CIM_Foo.Method1()" that modifies property "Property1"
of the target CIM instance and returns that property in an output parameter
"OutputParam1":

.. code-block:: python

    from pywbem import CIMInstanceName, CIMError, \\
        CIM_ERR_INVALID_PARAMETER, CIM_ERR_METHOD_NOT_AVAILABLE
    from pywbem_mock import MethodProvider

    class CIM_Foo_MethodProvider(MethodProvider):

        provider_classname = 'CIM_Foo'

        def InvokeMethod(self, methodname, localobject, params):

            if methodname.lower() == 'method1':
                if isinstance(localobject, CIMClassName):
                    raise CIMError(
                        CIM_ERR_INVALID_PARAMETER,
                        "CIM method {0} must be invoked on a CIM instance".
                        format(methodname))
                return self.Method1(localobject, params)
            else:
                raise CIMError(CIM_ERR_METHOD_NOT_AVAILABLE)

        def Method1(self, localobject, params):

            namespace = localobject.namespace
            instance_store = self.cimrepository.get_instance_store(namespace)

            # Get the instance the method was invoked on, from the CIM
            # repository (as a copy)
            instance = instance_store.get(localobject.path)  # a copy

            # Modify a property value in the local copy of the instance
            if 'Property1' not in instance.properties:
                instance.properties['Property1'] = 'new'
            instance.properties['Property1'] += '+'

            # Update the instance in the CIM repository from the changed
            # local instance
            instance_store.update(localobject.path, instance)

            # Return the property value in the output parameter
            outputparam1 = instance.properties['Property1']
            out_params = [
                CIMParameter('OutputParam1', type='string', value=outputparam1),
            ]

            # Set the return value of the CIM method
            return_value = 0

            return (return_value, out_params)

    def setup(conn, server, verbose):
        provider = CIM_Foo_MethodProvider(conn.cimrepository)
        conn.register_provider(provider, conn.default_namespace, verbose=verbose)


.. _`Caching of mock WBEM servers`:

Caching of mock WBEM servers
----------------------------

Pywbemcli automatically attempts to cache the mock WBEM server of a connection
definition. If the connection definition specifies only MOF files and
new-style mock scripts, that attempt will normally succeed. If it specifies
any old-style mock script, or if any MOF file fails to compile, or if any
mock script raises an exception, the mock WBEM server will not be cached.

The following data from a mock WBEM server is cached:

- its CIM repository
- the content of the Python namespaces of its mock scripts (this includes for
  example the definition of any Python classes for the providers)
- its registered providers
- a list of dependent files registered by its mock scripts

The caches for the connection definitions are maintained in the
``.pywbemcli_mockcache`` directory in the user's home directory.

If a connection is used, pywbemcli verifies whether its mock WBEM server has been
cached, and if so, whether the cache is up to date. If it is not up to date,
it is not used but re-generated.

For determining whether the cache is up to date, the file content of the
MOF files and mock scripts of the connection definition, as well as any
registered dependent files are used. The file dates are not used for this.

If a mock script uses further files that define the mock environment (e.g.
when an XML or YAML file is used that defines an entire WBEM management profile),
then pywbemcli does not know about these files. They can be made known to
pywbemcli by registering them as dependent files. Once that is done, they
are also used to determine whether the mock cache is up to date.
See :ref:`pywbem:Registry for provider dependent files` (in the pywbem
documentation) for details on how to register dependent files.
