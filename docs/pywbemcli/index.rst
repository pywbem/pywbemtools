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

.. _`Pywbemcli command`:

Pywbemcli command
=================

Pywbemcli provides access to WBEM servers from the command line.
It provides functionality to:

* Explore the CIM data of WBEM servers. It can manage/inspect the CIM model
  components including CIM classes, CIM instances, and CIM qualifiers and
  execute CIM methods and queries on the WBEM server.

* Execute specific CIM-XML operations on the WBEM server as defined in `DMTF`_
  standard :term:`DSP0200` (CIM Operations over HTTP).

* Inspect and manage WBEM server functionality including:

  * :term:`CIM namespaces <CIM namespace>`
  * Advertised :term:`WBEM management profiles <WBEM management profile>`
  * WBEM server brand and version information

* Capture detailed information on CIM-XML interactions with the WBEM server
  including time statistics and details of data flow.

* Maintain a file with persisted WBEM connection definitions so that pywbemcli
  can access multiple WBEM servers by name.

* Provide both a command line mode and an interactive mode where multiple
  pywbemcli commands can be executed within the context of a WBEM server.

* Use an integrated mock WBEM server to try out commands. The mock server
  can be loaded with CIM objects defined in MOF files or via Python scripts.

.. _DMTF: https://www.dmtf.org/

.. The maxdepth attribute overrides the maxdepth attribute of the
.. mastertoc if used.
.. The numbered attribute intentionally is not set, because the numbering
.. on sub-TOCs is created automatically when set on the top-level TOC.

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents in this Section:

   cmdlineinterface.rst
   generaloptions.rst
   features.rst
   commands.rst
   cmdshelp.rst
   mock_support.rst
