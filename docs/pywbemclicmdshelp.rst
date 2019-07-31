
.. _`pywbemcli Help Command Details`:

pywbemcli Help Command Details
==============================


This section defines the help output for each pywbemcli command group and subcommand.



The following defines the help output for the `pywbemcli  --help` subcommand


::

    Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...

      Pywbemcli is a command line WBEM client that uses the DMTF CIM/XML
      protocol to communicate with WBEM servers. Pywbemcli can:

          * Manage the information in WBEM Servers CIM objects using the
            operations defined in the DMTF specification.  It can manage CIM
            classes, CIM instances and CIM qualifier declarations in the WBEM
            Server and execute CIM methods and queries on the server.

          * Inspect WBEM Server characteristics including namespaces, registered
            profiles, and other server information.

          * Capture detailed information on communication with the WBEM
            server including time statistics and logs of the operations.

          * Maintain a persistent list of named WBEM servers and execute
            operations on them by name.

      Pywbemcli implements command groups and subcommands to execute the CIM/XML
      operations defined by the DMTF CIM Operations Over HTTP
      specification(DSP0201) specification.

      The general options shown below can also be specified on any of the
      (sub)commands as well as the command line.

      For more detailed information, see:

          https://pywbemtools.readthedocs.io/en/latest/

    Options:
      -s, --server URI                Hostname or IP address with scheme of the
                                      WBEMServer in format:
                                      [{scheme}://]{host}[:{port}]
                                      The server
                                      parameter is conditionally optional (see
                                      --name)
                                      * Scheme: must be "https" or "http"
                                      [Default: "https"]
                                      * Host: defines
                                      short/fully qualified DNS hostname, literal
                                      IPV4 address (dotted), or literal IPV6
                                      address
                                      * Port: (optional) defines WBEM
                                      server port to be used [Defaults: 5988(HTTP)
                                      and 5989(HTTPS)].
                                      (EnvVar:
                                      PYWBEMCLI_SERVER).
      -n, --name NAME                 Name for the connection.  If this option
                                      exists and the server option does not exist
                                      pywbemcli retrieves the connection
                                      information from the connections file
                                      (pywbemcliservers.json). If the server
                                      option and this option does not exist
                                      --server is used as the connection
                                      definition with  "default" as the name.This
                                      option and --server are mutually exclusive
                                      except when defining a new server from the
                                      command line(EnvVar: PYWBEMCLI_NAME).
      -d, --default_namespace NAMESPACE
                                      Default Namespace to use in the target WBEM
                                      server if no namespace is defined in a
                                      subcommand(EnvVar: PYWBEMCLI_NAME)
                                      []Default: root/cimv2].
      -u, --user USER                 User name for the WBEM Server connection.
                                      (EnvVar: PYWBEMCLI_NAME)
      -p, --password PASSWORD         Password for the WBEM Server. Will be
                                      requested as part  of initialization if user
                                      name exists and it is not  provided by this
                                      option.(EnvVar: PYWBEMCLI_PASSWORD).
      -t, --timeout INTEGER           Client timeout completion of WBEM server
                                      operation in seconds.
                                      (EnvVar:
                                      PYWBEMCLI_PYWBEMCLI_TIMEOUT)
      -N, --noverify                  If set, client does not verify WBEM server
                                      certificate.(EnvVar: PYWBEMCLI_NOVERIFY).
      -c, --certfile TEXT             Server certfile. Ignored if --noverify flag
                                      set. (EnvVar: PYWBEMCLI_CERTFILE).
      -k, --keyfile FILE PATH         Client private key file. (EnvVar:
                                      PYWBEMCLI_KEYFILE).
      --ca_certs TEXT                 File or directory containing certificates
                                      that will be matched against certificate
                                      received from WBEM server. Set --no-verify-
                                      cert option to bypass client verification of
                                      the WBEM server certificate.  (EnvVar:
                                      PYWBEMCLI_CA_CERTS).
                                      [Default: Searches for
                                      matching certificates in the following
                                      system directories: /etc/pki/ca-
                                      trust/extracted/openssl/ca-bundle.trust.crt]
                                      /etc/ssl/certs]
                                      /etc/ssl/certificates]
      -o, --output-format <choice>    Choice for command output data format.
                                      pywbemcli may override the format choice
                                      depending on the command group and command
                                      since not all formats apply to all output
                                      data types. Choices further defined in
                                      pywbemcli documentation.
                                      Choices: Table:
                                      [table|plain|simple|grid|psql|rst|html],
                                      Object: [mof|xml|txt|tree]
                                      [Default:
                                      "simple"]
      -U, --use-pull-ops [yes|no|either]
                                      Determines whether pull operations are used
                                      for EnumerateInstances, AssociatorInstances,
                                      ReferenceInstances, and ExecQuery
                                      operations.
                                      * "yes": pull operations
                                      required; if server does not support pull,
                                      the operation fails.
                                      * "no": forces
                                      pywbemcli to use only the traditional non-
                                      pull operations.
                                      * "either": pywbemcli trys
                                      first pull and then  traditional operations.
                                      (EnvVar: PYWBEMCLI_USE_PULL_OPS) [Default:
                                      either]
      --pull-max-cnt INTEGER          Maximium object count of objects to be
                                      returned for each request if pull operations
                                      are used. Must be  a positive non-zero
                                      integer.(EnvVar: PYWBEMCLI_PULL_MAX_CNT)
                                      [Default: 1000]
      -T, --timestats                 Show time statistics of WBEM server
                                      operations after each command execution.
      -l, --log COMP=DEST:DETAIL,...  Enable logging of CIM Operations and set a
                                      COMPONENT to a log level, DESTINATION, and
                                      DETAIL level.
                                      * COMP: [api|http|all],
                                      Default: all
                                      * DEST: [file|stderr], Default:
                                      file
                                      * DETAIL:[all|paths|summary], Default:
                                      all
      -v, --verbose                   Display extra information about the
                                      processing.
      -m, --mock-server FILENAME      Defines, a mock WBEM server as the target
                                      WBEM server. The option value defines a MOF
                                      or Python file path used to populate the
                                      mock repository. This option may be used
                                      multiple times where each use defines a
                                      single file_path.See the pywbemtools
                                      documentation for more information.(EnvVar:
                                      PYWBEMCLI_MOCK_SERVER).
      --version                       Show the version of this command and the
                                      pywbem package and exit.
      -h, --help                      Show this message and exit.

    Commands:
      class       Command group to manage CIM classes.
      connection  Command group to manage WBEM connections.
      help        Show help message for interactive mode.
      instance    Command group to manage CIM instances.
      qualifier   Command group to view QualifierDeclarations.
      repl        Enter interactive (REPL) mode (default).
      server      Command Group for WBEM server operations.


.. _`pywbemcli class --help`:

pywbemcli class --help
----------------------



The following defines the help output for the `pywbemcli class --help` subcommand


::

    Usage: pywbemcli class [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group to manage CIM classes.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      associators   Get the associated classes for CLASSNAME.
      delete        Delete a single CIM class.
      enumerate     Enumerate classes from the WBEM Server.
      find          Find all classes that match CLASSNAME-GLOB.
      get           Get and display a single CIM class.
      invokemethod  Invoke the class method named methodname.
      references    Get the reference classes for CLASSNAME.
      tree          Display CIM class inheritance hierarchy tree.


.. _`pywbemcli class associators --help`:

pywbemcli class associators --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class associators --help` subcommand


::

    Usage: pywbemcli class associators [COMMAND-OPTIONS] CLASSNAME

      Get the associated classes for CLASSNAME.

      Get the classes(or class names) that are associated with the CLASSNAME
      argument filtered by the --assocclass, --resultclass, --role and
      --resultrole options and modified by the other options.

      Results are formatted as defined by the output format general option.

    Options:
      -a, --assocclass <class name>   Filter by the association class name
                                      provided. Each returned class (or class
                                      name) should be associated to the source
                                      class through this class or its subclasses.
                                      Optional.
      -C, --resultclass <class name>  Filter by the association result class name
                                      provided. Each returned class (or class
                                      name) should be this class or one of its
                                      subclasses. Optional
      -r, --role <role name>          Filter by the role name provided. Each
                                      returned class (or class name)should be
                                      associated with the source class (CLASSNAME)
                                      through an association with this role
                                      (property name in the association that
                                      matches this parameter). Optional.
      -R, --resultrole <role name>    Filter by the result role name provided.
                                      Each returned class (or class name)should be
                                      associated with the source class (CLASSNAME)
                                      through an association with returned object
                                      having this role (property name in the
                                      association that matches this parameter).
                                      Optional.
      --no-qualifiers                 If set, request server to not include
                                      qualifiers in the returned class(s). The
                                      default behavior is to request qualifiers in
                                      returned class(s).
      -c, --includeclassorigin        Request that server include classorigin in
                                      the result.On some WBEM operations, server
                                      may ignore this option.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      option not specified a Null property list is
                                      created and the server returns all
                                      properties. Multiple properties may be
                                      defined with either a comma separated list
                                      or by using the option multiple times. (ex:
                                      -p pn1 -p pn22 or -p pn1,pn2). If defined as
                                      empty string the server should return no
                                      properties.
      -o, --names-only                Retrieve only the returned object names.
      -s, --sort                      Sort into alphabetical order by classname.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli class delete --help`:

pywbemcli class delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class delete --help` subcommand


::

    Usage: pywbemcli class delete [COMMAND-OPTIONS] CLASSNAME

      Delete a single CIM class.

      Deletes the CIM class defined by CLASSNAME from the WBEM Server.

      If the class has instances, the command is refused unless the --force
      option is used. If --force is used, instances are also deleted.

      If the class has subclasses, the command is rejected.

      WARNING: Removing classes from a WBEM Server can cause damage to the
      server. Use this with caution.  It can impact instance providers and other
      components in the server.

      Some servers may refuse the operation.

    Options:
      -f, --force             Force the delete request to be issued even if there
                              are instances in the server or subclasses to this
                              class. The WBEM Server may still refuse the request.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli class enumerate --help`:

pywbemcli class enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class enumerate --help` subcommand


::

    Usage: pywbemcli class enumerate [COMMAND-OPTIONS] CLASSNAME

      Enumerate classes from the WBEM Server.

      Enumerates the classes (or classnames) from the WBEMServer starting either
      at the top of the class hierarchy or from  the position in the class
      hierarchy defined by `CLASSNAME` argument if provided.

      The output format is defined by the output-format general option.

      The includeclassqualifiers, includeclassorigin options define optional
      information to be included in the output.

      The deepinheritance option defines whether the complete hiearchy is
      retrieved or just the next level in the hiearchy.

      Results are formatted as defined by the output format general option.

    Options:
      -d, --deepinheritance     Return complete subclass hierarchy for this class
                                if set. Otherwise retrieve only the next hierarchy
                                level.
      -l, --localonly           Show only local properties of the class.
      --no-qualifiers           If set, request server to not include qualifiers
                                in the returned class(s). The default behavior is
                                to request qualifiers in returned class(s).
      -c, --includeclassorigin  Request that server include classorigin in the
                                result.On some WBEM operations, server may ignore
                                this option.
      -o, --names-only          Retrieve only the returned object names.
      -s, --sort                Sort into alphabetical order by classname.
      -n, --namespace <name>    Namespace to use for this operation. If defined
                                that namespace overrides the general options
                                namespace
      -S, --summary             Return only summary of objects (count).
      -h, --help                Show this message and exit.


.. _`pywbemcli class find --help`:

pywbemcli class find --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class find --help` subcommand


::

    Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME-GLOB

      Find all classes that match CLASSNAME-GLOB.

      Find all classes in the namespace(s) of the target WBEMServer that match
      the CLASSNAME-GLOB regular expression argument and return the classnames.
      The CLASSNAME-GLOB argument is required.

      The CLASSNAME-GLOB argument may be either a complete classname or a
      regular expression that can be matched to one or more classnames. To limit
      the filter to a single classname, terminate the classname with $.

      The GLOB expression is anchored to the beginning of the CLASSNAME-GLOB, is
      is case insensitive and uses the standard GLOB special characters (*(match
      everything), ?(match single character)). Thus, `pywbem_*` returns all
      classes that begin with `PyWBEM_`, `pywbem_`, etc. '.*system*' returns
      classnames that include the case insensitive string `system`.

      The namespace option limits the search to the defined namespaces.
      Otherwise all namespaces in the target server are searched.

      Output is in table format if table output specified. Otherwise it is in
      the form <namespace>:<classname>

    Options:
      -s, --sort              Sort into alphabetical order by classname.
      -n, --namespace <name>  Namespace(s) to use for this operation. If defined
                              only those namespaces are searched rather than all
                              available namespaces. ex: -n root/interop -n
                              root/cimv2
      -h, --help              Show this message and exit.


.. _`pywbemcli class get --help`:

pywbemcli class get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class get --help` subcommand


::

    Usage: pywbemcli class get [COMMAND-OPTIONS] CLASSNAME

      Get and display a single CIM class.

      Get a single CIM class defined by the CLASSNAME argument from the WBEM
      server and display it. Normally it is retrieved from the default namespace
      in the server.

      If the class is not found in the WBEM Server, the server returns an
      exception.

      The --includeclassorigin, --includeclassqualifiers, and --propertylist
      options determine what parts of the class definition are retrieved.

      Results are formatted as defined by the output format general option.

    Options:
      -l, --localonly                 Show only local properties of the class.
      --no-qualifiers                 If set, request server to not include
                                      qualifiers in the returned class(s). The
                                      default behavior is to request qualifiers in
                                      returned class(s).
      -c, --includeclassorigin        Request that server include classorigin in
                                      the result.On some WBEM operations, server
                                      may ignore this option.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      option not specified a Null property list is
                                      created and the server returns all
                                      properties. Multiple properties may be
                                      defined with either a comma separated list
                                      or by using the option multiple times. (ex:
                                      -p pn1 -p pn22 or -p pn1,pn2). If defined as
                                      empty string the server should return no
                                      properties.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -h, --help                      Show this message and exit.


.. _`pywbemcli class invokemethod --help`:

pywbemcli class invokemethod --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class invokemethod --help` subcommand


::

    Usage: pywbemcli class invokemethod [COMMAND-OPTIONS] CLASSNAME METHODNAME

      Invoke the class method named methodname.

      This invokes the method named METHODNAME on the class named CLASSNAME.

      This is the class level invokemethod and uses only the class name on the
      invoke.The subcommand `instance invokemethod` invokes methods based on
      class name.

      Examples:

        pywbemcli invokemethod CIM_Foo methodx -p param1=9 -p param2=Fred

    Options:
      -p, --parameter parameter  Optional multiple method parameters of form
                                 name=value
      -n, --namespace <name>     Namespace to use for this operation. If defined
                                 that namespace overrides the general options
                                 namespace
      -h, --help                 Show this message and exit.


.. _`pywbemcli class references --help`:

pywbemcli class references --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class references --help` subcommand


::

    Usage: pywbemcli class references [COMMAND-OPTIONS] CLASSNAME

      Get the reference classes for CLASSNAME.

      Get the reference classes (or class names) for the CLASSNAME argument
      filtered by the role and result class options and modified by the other
      options.

      Results are displayed as defined by the output format general option.

    Options:
      -R, --resultclass <class name>  Filter by the result classname provided.
                                      Each returned class (or classname) should be
                                      this class or its subclasses. Optional.
      -r, --role <role name>          Filter by the role name provided. Each
                                      returned class (or classname) should refer
                                      to the target class through a property with
                                      a name that matches the value of this
                                      parameter. Optional.
      --no-qualifiers                 If set, request server to not include
                                      qualifiers in the returned class(s). The
                                      default behavior is to request qualifiers in
                                      returned class(s).
      -c, --includeclassorigin        Request that server include classorigin in
                                      the result.On some WBEM operations, server
                                      may ignore this option.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      option not specified a Null property list is
                                      created and the server returns all
                                      properties. Multiple properties may be
                                      defined with either a comma separated list
                                      or by using the option multiple times. (ex:
                                      -p pn1 -p pn22 or -p pn1,pn2). If defined as
                                      empty string the server should return no
                                      properties.
      -o, --names-only                Retrieve only the returned object names.
      -s, --sort                      Sort into alphabetical order by classname.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli class tree --help`:

pywbemcli class tree --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class tree --help` subcommand


::

    Usage: pywbemcli class tree [COMMAND-OPTIONS] CLASSNAME

      Display CIM class inheritance hierarchy tree.

      Displays a tree of the class hiearchy to show superclasses and subclasses.

      CLASSNAMe is an optional argument that defines the starting point for the
      hiearchy display

      If the --superclasses option not specified the hiearchy starting either at
      the top most classes of the class hiearchy or at the class defined by
      CLASSNAME is displayed.

      if the --superclasses options is specified and a CLASSNAME is defined the
      class hiearchy of superclasses leading to CLASSNAME is displayed.

      This is a separate subcommand because it is tied specifically to
      displaying in a tree format.so that the --output-format general option is
      ignored.

    Options:
      -s, --superclasses      Display the superclasses to CLASSNAME as a tree.
                              When this option is set, the CLASSNAME argument is
                              required
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli connection --help`:

pywbemcli connection --help
---------------------------



The following defines the help output for the `pywbemcli connection --help` subcommand


::

    Usage: pywbemcli connection [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group to manage WBEM connections.

      These command allow viewing and setting persistent connection definitions.
      The connections are normally defined in the file pywbemcliconnections.json
      in the current directory.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      add     Create a new named WBEM connection.
      delete  Delete connection information.
      export  Export the current connection information.
      list    List the entries in the connection file.
      save    Save current connection to repository.
      select  Select a connection from defined connections.
      show    Show current or NAME connection information.
      test    Execute a predefined wbem request.


.. _`pywbemcli connection add --help`:

pywbemcli connection add --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection add --help` subcommand


::

    Usage: pywbemcli connection add [COMMAND-OPTIONS]

      Create a new named WBEM connection.

      This subcommand creates and saves a named connection from the input
      options in the connections file.

      The new connection can be referenced by the name argument in the future.
      This connection object is capable of managing all of the properties
      defined for WBEMConnections.

      The NAME and URI arguments MUST exist. They define the server uri and the
      unique name under which this server connection information will be stored.
      All other properties are optional.

      Adding a connection does not the new connection as the current connection.
      Use `connection select` to set a particular stored connection definition
      as the current connection.

      A new connection can also be defined by supplying the parameters on the
      command line and using the `connection save` command to put it into the
      connection repository.

    Options:
      -s, --server SERVER             Required hostname or IP address with scheme
                                      of the WBEMServer in format:
                                      [{scheme}://]{host}[:{port}]
                                      * Scheme: must
                                      be "https" or "http" [Default: "https"]
                                      *
                                      Host: defines short/fully qualified DNS
                                      hostname, literal IPV4 address (dotted), or
                                      literal IPV6 address
                                      * Port: (optional)
                                      defines WBEM server port to be used
                                      [Defaults: 5988(HTTP) and 5989(HTTPS)].
                                      [required]
      -n, --name NAME                 Required name for the connection(optional,
                                      see --server).  This is the name for this
                                      defined WBEM server in the connection file
                                      [required]
      -d, --default_namespace TEXT    Default Namespace to use in the target
                                      WBEMServer if no namespace is defined in the
                                      subcommand (Default: root/cimv2).
      -u, --user TEXT                 User name for the WBEM Server connection.
      -p, --password TEXT             Password for the WBEM Server. Will be
                                      requested as part  of initialization if user
                                      name exists and it is not  provided by this
                                      option.
      -t, --timeout INTEGER RANGE     Operation timeout for the WBEM Server in
                                      seconds. Default: 30
      -N, --noverify                  If set, client does not verify server
                                      certificate.
      -c, --certfile TEXT             Server certfile. Ignored if noverify flag
                                      set.
      -k, --keyfile TEXT              Client private key file.
      -l, --log COMP=DEST:DETAIL,...  Enable logging of CIM Operations and set a
                                      component to destination, and detail level
                                      (COMP: [api|http|all], Default: all) DEST:
                                      [file|stderr], Default: file)
                                      DETAIL:[all|paths|summary], Default: all)
      -m, --mock-server FILENAME      If this option is defined, a mock WBEM
                                      server is constructed as the target WBEM
                                      server and the option value defines a MOF or
                                      Python file to be used to populate the mock
                                      repository. This option may be used multiple
                                      times where each use defines a single file
                                      or file_path.See the pywbemcli documentation
                                      for more information.
      --ca_certs TEXT                 File or directory containing certificates
                                      that will be matched against a certificate
                                      received from the WBEM server. Set the --no-
                                      verify-cert option to bypass client
                                      verification of the WBEM server certificate.
                                      Default: Searches for matching certificates
                                      in the following system directories:
                                      /etc/pki/ca-trust/extracted/openssl/ca-
                                      bundle.trust.crt
                                      /etc/ssl/certs
                                      /etc/ssl/certificates
      -V, --verify                    If set, The change is displayed and
                                      verification requested before the change is
                                      executed
      -h, --help                      Show this message and exit.


.. _`pywbemcli connection delete --help`:

pywbemcli connection delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection delete --help` subcommand


::

    Usage: pywbemcli connection delete [COMMAND-OPTIONS] NAME

      Delete connection information.

      Delete connection information from the persistent store for the connection
      defined by NAME. The NAME argument is optional.

      If NAME not supplied, a select list presents the list of connection
      definitions for selection.

      Example:   connection delete blah

    Options:
      -V, --verify  If set, The change is displayed and verification requested
                    before the change is executed
      -h, --help    Show this message and exit.


.. _`pywbemcli connection export --help`:

pywbemcli connection export --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection export --help` subcommand


::

    Usage: pywbemcli connection export [COMMAND-OPTIONS]

      Export  the current connection information.

      Creates an export statement for each connection variable and outputs the
      statement to the conole.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection list --help`:

pywbemcli connection list --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection list --help` subcommand


::

    Usage: pywbemcli connection list [COMMAND-OPTIONS]

      List the entries in the connection file.

      This subcommand displays all entries in the connection file as a table
      using the command line output_format to define the table format with
      default of simple format.

      An "*" after the name indicates the currently selected connection.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection save --help`:

pywbemcli connection save --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection save --help` subcommand


::

    Usage: pywbemcli connection save [COMMAND-OPTIONS]

      Save current connection to repository.

      Saves the current connection to the connections file if it does not
      already exist in that file.

      This is useful when you have defined a connection on the command line and
      want to set it into the connections file.

    Options:
      -V, --verify  If set, The change is displayed and verification requested
                    before the change is executed
      -h, --help    Show this message and exit.


.. _`pywbemcli connection select --help`:

pywbemcli connection select --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection select --help` subcommand


::

    Usage: pywbemcli connection select [COMMAND-OPTIONS] NAME

      Select a connection from defined connections.

      Selects a connection from the persistently stored set of named connections
      if NAME exists in the store. The NAME argument is optional.  If NAME not
      supplied, a list of connections from the connections definition file is
      presented with a prompt for the user to select a NAME.

      Select state is not persistent.

      Examples:

         connection select <name>    # select the defined <name>

         connection select           # presents select list to pick connection

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection show --help`:

pywbemcli connection show --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection show --help` subcommand


::

    Usage: pywbemcli connection show [COMMAND-OPTIONS] NAME

      Show current or NAME connection information.

      This subcommand displays  all the variables that make up the current WBEM
      connection if the optional NAME argument is NOT provided. If NAME not
      supplied, a list of connections from the connections definition file is
      presented with a prompt for the user to select a NAME.

      The information on the     connection named is displayed if that name is
      in the persistent repository.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection test --help`:

pywbemcli connection test --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection test --help` subcommand


::

    Usage: pywbemcli connection test [COMMAND-OPTIONS]

      Execute a predefined wbem request.

      This executes a predefined request against the currente WBEM server to
      confirm that the connection exists and is working.

      It executes getclass on CIM_ManagedElement as the test.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli help --help`:

pywbemcli help --help
---------------------



The following defines the help output for the `pywbemcli help --help` subcommand


::

    Usage: pywbemcli help [OPTIONS]

      Show help message for interactive mode.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli instance --help`:

pywbemcli instance --help
-------------------------



The following defines the help output for the `pywbemcli instance --help` subcommand


::

    Usage: pywbemcli instance [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group to manage CIM instances.

      This incudes functions to get, enumerate, create, modify, and delete
      instances in a namspace and additional functions to get more general
      information on instances (ex. counts) within the namespace

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      associators   Get associated instances or names.
      count         Get instance count for classes.
      create        Create a CIM instance of CLASSNAME.
      delete        Delete a single CIM instance.
      enumerate     Enumerate instances or names of CLASSNAME.
      get           Get a single CIMInstance.
      invokemethod  Invoke a CIM method on a CIMInstance.
      modify        Modify an existing instance.
      query         Execute an execquery request.
      references    Get the reference instances or names.


.. _`pywbemcli instance associators --help`:

pywbemcli instance associators --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance associators --help` subcommand


::

    Usage: pywbemcli instance associators [COMMAND-OPTIONS] INSTANCENAME

      Get associated instances or names.

      Returns the associated instances or names (--names-only option) for the
      `INSTANCENAME` argument filtered by the --assocclass, --resultclass,
      --role and --resultrole options.

      INSTANCENAME must be a CIM instance name in the format defined by DMTF
      `DSP0207`.

      This may be executed interactively by providing only a classname and the
      interactive option. Pywbemcli presents a list of instances in the class
      from which one can be chosen as the target.

      Results are formatted as defined by the --output_format general option.

    Options:
      -a, --assocclass <class name>   Filter by the association class name
                                      provided.Each returned instance (or instance
                                      name) should be associated to the source
                                      instance through this class or its
                                      subclasses. Optional.
      -c, --resultclass <class name>  Filter by the result class name provided.
                                      Each returned instance (or instance name)
                                      should be a member of this class or one of
                                      its subclasses. Optional
      -r, --role <role name>          Filter by the role name provided. Each
                                      returned instance (or instance name)should
                                      be associated with the source instance
                                      (INSTANCENAME) through an association with
                                      this role (property name in the association
                                      that matches this parameter). Optional.
      -R, --resultrole <role name>    Filter by the result role name provided.
                                      Each returned instance (or instance
                                      name)should be associated with the source
                                      instance name (`INSTANCENAME`) through an
                                      association with returned object having this
                                      role (property name in the association that
                                      matches this parameter). Optional.
      -q, --includequalifiers         If set, requests server to include
                                      qualifiers in the returned instances. This
                                      subcommand may use either pull or
                                      traditional operations depending on the
                                      server and the "--use--pull-ops" general
                                      option. If pull operations are used,
                                      qualifiers will not be included, even if
                                      this option is specified. If traditional
                                      operations are used, inclusion of qualifiers
                                      depends on the server.
      -c, --includeclassorigin        Include class origin attribute in returned
                                      instance(s).
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      option not specified a Null property list is
                                      created and the server returns all
                                      properties. Multiple properties may be
                                      defined with either a comma separated list
                                      or by using the option multiple times. (ex:
                                      -p pn1 -p pn22 or -p pn1,pn2). If defined as
                                      empty string the server should return no
                                      properties.
      -o, --names-only                Retrieve only the returned object names.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -s, --sort                      Sort into alphabetical order by classname.
      -i, --interactive               If set, `INSTANCENAME` argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -S, --summary                   Return only summary of objects (count).
      -f, --filterquery TEXT          A filter query to be passed to the server if
                                      the pull operations are used. If this option
                                      is defined and the --filterquerylanguage is
                                      None, pywbemcli assumes DMTF:FQL. If this
                                      option is defined and the traditional
                                      operations are used, the filter is not sent
                                      to the server. See the documentation for
                                      more information. (Default: None)
      --filterquerylanguage TEXT      A filterquery language to be used with a
                                      filter query defined by --filterquery.
                                      (Default: None)
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance count --help`:

pywbemcli instance count --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance count --help` subcommand


::

    Usage: pywbemcli instance count [COMMAND-OPTIONS] CLASSNAME-GLOB

      Get instance count for classes.

      Displays the count of instances for the classes defined by the `CLASSNAME-
      GLOB` argument in one or more namespaces.

      The size of the response may be limited by CLASSNAME-GLOB argument which
      defines a regular expression based on the desired class names so that only
      classes that match the regex are counted. The CLASSNAME-GLOB argument is
      optional.

      The CLASSNAME-GLOB argument may be either a complete classname or a
      regular expression that can be matched to one or more classnames. To limit
      the filter to a single classname, terminate the classname with $.

      The GLOB expression is anchored to the beginning of the CLASSNAME-GLOB, is
      is case insensitive and uses the standard GLOB special characters (*(match
      everything), ?(match single character)). Thus, `pywbem_*` returns all
      classes that begin with `PyWBEM_`, `pywbem_`, etc. '.*system*' returns
      classnames that include the case insensitive string `system`.

      This operation can take a long time to execute since it enumerates all
      classes in the namespace.

    Options:
      -s, --sort              Sort by instance count. Otherwise sorted by
                              classname
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli instance create --help`:

pywbemcli instance create --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance create --help` subcommand


::

    Usage: pywbemcli instance create [COMMAND-OPTIONS] CLASSNAME

      Create a CIM instance of CLASSNAME.

      Creates an instance of the class CLASSNAME with the properties defined in
      the property option.

      Pywbemcli creates the new instance using CLASSNAME retrieved from the
      current WBEM server as a template for property characteristics. Therefore
      pywbemcli will generate an exception if CLASSNAME does not exist in the
      current WBEM Server or if the data definition in the properties options
      does not match the properties characteristics defined the returned class.

      ex. pywbemcli instance create CIM_blah -p id=3 -p strp="bla bla", -p p3=3

    Options:
      -P, --property name=value  Optional property definitions of the form
                                 name=value.Multiple definitions allowed, one for
                                 each property to be included in the
                                 createdinstance. Array property values defined by
                                 comma-separated-values. EmbeddedInstance not
                                 allowed.
      -V, --verify               If set, The change is displayed and verification
                                 requested before the change is executed
      -n, --namespace <name>     Namespace to use for this operation. If defined
                                 that namespace overrides the general options
                                 namespace
      -h, --help                 Show this message and exit.


.. _`pywbemcli instance delete --help`:

pywbemcli instance delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance delete --help` subcommand


::

    Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME

      Delete a single CIM instance.

      Delete the instanced defined by INSTANCENAME from the WBEM server.

      This may be executed interactively by providing only a class name and the
      interactive option.

      Otherwise the INSTANCENAME must be a CIM instance name in the format
      defined by DMTF `DSP0207`.

    Options:
      -i, --interactive       If set, `INSTANCENAME` argument must be a class
                              rather than an instance and user is presented with a
                              list of instances of the class from which the
                              instance to process is selected.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli instance enumerate --help`:

pywbemcli instance enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance enumerate --help` subcommand


::

    Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME

      Enumerate instances or names of CLASSNAME.

      Get CIMInstance or CIMInstanceName (--name_only option) objects from the
      WBEMServer starting either at the top  of the hierarchy (if no CLASSNAME
      provided) or from the CLASSNAME argument if provided.

      Displays the returned instances in mof, xml, or table formats or the
      instance names as a string or XML formats (--names-only option).

      Results are formatted as defined by the --output_format general option.

    Options:
      -l, --localonly                 Show only local properties of the instances.
                                      This subcommand may use either pull or
                                      traditional operations depending on the
                                      server and the "--use--pull-ops" general
                                      option. If pull operations are used, this
                                      parameters will not be included, even if
                                      specified. If traditional operations are
                                      used, some servers do not process the
                                      parameter.
      -d, --deepinheritance           If set, requests server to return properties
                                      in subclasses of the target instances class.
                                      If option not specified only properties from
                                      target class are returned
      -q, --includequalifiers         If set, requests server to include
                                      qualifiers in the returned instances. This
                                      subcommand may use either pull or
                                      traditional operations depending on the
                                      server and the "--use--pull-ops" general
                                      option. If pull operations are used,
                                      qualifiers will not be included, even if
                                      this option is specified. If traditional
                                      operations are used, inclusion of qualifiers
                                      depends on the server.
      -c, --includeclassorigin        Include class origin attribute in returned
                                      instance(s).
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      option not specified a Null property list is
                                      created and the server returns all
                                      properties. Multiple properties may be
                                      defined with either a comma separated list
                                      or by using the option multiple times. (ex:
                                      -p pn1 -p pn22 or -p pn1,pn2). If defined as
                                      empty string the server should return no
                                      properties.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -o, --names-only                Retrieve only the returned object names.
      -s, --sort                      Sort into alphabetical order by classname.
      -S, --summary                   Return only summary of objects (count).
      -f, --filterquery TEXT          A filter query to be passed to the server if
                                      the pull operations are used. If this option
                                      is defined and the --filterquerylanguage is
                                      None, pywbemcli assumes DMTF:FQL. If this
                                      option is defined and the traditional
                                      operations are used, the filter is not sent
                                      to the server. See the documentation for
                                      more information. (Default: None)
      --filterquerylanguage TEXT      A filterquery language to be used with a
                                      filter query defined by --filterquery.
                                      (Default: None)
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance get --help`:

pywbemcli instance get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance get --help` subcommand


::

    Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME

      Get a single CIMInstance.

      Gets the instance defined by `INSTANCENAME` where `INSTANCENAME` must
      resolve to the instance name of the desired instance. This may be supplied
      directly as an untyped wbem_uri formatted string or through the
      --interactive option. The wbemuri may contain the namespace or the
      namespace can be supplied with the --namespace option. If no namespace is
      supplied, the connection default namespace is used.  Any host name in the
      wbem_uri is ignored.

      This method may be executed interactively by providing only a classname
      and the interactive option (-i).

      Otherwise the INSTANCENAME must be a CIM instance name in the format
      defined by DMTF `DSP0207`.

      Results are formatted as defined by the --output_format general option.

    Options:
      -l, --localonly                 Request that server show only local
                                      properties of the returned instance. Some
                                      servers may not process this parameter.
      -q, --includequalifiers         If set, requests server to include
                                      qualifiers in the returned instances. Not
                                      all servers return qualifiers on instances
      -c, --includeclassorigin        Include class origin attribute in returned
                                      instance(s).
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      option not specified a Null property list is
                                      created and the server returns all
                                      properties. Multiple properties may be
                                      defined with either a comma separated list
                                      or by using the option multiple times. (ex:
                                      -p pn1 -p pn22 or -p pn1,pn2). If defined as
                                      empty string the server should return no
                                      properties.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -i, --interactive               If set, `INSTANCENAME` argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance invokemethod --help`:

pywbemcli instance invokemethod --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance invokemethod --help` subcommand


::

    Usage: pywbemcli instance invokemethod [COMMAND-OPTIONS] INSTANCENAME
                                           METHODNAME

      Invoke a CIM method on a CIMInstance.

      Invoke the method defined by INSTANCENAME and METHODNAME arguments with
      parameters defined by the --parameter options.

      This issues an instance level invokemethod request and displays the
      results.

      INSTANCENAME must be a CIM instance name in the format defined by  DMTF
      `DSP0207`.

      Pywbemcli creates the method call using the class in INSTANCENAME
      retrieved from the current WBEM server as a template for parameter
      characteristics. Therefore pywbemcli will generate an exception if
      CLASSNAME does not exist in the current WBEM Server or if the data
      definition in the parameter options does not match the parameter
      characteristics defined the returned class.

      A class level invoke method is available as `pywbemcli class
      invokemethod`.

      Example:

      pywbmcli instance invokemethod  CIM_x.InstanceID='hi" methodx -p id=3

    Options:
      -p, --parameter name=value  Multiple definitions allowed, one for each
                                  parameter to be included in the new instance.
                                  Array parameter values defined by comma-
                                  separated-values. EmbeddedInstance not allowed.
      -i, --interactive           If set, `INSTANCENAME` argument must be a class
                                  rather than an instance and user is presented
                                  with a list of instances of the class from which
                                  the instance to process is selected.
      -n, --namespace <name>      Namespace to use for this operation. If defined
                                  that namespace overrides the general options
                                  namespace
      -h, --help                  Show this message and exit.


.. _`pywbemcli instance modify --help`:

pywbemcli instance modify --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance modify --help` subcommand


::

    Usage: pywbemcli instance modify [COMMAND-OPTIONS] INSTANCENAME

      Modify an existing instance.

      Modifies CIM instance defined by INSTANCENAME in the WBEM server using the
      property names and values defined by the property option and the CIM class
      defined by the instance name.  The propertylist option if provided is
      passed to the WBEM server as part of the ModifyInstance operation
      (normally the WBEM server limits modifications) to just those properties
      defined in the property list.

      INSTANCENAME must be a CIM instance name in the format defined by DMTF
      `DSP0207`.

      Pywbemcli builds only the properties defined with the --property option
      into an instance based on the CIMClass and forwards that to the WBEM
      server with the ModifyInstance method.

      ex. pywbemcli instance modify CIM_blah.fred=3 -p id=3 -p strp="bla bla"

    Options:
      -P, --property name=value       Optional property definitions of the form
                                      name=value.Multiple definitions allowed, one
                                      for each property to be included in the
                                      createdinstance. Array property values
                                      defined by comma-separated-values.
                                      EmbeddedInstance not allowed.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      option not specified a Null property list is
                                      created. Multiple properties may be defined
                                      with either a comma separated list defining
                                      the option multiple times. (ex: -p pn1 -p
                                      pn22 or -p pn1,pn2). If defined as empty
                                      string an empty propertylist is created. The
                                      server uses the propertylist to limit
                                      changes made to the instance to properties
                                      in the propertylist.
      -i, --interactive               If set, `INSTANCENAME` argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -V, --verify                    If set, The change is displayed and
                                      verification requested before the change is
                                      executed
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance query --help`:

pywbemcli instance query --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance query --help` subcommand


::

    Usage: pywbemcli instance query [COMMAND-OPTIONS] QUERY_STRING

      Execute an execquery request.

      Executes a query request on the target WBEM Server with the QUERY_STRING
      argument and query language options.

      The results of the query are displayed as mof or xml.

      Results are formatted as defined by the --output_format general option.

    Options:
      -l, --querylanguage QUERY LANGUAGE
                                      Use the query language defined. (Default:
                                      DMTF:CQL.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -s, --sort                      Sort into alphabetical order by classname.
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance references --help`:

pywbemcli instance references --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance references --help` subcommand


::

    Usage: pywbemcli instance references [COMMAND-OPTIONS] INSTANCENAME

      Get the reference instances or names.

      Gets the reference instances or instance names(--names-only option) for a
      target `INSTANCENAME` in the target WBEM server filtered by the `role` and
      `resultclass` options.

      INSTANCENAME must be a CIM instance name in the format defined by DMTF
      `DSP0207`.

      This may be executed interactively by providing only a class name for
      `INSTANCENAME` and the `interactive` option(-i). Pywbemcli presents a list
      of instances names in the class from which you can be chosen as the
      target.

      Results are formatted as defined by the --output_format general option.

    Options:
      -R, --resultclass <class name>  Filter by the result class name provided.
                                      Each returned instance (or instance name)
                                      should be a member of this class or its
                                      subclasses. Optional
      -r, --role <role name>          Filter by the role name provided. Each
                                      returned instance (or instance name) should
                                      refer to the target instance through a
                                      property with aname that matches the value
                                      of this parameter. Optional.
      -q, --includequalifiers         If set, requests server to include
                                      qualifiers in the returned instances. This
                                      subcommand may use either pull or
                                      traditional operations depending on the
                                      server and the "--use--pull-ops" general
                                      option. If pull operations are used,
                                      qualifiers will not be included, even if
                                      this option is specified. If traditional
                                      operations are used, inclusion of qualifiers
                                      depends on the server.
      -c, --includeclassorigin        Include class origin attribute in returned
                                      instance(s).
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      option not specified a Null property list is
                                      created and the server returns all
                                      properties. Multiple properties may be
                                      defined with either a comma separated list
                                      or by using the option multiple times. (ex:
                                      -p pn1 -p pn22 or -p pn1,pn2). If defined as
                                      empty string the server should return no
                                      properties.
      -o, --names-only                Retrieve only the returned object names.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -s, --sort                      Sort into alphabetical order by classname.
      -i, --interactive               If set, `INSTANCENAME` argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -S, --summary                   Return only summary of objects (count).
      -f, --filterquery TEXT          A filter query to be passed to the server if
                                      the pull operations are used. If this option
                                      is defined and the --filterquerylanguage is
                                      None, pywbemcli assumes DMTF:FQL. If this
                                      option is defined and the traditional
                                      operations are used, the filter is not sent
                                      to the server. See the documentation for
                                      more information. (Default: None)
      --filterquerylanguage TEXT      A filterquery language to be used with a
                                      filter query defined by --filterquery.
                                      (Default: None)
      -h, --help                      Show this message and exit.


.. _`pywbemcli qualifier --help`:

pywbemcli qualifier --help
--------------------------



The following defines the help output for the `pywbemcli qualifier --help` subcommand


::

    Usage: pywbemcli qualifier [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group to view QualifierDeclarations.

      Includes the capability to get and enumerate CIM qualifier declarations
      defined in the WBEM Server.

      pywbemcli does not provide the capability to create or delete CIM
      QualifierDeclarations

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      enumerate  Enumerate CIMQualifierDeclaractions.
      get        Display CIMQualifierDeclaration.


.. _`pywbemcli qualifier enumerate --help`:

pywbemcli qualifier enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli qualifier enumerate --help` subcommand


::

    Usage: pywbemcli qualifier enumerate [COMMAND-OPTIONS]

      Enumerate CIMQualifierDeclaractions.

      Displays all of the CIMQualifierDeclaration objects in the defined
      namespace in the current WBEM Server

    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -S, --summary           Return only summary of objects (count).
      -h, --help              Show this message and exit.


.. _`pywbemcli qualifier get --help`:

pywbemcli qualifier get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli qualifier get --help` subcommand


::

    Usage: pywbemcli qualifier get [COMMAND-OPTIONS] QUALIFIERNAME

      Display CIMQualifierDeclaration.

      Displays CIMQualifierDeclaration QUALIFIERNAME for the defined namespace
      in the current WBEMServer

    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli repl --help`:

pywbemcli repl --help
---------------------



The following defines the help output for the `pywbemcli repl --help` subcommand


::

    Usage: pywbemcli repl [OPTIONS]

      Enter interactive (REPL) mode (default).

      Enters the interactive mode where subcommands can be entered interactively
      and load the command history file.

      If no options are specified on the command line,  the interactive mode is
      entered. The prompt is changed to `pywbemcli>' in the interactive mode.

      Pywbemcli may be terminated form this mode by entering <CTRL-D>, :q,
      :quit, :exit

      Parameters:

        ctx (:class:`click.Context`): The click context object. Created by the
        ``@click.pass_context`` decorator.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server --help`:

pywbemcli server --help
-----------------------



The following defines the help output for the `pywbemcli server --help` subcommand


::

    Usage: pywbemcli server [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command Group for WBEM server operations.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      brand         Display information on the server.
      centralinsts  Display Central Instances in the WBEM Server.
      connection    Display connection info used by this server.
      info          Display general information on the Server.
      interop       Display the interop namespace name.
      namespaces    Display the namespaces in the WBEM server
      profiles      Display registered profiles from the WBEM Server.
      test_pull     Test existence of pull opeations.


.. _`pywbemcli server brand --help`:

pywbemcli server brand --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server brand --help` subcommand


::

    Usage: pywbemcli server brand [COMMAND-OPTIONS]

      Display information on the server.

      Display brand information on the current server if it is available. This
      is typically the definition of the server implementor.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server centralinsts --help`:

pywbemcli server centralinsts --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server centralinsts --help` subcommand


::

    Usage: pywbemcli server centralinsts [COMMAND-OPTIONS]

      Display Central Instances in the WBEM Server.

      Displays central instances for management profiles registered in the
      server. Displays management profiles that adher to to the central class
      methodology with none of the extra parameters (ex. scoping_class)

      However, profiles that only use the scoping methodology require extra
      information that is dependent on the profile itself. These profiles will
      only be accessed when the correct values of central_class, scoping_class,
      and scoping path for the particular profile is provided.

      This display may be filtered by the optional organization and profile name
      options that define the organization for each profile (ex. SNIA) and the
      name of the profile. This will display only the profiles that are
      registered for the defined organization and/or name.

      Profiles are display as a table showing the organization, name, and
      version for each profile.

    Options:
      -o, --organization <org name>   Filter by the defined organization. (ex. -o
                                      DMTF
      -n, --profilename <profile name>
                                      Filter by the profile name. (ex. -n Array
      -c, --central_class <classname>
                                      Optional. Required only if profiles supports
                                      only scopig methodology
      -s, --scoping_class <classname>
                                      Optional. Required only if profiles supports
                                      only scopig methodology
      -p, --scoping_path <pathname>   Optional. Required only if profiles supports
                                      only scopig methodology. Multiples allowed
      -r, --reference_direction [snia|dmtf]
                                      Navigation direction for association.
                                      [default: dmtf]
      -h, --help                      Show this message and exit.


.. _`pywbemcli server connection --help`:

pywbemcli server connection --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server connection --help` subcommand


::

    Usage: pywbemcli server connection [COMMAND-OPTIONS]

      Display connection info used by this server.

      Displays the connection information for the WBEM connection attached to
      this server.  This includes uri, default namespace, etc.

      This is equivalent to the connection show subcommand.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server info --help`:

pywbemcli server info --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server info --help` subcommand


::

    Usage: pywbemcli server info [COMMAND-OPTIONS]

      Display general information on the Server.

      Displays general information on the current server includeing brand,
      namespaces, etc.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server interop --help`:

pywbemcli server interop --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server interop --help` subcommand


::

    Usage: pywbemcli server interop [COMMAND-OPTIONS]

      Display the interop namespace name.

      Displays the name of the interop namespace defined for the WBEM Server.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server namespaces --help`:

pywbemcli server namespaces --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server namespaces --help` subcommand


::

    Usage: pywbemcli server namespaces [COMMAND-OPTIONS]

      Display the namespaces in the WBEM server

    Options:
      -s, --sort  Sort into alphabetical order by classname.
      -h, --help  Show this message and exit.


.. _`pywbemcli server profiles --help`:

pywbemcli server profiles --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server profiles --help` subcommand


::

    Usage: pywbemcli server profiles [COMMAND-OPTIONS]

      Display registered profiles from the WBEM Server.

      Displays the management profiles that have been registered for this
      server.  Within the DMTF and SNIA these are the definition of management
      functionality supported by the server.

      This display may be filtered by the optional organization and profile name
      options that define the organization for each profile (ex. SNIA) and the
      name of the profile. This will display only the profiles that are
      registered for the defined organization and/or name.

      Profiles are display as a table showing the organization, name, and
      version for each profile.

    Options:
      -o, --organization <org name>   Filter by the defined organization. (ex. -o
                                      DMTF
      -n, --profilename <profile name>
                                      Filter by the profile name. (ex. -n Array
      -h, --help                      Show this message and exit.


.. _`pywbemcli server test_pull --help`:

pywbemcli server test_pull --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server test_pull --help` subcommand


::

    Usage: pywbemcli server test_pull [COMMAND-OPTIONS]

      Test existence of pull opeations.

      Test whether the pull WBEMConnection methods (ex. OpenEnumerateInstances)
      exist on the WBEM server.

      This command tests all of the pull operations and reports any that return
      a NOT_SUPPORTED response.

    Options:
      -h, --help  Show this message and exit.

