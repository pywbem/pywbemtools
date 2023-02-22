.. _`Using the pywbemcli command line general options`:

Using the pywbemcli command line general options
------------------------------------------------

.. index:: single: general options

.. _`Overview of the general options`:


Overview of the general options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

General options define:

* The server definition (i.e. :term:connection definition) to the WBEM server or mock WBEM server
  against which the pywbemcli commands are targeted. See :ref:`Defining the WBEM server` for details.
* Attributes of the WBEM server which is being targeted. This includes attributes
  such as the user/password, certificates, etc. pull operations. These attributes
  are attached to the current WBEM server connection definition and persisted with that
  :term:`connection definition`.
* Operation behavior of pywbemcli for requests; i.e. using the pull operations
  vs the :term:`traditional operations`, the client side timeout, etc..
  See :ref:`Controlling operation behavior and monitoring operations` for
  details.
* Execution options to monitor the requests and responses (statistics keeping,
  and logging of operations) and to display the results.
  See :ref:`Controlling operation behavior and monitoring operations` and
  :ref:`Controlling output formats` for details.
* General options to show the pywbemcli version, and display help for any of
  the command groups or commands.

General options must be entered on the command line before the command group
or command.

For example the following enumerates qualifier declarations and outputs the
result in the ``simple`` table format:

.. code-block:: text

    pywbemcli --output-format simple --server http://localhost qualifier enumerate

    Qualifier Declarations
    Name         Type     Value    Array    Scopes       Flavors
    -----------  -------  -------  -------  -----------  ---------------
    Description  string            False    ANY          EnableOverride
                                                         ToSubclass
                                                         Translatable
    Key          boolean  False    False    PROPERTY     DisableOverride
                                            REFERENCE    ToSubclass

In interactive mode, general options from the command line are defined
once and retain their value throughout the execution of the interactive mode.

General options defined in the command line may be overwritten by specifying
them on interactive mode commands. The resulting new value is used only for
that one command, and is not retained for subsequent interactive mode commands.

In the following example, the :ref:`--output-format general option` is used
on an interactive mode command to overwrite the default output format, and the
:ref:`--server general option` is used to overwrite the server that was
specified in the command line invocation:

.. code-block:: text

    $ pywbemcli --server http://myserver

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

The following table is an overview of all of the pywbemcli general options with
a cross-reference to a detailed definition of each option.


.. list-table:: pywbemcli general options
   :widths: 20 20 20 20 20
   :header-rows: 1

   * - Option Name
     - Function(1)
     - Description
     - Type
     - Default Value

   * - :ref:`--server <--server general option>`
     - Server Definition
     - Define server URI
     - String
     -

   * - :ref:`--name <--name general option>`
     - Sever Definition
     - Get server definition by name
     - String
     -

   * - :ref:`--mock-server <--mock-server general option>`
     - Server Definition
     - Define mock server
     - String
     -

   * - :ref:`--user <--user general option>`
     - Server Attribute
     - Server user name
     - String
     -

   * - :ref:`--password <--password general option>`
     - Server Attribute
     - Server user password
     - String
     -

   * - :ref:`--use-pull <--use-pull general option>`
     - Server attribute
     - Use of pull Operations
     - Choice
     - either

   * - :ref:`--pull-max-cnt <--pull-max-cnt general option>`
     - Server attribute
     - Max pull response size
     - Integer
     - 1000

   * - :ref:`--certfile <--certfile general option>`
     - Server attribute
     - Server cert attribute
     - String
     -

   * - :ref:`--keyfile <--keyfile general option>`
     - Server attribute
     - Private key file attribute
     - String
     -

   * - :ref:`--timestats <--timestats general option>`
     - Client attribute
     - Control stats
     - Boolean
     -

   * - :ref:`--log <--log general option>`
     - Client attribute
     - Define log output
     - String
     -

   * - :ref:`--verify <--verify general option>`
     - Client attribute
     - Verify server cert
     - Boolean
     - True

   * - :ref:`--ca-certs <--ca-certs general option>`
     - Client blah
     - Define server ca certs
     - String
     -

   * - :ref:`--timeout <--timeout general option>`
     - Client attribute
     - Timeout server request
     - Integer (sec)
     - 30 sec

   * - :ref:`--default-namespace <--default-namespace general option>`
     - Client attribute
     - Connection default namespace
     - String
     - root/cimv2

   * - :ref:`--output-format <--output-format general option>`
     - Client attribute
     - Define Table format
     - Choice
     - MOF

   * - :ref:`--verbose <--verbose general option>`
     - Client attribute
     - Display processing details
     - Boolean
     - False

   * - :ref:`--version <--version general option>`
     - Client attribute
     - Show pywbemtools version
     -
     -

   * - :ref:`--warn <--warn general option>`
     - Client attribute
     - Control warnings display
     - Boolean
     -

   * - :ref:`--connections-file <--connections-file general option>`
     - Client attribute
     - Define file path
     - String
     - Default file

   * - :ref:`--pdb <--pdb general option>`
     - Client attribute
     - Run with debugger
     - Boolean
     -

   * - :ref:`--helo <--help general option>`
     - Client attribute
     - Show help
     - String
     -

1. Server definitions and server attributes are attached to a :term:`connection definition`
   and are used when defined for the current :term:`connection definition` in
   the interactive mode.  Client attribute exist for the life of an interactive
   session in the interactive mode. Thus --verbose entered on the command line
   is used for all commands in the interactive mode.  --user entered on the
   command line applies to the current server definition only.


.. index:: pair: WBEM server; defining the WBEM server

.. _`Defining the WBEM server`:

Defining the WBEM server
""""""""""""""""""""""""

The target WBEM server can be defined on the command line in several ways with
the following arguments :

1. General options that define the WBEM server to be used.

   The following 3 mutually exclusive general options define the WBEM server
   that wil be the target of pywbem cli server-request commands (ex. class get
   <class name).

   * The :ref:`--server general option` defines the URI of a real WBEM server.
     The attributes of the server used by pywbemcli are defined by the
     connection characteristics general options (ex. --user, etc.)

.. code-block:: text

    pwybmcli -s http:myserver

   * The :ref:`--name general option` defines the name of a :term:`connection definition`
     in a :term:`connections file`. This name must have been previously created
     by saving the name of a server definition with the :ref:`Command
     connection save` command.

.. code-block:: text

    pwybmcli -n mytestserver connection show

    defines the use of the previously defined connection ``mytestserver`` and
    executes the pywbem command ``connection show``.

   Connection definitions can be stored in a :term:`connections file`
   and are managed with the :ref:`Connection command group`.

   * The :ref:`--mock-server general option` defines a :ref:`Mock WBEM Server` that
     is created upon pywbemcli startup.  The MOF or python files that are defined
     with as values of the option define the characteristics of thes mock WBEM server
     (The CIM objects that will be build in the mock environment and that can be
     accesses as if they were a real WBEM server).

     The mock WBEM server allows testing or demonstrating pywbemcli without
     having access to a real WBEM server.

.. code-block:: text

    pwybmcli -m mytestmof.mof -m mytestscript.py class enumerate

    defines the use of the pywbemcli mock WBEM server script ``myscript.py`` and
    executes the pywbem command ``class enumerate`` to show the first level
    of the class hiearchy class names in the default namespace.

2. Define connection characteristics for a WBEM server by using the

   The following general options can be used for specifying additional
   information for the connection and become part of the :term:`connection definition`
   (i.e. connection) for a WBEM server.

   * The :ref:`--default-namespace general option` defines the :term:`default namespace`
     to be used if a command does not specify a namespace.
   * The :ref:`--user general option` defines the user name for authenticating
     with the WBEM server.
   * The :ref:`--password general option` defines the password for
     authenticating with the WBEM server.
   * The :ref:`--verify general option` defines whether the client verifies
     certificates received from the WBEM server.
   * The :ref:`--use-pull general option` defines whether pywbemcli issues
     requests like ``instance enumerate`` as pull operations or as the traditional
     operations. See :ref:`pywbem:Pull operations`.
   * The :ref:`--pull-max-cnt general option` defines the maximum number of
     instances the WBEM server can return in a single response to an Open or
     Pull client request
   * The :ref:`--certfile general option` defines the client certificate file.
   * The :ref:`--keyfile general option` defines the client key file.
   * The :ref:`--ca-certs general option` defines a collection of certificates
     against which certificates received from the WBEM server are verified.
   * The :ref:`--timeout general option` defines the client side timeout
     for operations.

   NOTE: Not all of the above general options are used by the mock WBEM server.
   Thus, since the mock WBEM server has no security layer, the ``--keyfile``,
   ``--certfile``, and ``--ca-certs`` options will be rejected if a
   mock WBEM server is specified

   A :term:`connection definition` can be named and persisted in a pywbemcli
   :term:`connections file` identified by a connection name so that it can
   be used by pywbem with the :ref:`--name general option`.


.. _`Controlling operation behavior and monitoring operations`:

Controlling operation behavior and monitoring operations
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Several general options control the behavior and monitoring of the operations
executed against the WBEM server.

The DMTF specifications allow alternative forms of some operations,
pywbemcli implements this flexibility and controls the choice of either the
pull operations or the traditional operations through the :ref:`--use-pull
general option`. With this option the user can choose to use either type of
operation if that operation is available on the WBEM server. See
:ref:`Pywbemcli and the DMTF pull operations` for more information on pull
operations.

Since the pull operations include the ability to select the maximum size of
returned chunks of data, the :ref:`--pull-max-cnt general option` can be used
to control response chunk sizes.

In many cases it is important to the user to be able to monitor details of the
operations executed against the WBEM server, either the APIs executed in pywbem,
or the HTTP requests and responses and the time statistics for these
operations.

.. index:: single: --log

The :ref:`--log general option` provides the capability to log information about
this flow including:

* The API calls and responses/exceptions executed by pywbem.
* the HTTP requests and responses that pass between pywbemcli and the WBEM server.

The :ref:`--log general option` configures the logging including what is logged
and the destination for the log output.

Thus, for example, the following command enumerates qualifiers and writes
the log entries for the CIM-XML HTTP requests and responses to the pywbemcli log
file ``pywbemcli.log``:

.. code-block:: text

   $ pywbemcli --output-format table --server http://localhost --log http=file qualifier enumerate
   <displays table of qualifier declarations>

   $ cat pywbemcli.log
   2019-09-16 21:14:04,296-pywbem.http.1-21020-Connection:1-21020 WBEMConnection(url='http://localhost', ...)
   2019-09-16 21:14:04,297-pywbem.http.1-21020-Request:1-21020 POST /cimom 11 http://localhost
       CIMOperation:'MethodCall' CIMMethod:'EnumerateQualifiers' CIMObject:u'root/cimv2'
       <?xml version="1.0" encoding="utf-8" ?>
       <CIM CIMVERSION="2.0" DTDVERSION="2.0"><MESSAGE ID="1001" PROTOCOLVERSION="1.0">
       ...
       </CIM>
   . . .

.. index:: pair: controlling output format; output format

.. _`Controlling output formats`:

Controlling output formats
""""""""""""""""""""""""""

Pywbemcli supports multiple output formats for command results by using the
:ref:`--output-format general option`.

The output formats fall into several groups (table formats, CIM object formats,
text formats, and a tree format); however, not all formats are supported or
applicable for all commands. For more details, see :ref:`Output formats`.


.. _`Other miscellaneous general options`:

Other miscellaneous general options
"""""""""""""""""""""""""""""""""""

The :ref:`--verbose general option` displays extra information about the
pywbemcli internal processing.

The :ref:`--warn general option` controls the display of warnings.

The :ref:`--version general option` displays pywbemcli version
information and the :ref:`--help general option` provides top level help


.. _`General options descriptions`:

General options descriptions
""""""""""""""""""""""""""""

This section defines in detail the requirements, characteristics, and any
special syntax of each general option.

.. index:: triple: --server; general options; server

.. _`--server general option`:

``--server`` general option
"""""""""""""""""""""""""""

The argument value of the ``--server``/``-s`` general option is a string that is
the URL of the WBEM server to which pywbemcli will connect, in the format:

.. code-block:: text

    [SCHEME://]HOST[:PORT]

Where:

* **SCHEME**: The protocol to be used. Must be "https" or "http". Default: "https".
* **HOST**: The WBEM server host. Must be a short hostname, fully qualified DNS
  hostname, literal IPv4 address, or literal IPv6 address.
  See :term:`RFC3986` and :term:`RFC6874` for details.
* **PORT**: The WBEM server port to be used.
  Default: 5988 for HTTP, and 5989 for HTTPS.

This option is mutually exclusive with the :ref:`--name general option` and the
:ref:`--mock-server general option` since each defines a connection to a WBEM
server.

In the interactive mode the connection is not actually established until a
command requiring access to the WBEM server is entered.

Examples for the argument value of this option include:

.. code-block:: text

    https://localhost:15345       # https, port 15345, hostname localhost
    http://10.2.3.9               # http, port 5988, IPv4 address 10.2.3.9
    https://10.2.3.9              # https, port 5989, IPv4 address 10.2.3.9
    http://[2001:db8::1234-eth0]  # http, port 5988, IPv6 address 2001:db8::1234, interface eth0

.. index:: triple: --name; general options; name

.. _`--name general option`:

``--name`` general option
"""""""""""""""""""""""""

The argument value of the ``--name``/``-n`` general option is a string that is
the name of a :term:`connection definition` in the :term:`connections file`.
The parameters for this named :term:`connection definition` will be loaded from the
:term:`connections file` to become the current WBEM connection in pywbemcli.

In the interactive mode the connection is not actually established until a
command requiring access to the WBEM server is entered.

This option is mutually exclusive with the :ref:`--server general option` and
the :ref:`--mock-server general option` since each defines a connection to a
WBEM server.

The following example creates a :term:`connection definition` named ``myserver``
in the connections file, and then uses that connection to execute
``class get``:

.. code-block:: text

    $ pywbemcli --server http://localhost --user me --password mypw connection save myserver

    $ pywbemcli --name myserver class get CIM_ManagedElement
    <displays MOF for CIM_ManagedElement>

See :ref:`Connection command group` for more information on managing
connections.

.. index:: triple: --default-namespace; general options; default-namespace

.. _`--default-namespace general option`:

``--default-namespace`` general option
""""""""""""""""""""""""""""""""""""""

The argument value of the ``--default-namespace``/``-d`` general option is a
string that defines the default :term:`CIM namespace` to use for the target
WBEM server.

If this option is not specified, the :term:`default namespace` will be ``root/cimv2``.

The default namespace will be used if the ``--namespace``/``-n`` command option
is not used on a command.

Some commands execute against multiple or all namespaces, for example the
the ``class find`` command.


.. _`--user general option`:

``--user`` general option
"""""""""""""""""""""""""

The argument value of the ``--user``/``-u`` general option is a string that is
the user name for authenticating with the WBEM server.

.. index:: triple: --password; general options; password

.. _`--password general option`:

``--password`` general option
"""""""""""""""""""""""""""""

The argument value of the ``--password``/``-p`` general option is a string that
is the password for authenticating with the WBEM server.

This option is normally required if the :ref:`--user general option` is defined.
If passwords are saved into the :term:`connections file`, they are not encrypted
in the file.

If the WBEM operations performed by any pywbemcli command require a password,
the password is prompted for if ``--user``/``-u`` is used (in both modes of
operation) and ``--password``/``-p`` is not used.

.. code-block:: text

    $ pywbemcli --server http://localhost --user me class get
    Enter password: <password>
    . . . <The display output from get class>

If both ``--user``/``-u`` and ``--password``/``-p`` are used, the command is
executed without a password prompt:

.. code-block:: text

    $ pywbemcli --server http://localhost --user me --password blah class get
    . . . <The display output from get class>

If the operations performed by a particular pywbemcli command do not
require a password or no user is supplied, no password is prompted.
For example:

.. code-block:: text

      $ pywbemcli --help
      . . . <help output>

For script integration, it is important to have a way to avoid the interactive
password prompt. This can be done by storing the password string in an
environment variable or specifying it on the command line.
See :ref:`Environment variables for general options`.

The pywbemcli :ref:`Connection export command` outputs the (bash/Windows)
shell commands to set all needed environment variables.

The environment variable output is OS dependent. Thus for example in Unix type
OSs:

.. code-block:: text

    $ pywbemcli --server http://localhost --user fred connection export
    export PYWBEMCLI_SERVER=http://localhost
    export PYWBEMCLI_NAMESPACE=root/cimv2
    ...

This ability can be used to set those environment variables and thus to persist
the connection name in the shell environment, from where it will be used in
any subsequent pywbemcli commands:

.. code-block:: text

    $ eval $(pywbemcli --server http://localhost --user fred connection export)

    $ env | grep PYWBEMCLI
    export PYWBEMCLI_SERVER=http://localhost
    export PYWBEMCLI_NAMESPACE=root/cimv2

    $ pywbemcli server namespaces
    . . . <list of namespaces for the defined server>

.. index:: triple: --timeout; general options; timeout

.. _`--timeout general option`:

``--timeout`` general option
""""""""""""""""""""""""""""

The argument value of the ``--timeout``/``-t`` general option is an integer
that defines the client side read timeout in seconds. The pywbem client
includes a timeout mechanism that closes a WBEM connection and terminates the
current pywbemcli request if there is no response to a WBEM server request
in the time defined by timeout with multiple retries. A read timeout
occurs any time no bytes have been received on the underlying socket for
timeout seconds.

See ``pywbemcli --help`` for the actual retry count value.  Thus, the actual
time to command failure is multiple times the value of this option. Therefore
a request that does not receive any response data and with timeout value of
5 would timeout in, for example ( 5 sec * 3 (request and retries)) = 15 seconds.

Pywbemcli defaults to a predefined read timeout (normally 30 seconds) if this
option is not defined.

The connection functionality has a separate timeout time set by pywbem and
set at 10 seconds also with retries. The connection timeout is not modifiable
by pywbemcli.

In general the timeout value should only be modified where there is a specific
reason such as specific commands or servers that have very long delay before
returning data.

.. index:: triple: --verify; general options; verify

.. _`--verify general option`:

``--verify`` general option
"""""""""""""""""""""""""""

The pair of ``--verify`` and ``--no-verify`` general options control whether or
not the client verifies any certificates received from the WBEM server.

By default or if ``--verify`` is specified, any certificates returned by the
server are verified. If ``--no-verify`` is specified, any certificates returned
by the server are accepted without verification.

This general option uses the approach with two long option names to allow the
user to specifically enable or disable certificate verification when this
general option is used in interactive mode.

.. index:: triple: --certfile; general options; certfile

.. _`--certfile general option`:

``--certfile`` general option
"""""""""""""""""""""""""""""

The argument value of the ``--certfile`` general option is the file path of a
PEM file containing a X.509 client certificate to be presented to the WBEM
server during the TLS/SSL handshake, enabling 2-way (mutual) authentication.
This option is used only with HTTPS.

If ``--certfile`` is not used, no client certificate is presented to the server,
resulting in 1-way authentication during the TLS/SSL handshake.

For more information on authentication types, see:
https://pywbem.readthedocs.io/en/stable/client/security.html#authentication-types

.. index:: triple: --keyfile; general options; keyfile

.. _`--keyfile general option`:

``--keyfile`` general option
""""""""""""""""""""""""""""

The argument value of the ``--keyfile`` general option is the file path of a
PEM file containing the private key belonging to the public key that is
part of the X.509 certificate. See :ref:`--certfile general option` for more
information.

Not required if the private key is part of the file defined in the
``--certfile`` option. ``--keyfile`` is not allowed if ``--certfile`` is not
provided. Default: No client key file. The client private key should then be
part of the file defined by ``--certfile``.

.. index:: triple: --ca-certs; general options; ca-certs

.. _`--ca-certs general option`:

``--ca-certs`` general option
"""""""""""""""""""""""""""""

The argument value of the ``--ca-certs`` general option specifies which
X.509 certificates are used on the client side for validating the X.509
certificate received from the WBEM server during SSL/TLS handshake when HTTPS
is used.

The client-side and server-side certificates may be CA certificates (i.e.
certificates issued by a certificate authority) or self-signed certificates.

Its value must be one of:

* The path name of a file in `PEM format`_ that contains one or more
  certificates. See the description of the 'CAfile' argument of the
  `OpenSSL SSL_CTX_load_verify_locations() function`_ for details.

* The path name of a directory with files in `PEM format`_, each of which
  contains exactly one certificate. The file names must follow a particular
  naming convention. See the description of the 'CApath' argument of the
  `OpenSSL SSL_CTX_load_verify_locations() function`_ for details.

* The string 'certifi' (only for pywbem version 1.0 or later). This choice will
  cause the certificates provided by the `certifi package`_ to be used. That
  package provides the certificates from the
  `Mozilla Included CA Certificate List`_. Note that this list only contains
  CA certificates, so this choice does not work if the WBEM server uses
  self-signed certificates.

The default behavior depends on the version of the installed pywbem package:

* Starting with pywbem version 1.0, the default is the behavior described
  above for the string 'certifi'.

* Before pywbem version 1.0, the default is the path name of the first existing
  directory from a list of system directories where certificates are expected to
  be stored.

The version of the installed pywbem package can be displayed using the
:ref:`--version general option`.

Specifying the ``--no-verify`` option (see :ref:`--verify general option`)
bypasses client side verification of the WBEM server certificate.

.. _PEM format: https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail
.. _OpenSSL SSL_CTX_load_verify_locations() function: https://www.openssl.org/docs/man1.1.0/ssl/SSL_CTX_load_verify_locations.html
.. _certifi package: https://certifi.io/en/latest/
.. _Mozilla Included CA Certificate List: https://wiki.mozilla.org/CA/Included_Certificates

.. index:: triple: --timestats; general options; timestats

.. _`--timestats general option`:

``--timestats`` general option
""""""""""""""""""""""""""""""

The ``--timestats`` / ``--no-timestats`` \ ``-T`` general option is a boolean
option that enables the display of time statistics on the interactions with the
WBEM server.

When the option is included on the command line, the display of statistics
is enabled after each command in the interactive mode and before exit in the
command mode.

Statistics are always gathered in pywbemcli for the current connection for every
command executed. They can be displayed at any time in the interactive mode with
the command ``statistics show``.


For more information on statistics gathered by pywbemcli and WBEM servers see
section :ref:`Statistics command group` .

.. index:: triple: --use-pull; general options; use-pull

.. _`--use-pull general option`:

``--use-pull`` general option
""""""""""""""""""""""""""""""

The argument value of the ``--use-pull``/``-u`` general option determines
whether the :ref:`pywbem:Pull Operations` or :term:`traditional operations` are
used for the ``instance enumerate``, ``instance references``, ``instance
associators`` and ``instance query`` commands. See
:ref:`Pywbemcli and the DMTF pull operations` for more information on pull
operations. The choices for the argument value are as follows:

* ``yes`` - pull operations will be used and if the server does not
  support pull, the request will fail.
* ``no`` - forces pywbemcli to try only the traditional non-pull operations.
* ``either`` - (default) pywbem tries both; first pull operations and then
  :term:`traditional operations`.  This is the recommended setting since it
  will generate a valid response from any server.

.. index:: triple: --pull-max-cnt; general options; pull-max-cnt

.. _`--pull-max-cnt general option`:

``--pull-max-cnt`` general option
"""""""""""""""""""""""""""""""""

The argument value of the ``--pull-max-cnt`` general option is an integer
passed to the WBEM server with the open and pull operation requests.
This integer tells the server the maximum number of objects
to be returned for each pull request if pull operations are used. This must
be a positive non-zero integer. The default is 1000. See :ref:`Pywbemcli and the
DMTF pull operations` for more information on pull operations.

.. index:: triple: --mock-server; general options; mock-server

.. _`--mock-server general option`:

``--mock-server`` general option
""""""""""""""""""""""""""""""""

The argument value of the ``--mock-server``/``-m`` general option is the file
path of a MOF  or Python script file that loads a mock WBEM server in the
pywbemcli process with mock data (i.e. CIM objects).

This allows users to write MOF and scripts that define a Server environment
including CIM namespaces, CIM qualifier declarations, CIM classes, and CIM instances that
responds to pywbemcli commands.

This option may be specified multiple times to define multiple MOF and Python
files that make up the definition of a mock server. The files must have the
suffix ".mof" for MOF files and ".py" for Python scripts.

When this option is used, the security options (i.e. ``user``, ``password``,
etc.) are irrelevant. They are rejected by pywemcli.

Section :ref:`Mock WBEM server` defines the characteristics of the MOF and
Python files that define a mock server environment.

.. index:: server definition cache: cache server definition

A mock server may be saved in the connections file and is cached if saved in
the default connections file.  This can significantly speed up the loading
of the mock server definition when pywbemcli is started.

The following example creates a mock server with two files defining the mock
data, shows what parameters are defined for the connection, and then saves that
connection named ``mymockserver`` where classdefs.mof could contain CIM qualifier
declarations and CIM class definitions and insts.py could contain CIM
instance definitions:

.. code-block:: text

    $ pywbemcli --mock-server classdefs.mof --mock-server insts.py --default-namespace root/myhome

    pywbemcli> connection show
    name: not-saved (current)
      server:
      mock-server: classdefs.mof, insts.py
      . . .

    pywbemcli> connection save mymockserver
    pywbemcli> connection show
    Connection status:
    name               value  (state)
    -----------------  ------------------------------------------
    name               mock1 (current)
    server
    default-namespace  root/cimv2
    user
    password
    timeout            30
    use-pull
    pull-max-cnt       1000
    verify             True
    certfile
    keyfile
    mock-server        tests/unit/pywbemcli/simple_mock_model.mof
    ca-certs
    pywbemcli>class enumerate --names-only
    CIM_BaseEmb
    CIM_BaseRef
    CIM_Foo
    CIM_FooAssoc
    pywbemcli>


See chapter :ref:`Mock WBEM server` for more information on defining
the files for a mock server.

.. index:: triple: --output-format; general options; output-format

.. _`--output-format general option`:

``--output-format`` general option
""""""""""""""""""""""""""""""""""

The argument value of the ``--output-format``/``-o`` general option is a string
that defines the output format in which the result of any pywbemcli commands
is displayed. The default output format depends on the command.

For details, see :ref:`Output formats`.

.. index:: triple: --log; general options; log

.. _`--log general option`:

``--log`` general option
""""""""""""""""""""""""

The argument value of the  ``--log``/``-l`` general option defines the
destination and parameters of logging of the requests and responses to the WBEM
server.

For details, see :ref:`Pywbemcli defined logging`.

.. index:: triple: --verbose; general options; verbose

.. _`--verbose general option`:

``--verbose`` general option
""""""""""""""""""""""""""""

The ``--verbose``/``-v`` general option is a boolean option that enables the
display of extra information about the processing.

In particular it outputs text for a number of commands that
normally return nothing upon successful execution(ex. instance delete,
instance enumerate that returns no CIM objects) to indicate the successful
command completion.

.. index:: triple: --connections-file; general options; connection-file

.. _`--connections-file general option`:

``--connections-file`` general option
"""""""""""""""""""""""""""""""""""""

The ``--connections-file``/``-C`` general option allows the user to select
a path name for the :term:`connections file`.

By default, the path name of the connections file is the value of the
``PYWBEMCLI_CONNECTIONS_FILE`` environment variable or if not set, the file
``.pywbemcli_connections.yaml`` in the user's home directory.
The user's home directory depends on the operating system used and is
determined with ``os.path.expanduser("~")``, which works on all operating
systems including Windows. See :func:`~py3:os.path.expanduser` for details.

The actually used path name of the connections file is shown in the
:ref:`connection list command`.

The :term:`connection definition` definitions in the connections file are
managed with the commands in the :ref:`connection command group`.

.. index:: triple: --warn; general options; warn

.. _`--warn general option`:

``--warn`` general option
"""""""""""""""""""""""""

The ``--warn``/``--no-warn`` general option is a boolean option that controls
the display of all Python warnings.

If ``--warn`` is used, all Python warnings are shown once. If ``--no-warn`` is
used (default), the ``PYTHONWARNINGS`` environment variable determines which
warnings are shown. If that variable is not set, no warnings are shown. See
`PYTHONWARNINGS <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONWARNINGS>`_
for details.

.. index:: triple: --warn; --no-warn; general options; warnings

.. _`--pdb general option`:

``--pdb`` general option
""""""""""""""""""""""""

The ``--pdb`` general option is a boolean option that enables debugging
with the built-in pdb debugger.

If debugging is enabled, execution of each pywbemcli command will pause just
before the command within pywbemcli is executed, and the pdb debugger prompt
will appear. See `pdb debugger commands`_ for details on how to operate the
built-in pdb debugger.

In addition to the ``--pdb`` option,

An alternate debugger such as `pdb++ debugger` can also be used.

.. _`pdb debugger commands`: https://docs.python.org/2.7/library/pdb.html#debugger-commands

.. _`pdb++ debugger`: https://github.com/pdbpp/pdbpp


.. index:: triple: --version; general options; version

.. _`--version general option`:

``--version`` general option
""""""""""""""""""""""""""""

The ``--version`` general option displays the version of the pywbemcli
command and the version of the pywbem package used by it, and then exits.

.. index:: triple: --help; general options; help

.. _`--help general option`:

``--help`` general option
"""""""""""""""""""""""""

The ``--help``/``-h`` general option displays help text which describes the
command groups, commands,  and general options, and then exits. A specific
help exists for each command group, and command and ``pywbemcli --help``
presents the help on the general options

.. index:: pair: environment variables; general options

.. _`Environment variables for general options`:

Environment variables for general options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:: index:: pair: general options; environment variables

Pywbemcli defines environment variables corresponding to its general options
as follows:

.. table: Environment variables and general options

=================================  =============================
Environment variable               Corresponding general option
=================================  =============================
PYWBEMCLI_SERVER                   ``--server``
PYWBEMCLI_NAME                     ``--name``
PYWBEMCLI_USER                     ``--user``
PYWBEMCLI_PASSWORD                 ``--password``
PYWBEMCLI_OUTPUT_FORMAT            ``--output-format``
PYWBEMCLI_DEFAULT_NAMESPACE        ``--default-namespace``
PYWBEMCLI_TIMEOUT                  ``--timeout``
PYWBEMCLI_KEYFILE                  ``--keyfile``
PYWBEMCLI_CERTFILE                 ``--certfile``
PYWBEMCLI_CA_CERTS                 ``--ca-certs``
PYWBEMCLI_USE_PULL                 ``--use-pull``
PYWBEMCLI_PULL_MAX_CNT             ``--pull-max-cnt``
PYWBEMCLI_STATS_ENABLED            ``--timestats``
PYWBEMCLI_MOCK_SERVER (1)          ``--mock-server``
PYWBEMCLI_LOG                      ``--log``
PYWBEMCLI_PDB                      ``--pdb``
PYWBEMCLI_CONNECTIONS_FILE         ``--connections-file``
PYWBEMCLI_SPINNER                  No option attached
=================================  =============================

Notes:

(1) The ``--mock-server`` general option can be specified multiple times. To
    do that with the PYWBEMCLI_MOCK_SERVER environment variable, separate
    the multiple path names with space.

If these environment variables are set, the corresponding general options
default to the value of the environment variables. If both an environment
variable and its corresponding general option are set, the command line option
overrides the environment variable with no warning.

Environment variables are not provided for command options or command arguments.

In the following example, the pywbemcli command uses server
``http://localhost`` defined by the environment variable:

.. code-block:: text

      $ export PYWBEMCLI_SERVER=http://localhost
      $ pywbemcli class get CIM_ManagedElement
        <displays MOF for CIM_ManagedElement>

The pywbemcli :ref:`Connection export command` outputs the (bash/Windows)
shell commands to set all of the environment variables:

.. code-block:: text

    $ pywbemcli --server http://localhost --user fred connection export
    export PYWBEMCLI_SERVER=http://localhost
    export PYWBEMCLI_NAMESPACE=root/cimv2
    . . .

This can be used to set those environment variables and thus to persist
the connection name in the shell environment, from where it will be used in
any subsequent pywbemcli commands until removed. The following shows the
display of the pywbbemcli environment variables that are set :

.. code-block:: text

    $ eval $(pywbemcli --server http://localhost --user fred)

    $ env | grep PYWBEMCLI
    export PYWBEMCLI_SERVER=http://localhost
    export PYWBEMCLI_NAMESPACE=root/cimv2
    . . .

    $ pywbemcli server namespaces
    . . . <list of namespaces for the defined server>

In addition, an environment variable is provided to disable the
spinner that is displayed when waiting for responses. The environment
variable is ``PYWBEMCLI_SPINNER`` and the spinner is disabled when
this environment variable is set.


.. index::
    pair: pull operations; general options
    single: --use-pull
    single: --pull-max-count
    single: traditional operations

.. _`Pywbemcli and the DMTF pull operations`:

Pywbemcli and the DMTF pull operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DMTF specifications and pywbem includes two ways to execute the enumerate
instance type operations (``Associators``, ``References``,
``EnumerateInstances``, ``ExecQuery``):

* The :term:`traditional operations` (ex. ``EnumerateInstances``) where the
  WBEM server returns all of the response instances as a single response
* The pull operations (ex. ``OpenEnumerateInstances``, etc.) where the
  client and the server cooperate with client requests for Open... and subsequent
  Pull... requests to return groups of response instances.

Pywbem implements an overlay of the above two operations called the ``Iter..``
operations where each ``Iter..`` operation executes either the traditional or
pull operation depending on the :ref:`--use-pull general option` of the
connection.

While the pull operations may not be supported by all WBEM servers they can be
significantly more efficient for large responses when they are available.
Pywbem implements the client side of these operation and pywbemcli provides for
the use of these operations through two general options:

* ``--use-pull`` - This option allows the user to select from the
  the following alternatives:

  * ``either`` - (default) pywbemcli first tries the open operation and if that is not
    implemented by the server retries the operation with the corresponding
    traditional operation. The result of this first operation determines whether
    pull or the traditional operation are used for any further requests
    during the current pywbem interactive session.


  * ``yes`` - Forces the use of the pull operations and fails if that is not
    implemented by the server.

  * ``no`` - Forces the use of the traditional operation.

* ``--pull-max-cnt`` - Sets the maximum count of objects the server is allowed
  to return for each open/pull operation. The default is 1000 objects which
  from experience is a logical choice.

The default alternative ``either`` is probably the most logical setting for
``--use-pull``, unless you are specifically testing the use of pull
operations.

However, there are some limitations with using the ``either`` choice as follows:

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
  deprecated this option and the user cannot depend on it being honored by
  the WBEM server, the most logical solution is to never use this option.

The following example forces the use of the pull operations and expects the
WBEM server to return no more than 10 instances per request. It fails if the
pull operations are not supported in the WBEM server:

.. code-block:: text

    $ pywbemcli --server http://localhost --use-pull=yes --pull-max-cnt=10 instance enumerate CIM_Foo


.. _`Output formats`:

Output formats
^^^^^^^^^^^^^^

Pywbemcli supports multiple output formats to present command results. The
output format can be selected with the :ref:`--output-format general option`.
The allowed output formats are different for the various command groups and
commands.

The output formats fall into the following groups:

* **Table formats** - The :ref:`Table formats` format the result as a table
  with rows and columns. Many of the result types allow table formatted
  response display including:

  * ``instance get``, ``instance enumerate``, ``instance references``,
    ``instance associators`` where the table formats are alternatives to the
    CIM model formats that shows the properties for each instance as a column
    in a table.
  * ``instance count``
  * ``server`` commands
  * ``class find``
  * ``connection`` commands

* **CIM object formats** - The :ref:`CIM object formats` format a result that
  consists of CIM objects in MOF, CIM-XML or pywbem repr format. All of the
  commands that return CIM objects support these output formats.

* **ASCII tree format** - The :ref:`ASCII tree format` formats the result
  as a tree, using ASCII characters to represent the tree to show the
  hierarchial relationship between CIM classes. The only command supporting the
  ASCII tree format is ``class tree``, and it supports only that one output
  format.  The tree format is not supported by any other command today.

* **TEXT format** - The :ref:`Text formats` is used for commands that output
  small quantites of text (ex. the interop namespace name) and that could be
  used as part of a command line redirection.

When an unsupported output format is specified for a command response, it is
rejected with an exception.  For example, the command ``class enumerate`` only
supports the :ref:`CIM object formats` and will generate an exception if the
command ``pywbemcli -o table class enumerate`` is entered.

.. index:: single: output formats

.. _`Output formats for groups and commands`:

Output formats for groups and commands
""""""""""""""""""""""""""""""""""""""

Each of the commands may allow only a subset of the possible ouput formats. Thus,
the `server brand` only outputs data in a table format so there is no defined
default format for the :ref:`--output-format general option`.

The following shows the default format for each command and the alternate
formats where the values mean:

objects: ``xml``, ``repr``, or ``txt``

table: ``table``, ``plain``, ``simple``, ``grid``, ``psql``, ``rst``, ``text``,
or ``html``

========== ============= ======== ============== ============================================
Group      Command       Default  Alternates     Comments
========== ============= ======== ============== ============================================
class      associators   'mof'    objects        See Note 1 below
class      delete        None     None           Nothing returned
class      enumerate     'mof'    objects        See Note 1 below
class      find          'simple' table
class      get           'mof'    objects        See Note 1 below
class      invokemethod  'mof'    objects        See Note 1 below
class      references    'mof'    objects        See Note 1 below
class      tree          None     None           Only outputs as ascii tree
instance   associators   'mof'    objects, table Output as cim object or table of properties
instance   count         'simple' table
instance   create        None     None           Nothing returned
instance   delete        None     None           Nothing returned
instance   enumerate     'mof'    objects, table
instance   get           'mof'    objects, table
instance   invokemethod  'mof'    objects, table
instance   modify        None     None           Nothing returned
instance   references    'mof'    table
qualifier  enumerate     'mof'    table
qualifier  get           'mof'    table
server     brand         'text'   text           Alternate is table format
server     centralinsts  'simple' table
server     info          'simple' table
server     interop       'text'   text           Alternate is table format
server     namespaces    'simple' table          Alternate is text format
server     profiles      'simple' table
connection delete        None     table
connection export        None     table
connection list          'simple' table
connection save          None     table
connection select        None     None
connection show          None     None           Currently ignores output format
connection test          None     None
========== ============= ======== ============== ============================================

NOTES:

1. The display of classes with the ``--names-only``/``--no`` or
   ``--summary``/``-s`` command options allows table output formats in addition
   to the objects output formats.

.. index:: pair: output formats; table formats

.. _`Table formats`:

Table formats
"""""""""""""

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


.. index::
    pair: CIM object output formats; output formats
    pair: output formats; MOF

.. _`CIM object formats`:

CIM object formats
""""""""""""""""""

The output of CIM objects allows multiple formats as follows:

* ``--output-format mof``: Format for CIM classes, CIM instances, and CIM Parameters.

  :term:`MOF` is the format used to define and document the CIM models released
  by the DMTF and SNIA. It textually defines the components and structure and
  data of CIM elements such as classes, instances, and qualifier declarations
  as shown in the following example of a CIM instance:

  .. code-block:: text

      instance of CIM_Foo {
         InstanceID = "CIM_Foo1";
         IntegerProp = 1;
      };

  The MOF output of CIM classes, CIM instances or CIM qualifier declaractions
  is normally compiler ready and can be recompiled by a MOF compiler such
  as the :ref:`pywbem MOF compiler <pywbem:MOF Compiler>`.

  The :class:`~pywbem.CIMInstanceName` object (i.e. instance path) does not have a
  MOF format. Rather it is a formatted UNICODE string format as documented in
  DMTF specifications :term:`DSP0004` and :termL`DSP0207`.

  The following is an example of the output of an instance of
  :class:`~pywbem.CIMInstanceName`:

    //ACME.com/cimv2/Test:CIM_RegisteredProfile.InstanceID="Acme.1"


* ``--output-format xml``: :term:`CIM-XML` format for CIM elements such as classes,
  instances and qualifier declarations. Besides being used as a protocol for WBEM
  servers, CIM-XML is also an alternative format for representing the CIM models
  released by the DMTF and SNIA. The XML syntax is defined in the DMTF
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

  This is the structure and data of the pywbem Python objects representing each
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
  the ``__str__()`` method of the Python class for each CIM object to output.

  Thus, for example, a ``class enumerate`` command of a model with only a single
  class creates output of the form:

  .. code-block:: text

      CIMClass(classname='CIM_Foo', ...)


.. _`ASCII tree format`:

ASCII tree format
"""""""""""""""""

This output format is an ASCII based output that shows the tree structure of
the results of the ``class tree`` command. It is the only output format
supported by this command, and therefore it is automatically selected and
cannot be specified explicitly with the :ref:`--output-format general option`.

.. code-block:: text

    $ pywbemcli --mock-server tests/unit/simple_mock_model.mof class tree
    root
    +-- CIM_Foo
        +-- CIM_Foo_sub
        |   +-- CIM_Foo_sub_sub
        +-- CIM_Foo_sub2

This shows a very simple mock repository with 4 classes where CIM_Foo is the
top level in the hierarchy, CIM_Foo_sub and CIM_Foo_sub2 are its subclasses, and
CIM_Foo_sub_sub is the subclass of CIM_Foo_sub.

.. index:: pair: output formats; text formats

.. _`Text formats`:

Text formats
""""""""""""

The TEXT format group outputs the data returned from the command as text
to the console without any formatting except for formatting lists and
comma separated strings.  It is useful for use with data that might be
redirected to other commands or output that is simple enough that a single
line of output is sufficient.

.. code-block:: text

    $ pywbemcli --mock-server tests/unit/testmock/wbemserver_mock.py -o table server namespaces
    Server Namespaces:
    Namespace Name
    ----------------
    interop

    $ pywbemcli --mock-server tests/unit/testmock/wbemserver_mock.py -o text server namespaces
    interop



.. _`Pywbemcli defined logging`:

Pywbemcli defined logging
"""""""""""""""""""""""""

Pywbemcli provides logging to either a file or the standard error stream
of information passing between the pywbemcli client and a WBEM server using the
standard Python logging facility.

Logging is configured and enabled using the :ref:`--log general option` on the
commmand line or the `PYWBEMCLI_LOG` environment variable.

Pywbemcli can log operation calls that send
requests to a WBEM server and their responses and the HTTP messages between
the pywbemcli client and the WBEM server including both the pywbem APIs
and their responses and the HTTP requests and responses.

The default is no logging if the ``--log`` option is not specified.

The argument value of the ``--log`` option and the value of the `PYWBEMCLI_LOG`
environment variable is a log configuration string with the format defined in
the ABNF rule ``LOG_CONFIG_STRING``, below. The log configuration string
defines a list of
one or more log configurations, each with fields ``COMPONENT``, ``DESTINATION``,
and ``DETAIL``:

.. code-block:: text

    LOG_CONFIG_STRING := CONFIG [ "," CONFIG ]
    CONFIG            := COMPONENT [ "=" DESTINATION [ ":" DETAIL ]]
    COMPONENT         := ( "all" / "api" / "http" )
    DESTINATION       := ( "stderr" / "file" )
    DETAIL            := ( "all" / "path" / "summary" )

For example the following log configuration string logs the pywbem API calls
and writes summary information to a log file and the HTTP requests and
responses to stderr:

.. code-block:: text

    $ pywbemcli --log api=file:summary,http=stderr

The simplest log configuration string to enable logging is ``all=stderr`` or
``all=file``.

The ``COMPONENT`` field defines the component for which logging is enabled:

* ``api`` - Logs the calls to the pywbem methods that make requests to a
  WBEM server. This logs both the requests and response including any
  exceptions generated by error responses from the WBEM server.
* ``http`` - Logs the headers and data for HTTP requests and responses to the
  WBEM server.
* ``all`` - (Default) Logs both the ``api`` and ``http`` components.

The ``DESTINATION`` field specifies the log destination:

* ``stderr`` - Output log to stderr.
* ``file`` - (default) Log to the pywbemcli log file ``pywbemcli.log`` in
  the current directory.  Logs are appended to an existing log file.

The ``DETAIL`` component of the log configuration string defines the level of
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

The log output is routed to the output defined by ``DESTINATION`` and includes the
information determined by the ``COMPONENT`` and ``DETAIL`` fields.

The log output format is:

.. code-block:: text

    <Date time>-<Component>.<connection id>-<Direction>:<connection id> <PywbemOperation>(<data>)

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


.. index:: single: connection definitions

.. _`Pywbemcli persisted connection definitions`:

Pywbemcli persisted connection definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pywbemcli can manage persisted connection definitions via the
:ref:`Connection command group`. These connection definitions are persisted in
a :term:`connections file` named ``.pywbemcli_connections.yaml`` in
the user's home directory. A connection definition has a name
and defines all parameters necessary to connect to a WBEM server. Once defined
these connection definitions can be used with the :ref:`--name general option`
or in the interactive mode by defining a current connection with the
:ref:`connection select command`.

A new persistent connection definition can be created with the
:ref:`connection save command`.

At any point in time, pywbemcli can communicate with only a single WBEM server.
That is the *current connection*.
In the command mode, this is the WBEM server defined by the general options
``--server`` or ``--mock-server`` or ``--name``.  In the interactive mode, the
current connection can be changed within an interactive session using the
:ref:`connection select command` so that within a single session, the user can
work with multiple WBEM servers (at different points in time).

The following example creates a persisted connection definition, using
interactive mode:

.. code-block:: text

    $ pywbemcli

    pywbemcli> --server http://localhost --user usr1 --password blah connection save testconn

    pywbemcli> connection list
    WBEM server connections: (#: default, *: current)
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+
    | name      | server           | namespace   | user   |   timeout | verify   | mock-server                            |
    |-----------+------------------+-------------+--------+-----------+----------+----------------------------------------|
    | testconn  | http://localhost | root/cimv2  | usr1   |        30 | True     |                                        |
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+

Since the connection definition is persisted, it is available in command mode
as well as in new interactive sessions:

.. code-block:: text

    $ pywbemcli connection list
    WBEM server connections: (#: default, *: current)
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+
    | name      | server           | namespace   | user   |   timeout | verify   | mock-server                            |
    |-----------+------------------+-------------+--------+-----------+----------+----------------------------------------|
    | testconn  | http://localhost | root/cimv2  | usr1   |        30 | True     |                                        |
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+

    $ pywbemcli

    pywbemcli> connection list
    WBEM server connections: (#: default, *: current)
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+
    | name      | server           | namespace   | user   |   timeout | verify   | mock-server                            |
    |-----------+------------------+-------------+--------+-----------+----------+----------------------------------------|
    | testconn  | http://localhost | root/cimv2  | usr1   |        30 | True     |                                        |
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+

Other connection definitions can be added, this time using command mode:

.. code-block:: text

    $ pywbemcli --server http://blah2 --user you --password xxx connection save Ronald

    $ pywbemcli connection list
    WBEM server connections: (#: default, *: current)
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+
    | name      | server           | namespace   | user   |   timeout | verify   | mock-server                            |
    |-----------+------------------+-------------+--------+-----------+----------+----------------------------------------|
    | Ronald    | http://blah2     | root/cimv2  | you    |        30 | True     |                                        |
    | testconn  | http://localhost | root/cimv2  | usr1   |        30 | True     |                                        |
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+

The following example shows how to select current connections in interactive
mode. Note the marker ``*`` in front of the name, which indicates the current
connection. The :ref:`connection show command` when used without a connection
name shows the current connection:

.. code-block:: text

    $ pywbemcli

    pywbemcli> connection select Ronald

    pywbemcli> connection list
    WBEM server connections: (#: default, *: current)
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+
    | name      | server           | namespace   | user   |   timeout | verify   | mock-server                            |
    |-----------+------------------+-------------+--------+-----------+----------+----------------------------------------|
    | *Ronald   | http://blah2     | root/cimv2  | you    |        30 | True     |                                        |
    | testconn  | http://localhost | root/cimv2  | usr1   |        30 | True     |                                        |
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+

    pywbemcli> connection show
    name: Ronald (current)
      server: http://blah2
      mock-server:
      . . .

    pywbemcli> connection select testconn

    pywbemcli> connection list
    WBEM server connections: (#: default, *: current)
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+
    | name      | server           | namespace   | user   |   timeout | verify   | mock-server                            |
    |-----------+------------------+-------------+--------+-----------+----------+----------------------------------------|
    | Ronald    | http://blah2     | root/cimv2  | you    |        30 | True     |                                        |
    | *testconn | http://localhost | root/cimv2  | usr1   |        30 | True     |                                        |
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+

    pywbemcli> connection show
    name: testconn (current)
      server: http://localhost
      mock-server:
      . . .

    pywbemcli> connection show Ronald
    name: Ronald
      server: http://blah2
      mock-server:
      . . .

The concept of a current connection that can be selected is useful mostly for
the interactive mode. In command mode, the connection specified with one of the
``-server``, ``--mock-server``, or ``--name`` general options automatically is
considered the current connection, and there is no concept of selecting a
current connection other than using these options.
Therefore, pywbemcli additionally supports the concept of a persisted default
connection.

The following example defines a persisted default connection and then uses it in
command mode:

.. code-block:: text

    $ pywbemcli connection select Ronald --default
    "Ronald" default and current

    $ pywbemcli connection list
    WBEM server connections: (#: default, *: current)
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+
    | name      | server           | namespace   | user   |   timeout | verify   | mock-server                            |
    |-----------+------------------+-------------+--------+-----------+----------+----------------------------------------|
    | #Ronald   | http://blah2     | root/cimv2  | you    |        30 | True     |                                        |
    | testconn  | http://localhost | root/cimv2  | usr1   |        30 | True     |                                        |
    +-----------+------------------+-------------+--------+-----------+----------+----------------------------------------+

    $ pywbemcli connection show
    name: Ronald (default, current)
      server: http://blah2
      mock-server:
      . . .

Connections can be deleted with the ``connection delete`` command either with
the command argument containing the connection name or with no name provided so
pywbemcli presents a list of connections to choose from:

.. code-block:: text

    $ pywbemcli connection delete Ronald
    Deleted default connection "Ronald".

or:

.. code-block:: text

    $ pywbemcli connection delete
    Select a connection or <CTRL-C> to abort.
    0: Ronald
    1: testconn
    Input integer between 0 and 1 or Ctrl-C to exit selection: 0
    Deleted default connection "Ronald".
