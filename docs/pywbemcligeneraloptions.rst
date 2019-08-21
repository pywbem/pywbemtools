.. _`Pywbemcli command line general options`:

Pywbemcli command line general options
======================================

The pywbemcli command line options are as follows (See the help in
pywbemcli and section :ref:`pywbemcli Help Command Details` for more precise
information on each command-group arguments and options):

* **--server/-s** - Host name or IP address of the WBEM server to which
  pywbemcli will connect in the format::

    [{scheme}://]{host}[:{port}]

  Where:

  * Scheme: must be "https" or "http" [Default: "https"].
  * Host: defines short/fully qualified DNS hostname, literal
    IPV4 address (dotted), or literal IPV6 address. see :term:`RFC3986` and
    :term:`RFC6874`
  * Port: (optional) defines WBEM server port to be used [Default: 5988(HTTP)
    and 5989(HTTPS)]..

  This option is mutually exclusive with the ``--name`` option and the
  ``--mock-server`` option since each defines a connection to a WBEM server.

  In the interactive mode this connection is not actually executed until a
  command or subcommand requiring access to the WBEM server is entered.
  (EnvVar: PYWBEMCLI_SERVER)
* **--name/-n** - The name of a WBEM server that is defined in the
  :term:`connection file`.  The server parameters for this connection name will
  be loaded from the :term:`connections file` to become the current WBEM
  connection in pywbemcli. Note: In the interactive mode a connection is not
  actually used until a command requiring access to the WBEM server is entered.
  This option is mutually exclusive with ``--server`` and ``--mock-server``
  since each option defines a WBEM server for pywbemcli.

  A new WBEM server (``myserver``) may be defined and saved in the connection
  file with a name defined as follows::

    $ pywbemcli add -s http://localhost --name myserver --user user --password password

  To use an existing WBEM server named ``myserver`` in the defined connections::

    $ pywbemcli --name myserver class get CIM_ManagedElement

  See :ref:`Connection command-group` for more information on managing
  connections.

* **--default-namespace/-d** - Default :term:`CIM namespace` to use in the target
  WBEM server if no namespace is defined in a command. If not defined the
  pywbemcli default is ``root/cimv2``.  This is the namespace used on all
  server operation requests unless a specific namespace is defined by:

  * In the interactive mode prepending the command-group name with the
    ``--namespace`` option.
  * Using the ``--namespace`` or ``-n`` command option to define a namespace
    on subcommands that specify this option.
  * Executing a command that looks in multiple namespaces (ex. ``class find``).
* **--user/-u** - User name for the WBEM server if a user name is required to
  authenticate the client.
* **--password/-p** - Password for the WBEM server. This option is normally
  required if the ``--user`` option is defined.  If the user does not enter a
  password when ``--user`` - is set, pywbemcli will prompt for the password.
  See :ref:`Avoiding password prompts`.
* **--noverify/-n** - If set, client does not verify server certificate. Any
  certificate returned by the server is accepted.
* **--certfile** - Server certificate file. Not used if ``--no-verify`` set or
  the connection does not use SSL (i.e. ``--server http://blah``)
* **--keyfile** - Client private key file for the server to use to authenticate
  the client if that is required by the WBEM server.
* **--output-format/-o** - Output format choice (Default: mof).
  Note that the actual output format may differ from this value because some
  subcommands only allow selected formats. Thus, for example, the
  ``class tree`` always displays as an ascii tree. See :ref:`Output formats`.
* **--use-pull-ops** [ ``yes`` | ``no`` | ``either`` ] - Determines whether the
  pull operations are used for ``EnumerateInstances``, ``AssociatorInstances``,
  ``ReferenceInstances``, and ``ExecQuery`` operations See :ref:`Pywbemcli and
  the DMTF pull operations` for more information on pull operations:

  * ``yes`` -  pull requests will be used and if the server does not
     support pull, the operation will fail.
  * ``no`` - forces pywbemcli to try only the traditional non-pull operations.
  * ``either`` - (default )allows pywbem to try both pull and then traditional
      operations.

* **--pull-max-cnt** -  ``MaxObjectCount`` of objects to be returned for each
  pull request if pull operations are used. This must be  a positive non-zero
  integer. Default is 1000. See :ref:`Pywbemcli and the DMTF pull operations`
  for more information on pull operations.

* **--mock-server** - Defines one or more files that define a mock server that
  can be used to define a mock WBEM server in the pywbemcli process so that
  pywbemcli commands without access to a real server. When this option is used
  to define a WBEM server the security options (ex. ``--user``) are irrevalent;
  they may be included but are not used.

  The following example creates a mock server with two files defining the
  mock data, shows what parameters are defined for the connection, and then
  saves that connection named ``mymockserver``:

  .. code-block:: text

      $ pywbemcli --mock-server classdefs.mof --mock-server insts.py --default-namespace root/myhome
      pywbemcli> connection show
        Name: default
          WBEMServer uri: None
          Default-namespace: root/myhome
          . . .
          use-pull-ops: either
          pull-max-cnt: 1000
          mock: classdefs.mof, insts.py
          log: None
      pywbecli> connection save --name mymockserver

  See chapter :ref:`Mock WBEM server support` for more information on defining
  mock servers.
* **--log/-l** - See :ref:`Pywbemcli defined logging`.
* **--verbose/-v** -  Display extra information about the processing.
* **--version** - Show the version of this command and of the pywbem package
      imported then exit.
* **--help/-h** - Show the help which describes the command line options and
      exit.


.. _`Environment variables for general options`:`:

Environment variables for general options
-----------------------------------------

Pywbemcli has environment variable options corresponding to the
command line general options as follows:

==============================  ============================
Environment variable            Corresponding general option
==============================  ============================
PYWBEMCLI_SERVER                ``--server``
PYWBEMCLI_NAME                  ``--name``
PYWBEMCLI_USER                  ``--user``
PYWBEMCLI_PASSWORD              ``--password``
PYWBEMCLI_OUTPUT_FORMAT         ``--output-format``
PYWBEMCLI_DEFAULT_NAMESPACE     ``--default-namespace``
PYWBEMCLI_TIMEOUT               ``--timeout``
PYWBEMCLI_KEYFILE               ``--keyfile``
PYWBEMCLI_CERTFILE              ``--certfile``
PYWBEWCLI_CACERTS               ``--ca_certs``
PYWBEMCLI_USE_PULL              ``--use_pull_ops``
PYWBEMCLI_PULL_MAX_CNT          ``--pull-max-cnt``
PYWBEMCLI_STATS_ENABLED         ``--timestats``
PYWBEMCLI_MOCK_SERVER           ``--mock-server``
PYWBEMCLI_LOG                   ``--log``
==============================  ============================

If these environment variables are set, the corresponding general options on the
command line are not required and the value of the environment variable is
used. Environment variable options are not provided for command/subcommand
options or arguments.

In the following example, the second line accesses the server
``http://localhost`` defined by the export command:

.. code-block:: text

      $ export PYWBEMCLI_SERVER=http://localhost
      $ pywbemcli class get CIM_ManagedElement


.. _`Avoiding password prompts`:

Avoiding password prompts
-------------------------

If the WBEM operations performed by a particular pywbemcli command require a
password, the password is prompted for if the ``--user`` option is set (in both
modes of operation) and the ``--password`` option is not set:

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

For a description of the commands and command-groups supported by pywbemcli,
see section :ref:`Pywbemcli command groups, commands, and subcommands` and
section:ref:`pywbemcli Help Command Details`. For example:

.. code-block:: text

    $ pywbemcli --help
    . . . <general help, listing the general options and possible commands>

    $ pywbemcli class --help
    . . . <help for class command-group, listing its subcommands, arguments and
          command-specific options>

Note that the help text for any pywbemcli command-group (such as ``class``) will
not show the general options again.

The general options (listed by ``pywbemcli --help``) can still be specified
together with (sub-)commands even though they are not listed in their help
text, but they must be specified before the (sub-)command, and any
command-specific options (listed by ``pywbemcli COMMAND --help``) must be
specified after the (sub-)command, as shown here:

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
sequence of ``OpenEnumerateInstances``/``PullInstances``).

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
    query language query (``--FilterQueryLanguage`` and ``--FilterQuery``) option which
    passes a filter query to the WBEM server so that it filters the responses
    before they are returned. This can greatly reduce the size of the responses
    if effectively used but is used only when the pull operations are available
    on the server and used with pywbemcli.

  * The pull operations do not support some of the options that traditional
    operations did including:

    * ``IncludeQualifiers`` - Since even the traditional operations specification
      deprecated this option and the user cannot depend on it being honored,
      the most logical solution is to never use this option.

    * ``LocalOnly`` - Since even the traditional operations specification deprecated
      this options and the user cannot depend on it being honored by the
      WBEM server the most logical soltuion is to never use this option


.. _`Output formats`:

Output formats
--------------

Pywbemcli supports various output formats for the results. The output format
can be selected with the ``-o``\``--output-format`` option.

The output formats fall into three groups however, not all formats are
applicable to all subcommands:

* **Table output formats** - There are a variety of table formats:ref:`Table formats`.
* **CIM model formats** - These formats provide display of returned CIM objects in
  formats that are specific to the CIM Model (ex. MOF, XML, etc.).
  See :ref:`CIM object formats`.
* **ASCII tree format** - This format option provides a tree display of outputs that
  are logical to display as a tree.  Thus, the command ``pywbemcli class tree . . .``
  which shows the hierarchy of the CIM classes defined by a WBEM server uses the
  tree output format. See :ref:`ASCII tree format`.


.. _`Table formats`:

Table formats
^^^^^^^^^^^^^

The different variations of the table format define different
formatting of the borders for tables or different output formats such as HTML.
The following are examples of the table formats with a single command ``class
find CIM_Foo``:

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


* ``-o rst``: Tables in `reStructuredText`_ markup:

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

The ouput of CIM objects allows multiple formats as follows:

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
CIM objects and can be useful in understanding the pywbem interpretation of the
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
class class hierarchy tree as follows:

.. code-block:: text

  $pywbemcli -m tests/unit/simple_mock_model.mof class tree

  root
  +-- CIM_Foo
      +-- CIM_Foo_sub
      |   +-- CIM_Foo_sub_sub
      +-- CIM_Foo_sub2

This shows a very simple mock repository with 4 classes where CIM_Foo is the
top level in the hierarchy, CIM_Foo_sub and CIM_Foo_sub2 are its subclasses, and
CIM_Foo_sub_sub is the subclass of CIM_Foo_sub


.. _`Pywbemcli defined logging`:

Pywbemcli defined logging
-------------------------

Pywbemcli provides for logging to either a file or the standard error stream
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

For example the following log configuration string logs only the pywbem API
calls and responses summary information to a file and the HTTP requests and
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

  * `stderr` - Output log to stderr.
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

For example, logging only of the summary  API information would look something
like dthe following:

.. code-block:: text

    $ pywbemcli -s http://localhost -u blah -p pw -l api=file:summary class enumerate -o

produces log output for the class enumerate operation in the log file
pywbemcli.log as follows showing the input parameters to the pywbem method
``EnumerateClassName`` and the number of objects in the response:

.. code-block:: text

    2019-07-09 18:27:22,103-pywbem.api.1-27716-Request:1-27716 EnumerateClassNames(ClassName=None, DeepInheritance=False, namespace=None)
    2019-07-09 18:27:22,142-pywbem.api.1-27716-Return:1-27716 EnumerateClassNames(list of str; count=103)

The format is::

.. code-block:: text

    <Date time>-<Component>.<ref:`connection id`>-<Direction>:<connection id> <PywbemOperation>(<data>)


.. _`Pywbemcli connections file`:

Pywbemcli connections file
--------------------------

Pywbemcli provides the capability to save the definition of parameters
for connecting to WBEM servers identified by name using the ``connection``
command-group (see :ref:`pywbemcli connection --help` and
:ref:`Connection command-group`). Once defined, these named connections are
saved in a a JSON formatted file(see :term:`connections file`) in the current
directory from which pywbemcli was executed.

To create a new persistent connection definition, pywbemcli should be executed
with either the ``--server``, or the ``--mock-server`` option, and the
``--name`` option and any other general options/arguments desired for the
connection.  Then executing the ``connection save`` command will save the new
connection in the connections file. For example the following example creates a
new connection in the interactive mode:

.. code-block:: text

    $ pywbemcli --server http://localhost --user usr1 -password blah --name testconn
    pywbemcli> connection list
    Name: testconn
      WBEMServer uri: http://localhost
      Default_namespace: root/cimv2
      User: usr1
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

.. code-block:: text

    pywbemcli> connection add Ronald http://blah2 -u you -p xxx
    pywbemcli> connection list
    WBEMServer Connections:
    name      server uri        namespace    user         password      timeout  noverify
    --------  ----------------  -----------  -----------  ----------  ---------  ----------
    Ronald    http://blah2      root/cimv2   you          xxx                    False
    testconn  http://localhost  root/blah    kschopmeyer  test8play          30  False

Connections can be deleted with the ``connection delete`` command either with
the command argument containing the connection name or with no name provided so
pywbemcli presents a list of connections:

.. code-block:: text

    $ pywbemcli connection delete Ronald

or:

.. code-block:: text

    $ pywbemcli connection delete
    Select a connection or CTRL_C to abort.
    0: Ronald
    1: testconn
    Input integer between 0 and 1 or Ctrl-C to exit selection: 0
    $
