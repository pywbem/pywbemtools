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

Pywbemcli Command line interface
================================

This package provides a command line interface (CLI) in the pywbemcli tool
that supports communication with a WBEM server through the pywbem client
api and shell scripting.

.. _`Modes of operation`:

Modes of operation
------------------

pywbemcli supports two modes of operation:

* `Interactive mode`_: Invoking an interactive pywbemcli shell for typing
  pywbemcli sub-commands.
* `Command mode`_: Using it as a standalone non-interactive command.

.. _`Interactive mode`:

Interactive mode
----------------

In interactive mode, an interactive shell environment is brought up that allows
typing pywbemcli commands, internal commands (for operating the pywbemcli
shell), and external commands (that are executed in the standard shell for the
user).

This pywbemcli shell is started when the ``pywbemcli`` command is invoked without
specifying any (sub-)commands::

    $ pywbemcli [GENERAL-OPTIONS]
    > _

Alternatively, the pywbemcl shell can also be started by specifying the ``repl``
(sub-)command::

    $ pywbemcli [GENERAL-OPTIONS] repl
    > _

The pywbemcli shell uses the ``>`` prompt, and the cursor is shown in the examples
above as an underscore ``_``.

General options may be specified on the ``pywbemcli`` command, and they serve as
defaults for the pywbemcli commands that can be typed in the pywbemcli shell and
as the definition of the connection to a WBEM Server.

The pywbemcli commands that can be typed in the pywbemcli shell are simply the command
line arguments that would follow the ``pywbemcli`` command when used in
`command mode`_::

    $ pywbemcli -s http://localhost -n root/cimv2 -u username
    Enter password: <password>
    > class enumerate -o
    . . . <Enumeration of the names of classes in the defined namespace>
    > class get CIM_System
    . . . <MOF output of the class CIM_System from the WBEM Server>
    > :q

For example, the pywbemcli shell command ``class get CIM_System`` in the example
above has the same effect as the standalone command::

    $ pywbemcli -s http://localhost -u username class get CIM_System
    Enter password: <password>
    . . . <MOF formated display of the CIM_System class>

TODO: This one is incorrect today
However, the pywbemcli shell will prompt for a password only once during its
invocation, while the standalone command will prompt for a password every time
it is executed
.
See also `Environment variables and avoiding password prompts`_.

The internal commands ``:?``, ``:h``, or ``:help`` display general help
information for external and internal commands::

    > :help
    REPL help:

      External Commands:
        prefix external commands with "!"

      Internal Commands:
        prefix internal commands with ":"
        :?, :h, :help     displays general help information
        :exit, :q, :quit  exits the repl

In this help text, "REPL" stands for "Read-Execute-Print-Loop" which is a
term that denotes the approach used in the pywbemcli shell.

In addition to using one of the internal shell commands shown in the help text
above, you can also exit the pywbemcli shell by typing `Ctrl-D`.

Typing ``--help`` in the pywbemcli shell displays general help information for the
pywbemcli commands, which includes global options and a list of the supported
commands::

    > --help
    Usage: pywbemcli  [GENERAL-OPTIONS] COMMAND [ARGS]...

      Command line browser for WBEM Servers. This cli tool implements the
      CIM/XML client APIs as defined in pywbem to make requests to a WBEM
      server.

      The options shown above that can also be specified on any of the
      (sub-)commands.

    Options:
      -s, --server TEXT               Hostname or IP address of the WBEMServer
                                      (Default: PYWBEMCLI_SERVER environment
                                      variable).
      -d, --default_namespace TEXT    Default Namespace to use in the target
                                      WBEMServer if no namespace is defined in the
                                      subcommand(Default: PYWBEMCLI_NAMESPACE
                                      environment variable or pywbemcli default
                                      TODO).
      -u, --user TEXT                 Username for the WBEM Server (Default:
                                      PYWBEMCLI_USER environment variable).
      -p, --password TEXT             Password for the WBEM Server (Default:
                                      PYWBEMCLI_PASSWORD environment variable).
      -t, --timeout TEXT              Operation timeout for the WBEM Server
                                      (Default: PYWBEMCLI_TIMEOUT environment
                                      variable).
      -n, --noverify                  If set, client does not verify server
                                      certificate.
      -k, --certfile TEXT             Server certfile. Not used if noverify
                                      set(Default: PYWBEMCLI_KEYFILE environment
                                      variable).
      -k, --keyfile TEXT              Client private key file(Default:
                                      PYWBEMCLI_KEYFILE environment variable).
      -o, --output-format [mof|xml|table|csv|text]
                                      Output format (Default: mof).
      --use-pull_ops [yes|no|either]  Determines whether the pull operations are
                                      used forthe EnumerateInstances,
                                      associatorinstances,referenceinstances, and
                                      ExecQuery operations. yes means that pull
                                      will be used and if the server does not
                                      support pull, the operation will fail. No
                                      choice forces pywbemcli to try only the
                                      traditional non-pull operations. either
                                      allows pywbem to try both pull and then
                                      traditional operations. This choice is
                                      acomplished by using the Iter... operations
                                      as the underlying pywbem api call.  The
                                      default is either.
      --pull-max-cnt INTEGER          MaxObjectCount of objects to be returned if
                                      pull operations are used. This must be  a
                                      positive non-zero integer. Default is 1000.
      -v, --verbose                   Display extra information about the
                                      processing.
      --version                       Show the version of this command and exit.
      --help                          Show this message and exit.

    Commands:
      class      Command group to manage CIM Classes.
      instance   Command Group to manage CIM instances.
      qualifier  Command Group to manage CIM...
      repl       Start an interactive shell.
      server     Command group for server operations

The usage line in this help text show the standalone command use. Within the
pywbemcli shell, the ``pywbemcli`` word is ommitted and the remainder is typed in.

Typing ``COMMAND --help`` in the pywbemcli shell displays help information for the
specified pywbemcli command, for example::

    > c --help
    Usage: pywbemcli  class [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group to manage CIM Classes.

    Options:
      --help  Show this message and exit.

    Commands:
      associators   Get the associated classes for the CLASSNAME...
      enumerate     Enumerate classes from the WBEMServer...
      find          Find all classes that match the CLASSNAME...
      get           get and display a single class from the WBEM...
      hierarchy     Display classnames inheritance hierarchy as a...
      invokemethod  Invoke the class method named methodname in...
      names         get and display a list of classnames from the...
      references    Get the reference classes for the CLASSNAME...

The pywbemcli shell supports popup help text while typing, where the valid choices
are shown based upon what was typed so far, and where an item from the popup
list can be picked with <TAB> or with the cursor keys. In the following
examples, an underscore ``_`` is shown as the cursor::

    > --_
      class      Command group to manage CIM Classes.
      instance   Command Group to manage CIM instances.
      qualifier  Command Group to manage CIM...
      repl       Start an interactive shell.
      server     Command group for server operations
    > c_
      class      Command group to manage CIM Classes.

The pywbemcli shell supports history (within one invocation of the shell, not
persisted across pywbemcli shell invocations).

.. _`Command mode`:

Command mode
------------

In command mode, the ``pywbemcli`` command performs its task and terminates,
like any other standalone non-interactive command.

This mode is used when the ``pywbemcli`` command is invoked with a (sub-)command::

    $ pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS...] [COMMAND-OPTIONS]

Examples::

    $ pywbemcli -s http://localhost -n root/cimv2 -u username class get
    Enter password: <password>
    . . . <TODO>

TODO: Need to sort this one out
In command mode, bash tab completion is also supported, but must be enabled
first as follows (in a bash shell)::

    $ eval "$(_PYWBEMCLI_COMPLETE=source pywbemcli)"

Bash tab completion for ``pywbemcli`` is used like any other bash tab completion::

    $ pywbemcli --<TAB><TAB>
    ... <shows the global options to select from>

    $ pywbemcli <TAB><TAB>
    ... <shows the commands to select from>

    $ pywbemcli class <TAB><TAB>
    ... <shows the class sub-commands to select from>

.. _`Environment variables and avoiding password prompts`:

Environment variables and avoiding password prompts
---------------------------------------------------

The pywbemcli CLI has  environment variable options corresponding to the
command line options for specifying the general options to be used including:

* PYWBEMCLI_SERVER - Corresponds to the general input option --server
* PYWBEM_CLI_DEFAULT_NAMESPACE - Corresponds to the general input option  --namespace
* PYWBEMCLI_USER - Corresponds to the general input option --user
* PYWBEMCLI_PASSWORD - Corresponds to the general input option --password
* PYWBEWCLI_NOVERIFY - Corresponds to the general input option -noverify
* PYWBEMCLI_CERTFILE - Corresponds to the general input option --cerrtfile
* PYWBEMCLI_KEYFILE - Corresponds to the general input option --keyfile
* PYWBEMCLI_KEYFILE - Corresponds to the general input option --cacerts
* PYWBEMCLI_USE_PULL - corresponds to the general input option --use_pull_ops
* PYWBEMCLI_PULL_MAX_CNT - corresponds to the general input option --max_object_cnt
* PYWBEMCLI_LOG - corresponds to the general input option --log

If these environment variables are set, the corresponding general option on the
command line is not required and the value of the environment variable is
used.

Thus, in the following example, the second line accesses the server
http://localhost::

      $ export PYWBEMCLI_SERVER=http://localhost
      $ pywbemcli class get CIM_Managed element

If the WBEM operations performed by a particular pywbemcli command require a
password, the password is prompted for if the --user option is set (in both
modes of operation) and the --pasword option is not set::

      $ pywbemcli -s http://localhost -n root/cimv2 -u user class get
      Enter password: <password>
      . . . <The display output from get class>

If both the --user and --password options are set, the command is executed
without a password prompt::

      $ pywbemcli -s http://localhost -n root/cimv2 -u user -p blah class get
      . . . <The display output from get class>

If the operations performed by a particular pywbemcli command do not
require a password or no user is supplied, no password is prompted for::

      $ pywbemcli --help
      . . . <help output>

For script integration, it is important to have a way to avoid the interactive
password prompt. This can be done by storing the password string in an
environment variable or entering it on the command line.


The ``pywbemcli`` command supports a ``connection export`` (sub-)command that
outputs the (bash) shell commands to set all needed environment variables::

      $ pywbemcli -s http://localhost -n root/cimv2 -u fred
      Enter password: <password>
      export PYWBEMCLI_SERVER=http://localhost
      export PYWBEMCLI_NAMESPACE=root/cimv2


This ability can be used to set those environment variables and thus to persist
the connection name in the shell environment, from where it will be used in
any subsequent pywbemcli commands::

      $ eval $(pywbemcli -s http://localhost -u username -n namespace)
      Enter password: <password>

      $ env |grep PYWBEMCLI
      export PYWBEMCLI_SERVER=http://localhost
      export PYWBEMCLI_NAMESPACE=root/cimv2

      $ pywbemcli instance server namespaces
      . . . <list of namespaces for the defined server>

The password is only prompted for when creating the connection, and the
connection info stored in the shell environment is utilized in the
``pywbemcli instance server namespaces`` command, avoiding
another password prompt.

.. _`pywbemcli defined logging`:

Pywbemcli defined logging
-------------------------

`pywbemccli` provides for logging to either a file or the standard error stream
of information passing between the pywbemcli client and a WBEM server using the
standard PYTHON logging facility.

Logging is configured and enabled using the `--log` global option on the
commmand line or the `PYWBEMCLI_LOG` environment variable.

`pywbemcli` provides logging of operations between the pywbemcli client and
a WBEM server, allowing logging of either the operation calls that send
requests to a WBEM server and their responses or the HTTP messages between
the pywbemcli client and the WBEM server.

The default is no logging if the `--logging` option is not specified with a
configuration string.

The general format of the `--log` option is a string with up to 3 fields
(COMPONENT, DESTINATION, DETAIL):

    LOG_CONFIG_STRING := CONFIG[,CONFIG]
    CONFIG := COMPONENT"="[DESTINATION[":"DETAIL]
    COMPONENT := ('all' / 'api' / 'http')
    DESTINATION := ('stderr' / 'file')
    DETAIL := ('all'/ 'path'/ 'summary')

For example::

      $ pywbemcli --log api=file:summary,http=stderr

The COMPONENT field defines the component for which logging is enabled:

  * `api` - Logs the calls to the pywbem methods that make requests to a
    WBEM Server. This logs both the requests and response including any
    exceptions generated by error responses from the WBEM server.

  * `http` - Logs the headers and data for HTTP requests and responses to the
     WBEM server.

  * `all` - (Default) Logs both the `api` and `http` components.

The DESTINATION field specified the log destination:
  * `stderr` - Log to stderr

  * 'file' - (default) Log to the predefined pywbemcli file

The DETAIL component of the log configuration string defines the level of
logging information for the api and http components.  Because enormous quantities
of information can be generated this option exists to limit the amount of
information generated. The possible keywords are:

  * `all` - (Default) Logs the full request including all input parameters and the
    complete response including all data. Exceptions are fully logged.

  * `paths` - Logs the full request but only the path component of the
    `api` responses. This reduces the data included in the responses.
    Exceptions are fully logged.

  * `summary` - Logs only the requests but only the count of objects receied
    in the response.  Exceptions are fully logged.
