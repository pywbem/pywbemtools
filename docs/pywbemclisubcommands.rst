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
  the behavior of the subcommand. Instead of just outputting a list and
  exiting the subcommand, ``pywbemcli`` presents a list for the user to use
  to select one of the options.  This is used, for example, with the
  ``instances get`` to get a list of instances to display.

* --namespace - On subcommands this overrides the current default namespace
  defined by the general option --namespace only for this subcommand. The
  current default namespace is retained.

* --name_only - On subcommands where this option exist, it changes the
  request to the server and the display from acquiring the full object to
  just acquiring the object names.  Thus, for example::

  $ pywbemcli class enumerate       # displays the mof of all classes

  $ pywbemcli class enumerate -o     # displays only the names of the classes

.. _`pywbemcli subcommands`:

pywbemcli subcommands
=====================

Generally the structure of pywbemcli is:

pywbemcli <general options> <cmd-group> <subcommand> <subcommand arguments> <subcommand options>

Generally each command group is a noun, referencing some entity (ex. class
referes to operation on CIMClasses). The subcommands are generally actions on
those entities defined by the group name. Thus ``class`` is a group and
``get`` is a subcommand so:

    $ pywbemcli class get CIM_ManagedElement

Defines a command to get the class CIM_ManagedElement from the current
target server and display it in the defined output-format.


**NOTE:** The following is the current list of subcommands.  This will change and
grow in the future so please use ``pywbemcli`` itself as the reference for
what exists in any current version of the tool.

The ``pywbemcli`` command includes a number of general subcommand groups as follows:

.. _`class subcommand group`:

class subcommand group
----------------------

The **class** group defines subcommands that act on CIMClasses including:

* **get** to get a single class and display in the defined format.
* **enumerate** to enumerate classes or their classnames within the
  current namespace or the namespace defined with this subcommand.
* **associators** to get the class level associators for a class defined
  as an input argument.
* **references** to get the class level reference classes or classnames for a
  class defined as an input argument.
* **find** to find classes in the target wbem server.  In this case the
  input argument is a regex which is used to search all namespaces for
  matching class names.
* **hiearchy** to display the class hierarchy as a tree.
* **invokemethod** to invoke a method defined for the class argument.

.. _`instance subcommand group`:

instance subcommand group
-------------------------

The **instance** group defines subcommands that act on CIMInstances including:

* **get** to get a single instance and display in the defined format.
* **enumerate** to enumerate instances or their paths within the
  current namespace or the namespace defined with this subcommand.
* **associators** to get the associator instances for an instance defined
  as an input argument.
* **references** to get the reference instances or paths for a
  instance defined as an input argument.
* **find** to find classes in the target wbem server.  In this case the
  input argument is a regex which is used to search all namespaces for
  matching class names.
* **query** to execute an execquery with query string defined as an argument.
* **invokemethod** to invoke a method defined for the class argument.

.. _`qualifier subcommand group`:

qualifier subcommand group
--------------------------

The **qualifier** group defines subcommands that act on CIMQualifierDeclarations
including:

* **get** to get a single qualifier declaration and display in the defined format.
* **enumerate** to enumerate qualifierDeclarations within the
  current namespace or the namespace defined with this subcommand.

.. _`server subcommand group`:

server subcommand group
-----------------------

The **server** group defines subcommands that act on a WBEM Server through
the pywbem WBEMServer class. This includes command to access general
information about the server including:

* **brand** to get general information on the server.
* **connection** to display information on the connection defined for this
  server.
* **info** to get general information on the server.
* **namespaces** to get a list of the namespaces defined in the target server.
* **profiles** to get overall information on the profiles defined in the
  target wbem server.

.. _`connection subcommand group`:

connection subcommand group
---------------------------

The **connection** group defines subcommands that provide for a persistent file
of connection definitons and allow selecting entries in this file as well as
adding entries to the file, deleting from the file an viewing the file. This
allows multiple connections to be defined and then used by name rather than
through the detailed information about the connection.

Connections in the connection file can be created by:

* Using the new subcommand. This allows defining the parameters of a connection
  as a subcommand
* Using the save subcommand with the current connection. This options uses the
  parameters from the pywbemcli for the connection to define and save a
  connection.

The connection information for each connection is based on the information
used to create a connection and is largely the same information as is in the
options for pywbemcli. For more detailed information on these The data includes:

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

The default connections file is named named ``pywbemcliservers.json`` and the
data is stored in JSON format within this file. It must be in the current
working directory where pywbemcli is called.

The subcommands include:

* **delete** delete a specific connection by name or by selection.
* **export** export the current connection information to environment variables.
* **list** list the connections in the connection file as a table.
* **new** create a new connection using the parameters.
* **save** create a new connection by saving the current connection information
  to the connection file.  If the current connection does not have a name
  a console request asks for a name for the connection.
* **select** select a connection from the connection table.  A connection
  may be selected either by using the name argument or if no argument is
  provided by selecting from a list presented on the console.
* **show** show information in the current connection.
* **test** execute a single predefined operation on the current connection
  to determine if it is a WBEM Server. It executes a single EnumerateClasses
  with WBEM operation in the default namespace.
