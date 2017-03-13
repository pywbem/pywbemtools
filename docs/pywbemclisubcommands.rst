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

.. _`pywbemcli subcommands`:

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

  $ pywbemcli class enumerte -o     # displays only the names of the classes
  

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

* The **class** group defines commands that act on CIMClasses including:

  * **get** to get a single class and display in the defined format
  * **enumerate** to enumerate classes or their classnames within the
      current namespace or the namespace defined with this subcommand
  * **associators** to get the class level associators for a class defined
      as an input argument
  * **references** to get the class level reference classes or classnames for a
      class defined as an input argument
  * **find** to find classes in the target wbem server.  In this case the
      input argument is a regex which is used to search all namespaces for
      matching class names
  * **hiearchy** to display the class hierarchy as a tree
  * **invokemethod** to invoke a method defined for the class argument.

* The **instance** group defines commands that act on CIMInstances including:

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

* The **qualifier** group defines commands that act on CIMQualifierDeclarations 
 including:
 
  * **get** to get a single qualifier declaration and display in the defined format.
  * **enumerate** to enumerate qualifierDeclarations within the
      current namespace or the namespace defined with this subcommand.

* The **server** group defines commands that act on a WBEM Server including:

  * **brand** to get general information on the server.
  * **connection** to display information on the connection defined for this
      server.
  * **info** to get general information on the server.
  * **namespaces** to get a list of the namespaces defined in the target server.
  * **profiles** to get overall information on the profiles defined in the
      target wbem server.
