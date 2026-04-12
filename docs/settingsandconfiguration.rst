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

Tab-completion is supported for pywbemlistener and pywbemcli in the
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

Tab-completion is not supported in the pywbemcli :ref:`Interactive mode`.

Tab-completion allows the terminal user to:

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

Tab-completion for pywbemlistener and pywbemcli must be manually activated after
pywbemtools installation.

.. index:: tab-completion
.. index:: Activating tab-completion

To activate shell tab-completion, the  script *magic variable*
(``<PROG-NAME>_COMPLETE``) must be defined in the shell initialization for the
shell defining the shell name and the pywbemtools name as follows:

.. code-block:: text

    * The shell magic variable    _<PROG-NAME>_COMPLETE=<SHELL-NAME>_source  <prog-name>

where:

    * `<PROG-NAME>` - pywbemtools command name in uppercase(i.e. PYWBEMCLI or PYWBEMLISTENER).
    * `<SHELL-NAME>` - shell name (i.e. bash, zsh, or fish).
    * `<prog-name>` - pywbemtools command name in lower case (pywbemcli or pywbemlistener).
                      The commands must be publicly available.

The existence of this shell *magic variable*  (``_<PROG-NAME>_COMPLETE``) in
the shell initialization file notifies the shell that this is a shell
tab-completion variable and the shell calls back to `<prog-name>` with
arguments containing ``_<PROG-NAME>_COMPLETE``, ``_<SHELL-NAME>_source`` and
other tab-completion information in environment variables.  The pywbemtools
command  `prog-name` returns the correct completion script text specific for
that shell as the call return value.

The ``eval`` completes the initialization by making the COMPLETE script returned
from the bash call to the pywbemtool command available within the current shell.

The pywbemtools commands must be public for this initialization.Note also that
the tab-completion script is created each time the shell is initialized

Table table:ref:`tab-complete-eval-statement` defines an ``eval`` statement
for the shells that pywbemcli/pywbemlistener support for tab-completion that
should be added to a shell startup file defined in the table, for example:

.. code-block:: text

    # example for tab-completion activation and bash shell, These lines
    # are be inserted into bash initialization (.bashrc)
    eval "$(_PYWBEMCLI>_COMPLETE=bash_source pywbemcli)"
    eval "$(_PYWBEMLISTENER_COMPLETE=bash_source pywbemlistener)"

.. table:: Eval statement and proposed startup shell startup  eval command to use for several shells

  ======  =======================================  =========================================================
  Shell   File to insert eval statement            Eval command
  ======  =======================================  =========================================================
  bash    ~/.bashrc                                eval "$(_<PROG-NAME>_COMPLETE=bash_source <prog-name>)"
  zsh     ~/.zshrc                                 eval "$(_<PROG-NAME>_COMPLETE=zsh_source <prog-name>_COMPLETE=zsh_source <prog-name>)"
  fish    ~/.config/fish/completions/foo-bar.fish  eval (env _<PROG-NAME>_COMPLETE=fish_source <prog-name>_COMPLETE=fish_source <prog-name>)
  ======  =======================================  =========================================================


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
pywbemtools active or for some reason pywbemtools is not in a public directory.

Create a complete tab-completion script file using the same statement (ex.
``_<PROG-NAME>_COMPLETE=<shell-type>_source <prog-name>``) but save the
resulting complete script in a file (ex: ``~/.pywbemcli-complete.bash``).  This
file contains the shell-specific logic to activate tab-completion and process
tab-completion calls. Then activate tab-completion by sourcing that script
file (ex. ``source ~/.pywbemcli-complete.bash``) which is independent of
whether pywbemcli and pywbemlistener are public.

The following table defines the shell command for supported shells to create the
complete script file.  The naming and exact location of the file is arbitrary and
the locations shown in the table are examples.  However, the file is different
for each shell.

.. _shell-completion-script:

.. table:: Creation of the complete script file as the tab-completion initialization
   :name: shell-completion-script

  =====  ===========================================================================
  Shell  Script creation command
  =====  ===========================================================================
  bash   _<PROG-NAME>_COMPLETE=bash_source <prog-name> > ~/.<prog-name>-complete.bash
  zsh    _<PROG-NAME>_COMPLETE=zsh_source <prog-name> > ~/.<prog-name>-complete.zsh
  fish   _<PROG-NAME>_COMPLETE=fish_source <prog-name> >
         ~/.config/fish/completions/<prog-name>.fish
  =====  ===========================================================================

Once the complete script file has been created, tab-completion activation is completed
by sourcing the complete script file to notify the shell of the complete file
each time a terminal is opened. For example as follows:

.. code-block:: text

    # example for bash and pywbemcli
    $ _PYWBEMCLI_COMPLETE=bash_source pywbemcli > ./blah/pywbemcli-complete.bash
    $ source  ~/blah.pywbemcli-complete.bash

This step can be executed automatically:

* by including the sourcing statement in a terminal startup script
  (ex. in ``.bashrc``).
* or including sourcing statement as part of a virtual environment startup

Or the sourcing statement can be executed when a terminal is open simply by
executing the script itself(ex. ``source  ~/.pywbemcli-complete.bash``).

Thus in summary, for bash, pywbemcli and pywbemlisteer can be activated by
inserting the following evaluation script into .bashrc if
pywbemcli/pywbemlistener are publicly available whenever the terminal is
started:

.. code-block::

    eval "$(_PYWBEMCLI_COMPLETE=bash_source pywbemcli)"
    eval "$(_PYWBEMLISTENER_COMPLETE=bash_source pywbelistener)"

or by creating a completion script file one time as follows when pywbemlistener
and pywbemcli are publicly available and then sourcing the script when,
for example, the terminal window is opened:

.. code-block::

    # Execute once when pywbemcli is in the path:

    _PYWBEMCLI_COMPLETE=bash_source pywbemcli > ~/.pywbemcli-complete.bash
    _PYWBEMLISTENER_COMPLETE=bash_source pywbemlistener > ~/.pywbemlistener-complete.bash


    # Source the resulting file each time a terminal is started (ex edit into .bashrc):

    source  ~/.pywbemcli-complete.bash
    source  ~/.pywbemlistener-complete.bash


