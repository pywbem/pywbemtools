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

The command groups are:

* :ref:`Class command group` - Command group for CIM classes.
* :ref:`Instance command group` - Command group for CIM instances.
* :ref:`Namespace command group` - Command group for Namespace management.
* :ref:`Profile command group` - Command group for WBEM management profiles.
* :ref:`Qualifier command group` - Command group for CIM qualifier declarations.
* :ref:`Server command group` - Command group for WBEM servers.
* :ref:`Statistics command group` - Command group for WBEM operation statistics.
* :ref:`Subscription command group` - Command group for WBEM operation statistics.
* :ref:`Connection command group` - Command group for WBEM connection definitions.

The individual commands (no command group) are:
* :ref:`help command` - Show help message for interactive mode.
* :ref:`repl command` - Enter interactive mode (default).


.. index:: pair: command groups; namespace commands

.. _`Namespace command group`:

``namespace`` command group
---------------------------

The ``namespace`` command group has commands that act on CIM namespaces:

* :ref:`Namespace list command` - List the namespaces on the server.
* :ref:`Namespace create command` - Create a namespace on the server.
* :ref:`Namespace delete command` - Delete a namespace on the server.
* :ref:`Namespace interop command` - Get the Interop namespace on the server.

See :ref:`pywbemcli namespace --help`.


.. index::
    pair: namespace commands; namespace list

.. _`Namespace list command`:

``namespace list`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``namespace list`` command lists the namespaces of the WBEM server of
the :term:`current connection`.

The result is displayed using ``txt`` output format or
:term:`Table output formats`.

The Interop namespace must exist on the server.

Example:

.. code-block:: text

    $ pywbemcli --name myserver --output-format plain namespace list
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

See :ref:`pywbemcli namespace list --help` for the exact help output of the command.


.. index::
    pair: namespace commands; namespace create

.. _`Namespace create command`:

``namespace create`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``namespace create`` command creates a CIM namespace on the WBEM server of
the :term:`current connection`.

Leading and trailing slash (``/``) characters specified in the NAMESPACE
argument will be stripped.

The namespace must not yet exist on the server.

The Interop namespace must exist on the server and cannot be created using
this command.

WBEM servers may not allow this operation or may severely limit the
conditions under which a namespace can be created on the server.

Example:

.. code-block:: text

    $ pywbemcli --name mymock namespace create /root/abc
    Created namespace root/abc

See :ref:`pywbemcli namespace create --help` for the exact help output of the command.


.. index::
    pair: namespace commands; namespace delete

.. _`Namespace delete command`:

``namespace delete`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``namespace delete`` command deletes a CIM namespace from the WBEM server of
the :term:`current connection`.

Leading and trailing slash (``/``) characters specified in the NAMESPACE
argument will be stripped.

The namespace must exist and must be empty. That is, it must not contain
any objects (qualifiers, classes or instances).

The Interop namespace must exist on the server and cannot be deleted using
this command.

WBEM servers may not allow this operation or may severely limit the
conditions under which a namespace can be deleted.

Example:

.. code-block:: text

    $ pywbemcli --name mymock namespace delete /root/abc
    Deleted namespace root/abc

See :ref:`pywbemcli namespace delete --help` for the exact help output of the command.


.. index::
    pair: namespace commands; namespace interop

.. _`Namespace interop command`:

``namespace interop`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``namespace interop`` command gets and displays the Interop namespace of
the WBEM server of the :term:`current connection`.

The Interop namespace must exist on the server.

Example:

.. code-block:: text

    $ pywbemcli --name mymock namespace interop
    root/interop

See :ref:`pywbemcli namespace interop --help` for the exact help output of the command.


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

The following example enumerates the class names of the root classes in the
default namespace because there is no classname and the --DeepInheritance
option is not specified:

.. code-block:: text

    $ pywbemcli --name mymock class enumerate --names-only
    TST_Person
    TST_Lineage
    TST_MemberOfFamilyCollection
    TST_FamilyCollection

.. index:: pair: result filters; class enumerate command

The ``class enumerate`` command includes result filter options that filter returned
classes to display only those classes that have the defined filter option.
Thus, ``pywbemcli class enumerate --association`` displays only classes that
have the Association qualifier set. The filters are documented in the `class
filter options table`_ .

.. index:: single: result filters; class enumerate command

.. _class filter options table:

.. table: Class/qualifier filter options

==========================================  =======================================
Filter option name                          Component filtered
==========================================  =======================================
``--association``/``--no-association``      Association qualifier(class) (see Note 1)
``--indication``/``--no-indication``        Indications qualifier(class)
``--experimental``/``--no-experimental``    Experimental qualifier(class)
``--deprecated``/``--no-deprecated``        Deprecated qualifier (any class element)
``--since <CIM_Version_string>``            Version qualifier GE <CIM_Version_string> (see Note 2)
``--schema <schema_string>``                Schema component of classname equality(see Note 3)
``--subclasses <classname>``                Subclasses of <classname>.
``--leaf-classes``                          Classes with no subclass.
==========================================  =======================================

1. The filters defined as ``--...``/``--no-...`` allow testing for the existence
   of the condition (association qualifier exists) or the non-existence(association
   qualifier does not exist on the class). When neither definition of the
   option is defined the association qualifier is ignored in the filtering.
   This applies to boolean qualifier declarations.
2. The CIM version string value in the Version qualifier is defined as 3 integers
   separated by periods  (ex. 2.14.0). All 3 integers must exist.
3. The schema component is True if the schema component of classname (characters
   before "_" match <schema_string>). Ex --schema "CIM"
4. The ``--leaf-classes`` filter can be important because the pywbem MOF compiler
   can compile all dependent classes given only the leaf classes.

If multiple filter options are applied, all of the boolean options must be true for
the class to be displayed and only the classes that pass non-boolean filters
(ex. ``--schema CIM``) for the classes to be displayed.

Thus, for example:

* the combination of ``--subclass-of CIM_blah`` and
  ``--leaf-classes`` will return all leaf classes that are a subclass of ``CIM_Blah``.
* ``--association`` and ``no-experimental`` will display only classes that have
  the Association qualifier set and the Experimental qualifier not set.

The following example displays classnames that are not associations
(``--no-association``).  The use of ``--deep-inheritance`` option returns the complete
set of classes in the namespace rather than just direct subclasses (in this case
the root classes).

.. code-block:: text

    $ pywbemcli --name mymock class enumerate --no --deep-inheritance --no-association
    TST_Person
    TST_Lineage

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

.. index:: pair: result filters; class find command

The ``class find`` command includes filter options that filter returned classes
to display only those classes that have the defined filter options.  Thus,
``pywbemcli class enumerate --association`` displays only classes that have the
Association qualifier set. The filters are documented in the `class filter
options table`_ .

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


Options to the `class tree` command allow the following:

1. Display the superclass hierarchy for a given class (``--superclasses``/``-s``)
   as shown in the following example:

Example:

.. code-block:: text

    $ pywbemcli -n mock1 class tree CIM_Foo_Sub2 -s
    root
     +-- CIM_Foo
         +-- CIM_Foo_sub2

2. Display additional information about each class (``--detail``/``-d``) including
   the value of the Version qualifier and the existence of the class the
   Association, Indication, Abstract qualifiers if they are True as shown in
   the following example:

Example:

.. code-block:: text

    $ pywbemcli -m tests/unit/tree_test_model.mof class tree --detail
    root
     +-- CIM_Foo (Version=2.30.0)
     |   +-- CIM_Foo_sub (Version=2.31.0)
     |       +-- CIM_Foo_sub_sub (Version=2.20.1)
     +-- CIM_Foo_no_version ()
     +-- CIM_Indication (Abstract,Indication,Version=2.24.0)
     +-- CIM_Indication_no_version (Abstract,Indication)
     +-- TST_Lineage (Association,Version=2.20.1)
     +-- TST_Lineage_no_version (Association)


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

.. index:: pair: result filters; instance count command

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

Key properties cannot be modified, as per :term:`DSP0004`.

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
INSTANCENAME in a namespace and displays the result either as tree in ASCII
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
   ``CreationClassName`` and ``SystemCreationClassName`` which are either already
   known or do not distinguish instances but make the instance name difficult
   to visualize on the console. These key bindings are replaced with the
   character ``~`` as a place-marker unless the ``--fullpath``/``-f`` option is
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

This displays the ``Role`` (Initiator), ``AssociationClass`` (TST_A3), etc. for the
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
* :ref:`qualifier delete command` - Delete a qualifier declaration.
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

.. index:: pair: qualifier commands; qualifier delete

.. _`Qualifier delete command`:

``qualifier delete`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``qualifier delete`` command deletes the specified qualifier declaration.

The qualifier declaration is named with the ``QUALIFIERNAME`` argument and is
in the namespace specified with the ``-namespace``/``-n`` command option, or
otherwise in the default namespace of the connection.

The qualifier declaration is deleted using the DeleteQualifier operation.
It is left to the WBEM server to reject the deletion if the qualifier is used
anywhere.

The following example deletes the ``Xyz`` qualifier declaration from the
default namespace:

.. code-block:: text

    $ pywbemcli --name mymock qualifier delete Xyz
    Deleted qualifier Xyz

See :ref:`pywbemcli qualifier delete --help` for the exact help output of the command.

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
* :ref:`Server add-mof command` - Compile the MOF files defined.
* :ref:`Server remove-mof command` - Remove the MOF objects from the server.
* :ref:`Server schema command` - List the namespaces of the server.

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

The result is displayed using ``txt`` output format or
:term:`Table output formats`.

The Interop namespace must exist on the server.

Example:

.. code-block:: text

    $ pywbemcli --name myserver --output-format plain server namespaces
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

.. index:: pair: server commands; server add-mof

.. _`Server add-mof command`:

``server add-mof`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``server add-mof`` command compiles one or more MOF files and adds the
resulting CIM objects to the target namespace in the WBEM server of the
:term:`current connection`.

Example:

.. code-block:: text

    $ pywbemcli --name myserver server add-mof mymodel.mof

See :ref:`pywbemcli server add-mof --help` for the exact help output of the
command.


.. index:: pair: server commands; server remove-mof

.. _`Server remove-mof command`:

``server remove-mof`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``server remove-mof`` command compiles one or more MOF files and removes the
resulting CIM objects from the target namespace in the WBEM server of the
:term:`current connection`.

Example:

.. code-block:: text

    $ pywbemcli --name myserver server remove-mof mymodel.mof

See :ref:`pywbemcli server remove-mof --help` for the exact help output of the
command.

.. _`Server schema command`:

``server schema`` command
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``server schema`` command returns information on the
:term:`schemas <schema>` in the namespace(s) of the :term:`current connection`
WBEM server.

The overview reports a summary by namespace of this information and the
detail view (``server schema --detail``) reports the information for each
:term:`schema` in the namespace.

For each schema in each namespace, the report provides information on the
:term:`CIM Schema` version (maximum qualifier 'Version' for classes in that
:term:`schema`), whether the :term:`schemas <schema>` have experimental
classes, and the number of classes in each :term:`schema` and
:term:`CIM Schema`.

Pywbemcli determines the version of the :term:`CIM Schema` by finding the highest
value of the ``Version`` qualifier on any of the classes in the namespace that
are in that :term:`schema`

There are two report outputs possible:

* Detail report (``--detail`` option) displays information on the number of classes,
  maximum version for each schema in each or the selected namespace, and
  whether the schema includes any experimental classes.

* The overview output (without ``--detail`` command option) displays information on the
  number of classes, the :term:`CIM Schema` and whether there are experimental
  classes in each or the selected namespace. For the :term:`CIM Schema` in the
  overview report the highest value is determined by finding the highest
  'Version' qualifier value for each :term:`schemas <schema>` in the
  :term:`CIM schema` (normally ``CIM``, or ``PRS``).

Example:

.. code-block:: text

    $ pywbemcli --name myserver server schema

    Schema information; namespaces: all;
    Namespace                      Schemas              classes  CIM schema    experimental
                                                          count  version
    -----------------------------  -----------------  ---------  -------------  --------------
    root                                                      0
    root/PG_InterOp                CIM, PG                  276  2.40.0
    root/benchmark                 CIM, (no-schema)         206  2.40.0
    root/cimv2                     CIM, PG, PRS            1463  2.41.0         Experimental


The above report would indicate that the namespace ``root/cimv2`` was probably
created with DMTF released :term:`CIM Schema` version 2.41.0. Other namespaces show a
lower level of version because they are not using any of the classes that
have the ``Version`` qualifier value of 2.41.0.

or a more detailed report (``--detail`` option):

.. code-block:: text

    $ pywbemcli --name myserver server schema --detail

    Namespace                      Schemas              classes  schema     experimental
                                                          count  version
    -----------------------------  -----------------  ---------  ---------  --------------
    root/PG_InterOp                CIM                      241  2.40.0
                                   PG                        35  2.12.0
    root/benchmark                 CIM                      177  2.40.0
                                   (no-schema)               29  1.0.0
    root/cimv2                     CIM                     1382  2.41.0     Experimental
                                   PG                        20  2.12.0

This report tells more about each :term:`schema` in that it reports that there
are classes in the ``root/cimv2`` namespace 'CIM' schema that are experimental
indicating that the :term:`CIM Schema` used was the Version 2.41.0, experimental
:term:`CIM Schema`.

See :ref:`pywbemcli server remove-mof --help` for the exact help output of the
command.


.. index:: pair: command groups;statistics command group

.. _`Statistics command group`:

``statistics`` command group
----------------------------

The ``statistics`` command group includes commands that display statistics
about the WBEM operations executed by a real WBEM server (or by a mock
environment).

.. index:: pair: Operation statistics;statistics commands

.. _Operation statistics:

Statistics on WBEM operations are maintained by the pywbemcli client, and also
separately by WBEM servers that support this. There are multiple components to
statistics gathering and reporting in pywbemcli:

1.  Pywbemcli gathers and maintains statistics on WBEM operations it executes
    against a WBEM server (or mock environment). The client maintained
    statistics can be displayed either automatically after each pywbemcli
    command if the ``--timestats`` / ``-T`` general option is used, or in
    interactive mode with the ``statistics show`` command.

    For mock environments, artificial operations on the MOF compile time
    needed for setting up the mock respository are included in the client
    maintained statistics.

2.  WBEM servers may support two capabilities for managing statistics on WBEM
    operations:

    a. Each CIM-XML response from the WBEM server may include an extra header
       field ``WBEMServerResponseTime`` with the server response time for that
       operation. Pywbemcli puts those server response times into the client
       statistics it maintains. The inclusion of the server response time
       into the CIM-XML response can be enabled and disabled with the
       ``statistics server-on`` and ``statistics server-off`` commands.

    b. Statistical information on operation execution in the WBEM server and
       its providers may be gathered and maintained and by the WBEM server.
       These server maintained statistics are completely independent of the
       client maintained statistics and will include the operations driven by
       all clients working with that server.
       The gathering of server statistics can be enabled and disabled with the
       ``statistics server-on`` and ``statistics server-off`` commands.
       The server maintained statistics can be retrieved and displayed with the
       ``statistics server-show`` command.

    The mock environment implemented by pywbemcli does not support server
    maintained statistics.

    The capabilities for managing and retrieving server maintained statistics is
    supported only in some WBEM server implementations. While these capabilities
    were documented in the :term:`CIM Schema`, they were never included as part of
    a DMTF or SNIA management profile, so the implementations may vary across
    WBEM server implementations. Pywbemcli makes a best effort to interact with
    the server maintained statistics based on the documentation in the
    :term:`CIM Schema`, and has been verified to work with OpenPegasus.

The statistics commands are:

* :ref:`Statistics reset command` -  Reset client maintained statistics.
* :ref:`Statistics server-on command` - Enable server maintained statistics.
* :ref:`Statistics server-off command` - Disable server maintained statistics.
* :ref:`Statistics server-show command` - Display server maintained statistics.
* :ref:`Statistics show command` -  Display client maintained statistics (interactive mode).
* :ref:`Statistics status command` - Show enabled status of client and server maintained statistics.


.. index:: pair: statistics commands; statistics server-on

.. _`Statistics server-on command`:

``statistics server-on`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``statistics server-on`` command attempts to enable statistics gathering
on the current WBEM server and the returning of the server response time in the
``WBEMServerResponseTime`` header field of the CIM-XML response, by setting the
``GatherStatisticalData`` property to True in the ``CIM_ObjectManager`` instance
for the WBEM server.

See '_Operation statistics'_ for more information on statistics in pywbemcli
and WBEM servers.

Since only some WBEM server implementations actually implement statistics
gathering, the command may fail, for example if the ``CIM_ObjectManager``
class or its property ``GatherStatisticalData`` have not been implemented by the
server, or if the server does not allow a client to modify the property.

Note that this command also affects whether the **Server Time** column of
the client maintained statistics shows a value.


.. index:: pair: statistics commands; statistics server-off

.. _`Statistics server-off command`:

``statistics server-off`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``statistics server-off`` command attempts to disable statistics gathering
on the current WBEM server and the returning of the server response time in the
``WBEMServerResponseTime`` header field of the CIM-XML response, by setting the
``GatherStatisticalData`` property to False in the ``CIM_ObjectManager`` instance
for the WBEM server.

See '_Operation statistics'_ for more information on statistics in pywbemcli
and WBEM servers.

Since only some WBEM server implementations actually implement statistics
gathering, the command may fail, for example if the 'CIM_ObjectManager'
class or its property 'GatherStatisticalData' have not been implemented by the
server, or if the server does not allow a client to modify the property.

Note that this command also affects whether the **Server Time** column of
the client maintained statistics shows a value.


.. index:: pair: statistics commands; statistics status

.. _`Statistics status command`:

``statistics status`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``statistics status`` command displays the enabled status of the
statistic gathering in the current WBEM server and of the automatic display
of the client maintained statistics.

See '_Operation statistics'_ for more information on statistics in pywbemcli
and WBEM servers.


.. index:: pair: statistics commands; statistics reset

.. _`Statistics reset command`:

``statistics reset`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``statistics reset`` command resets the counters of the client maintained
statistics. This includes the server response times returned by the WBEM server
that are part of the client maintained statistics.


.. index:: pair: statistics commands; statistics show

.. _`Statistics show command`:

``statistics show`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``statistics show`` command displays the client maintained statistics.

Using this command only makes sense in interactive mode. In interactive mode,
the statistics is maintained for the entire interactive session, and executing
commands that communicate with the server in the interactive session causes
the statistics counters to be updated.

The following example shows the use of the ``statistics show`` command in
the interactive mode with a real WBEM server:

.. code-block:: text

    $ pywbemcli -n pegasus

    pywbemcli> server brand
    OpenPegasus

    pywbemcli> statistics show
    Client statistics
    Operation                 Count    Errors    Client Time    Server Time    Request Size    Response Size
                                                        [ms]           [ms]             [B]              [B]
    ----------------------  -------  --------  -------------  -------------  --------------  ---------------
    EnumerateInstanceNames        2         1         33.174          1.407             333             6225
    EnumerateInstances            1         0          7.938          2.813             345             3504

The following example shows the use of the ``statistics show`` command in
the interactive mode with a mock environment:

.. code-block:: text

    $ pywbemcli -n mock1

    pywbemcli> class enumerate --di --no
    CIM_Foo
    CIM_Foo_sub
    CIM_Foo_sub2
    CIM_Foo_sub_sub

    pywbemcli> statistics show
    Client statistics
    Operation                    Count    Errors    Client Time    Server Time    Request Size    Response Size
                                                           [ms]           [ms]             [B]              [B]
    -------------------------  -------  --------  -------------  -------------  --------------  ---------------
    compile_mof_file(ns=None)        1         0        149.862              0               0                0
    CreateClass                      4         0          4.075              0               0                0
    CreateInstance                  12         0          1.715              0               0                0
    EnumerateClassNames              1         0          0.167              0               0                0
    SetQualifier                    10         0          0.139              0               0                0

The **Operation** column shows the name of the WBEM operation, plus the
following additional entries:

* compile_mof_file(ns=None)

The **Count** column shows the number of operations executed.

The **Errors** column shows the number of cases where the operation has
resulted in an error at the level of the CIM-XML protocol. The occurrence of
such errors is not necessarily a problem, depending on the logic in the
pywbemcli client program.

All time and size values in this report are average values across the number
of operations executed, rounded to the precision shown.

The **Client Time** column shows the total elapsed time the operation took from
a perspective of the pywbemcli client program. This time includes network time
and server time and most of the time spent in the pywbemcli command. More
specifically, the client time is measured by the statistics support of the
pywbem library directly after the API for executing an operation, so it does
include the creation of the CIM-XML for the request and the parsing of the
CIM-XML for the response, but it does not include any processing in the
code of the pywbemcli command above the pywbem API.

The **Server Time** column shows the total elapsed time the operation took from
a perspective of the WBEM server. It has the same meaning as the Server Time
value shown in the server statistics. This time includes time spent in the
CIM object manager code and time spent in its providers. The Server Time is
obtained from the header field ``WBEMServerResponseTime`` in the CIM-XML
response message; if the WBEM server does not support returning this field or
has it disabled, the Server Time is shown as 0. That is why the Server Time
values for the mock environment example are shown as 0.

The **Request Size** and **Response Size** columns show the size of the HTTP
bodies of the CIM-XML request and response messages, respectively. These values
do not include the size of the HTTP header fields.


.. index:: pair: statistics commands; statistics server-show

.. _`Statistics server-show command`:

``statistics server-show`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``statistics server-show`` command displays the server maintained statistics
of the current WBEM server. What is returned depends on the implementation of
statistics gathering in the WBEM server.

This command does that by retrieving "CIM_CIMOMStatisticalData" instances
associated from the "CIM_ObjectManager" instance representing the WBEM server,
and organizing them into a server statistics report.

The format of the server statistics report of a real WBEM server is shown in the
example below:

.. code-block:: text

    $ pywbemcli -s http://localhost statistics server-show

    Server statistics
    Operation                 Count    Server Time    Provider Time    Request Size    Response Size
                                              [ms]             [ms]             [B]              [B]
    ----------------------  -------  -------------  ---------------  --------------  ---------------
    GetClass                    315          0.239            0                 399             4124
    GetInstance                   4          0.495            0.07              862             3128
    ModifyInstance                4          0.795            0.024            3523              376
    EnumerateInstances          172          1.459            0.341             383            10111
    EnumerateInstanceNames      132          0.913            0.657             377             4102
    OpenEnumerateInstances      156          1.986            0                 616            14506

The **Operation** column shows the name of the WBEM operation.

The **Count** column shows the number of operations executed.

All time and size values in this report are average values across the number
of operations executed, rounded to the precision shown.

The **Server Time** column shows the total elapsed time the operation took from
a perspective of the WBEM server. It has the same meaning as the Server Time
value shown in the client statistics. This time includes time spent in the
CIM object manager code and time spent in any providers.

The **Provider Time** column shows the total elapsed time the operation spent
in the provider from a perspective of the CIM object manager portion of the
WBEM server that calls the provider. OpenPegasus only reports values for
instance providers and reports the values for class and qualifier operations
as 0. Other WBEM servers would typically also do that. The provider time
includes the time spent for performing any actions in the managed system
and also the time spent in any "up-calls" from the provider back to the CIM
object manager portion of the WBEM server (and possibly down to other providers).

The **Request Size** and **Response Size** columns show the size of the CIM-XML
request and response messages, respectively. For OpenPegasus and WBEM servers
that followed the description in CIM_CIMOMStatisticalData.mof, these values
include the size of the HTTP bodies and the size of the HTTP header fields.

Note that statistics gathering in WBEM servers is not standardized in WBEM
management profiles, so the statements above are based on typical
implementations of WBEM servers such as the implementation of OpenPegasus.


.. index:: pair: command groups;connection commands

.. _`Connection command group`:

``connection`` command group
----------------------------

The ``connection`` command group includes commands that manage named connection
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
* :ref:`Connection set-default command` - Sets or clears the default definition in a connections file.


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

The current connection is marked with `*` in the **Name** column.
The default connection, if defined, is marked with `#` in the **Name** column.

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
``--full`` option as follows:

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

This command includes an option (``set-default``) that sets the default
connection of the current connections file to the name of the definition being
saved.

.. code-block:: text

    $ pywbemcli --server http://blah connection save <name> --set-default

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
    | #mock1     |                  | root/cimv2  |             |        30 | False      | tests/unit/simple_mock_model.mof        |
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

If the ``--test-pull`` command option is included, pywbemcli will issue an
instances request for each of the DMTF defined pull operations and report the
results. This could be important because the pull operations are defined
as optional and some servers may not include them or all of them.

If the server accepts the request, a simple text ``OK <server url``
will be returned.

The following example defines the connection with ``--server``, ``--user``,
and ``--password`` and executes the test with successful result:

.. code-block:: text

    $ pywbemcli --server http://localhost --user me --password mypw connection test
    Connection successful

See :ref:`pywbemcli connection test --help` for the exact help output of the command.


.. index:: pair: connection commands; connection set-default

.. _`Connection set-default command`:

``connection set-default`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. index::
    single: connection set-default command
    pair: command; connection set-default

The ``connection set-default`` command sets or clears the
:term:`default-connection-name` attribute  in the currently specified
:term:`connections file`.

The :term:`default-connection-name` attribute allows a connection definition in a
connections file to be loaded on startup without using the ``--name`` option.  If
pywbemcli is started without ``--name``, ``--server``, or ``--mock-server`` options, the
``default-connection-name`` attribute is retrieved from the file and, if defined,
the name in the value of this attribute used as the name of the connection
definition set as current connection.

Thus, for example, if the default connection definition is ``mytests`` the
connection definition for ``mytests`` is created each time pywbemcli is started
with no --server, --mock-server or ``--name`` option.

This command also allows clearing the value of the default connections file
attribute with the ``--clear`` option.

The following demonstrates displaying the connection information for the
current default connection ``mytests``.

.. code-block:: text

    $ pywbemcli connection show

    name: mytests (current, default)
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

    $ pywbemcli connection set-default --clear
      Connection default name cleared replacing None

    $ pywbemcli connection show
      Error: No connection defined

    $ pywbemcli connection set-default mytests
       'mytests' set as default connection

    $ pywbemcli connection show
    WBEM server connections(brief): (#: default, *: current)

    file: tmp.yaml
    name       server           mock-server
    ---------  ---------------  -------------
    *#mytests  http://blah
    blahblah   http://blahblah

The current status of the :term:`default-connection-name` can be viewed with the
:ref:`Connection show command` and :ref:`Connection list command`.

See :ref:`pywbemcli connection set-default --help` for the exact help output
of the command.

.. index:: pair: command groups; subscription commands

.. _`subscription command group`:

``subscription`` command group
------------------------------

A CIM indication subscription consists of instances of 3 separate classes:

1. CIM_IndicationFilter - Defines the filter (using one of the DMTF query languages)
that defines the indications to be generated.
2. CIM_ListenerDestination - Defines a listener destination for indications.
Pywbem and pywbemcli use the subclass CIM_ListenerDestinationCIMXML specifically
that is the protocol supported by the pywbem listener and the pywbemlistener.
3. CIM_IndicationSubscription - A CIM association that links a filter definition
and a listener destination to link the definition of the indication to be
generated and the listener destination for the indication.

Pywbemcli provides commands that allow creating, displaying, and removing the
components of CIM indications from WBEM servers.

The ``subscription`` command group has commands that act on the CIM indication classes
on a WBEM server:

* :ref:`subscription add-destination command` - Add new listener destinations instances to the server.
* :ref:`subscription add-filter command` - Add a new indication filter instance to the server.
* :ref:`subscription add-subscription command` - Add indication subscription instances to the server.
* :ref:`subscription list command` - list overview of indication subscriptions to the server.
* :ref:`subscription list-destinations command` - Display destinations on the server.
* :ref:`subscription list-filters command` - Display filters on the server.
* :ref:`subscription list-subscriptions command` - Display subscriptions on the server.
* :ref:`subscription remove-destination command` - Remove destinations instances from the server.
* :ref:`subscription remove-filter command` - Remove filters from the server.
* :ref:`subscription remove-subscription command` - Remove subscriptions from the server.
* :ref:`subscription remove-server command` - Remove all owned subscriptions from the server.

pywbemtools groups indications with an ownership concept where the instances of
filters, destinations, and subscriptions can be either owned by the pywbemtools
client or permanent.

Owned destinations, filters, and subscriptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Owned CIM instances are created with the :ref:`subscription add-destination
command`, :ref:`subscription add-filter command`, and :ref:`subscription
add-subscription command` and their life cycle is bound to the life cycle of
the registration of a WBEM server with the subscription manager.

Pywbemcli registers a WBEM Server with the registration manager the first time
a ``subscription`` command is executed if a a WBEM server is currently defined
with the ``--name``, ``--server`` or ``--mock-server`` general options.

Owned CIM instances are deleted automatically when their WBEM server is
deregistered from pywbemcli. See :ref:`subscription remove-server command` or
by command with :ref:`subscription remove-destination command`,
:ref:`subscription remove-filter command`, :ref:`subscription
remove-subscription command`.

Owned instances provide a mechanism where the life cycle can be easily
controlled by the pywbemcli client.

Owned instances are identified by pywbemcli using a specific string pattern
in the instance ``Name`` property

Permanent destinations, filters, and subscriptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Permanent CIM instances are created via the subscription manager and their
life cycle is independent of the life cycle of the registration of that WBEM
server with the subscription manager.

Permanent CIM instances are not deleted automatically when their WBEM server
is deregistered from the subscription manager. The user is responsible for
their lifetime management: They can be deleted via the removal methods of the
:class:`~pywbem.WBEMSubscriptionManager` class.

Permanent CIM instances should be used in cases where the user needs to have
control over the destination ``Name`` property (e.g. because a DMTF management
profile requires a particular name).


Static destinations, filters, and subscriptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Static CIM instances pre-exist in the WBEM server and cannot be deleted
(or created) by a WBEM client.

If a client creates a subscription between a filter and a listener destination,
the types of ownership of these three CIM instances may be arbitrarily mixed,
with one exception:

* A permanent subscription cannot be created on an owned filter or an owned
  listener destination. Allowing that would prevent the automatic life cycle
  management of the owned filter or listener destination by the subscription
  manager. This restriction is enforced by the
  :class:`~pywbem.WBEMSubscriptionManager` class.

Pywbemcli remembers owned subscriptions, filters, and listener destinations between
commands in both command line and interactive mode. It does this by recovering
instances from the current WBEM server whenever the pywbem ``SubscriptionManager``
object is created by a pywbemcli subscription command.

Each command command execution in command mode discovers owned subscriptions,
filters, and listener destinations for the current server. This discovery,
is based upon the ``Name`` property. Therefore, if the ``Name`` property is set by the
user (e.g. because a management profile requires a particular name), the filter
must be permanent and cannot be owned.

Pywbemcli destination, filter, and subscription characteristics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pywbemcli creates all instances of CIM_IndicationSubscription,
CIM_ListenerDestinationCIMXML and CIM_IndicationFilter in the interop
namespace. It does not allow the use of subclasses in the creation of
instances. If a user requires the creation of instances with a specific
subclass, that must be done through the :ref:`Instance create command`.

Owned destinations, filters, and subscriptions created by pywbemcli are
maintained in a local cache between commands in interactive mode and
automatically restored from the WBEM server in command mode. Permanent
destinations, filters, and subscriptions are enumerated from the WBEM server
for each subscription command that uses them (ex. subscription list-filters
--permanent or subscription list-filters --all).

Since pywbemcli does not directly modify existing instances of filter or
destinations or subscriptions, the user must do this directly through the
`ModifyInstance` WBEM request method  and then update the local owned instances
list by executing subscription list-filters, subscription list_destinations(), or
subscription list-subscriptions().

**NOTE:** Pywbem_mock used in testing does not remember any of subscription
instances between  non-interactive commands so that most pywbemcli mock testing
is done in interactive mode.

Identifying destinations, filters, and subscriptions on the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While instances of destinations, filters, and subscriptions are uniquely
defined with their CIM instance name, this is difficult in a command line
environment so a simpler string based identity was defined to allow easily
showing and using a string value to add and remove instances from the
WBEM server.  In particular the instances associated are complex names involving
multiple components (SystemCreationClassName, SystemName, CreationClassName,
and Name properties).

Pywbemcli identifies the instances created for destinations and listeners through
the ``Name`` property both for owned and permanent/static instances.

For pwned destinations and filters, the ``Name`` property string value is
defined with a specific format that defines it as an owned instance and ends
with a string that is unique to the instance (the owned identity).

Thus, for a filter, the ``Name`` property would be a string of the form:

.. code-block:: text

    "pywbemfilter:" {submgr_id} ":" {IDENTITY}

where:
    submgr_id is the identity of the pywbem :term:`subscription manager ID`,

This identity is used to used to create the value of the ``Name`` property when
instances are created by pywbemcli and to identify the target instance for removal.
The IDENTITY must be unique for each destination and filter created or the add
command will be rejected.

For permanent instances of destinations and filters, the identity is always the
complete ``Name`` property.

Thus, a new owned destination would be created with the identity ODEST1 and
removed as follows (Note: filters created and removed without the option
defining the ownership (``--owned`` / ``--permanent``) default to owned):

.. code-block:: text

   pywbemcli> subscription add-filter ODEST1 --query "Select * from CIM_Indication"
   Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:ODEST1

   pywbemcli> subscription remove-filter ODEST1
   Removed owned indication destination: identity=ODEST1, Name=pywbemdestination:defaultpywbemcliSubMgr:ODEST1.

Indication subscriptions are also added and removed using IDENTITY in
pywbemcli. However, since subscriptions CIMInstanceName values are the
corresponding filter (``Filter`` reference property) and destination instance
(``Handler`` reference property) names both the destination and filter must be
defined to uniquely define an indication subscription on add and remove
commands.

Thus two identities are used to identify a subscription. For example:

.. code-block:: text

    pywbemcli> subscription add-subscription DESTINATION_IDENTITY FILTER_IDENTITY
    pywbemcli> subscription remove-subscription  DESTINATION_IDENTITY FILTER_IDENTITY

Thus an owned subscription is created with the following command

.. code-block:: text

    pywbemcli> subscription add-subscription ODEST1 OFILTER1

where the destination and filter have been previously defined.

See :ref:`subscription add-subscription command` for more information.

In general IDENTITY makes it simple to identify and manipulate all of the
destination, filter, and, subscription instances using just strings for
identity. However, there may be cases where instances outside the control of
pywbemcli may cause duplications in identity. Thus,  for example, an instance
created using a subclass of one of the pywbemcli used classes could have a
``Name`` property with the same value but be unique because the instance name
includes the class origin name.

In these cases, pywbemcli generates an exception noting the duplication but provides
an option (``--select``) to allow the user to select one instance from multiples
instead of the exception.

See :ref:`pywbemcli subscription --help`.


.. index::
    pair: subscription commands; subscription add-destination

.. _`subscription add-destination command`:

``subscription add-destination`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This command creates a listener destination instance (CIM class
"CIM_ListenerDestinationCIMXML") with the identity defined by the IDENTITY
argument and the ``--owned`` | ``--permanent`` option  in the Interop namespace
of the specified WBEM server on the target WBEM server.

A listener destination defines the location of a WBEM indication
listener (the URL including port) that defines the indication listener
for indications exported from a WBEM server.

The format of this command is:

.. code-block:: text

    pywbemcli [GENERAL-OPTIONS] subscription add-destination IDENTITY [COMMAND-OPTIONS]

The listener destination  to be added is identified by the ``IDENTITY`` argument and the
``--owned`` / ``--permanent`` option. Together these elements define the
``Name`` property of the destination instance.

If the instance is to be owned, (``--owned``) the value of the ``Name`` property
will be:

.. code-block:: text

    "pywbemdestination:" {submgr_id} ":" {IDENTITY}

where:

    - ``{submgr_id}`` is the :term:`subscription manager ID`
    - ``{IDENTITY}`` is the IDENTITY argument in add and remove commands

If the instance is to be permanent, (``--permanent`` option) the ``IDENTITY``
argument directly defines the instance ``Name`` property.

If an destination instance with the specified or generated ``Name``
property already exists, the method raises CIMError(CIM_ERR_ALREADY_EXISTS).
Note that this is a more strict behavior than what a WBEM server would do,
because the 'Name' property is only one of four key properties.

The options that can be applied when adding a destination are:

* ``--listener-url`` - the URL of the listener including its scheme, host name
  and protocol. The host name and protocol are required and the scheme defaults
  to ``https`` if not specified.
* ``-- owned`` / ``--permanent`` - flag defining whether the created instance
  will be owned or permanent where the default is owned.

The following example creates an owned destination instance with the IDENTITY ``ODEST1``
and a permanent destination with IDENTITY ``PDEST1``

In this case the owned instance will be created with the ``Name`` property value:

.. code-block:: text

    pywbemdestination:<subscription manager id>:ODEST1


.. code-block:: text

    $ pywbemcli subscription add-destinations ODEST1 --listener-url http://my-listener:5000 --owned
    Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:ODEST1

    $ pywbemcli subscription add-destinations PDEST1 --listener-url http://my-listener:5000 --permanent
    Added permanent destination: Name=PDEST1

See :ref:`pywbemcli subscription add-destination --help`.


.. index::
    pair: subscription commands; subscription add-filter

.. _`subscription add-filter command`:

``subscription add-filter`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The add-filter command creates a :term:`dynamic indication filter` to a WBEM
server, by creating an indication filter instance (CIM class
"CIM_IndicationFilter") and adding this instance to the Interop namespace of
the current pywbemcli WBEM server (defined by the general options ``--name``,
``--server``, or ``--mock-server``).

The format of this command is:

.. code-block:: text

    pywbemcli [GENERAL-OPTIONS] subscription add-filter IDENTITY [COMMAND-OPTIONS]

The filter to be added is identified by the ``IDENTITY`` argument and the
``--owned`` / ``--permanent`` option. Together these elements define the
``Name`` property of the filter instance.

If the instance is to be owned, (``--owned``) the value of the ``Name`` property
will be:

.. code-block:: text

    "pywbemfilter:" {submgr_id} ":" {IDENTITY}``

where:

    - ``{submgr_id}`` is the subscription manager ID
    - ``{IDENTITY}`` is the IDENTITY argument in add and remove commands

If the instance is to be permanent, (``--permanent``) the the ``IDENTITY``
argument directly defines the instance ``Name`` property. This should be used
in cases where the user needs to have control over the filter name (e.g.
because a DMTF management profile requires a particular name).

If a indication filter instance with the specified ``Name``
property already exists, the method raises an exception.
Note that this is a more strict behavior than what a WBEM server would do,
because the ``Name`` property is only one of four key properties.

The command line options for this command are:

* ``--query-language`` - The language in which the query is defined.  Normally
  this must be either ``WQL`` a Microsoft specified query language or
  ``DMTF:CQL`` (the DMTF specified query language), The default language for this
  command is ``WQL``.
* ``query`` - The query itself defined as a string.
* ``-- owned`` / ``--permanent`` - flag defining whether the created instance
  will be owned or permanent where the default is owned.
* ``--source-namespaces`` The name of WBEM namespaces on the server where
  indications originate.

The following example creates an owned subscription instance with the IDENTITY
``ofilter1`` and a permanent filter with the ``Name`` property of ``pfilter1``.

The owned instance ``ofilter1`` will be created with the ``Name`` property value of:

    pywbemfilter:<subscription manager id>:pfilter1

.. code-block:: text

    $ pywbemcli subscription add-filter ofilter1 --query-language DMTF:CQL -q "SELECT * from CIM_blah" --owned
    Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:pfilter1

    $ pywbemcli subscription add-filter pfilter1 --listener-url http://my-listener:5000 --permanent
    Added permanent filter: Name=filter1

See :ref:`pywbemcli subscription add-filter --help`.


.. index::
    pair: subscription commands; subscription add-subscription

.. _`subscription add-subscription command`:

``subscription add-subscription`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The add-subscription command creates a single indication subscription instance
(CIM class CIM_IndicationSubscription) that defines the association between
a previously defined indication filter and destination instance.

The identity of the destination and filter is the two required arguments of
the command ``DESTINATION_IDENTITY`` and ``FILTER_IDENTITY``. These arguments
may be either the complete name property value of the destination and
filter to be associated or the IDENTIY that was the IDENTITY argument of the
command that created each of the elements.

See :ref: for the definition of ``DESTINATION_IDENTITY and :ref: for the
definition of the ``FILTER_ARGUMENT``

The Arguments for the add-subscription command are:

  - DESTINATION_IDENTITY
  - FILTER-IDENTITY

The options for add-subscription are:

* ``-- owned`` / ``--permanent`` - flag defining whether the created instance
  will be owned or permanent where the default is owned. As described above, the
  limitation is that owned destinations and filters cannot be attached to
  permanent subscriptions.

The following is an example of the creation of the destination, filter and
subscription.

.. code-block:: text

    $> pywbemcli -s https:/blah
    pywbemcli> subscription add-destinations odest1 --listener-url http://my-listener:5000 --owned
    Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:odest1

    pywbemcli> subscription add-filter ofilter1 --query-language DMTF:CQL -q "SELECT * from CIM_blah" --owned
    Added owned filter: Name=pywbemfilter:defaultpywbemcliSubMgr:ofilter1

    pywbemcli> subscription list-destinations
    Indication Destinations: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988, type=all
    +-------------+------------+--------------------------------+-------------------+---------------+------------+----------------+
    | Ownership   | Identity   | Name                           | Destination       |   Persistence |   Protocol |   Subscription |
    |             |            | Property                       |                   |          Type |            |          Count |
    |-------------+------------+--------------------------------+-------------------+---------------+------------+----------------|
    | owned       | odest1     | pywbemdestination:defaultpywbe | http://blah:5000  |             3 |          2 |              0 |
    |             |            | mcliSubMgr:odest1              |                   |               |            |                |
    +-------------+------------+--------------------------------+-------------------+---------------+------------+----------------+

    pywbemcli> subscription list-filters
    Indication Filters: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988 type=all
    +-------------+------------+--------------------------------+----------------+------------+--------------+----------------+
    | Ownership   | identity   | Name                           | Query          | Query      | Source       |   Subscription |
    |             |            | Property                       |                | Language   | Namespaces   |          Count |
    |-------------+------------+--------------------------------+----------------+------------+--------------+----------------|
    | owned       | ofilter1   | pywbemfilter:defaultpywbemcliS | SELECT * from  | WQL        | root/cimv2   |              0 |
    |             |            | ubMgr:ofilter1                 | CIM_Indication |            |              |                |
    +-------------+------------+--------------------------------+----------------+------------+--------------+----------------+

    pywbemcli> subscription add-subscription pdest1 pfilter1 --owned
    Added owned subscription: DestinationName=pywbemdestination:defaultpywbemcliSubMgr:odest1, FilterName=pywbemfilter:defaultpywbemcliSubMgr:ofilter1

See :ref:`pywbemcli subscription add-subscription --help`.

.. index::
    pair: subscription commands; subscription list

.. _`subscription list command`:

``subscription list`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``subscription list command`` provides a table with an overview of the
subscription, filter, and destination counts organized by ownership.

The options are:

-  ``--type`` [ ``owned``| ``permanent`` | ``all`` ]  Defines whether the command is going to
   filter owned ,permanent, or all objects for the response display.  The default is
   all
- ``-s`` / ``--summary``             If True, show only summary count of instances


.. code-block:: text

    $ subscription list
    WBEM server instance counts: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988
    +-------------------------------+---------+-------------+-------+
    | CIM_class                     |   owned |   permanent |   all |
    |-------------------------------+---------+-------------+-------|
    | CIM_IndicationSubscription    |       1 |           0 |     1 |
    | CIM_IndicationFilter          |       2 |           1 |     3 |
    | CIM_ListenerDestinationCIMXML |       2 |           1 |     3 |
    +-------------------------------+---------+-------------+-------+

    $ subscription list --summary
    1 subscriptions, 3 filters, 3 destinations


.. index::
    pair: subscription commands; subscription list-destinations

.. _`subscription list-destinations command`:

``subscription list-destinations`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``subscription ``list-destinations`` command displays the existing
destination instances ((CIM class "CIM_ListenerDestinationCIMXML")) on
the current WBEM server.

**NOTE:** pywbemcli works only with the  ``CIM_ListenerDestinationCIMXML``
class so that any indication destination instances defined with the superclass
``CIM_ListenerDestination`` are not visible.

The set of destinations to be displayed may be all of the destinations, the
owned destinations, or the permanent (not-owned) destinations as defined by
the ``--type`` option where the values are ``owned`` | ``permanent`` | ``all``.

The format of the output is determined by the ``--output-format`` general
option so that the destinations may be displayed as either CIM objects ( for
example, ``-o mof``)  or in the table format. The default is to display the
destinations as a table.  In the table format, the most important information
for each instance is displayed, one instance per row.

The detail level of the output is determined by the ``--summary`` and the
``detail`` options and has an effect on both the mof and table outputs. The
``--summary`` displays counts of the number of objects and the ``--detail``
adds more data to the normal display, in particular displaying more properties
in the table view.

The options for list-destinations are:

* ``--type [ owned | permanent | all ]`` - choice option that
  limits the list of destinations displayed to either just owned or permanent instances
  or displays all destinations on the current WBEM server

* ``--detail`` - displays additional detail for all of the possible output formats.
  For MOF it includes empty properties. For table, it adds more rows with  properties
  from the instance.

* ``-s`` / ``--summary`` limits the display to an overview

* ``--no`` / ``--names-only`` displays only the CIM instance names (paths) of the instances.

The following is an example of the display of the destinations as a table:

.. code-block:: text

    Indication Destinations: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988, type=all
    +-------------+------------+--------------------------------+-------------------+---------------+------------+----------------+
    | Ownership   | Identity   | Name                           | Destination       |   Persistence |   Protocol |   Subscription |
    |             |            | Property                       |                   |          Type |            |          Count |
    |-------------+------------+--------------------------------+-------------------+---------------+------------+----------------|
    | owned       | odest1     | pywbemdestination:defaultpywbe | http://blah:5000  |             3 |          2 |              2 |
    |             |            | mcliSubMgr:odest1              |                   |               |            |                |
    | owned       | odest2     | pywbemdestination:defaultpywbe | http://blah:5001  |             3 |          2 |              1 |
    |             |            | mcliSubMgr:odest2              |                   |               |            |                |
    | permanent   | pdest1     | pdest1                         | https://blah:5003 |             2 |          2 |              2 |
    | permanent   | pdest2     | pdest2                         | https://blah:5003 |             2 |          2 |              1 |
    | owned       | pdestdup   | pywbemdestination:defaultpywbe | https://blah:5003 |             3 |          2 |              0 |
    |             |            | mcliSubMgr:pdestdup            |                   |               |            |                |
    | permanent   | pdestdup   | pdestdup                       | https://blah:5003 |             2 |          2 |              0 |
    +-------------+------------+--------------------------------+-------------------+---------------+------------+----------------+

where the rows shown in the table view are:

* *Ownership* - the owned/permanent definition of the destination.
* *Identity* - The identity of the destination which should be the  IDENTITY
  used to remove the destination
* *Name* - The value of the instance ``Name`` property
* *Destination* - The value of the Destination property.
* *Persistence Type* - The value of the ``PersistenceType`` property.
* *Protocol* - The value of the ``Protocol`` property.
* *Subscription Count* - The number of subscriptions with which this destination
  is associated via the ``CIM_IndicationSubscription`` ``Handler`` reference.


.. index::
    pair: subscription commands; subscription list-filters

.. _`subscription list-filters command`:

``subscription list-filters`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``subscription ``list-filters`` command displays the existing
indication filter instances ((CIM class "CIM_IndicationFilter")) on
the current WBEM server.

The set of filters to be displayed may be all of the filters, the
owned filters, or the permanent (not owned) filters as defined by
the ``--type`` option where the values are ``owned`` | ``permanent`` | ``all``.

The format of the output is determined by the ``--output-format`` general
option so that the destinations may be displayed as either CIM objects (``-o
mof``)  or in the table format. The default is to display the destinations as a
table.

The detail level of the output is determined by the ``--summary`` and the
``detail`` options and has an effect on both the MOF and table outputs. The
``--summary`` displays counts of the number of objects and the ``--detail``
adds more data to the normal display, in particular displaying more properties
in the table view.

The options for list-destinations are:

* ``-- type [ owned | permanent | all ]`` - choice option that
  limits the list of destinations displayed to either just owned or permanent instances
  or displays all destinations on the current WBEM server

* ``--detail`` - displays additional detail for all of the possible output formats.
  For MOF it includes empty properties. For table, it adds more rows with  properties
  from the instance.

* ``-s`` / ``--summary`` limits the display to an overview

* ``--no`` / ``--names-only`` displays only the CIM instance names (paths) of the instances.

The following is an example of table output of indication filters:

.. code-block:: text

    Indication Filters: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988 type=all
    +-------------+------------+--------------------------------+----------------+------------+--------------+----------------+
    | Ownership   | identity   | Name                           | Query          | Query      | Source       |   Subscription |
    |             |            | Property                       |                | Language   | Namespaces   |          Count |
    |-------------+------------+--------------------------------+----------------+------------+--------------+----------------|
    | owned       | ofilter1   | pywbemfilter:defaultpywbemcliS | SELECT * from  | WQL        | root/cimv2   |              2 |
    |             |            | ubMgr:ofilter1                 | CIM_Indication |            |              |                |
    | owned       | ofilter2   | pywbemfilter:defaultpywbemcliS | SELECT * from  | DMTF:CQL   | root/cimv2   |              1 |
    |             |            | ubMgr:ofilter2                 | CIM_Indication |            |              |                |
    | permanent   | pfilter1   | pfilter1                       | SELECT * from  | WQL        | root/cimv2   |              2 |
    |             |            |                                | CIM_Indication |            |              |                |
    | permanent   | pfilter2   | pfilter2                       | SELECT * from  | DMTF:CQL   | root/cimv2   |              1 |
    |             |            |                                | CIM_Indication |            |              |                |
    +-------------+------------+--------------------------------+----------------+------------+--------------+----------------+

where the rows shown in the table view are:

* *Ownership* - the owned/permanent definition of the destination.
* *Identity* - The identity of the destination which should be the  IDENTITY
  used to remove the destination
* *Name* - The value of the instance ``Name`` property
* *Query* - The query select statement defined for this filter.
* *QueryLanguage* - The query language defined for this filter.
* *SourceNamespaces* - The names of the local namespaces where the Indications
  originate. If NULL, the namespace of the Filter registration is assumed.
  SourceNamespaces replaces the deprecated SourceNamespace property on
  IndicationFilter to provide a means of defining the multiple
  namespaces where indications may originate.
* *Subscription Count* - The number of subscriptions with which this filter
  is associated via the ``CIM_IndicationSubscription`` ``Filter`` reference.


.. index::
    pair: subscription commands; subscription list-subscriptions

.. _`subscription list-subscriptions command`:

``subscription list-subscriptions`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``subscription`` ``list-filters`` command displays the existing
indication filter instances (CIM class "CIM_IndicationSubscription") on
the current WBEM server.

The set of subscriptions to be displayed may be all of the destinations, the
owned subscriptions, or the permanent (not owned) subscriptions as defined by
the ``--type`` option where the values are ``owned`` | ``permanent`` | ``all``.

The format of the output is determined by the ``--output-format`` general option so
that the destinations may be displayed as either CIM objects (``-o mof``)  or
in the table format. The default is to display the destinations as a table.

The detail level of the output is determined by the ``--summary`` and the
``detail`` options and has an effect on both the mof and table outputs. The
``--summary`` displays counts of the number of objects and the ``--detail``
adds more data to the normal display, in particular displaying more properties
in the table view.

The options for list-destinations are:

* ``-- type [ owned | permanent | all ]`` - choice option that
  limits the list of destinations displayed to either just owned or permanent instances
  or displays all destinations on the current WBEM server

* ``--detail`` - displays additional detail for all of the possible output formats.
  For MOF it includes empty properties. For table, it adds more rows with  properties
  from the instance.

* ``-s`` / ``--summary`` limits the display to an overview

* ``--no`` / ``--names-only`` displays only the CIM instance names (paths) of the instances.

The following is an example of table output of indication subscriptions:

.. code-block:: text

    pywbemcli> subscription list-subscriptions
    Indication Subscriptions: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988, type=all
    +-------------+-------------------+---------------------+-------------------+------------------------------+----------------+-------------------+
    | Ownership   | Handler           | Filter              | Handler           | Filter                       | Filter Query   | Subscription      |
    |             | Identity          | Identity            | Destination       | Query                        | language       | StartTime         |
    |-------------+-------------------+---------------------+-------------------+------------------------------+----------------+-------------------|
    | permanent   | pdest1(permanent) | pfilter1(permanent) | https://blah:5003 | SELECT * from CIM_Indication | WQL            | 10/22/21 14:31:30 |
    | permanent   | pdest2(permanent) | pfilter2(permanent) | https://blah:5003 | SELECT * from CIM_Indication | DMTF:CQL       | 10/22/21 14:31:30 |
    | owned       | odest1(owned)     | ofilter1(owned)     | http://blah:5000  | SELECT * from CIM_Indication | WQL            | 10/22/21 14:31:30 |
    | owned       | odest2(owned)     | ofilter2(owned)     | http://blah:5001  | SELECT * from CIM_Indication | DMTF:CQL       | 10/22/21 14:31:30 |
    | owned       | odest1(owned)     | pfilter1(permanent) | http://blah:5000  | SELECT * from CIM_Indication | WQL            | 10/22/21 14:31:31 |
    | owned       | pdest1(permanent) | ofilter1(owned)     | https://blah:5003 | SELECT * from CIM_Indication | WQL            | 10/22/21 14:31:31 |
    +-------------+-------------------+---------------------+-------------------+------------------------------+----------------+-------------------+
    pywbemcli>

where the rows shown in the table view are:

* *Ownership* - the owned/permanent definition of the destination.
* *HandlerIdentity* - The identity of the destination associated with this subscription.
* *FilterIdentity* -  The identity of the filter associated with this subscription.
* *Handler Destination* - The listener destination defined in the destination defined
  by the HandlerIdentity
* *FilterQuery* - The FilterQuery property from the associated filter defined by
  the FilterIdentity
* *FilterQueryLanguage* - The FilterQueryLanguage property from the associated filter defined by
  the FilterIdentity
* *Name* - The value of the instance ``Name`` property
* *Query* - The query select statement defined for this filter.
* *QueryLanguage* - The query language defined for this filter.
* *SubscriptionStartTime* - The date and time that the subscription was created
  if the WBEM server has implemented this property.

.. index::
    pair: subscription commands; subscription remove-destination

.. _`subscription remove-destination command`:

``subscription remove-destination`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removes a listener destination instance (CIM_ListenerDestinationCIMXML)
from the WBEM server where the instance to be removed is identified by the
IDENTITY argument and optional ``--owned`` option of the command.

The listener destination  to be removed is identified by the ``IDENTITY``
argument and the ``--owned`` / ``--permanent`` option. Together these elements
define the ``Name`` property of the target destination instance.

If the instance is owned, (``--owned``) the IDENTITY argument will define the
IDENTITY component of the ``Name`` property as follows:

.. code-block:: text

    ``"pywbemdestination:" {submgr_id} ":" {IDENTITY}``

where:

    - ``{submgr_id}`` is the subscription manager ID
    - ``{IDENTITY}`` is the IDENTITY argument

If the instance is to be permanent, (``--permanent`` option) the ``IDENTITY``
argument directly defines the instance ``Name`` property.

Some listener_destination instances on a server may be static in which case the
server should generate an exception if an attempt to made to remove them.
Pywbemcli has no way to identify these static destinations and they will appear
as permanent destination instances.

The ``--select`` option can be used if, for some reason, the IDENTITY and
ownership option returns multiple instances. This should only occur in rare
cases where destination instances have been created by other tools. If the
--select option is not used pywbemcli displays the paths of the instances and
terminates the command.

If the instance to be removed is part of an existing association the command
is aborted.  The :ref:`subscription list-destinations command` shows whether
the destination is part of an existing subscription.

The following example shows a command failure when an attempt is made to
remove a destination that is part of a subscription and a good completion
when that subscription has been removed.

.. code-block:: text

    pywbemcli> subscription list-destinations
    Indication Destinations: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988, type=all
    +-------------+------------+--------------------------------+-------------------+---------------+------------+----------------+
    | Ownership   | Identity   | Name                           | Destination       |   Persistence |   Protocol |   Subscription |
    |             |            | Property                       |                   |          Type |            |          Count |
    |-------------+------------+--------------------------------+-------------------+---------------+------------+----------------|
    | owned       | odest1     | pywbemdestination:defaultpywbe | http://blah:5000  |             3 |          2 |              1 |
    |             |            | mcliSubMgr:odest1              |                   |               |            |                |
    +-------------+------------+--------------------------------+-------------------+---------------+------------+----------------+
    pywbemcli> subscription remove-destination odest1
    Error: 1 (CIM_ERR_FAILED): The listener destination is referenced by subscriptions.; remove-destination failed: Exception :CIMError. Subscription mgr id: 'WBEMSubscriptionManager(_subscription_manager_id='defaultpywbemcliSubMgr', _servers={'http://FakedUrl:5988': WBEMServer(conn.url='http://FakedUrl:5988', interop_ns='interop', namespaces=None, namespace_paths=None, namespace_classname=None, brand='OpenPegasus', version='2.15.0', profiles=[0 instances])}, _systemnames={'http://FakedUrl:5988': 'Mock_WBEMServerTest'}...)', server id: 'http://FakedUrl:5988',

    pywbemcli> subscription list-subscriptions
    Indication Subscriptions: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988, type=all
    +-------------+-------------------+---------------------+-------------------+------------------------------+----------------+-------------------+
    | Ownership   | Handler           | Filter              | Handler           | Filter                       | Filter Query   | Subscription      |
    |             | Identity          | Identity            | Destination       | Query                        | language       | StartTime         |
    |-------------+-------------------+---------------------+-------------------+------------------------------+----------------+-------------------|
    | owned       | odest1(owned)     | ofilter1(owned)     | http://blah:5000  | SELECT * from CIM_Indication | WQL            | 10/24/21 11:36:03 |
    +-------------+-------------------+---------------------+-------------------+------------------------------+----------------+-------------------+

    pywbemcli> subscription remove-subscription odest1 ofilter1
    Removed 1 subscription(s) for destination-id: odest1, filter-id: ofilter1.

.. index::
    pair: subscription commands; subscription remove-filters

.. _`subscription remove-filter command`:

``subscription remove-filter`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removes an indication filter instance (CIM_IndicationFilter) from the WBEM
server.

The filter  to be removed is identified by the ``IDENTITY`` argument and the
``--owned`` / ``--permanent`` option. Together these elements define the
``Name`` property of the target filter instance.

If the instance is owned, (``--owned``) the IDENTITY argument will define the
IDENTITY component of the ``Name`` property as follows:

.. code-block:: text

    ``"pywbemfilter:" {submgr_id} ":" {IDENTITY}``

where:

    - ``{submgr_id}`` is the subscription manager ID
    - ``{IDENTITY}`` is the IDENTITY argument

If the instance is to be permanent, (``--permanent`` option) the ``IDENTITY``
argument directly defines the instance ``Name`` property.

Some filter instances on a server may be static in which case the
server should generate an exception if an attempt to made to remove them.
Pywbemcli has no way to identify these static filters and they will appear
as permanent filter instances.

The ``--select`` option can be used if, for some reason, the IDENTITY and
ownership option returns multiple instances. This should only occur in rare
cases where filter instances have been created by other tools. If the
--select option is not used pywbemcli displays the paths of the instances and
terminates the command.

If the instance to be removed is part of an existing association the command
is aborted.  The :ref:`subscription list-filters command` shows whether
the filter is part of an existing subscription.

TODO: Example

.. index::
    pair: subscription commands; subscription remove-subscriptions

.. _`subscription remove-subscription command`:

``subscription remove-subscription`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO: Complete these paragraphs.


The ``--select`` option can be used if, for some reason, the IDENTITY and
ownership option returns multiple instances. This should only occur in rare
cases where filter instances have been created by other tools. If the
--select option is not used pywbemcli displays the paths of the instances and
terminates the command.


.. index::
    pair: subscription commands; subscription remove-server

.. _`subscription remove-server command`:

``Subscription remove-server`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    This command unregisters owned listeners from the WBEM server and removes
    all owned indication subscriptions, owned indication filters, and owned
    listener destinations for this currently active pywbemcli WBEM server from
    that WBEM server.

    It can be used to completely clean the owned subscription entities for the
    currently active pywbemcli WBEM server from that wbem server and local
    caches.

    The currently active WBEM server is the WBEM server to which pywbemcli is
    currently attached; the WBEM server defined by  the ``--name``,
    ``--server``, or `--mock-server`` general options.

    The identity of the current wbem server id visible in the title of
    each of the subscription list table outputs.

    Thus, for example current server is defined by svr_id and is actually
    the fixed name ``http://FakedUrl:5988`` of the mock server.

.. code-block:: text

    pywbemcli> subscription list

    WBEM server instance counts: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988
    +-------------------------------+---------+-------------+-------+
    | CIM_class                     |   owned |   permanent |   all |
    |-------------------------------+---------+-------------+-------|
    | CIM_IndicationSubscription    |       2 |           2 |     6 |
    | CIM_IndicationFilter          |       2 |           3 |     6 |
    | CIM_ListenerDestinationCIMXML |       2 |           3 |     6 |
    +-------------------------------+---------+-------------+-------+

    pywbemcli> subscription remove-server
    Removing owned destinations, filters, and subscriptions for server-id http://FakedUrl:5988. Remove counts: destinations=2, filters=2, subscriptions=2

    pywbemcli> subscription list

    WBEM server instance counts: submgr-id=defaultpywbemcliSubMgr, svr-id=http://FakedUrl:5988
    +-------------------------------+---------+-------------+-------+
    | CIM_class                     |   owned |   permanent |   all |
    |-------------------------------+---------+-------------+-------|
    | CIM_IndicationSubscription    |       0 |           2 |     2 |
    | CIM_IndicationFilter          |       0 |           3 |     3 |
    | CIM_ListenerDestinationCIMXML |       0 |           3 |     3 |
    +-------------------------------+---------+-------------+-------+



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
