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


.. _`Pywbemcli command groups, comands and subcommands`:

Pywbemcli command groups, comands and subcommands
=================================================

The command syntax of pywbemcli is::

    $ pywbemcli <general-options> <cmd-group>|<command> <args>

    where:
        cmd_group = <command> <subcommand>

Each command group is a noun, referencing an entity (ex. class).

    $ pywbemcli -s http://localhost class get CIM_ManagedElement

defines a command to get the class `CIM_ManagedElement` from the current
target server and display it in the defined output-format.

The pywbemcli command groups are described below and the help output from
pywbemcli documented in :ref:`pywbemcli Help Command Details`

.. _`Class command group`:

Class command group
-------------------

The **class** group defines subcommands that act on CIM classes. see
:ref:`pywbemcli class --help`. This group includes the following commands:

* **associators** to get the class level associators for a class defined
  as an input argument in the default namespace or the namespace defined with this
  subcommand display in the defined format. This subcommand can display the
  class in several formats including MOF, XML, and REPR. It requires the class
  name as input.  This returns the class level associators but not the instance
  associators. The :ref:`Instance subcommand group` includes the corresponding
  associators operation for instances::

      $ pywbemcli --name mockassoc class associators TST_Person --names_only
        //FakedUrl/root/cimv2:TST_Person
      $

  See :ref:`pywbemcli class associators --help` for details.
* **delete** to delete the class defined by the CLASSNAME argument. Note that
  many WBEM servers may not allow this operation or may severely limit the
  conditions under which a class can be deleted from the server. For example::

    $ pywbemcli class delete CIM_blah     << attempt to delete CIM_Blah
    $

  Pywbemcli will not delete a class that has subclasses.
  See :ref:`pywbemcli class delete --help` for details.
* **enumerate** to enumerate classes or their classnames in the default
  namespace or the namespace defined with this subcommand.  If the
  ``--DeepInheritance``/``-d`  option is set it shows all the classes in the
  hiearchy, not just the next level f the hiearchy::

    $ pywbemcli --mock-server mockassoc class enumerate --name-only
    TST_Person
    TST_Lineage
    TST_MemberOfFamilyCollection
    TST_FamilyCollection
    $

  See :ref:`pywbemcli class enumerate --help` for details.
* **find** to find classes in the target WBEM server across namespaces.  The
  input argument is a regular expression which is used to search namespaces
  for matching class names.  This subcommand uses a regex for the classname to
  attempt to list the names and namespaces of all of the classes in the WBEM
  Server (or the namespaces defined with the ``--namespaces``/``-n` option)::

      $ pywbemcli> class find .*_WBEMS
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
* **get** to get a single class in the default namespace or the namespace
  defined with this subcommand and display in the defined format. This
  subcommand can display the class in several formats including MOF, XML, and
  REPR. It requires the class name as input::

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
* **invokemethod** to invoke a method defined for the class argument. This
  subcommand executed the invokemethod with the classname, not an instance
  name.   See :ref:`pywbemcli class invokemethod --help` for details.
* **references** to get the class level reference classes or classnames for a
  class defined as an input argument in the default namespace or the namespace
  defined with this subcommand display in the defined format. This subcommand
  can display the class in several formats including MOF, XML, and REPR.. This
  returns the class level references but not the instance references. The
  :ref:`Instance subcommand group` includes a corresponding instance references
  operation::


    $pywbemcli --mock-server mockassoc class references TST_Person --name-only
    //FakedUrl/root/cimv2:TST_Lineage
    //FakedUrl/root/cimv2:TST_MemberOfFamilyCollection

  See :ref:`pywbemcli class associators --help` for details.
* **tree** to display the class hierarchy as a tree.  This subcommand
  outputs an ascii tree defining the hiearchy of the class name input parameter
  as a tree::

      $ pywbemcli class tree CIM_Foo

        CIM_Foo
         +-- CIM_Foo_sub
         |   +-- CIM_Foo_sub_sub
         +-- CIM_Foo_sub2

  It can show either the subclasses or the superclasses of the defined class
  (``--superclasses`` option).

  This subcommand ignores the ``--output-format``\``-o' general option and
  always outputs the ASCII tree format.

  See :ref:`pywbemcli class tree --help` for details.


.. _`Instance subcommand group`:

Instance command group
----------------------

The **instance** group defines subcommands that act on CIM instances including:

* **associators** to get the associator instances for the instance name defined
  as input argument in the default namespace or the namespace defined with this
  subcommand display in the defined format. The inThis subcommand can display the
  class in several formats including MOF, XML, and REPR.::

    $ pywbemcli --name mockassoc instance references TST_Person --name-only --interactive
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
* **count** count the number of instances in a namespace. For example::

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

  See :ref:`pywbemcli instance count --help` for details.
* **create** create a CIM instance in a namespace in the WBEM server.
  The options of the pywbemcli ``instance create`` subcommand allow the
  user to create an instance from properties where the properties are
  defined as name/value pairs.  Since the WBEM server (and pywbem) requires
  that each property be typed, pywbemtools uses the CIMClass from the WBEM
  server to define the required type

  For singular properties this is simply:

    -p <property-name>=<property-value"

    where quotes are only required if the value includes whitespace

  For array properties the values are defined separated by commas::

    -p <property-name>=<value>(,<value>)

  An example would be::

    $pywbemcli instance create TST_Blah InstancId="blah1", intprop=3, intarr=3,6,9

  See :ref:`pywbemcli instance delete --help` for details.
* **delete** delete an instance in a namespace.  The instance to be deleted is
    the :term:`INSTANCENAME` argument. The form is determined by the
    ``--interactive`` options and must be either:

    * a string representation of a CIMInstanceName as defined by a :term:`WBEM-URI`
    * A classname in which case pywbemcli will get the instance names from the
      WBEM server and present a selection list for the user to select an
      instance name :ref:`Displaying CIM instances or CIM instance names`

  The following example deletes the instance defined by the explicit instance
  name (Note the extra backslash required to escape the double quote on the
  terminal)::

    $ pywbemcli --name mockassoc instance delete root/cimv2:TST_Person.name=\"Saara\"
    $

  See :ref:`pywbemcli instance delete --help` for details.
* **enumerate** to enumerate instances or their paths in the default in the
  defined format. This subcommand can display the class in several formats
  including MOF, XML, and REPR. namespace or the namespace defined with this
  subcommand::

    $ pywbemcli --name mockassocinstance enumerate TST_FamilyCollection
    instance of TST_FamilyCollection {
       name = "family1";
    };

    instance of TST_FamilyCollection {
       name = "Family2";
    };

  See :ref:`pywbemcli instance enumerate --help` for details.
* **get** to get a single CIM instance from the default namespace or the
    namespace defined with the subcommand and display it in the defined format.
    The instance to be deleted is the ``INSTANCENAME`` argument. The form is
    determined by the ``--interactive`` options and must be either:

    * a string representation of a CIMInstanceName as defined by a WBEM-URI
    * A classname in which case pywbemcli will get the instance names from the
      WBEM server and present a selection list for the user to select an
      instance name :ref:`Displaying CIM instances or CIM instance names`::

        $ pywbemcli --name mockassocinstance instance get root/cimv2:TST_Person.name=\"Saara\"
        instance of TST_Person {
           name = "Saara";
        };

  See :ref:`pywbemcli instance get --help` for details.
* **invokemethod** to invoke a method defined for the class argument.
  See :ref:`pywbemcli instance invokemethod --help` for details.
* **modify** modify an instance in a namespace. The user provides the definition
  of an instance in the same form as the ``add`` subcommand but the instance
  must already exist in the WBEM server and the instance created from the
  command line must include all of the key properties so that it can be
  identified in the server.

  See :ref:`pywbemcli instance delete --help` for details.
* **references** to get the reference instances or paths for a
  instance defined as an input argument in the default namespace or the
  namespace defined with this subcommand display in the defined format. This
  subcommand can display the class in several formats including MOF, XML, and
  REPR.::

        $ pywbemcli --name mockassocinstance instance references root/cimv2:TST_Person.name=\"Saara\"
        instance of TST_Lineage {
           InstanceID = "SaaraSofi";
           parent = "/root/cimv2:TST_Person.name=\"Saara\"";
           child = "/root/cimv2:TST_Person.name=\"Sofi\"";
        };

  See :ref:`pywbemcli instance references --help` for details.
* **query** to execute an execquery with query string defined as an argument.
  See :ref:`pywbemcli instance query --help` for details.

.. _`qualifier command group`:

Qualifier command group
--------------------------

The **qualifier** command group defines subcommands that act on
CIMQualifierDeclarations including:

* **get** to get a single qualifier declaration from the default_namespace or
  the namespace defined with this command in the WBEM server and
  display in the defined output format. The output formats can be either one
  of the MOF formats or one of the table formats::

    $ pywbemcli --name mockassocinstance qualifier get Key
    Qualifier Key : boolean = false,
        Scope(property, reference),
        Flavor(DisableOverride, ToSubclass);

  See :ref:`pywbemcli qualifier get --help` for details.

* **enumerate** to enumerate all  qualifier declarations within the
  default namespace or the namespace defined with this subcommand. The output
  formats can be either one of the MOF formats or one of the table formats::

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

.. _`Server command group`:

Server command group
--------------------

The **server** command group defines subcommands that interact with a WBEM server
to access information about the WBEM server itself. These subcommands use the
pywbem ``WBEMServer`` class. These subcommands are generally not namespace
specific but access information about the server, namespaces, etc.
The commands are:

* **brand** to get general information on the server.  Brand information is an
  attempt by pywbem and pywbemtools to determine the product that represents
  the WBEM server infrastructure.  Since that was not clearly defined in the DMTF
  specifications, this   command may return strange results but it returns
  legitimate results for most servers::

    $ pywbemcli --name op server brand
    Server Brand:
    +---------------------+
    | WBEM Server Brand   |
    |---------------------|
    | OpenPegasus         |
    +---------------------+

  See :ref:`pywbemcli server brand --help` for details.
* **connection** to display information on the connection defined for this
  server.  This is same information as was defined when the connection was
  saved with ``connection save``:

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
  WBEM Server::

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
* **interop** to get a the name of the interop namespace target WBEM server::

    $ pywbemcli --name op server interop
    Server Interop Namespace:
    +------------------+
    | Namespace Name   |
    |------------------|
    | root/PG_InterOp  |
    +------------------+

  See :ref:`pywbemcli server interop --help` for details.
* **namespaces** to get a list of the namespaces defined in the target server::

    $ pywbemcli --name op-o plain  --name op server namespaces
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
* **profiles** to get overall information on the WBEM profiles defined in the
  target wbem server. WBEM profiles are the mechanism WBEM uses to provide
  the user the means to connection defined management functionality with
  the implementation of that functionality in a WBEM server (see :term:`DSP1001`
  and :term:`DSP1033`). The following example shows the CIM profiles in
  an example WBEM server::

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
* **centralinsts** to get the instance names of the central/scoping instances of
  one or more profiles in the target WBEM server::

    $ pywbemcli> server centralinsts --org DMTF --profile "Computer System"
    Advertised Central Instances:
    +---------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Profile                         | Central Instances                                                                                                                                                                                                                       |
    |---------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | DMTF:Computer System:1.0.0      | //leonard/test/TestProvider:Test_StorageSystem.Name="StorageSystemInstance1",CreationClassName="Test_StorageSystem"://leonard/test/TestProvider:Test_StorageSystem.Name="StorageSystemInstance2",CreationClassName="Test_StorageSystem" |
    +---------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  See :ref:`pywbemcli server centralinsts --help` for details.
* **test_pull** test for the existence of the pull operations in the target
  WBEM server. NOTE: This subcommand not implemented.

  See :ref:`pywbemcli server test_pull --help` for details.

.. _`Connection command group`:

Connection command group
---------------------------

The **connection** command group defines subcommands that provide for a
persistent file of connection definitons and allow selecting entries in this
file as well as adding entries to the file, deleting entries from the file and
viewing servers defined in the the file. This allows multiple connections to be
defined and then used by name rather than through the detailed information
about the connection.

Connections in the :term:`connection` file can be created by:

* Using the add subcommand. This allows defining the parameters of a connection
  as a subcommand

* Using the save subcommand with the current connection. This options uses the
  parameters from the pywbemcli for the connection to define and save a
  connection.

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
* **noverify** the boolean value of the certificate noverify options.  The
  default is False.
* **certfile** optional server certificate filename.
* **keyfile** optional client private keyfile filename.
* **use_pull_ops** optional parameter that defines whether pull operations are
  the default is to use pull operations if they exist in the server.
* **pull_max_cnt** optional count of object per pull operation.
* **timeout** optional timeout value.
* **timestats** boolean that determines if time stats are captured.
* **log** optional log configuration.
* **verbose** optional boolean that enables the verbose mode.
* **output-format** optional output format.
* **mock_server** optional definition of the files that define a mock server
  environment using the pywbem mock module.

The :term:`connections file` is named ``pywbemcliservers.json`` in the directory
in which pywbemcli is executed. The data is stored in JSON format within this
file.  Multiple connection files may be maintained in separate directories.

The subcommands include:

* **add** creates a new connection using subcommand arguments and set the new
  connection as the current connection. This subcommand does not save the
  new connection to the :term:`connections file` (see ``connection save``)
  The following
  example shows creating a new connection from within the interactive mode of
  pywbemcli. The parameters for the connection are defined through the input
  options for the subcommand. These use the same option names as
  the corresponding general options to define the WBEM server::

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
  will be used for any commands. This can be changed using ``connection select``

  See :ref:`pywbemcli connection add --help` for details.
* **delete** delete a specific connection by name or by selection. The following
  example deletes the connection defined in the add subcommand above::

    $ pywbemcli connection delete me

  To delete by selection:

    $ pywbemcli connection delete
    Select a connection or Ctrl_C to abort.
    0: mock1
    1: mockassoc
    2: op
    Input integer between 0 and 2 or Ctrl-C to exit selection: 1  << users enters

    $


  See :ref:`pywbemcli connection delete --help` for details.
* **export** export the current connection information to environment variables.
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
  example shows changing connection from within the interactive mode of pywemcli::

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
  above for an example of this subcommand
  See :ref:`pywbemcli connection show --help` for details.
* **test** execute a single predefined operation on the current connection
  to determine if it is a WBEM server. It executes a single EnumerateClasses
  WBEM operation in the default namespace.

  See :ref:`pywbemcli connection test --help` for details.

  $ pywbemcli connection add --name me -s http://localhost --user me --password mypw --no-verify connection save

.. _`Repl command`:

Repl command
------------

This command sets pywbemcli into the :ref:`interactive mode`.  Pywbemcli can be started in
the :ref:`interactive mode` either by entering::

   $ pywbemcli repl

or by executing the script without any command or command group::

   $ pywbemcli


.. _`Help command`:

Help command
------------

The help command provides information on special commands and controls that

can be executed in the :ref:`interactive mode`. This is different than the ``--help`` option
that provides information on command groups, and subcommands.


