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


.. _`Pywbemcli special command line features`:

Pywbemcli special command line features
=======================================

Pywbemcli includes several features in the command syntax that are worth
presenting in detail to help the user understand the background, purpose and
syntactic implementation of the features. This includes:

* The ability to receive either CIM instances or classes or only their names
  with only a change of an option on the commands that request CIM instances or
  classes. The ``--names-only``/``--no`` command option defines whether only the
  name or the complete object will be displayed.
  See :ref:`Displaying CIM instances/classes or their names`

* The ability to define complete INSTANCE name command arguments or
  interactively select the instance names from a list presented by
  pywbemcli for certain objects rather than typing in long names the full name.
  See :ref:`Specifying the INSTANCENAME command argument`.

.. index::
  pair: classes; filter options
  pair: instances; filter options

* The ability to filter classes and instances returned from a number of the
  enumerate commands filtered by characteristics of the classes. Thus,
  for example, it can for experimental classes, association classes, and
  deprecated classes. See :ref:`Filtering responses for specific types of classes`

.. index::
    pair: namespace; multiple namespaces
    pair: --namespace option; command option --namespace

* The ability to view information on multiple namespaces in a single command.
  Many of the pywbemcli commands target a term:`Namespace` in the WBEM server
  for as the source of information (ex. enumerate, get, associators,
  references). Commands like create, delete, and modify are restricted to a
  single namespace which can be either the default namespace defined for the
  connection or a namespace defined with the ``--namespace`` command option.
  Commands like enumerate, get, associators, and references can be used to get
  CIM information from multiple namespaces in a single pywbemcli request using
  the ``--namespace`` command option.  Thus, if single namespace is defined
  (``--namespace root/blah``) that becomes the namespace for the command.
  However with these particular commands, multiple namespaces can be specified
  (``--namespace root/cimv2,root/cimv3`` or ``--namespace root/cimv2
  --namespace root/cimv3``) and the CIM objects retrieved from all of the
  namespaces on this list and displayed. See :ref:`Using multiple namespaces
  with server requests`.


.. _`pywbemcli command relation to WBEM operations`:

pywbemcli command relation to WBEM operations
---------------------------------------------

The following table defines which pywbemcli commands are used for the
corresponding WBEM operations.

=================================  ==============================================
WBEM CIM-XML Operation             pywbemcli command group & command
=================================  ==============================================
**Instance Operations:**
EnumerateInstances                 instance enumerate INSTANCENAME
EnumerateInstanceNames             instance enumerate INSTANCENAME --names-only
GetInstance                        instance get INSTANCENAME
ModifyInstance                     instance modify
CreateInstance                     instance create
DeleteInstance                     instance delete INSTANCENAME
Associators(instance)              instance associators INSTANCENAME
Associators(class)                 class associators CLASSNAME
AssociatorNames(instance)          instance associators INSTANCENAME --names-only
AssociatorNames(class)             class associators CLASSNAME --names-only
References(instance)               instance references INSTANCENAME
References(class)                  class references CLASSNAME
ReferenceNames(instance)           instance references INSTANCENAME --names-only
ReferenceNames(class)              class references CLASSNAME --names-only
InvokeMethod                       instance invokemethod INSTANCENAME --names-only
ReferenceNames                     class invokemethod CLASSNAME --names-only
ExecQuery                          instance query
**Pull Operations:**               Option --use-pull ``either`` or ``yes``
OpenEnumerateInstances             instance enumerate INSTANCENAME
OpenEnumerateInstancePaths         instance enumerate INSTANCENAME --names-only
OpenAssociatorInstances            instance associators INSTANCENAME
OpenAssociatorInstancePaths        instance associators INSTANCENAME --names-only
OpenReferenceInstances             instance references INSTANCENAME
OpenReferenceInstancePaths         instance references INSTANCENAME --names-only
OpenQueryInstances                 instance references INSTANCENAME --names-only
PullInstancesWithPath              part of pull sequence
PullInstancePaths                  part of pull sequence
PullInstances                      part of pull sequence
CloseEnumeration                   Not implemented
**Class Operations:**
EnumerateClasses                   class enumerate CLASSNAME
EnumerateClassNames                class enumerate --names-only
GetClass                           class get CLASSNAME
ModifyClass                        Not implemented
CreateClass                        Not implemented
DeleteClass                        class delete CLASSNAME
**QualifierDeclaration Ops:**
EnumerateQualifiers                qualifier enumerate
GetQualifier                       qualifier get QUALIFIERNAME
SetQualifier                       Not implemented
DeleteQualifier                    Not Implemented
=================================  ==============================================

.. index:: pair: Command Options; --property option

.. _`Specifying CIM property and parameter values`:

Specifying CIM property and parameter values
--------------------------------------------

The :ref:`instance create command`, :ref:`instance modify command`,
:ref:`class invokemethod command`, and :ref:`instance invokemethod command`
define the values of properties and parameters that are to be applied to CIM
instances and methods to be sent to the WBEM server.

For a single property or parameter these are the ``--property``/``-p`` or
``--parameter``/``-p`` command options with name and value in the form:

.. code-block:: text

    --property <name>=<value>
    --parameter <name>=<value>
    -p <name>=<value>

Where:

* <name> is the name of the of the property or parameter.
* <value> is the value of the property or parameter. The values represent the
  value of CIM types (ex. Uint32, String, etc.) or arrays of these types.

.. code-block:: text

    value := scalarValue | or arrayValues
    arrayValues := scalarValue [ "," scalarValue]
    scalarValue := integerValue, realValue, charValue, stringValue,
                   datetimeValue, booleanValue, nullValue, objectPath of
                   ANNEX A :term:`DSP0004`

These values define the syntax of the values to build  CIM properties and CIM
parameters to be sent to the CIM Server. Since the WBEM server requires that
each property/parameter be typed to be created, pywbemcli retrieves the target
CIM class from the WBEM Server to determine the CIM type and arrayness required
to define a CIMProperty.

The scalarValues limitations with respect to the definitions in :term:`DSP0004`
include:

* Only decimal integers are allowed (octal, hex, and binary are not supported).
* Integers must be in the value range of the corresponding CIM type
  (ex. Uint32) defined in the class to which the property is being applied.
* The format for objectPath is the WBEM URI as defined in
  :ref:`Specifying the INSTANCENAME command argument`

Quotes around the value are only required if the value includes whitespace. See
:term:`backslash-escaped` for information on use of backslashes in formating
property and parameter argument values.

The following are examples of scalar property definitions:

.. code-block:: text

    -p p1=SomeText
    -p p2=\"Text with space\"
    -p pint=3
    -p psint=-3

For array properties the values are defined separated by commas:

.. code-block:: text

    -p <property-name>=<value>(,<value>)

For example:

.. code-block:: text

    -p strarray=abc,def,ghjk
    -p strarray2=\"ab c\",def



.. _`Displaying CIM instances/classes or their names`:

Displaying CIM instances/classes or their names
-----------------------------------------------

The pywbem API includes different WBEM operations (ex. ``EnumerateInstances``,
``EnumerateInstanceNames``, ``EnumerateClasses``, and ``EnumerateClassNames``)
to request CIM objects or just their names. To simplify the overall command
line syntax pywbemcli combines these into a single command (i.e. ``enumerate``,
``references``, ``associators``)  in the :ref:`class command group` and the
:ref:`instance command group` and includes the
``--names-only``/``--no`` command option that determines whether the names or
the CIM objects are retrieved from the WBEM server.

Thus, for example an ``instance enumerate`` command with and without the
``--names-only``/``--no`` option:

.. code-block:: text

    $ pywbemcli --mock-server tests/unit/simple_mock_model.mof instance enumerate CIM_Foo

    instance of CIM_Foo {
       InstanceID = "CIM_Foo1";
       IntegerProp = 1;
    };

    instance of CIM_Foo {
       InstanceID = "CIM_Foo2";
       IntegerProp = 2;
    };

    instance of CIM_Foo {
       InstanceID = "CIM_Foo3";
    };

    $ pywbemcli --mock-server tests/unit/simple_mock_model.mof instance enumerate CIM_Foo --names-only

    root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"
    root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"
    root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"


.. index::
    pair: INSTANCENAME; command argument


.. _`Specifying the INSTANCENAME command argument`:

Specifying the INSTANCENAME command argument
--------------------------------------------

The INSTANCENAME  command argument used by some pywbemcli commands (e.g
``instance get``) specifies the instance path (aka instance name) of a CIM
instance in a CIM namespace of a WBEM server.

The instance name (INSTANCENAME argument) can be specified in two ways:

* By specifying a complete untyped WBEM URI as defined in section
  :ref:`The INSTANCENAME command argument as a WBEM URI`. The
  namespace of the instance is the namespace specified in the WBEM URI, or the
  namespace specified with the ``--namespace``/``-n`` command option, or the
  default namespace of the connection. Any host name in the WBEM URI will be
  ignored.

* By specifying the WBEM URI with the wildcard "?" in place of the keys
  component of the WBEM URI,  as defined in section
  :ref:`Interactively selecting INSTANCENAME command argument` (i.e.
  CLASSNAME.?). The namespace of the instance is the namespace specified with
  the ``--namespace``/``-n`` command option, or the default namespace of the
  connection.  If there is only a single instance, that instance is selected
  automaticaly with without user request.

* By specifying the WBEM URI without keybindings and using the
  ``--key``/``-k`` command option to specify the keybindings ad defined in
  section :ref:`Defining INSTANCENAME command argument with --key option`. The
  advantage of this technique is that it eliminates the use of the double
  quote surrounding the key values.


.. _`The INSTANCENAME command argument as a WBEM URI`:

The INSTANCENAME command argument as a WBEM URI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The format used by pywbemcli for specifying complete INSTANCENAME arguments on
the command line is an untyped WBEM URI for instance paths as defined in
:term:`DSP0207`, this is the *standard* format. There is also a *historical*
format for WBEM URIs that is described in the
:meth:`pywbem.CIMInstanceName.to_wbem_uri` method.

The INSTANCENAME argument can be specified using the standard format or
the historical format.

Because pywbemcli always works with a single WBEM server at a time, the
authority component of the WBEM URI does not need to be specified in an
INSTANCENAME argument. Because the namespace type of the WBEM URI
(e.g. "http" or "https") is not relevant for identifying the CIM instance,
the namespace type does not need to be specified in an INSTANCENAME argument.

With these simplifications and using the (simpler) historical format, the format
for the INSTANCENAME argument can be described by the following ABNF:

.. code-block:: text

    INSTANCENAME = [ NAMESPACE ":" ] CLASSNAME [ "." keybindings ]

    keybindings = keybinding *( "," keybinding )

    keybinding = PROPERTYNAME "=" value

    value = integerValue / charValue / stringValue / datetimeValue / booleanValue / referenceValue

    referenceValue = "\"" escaped_INSTANCENAME "\""

where:

* NAMESPACE, CLASSNAME and PROPERTYNAME are namespace, class and key
  property name, respectively, as used elsewhere in pywbemcli.

  The namespace, if specified, must be the target namespace of the operation.
  The purpose of being able to specify a namespace in INSTANCENAME is not to
  override the target namespace, but to use returned instance names that may
  contain a namespace, unchanged.

* integerValue, charValue, stringValue, datetimeValue and
  booleanValue are defined in ANNEX A of :term:`DSP0004`.

  Note that stringValue and datetimeValue when used in INSTANCENAME have exactly
  one set of surrounding double quotes (i.e. they cannot be constructed via
  string concatenation).

  Note that charValue when used in INSTANCENAME has exactly one set of
  surrounding single quotes.

  Note that DSP0004 prevents the use of real32 or real64 typed properties as
  keys.

* escaped_INSTANCENAME is a :term:`backslash-escaped` INSTANCENAME where at
  least backslash and double quote characters are backslash-escaped

Examples for UNIX-like shells. See :term:`backslash-escaped` for information on
use of backslashes:

.. code-block:: text

    pywbemcli instance get root/cimv2:MY_Foo.ID=42
    pywbemcli instance get MY_Foo.ID=42
    pywbemcli instance get "MY_Foo.CharKey='x'"
    pywbemcli instance get 'MY_Foo.InstanceID="foo1"'
    pywbemcli instance get "MY_Foo.InstanceID=\"$value\""
    pywbemcli instance get 'MY_CS.CreationClassName="MY_CS",Name="MyComp"'
    pywbemcli instance get 'MY_LogEntry.Timestamp="20190901183853.762122+120"'

Examples for Windows command processor:

.. code-block:: text

    pywbemcli instance get root/cimv2:MY_Foo.ID=42
    pywbemcli instance get MY_Foo.ID=42
    pywbemcli instance get MY_Foo.CharKey='x'
    pywbemcli instance get MY_Foo.InstanceID="foo1"
    pywbemcli instance get MY_Foo.InstanceID="%value%"
    pywbemcli instance get MY_CS.CreationClassName="MY_CS",Name="MyComp"
    pywbemcli instance get MY_LogEntry.Timestamp="20190901183853.762122+120"


.. _`Interactively selecting INSTANCENAME command argument`:

Interactively selecting INSTANCENAME command argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To simplify creating the INSTANCENAME argument on the command line, pywbemcli
provides a wildcard character "?" that can be used in the
INSTANCENAME argument in place of the keybindings component of the WBEM URI.

If an INSTANCENAME argument specifies the wildcard key, pywbemcli performs
an interactive selection of the instance name by enumerating the instance names
of the specified class, displaying the list of instance names along with index
numbers, and prompting the user for the index number of the instance name to be
used.

The ABNF for the INSTANCENAME argument with a wildcard key is:

.. code-block:: text

    INSTANCENAME = CLASSNAME "." wildcard

    wildcard = "?"

where:

* CLASSNAME is a class name as used elsewhere in pywbemcli.

Thus, in place of the full WBEM URI (ex. ``CIM_Foo.InstanceID="CIM_Foo1"``),
the user specifies ``CIM_Foo.?`` for the INSTANCENAME argument to trigger the
interactive selection, as shown in the following example:

.. code-block:: text

    $ pywbemcli --mock-server tests/unit/simple_mock_model.mof instance get CIM_Foo.?
    Pick Instance name to process
    0: root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"
    1: root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"
    2: root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"
    Input integer between 0 and 2 or Ctrl-C to exit selection: 0  << user enters 0
    instance of CIM_Foo {
       InstanceID = "CIM_Foo1";
       IntegerProp = 1;
    };


.. index:: pair: INSTANCENAME; --key command argument

.. _`Defining INSTANCENAME command argument with --key option`:

Defining INSTANCENAME command argument with --key option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The INSTANCENAME may be specified by a combination of the namespace/classname
as an argument with the ``--key``/``-k`` command option to define keybindings.
Each ``--key``/``-k`` option definition defines a single keybinding in the form
``name=value``.
In general, the value component does not require the double quote that is
required with the WBEM URI format unless there are space characters in a string
value.

Example::

    CIM_Foo --key InstanceId=inst1


.. _`Filtering responses for specific types of classes`:

Filtering responses for specific types of classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Several of the commands include result filter options that filter
returned information to include only those classes that have the defined filter
option. Thus, ``pywbemcli class enumerate --association`` displays only classes
that have the Association qualifier set. The filters are documented in the
`class filter options table`_  below.

All of this filtering is done in pywbemcli so that it may require that
significant information on the classes be requested from the server that would
not be required without the filter. Thus, these commands may take more processing
time.

.. index::
    single: result filters; class enumerate command
    pair; --association; Command Option
    pair: --indication; Command Option
    pair: --experimental; Command Option
    pair: --deprecated; Command Option
    pair: --since; Command Option
    pair: --schema; Command Option
    pair: --subclasses; Command Option
    pair: --leaf-classes; Command Option

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
4. The ``--leaf-classes`` filter can be important because the
   :ref:`pywbem MOF compiler <pywbem:MOF Compiler>` can compile all dependent
   classes given only the leaf classes. Thus, if the bottom class in a
   class hierarchy is specified, a path to schema classes is specified, and
   all classes are in files defined by the name of the class, the compiler
   will find and compile all super classes upon which the leaf class depends.
   NOTE: The user can observe this behavior be enabling the verbose mode
   :ref:`--verbose general option`.

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


.. index::
    pair: namespace; multiple namespace commands
    pair: --namespace; Command Option

.. _`Using multiple namespaces with server requests`:

Using multiple namespaces with server requests
----------------------------------------------

This feature was added in pywbemcli version 1.1.0.

Generally the CIM/XML commands defined by the DMTF execute operations on a single
:term:`CIM namespace` in the WBEM server.  Thus, the command:

    instance enumerate <classname> -n interop

is a request to the WBEM server to return instances of of <classname> from
namespace ``interop``.

However, pywbemcli expands this in version 1.1.0  to allow some requests to be executed against
multiple namespaces in a single request.  This was done primarily to allow
viewing CIM objects in the server across namespaces (ex. comparing classes
or instances between namespaces).

The commands ``enumerate``, ``get``, ``associators``, and ``references`` for
the command groups ``class`` and ``instance`` and the ``enumerate`` and ``get``
for the command group qualifiers allow issuing requests on multiple namespaces
in a single pywbemcli command. Multiple namespaces for a command is defined with
the ``--namespace`` option by defining the set of namespaces to be included
rather than just a single namespace. If the ``default-namespace`` is not
defined is the connection default namespace.

Thus, the requests below command pywbecli to make a request for each of the
namespaces interop and root/comv2 and to present the results of both requests
in a single response.

    class enumerate CIM_ManagedElement -n interop, root/cimve
    class enumerate CIM_ManagedElement -s interop -n root/cimv2

The responses are displayed in the same form as for a single namespace except
that the namespace is included for each type of output format to allow the user to
determine which object is in which namespace.  With MOF, the namespace appears as
a MOF namespace pragma (commented because not all WBEM server compilers honor the
namespace pragma). With tables, a namespace column is included in the table.

The order of the objects displayed in responses is controlled by a command
options ``--object-order``.  The default order is to order the objects by
namespace but defining this option allows modifying the order to display
objects ordered by object name which allows comparing objects between namespaces.

For example:

.. code-block:: text

    # pywbemcli instance enumerate CIM_Door --namespace root/cimv2,root/cimv3

return the instances of CIM_Door from two namespaces root/cimv2 and root/cimv3.

A table output has the following form with table output

.. code-block:: text

    pywbemcli> -o table instance enumerate CIM_Foo -n root/cimv2,root/cimv3
    Instances: CIM_Foo
    +-------------+---------------------+---------------+
    | namespace   | InstanceID          | IntegerProp   |
    |-------------+---------------------+---------------|
    | root/cimv2  | "CIM_Foo1"          | 1             |
    | root/cimv2  | "CIM_Foo2"          | 2             |
    | root/cimv2  | "CIM_Foo3"          |               |
    | root/cimv2  | "CIM_Foo30"         |               |
    | root/cimv2  | "CIM_Foo31"         |               |
    | root/cimv2  | "CIM_Foo_sub1"      | 4             |
    | root/cimv2  | "CIM_Foo_sub2"      | 5             |
    | root/cimv2  | "CIM_Foo_sub3"      | 6             |
    | root/cimv2  | "CIM_Foo_sub4"      | 7             |
    | root/cimv3  | "CIM_Foo1"          | 1             |
    | root/cimv3  | "CIM_Foo2"          | 2             |
    | root/cimv3  | "CIM_Foo3"          |               |
    | root/cimv3  | "CIM_Foo3-third-ns" | 3             |
    | root/cimv3  | "CIM_Foo30"         |               |
    | root/cimv3  | "CIM_Foo31"         |               |
    | root/cimv3  | "CIM_Foo_sub1"      | 4             |
    | root/cimv3  | "CIM_Foo_sub2"      | 5             |
    | root/cimv3  | "CIM_Foo_sub3"      | 6             |
    | root/cimv3  | "CIM_Foo_sub4"      | 7             |
    +-------------+---------------------+---------------+

The --namespace option can be defined either using multiple definitions of the
option: ``--namespace root/cimv2 --namespace root/cimv3`` or as a single
options with comma-separated namespace names : ``--namespace root/cimv2,root/cimv3``.

The :ref:`Class find command` and  also process multiple namespaces in a single
request but the default if the namespace is not provided is to use all of the
namespaces defined in the server since the goal of these commands is to execute
a wide search for the define class or instance entities.

To execute a request for multiple namespaces, pywbemcli executes the
corresponding server request (ex. GetInstance) once for each namespace defined
in the ``--namespace`` parameter. If a request for processing a command for
multiple namespaces gets an exception for some of the requests but not all of
them (ex. the class for a class get request only exists in some of the
namespaces) it continues processing until all of the namespaces are processed
and generates a warning message for each request exception.  If all the
requests fail, the command fails.  If any of server requests return results,
those results are displayed.
