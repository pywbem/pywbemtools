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


.. _`Pywbemcli command groups, commands, and subcommands`:

Pywbemcli command groups, commands, and subcommands
===================================================

This section defines the characteristics of each of the pywbemcli command
groups and subcommands including examples.

The command syntax of pywbemcli is:

.. code-block:: text

    $ pywbemcli <general-options> <cmd-group>|<command> <args>

where:

.. code-block:: text

        cmd-group := <command> <subcommand>

Within pywbemcli each command-group name is a noun, referencing an entity (ex.
class, instance, server).

.. code-block:: text

    $ pywbemcli -s http://localhost class get CIM_ManagedElement

defines a command to get the class ``CIM_ManagedElement`` from the current
target server and display it in the defined output format.

The pywbemcli command groups and commands are described below and the help
output from pywbemcli for each command documented in :ref:`pywbemcli Help
Command Details`

**NOTE:** Many of the examples below use the ``pywbem_mock`` module
(``-m``\``--mock-server`` general option) with mock files in the pywbemtools
tests/unit subdirectory to generate known results.

.. _`Pywbemcli special command line features`:

Pywbemcli special command line features
---------------------------------------

Pywbemcli includes several features in the command syntax that are worth
presenting in detail to help the user understand the background purpose and
syntactic implementation of the features. This includes:

* The ability to execute either the pull or traditional operations with the
  same command group.

* The ability to receive either CIM instances or CIM instance names with only
  a change of an option on the commands that request CIM instances. The option
  ``-o`` or ``--names-only`` defines whether only the instance name or the complete
  object will be displayed.

* The ability to interactively select the data for certain objects as opposed
  to having to enter the full name.


.. _`Using pywbem Pull Operations from pywbemcli`:

Using pywbem Pull Operations from pywbemcli
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pywbem includes multiple ways to execute the enumerate instance type operations
(``Associators``, ``References``,`` EnumerateInstances``, ``ExecQuery``):

* The traditional operations (ex. ``EnumerateInstances``)
* The pull operations (ex. the pull sequence ``OpenEnumerateInstances``, etc.)
* An overlay of the above two operations called the ``Iter..``. operations where
  each ``Iter..`` operation executes either the traditional or pull operation
  depending on a parameter of the connection.

Pywbemcli implements these method calls to pywbem using the ``Iter...``
operations so that either pull operations or traditional operation can be used
simply by changing a pywbemcli input parameter (``--use-pull-ops``).

Two options on the command line allow the user to either force the use of pull
operations, of traditional operations, or to let pywbem try them both.

The input parameter ``--use-pull-ops`` allows the choice of pull or traditional
operations with the default being to allow pywbem to decide.  The input
parameter ``max_object_cnt`` sets the ``MaxObjectCount`` variable on the operation
request if the pull operations are to be used which tells the WBEM server to
limit the size of the response.  For example::

    pywbemcli --server http/localhost use-pull-ops=yes max_object_cnt=10

would force the use of the pull operations and return an error if the target
server did not implement them and would set the ``MaxObjectCount`` parameter on the
api to 10, telling the server that a maximum of 10 objects can be returned for
each of the requests in an enumeration sequence.

Since the default for use-pull-ops is ``either``, normally pywbem first tries
the pull operation and then if that fails, the traditional operation.  That
is probably the most logical setting for ``use-pull-ops`` unless you are
specifically testing the use of pull operations.


.. _`pywbemcli commands to WBEM Operations`:

pywbemcli commands to WBEM Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following table defines which pywbemcli commands are used for the
corresponding pywbem request operations.

=================================  ==============================================
WBEM CIM-XML Operation             pywbemcli command-group & subcommand
=================================  ==============================================
**Instance Operations:**
EnumerateInstances                 instance enumerate INSTANCENAME
EnumerateInstanceNames             instance enumerate INSTANCENAME --name_only
GetInstance                        instance get INSTANCENAME
ModifyInstance                     instance modify
CreateInstance                     instance create
DeleteInstance                     instance delete INSTANCENAME
Associators(instance)              instance associators INSTANCENAME
Associators(class)                 class associators CLASSNAME
AssociatorNames(instance)          instance associators INSTANCENAME --name_only
AssociatorNames(class)             class associators CLASSNAME --name_only
References(instance)               instance references INSTANCENAME
References(class)                  class references CLASSNAME
ReferenceNames(instance)           instance references INSTANCENAME --name_only
ReferenceNames(class)              class references CLASSNAME --name_only
InvokeMethod                       instance invokemethod INSTANCENAME --name_only
ReferenceNames                     class invokemethod CLASSNAME --name_only
ExecQuery                          instance query
**Pull Operations:**               Option --use-pull-ops ``either`` or ``yes``
OpenEnumerateInstances             instance enumerate INSTANCENAME
OpenEnumerateInstancePaths         instance enumerate INSTANCENAME --name_only
OpenAssociatorInstances            instance associators INSTANCENAME
OpenAssociatorInstancePaths        instance associators INSTANCENAME --name_only
OpenReferenceInstances             instance references INSTANCENAME
OpenReferenceInstancePaths         instance references INSTANCENAME --name_only
OpenQueryInstances                 instance references INSTANCENAME --name_only
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

1. The pywbem ``Iter...`` operations are all used as the common code path by
pywbemcli to access CIM instances from the WBEM server. It is these operations
that determine whether the original operations (ex. ``EnumerateInstances``)


.. _`Displaying CIM instances or CIM instance names`:

Displaying CIM instances or CIM instance names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The pywbem API includes different WBEM operations (ex. ``EnumerateInstances`` and
``EnumerateInstanceNames``) to request CIM objects or just their names. To
simplify the overall command line syntax pywbemcli combines these into a single
subcommand (i.e. ``enumerate``, ``references``, ``associators``) and includes
an option (``-o,`` or ``--names-only``) that determines whether the instance
names or instances are retrieved from the WBEM server.

Thus, for example an ``instance enumerate`` with and without the ``-o`` option:

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

    $ pywbemcli --mock-server tests/unit/simple_mock_model.mof instance enumerate CIM_Foo -o

    root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"

    root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"

    root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"

.. _`Interactively selecting INSTANCENAME`:

Interactively selecting INSTANCENAME
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arguments like the INSTANCENAME on some of the instance group subcommands (
``get``, ``references``, ``associators``, etc) can be very difficult to correctly enter
since it can involve multiple keybindings, use of quotation marks, etc.  To
simplify this pywbemcli includes a option (``-i`` or ``--interactive``) on
these commands that allows the user to specify only the class name, retrieves
all the instance names from the server and presents the user with a select list
from which an instance name can be chosen. The following is an example:

.. code-block:: text

    $ pywbemcli --mock-server tests/unit/simple_mock_model.mof instance get CIM_Foo --interactive
    Pick Instance name to process
    0: root/cimv2:CIM_Foo.InstanceID="CIM_Foo1"
    1: root/cimv2:CIM_Foo.InstanceID="CIM_Foo2"
    2: root/cimv2:CIM_Foo.InstanceID="CIM_Foo3"
    Input integer between 0 and 2 or Ctrl-C to exit selection: 0  << user enters 0
    instance of CIM_Foo {
       InstanceID = "CIM_Foo1";
       IntegerProp = 1;
    };


.. _`Class command-group`:

Class command-group
-------------------

The **class** group defines subcommands that act on CIM classes. see
:ref:`pywbemcli class --help`. This group includes the following commands:

* **associators** to retrieve the class associators classes or classnames if the
  (``-o``/``--names-only``) option is set for a class defined by the CLASSNAME
  argument in the namespace with this subcommand or the default
  namespace and displayed in the defined format. If successful it displays the
  classes/classnames in the :term:`CIM model output formats` (see
  :ref:`Output formats`). If unsuccesful it an exception. This subcommand
  returns the class associators, not the instance associators. The
  :ref:`Instance command-group` includes the corresponding associators
  operation for instances:

  .. code-block:: text

      $ pywbemcli --name mockassoc class associators TST_Person --names_only
        //FakedUrl/root/cimv2:TST_Person
      $

  See :ref:`pywbemcli class associators --help` for details.
* **references** to get the class level reference classes or classnames for a
  class defined by the CLASSNAME argument in the default namespace or the namespace
  defined with this subcommand displayed in the defined format. If successful
  it displays the classes/classnames in the :term:`CIM model output formats`
  (see :ref:`Output formats`). If unsuccesful it an exception.. This returns
  the class level references,not the instance references. The :ref:`Instance
  command-group` includes a corresponding instance references operation:

  .. code-block:: text

    $pywbemcli --mock-server mockassoc class references TST_Person --names-only

    //FakedUrl/root/cimv2:TST_Lineage
    //FakedUrl/root/cimv2:TST_MemberOfFamilyCollection

  See :ref:`pywbemcli class associators --help` for details.
* **delete** to delete the class defined by the ``CLASSNAME`` argument. Note that
  many WBEM servers may not allow this operation or may severely limit the
  conditions under which a class can be deleted from the server.  If successful
  it returns nothing, otherwise it displays an exception.

  To delete the class ``CIM_Blah``:

  .. code-block:: text

    $ pywbemcli class delete CIM_blah
    $

  Pywbemcli will not delete a class that has subclasses.
  See :ref:`pywbemcli class delete --help` for details.
* **enumerate** to enumerate classes or their classnames in the default
  namespace or the namespace defined with this subcommand. If the CLASSNAME
  input property the enumeration starts at the subclasses of CLASSNAME. Otherwise
  it starts at the top of the class hierarchy if the
  ``--DeepInheritance``/``-d``  option is set it shows all the classes in the
  hierarchy, not just the next level of the hierarchy. Otherwise it only
  enumerates one level of the class hierarchy.  It can display the
  classes/classnames in the :term:`CIM model output formats` (see
  :ref:`Output formats`). The following example enumerates
  the class names starting at the root of the class hiearchy for a simple
  mocked CIM schema definition:

  .. code-block:: text

    $ pywbemcli --mock-server mockassoc class enumerate --names-only
    TST_Person
    TST_Lineage
    TST_MemberOfFamilyCollection
    TST_FamilyCollection
    $

  See :ref:`pywbemcli class enumerate --help` for details.
* **find** to find classes in the target WBEM server across multiple namespaces.
  The input argument is a GLOB expression which is used to search the server
  CIM namespaces for matching class names.  This subcommand uses a :term:`GLOB`
  Unix style pathname pattern expansion on the classname to attempt to filter
  the names and namespaces of all of the classes in the WBEM server (or the
  namespaces defined with the ``--namespaces``/``-n`` option):

  .. code-block:: text

      $ pywbemcli> class find .*_WBEMS*
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
      $

  See :ref:`pywbemcli class find --help` for details.
* **get** to get a single class defined by the required CLASSNAME argument in the
  default namespace or the namespace defined with this subcommand displayed in
  the format defined by the ``--output-format``/``-o`` general option. If
  successul it displays the returned class, otherwise it displays the exception
  generated.  It can display the classes/classnames in the :term:`CIM model
  output formats` (see :ref:`Output formats`).

  The following example shows getting the MOF representation of the class
  ``CIM_Foo`` from a mock repository that is named mock1 in the
  :term:`connections file`:

  .. code-block:: text

      $ pywbemcli> --name mock1 class get CIM_Foo

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

  See :ref:`pywbemcli class get --help` for details.
* **invokemethod** to invoke a method defined for the CLASSNAME argument. This
  subcommand executes the invokemethod with a class name, not an instance name
  and any input parameters for the InvokeMethod defined with the
  ``--parameter``\`-p`` option. If successful it returns the method return
  value and output parameters received from the server. If unsuccessful it
  displays the exception generated. It displays the return value as an integer and
  any returned CIM parameters in the :term:`CIM model
  output formats` (see :ref:`Output formats`)See :ref:`pywbemcli class invokemethod
  --help` for details.
* **tree** to display the class hierarchy as a tree.  This subcommand
  outputs a tree format in ASCII defining the either the subclass or superclass
  hierarchy of the class name input parameter as a tree:

  .. code-block:: text

      $ pywbemcli class tree CIM_Foo

        CIM_Foo
         +-- CIM_Foo_sub
         |   +-- CIM_Foo_sub_sub
         +-- CIM_Foo_sub2

  It can show either the subclasses or the superclasses of the defined class
  using the (``--superclasses`` option).

  This subcommand ignores the ``--output-format``\``-o' general option and
  always outputs the tree format.

  See :ref:`pywbemcli class tree --help` for details.


.. _`Instance command-group`:

Instance command-group
----------------------

The **instance** group defines subcommands that act on CIM instances including:

* **associators** to get the associator instances for the instance name defined
  as the :term:`INSTANCENAME` argument in the default namespace or the namespace defined with this
  subcommand displayed in the defined format. If successful it returns the
  instances or instancenames associated with INSTANCENAME otherwise it returns any
  exception generated by the response This subcommand displays the returned instances
  or instance in the :term:`CIM model output formats` or the table formats` (see
  :ref:`Output formats`).:

  .. code-block:: text

    $ pywbemcli --name mockassoc instance references TST_Person --names-only --interactive
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
    $

  See :ref:`pywbemcli instance associators --help` for details.
* **count** count the number of CIM instances in a namespace. For example:

  .. code-block:: text

        $ pywbemcli --name mockassoc instance count
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
  ``instance enumerate`` would show the instance for that class and its
  subclasses.

  Count is useful to determine which classes in the environment are actually
  implemented. However this subcommand can take a long time to execute because
  it must a) enumerate all the classes in the namespaces, b) enumerate the
  instances for each class.

  See :ref:`pywbemcli instance count --help` for details.
* **create** create a CIMInstance of the CLASSNAME argument in a namespace
  defined with as an option to the subcommand or the default namespace in the
  WBEM server. The command build the CIMInstance from the class defined by
  CLASSNAME and the properties defined by the ``--property``\``-p`` option The
  properties are defined as name/value pairs, one property for each instance of
  the ``--property`` option. Since the WBEM server (and pywbem) requires that
  each property be typed, pywbemtools uses the CIMClass defined by CLASSNAME
  retrieved from the WBEM server to define the type required to define the
  CIMProperty.

  For a single property in the new instance this is simply the `--property`` option
  with the property name and value:

  .. code-block:: text

    --property <property-name>=<property-value"

    where quotes are only required if the value includes whitespace.

  For array properties the values are defined separated by commas:

  .. code-block:: text

    -p <property-name>=<value>(,<value>)

  An example with two properties, InstanceId a scalar string property and intarr
  an array integer property. Note that the --property value does not determine
  the property type. However, generally integers and float values are used for
  integer and float property types.

  If the create is successful, the server defined CIM Instance path is displayed.
  If the operation fails, the exception is displayed. If there is a descrepency
  between the defined properties and the CIMClass property characteristics
  pywbemcli generates an exception.

  The following example creates an instance of the class TST_Blah with one
  scalar and one array property.

  .. code-block:: text

    $pywbemcli instance create TST_Blah InstancId="blah1", intprop=3, intarr=3,6,9

  See :ref:`pywbemcli instance create --help` for details.
* **delete** delete an instance defined by the :term:`INSTANCENAME` argument
    in a namespace defined by either the ``--namespace` option or the general
    `--default-namespace`` The form of INSTANCENAME is determined by the
    ``--interactive`` options and must be either:

    * a string representation of a CIMInstanceName as defined by a :term:`WBEM-URI`
    * A class name in which case pywbemcli will get the instance names from the
      WBEM server and present a selection list for the user to select an
      instance name :ref:`Displaying CIM instances or CIM instance names`

  The following example deletes the instance defined by the explicit instance
  name (Note the extra backslash required to escape the double quote on the
  terminal):

  .. code-block:: text

    $ pywbemcli --name mockassoc instance delete root/cimv2:TST_Person.name=\"Saara\"
    $

  See :ref:`pywbemcli instance delete --help` for details.
* **enumerate** to enumerate instances or their paths defined by the CLASSNAME
  argument in the namespace defined by ``-o``\``--namespace`` or the general option
  ``-o``\``--default-namespace`` in the defined format. This subcommand displays the
  returned instances or instance names in the :term:`CIM model output formats`
  or the table formats` (see :ref:`Output formats`).

  The following example returns a two instanced to an ``instance enumerate``
  command as MOF:

  .. code-block:: text

    $ pywbemcli --name mockassoc instance enumerate TST_FamilyCollection

    instance of TST_FamilyCollection {
       name = "family1";
    };

    instance of TST_FamilyCollection {
       name = "Family2";
    };

  See :ref:`pywbemcli instance enumerate --help` for details.
* **get** to get a single CIM instance defined by the :term:`INSTANCENAME`
    argument from the default namespace or the namespace defined with the
    subcommand displayed in the defined format. The form of :term:`INSTANCENAME` is
    determined by the ``--interactive`` option. It can display the returned
    instance in the :term:`CIM model output formats` or the table formats`
    (see :ref:`Output formats`). Otherwise it returns the received exception.

    This example successfully retrieves the instance defined by the INSTANCENAME
    ``root/cimv2:TST_Person.name=\"Saara\"``:

    .. code-block:: text

        $ pywbemcli --name mockassocinstance instance get root/cimv2:TST_Person.name=\"Saara\"

        instance of TST_Person {
           name = "Saara";
        };

  See :ref:`pywbemcli instance get --help` for details.
* **invokemethod** to invoke a method defined for the class argument.
  See :ref:`pywbemcli instance invokemethod --help` for details.
* **modify** modify an existing instance of the class defined by the CLASSNAME argument
  in the WBEM server  namespace defined by either the default namespace or
  namespace option. The user provides the definition of an instance in the same
  form as the ``add`` subcommand but the instance must already exist in the
  WBEM server and the instance created from the command line must include all
  of the key properties so that it can be identified in the server.

  If successful, this subcommand displays nothing, otherwise it displays the
  received exception.

  See :ref:`pywbemcli instance modify --help` for details.
* **references** to get the reference instances or paths for a
  instance defined as the :term:`INSTANCENAME` input argument in the default
  namespace or the namespace defined with this subcommand displayed in the
  defined format. It can display any returned instances in the
  :term:`CIM model output formats` or the table formats`
  (see :ref:`Output formats`). Otherwise it returns the received exception.:

  .. code-block:: text

      $ pywbemcli --name mockassocinstance instance references root/cimv2:TST_Person.name=\"Saara\"
      instance of TST_Lineage {
         InstanceID = "SaaraSofi";
         parent = "/root/cimv2:TST_Person.name=\"Saara\"";
         child = "/root/cimv2:TST_Person.name=\"Sofi\"";
      };

  See :ref:`pywbemcli instance references --help` for details.
* **query** to execute an execquery with query string defined as an argument.
  The QUERY argument must be a valid query defined for the ``--querylanguage``
  option and available in the WBEM server being queried.  The default for
  the ``--querylanguage`` option is DMTF:CQL but any query language and query
  will be passed to the server.

  It displays any instances returned in the defined formats or any exception
  returned.  It can display any returned instances in the :term:`CIM model
  output formats` or the table formats` (see :ref:`Output formats`)
  See :ref:`pywbemcli instance query --help` for details.

.. _`qualifier command-group`:

Qualifier command-group
-----------------------

The **qualifier** command-group defines subcommands that act on
CIMQualifierDeclaration entities in the WBEM server including:

* **get** to get a single qualifier declaration defined by the ``QUALIFIERNAME``
  argument from the namespace in the target WBEM server defined with this command  or
  the default_namespace and display in the defined output format. The output
  formats can be either one  of the :term:`CIM model output formats` or the
  table formats` (see :ref:`Output formats`).

  The following example gets the ``Key`` qualifier declaration from the
  default namespace:

  .. code-block:: text

    $ pywbemcli --name mockassocinstance.mof qualifier get Key
    Qualifier Key : boolean = false,
        Scope(property, reference),
        Flavor(DisableOverride, ToSubclass);

  See :ref:`pywbemcli qualifier get --help` for details.

* **enumerate** to enumerate all qualifier declarations within the namespace
  defined with this subcommand or the default namespace in the target WBEM
  server . The output formats can be either one  of the
  :term:`CIM model output formats` or the table formats`
  (see :ref:`Output formats`).

  This example displays all of the qualifier declarations in the default
  namespace as a simple table.

  .. code-block:: text

    $ pywbemcli --name mockassocinstance --output-format table qualifier enumerate

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

.. _`Server command-group`:

Server command-group
--------------------

The **server** command-group defines subcommands that interact with a WBEM
server to access information about the WBEM server itself. These subcommands
are generally not namespace specific but access information about the server,
namespaces, etc. The subcommands are:

* **brand** to get general information on the server.  Brand information is an
  attempt by pywbem and pywbemtools to determine the product that represents
  the WBEM server infrastructure.  Since that was not clearly defined in the DMTF
  specifications, this subcommand may return strange results but it returns
  legitimate results for most servers:

  .. code-block:: text

    $ pywbemcli --name op server brand
    Server Brand:
    +---------------------+
    | WBEM server brand   |
    |---------------------|
    | OpenPegasus         |
    +---------------------+

  See :ref:`pywbemcli server brand --help` for details.
* **connection** to display information on the connection defined for this
  server.  This is same information as was defined when the connection was
  saved with ``connection save`` or the cli general options:

  .. code-block:: text

    $pywbemcli --name op server connection

    url: http://localhost
    creds: ('kschopmeyer', 'test8play')
    .x509: None
    default_namespace: root/cimv2
    timeout: 30 sec.
    ca_certs: None

  See :ref:`pywbemcli server connection --help` for details.
* **info** to get general information on the server.  This subcommand returns
  information on the brand, namespaces, and other reasonable information on the
  WBEM server:

  .. code-block:: text

    $ pywbemcli --name op server info
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
* **interop** to get a the name of the interop namespace target WBEM server:

  .. code-block:: text

    $ pywbemcli --name op server interop
    Server Interop Namespace:
    +------------------+
    | Namespace Name   |
    |------------------|
    | root/PG_InterOp  |
    +------------------+

  See :ref:`pywbemcli server interop --help` for details.
* **namespaces** to get a list of the namespaces defined in the target server:

  .. code-block:: text

    $ pywbemcli --name op -output-format plain server namespaces
    Server Namespaces:
    Namespace Name
    root/PG_InterOp
    root/benchmark
    root/SampleProvider
    test/CimsubTestNS2
    test/CimsubTestNS3
    test/CimsubTestNS0
    test/CimsubTestNS1
    root/PG_Internal
    test/WsmTest
    test/TestIndSrcNS1
    test/TestINdSrcNS2
    test/EmbeddedInstance/Static
    test/TestProvider
    test/EmbeddedInstance/Dynamic
    root/cimv2
    root
    test/cimv2
    test/static
    $

  See :ref:`pywbemcli server namespaces --help` for details.
* **profiles** to get information on the WBEM management profiles
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


     $ pywbemcli --output-format simple  --name op server profiles
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
* **get_centralinsts** to get the instance names of the central/scoping
  instances of one or more :term:`WBEM management profile` s defined in the
  target WBEM server:

  .. code-block:: text


    $ pywbemcli> server centralinsts --org DMTF --profile "Computer System"
    Advertised Central Instances:
    +---------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Profile                         | Central Instances                                                                                                                                                                                                                       |
    |---------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | DMTF:Computer System:1.0.0      | //leonard/test/TestProvider:Test_StorageSystem.Name="StorageSystemInstance1",CreationClassName="Test_StorageSystem"://leonard/test/TestProvider:Test_StorageSystem.Name="StorageSystemInstance2",CreationClassName="Test_StorageSystem" |
    +---------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  See :ref:`pywbemcli server get-centralinsts --help` for details.

.. _`Connection command-group`:

Connection command-group
------------------------

The **connection** command-group defines subcommands that provide for a
persistent file (:term:`connections file`) of WBEM server connection
parameters and allow selecting entries in this file as well as adding entries
to the file, deleting entries from the file and viewing WBEM servers defined in the
the file. This allows multiple connections to be defined and then used by name
rather than through the detailed parameters of the connection.

Connections in the :term:`connections file` can be created by:

* Using the ``connection add`` subcommand. This allows defining the parameters
  of a connection as a subcommand.

* Using the ``connection save`` subcommand with the current connection. This options
  uses the parameters current connection to define and save a connection in the
  connections file.

The connection information for each connection is based on the information
used to create a connection and is largely the same information as is in the
options for pywbemcli. The data includes:

* **name** name of the connection (required).
* **server_url** the url for the defined connection (required unless
  ``--mock-server``/``-m`` defined).
* **default_namespace** the default namespace defined for the connection
  (required).
* **user** the user name for the connection (optional).
* **password** the password for the connection (optional).
* **noverify** the boolean value of the certificate noverify option.  The
  default is False.
* **certfile** optional server certificate filename.
* **keyfile** optional client private keyfile filename.
* **use_pull_ops** optional parameter that defines whether pull operations are
  to be required, used if they exist or not used.
* **pull_max_cnt** optional count of object per pull operation.
* **timeout** optional timeout value.
* **timestats** boolean that determines if time stats are captured.
* **log** optional log configuration.
* **verbose** optional boolean that enables the verbose mode.
* **output-format** optional output format.
* **mock_server** optional definition of the files that define a mock server
  environment using the pywbem mock module. This parameter is used, the
  ``--server_url`` must not be defined.

The :term:`connections file` is named ``pywbemcliservers.json`` in the directory
in which pywbemcli is executed. The data is stored in JSON format within this
file.  Multiple connection files may be maintained in separate directories.

The subcommands include:

* **add** creates a new connection using the subcommand arguments and sets the new
  connection as the current connection. This subcommand saves the
  new connection to the :term:`connections file` (see ``connection save``).

  The following example shows creating a new connection from within the
  interactive mode of pywbemcli. The parameters for the connection are defined
  through the input options for the subcommand. These use the same option names
  as the corresponding general options to define the WBEM server:

  .. code-block:: text

    pywbemcli> connection add --name me --server http://localhost --user me --password mypw -no-verify
    pywbemcli> connection list
    WBEMServer Connections:
    +-----------+------------------+-------------+-------------+------------+-----------+------------+------------+-----------+-------+
    | name      | server uri       | namespace   | user        | password   |   timeout | noverify   | certfile   | keyfile   | log   |
    |-----------+------------------+-------------+-------------+------------+-----------+------------+------------+-----------+-------|
    | me*       | http://localhost | root/cimv2  | me          | mypw       |           | True       |            |           |       |
    | mock1     |                  | root/cimv2  |             |            |        30 | False      |            |           |       |
    | mockassoc |                  | root/cimv2  |             |            |        30 | False      |            |           |       |
    | op        | http://localhost | root/cimv2  | kschopmeyer | test8play  |        30 | True       |            |           |       |
    +-----------+------------------+-------------+-------------+------------+-----------+------------+------------+-----------+-------+
    pywbemcli>

  NOTE: The ``*`` on the name indicates the current connection, the one that
  will be used for any subsequent commands within a single interactive session.
  This can be changed using ``connection select``

  See :ref:`pywbemcli connection add --help` for details.
* **delete** delete a specific connection by name or by selection. The following
  example deletes the connection defined in the add subcommand above:

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

    $


  See :ref:`pywbemcli connection delete --help` for details.
* **export** export the current connection information as environment variables.
  See :ref:`pywbemcli connection export --help` for details.
* **list** list the connections in the :term:`connections file` as a table. This produces
  a table output showing the connections defined in the connections file.

  See :ref:`pywbemcli connection list --help` for details.
* **save** Save the current connection information
  to the :term:`connections file`.  If the current connection does not have a name
  a console request asks for a name for the connection.
  See :ref:`pywbemcli connection save --help` for details.
* **select** select a connection from the connection table.  A connection
  may be selected either by using the name argument or if no argument is
  provided by selecting from a list presented on the console. The following
  example shows changing connection from within the interactive mode of pywbemcli:

  .. code-block:: text

    pywbemcli> connection select
    Select a connection or Ctrl_C to abort.
    0: mock1
    1: mockassoc
    2: op
    Input integer between 0 and 2 or Ctrl-C to exit selection: 1
    pywbemcli> connection list
    WBEMServer Connections:
    +------------+------------------+-------------+-------------+------------+-----------+------------+------------+-----------+-------+
    | name       | server uri       | namespace   | user        | password   |   timeout | noverify   | certfile   | keyfile   | log   |
    |------------+------------------+-------------+-------------+------------+-----------+------------+------------+-----------+-------|
    | mock1      |                  | root/cimv2  |             |            |        30 | False      |            |           |       |
    | mockassoc* |                  | root/cimv2  |             |            |        30 | False      |            |           |       |
    | op         | http://localhost | root/cimv2  | kschopmeyer | test8play  |        30 | True       |            |           |       |
    +------------+------------------+-------------+-------------+------------+-----------+------------+------------+-----------+-------+
    $ pywbemcli> connection show

    Name: mockassoc
      WBEMServer uri: None
      Default_namespace: root/cimv2
      User: None
      Password: None
      Timeout: 30
      Noverify: False
      Certfile: None
      Keyfile: None
      use-pull-ops: either
      pull-max-cnt: 1000
      mock: tests/unit/simple_assoc_mock_model.mof
      log: None

  See :ref:`pywbemcli connection select --help` for details.
* **show** show information in the current connection.  See the the ``select``
  above for an example of this subcommand.

  See :ref:`pywbemcli connection show --help` for details.
* **test** execute a single predefined operation on the current connection
  to determine if it is a WBEM server. It executes a single ``EnumerateClasses``
  WBEM operation in the default namespace. If the server accepts the request
  a simple text ``Connection successful`` will be returned.

  See :ref:`pywbemcli connection test --help` for details.

  The following example defines the connection with ``--server``, ``--user``,
  and ``--pasword`` and executes the test with successful result:

 .. code-block:: text

  $ pywbemcli --server http://localhost --user me --password mypw connection test
  $ Connection successful

  An unsuccessful test will normally result in an exception that defines the
  issue as follows for the server http://blah in the example below:

  .. code-block:: text

  pywbemcli -s http://blah connection test
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

or by executing the script without any command or command-group:

  .. code-block:: text

   $ pywbemcli
   Enter 'help' for help, <CTRL-D> or ':q' to exit pywbemcli.
   pywbemcli>

The repl mode is recognized by the prompt ``pywbemcli>``.


.. _`Help command`:

Help command
------------

The help command provides information on special commands and controls that can
be executed in the :ref:`interactive mode`. This is different from the
``--help`` option that provides information on command groups, and subcommands.


