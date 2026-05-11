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

This section describes the command line interface of the pywbemlistener
terminal command.

The pywbemlistener command is invoked from a command line terminal with a command
and arguments/options as shown here:

.. code-block:: text

    $ pywbemlistener [GENERAL-OPTIONS] COMMAND [COMMAND-OPTIONS] [ARGUMENTS]
    or
    $ pywbemlistener [GENERAL-OPTIONS] COMMAND [ARGUMENTS] [COMMAND-OPTIONS]


Where the components are:

.. index:: pair: General Options; command components

* **GENERAL-OPTIONS** - General options apply to all pywbemlistener commands.
  They start with ``-`` or ``--``. See :ref:`Pywbemlistener general options`

* **COMMAND** - A name of a command to be executed. See :ref:`Pywbemlistener commands`

* **ARGUMENTS** - Arguments may be defined for specific commands. Arguments
  do not have preceeding dashes. Arguments name the target listener
  for commands that execute against a single listener (ex. ``start lis1``)

* **COMMAND-OPTIONS** - Options that apply only to a particular
  COMMAND. Options are prefixed with the characters ``-`` for the short form or
  ``--`` for the long form (ex. ``-n`` or ``--namespace``).

.. index::
   pair: tab-completion; auto-suggestion
   single: auto-suggestion

Pywbemistener supports  :term:`tab-completion`. Tab-completion is available
with some command shells and only when activated for the shell type after
pywbemlistener installation. It is available for bash, zsh, and fish shells.

Tab-completion is available in pywbemcli for:
    * All command names
    * All general and command specific option names
    * command arguments (i.e. listener names)

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
