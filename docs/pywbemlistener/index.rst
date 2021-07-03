.. Copyright 2021 Inova Development Inc.
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

.. _`Pywbemlistener command`:

Pywbemlistener command
======================

The pywbemlistener command can run and manage WBEM listeners.

Each listener is a process that executes the ``pywbemlistener run``
command to receive WBEM indications sent from a WBEM server.

A listener process can be started with the ``pywbemlistener start``
command and stopped with the ``pywbemlistener stop`` command.

There is no central registration of the currently running listeners.
Instead, the currently running processes executing the
``pywbemlistener run`` command are by definition the currently running
listeners. Because of this, there is no notion of a stopped listener nor
does a listener have an operational status.

.. The maxdepth attribute overrides the maxdepth attribute of the
.. mastertoc if used.
.. The numbered attribute intentionally is not set, because the numbering
.. on sub-TOCs is created automatically when set on the top-level TOC.

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents in this Section:

   commands.rst
   generaloptions.rst
   cmdshelp.rst
