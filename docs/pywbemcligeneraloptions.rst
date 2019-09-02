.. _`Using the pywbemcli command line general options`:

Using the pywbemcli command line general options
================================================


.. _`Oveview of the general options`:

Overview of the general options
-------------------------------

General options define:

* The connection to the WBEM server against which the pywbemcli commands are to be
  executed (i.e url, default CIM namespace, security parameters, etc.).
  or the alternative mock of a WBEM server See :ref:`Defining the WBEM Server`
* Operation behavior of pywbemtools for requests; i.e. using the pull operations
  vs the :term:`traditional operations` and defined in
  :ref:`Pywbemcli and the DMTF pull operations`, and the client side timeout.
  See :ref:`Controlling operation behavior and monitoring operations`
* Execution options to monitor the requests and responses(statistics keeping,
  and logging of operations) and to display the results.
  See :ref:`Controlling operation behavior and monitoring operations`  and
  :ref:`Controlling result output formats`
* General options to show the pywbemtools version, and display help for any of
  the command groups or commands.

General options must be entered on the command line  before the command group
or command.

For example the following enumerates qualifier declarations and outputs the
result in the ``simple`` table format:

.. code-block:: text

    pywbemcli --output-format simple --server http://localhost qualifier enumerate

    <table of qualifier declarations>

    or

    pywbemcli -o simple --server http://localhost qualifier enumerate

    <table of qualifier declarations>

In the interactive mode, general options from the command line are defined
once and retain their value throughout the execution of the interactive mode.

However, they may be modified in the interactive mode by entering them before
the command.  Thus, for example to display the qualifier declarations in
interactive mode and as a table:

.. code-block:: text

   $ pywbemcli

   pywbemcli> --output-format table --server http://localhost qualifier enumerate

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

**Note:** - When using the general options as part of an interactive mode
command, general the options redefinition's are not retained between command
executions.


.. _`Defining the WBEM Server`:

Defining the WBEM Server
^^^^^^^^^^^^^^^^^^^^^^^^

The target WBEM server can be defined on the command line in several ways with
the following arguments :

1. Define the WBEM server connection information with a set of general options
   The general options that define the WBEM Server include:

   * The :ref:`--server general option` that defines the URI of the WBEM server
   * The :ref:`--default-namespace general option`, that defines the namespace
     used if no namespace is included with each command,
   * several connection security general options:

     * The :ref:`--user general option`,  defines the WBEM server user name
     * The :ref:`--password general option`, defining the password for the WBEM
       server user
     * The :ref:`--no-verify general option` that defines whether the client verifies
       certificates received from the WBEM server,
     * The :ref:`--certfile general option`, client certificate file,
     * The :ref:`--keyfile general option`,  client key file,
     * The :ref:`--ca-certs general option`), a collection of certificates against
       which certificates received from the WBEM server are verified.

   * The :ref:`--timeout general option` that defines the client side timeout
     of operations. Any operation that does not receive a response in the defined
     time will result timeout exception.

2. Define a mock-server. A mock server see :ref:`Mock WBEM server support`
   substitutes a local mock WBEMConnection for a WBEM server and allows
   testing or demonstrating pywbemcli without having access to a real WBEM
   server.

3. Define connections for either a WBEM server or mock WBEM server with
   pywbemcli and add the data to a pywbemcli :term:`connections file`.
   pywbemcli can access the server data by simply defining the name on with the
   pywbem call.


.. _`Controlling operation behavior and monitoring operations`:

Controlling operation behavior and monitoring operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Several general options control the behavior and monitoring of the operations
executed against the WBEM server.

The DMTF specifications allow alternative forms of some operations,
pywbemcli implements this flexibility and controls the choice of either the
pull operations or the traditional operations through the :ref:`--use-pull
general option`. With this option the user can chose to use either type of
operation if that operation is available on the WBEM server. See
:ref:`Pywbemcli and the DMTF pull operations` for more information on pull
operations.

Since the pull operations include the ability to select the maximum size of
returned chunks of data, the :ref:`--pull-max-cnt general option` can be used
to control response chunk sizes.

In many cases it is important to the user to be able to monitor details of the
operations executed against the WBEM server, either the APIs executed in pywbem,
or the HTTP/HTML requests and responses and the time statistics for these
operations.

The :ref:`--log general option` provides the capability to log information about
this flow including:

* The API calls and responses/exceptions executed by pywbem.
* the HTTP requests and responses that pass between pywbemcli and the WBEM Server

The :ref:`--log general option` configures the logging including what is logged
and the destination for the log output.

Thus, for example, the following command would enumerate qualifiers and log
the requests and responses to the pywbemcli log file:

.. code-block:: text

   $ pywbemcli

   pywbemcli> --output-format table --server http://localhost --log all=stderr qualifier enumerate
   <returns table of qualifier declarations>
   <the pywbem API calls and esponses and the HTTP requests and responses are logged>


.. _`Controlling result output formats`:

Controlling result output formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pywbemcli allows multiple output formats for command responses using the
:ref:`--output-format general option`.

The output formats fall into three groups (table formats, CIM object formats,
and a tree format); however, not all formats are supported or applicable for all
commands:



.. _`Other miscellaneous general options`:

Other miscellaneous general options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :ref:`--verbose general option` displays extra information about the pywbemcli
internal processing, the :ref:`--version general option` displays pywbemcli version
information and  the :ref:`--help general option` provides top level help

.. _`General options descriptions`:


General options descriptions
----------------------------

This section defines in detail the requirements, characteristics, and any special
syntax of each general option

.. _`--server general option`:

--server general option
^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--server/-s`` general option is a string that is the host
name or IP address of the WBEM server to which pywbemcli will connect in the
format::

    [{Scheme}://]{Host}[:{Port}]

Where:

* Scheme: must be "https" or "http" [Default: "https"].
* Host: defines short/fully qualified DNS hostname, literal
  IPV4 address (dotted), or literal IPV6 address. see :term:`RFC3986` and
  :term:`RFC6874`
* Port: (optional) defines WBEM server port to be used [Default: 5988(HTTP)
  and 5989(HTTPS)]..

This option is mutually exclusive with the :ref:`--name general option` and the
:ref:`--mock-server general option` since each defines a connection to a WBEM server.

In the interactive mode the connection is not actually executed until a
command requiring access to the WBEM server is entered.

Examples for the `URL` parameter of this option include:

.. code-block:: text

  https://localhost:15345 (https, port 15345, host name localhost)
  http://10.2.3.9 (http, port 5988, IPv4 address 10.2.3.9)
  https://10.2.3.9 (http, port 5989, IPv4 address 10.2.3.9)
  http://[2001:db8::1234-eth0] (http, port 5988, IPv6 address 2001:db8::1234)


.. _`--name general option`:

--name general option
^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--name/-n`` general option is a string that is the name of a
WBEM server contained in the :term:`connections file`.  The server parameters
for this connection name will be loaded from the :term:`connections file` to
become the current WBEM connection in pywbemcli. Note: In the interactive mode
a connection is not actually used until a command requiring access to the WBEM
server is entered. This option is mutually exclusive with :ref:`--server
general option` and :ref:`--mock-server general option` since each option
defines a WBEM server for pywbemcli.

The following example creates a new  WBEM server named (``myserver``)
and saves in the connection file with command as follows. It then uses the
name to execute ``class get ...``:

.. code-block:: text

 $ pywbemcli connection add --server http://localhost --user me --password mypw --name myserver

 $ pywbemcli --name myserver class get CIM_ManagedElement
   <<... returns mof for CIM_ManagedElement>>>

See :ref:`Connection command group` for more information on managing
connections.


.. _`--default-namespace general option`:

--default-namespace general option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--default-namespace/-d`` is a string that defines the default
:term:`CIM namespace` to use for the target WBEM server if no namespace is
defined in a command. If this option is not defined the pywbemcli default is
``root/cimv2``.

This is the namespace used on all server operation requests unless a specific
namespace is defined by:

  * In the interactive mode prepending the command group name with the
    ``--namespace`` option.
  * Using the ``--namespace/-n`` command option to define a namespace
    on commands that specify this option.
  * Executing a command that looks in multiple namespaces (ex. ``class find``).

.. _`--user general option`:

--user general option
^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--user/-u`` general option is a string that is the user name
on the WBEM server if a user name is required by the WBEM server to
authenticate the client.

.. _`--password general option`:

--password general option
^^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--password/-p`` general option is a string that is the
password for the WBEM server. This option is normally required if the
:ref:`--user general option` is defined.  If passwords are saved into the
:term:`connections file` they are not encrypted in the file.

If the WBEM operations performed by any pywbemcli command require a password,
the password is prompted for if the :ref:`--user general option` is set (in both
modes of operation) and the ``--password`` general option is not set.

.. code-block:: text

      $ pywbemcli -s http://localhost -d root/cimv2 -u user class get
      Enter password: <password>
      . . . <The display output from get class>

If both the ``--user`` and ``--password`` options are set, the command is
executed without a password prompt:

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
See :ref:`Environment variables for general options`

The pywbemcli ``connection export`` command outputs the (bash/windows)
shell commands to set all needed environment variables.

The environment variable output is OS dependent. Thus for example in Unix type
OSs:

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

.. _`--timeout general option`:

--timeout general option
^^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--timeout\-t`` general option is an integer that defines the
client side timeout in seconds. The pywbem client includes a timeout mechanism
that closes a WBEM connection if there is no response to a request to the WBEM
server in the time defined by this value. Pywbemcli defaults to a
predefined timeout (normally 30 seconds) if this option is not defined.


.. _`--no-verify general option`:

--no-verify general option
^^^^^^^^^^^^^^^^^^^^^^^^^^

If the ``--no-verify/-n`` boolean general option is set, the client does not
verify any certificates received from the WBEM server. Any certificate returned
by the WBEM server is accepted.


.. _`--certfile general option`:

--certfile general option
^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--certfile`` general options is a file path for a X.509
client certificate to be presented to the WBEM server with the :ref:`--keyfile
general option` during the TLS/SSL handshake. This parameter is used only with
HTTPS.  If ``--certfile`` is not defined no client certificate is presented to
the server, enabling 1-way authentication. If ``--certfile`` is defined, the
client certificate is presented to the server, enabling 2-way (mutual)
authentication.

For more information on authentication types, see:
https://pywbem.readthedocs.io/en/stable/client/security.html#authentication-types

.. _`--keyfile general option`:

----keyfile general option
^^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--keyfile`` general option is a file path of the client
private key file containing the private key belonging to the public key that is
part of the X.509 certificate. See :ref:`--certfile general option` for more
information. Not required if the private key is part of the file defined in the
:ref:`--certfile general option`. ``keyfile`` is not allowed if
:ref:`--certfile general option` is not provided. Default: No client
key file. The client private key should then be part of the file defined by
``--certfile``.


.. _`--ca-certs general option`:

----ca-certs general option
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--ca-certs`` general option is the path name of a  file or
directory containing certificates that will be matched against a certificate
received from the WBEM server. The default is OS dependent and is a set of
system directories where certificates are expected to be stored for the client
OS.

Setting the :ref:`--no-verify general option` bypasses client verification of
the WBEM server certificate.


.. _`--use-pull general option`:

--use-pull general option
^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--use-pull/-u`` general option is one of the following
strings: [``yes``|``no``|``either``] that determines whether the pull
operations or :term:`traditional operations` are used for the
``instance enumerate``, ``instance references``, ``instance associators``
and ``instance query`` commands.  See :ref:`Pywbemcli and
the DMTF pull operations` for more information on pull operations. The value
choices are as follows:

* ``yes`` - pull operations will be used and if the server does not
  support pull, the request will fail.
* ``no`` - forces pywbemcli to try only the traditional non-pull operations.
* ``either`` - (default) pywbem tries both; first pull operations and then
  :term:`traditional operations` .

.. _`--pull-max-cnt general option`:

--pull-max-cnt general option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--pull-max-cnt`` general option is an integer passed to the
WBEM server with the open and pull operation requests. This integer,
``MaxObjectCount`` tells the server the maximum number of objects
to be returned for each pull request if pull operations are used. This must
be  a positive non-zero integer. The default is 1000. See :ref:`Pywbemcli and the
DMTF pull operations` for more information on pull operations.

.. _`--mock-server general option`:

--mock-server general option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--mock-server/-m`` general option is a file path that
defines MOF and python that can be used to define a mock WBEM server in the
pywbemcli process. This allows pywbemcli to be used without access to a real server.
When this option is used to define a WBEM server the security options (ex.
``--user``) are irrelevant; they may be included but are not used.

The following example creates a mock server with two files defining the mock
data, shows what parameters are defined for the connection, and then saves that
connection named ``mymockserver``:

.. code-block:: text

  $ pywbemcli --mock-server classdefs.mof --mock-server insts.py --default-namespace root/myhome
  pywbemcli> connection show
    Name: default
      WBEMServer uri: None
      Default-namespace: root/myhome
      . . .
      use-pull: either
      pull-max-cnt: 1000
      mock: classdefs.mof, insts.py
      log: None
  pywbemcli> connection save --name mymockserver

See chapter :ref:`Mock WBEM server support` for more information on defining
the files for a mock server.

.. _`--output-format general option`:

--output-format general option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The argument value of the ``--output-format/-o`` general option is a string
that defines
the output format for the pywbemcli command or interactive session. This argument
values of this option are described in the :ref:`Output formats` section.

.. _`--log general option`:

--log general option
^^^^^^^^^^^^^^^^^^^^

The argument value of the  ``--log/-l`` general option defines the destination and
parameters of logging of the requests and responses to the WBEM Server as
documente in :ref:`Pywbemcli defined logging`.

.. _`--verbose general option`:

--verbose general option
^^^^^^^^^^^^^^^^^^^^^^^^

``--verbose/-v``  is a boolean general option. When set it enables display of
extra information about the processing.

.. _`--version general option`:

--version general option
^^^^^^^^^^^^^^^^^^^^^^^^

``--version/-V`` displays the version of this command and of the pywbem package
  imported then exit.

.. _`--help general option`:

--help general option
^^^^^^^^^^^^^^^^^^^^^
``--help/-h`` display help text which describes the command line general
options and exits.


.. _`Environment variables for general options`:

Environment variables for general options
-----------------------------------------

Pywbemcli defines environment variables corresponding to the command line
general options as follows:

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
PYWBEMCLI_CACERTS               ``--ca-certs``
PYWBEMCLI_USE_PULL              ``--use-pull``
PYWBEMCLI_PULL_MAX_CNT          ``--pull-max-cnt``
PYWBEMCLI_STATS_ENABLED         ``--timestats``
PYWBEMCLI_MOCK_SERVER           ``--mock-server``
PYWBEMCLI_LOG                   ``--log``
==============================  ============================

If any of these environment variables are set, the corresponding general
options on the command line are not required and the value of the environment
variable is used. If both the environment variable and the command line option
are included the command line option overrides the environment variable with no
warning.

Environment variable options are not provided for command options or arguments.

In the following example, the second line accesses the server
``http://localhost`` defined by the export command:

.. code-block:: text

      $ export PYWBEMCLI_SERVER=http://localhost
      $ pywbemcli class get CIM_ManagedElement
        <displays MOF for CIM_ManagedElement>

The pywbemcli ``connection export`` command that outputs the (bash/windows)
shell commands to set all needed environment variables:

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



.. _`Pywbemcli and the DMTF pull operations`:

Pywbemcli and the DMTF pull operations
--------------------------------------

The DMTF specifications and pywbem includes two ways to execute the enumerate
instance type operations (``Associators``, ``References``,``
EnumerateInstances``, ``ExecQuery``):

* The :term:`traditional operations` (ex. ``EnumerateInstances``)
* The pull operations (ex. the pull sequence ``OpenEnumerateInstances``, etc.)

pywbem implements an overlay of the above two operations called the ``Iter..``.
operations where each ``Iter..`` operation executes either the traditional or
pull operation depending on a parameter of the connection.

While the pull operations may not be supported by all WBEM servers they can be
significantly more efficient for large responses when they are available.
Pywbem implements the client side of these operation and pywbemcli provides for
the use of these operations through two general options:

* ``--use-pull`` - This option allows the user to select from the
  the following alternatives:

    * ``either`` - pywbemcli first tries the open operation and if that is not
      implemented by the server retries the operation with the corresponding
      non-pull operation. The result of this first operation determines whether
      pull or the traditional operation are used for any further requests
      during the current pywbem interactive session. `either` is the default.

    * ``yes`` - Forces the use of the pull operations and if those operations fail
      generates an error.

    * ``no`` - Forces the use of the non-pull operation.

* ``--pull-max-cnt`` - Sets the maximum count of objects the server is allowed
  to return for each open/pull operation. ``pull-max-cnt`` of 1000 objects is the
  default size which from experience is a logical choice.

There are limitations with using the the ``either`` choice as follows"

* The original operations did not support the filtering of responses with a
  query language query (``--filter-query-language`` and ``--filter-query`` )
  which requests that the WBEM server filter
  the responses before they are returned. This can greatly reduce the size of
  the responses if effectively used but is used only when the pull operations
  are available on the server.

* The pull operations do not support some of the options that traditional
  operations do:

* ``--include-qualifiers`` - Since even the traditional operations specification
  deprecated this option and the user cannot depend on it being honored,
  the most logical solution is to never use this option.

* ``--local-only`` - Since even the traditional operations specification
  deprecated this options and the user cannot depend on it being honored by
  the WBEM server the most logical solution is to never use this option.

The following example forces the use of the pull operations  and expects the
WBEM server to return no more that 10 instances per request. It returns an
exception if the pull operations are not supported in the WBEM server::

    pywbemcli --server http/localhost --use-pull=yes max_object_cnt=10

Since the default for ``--use-pull`` is ``either``, normally pywbem first tries
the pull operation and then if that fails, the traditional operation.  That
is probably the most logical setting for ``--use-pull`` unless you are
specifically testing the use of pull operations.


.. _`Output formats`:

Output formats
--------------

Pywbemcli supports various output formats for the command result. The output
format can be selected with the ``--output-format/-o`` option.

The output formats fall into three groups:

* **Table formats** - The :ref:`Table formats` format the result as a table
  with rows and columns. Many of the results types allow table formatted
  response display including:

  * ``instance get`` , enumerate, references, associators where the table
    formats are alternates to the CIM model formats that shows the properties
    for each instance as a column in a table.
  * ``instance count``
  * ``server`` commands
  * ``class find``
  * ``connection`` commands

* **CIM object formats** - The :ref:`CIM object formats` format a result that
  consists of CIM objects in MOF, CIM-XML or pywbem repr format. All of the
  commands that return CIM objects support these output formats.

* **ASCII tree format** - The :ref:`ASCII tree format` formats the result
  as a tree, using ASCII characters to represent the tree. The only command
  supporting the ASCII tree format is ``class tree``, and it supports only
  that one output format.

When an unsupported output format is specified for a command response, it is
ignored and a default output format is used instead.  Thus, the command
``class enumerate`` only supports the CIM object formats and always outputs
in those formats.


.. _`Table formats`:

Table formats
^^^^^^^^^^^^^

The different variations of the table format define different formatting of the
borders for tables. The following are examples of the table formats with a
single command ``class find CIM_Foo``:

* ``--output-format table``: Tables with a single-line border. This is the default:

  .. code-block:: text

    Find class CIM_Foo*
    +-------------+-----------------+
    | Namespace   | Classname       |
    |-------------+-----------------|
    | root/cimv2  | CIM_Foo         |
    | root/cimv2  | CIM_Foo_sub     |
    | root/cimv2  | CIM_Foo_sub2    |
    | root/cimv2  | CIM_Foo_sub_sub |
    +-------------+-----------------+

* ``--output-format simple``: Tables with a line between header row and data
  rows, but otherwise without borders:

  .. code-block:: text

    Find class CIM_Foo*
    Namespace    Classname
    -----------  ---------------
    root/cimv2   CIM_Foo
    root/cimv2   CIM_Foo_sub
    root/cimv2   CIM_Foo_sub2
    root/cimv2   CIM_Foo_sub_sub

* ``--output-format plain``: Tables do not use any pseudo-graphics to draw borders:

  .. code-block:: text

    Find class CIM_Foo*
    Namespace    Classname
    root/cimv2   CIM_Foo
    root/cimv2   CIM_Foo_sub
    root/cimv2   CIM_Foo_sub2
    root/cimv2   CIM_Foo_sub_sub

* ``--output-format grid``: Tables tables formatted by Emacs' `table.el`
  package. It corresponds to ``grid_tables`` in Pandoc Markdown extensions:

  .. code-block:: text

    Find class CIM_Foo*
    +-------------+-----------------+
    | Namespace   | Classname       |
    +=============+=================+
    | root/cimv2  | CIM_Foo         |
    +-------------+-----------------+
    | root/cimv2  | CIM_Foo_sub     |
    +-------------+-----------------+
    | root/cimv2  | CIM_Foo_sub2    |
    +-------------+-----------------+
    | root/cimv2  | CIM_Foo_sub_sub |
    +-------------+-----------------+


* ``--output-format rst``: Tables in `reStructuredText`_ markup:

  .. code-block:: text

    Find class CIM_Foo*
    ===========  ===============
    Namespace    Classname
    ===========  ===============
    root/cimv2   CIM_Foo
    root/cimv2   CIM_Foo_sub
    root/cimv2   CIM_Foo_sub2
    root/cimv2   CIM_Foo_sub_sub
    ===========  ===============

* ``--output-format psql``: Like tables formatted by Postgres' psql cli:

  .. code-block:: text

    Find class CIM_Foo*
    ===========  ===============
    Namespace    Classname
    ===========  ===============
    root/cimv2   CIM_Foo
    root/cimv2   CIM_Foo_sub
    root/cimv2   CIM_Foo_sub2
    root/cimv2   CIM_Foo_sub_sub
    ===========  ===============

* ``--output-format html``: Tables formatted as html table:

  .. code-block:: text

    <p>Find class CIM_Foo*</p>
    <table>
    <thead>
    <tr><th>Namespace  </th><th>Classname      </th></tr>
    </thead>
    <tbody>
    <tr><td>root/cimv2 </td><td>CIM_Foo        </td></tr>
    <tr><td>root/cimv2 </td><td>CIM_Foo_sub    </td></tr>
    <tr><td>root/cimv2 </td><td>CIM_Foo_sub2   </td></tr>
    <tr><td>root/cimv2 </td><td>CIM_Foo_sub_sub</td></tr>
    </tbody>
    </table>

.. _`reStructuredText`: http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables
.. _`Mediawiki`: http://www.mediawiki.org/wiki/Help:Tables
.. _`HTML`: https://www.w3.org/TR/html401/struct/tables.html
.. _`LaTeX`: https://en.wikibooks.org/wiki/LaTeX/Tables
.. _`JSON`: http://json.org/example.html


.. _`CIM object formats`:

CIM object formats
^^^^^^^^^^^^^^^^^^

The output of CIM objects allows multiple formats as follows:

* ``--output-format mof``: Format for CIM classes, CIM instances, and CIM Parameters:

  :term:`MOF` is the format used to define and document the CIM models released
  by the DMTF and SNIA. It textually defines the components and structure and
  data of CIM elements such as classes, instances, and qualifier declarations.:

  .. code-block:: text

      instance of CIM_Foo {
         InstanceID = "CIM_Foo1";
         IntegerProp = 1;
      };

* ``--output-format xml``: :term:`CIM-XML` format for CIM elements such as classes,
  instances and qualifier declarations. Besides being used as a protocol for WBEM
  servers, CIM-XML is also an alternative format for representing the CIM models
  released by the DMTF and SNIA. The XML syntax is defined in  the DMTF
  specification :term:`DSP0201`.

  This is the format used in the DMTF CIM-XML protocol:

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

* ``--output-format repr``: Python repr format of the objects.

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

* ``--output-format txt``: Python str format of the objects.

  This should be considered the output of last resort as it simply uses
  the __str__ method of the python class for each CIM object to output.

  Thus, for example the a ``class enumerate`` of a model with only a single
  class is of the form:

  .. code-block:: text

      CIMClass(classname='CIM_Foo', ...)


.. _`ASCII tree format`:

ASCII tree format
^^^^^^^^^^^^^^^^^

This output format is an ASCII based output that shows the tree structure of
the results of the ``class tree`` command. It is the only output format
supported by this command, and therefore it is automatically selected and
cannot be specified explicitly with the ``--output-format`` option.

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

Pywbemcli provides logging to either a file or the standard error stream
of information passing between the pywbemcli client and a WBEM server using the
standard Python logging facility.

Logging is configured and enabled using the ``--log`` general option on the
commmand line or the `PYWBEMCLI_LOG` environment variable.

Pywbemcli can log  operation calls that send
requests to a WBEM server and their responses and the HTTP messages between
the pywbemcli client and the WBEM server including both the pywbem APIs
and their responses and the HTTP requests and responses.

The default is no logging if the ``--log`` option is not specified.

The argument value of the the `--log` option parameter and of the PYWBEMCLI_LOG
environment variable is a log configuration string with the format defined in
the ABNF rule LOG_CONFIG_STRING. The log configuration string defines a list of
one or more log configurations, each with fields COMPONENT, DESTINATION, and
DETAIL:".

.. code-block:: text

    LOG_CONFIG_STRING := CONFIG[ "," CONFIG]
    CONFIG            := COMPONENT "=" [DESTINATION[ ":" DETAIL]
    COMPONENT         := ("all" / "api" / "http")
    DESTINATION       := ("stderr" / filepath)
    DETAIL            := ("all"/ "path"/ "summary")

For example the following log string logs the pywbem API calls and responses
summary information to a file and the HTTP requests and responses to stderr:

.. code-block:: text

      $ pywbemcli --log api=file:summary,http=stderr

The COMPONENT field defines the component for which logging is enabled:

  * ``api`` - Logs the calls to the pywbem methods that make requests to a
    WBEM server. This logs both the requests and response including any
    exceptions generated by error responses from the WBEM server.
  * ``http`` - Logs the headers and data for HTTP requests and responses to the
    WBEM server.
  * ``all`` - (Default) Logs both the ``api`` and ``http`` components.

The DESTINATION field specifies the log destination:

  * ``stderr`` - Output log to stderr.
  * ``file`` - (default) Log to the pywbemcli log file ``pywbemcli.log`` in
    the current directory.  Logs are appended to an existing log file.

The DETAIL component of the log configuration string defines the level of
logging information for the api and http components.  Because enormous quantities
of information can be generated this option exists to limit the amount of
information generated. The possible keywords are:

  * ``all`` - (Default) Logs the full request including all input parameters and
    the complete response including all data. Exceptions are fully logged.

  * ``paths`` - Logs the full request but only the path component of the
    `api` responses. This reduces the data included in the responses.
    Exceptions are fully logged.

  * ``summary`` - Logs the requests but only the count of objects received
    in the response.  Exceptions are fully logged.

The log output is routed to the output defined by DESTINATION and includes the
information determined by the COMPONENT and DETAIL fields.

The log output format is:

.. code-block:: text

    <Date time>-<Component>.<ref:`connection id`>-<Direction>:<connection id> <PywbemOperation>(<data>)

For example, logging only of the summary  API information would look something
like the following:

.. code-block:: text

    $ pywbemcli -s http://localhost -u blah -p pw -l api=file:summary class enumerate -o

produces log output for the class enumerate operation in the log file
pywbemcli.log as follows showing the input parameters to the pywbem method
``EnumerateClassName`` and the number of objects in the response:

.. code-block:: text

    2019-07-09 18:27:22,103-pywbem.api.1-27716-Request:1-27716 EnumerateClassNames(ClassName=None, DeepInheritance=False, namespace=None)
    2019-07-09 18:27:22,142-pywbem.api.1-27716-Return:1-27716 EnumerateClassNames(list of str; count=103)


.. _`Pywbemcli persisted connection definitions`:

Pywbemcli persisted connection definitions
------------------------------------------

Pywbemcli can manage connections via the :ref:`connection command group`. These
connections are persisted in a :term:`connections file` named
`pywbemcli_connections.json` in the current directory. A connection has a name
and defines all parameters necessary to connect to a WBEM server. Once defined
these connections can be accessed with the general option ``--name`` or in the
interactive mode the ``connection select`` command.

A new persistent connection definition can be created  by executing
pywbemcli with the ``connection add`` command. The options on this command will
define the WBEM server and its security characteristics, a name for that server
and save the result to the :term:`connections file`.

At any point in time, pywbemcli can communicate with only a single WBEM server. That
is the current connection.
In the command mode, this is the WBEM server defined by the command line inputs
``--server`` or ``--mock-server`` or ``--name``.  In the interactive mode, the
connection that is active (the current connection) can be changed within an
interactive session using ``connection select`` so that within a single
session, the user can work with multiple WBEM servers. The server that was defined
when pywbemcli was started or the server selected by ``connection select`` is the
current server.

For example the following example of a pywbemcli interactive session creates a
new connection in the CLI command mode:

.. code-block:: text

    $ pywbemcli
    pywbemcli> connection add --server http://localhost --user usr1 -password blah --name testconn
    pywbemcli> connection show
    name: testconn
      server: http://localhost
      default-namespace: root/cimv2
      user: usr1
      password: blah
      timeout: None
      no-verify: False
      certfile: None
      keyfile: None
      use-pull: None
      pull-max-cnt: 1000
      mock-server:
      log: None

    pywbemcli> connection list

    name       server uri        namespace    user         timeout  noverify
    ---------  ----------------  -----------  -----------  -------  ----------
    testconn*  http://localhost  root/blah    me                30  False

Note: The * indicates that this is the current connection.

Other connections can be added from either the command mode or interactive mode
using the add command:

.. code-block:: text

    pywbemcli> connection add Ronald http://blah2 -u you -p xxx
    pywbemcli> connection list
    WBEMServer Connections:
    name      server uri        namespace    user         password      timeout  noverify
    --------  ----------------  -----------  -----------  ----------  ---------  ----------
    Ronald    http://blah2      root/cimv2   you          xxx                    False
    testconn  http://localhost  root/blah    kschopmeyer  test8play          30  False

These persisted connections can now be used either in the command mode or interactive mode.

For example, in the command mode the following executes a command with a WBEM
server definition from the :term:`connections file`.

.. code-block:: text

    $ pywbemcli -n Ronald server brand

    Server brand:
    +---------------------+
    | WBEM server brand   |
    |---------------------|
    | OpenPegasus         |
    +---------------------+

In the interactive mode the current WBEM server can be defined with the
``connection select`` command which selects a connection definition from the
:term:`connections file` and makes that the current connection.

.. code-block:: text

    $ pywbemcli
    pywbemcli> connection select Ronald
    pywbemcli> connection list

    WBEMServer Connections:
    name      server uri        namespace    user         timeout  noverify
    --------  ----------------  -----------  -----------  ---------  ----------
    Ronald*   http://blah2      root/cimv2   you                     False
    testconn  http://localhost  root/blah    kschopmeyer         30  False

    pywbemcli> server interop

    Server Interop Namespace:
    +------------------+
    | Namespace Name   |
    |------------------|
    | root/PG_InterOp  |
    +------------------+

    pywbemcli> connection select testconn

    WBEMServer Connections:
    name      server uri        namespace    user         timeout  noverify
    --------  ----------------  -----------  -----------  ---------  ----------
    Ronald    http://blah2      root/cimv2   you                     False
    testconn* http://localhost  root/blah    kschopmeyer         30  False

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
    $ pywbemcle connection list
    WBEMServer Connections:
    name      server uri        namespace    user         timeout  noverify
    --------  ----------------  -----------  -----------  ---------  ----------
    testconn  http://localhost  root/blah    kschopmeyer         30  False
