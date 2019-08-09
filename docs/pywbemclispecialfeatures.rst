g.. Copyright  2017 IBM Corp. and Inova Development Inc.
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

Pywbemcli includes several features in the syntax that are worth presenting
in detail to help the user understand the background purpose and syntactic
implementation of the features. This includes:

* The ability to execute either the pull or traditional operations with the
  same command group.

* The ability to receive either CIM instances or CIM instance names with only
  a change of an option on the commands that request CIM instances. The option
  ``-o`` or ``--name-only`` defines whether only the instance name or the complete
  object will be displayed.

* The ability to interactively select the data for certain objects as opposed
  to having to enter the full name.


.. _`Using pywbem Pull Operations from pywbemcli`:

Using pywbem Pull Operations from pywbemcli
-------------------------------------------

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
request if the pull operations are to be set which tells the WBEM server to
limit the size of the response.  For example::

    pywbemcli --server http/localhost use-pull-ops=yes max_object_cnt=10

would force the use of the pull operations and return an error if the target
server did not implement them and would set the ``MaxObjCount`` parameter on the
api to 10, telling the server that a maximum of 10 object can be returned for
each of the requests in an enumeration sequence.

Since the default for use-pull-ops is ``either``, normally pywbem first tries
the pull operation and then if that fails, the traditional operation.  That
is probably the most logical setting for ``use-pull-ops`` unless you are
specifically testing the use of pull operations.

Note that there is a special request ``server test-pull`` that will test if
a server implements the pull operations and for which of the possible operations
pull is implemented.

The following table defines which pywbemcli commands are used for the
corresponding pywbem request operations.

=================================  ==============================================
WBEM CIM-XML Operation             pywbemtools command-group & subcommand
=================================  ==============================================
EnumerateInstances                 instance enumerate INSTANCENAME
EnumerateInstanceNames             instance enumerate INSTANCENAME --name_only
GetInstance                        instance get INSTANCENAME
ModifyInstance                     instance modify
CreateInstance                     instance create
DeleteInstance                     instance delete INSTANCENAME
Associators                        instance associators INSTANCENAME
Associators                        class associators CLASSNAME
AssociatorNames                    instance associators INSTANCENAME --name_only
AssociatorNames                    class associators CLASSNAME --name_only
References                         instance references INSTANCENAME
References                         class references CLASSNAME
ReferenceNames                     instance references INSTANCENAME --name_only
ReferenceNames                     class references CLASSNAME --name_only
InvokeMethod                       instance invokemethod INSTANCENAME --name_only
ReferenceNames                     class invokemethod CLASSNAME --name_only
ExecQuery                          instance query
IterEnumerateInstances             instance enumerate INSTANCENAME
IterEnumerateInstancePaths         instance enumerate INSTANCENAME --name_only
IterAssociatorInstances            instance associators INSTANCENAME
IterAssociatorInstancePaths        instance associators INSTANCENAME --name_only
IterReferenceInstances             instance references INSTANCENAME
IterReferenceInstancePaths         instance references INSTANCENAME --name_only
IterQueryInstances                 instance query
When --use-pull-ops either or yes  TODO
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
EnumerateClasses                   class enumerate CLASSNAME
EnumerateClassNames                class enumerate --name-only
GetClass                           class get CLASSNAME
ModifyClass                        Not implemented
CreateClass                        Not implemented
DeleteClass                        class delete CLASSNAME
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
----------------------------------------------

The pywbem API includes different WBEM operations (ex. ``EnumerateInstances`` and
``EnumerateInstanceNames``) to request CIM objects or just their names. To
simplify the overall command line syntax pywbemcli combines these into a single
subcommand (i.e. enumerate, references, associators) and includes an option
(``-o,`` or ``--names-only``) that determines whether the instance names or
instances are retrieved from the WBEM Server.

Thus, for example an `instance enumerate` with and without the ``-o`` option::


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
------------------------------------

Arguments like the INSTANCENAME on some of the instance group subcommands (
get, references, associators, etc) can be very difficult to correctly enter
since it can involve multiple keybindings, use of quotation marks, etc.  To
simplify this pywbemcli includes a option (``-i`` or ``--interactive``) on
these commands that allows the user to specify only the class name, retrieves
all the instance names from the server and presents the user with a select list
from which an instance name can be chosen. The following is an example::

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







