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

.. _`Pywbemcli Command line interface`:

Pywbemcli command line interface
================================

This section describes the command line interface of the pywbemcli command
within the pywbemtools package.

Pywbemcli provides a command line interface(CLI) interaction with WBEM servers.

The command line can contain the following components:

* **general-options** - Options that apply to all commands.
  See :ref:`Using the pywbemcli command line general options` for infomation on the
  pywbemcli general options
* **command group** - A name of a group of commands.
  See :ref:`Pywbemcli command groups and commands`
* **command** - A command name normally within a command group.
  There are however some special commands that exist outside of any
  command group; they are not in any command group.
* **args** - Arguments and options that are defined for a particular
  command. Options are proceeded by the characters '-' for the
  short form or '--' for the long form. (ex. ``-n`` or ``--namespace``).
  Arguments do not have a ``-`` or ``--`` prefix and follow the
  command name. (ex. ``pywbemcli class get CIM_Foo``. CIM_Foo is
  an argument.). Options include the ``-`` or ``--`` prefix.

The syntax is:

.. code-block:: text

    pywbemcli <general-options> <command group> <command> <args>

**NOTE:** pywbemcli has two special commands that are not a part of any
command group ``repl`` and ``help``.

A command group is the name of an object, (ex. ``class`` refers to operation on
CIM classes). The commands are generally actions on the objects defined by the
command group name (``get``, ``list``, etc.). Thus ``class`` is a command group
name used to access CIM classes and ``get`` is a command so:

.. code-block:: text

    $ pywbemcli --output-format mof class get CIM_ManagedElement --namespace interop

Defines a command sequence to get the class ``CIM_ManagedElement`` from the current
target server in the namespace ``interop`` and display it in the
``MOF`` output-format.

.. _`Modes of operation`:

Modes of operation
------------------

Pywbemcli supports two modes of operation:

* `Interactive mode`_: Invoking an interactive pywbemcli shell for typing
  pywbemcli commands.
* `Command mode`_: Executing standalone non-interactive commands.

.. _`Interactive mode`:

Interactive mode
----------------

In interactive mode also known as :term:`REPL` mode, an interactive shell
environment is within pywbemcli that allows typing pywbemcli commands, internal
commands (for operating the pywbemcli shell), and external commands (that are
executed in the standard shell for the user).

This pywbemcli shell is started when the ``pywbemcli`` command is invoked
without specifying any command group or command:

.. code-block:: text

    $ pywbemcli [GENERAL-OPTIONS]
    pywbemcli> _

Alternatively, the pywbemcli shell can also be started by specifying the ``repl``
command:

.. code-block:: text

    $ pywbemcli [GENERAL-OPTIONS] repl
    pywbemcli> _

The pywbemcli shell uses the prompt "``pywbemcli>``\  ". The cursor is shown in
the examples above as an underscore (\ ``_``\ ).

General options are specified immediately after ``pywbemcli``; they serve
as the parameters for the connection to a WBEM server and values for the
pywbemcli commands and arguments that can be typed in the pywbemcli shell.

The pywbemcli commands that can be typed in the pywbemcli shell are the
command or command group that would follow the ``pywbemcli`` command and
general options when used in `command mode`_. The following example
starts a pywbemcli shell in interactive mode and executes several commands
(ex. ``class enumerate -o``).

.. code-block:: text

    $ pywbemcli -s http://localhost -d root/cimv2 -u username

    pywbemcli> class enumerate -o
    . . . <Enumeration of the names of classes in the defined namespace>

    pywbemcli> class get CIM_System
    . . . <MOF output of the class CIM_System from the WBEM server>

    pywbemcli> :q

The pywbemcli shell command ``class get CIM_System`` in the example
above has the same effect as the standalone command:

.. code-block:: text

    $ pywbemcli -s http://localhost -u username class get CIM_System
    . . . <MOF formatted display of the CIM_System class>

The internal commands ``:?``, ``:h``, or ``:help`` display general help
information for external and internal commands:

.. code-block:: text

    > :help
    REPL help:

      External Commands:
        prefix external commands with "!"

      Internal Commands:
        prefix internal commands with ":"
        :?, :h, :help     displays general help information
        :exit, :q, :quit  exits the REPL

In addition to using one of the internal shell commands shown in the help text
above, you can also exit the pywbemcli shell by typing `Ctrl-D`. Note: the
pywbemcli shell exit command may vary by operating system.

Typing ``--help`` or ``-h`` in the pywbemcli shell displays general help
information for the pywbemcli commands which includes general options and a
list of the supported commands.

.. code-block:: text

    $ pywbemcli
    pywbemcli> --help

    Pywbemcli is a command line WBEM client that uses the DMTF CIM-XML
    protocol to communicate with WBEM servers. Pywbemcli can:

    . . .

    Commands:
      class      Command group to manage CIM Classes.
      instance   Command group to manage CIM instances.
      qualifier  Command group to manage CIM...
      repl       Start an interactive shell.
      server     Command group for server operations

The usage line in this help text shows the standalone command use. Within the
pywbemcli shell (interactive mode), the ``pywbemcli`` word is omitted and the
command and options is typed in.

Typing ``command group --help``,  or ``command group -h``, or ``command group
command --help`` in the pywbemcli shell displays help information for the
specified pywbemcli command group, for example:

.. code-block:: text

    pywbemcli> class --help
    Usage: pywbemcli  class [COMMAND-OPTIONS] COMMAND [ARGS]...

    . . .
      references    Get the reference classes for the CLASSNAME.

The pywbemcli shell command in the interactive mode supports popup help text
while typing, where the valid choices are shown based upon what was typed so
far, and where an item from the popup list can be picked with <TAB> or with the
cursor keys. It can be used to select from the list of general options. In the
following examples, an underscore ``_`` is shown as the cursor:

.. code-block:: text

    pywbemcli> --_
     --server             Hostname or IP address with scheme of the WBEMServer ...
     --name               Name for the connection(optional, see --server).  If ...
     --default_namespace  Default Namespace to use in the target WBEMServer if ...

    pywbemcli> cl_
      class      Command group to manage CIM Classes.

The pywbemcli shell supports history across multiple invocations of the shell
using <up-arrow, down-arrow>.

.. _`Command mode`:

Command mode
------------

In command mode, the pywbemcli command performs its task and terminates
like any other standalone non-interactive command.

This mode is used when the pywbemcli command is invoked with a command or
command group name and arguments/options:

.. code-block:: text

    $ pywbemcli [GENERAL-OPTIONS] command|command group command] [ARGS...]

The following example defines a WBEM server and then executes ``class enumerate``:

.. code-block:: text

    $ pywbemcli --server http://localhost --default-namespace root/cimv2 --user username class enumerate
    Enter password: <password>
    . . .
    <Returns MOF for classes found with the enumerate>

In command mode, tab completion is also supported for some command shells, but
must be enabled specifically for each shell.

For example, with a bash shell, enter the following before using pywbemcli to
enable completion:

.. code-block:: text

    $ eval "$(_PYWBEMCLI_COMPLETE=source pywbemcli)"

Bash tab completion for ``pywbemcli`` is used like any other bash tab
completion:

.. code-block:: text

    $ pywbemcli --<TAB><TAB>
    ... <shows the general options to select from>

    $ pywbemcli <TAB><TAB>
    ... <shows the commands to select from>

    $ pywbemcli class <TAB><TAB>
    ... <shows the class commands to select from>

The documentation for the python CLI tool click contains information on other
shell tab completion solutions.
