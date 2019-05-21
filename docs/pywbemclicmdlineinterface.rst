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

Pywbemcli provides a command line interface(CLI) interaction with WBEM servers.

The command line  can contain the following components::

* general-options - see :ref:`Command line general options`

* command-group - A name of a group of subcommands

* command - Alternative to command-group when there are no
  subcommands.

* subcommand - Command name within a command group

* args - Arguments and options that are defined for a particular
  command or subcommand.

The syntax is:

.. code-block:: text

    pywbemcli <general-options> <command-group>|<command> <args>

    where:
        command-group = <command> <subcommand>

A command-group is the name of an object, referencing an entity (ex. class
refers to operation on CIM classes). The subcommands are generally actions on
the objects defined by the command-group name. Thus ``class`` is a
command-group name used to access CIM classes and ``get`` is a subcommand so::

    $ pywbemcli --output-format mof class get CIM_ManagedElement --namespace interop

Defines a command to get the class `CIM_ManagedElement` from the current
target server in the namespace `interop` and display it in the
``mof`` output-format.

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

In interactive mode, an interactive shell environment is brought up that allows
typing pywbemcli commands, internal commands (for operating the pywbemcli
shell), and external commands (that are executed in the standard shell for the
user).

This pywbemcli shell is started when the ``pywbemcli`` command is invoked
without specifying any command-group or command:

.. code-block:: text

    $ pywbemcli [GENERAL-OPTIONS]
    pywbemcli> _

Alternatively, the pywbemcl shell can also be started by specifying the ``repl``
command:

.. code-block:: text

    $ pywbemcli [GENERAL-OPTIONS] repl
    pywbemcli> _

The pywbemcli shell uses the prompt ``pywbemcli> ``, The cursor is shown in
the examples above as an underscore ``_``.

General options are specified on the pywbemcli command; they serve
as the parameters for the connection to a WBEM server and values for the
pywbemcli commands and arguments that can be typed in the pywbemcli shell.

The pywbemcli commands that can be typed in the pywbemcli shell are the
command or command-group that would follow the ``pywbemcli`` command and
general options when used in `command mode`_. The following example
starts a pywbemcli shell in interactive mode and executes serveral commands
(ex. `class enumerate -o`).

.. code-block:: text

    $ pywbemcli -s http://localhost -d root/cimv2 -u username
    pywbemcli shell uses the >> class enumerate -o
    . . . <Enumeration of the names of classes in the defined namespace>
    pywbemcli shell uses the >> class get CIM_System
    . . . <MOF output of the class CIM_System from the WBEM server>
    pywbemcli shell uses the >> :q

The pywbemcli shell command ``class get CIM_System`` in the example
above has the same effect as the standalone command:

.. code-block:: text

    $ pywbemcli -s http://localhost -u username class get CIM_System
    . . . <MOF formated display of the CIM_System class>

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
        :exit, :q, :quit  exits the repl

In this help text, "REPL" stands for "Read-Execute-Print-Loop" which is a
term that denotes the pywbemcli shell interactive mode.

In addition to using one of the internal shell commands shown in the help text
above, you can also exit the pywbemcli shell by typing `Ctrl-D`. Note that the
pywbemshell exit command may vary by operating system

Typing ``--help`` or ``-h`` in the pywbemcli shell displays general help
information for the pywbemcli commands, which includes general options and a
list of the supported commands.

.. code-block:: text

    $ pywbemcli --help

    Pywbemcli is a command line WBEM client that uses the DMTF CIM/XML
    protocol to communicate with WBEM servers. Pywbemcli can:

    . . .

    For more detailed information, see:

      https://pywbemtools.readthedocs.io/en/latest/

    Options:
      -s, --server URI                Hostname or IP address of the WBEMServer
                                      (Default: PYWBEMCLI_SERVER environment
                                      variable).
      -d, --default_namespace TEXT    Default Namespace to use in the target
                                      WBEMServer if no namespace is defined in the
                                      subcommand(Default: PYWBEMCLI_NAMESPACE
                                      environment variable or pywbemcli default.

      . . .

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

The usage line in this help text shows the standalone command use. Within the
pywbemcli shell (interactive mode), the ``pywbemcli`` word is omitted and the
subcommand and options is typed in.

Typing ``COMMAND --help``  or ``COMMAND -h`` in the pywbemcli shell displays
help information for the specified pywbemcli command, for example:

.. code-block:: text

    pywbemcli> class --help
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

The pywbemcli shell command in the interactive mode supports popup help text
while typing, where the valid choices are shown based upon what was typed so
far, and where an item from the popup list can be picked with <TAB> or with the
cursor keys. It can be used to select from the list of general options. In the
following examples, an underscore ``_`` is shown as the cursor:

.. code-block:: text

    pywbemcli shell uses the >> --_
     --server             Hostname or IP address with scheme of the WBEMServer ...
     --name               Name for the connection(optional, see --server).  If ...
     --default_namespace  Default Namespace to use in the target WBEMServer if ...

    pywbemcli shell uses the >> cl_
      class      Command group to manage CIM Classes.

The pywbemcli shell supports history across multiple invocations of the shell
using <up-arrow, down-arrow>.

.. _`Command mode`:

Command mode
------------

In command mode, the pywbemcli command performs its task and terminates,
like any other standalone non-interactive command.

This mode is used when the pywbemcli command is invoked with a command or
command group name:

.. code-block:: text

    $ pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS...] [COMMAND-OPTIONS]

Examples:

.. code-block:: text

    $ pywbemcli -s http://localhost -d root/cimv2 -u username class get
    Enter password: <password>
    . . .

In command mode, tab completion is also supported for some shells, but must be
enabled specifically for each shell.

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
    ... <shows the class sub-commands to select from>

.. _`Command line general options`:

Command line general options
----------------------------

The general options are entered before the command-group or command. For
example the following enumerates the qualifier declarations and outputs the
result as a table:

.. code-block:: text

    pywbemcli --output simple qualifier enumerate

    or

    pywbemcli -o simple qualifier enumerate

In the interactive mode, the general options are defined once and retain their
value through the execution of the interactive mode.

However, they may be modified in the interactive mode by entering them before
the COMMAND.  Thus, for example to display the qualifier declarations in
interactive mode and as a table:

.. code-block:: text

   $ pywbemcli

   pywbemcli> -o table qualifier enumerate

    Qualifier Declarations
    +-------------+---------+---------+---------+-----------+-----------------+
    | Name        | Type    | Value   | Array   | Scopes    | Flavors         |
    +=============+=========+=========+=========+===========+=================+
    | Description | string  |         | False   | ANY       | EnableOverride  |
    |             |         |         |         |           | ToSubclass      |
    |             |         |         |         |           | Translatable    |
    +-------------+---------+---------+---------+-----------+-----------------+
    | Key         | boolean | False   | False   | PROPERTY  | DisableOverride |
    |             |         |         |         | REFERENCE | ToSubclass      |
    +-------------+---------+---------+---------+-----------+-----------------+

   pywbemcli>

**Note:** - With this use of the general options as part of an interactive mode
command, the options redefinitions are not retained between command executions.

.. _`Pywbemcli command line general options`:

Pywbemcli command line general options
--------------------------------------

The pywbemcli command line options are as follows (See the help in
pywbemcli and section :ref:`pywbemcli Help Command Details` for more precise
information on each command group arguments and options):

* ``--server`` Host name or IP address of the WBEMServer to which
  pywbemcli will connect in the format::

    [{scheme}://]{host}[:{port}]

  Where:

  * Scheme: must be "https" or "http" [Default: "https"].
  * Host: defines short/fully qualified DNS hostname, literal
    IPV4 address (dotted), or literal IPV6 address. see :term:`RFC3986` and
    :term:`RFC6874`
  * Port: (optional) defines WBEM server port to be used [Defaults: 5988(HTTP)
    and 5989(HTTPS)]. (EnvVar: PYWBEMCLI_SERVER).

  The server parameter is conditionally optional (see ``--name``). If the
  ``--name`` option exists and there is a server with the name defined by
  ``--name`` defined in the :term:`connections file` the parameters of that
  name are used for the connection.

  In the interactive mode this connection is not actually executed until a
  COMMAND is entered.
* ``--name`` - The name of a WBEMServer that is defined in the connection
  file or to define a name for a connection that will be entered in the connection
  file if the ``--server`` parameter exists.  The server parameters for this
  connection will be set in pywbemcli.
  In the interactive mode this connection is not actually used until
  a COMMAND is entered.

  A new server (``myserver``)may be defined in the connection file with a
  name is defined as follows::

    $ pywbemcli -s http://localhost -N myserver -u user -p password connection save

  To use an existing server named ``myserver`` in the defined connections:

    $ pywbemcli --name myserver  class get CIM_ManagedElement

  See :ref:`Connection command group` for more information on managing
  connections.

* ``--default_namespace`` - Default namespace to use in the target
   WBEM server if no namespace is defined in a command. If not defined the
   pywbemcli default is ``root/cimv2``.  This is the namespace used on all
   requests unless a specific namespace is defined by:

   * In the interactive mode prepending the command group name with the
     ``--namespace`` option.
   * Using the ``--namespace`` or ``-n`` command option to define a namespace
     on commands that specify this option.
   * Executing a command that looks in multiple namespaces (ex. ``class find``).
* ``--user`` - Username for the WBEM server if a user name is required to
  authenticate the client.
* ``--password`` - Password for the WBEM server. This option is normally
  required if the ``--pasword`` is used.  If the user does not enter a password
  when ``--user`` is set, pywbemcli will prompt for the password.
  See :ref:``Environment variables and avoiding password prompts``
* ``--noverify`` - If set, client does not verify server certificate. Any
  certificate returned by the server is accepted.
* ``--certfile`` Server certificate file. Not used if ``--noverify`` set or
  the connection does not use SSL (i.e. http)
* ``--keyfile`` - Client private key file
* ``--output-format`` Output format choice (Default: mof).
  Note that the actual output format may differ because some results only allow
  selected formats. See :ref:`Output formats`.
* ``--use-pull_ops`` [``yes``|``no``|``either``] - Determines whether the pull operations are
  used for EnumerateInstances, AssociatorInstances, ReferenceInstances, and
  ExecQuery operations See :ref:`Pywbemcli and the DMTF pull operations`
  for more information on pull operations:

  * ``yes`` means that pull requests will be used and if the server does not
     support pull, the operation will fail.
  * ``no`` forces pywbemcli to try only the traditional non-pull operations.
  * ``either`` allows pywbem to try both pull and then traditional operations.
    The default is ``either``.

* ``--pull-max-cnt``  MaxObjectCount of objects to be returned if
  pull operations are used. This must be  a positive non-zero integer. Default
  is 1000. See :ref:`Pywbemcli and the DMTF pull operations` for more
  information on pull operations.

* ``--log`` - See:ref:`Pywbemcli defined logging`.
* ``--verbose``  Display extra information about the processing.
* ``--version`` Show the version of this command and of the pywbem package
      imported then exit.
* ``--help`` Show the help which describes the command line options and exit.


.. _`Environment variables and avoiding password prompts`:

Environment variables and avoiding password prompts
---------------------------------------------------

Pywbemcli has environment variable options corresponding to the
command line general options as follows:

==============================  ============================
Export Name                     Corresponding general option
==============================  ============================
PYWBEMCLI_SERVER                ``--server``
PYWBEMCLI_NAME                  ``--name``
PYWBEMCLI_USER                  ``--user``
PYWBEMCLI_PASSWORD              ``--password``
PYWBEMCLI_DEFAULT_NAMESPACE     ``--namespace``
PYWBEMCLI_TIMEOUT               ``--timeout``
PYWBEMCLI_KEYFILE               ``--keyfile``
PYWBEMCLI_CERTFILE              ``--cerrtfile``
PYWBEWCLI_CACERTS               ``--cacerts``
PYWBEMCLI_USE_PULL              ``--use_pull_ops``
PYWBEMCLI_PULL_MAX_CNT          ``--max_object_cnt``
PYWBEMCLI_STATS_ENABLED         ``--stats_enabled``
PYWBEMCLI_MOCK_SERVER           ``--mock_server``
PYWBEMCLI_LOG                   ``--log``
==============================  ============================

If these environment variables are set, the corresponding general options on the
command line are not required and the value of the environment variable is
used.

Thus, in the following example, the second line accesses the server
``http://localhost``:

.. code-block:: text

      $ export PYWBEMCLI_SERVER=http://localhost
      $ pywbemcli class get CIM_ManagedElement

If the WBEM operations performed by a particular pywbemcli command require a
password, the password is prompted for if the ``--user`` option is set (in both
modes of operation) and the ``--pasword`` option is not set:

.. code-block:: text

      $ pywbemcli -s http://localhost -d root/cimv2 -u user class get
      Enter password: <password>
      . . . <The display output from get class>

If both the ``--user`` and ``--password`` options are set, the command is executed
without a password prompt:

.. code-block:: text

      $ pywbemcli -s http://localhost -d root/cimv2 -u user -p blah class get
      . . . <The display output from get class>

If the operations performed by a particular pywbemcli command do not
require a password or no user is supplied, no password is prompted for example:

.. code-block:: text

      $ pywbemcli --help
      . . . <help output>

For script integration, it is important to have a way to avoid the interactive
password prompt. This can be done by storing the password string in an
environment variable or specifying it on the command line.

The ``pywbemcli`` command supports a ``connection export`` (sub-)command that
outputs the (bash/windows) shell commands to set all needed environment variables:

.. code-block:: text

      $ pywbemcli -s http://localhost -d root/cimv2 -u fred connection export
      export PYWBEMCLI_SERVER=http://localhost
      export PYWBEMCLI_NAMESPACE=root/cimv2
      ...

This ability can be used to set those environment variables and thus to persist
the connection name in the shell environment, from where it will be used in
any subsequent pywbemcli commands:

.. code-block:: text

      $ eval $(pywbemcli -s http://localhost -u username -d root/cimv2)

      $ env |grep PYWBEMCLI
      export PYWBEMCLI_SERVER=http://localhost
      export PYWBEMCLI_NAMESPACE=root/cimv2

      $ pywbemcli server namespaces
      . . . <list of namespaces for the defined server>


.. _`CLI commands`:

CLI commands
------------

For a description of the commands supported by pywbemcli, see section
:ref:`Pywbemcli command groups, comands and subcommands` and
section:ref:`pywbemcli Help Command Details`. For example:

.. code-block:: text

    $ pywbemcli --help
    . . . <general help, listing the general options and possible commands>

    $ pywbemcli class --help
    . . . <help for cpc command, listing its subcommands, arguments and
          command-specific options>

Note that the help text for any pywbemcl command group (such as ``class``) will
not show the general options again.

The general options (listed by ``pywbemcli --help``) can still be specified
together with (sub-)commands even though they are not listed in their help
text, but they must be specified before the (sub-)command, and any
command-specific options (listed by ``pywbemcli COMMAND --help``) must be
specified after the (sub-)command, like shown here:

.. code-block:: text

      $ pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS...] [COMMAND-OPTIONS]

For example:

.. code-block:: text

    $ pywbemcli -s http:/<wbemserver> --outformat xml class enumerate

    ... Displays the xml formatted output of the classes returned by
        the enumerate class subcommand


.. _`Pywbemcli and the DMTF pull operations`:

Pywbemcli and the DMTF pull operations
--------------------------------------

For DMTF CIM/XML operations that can return many objects the DMTF CIM/XML protocol
allows two variations on the enumerate operations (enumerate and an operation
sequence of OpenEnumerateInstances/PullInstances).

While the pull operation may not be supported by all WBEM servers  they can be
significantly more efficient when they are available.  Pywbem implements the
client side of these operation and pywbemcli provides for the use of these
operations through two general options:

* ``--use-pull-operations`` - This option allows the user to select from the
    the following alternatives:

    * `either` - pywbemcli first tries the pull operation and if that fails
      retries the operation with the corresponding non-pull operation. The
      result of this first operation determines whether pull or the traditional
      operation are used for any further requests during the current
      pywbem interactive session. `either` is the default.

    * ``yes`` - Forces the use of the pull operations and if those operations fail
      generates an error.

    * ``no`` - Forces the use of the non-pull operation.

* ``--pull-max-cnt`` - Sets the maximum count of objects the server is allowed
  to return for each open/pull operation. max_pull_cnt of 1000 objects is the
  default size which from experience is a logical choice.

  The one issue with using the the ``either`` choice is that there are limitations
  with the original operations that do not exist with the pull operations:

  * The original operations did not support the filtering of responses  with a
    query language query (--FilterQueryLanguage and --FilterQuery) option which
    passes a filter query to the WBEM server so that it filters the responses
    before they are returned. This can greatly reduce the size of the responses
    if effectively used but is used only when the pull operations are available
    on the server and used with pywbemcli.


.. _`Output formats`:

Output formats
--------------

Pywbemcli supports various output formats for the results. The output format
can be selected with the ``-o`` or ``--output-format`` option.

Generally the formats fall into three groups however, not all formats are
applicable sto all subcommands:

* **Table output formats** - There are a variety of table formats:ref:`Table formats`.
* **CIM model formats** - These formats provide display of returned CIM objects in
  formats that are specific to the CIM Model (ex. MOF, XML, etc.).
  see:ref:`CIM object formats`.
* **ASCII tree format** - This format option provides a tree display of outputs that
  are logical to display as a tree.  Thus, the command `pywbemcli class tree . . .`
  which shows the hiearchy of the cim classes defined by a WBEM server uses the
  tree output format. See:ref:`ASCII tree format`.


.. _`Table formats`:

Table formats
^^^^^^^^^^^^^

There different variations of the table format primarily define different
formatting of the borders for tables. The following are examples of the
table formats with a single command ``class find CIM_Foo``:

* ``-o table``: Tables with a single-line border. This is the default:

  .. code-block:: text

    Find class CIM_Foo
    +-------------+-----------------+
    | Namespace   | Classname       |
    |-------------+-----------------|
    | root/cimv2  | CIM_Foo         |
    | root/cimv2  | CIM_Foo_sub     |
    | root/cimv2  | CIM_Foo_sub2    |
    | root/cimv2  | CIM_Foo_sub_sub |
    +-------------+-----------------+


* ``-o simple``: Tables with a line between header row and data rows, but
  otherwise without borders:

  .. code-block:: text

    Instances: CIM_Foo
    InstanceID    IntegerProp
    ------------  -------------
    "CIM_Foo1"    1
    "CIM_Foo2"    2
    "CIM_Foo3"

* ``-o plain``: Tables without borders:

  .. code-block:: text

    Instances: CIM_Foo
    InstanceID    IntegerProp
    "CIM_Foo1"    1
    "CIM_Foo2"    2
    "CIM_Foo3"

* ``-o grid``: Tables without borders:

  .. code-block:: text

    Instances: CIM_Foo
    +--------------+---------------+
    | InstanceID   |   IntegerProp |
    +==============+===============+
    | "CIM_Foo1"   |             1 |
    +--------------+---------------+


* ``-o rst``: Simple tables in `reStructuredText`_ markup:

  .. code-block:: text

    Instances: CIM_Foo
    ============  =============
    InstanceID    IntegerProp
    ============  =============
    "CIM_Foo1"    1
    "CIM_Foo2"    2
    "CIM_Foo3"
    ============  =============


.. _`reStructuredText`: http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables
.. _`Mediawiki`: http://www.mediawiki.org/wiki/Help:Tables
.. _`HTML`: https://www.w3.org/TR/html401/struct/tables.html
.. _`LaTeX`: https://en.wikibooks.org/wiki/LaTeX/Tables
.. _`JSON`: http://json.org/example.html


.. _`CIM object formats`:

CIM object formats
^^^^^^^^^^^^^^^^^^

* ``-o mof``: Format for CIM classes, CIM instances, and CIM Parameters:

MOF is the format used to define the models released by the DMTF and SNIA. It
textually defines the components and structure and data of these elements:

  .. code-block:: text

    instance of CIM_Foo {
       InstanceID = "CIM_Foo1";
       IntegerProp = 1;
    };

* ``-o xml``: Alternate format for CIM classes and instances defined by DMTF.

This is the format used in the DMTF CIM/XML protocol:

  .. code-block:: text

    <VALUE.OBJECTWITHLOCALPATH>
        <LOCALINSTANCEPATH>
            <LOCALNAMESPACEPATH>
                <NAMESPACE NAME="root"/>
                <NAMESPACE NAME="cimv2"/>
            </LOCALNAMESPACEPATH>
            <INSTANCENAME CLASSNAME="CIM_Foo">
                <KEYBINDING NAME="InstanceID">
                    <KEYVALUE VALUETYPE="string">CIM_Foo1</KEYVALUE>
                </KEYBINDING>
            </INSTANCENAME>
        </LOCALINSTANCEPATH>
        <INSTANCE CLASSNAME="CIM_Foo">
            <PROPERTY NAME="InstanceID" PROPAGATED="false" TYPE="string">
                <VALUE>CIM_Foo1</VALUE>
            </PROPERTY>
            <PROPERTY NAME="IntegerProp" PROPAGATED="false" TYPE="uint32">
                <VALUE>1</VALUE>
            </PROPERTY>
        </INSTANCE>
    </VALUE.OBJECTWITHLOCALPATH>

* ``-o repr``: Python repr format of the objects.

This is the structure and data of the pywbem Python objects representing these
CIM objects and can be useful in understanding the pywbem interpetation of the
CIM objects:

  .. code-block:: text

    CIMInstance(classname='CIM_Foo', path=CIMInstanceName(classname='CIM_Foo',
        keybindings=NocaseDict({'InstanceID': 'CIM_Foo1'}), namespace='root/cimv2',
        host=None),
        properties=NocaseDict({
          'InstanceID': CIMProperty(name='InstanceID',
            value='CIM_Foo1', type='string', reference_class=None, embedded_object=None,
            is_array=False, array_size=None, class_origin=None, propagated=False,
            qualifiers=NocaseDict({})),
          'IntegerProp': CIMProperty(name='IntegerProp', value=1, type='uint32',
              reference_class=None, embedded_object=None, is_array=False,
              array_size=None, class_origin=None, propagated=False,
              qualifiers=NocaseDict({}))}), property_list=None,
              qualifiers=NocaseDict({}))

NOTE: The above is output as a single line and has been manually formatted for
this documentation.

.. _`ASCII tree format`:

ASCII tree format
^^^^^^^^^^^^^^^^^
This output format it an ASCII based output that shows the tree structure of
the results of certain subcommands.  It is used specifically to show the
class class hiearchy tree as follows:

.. code-block:: text

  $pywbemcli -m tests/unit/simple_mock_model.mof class tree

  root
  +-- CIM_Foo
      +-- CIM_Foo_sub
      |   +-- CIM_Foo_sub_sub
      +-- CIM_Foo_sub2

This shows a very simple mock repository with 4 classes where CIM_Foo is the
top level in the hiearchy, CIM_Foo_sub and CIM_Foo_sub2 are its subclasses, and
CIM_Foo_sub_sub is the subclass of CIM_Foo_sub


.. _`Pywbemcli defined logging`:

Pywbemcli defined logging
-------------------------

Pywbemccli provides for logging to either a file or the standard error stream
of information passing between the pywbemcli client and a WBEM server using the
standard Python logging facility.

Logging is configured and enabled using the ``--log`` general option on the
commmand line or the `PYWBEMCLI_LOG` environment variable.

Pywbemcli can log  operation calls that send
requests to a WBEM server and their responses or the HTTP messages between
the pywbemcli client and the WBEM server including both the pywbem APIs
and their responses and the HTTP requests and responses.

The default is no logging if the ``--log`` option is not specified with a
configuration string.

The general format of the ``--log`` option is a string with up to 3 fields
(COMPONENT, DESTINATION, DETAIL):

.. code-block:: text

    LOG_CONFIG_STRING := CONFIG[,CONFIG]
    CONFIG            := COMPONENT"="[DESTINATION[":"DETAIL]
    COMPONENT         := ('all' / 'api' / 'http')
    DESTINATION       := ('stderr' / 'file')
    DETAIL            := ('all'/ 'path'/ 'summary')

For example the following log configuration string logs only the pywbem api
calls and responses summary information to a file and the http requests and
responses to stderr:

.. code-block:: text

      $ pywbemcli --log api=file:summary,http=stderr

The COMPONENT field defines the component for which logging is enabled:

  * `api` - Logs the calls to the pywbem methods that make requests to a
    WBEM server. This logs both the requests and response including any
    exceptions generated by error responses from the WBEM server.
  * `http` - Logs the headers and data for HTTP requests and responses to the
     WBEM server.
  * `all` - (Default) Logs both the `api` and `http` components.

The DESTINATION field specified the log destination:

  * `stderr` - Log to stderr
  * 'file' - (default) Log to the predefined pywbemcli file. The pywbemcli
    log file is `pywbemcli.log` in the current directory.

The DETAIL component of the log configuration string defines the level of
logging information for the api and http components.  Because enormous quantities
of information can be generated this option exists to limit the amount of
information generated. The possible keywords are:

  * `all` - (Default) Logs the full request including all input parameters and
    the complete response including all data. Exceptions are fully logged.

  * `paths` - Logs the full request but only the path component of the
    `api` responses. This reduces the data included in the responses.
    Exceptions are fully logged.

  * `summary` - Logs the requests but only the count of objects received
    in the response.  Exceptions are fully logged.

The log output is routed to the output defined by DESTINATION and includes the
information determined by the COMPONENT and DETAIL fields.

For example, logging only of the summary  api information would look something
like gisthe following:

.. code-block:: text

    $ pywbemcli -s http://localhost -u blah -p pw -l api=file:summary class enumerate -o

produces log output for the class enumerate operation in the log file
pywbemcli.log as follows showing the input parameters to the pywbem method
EnumerateClassName and the number of objects in the response:

.. code-block:: text

    2019-07-09 18:27:22,103-pywbem.api.1-27716-Request:1-27716 EnumerateClassNames(ClassName=None, DeepInheritance=False, namespace=None)
    2019-07-09 18:27:22,142-pywbem.api.1-27716-Return:1-27716 EnumerateClassNames(list of str; count=103)

The format is::

    <Date time>-<Component>.<ref:`connection id`>-<Direction>:<connection id> <PywbemOperation>(<data>)


.. _`Pywbemcli connections file`:

Pywbemcli connections file
--------------------------

Pywbemcli provides the capability to persistent the definition of parameters
for connecting to WBEM servers identified by name using the ``connection``
COMMAND (see:ref:`pywbemcli connection --help`). Once defined, these named
connections are saved in a a JSON formatted file named
``pywbemcliservers.json`` in the current directory from which pywbemcli was
executed.

To create a new persistent connection, the pywbemcli should be executed with
the server option, the name option and any other general parameters desired for
the connection in the interactive mode.  Then executing the ``connection save``
COMMAND will save the new connection in the connections file. For example:

.. code-block:: text

    $ pywbemcli -s "//localhost -u me -p blah -N testconn
    pywbemcli> connection list
    Name: testconn
      WBEMServer uri: http://localhost
      Default_namespace: root/cimv2
      User: me
      Password: blah
      Timeout: 30
      Noverify: False
      Certfile: None
      Keyfile: None
      use-pull-ops: either
      pull-max-cnt: 1000
      mock:
      log: None

    pywbemcli> connection save
    pywbemcli> connection list

    name       server uri        namespace    user         password      timeout  noverify    certfile    keyfile    log
    ---------  ----------------  -----------  -----------  ----------  ---------  ----------  ----------  ---------  -----
    testconn*  http://localhost  root/blah    me           blah               30  False

Note: The * indicates that this is the current connection.

Other connections can be added from either the command mode or interactive mode.

    pywbemcli> connection add Ronald http://blah2 -u you -p xxx
    pywbemcli> connection list
    WBEMServer Connections:
    name      server uri        namespace    user         password      timeout  noverify    certfile    keyfile    log
    --------  ----------------  -----------  -----------  ----------  ---------  ----------  ----------  ---------  -----
    Ronald    http://blah2      root/cimv2   you          xxx                    False
    testconn  http://localhost  root/blah    kschopmeyer  test8play          30  False

Connections can be deleted with the ``connection delete`` command either with
the command argument containing the connection name or with no name provided so
pywbemcli presents a list of connections::

    $ pywbemcli connection delete Ronald

or::

    $ pywbemcli connection delete
    Select a connection or CTRL_C to abort.
    0: Ronald
    1: testconn
    Input integer between 0 and 1 or Ctrl-C to exit selection: 0
    $
