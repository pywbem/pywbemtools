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

.. index:: pair: command groups; class commands

.. _`Class command group`:

``class`` command group
-----------------------

The ``class`` command group has commands that act on CIM classes:

* :ref:`Class associators command` - List the classes associated with a class.
* :ref:`Class delete command` - Delete a class.
* :ref:`Class enumerate command` - List top classes or subclasses of a class in a namespace.
* :ref:`Class find command` - List the classes with matching class names on the server.
* :ref:`Class get command` - Get a class.
* :ref:`Class invokemethod command` - Invoke a method on a class.
* :ref:`Class references command` - List the classes referencing a class.
* :ref:`Class tree command` - Show the subclass or superclass hierarchy for a class.

See :ref:`pywbemcli class --help`.

.. index::
    pair: class commands; class associators
    single: associators; class

.. _`Class associators command`:

``class associators`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``class associators`` command lists the CIM classes that are associated
with the specified source class.

The source class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

If the ``--names-only``/``--no`` command option is set, only the class path is
displayed, using :term:`CIM object output formats` or
:term:`Table output formats`. Otherwise, the class definition is displayed,
using :term:`CIM object output formats`.

Note: This command returns class associations. The :ref:`Instance associators
command` returns instance associations.

Example:

.. code-block:: text

    $ pywbemcli --name mymock class associators TST_Person --names-only
    //FakedUrl/root/cimv2:TST_Person

See :ref:`pywbemcli class associators --help` for the exact help output of the command.

.. index:: pair: class commands; class delete
.. index:: pair: delete classes; class commands

.. _`Class delete command`:

``class delete`` command
^^^^^^^^^^^^^^^^^^^^^^^^

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

See :ref:`pywbemcli class delete --help` for the exact help output of the command.

.. index:: pair: class commands; class enumerate

.. _`Class enumerate command`:

``class enumerate`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``class enumerate`` command enumerates the subclasses of the specified
class, or the root classes of the class hierarchy.

.. index:: pair: CLASSNAME argument; class enumerate

If the ``CLASSNAME`` argument is specified, the command enumerates the
subclasses of the class named with the ``CLASSNAME`` argument in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

If the ``CLASSNAME`` argument is omitted, the command enumerates the top
classes of the class hierarchy in the namespace specified with the
``-namespace``/``-n`` command option, or otherwise in the default namespace of
the connection.

If the ``--names-only``/``--no`` command option is set, only the class path is
displayed, using :term:`CIM object output formats` or
:term:`Table output formats`. Otherwise, the class definition is displayed,
using :term:`CIM object output formats`.

If the ``--deep-inheritance``/``--di`` command option is set, all direct and
indirect subclasses are included in the result. Otherwise, only one level of
the class hierarchy is in the result.

.. index:: single: qualifier filters; class enumerate command

The ``--association``/``--no-association``,
``--indication``/``--no-indication``, ,``--experimental``/``--no-experimental``
and ``--deprecated``/``--no-deprecated`` options filter the returned classes or
classnames to include or exclude classes with the corresponding qualifiers.
Thus the ``--association`` option returns only classes or classnames that are
association classes.

The following example enumerates the class names of the root classes in the
default namespace:

.. code-block:: text

    $ pywbemcli --name mymock class enumerate --names-only
    TST_Person
    TST_Lineage
    TST_MemberOfFamilyCollection
    TST_FamilyCollection

See :ref:`pywbemcli class enumerate --help` for the exact help output of the command.

.. index:: pair: class commands; class find
.. index:: pair: find command; class group

.. _`Class find command`:

``class find`` command
^^^^^^^^^^^^^^^^^^^^^^

The ``class find`` command lists classes with a class name that matches the
:term:`Unix-style path name pattern` specified in the ``CLASSNAME-GLOB``
argument in all namespaces of the connection, or otherwise in the specified
namespaces if the ``-namespace``/``-n`` command option is specified one or more
times.

.. index:: pair: qualifier filters; class find command

The ``--association``/``--no-association``,
``--indication``/``--no-indication``, ,``--experimental``/``--no-experimental``
and ``--deprecated``/``--no-deprecated`` options filter the returned classes or
classnames to include or exclude classes with the corresponding qualifiers.
Thus the ``--association`` option returns only classes or classnames that are
association classes.

The command displays the namespaces and class names of the result using the
``txt`` output format (default), or using :term:`Table output formats`.

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

See :ref:`pywbemcli class find --help` for the exact help output of the command.

.. index:: pair: class commands; class get

.. _`Class get command`:

``class get`` command
^^^^^^^^^^^^^^^^^^^^^

The ``class get`` command gets the specified class.

The class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

The class definition is displayed using :term:`CIM object output formats`.
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

See :ref:`pywbemcli class get --help` for the exact help output of the command.

.. index:: pair: class commands; class invokemethod

.. _`Class invokemethod command`:

``class invokemethod`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``class invokemethod`` command invokes a CIM method on the specified class
and displays the return value and any output parameters.

The class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

Input parameters for the method can be specified with the ``--parameter``/``-p``
command option, which can be specified multiple times.
For details, see :ref:`Specifying CIM property and parameter values`.

The return value and output parameters are displayed using
:term:`CIM object output formats`.

This command invokes a method on a class, not on an instance. To invoke a
method on an instance, use the :ref:`instance invokemethod command`.

Example:

.. code-block:: text

    $ pywbemcli --mock-server tests/unit/all_types.mof --mock-server tests/unit/all_types_method_mock.py.py

    pywbemcli> class invokemethod PyWBEM_AllTypes AllTypesMethod --parameter arrBool=True,False
    ReturnValue=0
    arrBool=true, false

See :ref:`pywbemcli class invokemethod --help` for the exact help output of the command.

.. index:: pair: class commands; class references

.. _`Class references command`:

``class references`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``class references`` command lists the CIM classes that reference
the specified source class.

The source class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

If the ``--names-only``/``--no`` command option is set, only the class path is
displayed, using :term:`CIM object output formats` or
:term:`Table output formats`. Otherwise, the class definition is displayed,
using :term:`CIM object output formats`.

Note: This command returns the class references, not the instance references.
The :ref:`Instance references command` returns the instance references.

.. code-block:: text

    $ pywbemcli --name mymock class references TST_Person --names-only
    //FakedUrl/root/cimv2:TST_Lineage
    //FakedUrl/root/cimv2:TST_MemberOfFamilyCollection

See :ref:`pywbemcli class references --help` for the exact help output of the command.

.. index:: pair: class commands; class tree

.. _`Class tree command`:

``class tree`` command
^^^^^^^^^^^^^^^^^^^^^^

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

See :ref:`pywbemcli class tree --help` for the exact help output of the command.

.. index:: pair: command groups; instance commands

.. _`Instance command group`:

``instance`` command group
--------------------------

The ``instance`` command group has commands that act on CIM instances:

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
* :ref:`Instance shrub command` - Display association instance relationships.

See :ref:`pywbemcli instance --help`.

.. index::
    pair: instance commands; instance associators
    single: associators; instance

.. _`Instance associators command`:

``instance associators`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance associators`` command lists the CIM instances that are associated
with the specified source instance.

The specification of the instance name (INSTANCENAME argument) is documented
in the section :ref:`Specifying the INSTANCENAME command argument`.

If the ``--names-only``/``--no`` command option is set, only the instance paths
are displayed. Otherwise, the instances are displayed.

Valid output formats in both cases are :term:`CIM object output formats` or
:term:`Table output formats`.

Note: This command returns the instance associators, not the class associators.
The :ref:`Class associators command` returns the class associators.

Example:

.. code-block:: text

    $ pywbemcli --name mymock instance references TST_Person.? --names-only
    Pick Instance name to process: 0
    0: root/cimv2:TST_Person.name="Mike"
    1: root/cimv2:TST_Person.name="Saara"
    2: root/cimv2:TST_Person.name="Sofi"
    3: root/cimv2:TST_Person.name="Gabi"
    4: root/cimv2:TST_PersonSub.name="Mikesub"
    5: root/cimv2:TST_PersonSub.name="Saarasub"
    6: root/cimv2:TST_PersonSub.name="Sofisub"
    7: root/cimv2:TST_PersonSub.name="Gabisub"
    Input integer between 0 and 7 or Ctrl-C to exit selection: 0   << entered by user

    //FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeSofi"
    //FakedUrl/root/cimv2:TST_Lineage.InstanceID="MikeGabi"
    //FakedUrl/root/cimv2:TST_MemberOfFamilyCollection.family="root/cimv2:TST_FamilyCollection.name=\"Family2\"",member="root/cimv2:TST_Person.name=\"Mike\""

See :ref:`pywbemcli instance associators --help` for the exact help output of the command.

.. index:: pair: instance commands; instance count

.. _`Instance count command`:

``instance count`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance count`` command counts the CIM instances of some or all classes
in the namespaces specified with the ``-namespace``/``-n`` command option, or
all namespaces in the server.

This command displays the count of instances of each CIM class whose class name
matches the specified wildcard expression (CLASSNAME-GLOB) in all CIM
namespaces of the WBEM server, or in the specified namespaces (--namespace
option).  This differs from instance enumerate, etc. in that it counts the
instances specifically for the classname of each instance returned (the
creation classname), not including subclasses.

If the ``CLASSNAME-GLOB`` argument is specified, only instances of classes that
match the specified :term:`Unix-style path name pattern` are counted. If the
``CLASSNAME-GLOB`` argument is not specified all instances of all classes in
the target namespaces are counted.

.. index:: pair: qualifier filters; instance count command

The ``--association``/``--no-association``,
``--indication``/``--no-indication``, ,``--experimental``/``--no-experimental``
and ``--deprecated``/``--no-deprecated`` options filter the returned classes or
classnames to include or exclude classes with the corresponding qualifiers.
Thus the ``--association`` option returns only classes or classnames that are
association classes.

Results for classes that have no instances are not displayed.

This command can take a long time to execute since it potentially enumerates
all instance names for all classes in all namespaces.

Valid output formats are :term:`Table output formats`.

Example:

.. code-block:: text

    $ pywbemcli --name mymock instance count
    Count of instances per class
    +-------------+------------------------------+---------+
    | Namespace   | Class                        |   count |
    |-------------+------------------------------+---------|
    | root/cimv2  | TST_FamilyCollection         |       2 |
    | root/cimv2  | TST_Lineage                  |       3 |
    | root/cimv2  | TST_MemberOfFamilyCollection |       3 |
    | root/cimv2  | TST_Person                   |       4 |
    | root/cimv2  | TST_Personsub                |       4 |
    +-------------+------------------------------+---------+


Count is useful to determine which classes in the environment are actually
implemented. However this command can take a long time to execute because
it must a) enumerate all classes in the namespace, b) enumerate the
instances for each class.

See :ref:`pywbemcli instance count --help` for the exact help output of the command.

.. index:: pair: instance commands; instance create

.. _`Instance create command`:

``instance create`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance create`` command creates a CIM instance in the namespace
specified with the ``-namespace``/``-n`` command option, or otherwise in the
default namespace of the connection.

The new CIM instance has the creation class specified in the ``CLASSNAME``
argument and initial property values as specified by zero or more
``--property``/``-p`` command options.
For details, see :ref:`Specifying CIM property and parameter values`.

The command displays the instance path of the new instance that is returned by
the WBEM server, using ``txt`` output format.

Since the WBEM server (and pywbem) requires that each property be typed,
pywbemcli retrieves the creation class from the WBEM server to determine
the data types for the properties.

The following examples create an instance of the class TST_Blah with two
scalar and one array property:

.. code-block:: text

    $ pywbemcli instance create TST_Blah --property InstancId=blah1 --property IntProp=3 --property IntArr=3,6,9

    $ pywbemcli instance create TST_Blah --property InstancId=\"blah 2\" --property IntProp=3 --property IntArr=3,6,9

See :ref:`pywbemcli instance create --help` for the exact help output of the command.

.. index:: pair: instance commands; instance delete

.. _`Instance delete command`:

``instance delete`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance delete`` command deletes a CIM instance.

The specification of the instance name (INSTANCENAME argument) is documented
in the section :ref:`Specifying the INSTANCENAME command argument`.

The following example deletes an instance by specifying its instance name.
Note the extra backslash (see :term:`backslash-escaped`) that is required to
escape the double quote on the terminal:

.. code-block:: text

    $ pywbemcli --name mymock instance delete root/cimv2:TST_Person.name=\"Saara\"

See :ref:`pywbemcli instance delete --help` for the exact help output of the command.

.. index:: pair: instance commands; instance enumerate

.. _`Instance enumerate command`:

``instance enumerate`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance enumerate`` command lists the CIM instances of the specified
class (including subclasses) in a namespace.

The class is named with the ``CLASSNAME`` argument and is in the
namespace specified with the ``-namespace``/``-n`` command option, or otherwise
in the default namespace of the connection.

If the ``--names-only``/``--no`` command option is set, only the instance paths
are displayed. Otherwise, the instances are displayed.

The ``--propertylist``/``--pl`` command option allows restricting the set of
properties to be retrieved and displayed on the instances.

Valid output formats in both cases are :term:`CIM object output formats` or
:term:`Table output formats`.

The following example returns two instances as MOF:

.. code-block:: text

    $ pywbemcli --name mymock instance enumerate TST_FamilyCollection

    instance of TST_FamilyCollection {
       name = "family1";
    };

    instance of TST_FamilyCollection {
       name = "Family2";
    };

See :ref:`pywbemcli instance enumerate --help` for the exact help output of the command.

.. index:: pair: instance commands; instance get

.. _`Instance get command`:

``instance get`` command
^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance get`` command gets a CIM instance.

The specification of the instance name (INSTANCENAME argument) is documented
in the section :ref:`Specifying the INSTANCENAME command argument`.

The ``--propertylist``/``--pl`` command option allows restricting the set of
properties to be retrieved and displayed on the instance.

The command displays the instance using :term:`CIM object output formats`
or :term:`Table output formats`.

This example gets an instance by instance name:

.. code-block:: text

    $ pywbemcli --name mymock instance get root/cimv2:TST_Person.name=\"Saara\"
    instance of TST_Person {
       name = "Saara";
    };

or using the keys wildcard:

.. code-block:: text

    $ pywbemcli --name mymock instance get root/cimv2:TST_Person.?
    Pick Instance name to process
    0: root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"
    1: root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"
    2: root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"
    Input integer between 0 and 2 or Ctrl-C to exit selection: 0   << entered by user
    instance of TST_Person {
       name = "Saara";
    };


See :ref:`pywbemcli instance get --help` for the exact help output of the command.

.. index:: pair: instance commands; instance invokemethod

.. _`Instance invokemethod command`:

``instance invokemethod`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance invokemethod`` command invokes a CIM method on the specified
instance and displays the return value and any output parameters.

The specification of the instance name (INSTANCENAME argument) is documented
in the section :ref:`Specifying the INSTANCENAME command argument`.

Input parameters for the method can be specified with the ``--parameter``/``-p``
command option, which can be specified multiple times.
For details, see :ref:`Specifying CIM property and parameter values`.

The return value and output parameters are displayed using
:term:`CIM object output formats`.

Example:

.. code-block:: text

    $ pywbemcli --mock-server tests/unit/all_types.mof --mock-server tests/unit/all_types_method_mock.py.py

    pywbemcli> instance invokemethod PyWBEM_AllTypes.InstanceId=\"test_instance\" AllTypesMethod --parameter arrBool=True,False
    ReturnValue=0
    arrBool=true, false

Or using the wildcard to create a selection list for the instance names

.. code-block:: text

    $ pywbemcli --mock-server tests/unit/all_types.mof --mock-server tests/unit/all_types_method_mock.py.py

    pywbemcli> instance invokemethod PyWBEM_AllTypes.? --parameter arrBool=True,False
    Pick Instance name to process
    0: root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"
    1: root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"
    2: root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"
    Input integer between 0 and 2 or Ctrl-C to exit selection: 0   << entered by user
    ReturnValue=0
    arrBool=true, false

See :ref:`pywbemcli instance invokemethod --help` for the exact help output of the command.

.. index:: pair: instance commands; instance modify

.. _`Instance modify command`:

``instance modify`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance modify`` command modifies the properties of an existing CIM
instance.

The specification of the instance name (INSTANCENAME argument) is documented
in the section :ref:`Specifying the INSTANCENAME command argument`.

The new property values are specified by possibly multiple ``--property``/``-p``
command options.
For details, see :ref:`Specifying CIM property and parameter values`.

Note that key properties cannot be modified, as per :term:`DSP0004`.

The ``--propertylist``/``--pl`` command option allows restricting the set of
properties to be modified. It is supported for consistency with the
corresponding parameter at the CIM-XML protocol level, but given that the set
of properties to be modified is already determined by the specified
``--property``/``-p`` command options, the ``--propertylist``/``--pl`` command
option does not need to be specified.

Since the WBEM server (and pywbem) requires that each property be typed,
pywbemcli retrieves the creation class from the WBEM server to determine
the data types for the properties.

The following examples modifies an instance of the class TST_Blah with two
scalar and one array property:

.. code-block:: text

    $ pywbemcli instance modify TST_Blah --property InstancId=blah1 --property IntProp=3 --property IntArr=3,6,9

    $ pywbemcli instance modify TST_Blah --property InstancId=\"blah 2\" --property IntProp=3 --property IntArr=3,6,9

See :ref:`pywbemcli instance modify --help` for the exact help output of the command.

.. index:: pair: instance commands; instance references

.. _`Instance references command`:

``instance references`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance references`` command lists the CIM instances that reference
the specified source instance.

The specification of the instance name (INSTANCENAME argument) is documented
in the section :ref:`Specifying the INSTANCENAME command argument`.

If the ``--names-only``/``--no`` command option is set, only the instance paths
are displayed. Otherwise, the instances are displayed.

Valid output formats in both cases are :term:`CIM object output formats` or
:term:`Table output formats`.

Note: This command returns the instance references, not the class references.
The :ref:`Class references command` returns the class references.

Example:

.. code-block:: text

    $ pywbemcli --name mymock instance references root/cimv2:TST_Person.name=\"Saara\"
    instance of TST_Lineage {
       InstanceID = "SaaraSofi";
       parent = "/root/cimv2:TST_Person.name=\"Saara\"";
       child = "/root/cimv2:TST_Person.name=\"Sofi\"";
    };

See :ref:`pywbemcli instance references --help` for the exact help output of the command.

.. index:: pair: instance commands; instance query

.. _`Instance query command`:

``instance query`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance query`` command executes a query for CIM instances in a
namespace.

The query is specified with the ``QUERY`` argument and must be a valid query
in the query language specified with the ``--query-language``/``--ql`` command
option. The default for that option is ``DMTF:CQL`` (see :term:`CQL`).

The namespace is specified with the ``--namespace``/``-n`` command option, or
otherwise is the default namespace of the connection.

Valid output formats are :term:`CIM object output formats` or
:term:`Table output formats`.

See :ref:`pywbemcli instance query --help` for the exact help output of the command.

.. index:: pair: instance commands; instance shrub

.. _`Instance shrub command`:

``instance shrub`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instance shrub`` command executes a set of requests to get the
association relationships for a non-association CIM instance defined by
INSTANCENAME in a namespace and displays the result either as tree in ascii
or as a table showing the roles, reference classes, associated
classes and associated instances for the input instance.

A shrub is a structure that attempts to show all of the relationships and the
paths between the input INSTANCENAME and the associated instances whereas the
References command only shows referencing(associator) classes or instances and
the Associators command only shows associated classes or instances.

The namespace for the INSTANCENAME is specified with the ``-namespace``/``-n``
command option, or otherwise is the default namespace of the connection.

Valid output formats are :term:`Table output formats` or the default which
displays the a visual tree.

The ``instance shrub`` command includes command options to:

1. ``--summary``/``-s``: Show only the class components and a count of instances.

2. ``--fullpath``/``-f``: Show the full path of the instances.  The
   default is to attempt to shorten the path by removing path components that
   are the same for all instances displayed.  This can be important for some
   of the components of the model where instance paths include keys like
   ``CreationClassName`` and 'SystemCreationClassName'which are either already
   known or do not distinguish instances but make the instance name difficult
   to visualize on the console. These key bindings are replaced with the
   character ``~`` as a placemarker unless the ``--fullpath``/``-f`` option is
   defined.

Thus, a full path might look like:

   ``/:CIM_FCPort.SystemCreationClassName="CIM_ComputerSystem",SystemName="ACME+CF2A5091300089",CreationClassName="CIM_FCPort",DeviceID="ACME+CF2A5091300089+SP_A+10"``

But the shortened path would be:

   ``/:CIM_FCPort.~,~,~,DeviceID="ACME+CF2A5091300089+SP_A+10"``

This command is primarily a diagnostic and test tool to help users understand what
comprises CIM association relationships.

See :ref:`pywbemcli instance shrub --help` for the exact help output of the command.

Example:

.. code-block:: text

    $ pywbemcli instance shrub root/cimv2:TST_EP.InstanceID=1

    TST_EP.InstanceID=1
     +-- Initiator(Role)
         +-- TST_A3(AssocClass)
             +-- Target(ResultRole)
             |   +-- TST_EP(ResultClass)(3 insts)
             |       +-- TST_EP.InstanceID=2(refinst:0)
             |       +-- TST_EP.InstanceID=5(refinst:1)
             |       +-- TST_EP.InstanceID=7(refinst:2)
             +-- LogicalUnit(ResultRole)
                 +-- TST_LD(ResultClass)(3 insts)
                     +-- TST_LD.InstanceID=3(refinst:0)
                     +-- TST_LD.InstanceID=6(refinst:1)
                     +-- TST_LD.InstanceID=8(refinst:2)

This displays the Role (Initiator), AssociationClass (TST_A3), etc for the
instance name defined in the command which is a complex association that
contains 3 reference properties.  The tag ``refinst`` on each instance
defines the corresponding reference instance so that the instances
returned can be correlated back to their reference instances.

The resulting table output for the same command but with ``-o table`` is:

Example:

.. code-block:: text

    $ pywbemcli -o table instance shrub root/cimv2:TST_EP.InstanceID=1

    Shrub of root/cimv2:TST_EP.InstanceID=1
    +-----------+-------------------+--------------+--------------------+-------------------------+
    | Role      | Reference Class   | ResultRole   | Associated Class   | Assoc Inst paths        |
    |-----------+-------------------+--------------+--------------------+-------------------------|
    | Initiator | TST_A3            | Target       | TST_EP             | /:TST_EP.               |
    |           |                   |              |                    | InstanceID=2(refinst:0) |
    |           |                   |              |                    | /:TST_EP.               |
    |           |                   |              |                    | InstanceID=5(refinst:1) |
    |           |                   |              |                    | /:TST_EP.               |
    |           |                   |              |                    | InstanceID=7(refinst:2) |
    | Initiator | TST_A3            | LogicalUnit  | TST_LD             | /:TST_LD.               |
    |           |                   |              |                    | InstanceID=3(refinst:0) |
    |           |                   |              |                    | /:TST_LD.               |
    |           |                   |              |                    | InstanceID=6(refinst:1) |
    |           |                   |              |                    | /:TST_LD.               |
    |           |                   |              |                    | InstanceID=8(refinst:2) |
    +-----------+-------------------+--------------+--------------------+-------------------------+

.. index:: pair: command groups; qualifier commands

.. _`Qualifier command group`:

``qualifier`` command group
---------------------------

The ``qualifier`` command group has commands that act on CIM qualifier
declarations:

* :ref:`qualifier get command` - Get a qualifier declaration.
* :ref:`qualifier enumerate command` - List the qualifier declarations in a
  namespace.

.. index:: pair: qualifier commands; qualifier get

.. _`Qualifier get command`:

``qualifier get`` command
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``qualifier get`` command gets the specified qualifier declaration.

The qualifier declaration is named with the ``QUALIFIERNAME`` argument and is
in the namespace specified with the ``-namespace``/``-n`` command option, or
otherwise in the default namespace of the connection.

The qualifier declaration is displayed using :term:`CIM object output formats`
or :term:`Table output formats`.

The following example gets the ``Key`` qualifier declaration from the
default namespace:

.. code-block:: text

    $ pywbemcli --name mymock qualifier get Key
    Qualifier Key : boolean = false,
        Scope(property, reference),
        Flavor(DisableOverride, ToSubclass);

See :ref:`pywbemcli qualifier get --help` for the exact help output of the command.

.. index:: pair: qualifier commands; qualifier enumerate

.. _`Qualifier enumerate command`:

``qualifier enumerate`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``qualifier enumerate`` command enumerates the qualifier declarations in
a namespace.

The namespace is specified with the ``-namespace``/``-n`` command option, or
otherwise is the default namespace of the connection.

The qualifier declaration is displayed using :term:`CIM object output formats`
or :term:`Table output formats`.

This example displays all of the qualifier declarations in the default
namespace as a table:

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

See :ref:`pywbemcli qualifier enumerate --help` for the exact help output of the command.

.. index:: pair: command groups; profile commands

.. _`Profile command group`:

``profile`` command group
-------------------------
* :ref:`Profile list command` - List management profiles advertised by the server.
* :ref:`Profile centralinsts command` - List central instances of management profiles on the server.

.. index:: pair: profile commands; profile list

.. _`Profile list command`:

``Profile list`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``profile list`` command lists the
:term:`management profiles <management profile>` advertised by the
WBEM server of the :term:`current connection`.

The returned management profiles are displayed with organization, profile name,
and profile version using the :term:`Table output formats`.

The ``--organization``/``-o`` and ``--profile``/ ``-p`` command options can be
used to filter the returned management profiles by organization and profile
name, respectively.

Example:

.. code-block:: text

    $ pywbemcli --name myserver --output-format simple profile list
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

See :ref:`pywbemcli profile list --help` for the exact help output of the command.

.. index:: pair: sprofile commands; profile centralinsts

.. _`Profile centralinsts command`:

``profile centralinsts`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``profile centralinsts`` command gets the :term:`central instances`
of the :term:`management profiles <management profile>` advertised by the
WBEM server of the :term:`current connection`.

The command displays the instance paths of the central instances by profile,
using the :term:`Table output formats`.

The ``--organization``/``-o`` and ``--profile``/ ``-p`` command options can be
used to filter the result by organization and name of the management profiles,
respectively.

Example:

.. code-block:: text

    $ pywbemcli profile centralinsts --organization DMTF --profile "Computer System"
    Advertised Central Instances:
    +---------------------------------+----------------------------------------------------------------------------------------------------------------------+
    | Profile                         | Central Instances                                                                                                    |
    |---------------------------------+----------------------------------------------------------------------------------------------------------------------|
    | DMTF:Computer System:1.0.0      | //leonard/test/TestProvider:Test_StorageSystem.Name="StorageSystemInstance1",CreationClassName="Test_StorageSystem"  |
    |                                 | //leonard/test/TestProvider:Test_StorageSystem.Name="StorageSystemInstance2",CreationClassName="Test_StorageSystem"  |
    +---------------------------------+----------------------------------------------------------------------------------------------------------------------+

See :ref:`pywbemcli profile centralinsts --help` for the exact help output of the command.

.. _`Server command group`:

``server`` command group
------------------------

The ``server`` command group has commands that interact with the WBEM
server of the :term:`current connection` to access information about the
WBEM server itself:

* :ref:`Server brand command` - Get the brand of the server.
* :ref:`Server info command` - Get information about the server.
* :ref:`Server interop command` - Get the Interop namespace of the server.
* :ref:`Server namespaces command` - List the namespaces of the server.

.. index:: pair: server commands; server brand

.. _`Server brand command`:

``server brand`` command
^^^^^^^^^^^^^^^^^^^^^^^^

The ``server brand`` command gets the brand of the WBEM server of the
:term:`current connection`.

The brand is intended to identify the product that represents the WBEM server
infrastructure. Since that was not clearly defined in the DMTF
specifications, this command may return strange results for some servers, but
it returns legitimate results for the most commonly used servers.

The brand is displayed using :term:`Table output formats`.

Example:

.. code-block:: text

    $ pywbemcli --name myserver server brand
    Server Brand:
    +---------------------+
    | WBEM server brand   |
    |---------------------|
    | OpenPegasus         |
    +---------------------+

See :ref:`pywbemcli server brand --help` for the exact help output of the command.

.. index:: pair: server commands; server info

.. _`Server info command`:

``server info`` command
^^^^^^^^^^^^^^^^^^^^^^^

The ``server info`` command gets general information on the WBEM server of the
:term:`current connection`.

This includes the brand, version, namespaces, and other reasonable information
on the WBEM server.

The result is displayed using :term:`Table output formats`.

Example:

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

See :ref:`pywbemcli server info --help` for the exact help output of the command.

.. index:: pair: server commands; server interop

.. _`Server interop command`:

``server interop`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``server interop`` command gets the name of the Interop namespace of the
WBEM server of the :term:`current connection`.

The result is displayed using :term:`Table output formats`.

Example:

.. code-block:: text

    $ pywbemcli --name myserver server interop
    Server Interop Namespace:
    +------------------+
    | Namespace Name   |
    |------------------|
    | root/PG_InterOp  |
    +------------------+

See :ref:`pywbemcli server interop --help` for the exact help output of the command.

.. index:: pair: server commands; server namespaces

.. _`Server namespaces command`:

``server namespaces`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``server namespaces`` command lists the namespaces of the WBEM server of
the :term:`current connection`.

The result is displayed using :term:`Table output formats`.

Example:

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

See :ref:`pywbemcli server namespaces --help` for the exact help output of the command.

.. index:: pair: command groups;connection commands

.. _`Connection command group`:

``connection`` command group
----------------------------

The ``connection`` command group has commands that manage named connection
definitions that are persisted in a :term:`connections file`.
This allows maintaining multiple connection definitions and then using any
one via the :ref:`--name general option`. Only a single connection is
active (selected) at any point in time but the connection connection can
be selected on the pywbemcli command line (:ref:`--name general option`) or
changed within an interactive session using the :ref:`Connection select command`

.. index:: pair: connections file; persistent connection attributes

The attributes of each connection definition in the :term:`connections file` are:

* **name** - name of the connection definition. See :ref:`--name general option`.
* **server** - URL of the WBEM server, or None if the connection definition is
  for a mock WBEM server. See :ref:`--server general option`.
* **default-namespace** - default namespace for the WBEM server. See :ref:`--default-namespace general option`.
* **user** - user name for the WBEM server. See :ref:`--user general option`.
* **password** - password for the WBEM server. See :ref:`--password general option`.
* **use-pull** - determines whether the pull operations are to be used for
  the WBEM server. See :ref:`--use-pull general option`.
* **verify** - a boolean flag controlling whether the pywbem client verifies
  any certificate received from the WBEM server. See :ref:`--verify general option`.
* **certfile** - path name of the server certificate file. See :ref:`--certfile general option`.
* **keyfile** - path name of the client private key file. See :ref:`--keyfile general option`.
* **timeout** - client-side timeout for operations against the WBEM server. See :ref:`--timeout general option`.
* **mock-server** - list of files defining the setup of the mock WBEM server,
  or None if the connection definition is for a real WBEM server.
  See :ref:`--mock-server general option`.

The commands in this group are:

* :ref:`Connection delete command` - Delete a WBEM connection definition.
* :ref:`Connection export command` - Export the current connection.
* :ref:`Connection list command` - List the WBEM connection definitions.
* :ref:`Connection save command` - Save the current connection to a new WBEM connection definition.
* :ref:`Connection select command` - Select a WBEM connection definition as current or default.
* :ref:`Connection show command` - Show connection info of a WBEM connection definition.
* :ref:`Connection test command` - Test the current connection with a predefined WBEM request.

.. index:: pair: connection commands; connection delete

.. _`Connection delete command`:

``connection delete`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``connection delete`` command deletes a connection definition from the
:term:`connections file`.

If the ``NAME`` argument is specified, the connection definition with that name
is deleted. Otherwise, the command displays the list of connection definitions
and prompts the user to select the one to be deleted. If there is only a
single connection, that connection is deleted without the user selection
request.

Example that deletes a connection definition by the specified name:

.. code-block:: text

    $ pywbemcli connection delete me

Example that deletes a connection definition by selecting it:

.. code-block:: text

    $ pywbemcli connection delete
    Select a connection or Ctrl_C to abort.
    0: mock1
    1: mockassoc
    2: op
    Input integer between 0 and 2 or Ctrl-C to exit selection: 1   << entered by user
    Deleted connection "mockassoc".

See :ref:`pywbemcli connection delete --help` for the exact help output of the command.

.. index:: pair: connection commands; connection export

.. _`Connection export command`:

``connection export`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``connection export`` command exports the current connection as a set of
environment variables.

This is done by displaying the commands to set the environment variables.

.. code-block:: text

    $ pywbemcli --server http://localhost connection export
    export PYWBEMCLI_SERVER=http://localhost
    export PYWBEMCLI_DEFAULT_NAMESPACE=root/cimv2
    export PYWBEMCLI_TIMEOUT=30
    . . .

This can be used for example on Linux and OS-X to set the environment variables
as follows:

.. code-block:: text

    $ eval $(pywbemcli --server http://localhost connection export)

    $ env |grep PYWBEMCLI
    PYWBEMCLI_SERVER=http://localhost
    PYWBEMCLI_DEFAULT_NAMESPACE=root/cimv2
    PYWBEMCLI_TIMEOUT=30
    . . .

See :ref:`pywbemcli connection export --help` for the exact help output of the command.

.. index:: pair: connection commands; connection list

.. _`Connection list command`:

``connection list`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``connection list`` command lists the connection definitions in the
:term:`connections file` and the current connection(if it has not been
saved to the connections file).

Valid output formats are :term:`Table output formats`.

This shows which connection is the current connection
and if any connection is set as the default connection (:ref:`Connection select
command` ).

The current connection is marked with `*` in the Name column.
The default connection, if defined, is marked with `#` in the Name column.

The title also displays the path of the file that is being used as the
current connections file.

.. code-block:: text

    pywbemcli> --server http://localhost --user me --password mypw --no-verify connection save me

    pywbemcli> --server http://blahblah connection list
    WBEM server connections(brief):  (#: default, *: current)
    file: /home/johndoe/.pywbemcli_connections.yaml
    +--------------+------------------+----------------------------------------+
    | name         | server           | mock-server                            |
    |--------------+------------------+----------------------------------------|
    | *blahblah    | http://blah      |                                        |
    | mock1        |                  | tests/unit/simple_mock_model.mof       |
    | mockalltypes |                  | tests/unit/all_types.mof               |
    | mockassoc    |                  | tests/unit/simple_assoc_mock_model.mof |
    | mockext      |                  | tests/unit/simple_mock_model_ext.mof   |
    | op           | http://localhost |                                        |
    | test3        |                  | tests/unit/simple_mock_model.mof       |
    |              |                  | tests/unit/mock_confirm_y.py           |
    +--------------+------------------+----------------------------------------+

A more complete display of the server parameters is available with the
`--full` option as follows:

.. code-block:: text

    pywbemcli> connection list --full

    WBEM server connections(full): (#: default, *: current)
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | name         | server               | namespace              | user        |   timeout | use_pull   | verify   | certfile   | keyfile   | mock-server                                      |
    +==============+======================+========================+=============+===========+============+==========+============+===========+==================================================+
    | #mockassoc   |                      | root/cimv2             |             |        30 |            | True     |            |           | tests/unit/simple_assoc_mock_model.mof           |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | alltypes     |                      | root/cimv2             |             |        30 |            | True     |            |           | tests/unit/all_types.mof                         |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | complexassoc |                      | root/cimv2             |             |        30 |            | True     |            |           | tests/unit/complex_assoc_model.mof               |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | mock1        |                      | root/cimv2             |             |        30 |            | True     |            |           | tests/unit/simple_mock_model.mof                 |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | mock1ext     |                      | root/cimv2             |             |        30 |            | True     |            |           | tests/unit/simple_mock_model_ext.mof             |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | mock1interop |                      | interop                |             |        30 |            | True     |            |           | tests/unit/simple_mock_model.mof                 |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | ophttp       | http://localhost     | root/cimv2             |             |        30 |            | True     |            |           |                                                  |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | ophttps      | https://localhost    | root/cimv2             | blahblah    |        30 |            | False    |            |           |                                                  |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | opt          | https://blah         | root/cimv2             |             |        45 |            | False    | c1.pem     | k1.pem    |                                                  |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+
    | test1        |                      | root/cimv2             |             |        30 |            | True     |            |           | tests/unit/simple_assoc_mock_model.mof           |
    +--------------+----------------------+------------------------+-------------+-----------+------------+----------+------------+-----------+--------------------------------------------------+


`Connection list` does not display some fields such as the ca-certs field.  See
:ref:`Connection show command` for more detailed display of individual fields
used by the server.

See :ref:`pywbemcli connection list --help` for the exact help output of the command.

.. index:: pair: connection commands; connection save

.. _`Connection save command`:

``connection save`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``connection save`` command saves the current connection in the
:term:`connections file` as a connection definition with the name specified
in the ``NAME`` argument.

If a connection definition with that name already exists, it will be overwritten
without notice.

See :ref:`pywbemcli connection save --help` for the exact help output of the command.

.. index:: pair: connection commands; connection select

.. _`Connection select command`:

``connection select`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``connection select`` command selects a connection definition from the
:term:`connections file` to become the current connection.

If the ``NAME`` argument is specified, the connection definition with that name
is selected. Otherwise, the command displays the list of connection definitions
and prompts the user to pick the one to be selected. If there is only a
single connection, that connection is selected without the user
request.

If the ``--default``/``-d`` command option is set, the connection definition in
addition becomes the default connection, by marking it accordingly in the
:term:`connections file`.

The following example shows changing connection from within the interactive
mode of pywbemcli:

.. code-block:: text

    $ pywbemcli

    pywbemcli> connection select
    Select a connection or Ctrl_C to abort.
    0: mock1
    1: mockassoc
    2: op
    Input integer between 0 and 2 or Ctrl-C to exit selection: 1   << entered by user

    pywbemcli> connection list
    WBEMServer Connections:   (#: default, *: current)
    +------------+------------------+-------------+-------------+-----------+------------+-----------------------------------------+
    | name       | server           | namespace   | user        |   timeout | verify     | mock-server                             |
    |------------+------------------+-------------+-------------+-----------+------------+-----------------------------------------|
    | mock1      |                  | root/cimv2  |             |        30 | False      | tests/unit/simple_mock_model.mof        |
    | *mockassoc |                  | root/cimv2  |             |        30 | False      | tests/unit/simple_assoc_mock_model.mof  |
    | op         | http://localhost | root/cimv2  | me          |        30 | True       |                                         |
    +------------+------------------+-------------+-------------+-----------+------------+-----------------------------------------+

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

See :ref:`pywbemcli connection select --help` for the exact help output of the command.

.. index:: pair: connection commands; connection show

.. _`Connection show command`:

``connection show`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: single: connection show command
.. index:: pair: command; connection show

The ``connection show`` command shows information about a connection definition:

* If ``NAME`` is ``?``, pywbemcli prompts the user to select one and shows
  the existing current connection. If there is only a single connection the
  user selection is bypassed.
* If ``NAME`` is specified, show the connection definition with that name.
* If ``NAME`` is not specified, show the existing current connection.

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

See :ref:`pywbemcli connection show --help` for the exact help output of the command.

.. index:: pair: connection commands; connection test

.. _`Connection test command`:

``connection test`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
    single: connection test command
    pair: command; connection test

The ``connection test`` command executes a single predefined operation on
the current connection to verify that accessing the WBEM server works.

The predefined operation is ``EnumerateClasses`` which attempts to enumerate
the classes in the default namespace of the WBEM Server.  Even if the server
does not support the classes operations, this command should return a
CIMError indicating that WBEM is supported (ex. CIM_ERR_NOT_SUPPORTED)
indicating that WBEM is supported by the server.

If the `--test-pull` command option is included, pywbemcli will issue an
instances request for each of the DMTF defined pull operations and report the
results. This could be important because the pull operations are defined
as optional and some server may not include them.

If the server accepts the request, a simple text ``OK <server url``
will be returned.

The following example defines the connection with ``--server``, ``--user``,
and ``--password`` and executes the test with successful result:

.. code-block:: text

    $ pywbemcli --server http://localhost --user me --password mypw connection test
    Connection successful

See :ref:`pywbemcli connection test --help` for the exact help output of the command.

.. index:: pair: repl; command

.. _`Repl command`:

``repl`` command
----------------

.. index::
    single: repl command
    pair: command; repl
    pair: repl; interactive mode

The ``repl`` command sets pywbemcli into the :ref:`interactive mode`. Pywbemcli
can be started in the :ref:`interactive mode` either by entering:

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

Command history is available in the :ref:`interactive mode` either by using
<UP-ARROW> and <DOWN-ARROW> keys to step through the history file or by using
incremental search of the command history.

An incremental search is initiated by <CTRL-r> (similar to some shells like
bash) and does a search based on a string entered after the <CTRL-r> for the
last command containing the search string. The search string may be modified
and <UP_ARROW>, <DOWN-ARROW> will find other commands containing the search
string. Hitting <ENTER> selects the currently shown command.

see :ref:`interactive mode` for more details on using this mode and the
search.

.. index:: pair: help; command

.. _`Help command`:

``help`` command
----------------

.. index::
    single: help command
    pair: help; command

The ``help`` command provides information on special commands and controls
that can be executed in the :ref:`interactive mode` including:

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
