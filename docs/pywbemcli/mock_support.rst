.. index:: pair: Mock WBEM server support; server mock

.. _`Mock WBEM server`:

Mock WBEM Server
================

.. _`Mock WBEM server overview`:

Mock WBEM server overview
-------------------------

The pywbemcli implements an in-process Mock WBEM Server using the
:ref:`pywbem:Mock WBEM server` that provides WBEM server responses to pywbmcli
commands based on the definition of the CIM elements defined for the mock
WBEM server.

Pywbemcli starts WBEM server when pywbemcli :ref:`--mock-server general option`
is defined.  This option defines either a MOF file or Python script that
defines a mock WBEM server environment that can include CIM namespaces, CIM
classes, CIM instances, CIM qualifier declarations CIM instances, and CIM
providers. This allows executing pywbemcli commands against the mock WBEM server
that is created in pywbemcli rather than a real WBEM server.

The :ref:`--mock-server general option` is mutually exclusive with the
:ref:`--server general option` and :ref:`--name general option`, since each
defines a target WBEM server.

The created mock WBEM server has a in-memory repository for the
CIM objects defined by the MOF/script (qualifier declarations, classes, and
instances) and supports CIM namespaces. The operations performed against the
mock WBEM server cause that mock repository to be inspected (ex. ``class
enumerate``) or manipulated (ex.``instance create ....``) accordingly.

The mock repository can be defined and created with CIM objects from files
specified as an argument to the :ref:`--mock-server general option`. Each use
of the option specifies one file path. The option may be used
multiple times and each specified file is processed sequentially, in the
sequence of the options on the command line.

pywbemcli supports the following file types for the ``--mock-server`` option:

.. index:: pair: MOF; server mock
.. index:: pair: compile_string(); mock setup methods

* **MOF files**: If the file extension is ``.mof``, the file is considered a
  :term:`MOF` file and must be compilable with the :ref:`pywbem:MOF Compiler`
  and the MOF syntax defined by the DMTF in :term:`DSP0004`. Pywbemcli compiles
  the MOF in the file and adds the resulting CIM objects to the mock
  repository.

  The following is a very simple example that simply compiles two qualifier
  declaration in a file ``qualdecls.mof`` and executes the command
  ``qualifier enumerate``:

.. code-block:: text

    pywbemcli -m qualdecl.mof qualifier enumerate

    Qualifier Abstract : boolean = false,
        Scope(class, association, indication),
        Flavor(EnableOverride, Restricted);

    Qualifier Aggregate : boolean = false,
        Scope(reference),
        Flavor(DisableOverride, ToSubclass);

  The MOF file may define CIM namespaces (#pragma namespace ("user")), CIM
  qualifier declarations, CIM classes and CIM instances.

  Thus MOF files can create mocks of complete multi-namespace environments
  including multiple namespaces, multiple classes, and instances including
  complete association instances using the MOF compiler instance alias
  construct.

  If a CIM object already exists in the repository, it is updated accordingly.

.. index:: triple: Python files; server mock; add_cimobjects()

* **Mock scripts**: If the file extension is ``.py``, the file is considered
  a Python script and the script is executed as part of the startup of pywbemcli
  in the command line mode or upon the first command executed that communicates
  with a server in the interactive mode.

  Mock scripts can for example create Python objects of type
  :class:`~pywbem.CIMQualifierDeclaration`, :class:`~pywbem.CIMClass` and
  :class:`~pywbem.CIMInstance` for representing CIM objects, and add them to
  the mock repository via calls to
  :meth:`pywbem_mock.FakedWBEMConnection.add_cimobjects`.

  Mock scripts can also install user-defined providers (see
  :ref:`pywbem:User-defined providers`) and register these providers with the
  mock WBEM server (TODO).

  Finally, mock scripts can be used to add or update CIM objects in the mock
  CIM repository. This is an alternative to specifying MOF files, and can be
  used for example to parse files defining the CIM objects for entire WBEM
  management profiles.

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
.. _`Setting up the mock WBEM server with a MOF file`:

Setting up the mock WBEM server with a MOF file
-----------------------------------------------

If the :ref:`--mock-server general option` defines a MOF file, The file
most consist of DMTF MOF definitions of CIM qualifier declarations, CIM
class definitions, and CIM instance definitions that are compiled by
pywbemcli using the pywbem MOF compiler and installed in the mock
cim repository before the first pywbemcli command that calls the server
is executed.   CIM namespaces may be created (in addition to the
default namespace) with the MOF namespace pragma command.

The following is an example MOF file named ``tst_file.mof`` that defines some
CIM qualifier declarations, a single CIM class, and a single CIM instance of
that class:

.. code-block:: text

    // Define some qualifier declarations

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

    // Define a class

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

    // Define an instance of the class

    instance of CIM_Foo as $foo1 {
        InstanceID = "CIM_Foo1";
        IntegerProp = 1;
    };

The pywbemcli command to use this MOF file for loading into a mock WBEM server,
and then to enumerate its CIM class names is::

    $ pywbemcli --mock-server tst_file.mof class enumerate --names-only

    CIM_Foo


.. _`Defining the mock WBEM server with a Python script`:

Defining the mock WBEM server with a Python script
--------------------------------------------------

Creating a python script provides additional flexibility in defining mock
environments over just installing MOF files including:

1. The ability to install instance providers to control the processing of
specific instance operations (create, modify, delete) on specific classes. This
is similar to the definition of providers in WBEM servers such as OpenPegasus
which process requests and generate responses to the client in the WBEM server
for specific request types and CIM classes.  pywbem provides several prebuilt
instance providers that can be installed with the setup script.

2. The ability to install CIM qualifier declarations and CIM classes from
   DMTF schemas rather than simply from local MOF files. See
   :ref:`pywbem:Building a mocked CIM repository` rather than from local MOF
   files.

3. The ability to dynamically define and create CIM instances and in particular
   instances of associations using both MOF and instances build from
   pywbem cim objects ref:`pywbem.CIM objects`.

A pywbem startup script can create many of the basic characteristics of a
WBEM server including:

1. Building the mock environment namespaces where the namespaces can be as simple
   as just the connection default namespace or as complex as an environment
   with an :term:`Interop namespace` and multiple other namespaces.
2. Installing mock classes and qualifiers. This can be done by:

   * Compiling a fixed set of classes and qualifier declarations defined in a
     file or python string defining MOF.
   * Compiling qualifier declarations and classes from a DMTF schema. The
     following statements in a script installs qualifier declarations and CIM
     classes, from the DMTF schema version 2.49.0 from the DMTF web site (if it
     was not already on the local system compile the qualifier declarations
     specified by the list of classnames).

.. code-block::

       VERBOSE = False
       namespace = 'Interop'          # Namespace where qds and classes installed
       schema_dir = '.'               # Directory where DMTF schema downloaded and expanded
       DMTF_SCHEMA_VER = (2, 49, 0)   # defines DMTF schema version 2.49.0
       schema_dir = schema_dir        # Directory where schema will be downloaded and installed
       experimental-schema = True     # If True, DMTF experimental schema used

       # Get and expand the schema.
       schema = DMTFCIMSchema(DMTF_SCHEMA_VER,
                              schema_dir,
                              use_experimental=False,
                              verbose=VERBOSE)
       leaf_classes = ['CIM_ObjectManager', 'CIM_Namespace']

       # Compile the qualifier declarations from the schema
       # Compile the leaf classes and all classes on which they depend
       conn.compile_schema_classes(
                    leaf_classes,
                    schema.schema_pragma_file,
                    namespace=namespace,
                verbose=VERBOSE)

   These methods are documented in :ref:`pywbem.FakedWBEMConnection class`

3. Installing/registering instance providers required for the mock.
   Pywbemcli itself includes predefined providers for creating namespaces and
   managing indication subscriptions that provide interfaces the same as most
   WBEM servers.
4. Installing CIM instances required for the mock environment by:

   * Compiling MOF for the instances from a string or file
   * Defining the instances with the pywbem.CIMInstance() class and installing
     them .
5. Registering dependent startup files used in the startup script using TODO
   so that the mock WBEM server can be cached and restored
   or recreated if any of the dependent files change.
   Caching significantly increases the install speed of mock servers since
   the CIM objects are already compiled and the repository created. The
   pywbemcli method

   The following is an example of registering dependent files including the
   script file itself.

.. code-block:: python

    def register_dependents(conn, this_file_path, dependent_file_names):
        """
        Register a dependent file name with the pywbemcli dependent file api.
        This insures that any change to a dependent file will cause the
        script to be recompiled.
        """
        if isinstance(dependent_file_names, six.string_types):
            dependent_file_names = [dependent_file_names]

        for fn in dependent_file_names:
            dep_path = os.path.join(os.path.dirname(this_file_path), fn)
            conn.provider_dependent_registry.add_dependents(this_file_path,
                                                        dep_path)

    def _setup(conn, server, verbose):

        . . .

        if sys.version_info >= (3, 5):
            this_file_path = __file__
        else:
            # Unfortunately, it does not seem to be possible to find the file path
            # of the current script when it is executed using exec(), so we hard
            # code the file path. This requires that the tests are run from the
            # repo main directory.
            this_file_path = 'tests/unit/pywbemcli/simple_interop_mock_script.py'
            assert os.path.exists(this_file_path)

    # Register the script file itself and any other files used in the script.
    register_dependents(conn, this_file_path, <file-used-in-script>)

6. Setting up the startup script interface from pywbemcli:

   Mock scripts can be used for any kind of setup of the mock WBEM server, for
   example for creating namespaces, implementing and registering providers, or
   adding CIM objects either from the corresponding Python objects or by
   compiling MOF files or MOF strings.

   Mock scripts support two approaches for passing the mock WBEM server they
   should operate on depending on the Python version:

   * New-style(Python >=3.5): The mock script has a ``setup()`` function.  It enables
     the mock environment of a connection definition to be cached.

     New-style mock scripts are imported as a Python module into Python namespace
     ``pywbemtools.pywbemcli.mockscripts.<mock-script-name>`` and their
     ``setup()`` function is called. That function has the following interface:

    .. code-block::

        def setup(conn, server, verbose):

     where:

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

   * Old-style(all Python versions(*Deprecated*)):  The mock script does not have a
     ``setup()`` function. This approach is not recommended, but it is supported
     on all supported Python versions. Using old-style mock scripts in a
     connection definition prevents caching of its mock environment.

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

Thus the structure of a setup script might be as shown in the following example
that creates an :term:`Interop namespace`, CIM_Namespace and indication subscription
providers, and MOF in the default_namespace from a MOF file.

.. code-block:: python

    def register_dependents(conn, this_file_path, dependent_file_names):
        """
        Register a dependent file name with the pywbemcli dependent file api.
        This insures that any change to a dependent file will cause the
        script to be recompiled.
        """
        if isinstance(dependent_file_names, six.string_types):
            dependent_file_names = [dependent_file_names]

        for fn in dependent_file_names:
            dep_path = os.path.join(os.path.dirname(this_file_path), fn)
            conn.provider_dependent_registry.add_dependents(this_file_path,
                                                        dep_path)

    def _setup(conn, server, verbose):

        if sys.version_info >= (3, 5):
            this_file_path = __file__
        else:
            # Unfortunately, it does not seem to be possible to find the file path
            # of the current script when it is executed using exec(), so we hard
            # code the file path. This requires that the tests are run from the
            # repo main directory.
            this_file_path = 'tests/unit/pywbemcli/simple_interop_mock_script.py'
            assert os.path.exists(this_file_path)

    # Prepare an Interop namespace and namespace provider a DMTF schema

    INTEROP_NAMESPACE = 'interop'

    interop_mof_file = 'mock_interop.mof'
    if INTEROP_NAMESPACE not in conn.cimrepository.namespaces:
        conn.add_namespace(INTEROP_NAMESPACE, verbose=verbose)

    interop_mof_path = os.path.join(
        os.path.dirname(this_file_path), interop_mof_file)
    conn.compile_mof_file(interop_mof_path, namespace=INTEROP_NAMESPACE,
                          verbose=verbose)
    register_dependents(conn, this_file_path, interop_mof_file)

    ns_provider = pywbem_mock.CIMNamespaceProvider(conn.cimrepository)
    conn.register_provider(ns_provider, INTEROP_NAMESPACE, verbose=verbose)

    # Add namespace-neutral MOF to the default namespace

    mof_file = 'simple_mock_model.mof'
    mof_path = os.path.join(os.path.dirname(this_file_path), mof_file)
    conn.compile_mof_file(mof_path, namespace=None, verbose=verbose)
    register_dependents(conn, this_file_path, mof_file)


    # Interface from pywbemcli for both old and new interfaces

    if sys.version_info >= (3, 5):
        # New-style setup

        # If the function is defined directly, it will be detected and refused
        # by the check for setup() functions on Python <3.5, despite being defined
        # only conditionally. The indirect approach with exec() addresses that.
        # pylint: disable=exec-used
        exec("""
    def setup(conn, server, verbose):
        _setup(conn, server, verbose)
    """)

    else:
        # Old-style setup

        global CONN  # pylint: disable=global-at-module-level
        global SERVER  # pylint: disable=global-at-module-level
        global VERBOSE  # pylint: disable=global-at-module-level

        # pylint: disable=undefined-variable
        _setup(CONN, SERVER, VERBOSE)  # noqa: F821

Examples of pywbemcli startup python script
-------------------------------------------

Simple MOF based startup file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is an example of the new-style version of mock script
``tst_script.py`` that builds CIM classes and instances from pywbem CIM classes
(:ref:`pywbem:CIM Objects`) representing the cim objects:

.. index:: pair: add_cimobjects(); mock setup methods

.. code-block:: python

    from pywbem import CIMQualifierDeclaration, CIMQualifier, CIMClass, \
        CIMProperty, CIMMethod, CIMParameter, CIMInstance, CIMInstanceName, Uint32

    def setup(conn, server, verbose):
        """Setup script for python >= version 3.5"""

        # Define qualifier declarations using pywbem CIMQualifierDeclaration class

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

        # Define a class using pywbem CIMClass
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

        # Define an instance of the class using pywbem CIMInstances.
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

Example setup script old-style with MOF file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is a  old-style(deprecated) mock script named ``tst_script.py`` that will add
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


The pywbemcli command to use this mock script, and then to enumerate its
CIM class names is::

    $ pywbemcli --mock-server tst_script.py class enumerate --names-only
    CIM_Foo

As you can see, adding CIM objects with a MOF file is more compact than
doing that in a mock script, but the mock script can contain logic,
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


The pywbemtools github tests/unit/pywbemcli directory includes several good
examples of pywbemcli startup scripts that are used for testing including:

1. tests/unit/pywbemcli/simple_foo_mock_script.py that uses the default
   namespace to create a simple but repository with classes and instances
   defined in associated MOF files. See

.. _a link: git://github.com/pywbem/pywbem.git/tests/unit/pywbemcli/simple_foo_mock_script.py

2. simple_interop_mock_script.py - creates a mock server with interop
   and user namespaces and installs the namespace provider. It uses local
   MOF files to provide the qualifier declaration and class definitions.

3. tests/unit/pywbemcli/testmock/wbemserver_mock_script.py which defines a
   dictionary to build a mock server and uses the class in
   tests/unit/pywbemcli/testmock/wbemserver_mock_script.py to build a
   mock environment that can includes building multiple namespaces,
   installing the namespace provider and subscription providers,
   and installing sample profiles, central classes, and the
   association classes for profile traversing.


.. index:: pair: mock WBEM server ; cache mock WBEM server

.. _`Caching mock WBEM servers connection definitions`:


Caching mock WBEM servers connection definitions
------------------------------------------------

Pywbemcli automatically attempts to cache the contents of mock WBEM server
definition when:

1. the definition is saved (``connection save <name>``)
2. command executed that uses the mock repository (ex. ``class enumerate --no``).

Further, the connection will only be cached if:

1. The setup script is the new-style mock script or a MOF file. The old style
   setup script cannot be cached.
2. The default connection file is used (i.e the
   :ref:`--connections-file general option` is not used).
3. The MOF compiles correctly and the setup script does not pass an exception
   back to the caller.

The advantage of caching the mock server definition is the speed of startup,
in particular if the startup script compiles any classes and if the
DMTF schema functions of pywbem are used to get CIM qualifier declaration and
CIM class MOF.

The following data from a mock WBEM server is cached:

- its CIM repository including namespaces defined, CIM qualifiers,
  CIM classes, and CIM_instances
- the content of the Python namespaces of its mock scripts (this includes for
  example the definition of any Python classes for the providers)
- its registered providers
- a list of dependent files registered by its mock scripts

The caches for the connection definitions are maintained in the
``.pywbemcli_mockcache`` directory in the user's home directory in separate
files with names of the form <quid>.<connection name>

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
