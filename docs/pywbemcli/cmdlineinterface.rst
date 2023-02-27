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

.. index::
    single: pywbemcli command line interface
    single: command line interface

.. _`Pywbemcli command line interface`:

Pywbemcli command line interface
================================

This section describes the command line interface of the pywbemcli command
within the pywbemtools package.

Pywbemcli provides a command line interface(CLI) interaction with WBEM servers.

The pywbemcli command is invoked with a command  and arguments/options:

.. code-block:: text

    $ pywbemcli [GENERAL-OPTIONS] COMMAND [COMMAND-OPTIONS] [ARGS]

Where the components are:

The pywbemcli command is invoked with a command and arguments/options:

.. code-block:: text

    $ pywbemcli [GENERAL-OPTIONS] COMMAND [COMMAND-OPTIONS] [ARGUMENTS]
    or
    $ pywbemcli [GENERAL-OPTIONS] COMMAND [ARGUMENTS] [COMMAND-OPTIONS]


Where the components are:

.. index:: pair: General Options; command components

* **GENERAL-OPTIONS** - General options; they apply to all commands.
  See :ref:`Using the pywbemcli command line general options` for information
  on the pywbemcli general options.

.. index:: pair: commands ; command components

* **COMMAND** - A name of a command which may consist of:
   * <group name> <command name> for commands that are defined within
     groups (ex. ``class find``).
   * <group name> (ex. ``class``) to show group help including list of  command
     within the group.
   * <command name> for those commands that are not part of a group. For
     example ``repl`` and ``help`` that are not in any command group.

.. index:: pair: command arguments; command components

* **ARGUMENTS** - Arguments may be defineda specific command. Arguments
  are not individually
  documented in the help and do not have preceeding dashes. In pywbemcli
  arguments are only used in commands. There are no general arguments.
  Specifically they are used to specify request object names (ex. class namme
  or instance name for specifice commands.

.. index:: pair: command interface; Command Options

* **COMMAND-OPTIONS** - Options that apply only to a particular
  COMMAND.

Options are prefixed with the characters ``-`` for the short form or ``--`` for
the long form (ex. ``-n`` or ``--namespace``). The other command line components
do not begin with ``-``.

.. index:: pair: command groups; command interface

Command groups are generally named after the objects the commands operate on
(ex. ``class``, ``instance``, ``qualifier``, ``server``, ``connection``,
``namespace``, etc.). Executing:

.. code-block:: text

   $ pywbemcli --help

   Commands:
     class       Command group for CIM classes.
     ...


returns the list of command groups under the title `Commands`.

Commands are named after actions on these objects
(ex. ``get``, ``create``, ``delete``). The list of commands for each group
is displayed with the command `pywbemcli <group name> --help`.

The list of commands for each group
is listed with the command `pywbemcli <group name> --help`.

For example, the command:

.. code-block:: text

    $ pywbemcli --output-format mof class get CIM_ManagedElement --namespace interop

gets class ``CIM_ManagedElement`` in namespace ``interop`` and displays it in
the MOF output format. The option ``--output-format`` is a general option
and ``--namespace`` is a command option.

.. index::
   pair: tab-completion; auto-suggestion
   single: auto-suggestion

Pywbemcli supports  :term:`tab-completion` and :term:`auto-suggestion`
depending on whether it is in command mode or interactive mode.

  * :ref:`interactive mode` - both tab-completion and auto-suggestion are always
    available.
  * :ref:`command mode` - tab-completion is available with some command shells
    and only when activated for the shell type.  Auto-suggestion is not
    available.

Tab-completion is available in pywbemcli for:
    * All comand group and command names
    * All option names
    * At least the following general options values:
        * --name
        * --mock-server - The completion uses the default connection file
          unless the --connection-file general option has already been defined
          for an alternate connection file on the command line.
        * --connection-file
        * --keyfile
        * --certfile
        * --use-pull
        * --output-format
    * At least the following command arguments
        * help <subject-argument>
    * At least the following command options
        * Subscription <command> --owned / -- permanent option

Tab-completion for option/argument values only works for pywbemcli running with
Python version greater than 3.5. If pywbemcli is running on Python 3.5 or 2.7,
option values has no support for tab-completion. Nothing happens if <TAB> is
hit while entering an option value. However, the tab-completion of other
command line syntax elements is supported.


.. code-block:: text

    $ pywbemcli --<TAB><TAB>
    ... <shows the general options to select from>

    $ pywbemcli <TAB><TAB>
    ... <shows the command groups to select from>

    $ pywbemcli clas<TAB>
    ... completes the command group class

    $ pywbemcli class <TAB><TAB>
    ... <shows the class commands to select from>

    $ pywbemcli -n moc <TAB><TAB>  (Only only with Python 3)
    ... returns connection names in the default connection file that start
    ... with moc

Tab-completion for ``pywbemcli`` is used like any other tab-completion by
hitting <TAB> or <TAB><TAB> where completion is possible. Generally <TAB>
returns a complete response completion if there is only one available while
<TAB><TAB> returns a list if there are multiple possible completions but the
exact behavior depends on the shell and any number of shell flags, extensions
that are particular to each shell.

.. index::
    pair: Modes of operation; Command mode
    pair: Modes of operation; Interactive mode
    pair: Command mode; Interactive mode

.. _`Modes of operation`:

Modes of operation
------------------

Pywbemcli supports two modes of operation:

* `Command mode`_: Executing standalone non-interactive commands.
* `Interactive mode`_: Invoking an interactive pywbemcli shell for typing
  pywbemcli commands.

.. index:: pair: Interactive mode; command modes
.. index:: pair: Interactive mode; modes of operation

.. _`Command mode`:

Command mode
------------

.. index:: single: Command mode

In command mode, the pywbemcli command performs its task defined on the command
line and terminates like any other standalone non-interactive command.

This mode is used when the pywbemcli command is invoked with a command or
command group name and arguments/options:

.. code-block:: text

    $ pywbemcli [GENERAL-OPTIONS] COMMAND [COMMAND-OPTIONS] [ARGS]

The following example enumerates classes in the ``root/cimv2`` namespace of the
WBEM server on ``localhost``:

.. code-block:: text

    $ pywbemcli --server http://localhost --default-namespace root/cimv2 --user username class enumerate
    Enter password: <password>
    . . .
    <Returns MOF for the enumerated classes>

.. index::
   pair: tab-completion; command mode
   pair: auto-suggestion; command mode

In command mode, tab-completion is supported for some command shells (ex. bash,
zsh), but must be activated specifically for each command line shell type.
Section :ref:"Activating shell tab-completion" documents the mechanisms for
activating shell completion.



.. index:: pair: interactive mode; command modes
.. index:: pair: interactive mode; modes of operation

.. _`Interactive mode`:

Interactive mode
----------------

In interactive mode (also known as :term:`REPL` mode), pywbem provides an
interactive shell environment that allows typing pywbemcli commands, internal
commands (for operating the pywbemcli shell), and external commands (that are
executed in the standard shell of the user).

The pywbemcli shell uses the prompt ``pywbemcli>``. The cursor is shown in
the examples as an underscore (``_``) in the following examples in this document.

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

The commands and options that can be typed in the pywbemcli shell are the rest
of the command line that would follow the ``pywbemcli`` command in
`command mode`_, as well as internal commands (for operating the pywbemcli
shell), and external commands (that are executed in the standard shell of the
user):

.. code-block:: text

    pywbemcli> [GENERAL-OPTIONS] COMMAND [ARGS] [COMMAND-OPTIONS]

        where: COMMAND can be either a group name and
               a command (ex. class find or repl)

    pywbemcli> :INTERNAL-COMMAND

    pywbemcli> !EXTERNAL-COMMAND

The general options may be included on the interactive command line to
override the general options entered in the initial command line for pywbemcli.
Thus, a user can define a server on the command line and override elements
of that definition with commands in the interactive mode.

NOTE: The effects of any general option entered in the interactive mode exists
only for that command and the original definition from the command line is
restored for the next command. Any changes to the :term:`connections file`
defined in the interactive mode and executed in the same command are retained
(ex. setting the default connection).

Thus:

.. code-block:: text

    pywbemcli --server http://blah
    pywbemcli> class get CIM_ManagedObject
    # The timeout change below only applies to the command on that line
    pywbemcli> --timeout 90 class get CIM_ManagedObject.
    # The --verbose mode only applies to the command on the same line.
    pywbemcli> --verbose class get CIM_ManagedObject

The following example starts a pywbemcli shell in interactive mode,
executes several commands, and exits the shell:

.. code-block:: text

    $ pywbemcli -s http://localhost -d root/cimv2 -u username

    pywbemcli> class enumerate --no
    . . . <Enumeration of class names in the default namespace>

    pywbemcli> class get CIM_System
    . . . <Class CIM_System in the default namespace in MOF format>

    pywbemcli> :q

The pywbemcli shell command ``class get CIM_System`` in the example
above has the same effect as the standalone command:

.. code-block:: text

    $ pywbemcli -s http://localhost -d root/cimv2 -u username class get CIM_System
    . . . <Class CIM_System in the default namespace in MOF format>


.. index:: pair: interactive mode; help

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

.. index:: pair: interactive mode; exit

In addition to using one of the internal exit commands shown in the help text
above, you can also exit the pywbemcli shell by typing <Ctrl-D> (on Linux,
OS-X and UNIX-like environments on Windows), or <Ctrl-C> (on native Windows).

.. index:: pair: interactive mode; --help

Typing ``--help`` or ``-h`` in the pywbemcli shell displays general help
information for the pywbemcli commands which includes general options and a
list of the supported command groups and commands without command group.

.. code-block:: text

    $ pywbemcli
    pywbemcli> --help
    Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS] [COMMAND-OPTIONS]
    . . .

    General Options:
      -n, --name NAME                 Use the WBEM server ...
      . . .

    Commands:
      class       Command group for CIM classes.
      connection  Command group for WBEM connection definitions.
      . . .

The usage line in this help text shows the usage in command mode. In
interactive mode, the ``pywbemcli`` word is omitted.

.. index:: pair: interactive mode; command help

Typing ``COMMAND --help``,  or ``COMMAND -h`` in the pywbemcli shell
displays help information for the specified pywbemcli command group, for
example:

.. code-block:: text

    pywbemcli> class --help
    Usage: pywbemcli [GENERAL-OPTIONS] class COMMAND [ARGS] [COMMAND-OPTIONS]
    . . .

    Command Options:
      -h, --help  Show this message and exit.

    Commands:
      associators   List the classes associated with a class.
      . . .

.. index::
   pair: tab-completion; interactive mode
   pair: auto-suggestion; interactive mode

The pywbemcli shell in the interactive mode always supports tab-completion and
usually with popup help text for commands, arguments, and options typing, where
the valid choices are shown based upon what was typed so far, and where an item
from the popup list can be picked with <TAB> or with the cursor keys. It can be
used to select from the list of general options. Interacitve
mode tab-completion may differ from command mode tab-completion because the
support is provided by a python package and not the shell. The following
examples show interactive mode tab-completion; an
underscore ``_`` is shown as the cursor:

.. code-block:: text

    pywbemcli> --_
    --name               Use the WBEM server defined by the WBEM connection ...
    --mock-server        Use a mock WBEM server that is automatically ...
    --server             Use the WBEM server at the specified URL with ...
    . . .

    pywbemcli> cl_
                  class

Interactive mode uses a combination of tab-completion and auto-suggestion  for
aut completion which are both always active:

  * :term:`tab-completion` - In this mode, a single <TAB> enables the display of
    available completion possibilities for command groups, commands, options
    and selected option values.
  * :term:`auto-suggestion` - The pywbemcli interactive mode also supports
    automated parameter suggestions based on the pywbemcli history file which
    works with the tab-completion described above. The input is compared to
    the history and when there is another entry starting with the given text,
    the completion will be shown as gray text behind the current input.
    Pressing the right arrow → or <CTRL-e> will insert this suggestion.


General options can be entered in the interactive mode but they generally only
apply to the current command defined in the same command input as the general
option.  Thus, to modify the output format for a particular command, enter the
--output-format general option before the command.  The following command
sets the output format to ``table`` before executing the command and then
restores it to the original value.:

.. code-block:: text

    pywbemcli> --output-format table instance enumerate CIM_Foo

A particular difference between general options in the interactive mode and
the command line mode is the ability to set general options back to their
default value in the interactive mode.   In the command mode this is not
required.  However, in the interactive mode, it could be useful to reset a
general option to its default value for a command.  Thus, if the log was set
on startup (--log all), it could be disabled for a command or the user name
(--user) could be set back to None.  However, normally the default value is
only set by not including that general option with the command line input

To reset selected string type general options in the interactive, the string
value of ``""`` (an empty string) is provided as the value which causes pywbemcli
to set the default value of that general option.

The following code defines a server with ``--user`` and ``--password`` in interactive
mode.  Then it attempts to modify the user and password to their default values
of None and execute the class enumerate again.  This command would be executed
without using the user and password because they have been reset for that command.

The following is an example of tab-completion when the next expected element is
an option; a single <TAB> enables the display of available completion possibilities:

.. code-block:: text

    pywbemcli> class enumerate <TAB>
     --di                   Include the complete subclass hierarchy of the requested classes in the result set. Default: Do not include sub...
     --deep-inheritance     Include the complete subclass hierarchy of the requested classes in the result set. Default: Do not include sub...
     --lo                   Do not include superclass properties and methods in the returned class(es). Default: Include superclass propert...
     --local-only           Do not include superclass properties and methods in the returned class(es). Default: Include superclass propert...
     --nq                   Do not include qualifiers in the returned class(es). Default: Include qualifiers.
     --no-qualifiers        Do not include qualifiers in the returned class(es). Default: Include qualifiers.
     --ico                  Include class origin information in the returned class(es). Default: Do not include class origin information.

Example of auto suggestion:

.. code-block:: text

    pywbemcli> cl
       The command line shows the proposed command grayed out based on that
       command being previously executed as depicted below. The <TAB> can be
       used to modify what is selected.
    pywbemcli> class get PG_TestElement -n test/static


.. index:: pair: command history; interactive mode

The pywbemcli shell supports commandhistory across multiple invocations of the shell
using <UP_ARROW>, <DOWN-ARROW> to step through the history line by line. The
pywbem interactive mode history file is separate from any shell history
files and is used only by pywbemcli.

.. index::
   single: command history; search
   pair: interactive mode; command history

A incremental search of the history can be initiated by entering <CTRL-r>
followed by one or more characters that define the search. The search displays
the last command containing the search string. This search string can be
modified in place to change the search, returning the last command in the
command history that contains the the string. <UP_ARROW>, <DOWN-ARROW> will
find other commands in the history containing the same string.

.. code-block:: text

    pywbemcli> <CTRL-r>
    (reverse-i-search)`':
                                                        ENTER Characters CIM
    (reverse-i-search)`CIM': class get CIM_ManagedElement
                                                        <UP-ARROW> and <DOWN-ARROW> find
                                                        other commands containing of "CIM"

    <DOWN_ARROW>
    (i-search)`get': instance get CIM_ComputerSystem.?
                                                        Hit <ENTER> selects current found command
    pywbemcli> instance get CIM_ComputerSystem.?

.. index:: pair: interactive mode; history file

The pywbemcli history is stored in the user home directory on linux systems.


A summary of help can be viewed by entering ``help repl`` when in the
interactive mode.

.. code-block:: text

    pywbemcli -s https:blah --user fred --pasword blah
    pywbemcli> class enumerate
    pywbemcli> --user "" --pasword "" class enumerate

.. index:: pair: Error handling; exit codes

.. _`Error handling`:

Error handling
--------------

.. index:: Exit codes

Pywbemcli terminates with one of the following program exit codes:

* **0 - Success**: The pywbemcli command has succeeded.

* **1 - Error**: In such cases, pywbemcli aborts the requested operation and
  displays one or more human readable error messages on standard error.

  If this happens for a command entered in interactive mode, the pywbemcli shell
  is not terminated; only the command that failed is terminated.

  Examples for errors reported that way:

  * Local system issues, e.g. pywbemcli history file or term:`connections file`
    cannot be written to.

  * WBEM server access issues, e.g. pywbemcli cannot connect to or authenticate
    with the WBEM server. This includes CIM errors about failed authentication
    returned by the server.

  * WBEM server operation issues, e.g. pywbemcli attempts to retrieve an
    instance that does not exist, or the WBEM server encountered an internal
    error. This will mostly be caused by CIM errors returned by the server,
    but can also be caused by the pywbemcli code itself.

  * Programming errors in mock Python scripts (see: :ref:`Mock WBEM server overview`);
    the error message includes a Python traceback of the error.

* **1 - Python traceback**: In such cases, pywbemcli terminates during its
  processing, and displays the Python stack traceback on standard error.

  If this happens for a command entered in interactive mode, the pywbemcli shell
  also terminates with a program exit code of 1.

  These Python tracebacks should never happen and are always considered a
  reason to open a bug in the
  `pywbemtools issue tracker <https://github.com/pywbem/pywbemtools/issues>`_.

  Note that an error message with a traceback from a mock Python script does
  not fall into this category and is an issue in that Python script and not
  in pywbemcli.

* **2 - User error**: In such cases, pywbemcli terminates without even
  attempting to perform the requested operation, and displays one or more human
  readable error messages on standard error.

  If this happens for a command entered in interactive mode, the pywbemcli shell
  is not terminated; only the command that failed is terminated.

  Examples for user errors are a missing required command argument, the use of
  an invalid option, or an invalid option argument.

* **2 - Help**: When help is requested (``--help``/``-h`` option or
  ``help command``), pywbemcli displays the requested help text on standard
  output and terminates.

  If this happens for a command entered in interactive mode, the pywbemcli shell
  is not terminated; only the command that displayed the help is terminated.
