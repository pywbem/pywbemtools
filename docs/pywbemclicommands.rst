.. Copyright 2016 IBM Corp. All Rights Reserved.
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..    http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
..


.. _`Pywbemcli command groups and commands`:

Pywbemcli command groups and commands
=====================================

This section defines the characteristics of each of the pywbemcli command
groups and commands including examples.

For the command line syntax of pywbemcli using these command groups and
commands, see :ref:`Pywbemcli command line interface`.

**NOTE:** Many of the examples below use the :ref:`--mock-server general option`
with mock files that are located in the pywbemtools ``tests/unit`` subdirectory.


.. _`Class command group`:

Class command group
-------------------

The **class** command group has commands that act on CIM classes.

This group has the following commands:

* :ref:`Class associators command` - List the classes associated with a class.
* :ref:`Class delete command` - Delete a class.
* :ref:`Class enumerate command` - List top classes or subclasses of a class in a namespace.
* :ref:`Class find command` - List the classes with matching class names on the server.
* :ref:`Class get command` - Get a class.
* :ref:`Class invokemethod command` - Invoke a method on a class.
* :ref:`Class references command` - List the classes referencing a class.
* :ref:`Class tree command` - Show the subclass or superclass hierarchy for a class.

See :ref:`pywbemcli class --help`.


.. _`Class associators command`:

Class associators command
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``class associators`` command lists the CIM classes that are associated
with the specified source class.

The source class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

If the ``--names-only``/``--no`` command option is set, only the class path is
displayed,
using a :term:`CIM object output formats` or a :term:`Table output formats`.
Otherwise, the class definition is displayed,
using a :term:`CIM object output formats`.

Note: This command returns the class associators, not the instance associators.
The :ref:`Instance associators command` returns the instance associators.

Example:

.. code-block:: text

    $ pywbemcli --name mymock class associators TST_Person --names-only
    //FakedUrl/root/cimv2:TST_Person

See :ref:`pywbemcli class associators --help` for details.


.. _`Class delete command`:

Class delete command
^^^^^^^^^^^^^^^^^^^^

The ``class delete`` command deletes the specified class on the server.

The class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

If the class has subclasses, the command is rejected.

If the class has instances, the command is rejected, unless the ``--force``
command option was specified, in which case the instances are also deleted.

WARNING: Deleting classes can cause damage to the server: It can impact
instance providers and other components in the server. Use this command with
caution.

Many WBEM servers may not allow this operation or may severely limit
the conditions under which a class can be deleted from the server.

Example:

.. code-block:: text

    $ pywbemcli class delete CIM_Blah

See :ref:`pywbemcli class delete --help` for details.


.. _`Class enumerate command`:

Class enumerate command
^^^^^^^^^^^^^^^^^^^^^^^

The ``class enumerate`` command enumerates the subclasses of the specified
class, or the root classes of the class hierarchy.

If the ``CLASSNAME`` argument is specified, the command enumerates the
subclasses of the class named with the ``CLASSNAME`` argument in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

If the ``CLASSNAME`` argument is omitted, the command enumerates the top
classes of the class hierarchy in the namespace specified with the
``-namespace``/``-n`` command option, or otherwise in the default namespace of
the connection.

If the ``--names-only``/``--no`` command option is set, only the class path is
displayed,
using a :term:`CIM object output formats` or a :term:`Table output formats`.
Otherwise, the class definition is displayed,
using a :term:`CIM object output formats`.

If the ``--deep-inheritance``/``--di`` command option is set, all direct and
indirect subclasses are included in the result. Otherwise, only one level of
the class hierarchy is in the result.

The following example enumerates the class names of the root classes in the
default namespace:

.. code-block:: text

    $ pywbemcli --name mymock class enumerate --names-only
    TST_Person
    TST_Lineage
    TST_MemberOfFamilyCollection
    TST_FamilyCollection

See :ref:`pywbemcli class enumerate --help` for details.


.. _`Class find command`:

Class find command
^^^^^^^^^^^^^^^^^^

The ``class find`` command lists classes with a class name that matches the
:term:`Unix-style path name pattern` specified in the ``CLASSNAME-GLOB``
argument in all namespaces of the connection, or otherwise in the specified
namespaces if the ``-namespace``/``-n`` command option is specified one or more
times.

The command displays the namespaces and class names of the result using the
``txt`` output format (default), or in a :term:`Table output formats`.

.. code-block:: text

    $ pywbemcli class find .*_WBEMS*
    root/PG_InterOp:CIM_WBEMServer
    root/PG_InterOp:CIM_WBEMServerCapabilities
    root/PG_InterOp:CIM_WBEMServerNamespace
    root/PG_InterOp:CIM_WBEMService
    test/EmbeddedInstance/Dynamic:CIM_WBEMService
    test/EmbeddedInstance/Static:CIM_WBEMService
    test/TestProvider:CIM_WBEMServer
    test/TestProvider:CIM_WBEMServerCapabilities
    test/TestProvider:CIM_WBEMServerNamespace
    test/TestProvider:CIM_WBEMService
    root/SampleProvider:CIM_WBEMService
    root/cimv2:CIM_WBEMServer
    root/cimv2:CIM_WBEMServerCapabilities
    root/cimv2:CIM_WBEMServerNamespace
    root/cimv2:CIM_WBEMService
    root/PG_Internal:PG_WBEMSLPTemplate

    $ pywbemcli --output-format table class find CIM_SystemComponent*
    Find class CIM_SystemComponent*
    +-------------------------------+---------------------+
    | Namespace                     | Classname           |
    |-------------------------------+---------------------|
    | root/PG_InterOp               | CIM_SystemComponent |
    | test/WsmTest                  | CIM_SystemComponent |
    | test/cimv2                    | CIM_SystemComponent |
    | test/CimsubTestNS0            | CIM_SystemComponent |
    | test/TestProvider             | CIM_SystemComponent |
    | test/EmbeddedInstance/Dynamic | CIM_SystemComponent |
    | root/SampleProvider           | CIM_SystemComponent |
    | test/CimsubTestNS1            | CIM_SystemComponent |
    | test/static                   | CIM_SystemComponent |
    | test/CimsubTestNS2            | CIM_SystemComponent |
    | test/TestINdSrcNS2            | CIM_SystemComponent |
    | test/EmbeddedInstance/Static  | CIM_SystemComponent |
    | test/CimsubTestNS3            | CIM_SystemComponent |
    | test/TestIndSrcNS1            | CIM_SystemComponent |
    | root/cimv2                    | CIM_SystemComponent |
    | root/benchmark                | CIM_SystemComponent |
    +-------------------------------+---------------------+

See :ref:`pywbemcli class find --help` for details.


.. _`Class get command`:

Class get command
^^^^^^^^^^^^^^^^^

The ``class get`` command gets the specified class.

The class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

The class definition is displayed using a :term:`CIM object output formats`.
This command does not support :term:`Table output formats`.

The following example shows getting the MOF representation of the class
``CIM_Foo``:

.. code-block:: text

    $ pywbemcli --name mymock class get CIM_Foo

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

See :ref:`pywbemcli class get --help` for details.


.. _`Class invokemethod command`:

Class invokemethod command
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``class invokemethod`` command invokes a CIM method on the specified class
and displays the return value and any output parameters.

The class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

Input parameters for the method can be specified with the ``--parameter``/``-p``
command option, which can be specified multiple times.

The return value and output parameters are displayed in the
:term:`CIM object output formats`.

This command invokes a method on a class, not on an instance. To invoke a
method on an instance, use the :ref:`instance invokemethod command`.

See :ref:`pywbemcli class invokemethod --help` for details.


.. _`Class references command`:

Class references command
^^^^^^^^^^^^^^^^^^^^^^^^

The ``class references`` command lists the CIM classes that reference
the specified source class.

The source class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

If the ``--names-only``/``--no`` command option is set, only the class path is
displayed,
using a :term:`CIM object output formats` or a :term:`Table output formats`.
Otherwise, the class definition is displayed,
using a :term:`CIM object output formats`.

Note: This command returns the class references, not the instance references.
The :ref:`Instance references command` returns the instance references.

.. code-block:: text

    $ pywbemcli --name mymock class references TST_Person --names-only
    //FakedUrl/root/cimv2:TST_Lineage
    //FakedUrl/root/cimv2:TST_MemberOfFamilyCollection

See :ref:`pywbemcli class references --help` for details.


.. _`Class tree command`:

Class tree command
^^^^^^^^^^^^^^^^^^

The ``class tree`` command displays the subclass or superclass hierarchy of the
specified class.

The class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

If ``CLASSNAME`` is omitted, the complete class hierarchy of the namespace is
displayed.

If the ``-superclasses`` command option is set, the specified class and its
superclass ancestry up to the top-level class are displayed. Otherwise,
the specified class and its subclass hierarchy are displayed.

The class hierarchy (or ancestry) is always formatted in the
:term:`Tree output format`; the ``--output-format``/``-o`` general option is
ignored.

Example:

.. code-block:: text

    $ pywbemcli class tree CIM_Foo
    CIM_Foo
     +-- CIM_Foo_sub
     |   +-- CIM_Foo_sub_sub
     +-- CIM_Foo_sub2

See :ref:`pywbemcli class tree --help` for details.


.. _`Instance command group`:

Instance command group
----------------------

The **instance** command group defines commands that act on CIM instances as defined
in the following subsections:

This group consists of the following commands:

* :ref:`Instance associators command` - List the instances associated with an instance.
* :ref:`Instance count command` - Count the instances of each class with matching class name.
* :ref:`Instance create command` - Create an instance of a class in a namespace.
* :ref:`Instance delete command` - Delete an instance of a class.
* :ref:`Instance enumerate command` - List the instances of a class.
* :ref:`Instance get command` - Get an instance of a class.
* :ref:`Instance invokemethod command` - Invoke a method on an instance.
* :ref:`Instance modify command` - Modify properties of an instance.
* :ref:`Instance references command` - Execute a query on instances in a namespace.
* :ref:`Instance query command` - List the instances referencing an instance.


.. _`Instance associators command`:

Instance associators command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance associators`` command gets the associator instances for the argument
as the :term:`INSTANCENAME` argument in the namespace defined with this
command or the default namespace and displays it in the defined format. If successful it returns the
instances or instance names associated with :term:`INSTANCENAME` otherwise it returns an
exception generated by the response This command displays the returned instances
or instance in the :term:`CIM object output formats` or :term:`Table output formats` (see
:ref:`Output formats`).:

.. code-block:: text

    $ pywbemcli --name mymock instance references TST_Person --names-only --interactive
    Pick Instance name to process: 0
    0: root/cimv2:TST_Person.name="Mike"
    1: root/cimv2:TST_Person.name="Saara"
    2: root/cimv2:TST_Person.name="Sofi"
    3: root/cimv2:TST_Person.name="Gabi"
    4: root/cimv2:TST_PersonSub.name="Mikesub"
    5: root/cimv2:TST_PersonSub.name="Saarasub"
    6: root/cimv2:TST_PersonSub.name="Sofisub"
    7: root/cimv2:TST_PersonSub.name="Gabisub"
    Input integer between 0 and 7 or Ctrl-C to exit selection: 0   << user responds 0

    //FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"
    //FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"
    //FakedUrl/root/cimv2:TST_MemberOfFamilyCollection.family="root/cimv2:TST_FamilyCollection.name=\"Family2\"",member="root/cimv2:TST_Person.name=\"Mike\""

See :ref:`pywbemcli instance associators --help` for details.


.. _`Instance count command`:

Instance count command
^^^^^^^^^^^^^^^^^^^^^^

The ``instance count`` command returns acount of the number of CIM instances in the
namespace defined by ``--namespace`` or the default namespace. The list of
classes processed is filtered by the ``CLASSNAME-GLOB`` optional argument using
using a :term:`Unix-style path name pattern`.

For example:

.. code-block:: text

    $ pywbemcli --name mymock instance count
    Count of instances per class
    +------------------------------+---------+
    | Class                        |   count |
    |------------------------------+---------|
    | TST_FamilyCollection         |       2 |
    | TST_Lineage                  |       3 |
    | TST_MemberOfFamilyCollection |       3 |
    | TST_Person                   |       4 |
    +------------------------------+---------+

This counts the number of instances specific to the class shown where the
``instance enumerate`` would show the instances for that class and its
subclasses.

Count is useful to determine which classes in the environment are actually
implemented. However this command can take a long time to execute because
it must a) enumerate all the classes in the namespaces, b) enumerate the
instances for each class.

See :ref:`pywbemcli instance count --help` for details.


.. _`Instance create command`:

Instance create command
^^^^^^^^^^^^^^^^^^^^^^^

The ``instance create`` command creates a new CIMInstance in the WBEM server namespace
defined with ``--namespace`` or the default namespace. The command builds the CIMInstance from the class defined by
CLASSNAME and the properties defined by the ``--property``/``-p`` option. The
properties are defined as name/value pairs, one property for each instance of
the ``--property`` option. Since the WBEM server (and pywbem) requires that
each property be typed, pywbemtools uses the CIMClass defined by CLASSNAME
retrieved from the WBEM server to define the type required to define the
CIMProperty.

For a single property in the new instance this is simply the ``--property`` option
with the property name and value:

.. code-block:: text

    --property PROPERTY-NAME=PROPERTY-VALUE

    --property PROPERTY-NAME="PROPERTY-VALUE"

where quotes are only required if the value includes whitespace.

For array properties the values are defined separated by commas.

The following examples create an instance of the class TST_Blah with two
scalar and one array property.

.. code-block:: text

    $ pywbemcli instance create TST_Blah --property InstancId=blah1 --property IntProp=3 --property IntArr=3,6,9

    $ pywbemcli instance create TST_Blah --property InstancId=\"blah 2\" --property IntProp=3 --property IntArr=3,6,9

If the create is successful, the server defined CIM Instance path is displayed.
If the operation fails, the exception is displayed. If there is a discrepancy
between the defined properties and the CIMClass property parameters
pywbemcli generates an exception.

See :ref:`pywbemcli instance create --help` for details.


.. _`Instance delete command`:

Instance delete command
^^^^^^^^^^^^^^^^^^^^^^^

The ``instance delete`` command deletes an instance defined by the
:term:`INSTANCENAME` argument in a namespace defined by either the
``--namespace`` option or the general ``--default-namespace``. The form of
INSTANCENAME is determined by the ``--interactive`` options and must be either:

* a string representation of a CIMInstanceName as defined by a :term:`WBEM URI`
* A class name in which case pywbemcli will get the instance names from the
  WBEM server and present a selection list for the user to select an
  instance name :ref:`Displaying CIM instances/classes or their names`

The following example deletes the instance defined by the explicit instance
name (Note the extra backslash (see :term:`backslash-escaped` required to
escape the double quote on the terminal):

.. code-block:: text

    $ pywbemcli --name mymock instance delete root/cimv2:TST_Person.name=\"Saara\"

See :ref:`pywbemcli instance delete --help` for details.


.. _`Instance enumerate command`:

Instance enumerate command
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance enumerate`` command enumerates instances or their paths defined by the CLASSNAME
argument in the namespace defined by ``--namespace``/``-n`` or the general option
``--default-namespace``/``-d`` in the defined format. This command displays the
returned instances or instance names in the :term:`CIM object output formats`
or :term:`Table output formats` (see :ref:`Output formats`).

The following example returns a two instanced to an ``instance enumerate``
command as MOF:

.. code-block:: text

    $ pywbemcli --name mymock instance enumerate TST_FamilyCollection

    instance of TST_FamilyCollection {
       name = "family1";
    };

    instance of TST_FamilyCollection {
       name = "Family2";
    };

See :ref:`pywbemcli instance enumerate --help` for details.


.. _`Instance get command`:

Instance get command
^^^^^^^^^^^^^^^^^^^^

The ``instance get`` command gets a single CIM instance defined by the :term:`INSTANCENAME`
argument from the default namespace or the namespace defined with the
command displayed in the defined format. The form of :term:`INSTANCENAME` is
determined by the ``--interactive`` option. It can display the returned
instance in the :term:`CIM object output formats` or :term:`Table output formats`
(see :ref:`Output formats`). Otherwise it returns the received exception.

This example successfully retrieves the instance defined by the INSTANCENAME
``root/cimv2:TST_Person.name=\"Saara\"``:

.. code-block:: text

    $ pywbemcli --name mymock instance get root/cimv2:TST_Person.name=\"Saara\"
    instance of TST_Person {
       name = "Saara";
    };

See :ref:`pywbemcli instance get --help` for details.


.. _`Instance invokemethod command`:

Instance invokemethod command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The invokemethod command invokes a method defined for the INSTANCENAME  and
METHOD arguments using any CIM parameters defined with the ``-parameter`` option.
If successful, it returns a return value and and CIM output parameters included in
the response. This command only formats in a simple text format.

As as example:

.. code-block:: text

    $ pywbemcli --mock-server tests/unit/all_types.mof --mock-server tests/unit/all_types_method.py

    pywbemcli> instance invokemethod PyWBEM_AllTypes.InstanceId=\"test_instance\" AllTypesMethod -parameter arrBool=True,False
    ReturnValue=0
    arrBool=true, false

See :ref:`pywbemcli instance invokemethod --help` for details.


.. _`Instance modify command`:

Instance modify command
^^^^^^^^^^^^^^^^^^^^^^^

The ``instance modify`` command modifies an existing instance of the class
defined by the CLASSNAME argument in the WBEM server  namespace defined by
either the default namespace or namespace option. The user provides the
definition of an instance in the same form as the ``add`` command but the
instance must already exist in the WBEM server and the instance created from
the command line must include all of the key properties so that it can be
identified in the server.

If successful, this command displays nothing, otherwise it displays the
received exception.

See :ref:`pywbemcli instance modify --help` for details.


.. _`Instance references command`:

Instance references command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance references`` command gets the reference instances or paths for a
instance defined as the :term:`INSTANCENAME` input argument in the default
namespace or the namespace defined with this command displayed in the
defined format. It can display any returned instances in the
:term:`CIM object output formats` or :term:`Table output formats`
(see :ref:`Output formats`). Otherwise it returns the received exception.:

.. code-block:: text

    $ pywbemcli --name mymock instance references root/cimv2:TST_Person.name=\"Saara\"
    instance of TST_Lineage {
       InstanceID = "SaaraSofi";
       parent = "/root/cimv2:TST_Person.name=\"Saara\"";
       child = "/root/cimv2:TST_Person.name=\"Sofi\"";
    };

See :ref:`pywbemcli instance references --help` for details.


.. _`Instance query command`:

Instance query command
^^^^^^^^^^^^^^^^^^^^^^

The ``instance query`` command executes an ExecQuery CIM-XML operation with query string defined as an argument.
The QUERY argument must be a valid query defined for the ``--query-language``
option and available in the WBEM server being queried.  The default for
the ``--query-language`` option is DMTF:CQL but any query language and query
will be passed to the server.

It displays any instances returned in the defined formats or any exception
returned.  It can display any returned instances in the
:term:`CIM object output formats` or :term:`Table output formats`
(see :ref:`Output formats`).

See :ref:`pywbemcli instance query --help` for details.


.. _`qualifier command group`:

Qualifier command group
-----------------------

The **qualifier** command group defines commands that act on
CIMQualifierDeclaration objects in the WBEM server including:

This group consists of the following commands:

* :ref:`qualifier get command` - Get a qualifier declaration.
* :ref:`qualifier enumerate command` - List the qualifier declarations in a
  namespace.


.. _`Qualifier get command`:

Qualifier get command
^^^^^^^^^^^^^^^^^^^^^

The ``qualifier get`` command gets a single qualifier declaration defined by the ``QUALIFIERNAME``
argument from the namespace in the target WBEM server defined with this
command  or the default namespace and display in the defined output format.
The output formats can be either one of the :term:`CIM object output formats`
or :term:`Table output formats` (see :ref:`Output formats`).

The following example gets the ``Key`` qualifier declaration from the
default namespace:

.. code-block:: text

    $ pywbemcli --name mymock qualifier get Key
    Qualifier Key : boolean = false,
        Scope(property, reference),
        Flavor(DisableOverride, ToSubclass);

See :ref:`pywbemcli qualifier get --help` for details.


.. _`Qualifier enumerate command`:

Qualifier enumerate command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``qualifier enumerate`` command  enumerates all qualifier declarations within the namespace
defined with this command or the default namespace in the target WBEM
server . The output formats can be either one  of the
:term:`CIM object output formats` or :term:`Table output formats`
(see :ref:`Output formats`).

This example displays all of the qualifier declarations in the default
namespace as a simple table.

.. code-block:: text

    $ pywbemcli --name mymock --output-format table qualifier enumerate
    Qualifier Declarations
    +-------------+---------+---------+---------+-------------+-----------------+
    | Name        | Type    | Value   | Array   | Scopes      | Flavors         |
    |-------------+---------+---------+---------+-------------+-----------------|
    | Association | boolean | False   | False   | ASSOCIATION | DisableOverride |
    |             |         |         |         |             | ToSubclass      |
    | Description | string  |         | False   | ANY         | EnableOverride  |
    |             |         |         |         |             | ToSubclass      |
    |             |         |         |         |             | Translatable    |
    | In          | boolean | True    | False   | PARAMETER   | DisableOverride |
    |             |         |         |         |             | ToSubclass      |
    | Key         | boolean | False   | False   | PROPERTY    | DisableOverride |
    |             |         |         |         | REFERENCE   | ToSubclass      |
    | Out         | boolean | False   | False   | PARAMETER   | DisableOverride |
    |             |         |         |         |             | ToSubclass      |
    +-------------+---------+---------+---------+-------------+-----------------+

See :ref:`pywbemcli qualifier enumerate --help` for details.


.. _`Server command group`:

Server command group
--------------------

The **server** command group defines commands that interact with a WBEM
server to access information about the WBEM server itself. These commands
are generally not namespace specific but access information about the server,
namespaces, etc. The commands are:

This group consists of the following commands:

* :ref:`Server brand command` - Get the brand of the server.
* :ref:`Server connection command` - Get connection info used by this server.
* :ref:`Server info command` - Get information about the server.
* :ref:`Server get-centralinsts command` - List central instances of mgmt profiles on the server.
* :ref:`Server interop command` - Get the Interop namespace of the server.
* :ref:`Server namespaces command` - Get the Interop namespace of the server.
* :ref:`Server profiles command` - List management profiles advertized by the server.


.. _`Server brand command`:

Server brand command
^^^^^^^^^^^^^^^^^^^^

The ``server brand`` command gets general information on the server.  Brand information is an
attempt by pywbem and pywbemtools to determine the product that represents
the WBEM server infrastructure.  Since that was not clearly defined in the DMTF
specifications, this command may return strange results but it returns
legitimate results for most servers:

.. code-block:: text

    $ pywbemcli --name myserver server brand
    Server Brand:
    +---------------------+
    | WBEM server brand   |
    |---------------------|
    | OpenPegasus         |
    +---------------------+

See :ref:`pywbemcli server brand --help` for details.


.. _`Server connection command`:

Server connection command
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``server connection command`` displays information on the connection defined for this
server.  This is same information as was defined when the connection was
saved with :ref:`connection save command` or the cli general options:

.. code-block:: text

    $ pywbemcli --name myserver server connection
    url: http://localhost
    creds: ('kschopmeyer', 'test8play')
    .x509: None
    default_namespace: root/cimv2
    timeout: 30 sec.
    ca_certs: None

See :ref:`pywbemcli server connection --help` for details.


.. _`Server info command`:

Server info command
^^^^^^^^^^^^^^^^^^^

The server info command gets general information on the server.  This command returns
information on the brand, namespaces, and other reasonable information on the
WBEM server:

.. code-block:: text

    $ pywbemcli --name myserver server info
    Server General Information
    +-------------+-----------+---------------------+-------------------------------+
    | Brand       | Version   | Interop Namespace   | Namespaces                    |
    |-------------+-----------+---------------------+-------------------------------|
    | OpenPegasus | 2.15.0    | root/PG_InterOp     | root/PG_InterOp               |
    |             |           |                     | root/benchmark                |
    |             |           |                     | root/SampleProvider           |
    |             |           |                     | test/CimsubTestNS2            |
    |             |           |                     | test/CimsubTestNS3            |
    |             |           |                     | test/CimsubTestNS0            |
    |             |           |                     | test/CimsubTestNS1            |
    |             |           |                     | root/PG_Internal              |
    |             |           |                     | test/WsmTest                  |
    |             |           |                     | test/TestIndSrcNS1            |
    |             |           |                     | test/TestINdSrcNS2            |
    |             |           |                     | test/EmbeddedInstance/Static  |
    |             |           |                     | test/TestProvider             |
    |             |           |                     | test/EmbeddedInstance/Dynamic |
    |             |           |                     | root/cimv2                    |
    |             |           |                     | root                          |
    |             |           |                     | test/cimv2                    |
    |             |           |                     | test/static                   |
    +-------------+-----------+---------------------+-------------------------------+

See :ref:`pywbemcli server info --help` for details.


.. _`Server interop command`:

Server interop command
^^^^^^^^^^^^^^^^^^^^^^

The ``server interop`` command get a the name of the interop namespace target WBEM server:

.. code-block:: text

    $ pywbemcli --name myserver server interop
    Server Interop Namespace:
    +------------------+
    | Namespace Name   |
    |------------------|
    | root/PG_InterOp  |
    +------------------+

See :ref:`pywbemcli server interop --help` for details.


.. _`Server namespaces command`:

Server namespaces command
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``server namespaces`` command gets a list of the namespaces defined in the target server:

.. code-block:: text

    $ pywbemcli --name myserver --output-format plain server namespaces
    Server Namespaces:
    Namespace Name
    root/PG_InterOp
    root/benchmark
    root/PG_Internal
    test/WsmTest
    test/EmbeddedInstance/Static
    test/TestProvider
    test/EmbeddedInstance/Dynamic
    root/cimv2
    root
    test/cimv2
    test/static

See :ref:`pywbemcli server namespaces --help` for details.


.. _`Server profiles command`:

Server profiles command
^^^^^^^^^^^^^^^^^^^^^^^

The ``server profiles`` command gets information on the WBEM management profiles
(see :term:`WBEM management profile`)
defined in the target WBEM server. WBEM management profiles are the mechanism WBEM
uses to provide the user a programmatic connection to defined management
functionality with the implementation of that functionality in a WBEM server
(see :term:`DSP1001` and :term:`DSP1033`).

This request returns the organization, registered name, and version of each
profile definition returned from the server and the options can be used to
filter the returned profiles by Organization and registered name.

The following example shows the CIM profiles in
an example WBEM server:

.. code-block:: text

    $ pywbemcli --name myserver --output-format simple server profiles
    Advertised management profiles:
    Organization    Registered Name           Version
    --------------  ------------------------  ---------
    DMTF            CPU                       1.0.0
    DMTF            Computer System           1.0.0
    DMTF            Ethernet Port             1.0.0
    DMTF            Fan                       1.0.0
    DMTF            Indications               1.1.0
    DMTF            Profile Registration      1.0.0
    Other           Some Other Subprofile     0.1.0
    Other           Some Subprofile           0.1.0
    Other           SomeSystemProfile         0.1.0
    SNIA            Array                     1.1.0
    SNIA            Block Server Performance  1.1.0
    SNIA            Disk Drive Lite           1.1.0
    SNIA            Indication                1.1.0
    SNIA            Indication                1.2.0
    SNIA            Profile Registration      1.0.0
    SNIA            SMI-S                     1.2.0
    SNIA            Server                    1.1.0
    SNIA            Server                    1.2.0
    SNIA            Software                  1.1.0
    SNIA            Software                  1.2.0

See :ref:`pywbemcli server profiles --help` for details.


.. _`Server get-centralinsts command`:

Server get-centralinsts command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``server get-centralinsts`` command gets the instance names of the central/scoping
instances of one or more :term:`WBEM management profile` s defined in the
target WBEM server:

.. code-block:: text

    $ pywbemcli server centralinsts --org DMTF --profile "Computer System"
    Advertised Central Instances:
    +---------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Profile                         | Central Instances                                                                                                                                                                                                                       |
    |---------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | DMTF:Computer System:1.0.0      | //leonard/test/TestProvider:Test_StorageSystem.Name="StorageSystemInstance1",CreationClassName="Test_StorageSystem"://leonard/test/TestProvider:Test_StorageSystem.Name="StorageSystemInstance2",CreationClassName="Test_StorageSystem" |
    +---------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

See :ref:`pywbemcli server get-centralinsts --help` for details.


.. _`Connection command group`:

Connection command group
------------------------

The **connection** command group defines commands that provide for a
persistent file (:term:`connections file`) of WBEM server connection
parameters and allow selecting entries in this file as well as adding entries
to the file, deleting entries from the file and viewing WBEM servers defined in the
the file. This allows multiple connections to be defined and then used by name
rather than through the detailed parameters of the connection.

Connections in the :term:`connections file` can be created by:

* Using the :ref:`connection save command` with the current connection. This options
  uses the parameters current connection to define and save a connection in the
  connections file.

The connection information for each connection is based on the information
used to create a connection and is largely the same information as is in the
options for pywbemcli. The data includes:

* **name** - name of the connection (required) and defined with an argument.
* **server** - the url for the defined connection. See :ref:`--server general option`.
* **default-namespace** - the default namespace defined for the connection
  (required). See :ref:`--default-namespace general option`.
* **user** - the user name for the connection (optional). See :ref:`--user general option`.
* **password** - the password for the connection (optional). See :ref:`--password general option`.
* **no-verify** - a boolean flag option that, if set causes the pywbem client not
  to verify any certificate received from the WBEM server certificate. Otherwise
  the ssh client software verifies the validity of the server certificate
  received from the WBEM server during connection setup. See :ref:`--verify general option`.
* **certfile** - optional server certificate filename. See :ref:`--certfile general option`.
* **keyfile** - optional client private keyfile filename. See :ref:`--keyfile general option`.
* **timeout** - optional timeout value. See :ref:`--timeout general option`.
* **mock-server** - optional definition  a mock server
  environment using the pywbem mock module. This parameter is used, the
  ``--server`` must not be defined.  See :ref:`--mock-server general option`.

The connection information is saved in the :term:`connections file` when the
:ref:`connection save command` command are executed. Multiple
connection files may be maintained in separate directories.

The commands in this group are:

* :ref:`Connection delete command` - Delete a WBEM connection definition.
* :ref:`Connection export command` -  Export the current connection.
* :ref:`Connection list command` - List the WBEM connection definitions.
* :ref:`Connection save command` - Save a connection to a new WBEM connection
  definition named NAME.
* :ref:`Connection select command` - Select a WBEM connection definition as
  current/default connection.
* :ref:`Connection show command` - Show connection info of a WBEM connection
  definition.
* :ref:`Connection test command` - Test the current connection with a
  predefined WBEM request.


.. _`Connection delete command`:

Connection delete command
^^^^^^^^^^^^^^^^^^^^^^^^^
The ``connection delete`` command deletes a specific connection by name or selection.
If the NAME argument exists, it attemts to delete the connection with that name;
otherwise it presents a selection list for the user to pick a connection to
delete.

The following
example deletes the connection defined in the add command above:

.. code-block:: text

    $ pywbemcli connection delete me

To delete by selection:

.. code-block:: text

    $ pywbemcli connection delete
    Select a connection or Ctrl_C to abort.
    0: mock1
    1: mockassoc
    2: op
    Input integer between 0 and 2 or Ctrl-C to exit selection: 1  << users enters

See :ref:`pywbemcli connection delete --help` for details.


.. _`Connection export command`:

Connection export command
^^^^^^^^^^^^^^^^^^^^^^^^^
The ``connection export`` command  exports the current connection information as environment variables.

.. code-block:: text

    $ pywbemcli --server http://localhost connection export
    export PYWBEMCLI_SERVER=http://localhost
    export PYWBEMCLI_DEFAULT_NAMESPACE=root/cimv2
    export PYWBEMCLI_TIMEOUT=30

  See :ref:`pywbemcli connection export --help` for details.


.. _`Connection list command`:

Connection list command
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``connection list`` command lists the connections in the :term:`connections
file` as a table. This produces a table output showing the connections defined
in the connections file.  It displays all of the persistent connections and
also the current connection if it has not been saved (i.e. defined with the
:ref:`--server general option` or :ref:`--mock-server general option` general
options and not saved).  This shows if a connection is the current connection
and if any connection is set as the default connection (:ref:`Connection select
command` ).


.. code-block:: text

    pywbemcli> --server http://localhost --user me --password mypw --no-verify connection save me

    pywbemcli> --server http://blahblah connection list
    WBEM server connections:  (#: default, *: current)
    +--------------+------------------+-------------+-------------+-----------+------------+----------------------------------------+
    | name         | server           | namespace   | user        |   timeout | no-verify  | mock-server                            |
    |--------------+------------------+-------------+-------------+-----------+------------+----------------------------------------|
    | *blahblah    | http://blah      | root/cimv2  |             |        45 | False      |                                        |
    | mock1        |                  | root/cimv2  |             |           | False      | tests/unit/simple_mock_model.mof       |
    | mockalltypes |                  | root/cimv2  |             |        30 | False      | tests/unit/all_types.mof               |
    | mockassoc    |                  | root/cimv2  |             |        30 | False      | tests/unit/simple_assoc_mock_model.mof |
    | mockext      |                  | root/cimv2  |             |        30 | False      | tests/unit/simple_mock_model_ext.mof   |
    | op           | http://localhost | root/cimv2  | xxxxxxxxxxx |           | False      |                                        |
    | test3        |                  | root/cimv2  |             |           | False      | tests/unit/simple_mock_model.mof       |
    |              |                  |             |             |           |            | tests/unit/mock_confirm_y.py           |
    +--------------+------------------+-------------+-------------+-----------+------------+----------------------------------------+

See :ref:`pywbemcli connection list --help` for details.


.. _`Connection save command`:

Connection save command
^^^^^^^^^^^^^^^^^^^^^^^
The ``connection save`` command saves the current connection information
to the :term:`connections file`.  If the current connection does not have a name
a console request asks for a name for the connection.
See :ref:`pywbemcli connection save --help` for details.


.. _`Connection select command`:

Connection select command
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``connection select`` command selects a connection from the connections
file sets that connection as the :term:`current connection` and optionally the
:term:`default connection` by using the ``--default option``.

A connection may be selected
to be the current connection by using the NAME argument or by selecting from a
list presented on the console if there is no NAME argument.

In the interactive mode, the selected connection remains the current connection
for the remainder of the interactive session unless another connection is selected.


The following example shows changing connection from within the interactive
mode of pywbemcli:

.. code-block:: text

    $ pywbemcli

    pywbemcli> connection select
    Select a connection or Ctrl_C to abort.
    0: mock1
    1: mockassoc
    2: op
    Input integer between 0 and 2 or Ctrl-C to exit selection: 1

    pywbemcli> connection list
    WBEMServer Connections:   (#: default, *: current)
    +------------+------------------+-------------+-------------+------------+-----------+------------+
    | name       | server uri       | namespace   | user        | password   |   timeout | no-verify  |
    |------------+------------------+-------------+-------------+------------+-----------+------------+
    | mock1      |                  | root/cimv2  |             |            |        30 | False      |
    | mockassoc* |                  | root/cimv2  |             |            |        30 | False      |
    | op         | http://localhost | root/cimv2  | xxxxxxxxxxx | edfddfedd  |        30 | True       |
    +------------+------------------+-------------+-------------+------------+-----------+------------+

    pywbemcli> connection show
    name: mockassoc
      server: None
      default-namespace: root/cimv2
      user: None
      password: None
      timeout: 30
      no-verify: False
      certfile: None
      keyfile: None
      use-pull: either
      pull-max-cnt: 1000
      mock-server: tests/unit/simple_assoc_mock_model.mof
      log: None

See :ref:`pywbemcli connection select --help` for details.


.. _`Connection show command`:

Connection show command
^^^^^^^^^^^^^^^^^^^^^^^
The ``connection show`` command shows information about the current connection, the
connection with name NAME, or any connection in the :term:`connections file` by using
"?" as the NAME argument.  The connection to be displayed will be
the :term:`current connection` if the NAME argument is omitted, the connection named
with the NAME argument, or selected from a selection list the NAME argument "?"

.. code-block:: text

    pywbemcli -s http://blah connection show
    name: not-saved (current)
      server: http://blah
      default-namespace: root/cimv2
      user: None
      password: None
      timeout: 30
      verify: True
      certfile: None
      keyfile: None
      mock-server:
      ca-certs: None

See :ref:`pywbemcli connection show --help` for details.


.. _`Connection test command`:

Connection test command
^^^^^^^^^^^^^^^^^^^^^^^
The ``connection test`` command executes a single predefined operation on the current connection
to determine if it is a WBEM server. It executes a single ``EnumerateClasses``
WBEM operation in the default namespace. If the server accepts the request
a simple text ``Connection successful`` will be returned.

See :ref:`pywbemcli connection test --help` for details.

The following example defines the connection with ``--server``, ``--user``,
and ``--password`` and executes the test with successful result:

.. code-block:: text

    $ pywbemcli --server http://localhost --user me --password mypw connection test
    Connection successful

An unsuccessful test will normally result in an exception that defines the
issue as follows for the server http://blah in the example below:

.. code-block:: text

    $ pywbemcli --server http://blah connection test
    Error: ConnectionError: Socket error: [Errno -2] Name or service not known


.. _`Repl command`:

Repl command
------------

This command sets pywbemcli into the :ref:`interactive mode`.  Pywbemcli can be
started in the :ref:`interactive mode` either by entering:

.. code-block:: text

    $ pywbemcli repl
    Enter 'help' for help, <CTRL-D> or ':q' to exit pywbemcli.
    pywbemcli>

or by executing the script without any command or command group:

.. code-block:: text

    $ pywbemcli
    Enter 'help' for help, <CTRL-D> or ':q' to exit pywbemcli.
    pywbemcli>

The repl mode is recognized by the prompt ``pywbemcli>``.


.. _`Help command`:

Help command
------------

The help command provides information on special commands and controls that can
be executed in the :ref:`interactive mode` including:

* executing shell commands,
* exiting pywbemcli,
* getting help on commands,
* viewing interactive mode command history.

This is different from the ``--help`` option that provides information on
command groups, and commands.

.. code-block:: text

    $ pywbemcli help

    The following can be entered in interactive mode:

      <pywbemcli-cmd>             Execute pywbemcli command <pywbemcli-cmd>.
      !<shell-cmd>                Execute shell command <shell-cmd>.

      <CTRL-D>, :q, :quit, :exit  Exit interactive mode.

      <TAB>                       Tab completion (can be used anywhere).
      -h, --help                  Show pywbemcli general help message, including a
                                  list of pywbemcli commands.
      <pywbemcli-cmd> --help      Show help message for pywbemcli command
                                  <pywbemcli-cmd>.
      help                        Show this help message.
      :?, :h, :help               Show help message about interactive mode.
      <up-arrow, down-arrow>      View pwbemcli command history:
