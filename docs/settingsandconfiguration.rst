.. Copyright  2023 IBM Corp. and Inova Development Inc.
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


.. _`Settings and Configuration`:

Settings and Configuration
==========================

Both pywbemtools and pywbemcli execute after installation without any
configuration except for the use of tab-completion (using <TAB> on the shell
command line) to attempt to complete parameters.

.. _`Activating shell tab-completion`:

Activating shell tab-completion
-------------------------------

.. index:: pair: bash shell; tab-completion
.. index:: pair: zsh shell; tab-completion
.. index:: pair: fish shell; tab-completion

Shell tab-completion for pywbemlistener and pywbemcli must be manually activated
after installation and tab-completion is available only for the following shells:
(bash, zsh, and fish).  Tab-completion must be activated separately for
pywbemcli and pywbemlistener.

.. index:: tab-completion
.. index:: Activating tab-completion

To activate shell tab-completion for the shells where pywbemcli and pywbemlistener
support shell completion, you inform the shell that completion is
available for each tool. This is done through the following statement:

    ``_<PROG-NAME>_COMPLETE = _<SHELL-NAME>_source  <prog-name>``

    where:

      * ``<PROG-NAME>`` is the name of the pywbemtool in uppercase
      * ``<SHELL-NAME>`` is the name of the shell (ex. bash, zsh, or fish)
      * ``<prog-name`` the name of the pywbemtool in lower case

This magic variable notifies the shell that this is a shell tab-completion
variable and the shell then calls back to ``<prog-name>`` with arguments
containing ``_<PROG-NAME>_COMPLETE`` and ``_<SHELL-NAME>_source`` and other
tab-completion information in environment variables.  The pywbemtool returns
the pywbemtool competion script specific for that shell.

Tab-completion is supported in pywbemcli and pywbemlistener to:

* Completd  the static elements of the command line including:
    * command group names (ex. ``subscription``),
    * command names (ex. ``enumerate``, ``list``, etc.),
    * option names (``--name``, ``-n``, etc.).
* Complete the value of arguments and options that depend on
  local data to complete the commands (i.e where a WBEM server is not contacted).
  Thus, the pywbemcli option ``--name`` which defines the name of a connection
  in a connection file can be completed (pywbemcli search the names
  in the file). But the value of the class in ``class get`` does not support
  tab-completion because that involves a connection to the WBEM server.

Tab-completion is:

* Always enabled in the pywbemcli :ref:`Interactive mode`. **WARNING:** Currently the
  tab-completion of option and argument values does not work in the interactive
  mode because of issues with a pywbemcli dependencies.
* Enabled in the :ref:`command mode` when shell tab-completion is activated
  for pywbemcli/pywbemlistener and only with the following shells:

  * **bash shell** - (bash version 4.4 or greater). not all Linux implementations
    include the bash_complete addon so that the user may be required to install
    the add-on. A simple test with a utility like ``ls`` will indicate if
    tab-completion is available  in bash(ex. enter ``ls <TAB>`` to test for the
    existence of the bash_complete addon).
  * **zsh shell** - Tab-completion is available for all versions of zsh but
    may need to be activated in the zsh config file. Furthermore there are two
    different completion systems for zsh.
  * **fish shell** - Available for all versions of this shell.

Once tab-completion is activated for a shell type , hitting <TAB> or <TAB><TAB>
initiates tab-completion for command names, option names, and some
option/argument values which attempts to return the completion of the word on
the command line where <TAB> was entered. If there are multiple possible
completions, the shell returns the list or do nothing until a second <TAB> is
entered.

If hitting <TAB> or <TAB><TAB> when tab-completion is active returns nothing,
either the word at the terminal cursor does is not matched with a possible
target (ex. ``pywbemcli --name xxx<TAB>`` for pywbemcli connection name when
there is no connection name that starts with ``xxx`) or there is no
tab-completion (ex. for example for the class name in ``get class
<class-name>``)

Activation of tab-completion involves the following but with different
formats for each shell type:

1. Getting from pywbemcli the body of a completion script for the terminal's
   shell type as defined above using the magic variable.
2. Notifying the shell of this completion script by either:
   * notifying the shell with a shell  ``eval`` statement or,
   * saving the script to a completion script file and notifying the shell later
   by sourcing the resulting completion script file.

Activation with eval statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Table table:ref:`tab-complete-eval-statement` defines the ``eval`` statement
for the shells that pywbemcli/pywbemlistener support for tab-completion that
would be added to a shell startup file defined in the table, for example
with a bash shell:

  _COMPLETE_PYWBEMCLI=bash_source pywbemcli

.. _tab-complete-eval-statement:

.. table:: Eval statement and proposed startup shell startup file to use for several shells

  ======  =======================================  =========================================================
  Shell   File to insert eval statement            Eval command
  ======  =======================================  =========================================================
  bash    ~/.bashrc                                eval "$(_<PROG_NAME>_COMPLETE=bash_source pywbemcli)"
  zsh     ~/.zshrc                                 eval "$(_<PROG_NAME>_COMPLETE=zsh_source pywbemcli)"
  fish    ~/.config/fish/completions/foo-bar.fish  eval (env _<PROG_NAME>_COMPLETE=fish_source pywbemcli)
  ======  =======================================  =========================================================

.. note :: With Python 2.7 or Python 3.5 the variable value (ex. ``bash_source``)
           must have the two words reversed  (ex. ``source_bash)`` because these
           python versions only support an old version of the package click
           which maintains the scripts.

The above method may be difficult when the location of the pywbemcli
executable is not in the path (ex. when pywbemtools is in a virtual environment)
since the ``eval`` statement initiates a callback to the pywbemcli/pywbemlistener and
the location of those executables may not be publially available. Also it can
slow down terminal startup because pywbemcli must be called on each terminal
startup to get the completion script definition.

Activation by creating a complete script file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An alternative is to create a complete script file using the same statement
(ex. ``_<PROG-NAME>_COMPLETE=<shell-type>_source pywbemcli``) but saving the
resulting complete script in a file.  This file contains the shell-specific
logic to activate tab-completion and process tab-completion calls. The user
then activates tab-completion by sourcing that file (ex. ``source
~/.pywbemcli-complete.bash``) which is independent of whether
pywbemcli/pywbemlistener are public.

The following table defines the shell command for supported shells to create the
complete script file.  The naming and exact location of the file is arbitray and
the locations shown in the table are examples.  However, 1. the file is different
for each shell and also it is different if Python versions 2.7 or 3.5 are use rather
than later versions of Python.

.. _shell-completion-script:

.. table:: Creation of the complete script file as the tab-completion initialization
   :name: shell-completion-script

  =====  ===========================================================================
  Shell  Script
  =====  ===========================================================================
  bash   _<PROG_NAME>_COMPLETE=bash_source pywbemcli > ~/.<prog_name>-complete.bash
  zsh    _<PROG_NAME>_COMPLETE=zsh_source pywbemcli > ~/.<prog_name>-complete.zsh
  fish   _<PROG_NAME>_COMPLETE=fish_source pywbemcli >
         ~/.config/fish/completions/<prog_name>.fish
  =====  ===========================================================================

.. note :: The variable value (ex. ``bash_source``) must have the two words reversed
           if tab-completion is being activated with Python 2.7 or Python 3.5 (ex.
           ``source_bash``)

Once the complete script file has been created, tab-completion activation is completed
by sourcing the complete script file to notify the shellof the complete file
each time a terminal is opened. For example as follows:

.. code-block:: text

    $ source  ~/.pywbemcli-complete.bash

This step can be executed automatically:

* by including the sourcing statement in a terminal startup script
  (ex. in ``.bashrc``).
* or including sourcing statement as part of a virtual environment startup

Or the sourcing statement can be executed when a terminal is open simply by
executing the script itself(ex. ``source  ~/.pywbemcli-complete.bash``).

Thus in summary, for bash, pywbemcli can be activated by inserting the following
evaluation script into .bashrc if pywbemcli/pywbemlistener are publically
available whenever the terminal is started:

.. code-block::

    eval "$(_PYWBEMCLI_COMPLETE=bash_source pywbemcli)"

or by creating a completion script file one time as follows when pywbemlistener
and pywbemcli are publically avialable and then sourcing the script when,
for example, the terminal window is opened.:

.. code-block::

    # Execute once when pywbemcli is in the path:

    _PYWBEMCLII_COMPLETE=bash_source pywbemcli > ~/.pywbemcli-complete.bash

    # Source the resulting file each time a terminal is started (ex edit into .bashrc)
    source  ~/.pywbemcli-complete.bash


Testing that pywbemcli tab-completion is activated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The tab-completion activation of pywbemcli and pywbemlistener can be tested in
a terminal by entering part of a known command and using the <TAB> to request
completion. The example below shows testing:

.. code-block:: text

   $ pywbemcli clas<TAB>

   This should complete the class statement (i.e. expand cmd line to
   ``pywbemcli class``).

Each shell type has one or more commands to determine the state of
tab-completion for a particular application.  In bash it is the builtin command
``complete`` used both to define the tab-completion for a particular command
and to list which commands have been activated.

Executing the bash builtin ``complete -p pywbemcli`` command should return the
a line that defines the completion for pywbemcli as follows:

.. code-block:: text

    $ complete -p pywbemcli       < ------------ This returns the following
                                                 if tab-completion is active

    complete -o nosort -F _pywbemcli_completion pywbemcli

Zsh has corresponding commands depending on the version of completion and the
use of the bashcompinit plugin.

Removing shell tab-completion activation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bash: The command ``complete -r pywbemcli`` removes the tab-completion for
pywbemcli.

Zsh: Depends on zsh configuration


