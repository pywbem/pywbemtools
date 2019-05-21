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

.. _`pywbemcli subcommand options`:

pywbemcli subcommand options
============================

There are a number of ``pywbemcli``  groups and subcommands defined.  Each subcommand
may have arguments  and options (defined with - or -- as part of the
name). While many arguments and options are specific to each subcommand, there
are several that are more general and apply to multiple subcommands including
the following:

* --interactive - On subcommands where this option is available it changes
  the behavior of the subcommand. Instead of just outputting a result and
  exiting the subcommand, ``pywbemcli`` presents a list for the user to use
  to select one of the options.  This is used, for example, with the
  ``instances get`` to get a list of instances to display rather than having
  to type in the complete instance name.

* --namespace - On subcommands this overrides the current default namespace
  defined by the general option --namespace only for this subcommand. The
  current default namespace is retained.

* --name_only - On subcommands where this option exist, it changes the
  request to the server and the display from acquiring the full object to
  just acquiring the object names.  Thus, for example::

  $ pywbemcli class enumerate       # displays the mof of all classes

  $ pywbemcli class enumerate -o     # displays only the names of the classes

.. _`Pywbemcli command groups, comands and subcommands`:

Pywbemcli command groups, commands and subcommands
==================================================

The general command structure of pywbemcli is::

    pywbemcli <general-options> <cmd-group>|<command> <subcommand> <ARGS>

Each command group is a noun, referencing an entity (ex. class
refers to operation on CIM classes). The subcommands are generally actions on
those entities defined by the group name. Thus ``class`` is a group and
``get`` is a subcommand so:

    $ pywbemcli class get CIM_ManagedElement

Defines a command to get the class `CIM_ManagedElement` from the current
target server and display it in the defined output-format.


The pywbemcli command groups are as follows: Note that this is the current
list of command groups and subcommands and this will grow in the future.

.. _`Class command group`:

Class command group
----------------------

The **class** group defines subcommands that act on CIM classes including:

* **get** to get a single class and display in the defined format.
  See ref:`pywbemcli class get --help` for details.
* **enumerate** to enumerate classes or their classnames in a
  namespace or the namespace defined with this subcommand.
  See ref:`pywbemcli class enumerate --help` for details.
* **associators** to get the class level associators for a class defined
  as an input argument.  This returns the class level associators
  but not the instance  associators. The ``instance`` command group
  includes an associators operation..
  See ref:`pywbemcli class associators --help` for details.

* **references** to get the class level reference classes or classnames for a
  class defined as an input argument. This returns the class level references
  but not the instance references. The ``instance`` command group
  includes an references operation..
  See ref:`pywbemcli class associators --help` for details.
* **delete** Delete the class defined by the CLASSNAME argument. Note that
  many WBEM servers may not allow this operation or may severely limit the
  conditions under which a class can be deleted from the server.
  See ref:`pywbemcli class delete --help` for details.
* **find** to find classes in the target wbem server.  In this case the
  input argument is a regular expression which is used to search all namespaces for
  matching class names.
  See ref:`pywbemcli class find --help` for details.
* **tree** to display the class hierarchy as a tree.
  See ref:`pywbemcli class hiearchy --help` for details.
* **invokemethod** to invoke a method defined for the class argument. This
  subcommand executed the invokemethod with the classname, not an instance
  name.   See ref:`pywbemcli class invokemethod --help` for details.

.. _`Instance subcommand group`:

Instance command group
-------------------------

The **instance** group defines subcommands that act on CIMInstances including:

* **get** to get a single instance and display in the defined format.
  See ref:`pywbemcli instance get --help` for details.
* **enumerate** to enumerate instances or their paths in a
  namespace or the namespace defined with this subcommand.
  See ref:`pywbemcli instance enumerate --help` for details.
* **associators** to get the associator instances for an instance defined
  as an input argument.
  See ref:`pywbemcli instance associators --help` for details.
* **references** to get the reference instances or paths for a
  instance defined as an input argument.
  See ref:`pywbemcli instance references --help` for details.
* **find** to find classes in the target wbem server.  In this case the
  input argument is a regex which is used to search all namespaces for
  matching class names.
  See ref:`pywbemcli instance find --help` for details.
* **query** to execute an execquery with query string defined as an argument.
  See ref:`pywbemcli instance query --help` for details.
* **invokemethod** to invoke a method defined for the class argument.
  See ref:`pywbemcli instance invokemethod --help` for details.
* **count** count the number of instances in a namespace.
  See ref:`pywbemcli instance count --help` for details.
* **delete** delete an instance in a namespace.
  See ref:`pywbemcli instance delete --help` for details.
* **create** create an instance in a namespace.
  See ref:`pywbemcli instance delete --help` for details.
* **modify** modify an instance in a namespace.
  See ref:`pywbemcli instance delete --help` for details.

.. _`qualifier command group`:

Qualifier command group
--------------------------

The **qualifier** command group defines subcommands that act on
CIMQualifierDeclarations including:

* **get** to get a single qualifier declaration and display in the defined format.
  See ref:`pywbemcli qualifier get --help` for details.

* **enumerate** to enumerate qualifierDeclarations within the
  current namespace or the namespace defined with this subcommand.
  See ref:`pywbemcli qualifier enumerate --help` for details.


.. _`Server command group`:

Server command group
--------------------

The **server** command group defines subcommands that interact with a WBEM server
to access information about the WBEM server itself. These commands use the
pywbem ``WBEMServer`` class. The commands are:

* **brand** to get general information on the server.
  See ref:`pywbemcli server brand --help` for details.
* **connection** to display information on the connection defined for this
  server. See ref:`pywbemcli server connection --help` for details.
* **info** to get general information on the server.
  See ref:`pywbemcli server info --help` for details.
* **interop** to get a the name of the interop namespace target WBEM server.
  See ref:`pywbemcli server interop --help` for details.
* **namespaces** to get a list of the namespaces defined in the target server.
  See ref:`pywbemcli server namespaces --help` for details.
* **profiles** to get overall information on the profiles defined in the
  target wbem server.   See ref:`pywbemcli server profiles --help` for details.
* **centralinsts** to get the instance names of the central/scoping instances of
  one or more profiles in the target WBEM server.
  See ref:`pywbemcli server centralinsts --help` for details.
* **test_pull** test for the existence of the pull operations in the target
  WBEM server.
  See ref:`pywbemcli server test_pull --help` for details.

.. _`Connection command group`:

Connection subcommand group
---------------------------

The **connection** command group defines subcommands that provide for a
persistent file of connection definitons and allow selecting entries in this
file as well as adding entries to the file, deleting from the file an viewing
the file. This allows multiple connections to be defined and then used by name
rather than through the detailed information about the connection.

Connections in the connection file can be created by:

* Using the add subcommand. This allows defining the parameters of a connection
  as a subcommand

* Using the save subcommand with the current connection. This options uses the
  parameters from the pywbemcli for the connection to define and save a
  connection.

The connection information for each connection is based on the information
used to create a connection and is largely the same information as is in the
options for pywbemcli. The data includes:

* **name** name of the connection (required).
* **server_url** the url for the defined connection (required).
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

The connections file is named ``pywbemcliservers.json`` in the directory
in which pywbemcli is executed. The data is stored in JSON format within this
file.

The subcommands include:

* **delete** delete a specific connection by name or by selection.
  See ref:`pywbemcli connection delete --help` for details.
* **export** export the current connection information to environment variables.
  See ref:`pywbemcli connection export --help` for details.
* **list** list the connections in the connection file as a table.
  See ref:`pywbemcli connection list --help` for details.
* **add** create a new connection using the parameters.
  See ref:`pywbemcli connection add --help` for details.
* **save** create a new connection by saving the current connection information
  to the connection file.  If the current connection does not have a name
  a console request asks for a name for the connection.
  See ref:`pywbemcli connection save --help` for details.
* **select** select a connection from the connection table.  A connection
  may be selected either by using the name argument or if no argument is
  provided by selecting from a list presented on the console.
  See ref:`pywbemcli connection select --help` for details.
* **show** show information in the current connection.
  See ref:`pywbemcli connection show --help` for details.
* **test** execute a single predefined operation on the current connection
  to determine if it is a WBEM server. It executes a single EnumerateClasses
  with WBEM operation in the default namespace.
  See ref:`pywbemcli connection test --help` for details.

TODO: Add examples of creating and deleting connections.



.. _`Repl command`:

Repl command
------------

This command sets pywbemcli into the repl mode.


.. _`Help command`:

Help command
------------

The help command provides information on special commands and controls that
can be executed in the repl mode. This is different than the --help option
that provides information on command groups and commands.


