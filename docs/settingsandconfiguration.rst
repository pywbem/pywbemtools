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

Both pywbemtools (pywbemcli and pywbemlistener) execute after installation
without any configuration except for the use of tab-completion (using <TAB> on
the shell command line) to attempt to complete parameters. The tab-completion
is not active after installation and must be activated separately.


.. _`Activating shell tab-completion`:

Activating shell tab-completion
-------------------------------

.. index:: pair: bash shell; tab-completion
.. index:: pair: zsh shell; tab-completion
.. index:: pair: fish shell; tab-completion
.. index:: pair: shell tab completion; tab completion

Shell tab-completion, when activated, allows the terminal user to:

* Complete the static elements of the command line including:

    * command group names (ex. ``pywbemcli subscription``),
    * command names (ex. ``pywbemcli class enumerate``, ``list``, etc.),
    * command option names (``pywbemcli connection --name``, ``-n``, etc.).

* Complete the value of arguments and options that depend on local data to
  complete the commands (ex. where a WBEM server is not contacted). Thus, the
  pywbemcli option ``--name`` which defines the name of a connection in a
  connection file can be completed (pywbemcli searches the names in the file).
  But the value of the class in ``class get`` does not support tab-completion
  because that involves a connection to the WBEM server.

Tab-completion for the pywbemtool commands (pywbemlistener and pywbemcli) must
be manually activated after pywbemtools installation.

Shell tab-completion is supported for pywbemlistener and pywbemcli in the
:ref:`command mode`, for the following shells:

  * **bash shell** - (bash version 4.4 or greater). Not all Linux implementations
    include the bash_complete addon so that the user may be required to install
    the add-on. A simple test with a utility like ``ls`` will indicate if
    tab-completion is available  in bash(ex. enter ``ls <TAB>`` to test for the
    existence of the bash_complete addon).

  * **zsh shell** - Tab-completion is available for all versions of zsh but
    may need to be activated in the zsh config file. Furthermore there are two
    different completion systems for zsh.

  * **fish shell** - Available for all versions of this shell.

.. index:: tab-completion
.. index:: Activating tab-completion

To activate shell tab-completion, the shell magic variable
(``_<PROG-NAME>_COMPLETE``) must be defined in the shell initialization for the
shell, defining the shell name and the pywbemtools name as follows:

.. code-block:: text

    * _<PROG-NAME>_COMPLETE=<SHELL-NAME>_source  <prog-name>

where:

    * `<PROG-NAME>` - pywbemtools command name in uppercase(i.e. PYWBEMCLI or PYWBEMLISTENER).
    * `<SHELL-NAME>` - shell name (i.e. bash, zsh, or fish).
    * `<prog-name>` - pywbemtools command name in lower case (pywbemcli or pywbemlistener).
      pywbemcli and pywbemlistener must be publicly available.

The existence of this shell variable (``_<PROG-NAME>_COMPLETE``) when the
shell is started indicates that this is a shell tab-completion variable and the
shell calls back to `<prog-name>` oon terminal startup with arguments containing
``_<PROG-NAME>_COMPLETE``, ``_<SHELL-NAME>_source`` and other tab-completion
information in environment variables.  The pywbemtools command  `prog-name`
returns the correct completion script text specific for that shell as the call
return value.

The ``eval`` statement defined in the table below contains the ``eval``
statement in the shell startup script for supported shells that activates the
tab-completion initialization by making the script returned from the shell call
to the pywbemtools command available within the current shell instantiation.

The pywbemtools commands must be public for this initialization to work. The
tab-completion script is created each time the shell is initialized and is
placed in the user root directory.

An ``eval` command specific for each supported shell should be added to the
shell started up file for that shell type  to activate shell tab-completion
of that particular shell, and each of the pywbemtools commands. For example
the following example activates the bash shell tab-completion for pywbemcli
each time a bash terminal shell is started. :

.. code-block:: text

    eval "$(_PYWBEMCLI_COMPLETE=bash_source pywbemcli)"
    eval "$(_PYWBEMLISTENER_COMPLETE=bash_source pywbemlistener)"

The following table defines the shell tab-activation ``eval`` command for each
of the shell types supported by pywbemtools.

.. table::

  ======  =======================================  =========================================================
  Shell   File to insert eval statement            Eval command
  ======  =======================================  =========================================================
  bash    ~/.bashrc                                eval "$(_<PROG-NAME>_COMPLETE=bash_source <prog-name>)"
  zsh     ~/.zshrc                                 eval "$(_<PROG-NAME>_COMPLETE=zsh_source <prog-name>_COMPLETE=zsh_source <prog-name>)"
  fish    ~/.config/fish/completions/foo-bar.fish  eval (env _<PROG-NAME>_COMPLETE=fish_source <prog-name>_COMPLETE=fish_source <prog-name>)
  ======  =======================================  =========================================================


This `eval` statement defines the shell variable and the pywbemtool tool in a
shell variable(_<prog_name>_COMPLETE) and notifies the the defined shell that
the pywbemtool is to be activated. The shell both the pywbemtool to create the
required script.


Testing that tab-completion is activated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The tab-completion activation of pywbemcli and pywbemlistener can be tested in
a terminal by entering part of a known command and using the <TAB> to request
completion. The example below shows testing:

.. code-block:: text

   $ pywbemcli clas<TAB>

   This should complete the class statement (i.e. expand cmd line to
   ``pywbemcli class``).

   $ pywbemlistener star<TAB>

   This should complete the start command name (i.e. expand command line to
   ``pywbemlistener start``)

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


Alternate activation by directly creating the tab-completion script file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This activation technique is useful if you have multiple implementations of
pywbemtools installed or for some reason pywbemtools is not in a public
directory.

Create a complete tab-completion script file using the statement (ex.
``_<PROG-NAME>_COMPLETE=<shell-type>_source <prog-name>``) but save the
resulting complete script in a file (ex: ``~/.pywbemcli-complete.bash``).  This
file contains the shell-specific logic to activate tab-completion and process
tab-completion calls. Then activate tab-completion by sourcing that script
file (ex. ``source ~/.pywbemcli-complete.bash``) which is independent of
whether pywbemcli and pywbemlistener are public.

The following table defines the shell command for supported shells to create the
complete script file.  The naming and exact location of the file is arbitrary and
the locations shown in the table are examples.  However, the script file created
is different for each shell. The following table defines the line to be executed
to create the COMPLETE shell script for each supported shell type. This can be
executed one time after pywbemtools is installed since that script is fixed
by the code in the pywbemtool.

.. table::

  =====  ===========================================================================
  Shell  Script creation command
  =====  ===========================================================================
  bash   _<PROG-NAME>_COMPLETE=bash_source <prog-name> > ~/.<prog-name>-complete.bash
  zsh    _<PROG-NAME>_COMPLETE=zsh_source <prog-name> > ~/.<prog-name>-complete.zsh
  fish   _<PROG-NAME>_COMPLETE=fish_source <prog-name> >
         ~/.config/fish/completions/<prog-name>.fish
  =====  ===========================================================================


The activation is completed by sourcing the script before the pywbemtool is
executed in an active shell. For example to complete activation for bash where
the script is in ~/blah execute :

.. code-block:: text

    $ source ~/blah/pywbemcli-complete.bash

    The pywbemtool should now have shell tab completion active for bash

For example the following creates the shell tab-completion script for bash and
pywbemcli in directory ./blah and can be executed once after pywbemcli
installation:

.. code-block:: text

    # example for bash and pywbemcli where the script is placed in  directory ./blah
    $ _PYWBEMCLI_COMPLETE=bash_source pywbemcli > ./blah/pywbemcli-complete.bash

The second step can be executed any time before pywbemcli is executed and
activates shell tab-completion for the current shell execution by sourcing the
COMPLETE script created in the first step:


.. code-block:: text

    $ source  ~/blah.pywbemcli-complete.bash

This step can be executed automatically:

* by including sourcing statement as part of a virtual environment startup

* or executing the sourcing statement when a terminal is opened by
  executing the script itself (ex. ``source  ~/.pywbemcli-complete.bash``).

* or executing in the shell before using pywbemcli in a single terminal session.

