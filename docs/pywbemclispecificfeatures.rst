.. Copyright  2017 IBM Corp. and Inova Development Inc.
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


.. _`Pywbemcli Specific Features`:

Pywbemcli Specific Features
===========================

TODO need more on overview


Using pywbem Pull Operations from pywbemcli
-------------------------------------------

pywbem includes multiple ways to execute the enumerate instance type operations
(associators, references, enumerateinstances, execquery):

* The traditional operations (ex. EnumerateInstances)
* The pull operations (ex. the pull sequence OpenEnumerateInstances, etc.)
* An overlay of the above two operations called the Iter... operations. Each
  iter operation executes either the traditional or pull depending on
  input parameters.

see TODO for detailed information.

pywbemcli implements these method calls to pywbem using the iter operations
so that either pull operations or traditional operation can be used simply
by changing a pywbemcli input parameter (use-pull-ops).

Two options on the command line allow you to either force the use of pull
operations, of traditional operations, or to let pywbem try them both.

The input parameter `use-pull-ops` allows the choice of pull or traditional
operations with the default being to allow pywbem to decide.  The input
parameter `max_object_cnt` sets the `MaxObjectCount` variable if the pull
operations are to be set.  As an example:

pywbemcli -s http/localhost use-pull-ops=yes max_object_cnt=10

would force the use of the pull operations and return an error if the target
server did not implement them and would set the MaxObjCount parameter on the
api to 10, telling the server that a maximum of 10 object can be returned for
each of the requests in an enumeration sequence.

Since the default for use-pull-ops is `either`, normally pywbem first tries
the pull operation and then if that fails, the traditional operation.  That
is probably the most logical setting for `use-pull-ops` unless you are
specifically testing the use of pull operations.

Note that there is a special request `server test-pull` that will test if
a server implements the pull operations and for which of the possible operations
pull is implemented.
