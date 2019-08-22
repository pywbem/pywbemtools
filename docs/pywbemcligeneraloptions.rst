.. _`Pywbemcli command line general options`:

Pywbemcli command line general options
======================================


.. _`General options overview`:

General options overview
------------------------

The general options are entered before the command-group or command. They
define:

* Characteristics of the WBEM server against which the commands are to be
  executed (i.e url, default-namespace, security parameters, etc.)
* Execution options that apply to multiple commands (i.e. output
  formats, statistics keeping, logging and using pull operations).
* General options to show version, display additional information.

For example the following enumerates the qualifier declarations and outputs the
result as a ``simple`` table:

.. code-block:: text

    pywbemcli --output-format simple qualifier enumerate

    or

    pywbemcli -o simple qualifier enumerate

In the interactive mode, the general options from the command line are defined
once and retain their value throughout the execution of the interactive mode.

However, they may be modified in the interactive mode by entering them before
the COMMAND.  Thus, for example to display the qualifier declarations in
interactive mode and as a table:

.. code-block:: text

   $ pywbemcli

   pywbemcli> --output-format table qualifier enumerate

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


General options descriptions
----------------------------

The pywbemcli command line options are as follows (The following complements
the exact help text output shown in section :ref:`pywbemcli Help Command
Details`):

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

  Examples for the `URL` parameter of this option:

  .. code-block:: text

      https://localhost:15345 (http port 5989, host name localhost)
      http://10.2.3.9 (port 5988, ipv4 ip address 10.2.3.9)
      http://[2001:db8::1234-eth0] -(http port 5988 ipv6, zone id eth0)

* **--name/-n** - The name of a WBEM server that is defined in the
  :term:`connections file`.  The server parameters for this connection name will
  be loaded from the :term:`connections file` to become the current WBEM
  connection in pywbemcli. Note: In the interactive mode a connection is not
  actually used until a command requiring access to the WBEM server is entered.
  This option is mutually exclusive with ``--server`` and ``--mock-server``
  since each option defines a WBEM server for pywbemcli.

  A new WBEM server named (``myserver``) may be defined and saved in the connection
  file with command as follows:

  .. code-block:: text

     $ pywbemcli connection add --server http://localhost --user me --password mypw --name myserver

  To use an existing WBEM server named ``myserver`` in the defined connections:

  .. code-block:: text

     $ pywbemcli --name myserver class get CIM_ManagedElement
       <<... returns mof for CIM_ManagedElement>>>

  See :ref:`Connection command-group` for more information on managing
  connections.
* **--default-namespace/-d** - Default :term:`CIM namespace` to use in the target
  WBEM server if no namespace is defined in a command. If not defined the
  pywbemcli default is ``root/cimv2``.  This is the namespace used on all
  server operation requests unless a specific namespace is defined by:

  * In the interactive mode prepending the command-group name with the
    ``--namespace`` option.
  * Using the ``--namespace/-n`` command option to define a namespace
    on subcommands that specify this option.
  * Executing a command that looks in multiple namespaces (ex. ``class find``).
* **--user/-u** - User name for the WBEM server if a user name is required to
  authenticate the client.
* **--password/-p** - Password for the WBEM server. This option is normally
  required if the ``--user/-u`` option is defined.  If the ``--password``
  option is not used when ``--user/-u`` - is set, pywbemcli will prompt for
  the password.  If passwords are saved into the :term:`connections file` they
  are not encrypted in the file.
  See :ref:`Avoiding password prompts`.
* **--no-verify/-n** - If set, client does not verify server certificate. Any
  certificate returned by the server is accepted.
* **--certfile** - Server certificate file. Not used if ``--no-verify/-n`` set or
  the connection does not use SSL (i.e. ``--server http://blah``)
* **--keyfile** - Client private key file for the server to use to authenticate
  the client if that is required by the WBEM server.
* **--output-format/-o** - Output format choice (Default: mof).
  Note that the actual output format may differ from this value because some
  subcommands only allow selected formats.  See :ref:`Output formats` for
  detailed information on the output formats.
* **--use-pull-ops** [ ``yes`` | ``no`` | ``either`` ] - Determines
  whether the pull operations are used for ``EnumerateInstances``,
  ``AssociatorInstances``, ``ReferenceInstances``, and ``ExecQuery`` operations,
  See :ref:`Pywbemcli and the DMTF pull operations` for more information on
  pull operations:

  * ``yes`` -  pull requests will be used and if the server does not
    support pull, the operation will fail.
  * ``no`` - forces pywbemcli to try only the traditional non-pull operations.
  * ``either`` - (default) pywbem tries both; first pull and then traditional
    operations.

* **--pull-max-cnt** -  controls the CIM-XML open and pull request parameter
  ``MaxObjectCount`` that tells the server the maximum number of objects
  to be returned for each pull request if pull operations are used. This must
  be  a positive non-zero integer. The default is 1000. See :ref:`Pywbemcli and the
  DMTF pull operations` for more information on pull operations.
* **--mock-server/-m** - Defines one or more files that define a mock server that
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
* **--version/-V** - Show the version of this command and of the pywbem package
  imported then exit.
* **--help/-h** - Show the help which describes the command line options and exit.


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
PYWBEWCLI_CACERTS               ``--ca-certs``
PYWBEMCLI_USE_PULL              ``--use-pull-ops``
PYWBEMCLI_PULL_MAX_CNT          ``--pull-max-cnt``
PYWBEMCLI_STATS_ENABLED         ``--timestats``
PYWBEMCLI_MOCK_SERVER           ``--mock-server``
PYWBEMCLI_LOG                   ``--log``
==============================  ============================

If these environment variables are set, the corresponding general options on the
command line are not required and the value of the environment variable is
used. If both the env var and the command line option are included the
command line option overrides the environment variable with no warning.

Environment variable options are not provided for command/subcommand
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



.. _`Pywbemcli and the DMTF pull operations`:

Pywbemcli and the DMTF pull operations
--------------------------------------

For DMTF CIM-XML operations that can return many objects the DMTF CIM-XML protocol
allows two variations on the enumerate operations (enumerate and an operation
sequence of ``OpenEnumerateInstances``/``PullInstances``).

While the pull operation may not be supported by all WBEM servers  they can be
significantly more efficient when they are available.  Pywbem implements the
client side of these operation and pywbemcli provides for the use of these
operations through two general options:

* ``--use-pull-ops`` - This option allows the user to select from the
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

  There are issues with using the the ``either`` choice as follows"

  * The original operations did not support the filtering of responses  with a
    query language query (``--filter-query-language`` and ``--filter-query``)
    option which passes a filter query to the WBEM server so that it filters
    the responses before they are returned. This can greatly reduce the size of
    the responses if effectively used but is used only when the pull operations
    are available on the server.

  * The pull operations do not support some of the options that traditional
    operations do:

    * ``--include-qualifiers`` - Since even the traditional operations specification
      deprecated this option and the user cannot depend on it being honored,
      the most logical solution is to never use this option.

    * ``--local-nly`` - Since even the traditional operations specification
      deprecated this options and the user cannot depend on it being honored by
      the WBEM server the most logical solution is to never use this option.


.. _`Output formats`:

Output formats
--------------

Pywbemcli supports various output formats for the results. The output format
can be selected with the ``--output-format/-o`` option.

The output formats fall into three groups. However, not all formats are
applicable to all subcommands:

* **Table formats** - The :ref:`Table formats` display the output as a table with
  rows and columns. For example output of CIM instances shows each property as
  a column with the data for each instance in a row.
* **CIM object formats** - The :ref:`CIM object formats` display of returned CIM
  objects in formats specific to the CIM Model and also the pywbem implementation
  of the CIM model (ex. DMTF MOF and XML formats and pywbem repr and string
  formats).
* **ASCII tree format** - The :ref:`ASCII tree format` provides a tree display
  of results that is logical to display as a tree.  Thus, the command
  ``pywbemcli class tree . . .`` which shows the hierarchy of the CIM classes
  defined by a WBEM server uses the tree output format.

The goal of the ``--output-format`` general option is to define the prefered
value for either the table output format or the CIM object format for the
command or interactive session.

Not all commands output in all possible formats.  There are be cases where
even if the format set to a table format ``--output simple`` the display will
be in the CIM model format. Some specific cases include:

1. The output of the class commands enumerate, get, references, associators with
   classes is always in one of the CIM model formats, not a table.

2. Connection commands like ``list`` only output a table oriented
   set of values, not CIM objects.  Therefore, they always output in table formats
   and if the output_format is set to, for example, ``mof`` they still output
   as a table using the default value of the table formats. If the the output
   format definition is ``mof``, they will output in the default table format.

3. The server commands only outputs table oriented information. not CIM
   objects so the output is either the default or specified table format.

3. The command ``class tree`` outputs a hiearchy of classes and therefore
   the only defined output for this command is the ascii tree format.


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

* ``output-format mof xml``: :term:`CIM-XML` format for CIM elements such as classes,
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

* ``output-format mof repr``: Python repr format of the objects.

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


* ``-o txt``: Python str format of the objects.

    This should be considered the output of last resort as it simply uses
    the __str__ method of each command to output.

    Thus, for example the a ``class enumerate`` of a model with only a single
    class is of the form:

    .. code-block:: text

        CIMClass(classname='CIM_Foo', ...)

.. _`ASCII tree format`:

ASCII tree format
^^^^^^^^^^^^^^^^^
This output format is an ASCII based output that shows the tree structure of
the results of certain subcommands.  It is used specifically to show the
class class hierarchy tree from the command ``class tree`` as follows:

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

The value of the the `--log` option parameter and of the PYWBEMCLI_LOG
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

Pywbemcli can manage connections via the :ref:`connection command-group`. These
connections are persisted in a :term:`connections file` named
`pywbemcli_connections.json` in the current directory. A connection has a name
and defines all parameters necessary to connect to a WBEM server. Once defined
these connections can be accessed with the general option ``--name`` or in the
interactive mode the ``connection select` command.

A new persistent connection definition can be created  by executing
pywbemcli with the ``connection add`` command. The options on this command will
define the WBEM server and its security characteristics, a name for that server
and save the result to the :term:`connections file`

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
using the add subcommand:

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

