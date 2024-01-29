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


.. _`Pywbemlistener commands`:

Pywbemlistener commands
=======================

This section describes each of the pywbemlistener commands including examples.

The pywbemlistener commands are:

* :ref:`pywbemlistener list command` - List the currently running named WBEM indication listeners.
* :ref:`pywbemlistener show command` - Show a named WBEM indication listener.
* :ref:`pywbemlistener start command` - Start a named WBEM indication listener in the background.
* :ref:`pywbemlistener stop command` -  Stop a named WBEM indication listener.
* :ref:`pywbemlistener test command` -  Send a test indication to a named WBEM indication listener.
* :ref:`pywbemlistener run command` - Run as a named WBEM indication listener.
* :ref:`pywbemlistener help command` - Show help for particular pywbemcli subjects
* :ref:`pywbemlistener docs command` - Issue request to web browser to load pywbemcli documentation

.. _`pywbemlistener list command`:

``pywbemlistener list`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pywbemlistener list`` command lists the currently running WBEM indication
listeners on the local system. They are identified as the processes executing
the ``pywbemlistener run`` command.

Example:

.. code-block:: text

    $ pywbemlistener list
    +--------+--------+----------+-------------+--------+---------------------+
    | Name   |   Port | Scheme   | Bind addr   |    PID | Created             |
    |--------+--------+----------+-------------+--------+---------------------|
    | lis1   |  25989 | http     | none        | 131870 | 2023-06-07 12:17:55 |
    +--------+--------+----------+-------------+--------+---------------------+


The ``-o, --output-format`` general option can be used to control the format of
the table that is displayed, for example:

Example:

.. code-block:: text

    $ pywbemlistener -o rst list
    ======  ======  ========  =====  ===================
    Name      Port  Scheme      PID  Created
    ======  ======  ========  =====  ===================
    lis1     25989  https     59327  2021-07-03 15:31:55
    ======  ======  ========  =====  ===================

See :ref:`pywbemlistener list --help` for the exact help output of the command.


.. _`pywbemlistener show command`:

``pywbemlistener show`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pywbemlistener show`` command shows details of a specific running WBEM
indication listener on the local system, by specifying the listener name.

The running listeners are identified as the processes executing the
``pywbemlistener run`` command. The listener name is also identified from
the process command line.

Example:

.. code-block:: text

    $ pywbemlistener show lis1
    +------------------+---------------------+
    | Attribute        | Value               |
    |------------------+---------------------|
    | Name             | lis1                |
    | Port             | 25989               |
    | Scheme           | http                |
    | Bind addr        | none                |
    | Certificate file |                     |
    | Key file         |                     |
    | Indication call  |                     |
    | Indication file  |                     |
    | Log file         |                     |
    | PID              | 131870              |
    | Start PID        | 131868              |
    | Created          | 2023-06-07 12:17:55 |
    +------------------+---------------------+


See :ref:`pywbemlistener show --help` for the exact help output of the command.


.. _`pywbemlistener start command`:

``pywbemlistener start`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pywbemlistener start`` command starts a new WBEM indication listener on
the local system.

The listener is running as a normal user process in the background, inheriting
the group and user context from the process that runs the ``pywbemlistener start``
command (usually the shell process in a terminal session).

Example:

.. code-block:: text

    $ pywbemlistener start lis1 --cert-file .../certs/server_cert.pem --key-file .../certs/server_key.pem
    Running listener lis1 at https://localhost:25989

The previous example started a listener for HTTPS (the default) on the default
port 25989. Because HTTPS was used, it was necessary to specify an X.509 server
certificate and its key file.

The ``-p, --port`` option specifies the port on which the listener will
receive indicaitons.

The use of HTTP instead of the default HTTPS can be used by specifying it with
the ``-s, --scheme`` option defines whether HTTP or HTTPS schema will be used
as the bind url on which the listener is expecting indications. The default is
HTTPS.

The ``-b, --bind-addr`` option specifies that the listener will be bound to a
single network interface and on linux systems, typically, to a single IP
address on that interface. When a listener is bound to a single network
interface/IP address it can receive indications only addressed to that network
interface/IP address. Thus if the listener is bound to ``localhost`` (i.e. the
local network interface) it will be able to only receive indications addressed
to that network interface. The default when --bind-addr is not set is for the
the listener to received indications addressed to any valid IPV4 or IPV6 IP
address defined on the local system. (New in pywbemtools version 1.3.0).

When the listener receives an indication, by default it drops it and does nothing
else.

The following actions can be configured to be performed on each received
indication. Multiple actions can be specified.

* Appending it as a line to a file:

  This action is enabled by specifying the ``--indi-file FILE`` option.

  The format of the line can be configured using the ``--indi-format FORMAT``
  option.

  ``FORMAT`` is a Python new-style format string that can use the following
  keyword args:

  * 'dt' - datetime object of the time the listener received the indication, in
    local time. The object is timezone-aware on Python 3.6 or higher.
  * 'dt_tzname' - timezone name of the datetime object if timezone-aware, else
    the empty string.
  * 'h' - Host name or IP address of the host that sent the indication
  * 'i' - pywbem.CIMInstance object with the indication instance
  * 'c' - CIM classname of the indication instance
  * 'p' - Case-insensitive dictionary of the indication properties, displayed
    as blank-separated name=value items

  The default format is: "{dt} {h} {c} {p}".

* Calling a Python function, via the ``--indi-call MODULE.FUNCTION`` option.

  ``MODULE`` must be a module name or a dotted package name in the module search
  path, e.g. 'mymodule' or 'mypackage.mymodule'.

  The current directory is added to the front of the Python module search path,
  if needed. Thus, the module can be a single module file in the current
  directory, for example:

  .. code-block:: text

      ./mymodule.py

  or a module in a package in the current directory, for example:

  .. code-block:: text

      ./mypackage/__init__.py
      ./mypackage/mymodule.py

  ``FUNCTION`` must be a function in that module with the following interface:

  .. code-block:: text

      def func(indication, host)

  Parameters:

  * 'indication' is a :class:`pywbem.CIMInstance` object representing the CIM
    indication that has been received. Its 'path' attribute is None.

  * 'host' is a string with the host name or IP address of the indication sender
    (typically a WBEM server).

  The return value of the function will be ignored.

  Exceptions raised when importing the module cause the 'pywbemlistener run'
  command to terminate with an error. Exceptions raised by the function when
  it is called cause an error message to be displayed on stderr of the listener
  process and logged, if logging is enabled.

The started WBEM indication listener can log any issues it encounters, to a file.
This is enabled by using the ``-l, --logdir DIR`` general option.

See :ref:`pywbemlistener start --help` for the exact help output of the command.


.. _`pywbemlistener stop command`:

``pywbemlistener stop`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pywbemlistener stop`` command stops a running WBEM indication listener on
the local system.

Example:

.. code-block:: text

    $ pywbemlistener stop lis1
    Shut down listener lis1 running at http://localhost:25989

On Windows, the listener process is stopped immediately without giving the
process control to clean up. On other platforms, the listener process is stopped
gracefully, giving the process control to clean up.

See :ref:`pywbemlistener stop --help` for the exact help output of the command.


.. _`pywbemlistener test command`:

``pywbemlistener test`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pywbemlistener test`` command sends a test indication to a running WBEM
indication listener on the local system.

This command has two options:

The ``-c, --count`` option that defines the number of indications to set where
the default is to send a single indication.

The ``-l, --listener`` option that defines a host name or IP address to which
the indications will be sent.  The default ``--listener`` is ``localhost``.

Example:

.. code-block:: text

    $ pywbemlistener test lis1
    Sending the following test indication:
    instance of CIM_AlertIndication {
       IndicationIdentifier = NULL;
       IndicationTime = "20210711160151.847111+000";
       AlertingElementFormat = 2;
       AlertingManagedElement = NULL;
       AlertType = 2;
       Message = "Test message";
       MessageID = "TEST0000";
       OwningEntity = "TEST";
       PerceivedSeverity = 2;
       ProbableCause = 0;
       SystemName = NULL;
       MessageArguments = { };
    };
    Sent test indication to listener lis1 at http://localhost:25989

See :ref:`pywbemlistener test --help` for the exact help output of the command.


.. _`pywbemlistener run command`:

``pywbemlistener run`` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pywbemlistener run`` command runs the WBEM indication listener code
in a loop that never ends. It is possible to start this command in the
background or even run it in the foreground, but it is not recommended that
users do that directly. Instead, users should use the
:ref:`pywbemlistener start command`, which starts the ``pywbemlistener run``
command as a background process. Use the  ``pywbemlistener run`` command only
when you need to have control over how exactly the process runs in the
background.

The argument and options for the run command are the same as for the
``pywbemlistener start`` command.

Note: The --start-pid option is needed because on Windows, the
``pywbemlistener run`` command is not the direct child process of the
``pywbemlistener start`` command starting it.

See :ref:`pywbemlistener run --help` for the exact help output of the command.

.. index::
    pair: help; command

.. _`pywbemlistener help command`:

pywbemlistener ``help`` command
-------------------------------

.. index::
    single: pywbemlistener help command
    pair: help; pywbemlistener command

The ``help`` command provides information on a number of subjects where the
extra help might be needed on pywbemlistener: This includes subjects like

* activating the shell tab-completion,


This is different from the ``--help`` option that provides information on
command groups, and commands.

.. code-block:: text

    $ pywbemcli help

    Help subjects:
    Subject name    ubject description
    --------------  --------------------------------------------
    activate        How to activate tab-completion
    tab-completion  Using tab-completion

The help for each subject is retrieved by entering the subject name for
the subject of interest as the argument to the help command:

Thus, for example:

.. code-block:: text

    $ pywbemcli help activate
      . . . returns help on activating tab-completion

.. index::
    pair: help; command

.. _`pywbemlistener docs command`:

pywbemlistener ``docs`` command
-------------------------------

.. index::
    single: pywbemlistener docs command
    pair: docs; pywbemlistener command

The ``docs`` command provides a simple way to access the pywbemtools
documentation  publically available on the WEB.  This command calls the
system default WEB browser with the URL of the pywbemtools documentation
to open a new browser window with the top level page of that documentation and
immediatly terminates or returns to the repl command line.

This is ``experimental`` as of pywbemtools 1.2.0.
