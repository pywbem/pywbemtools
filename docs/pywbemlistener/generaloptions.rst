.. _`pywbemlistener general options`:

Pywbemlistener general options
------------------------------

General options are those that are specified directly after the ``pywbemlistener``
command, e.g. ``--output-format simple`` in the following example:

.. code-block:: text

    pywbemlistener --output-format simple list

Most of the general options can be specified with any of the sub-commands of the
``pywbemlistener`` command, but there are some general options that are used
only on some sub-commands, and are ignored on the other sub-commands.


.. index:: single: pywbemlistener logging

.. _`pywbemlistener logging`:

Logging
"""""""

Logging is performed only by the ``pywbemlistener run`` command. The
``pywbemlistener start`` command passes its logging settings on to the
``pywbemlistener run`` command it starts as a background process. All other
``pywbemlistener`` commands ignore the logging settings.

Logging is enabled by specifying the ``-l DIR`` or ``--logdir DIR`` general
option, or by setting the ``PYWBEMLISTENER_LOGDIR`` environment variable to
``DIR``. The general option has precedence over the environment variable.
``DIR`` is the path name of the directory where the log files will
reside in.

There is a log file created for each listener that is running.
The log files are named ``pywbemlistener_NAME.log`` where ``NAME`` is the
listener name.

Existing log files are appended to when a listener is started.

The lines in the log file are plain messages without any specific format, and
without a time stamp.


.. index:: single: pywbemlistener output formats

.. _`pywbemlistener output formats`:

Output format
"""""""""""""

The output of the ``pywbemlistener list`` and ``pywbemlistener show`` commands
is influenced by the ``--output-format`` general option.

Only table formats can be specified; for details see :ref:`Table formats`.


.. _`pywbemlistener miscellaneous general options`:

Miscellaneous
"""""""""""""

The ``--verbose`` or ``-v`` general option displays extra information about the
processing. It can be specified multiple times as follows:

* ``-v`` (one time): Display indication processing settings
* ``-vv`` (two times): Display interactions between start and run commands

The ``--warn`` general option controls the display of Python warnings.

The ``--version`` general option displays pywbemlistener version
information

The ``--pdb`` general option is for debugging the command: It brings up the
pdb debugger right before the sub-command starts executing.

The ``--help`` or ``-h`` general option provides help for the ``pywbemlistener``
command and its general options.
