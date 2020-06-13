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

* The ability to define complete INSTANCE name command arguments or
  interactively select the instance namesfrom a list presented by
  pywbemcli for certain objects rather than typing in long names the full name.
  see :ref:`Specifying the INSTANCENAME command argument`.


.. _`pywbemcli commands to WBEM operations`:

pywbemcli commands to WBEM operations
-------------------------------------

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
**QualifierDeclaration ops:**
EnumerateQualifiers                qualifier enumerate
GetQualifier                       qualifier get QUALIFIERNAME
SetQualifier                       Not implemented
DeleteQualifier                    Not Implemented
=================================  ==============================================


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


.. _`Specifying the INSTANCENAME command argument`:

Specifying the INSTANCENAME command argument
--------------------------------------------

The INSTANCENAME argument used by some pywbemcli commands (e.g ``instance get``)
specifies the instance path (aka instance name) of a CIM instance in a CIM
namespace of a WBEM server.

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
