
.. _`pywbemcli Help Command Details`:

pywbemcli Help Command Details
==============================


This section defines the help output for each pywbemcli command-group and command.



The following defines the help output for the `pywbemcli  --help` command


::

    Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...

      Pywbemcli is a command line WBEM client that uses the DMTF CIM-XML
      protocol to communicate with WBEM servers. Pywbemcli can:

      * Manage the information in WBEM servers CIM objects using the
        operations defined in the DMTF specification.  It can manage CIM
        classes, CIM instances and CIM qualifier declarations in the WBEM
        Server and execute CIM methods and queries on the server.

      * Inspect WBEM server characteristics including namespaces, registered
        profiles, and other server information.

      * Capture detailed information on communication with the WBEM
        server including time statistics and logs of the operations.

      * Maintain a persistent list of named connections to WBEM servers
        and execute operations on them by name.

      Pywbemcli implements command groups and commands to execute the CIM-XML
      operations defined by the DMTF CIM Operations Over HTTP specification
      (DSP0200).

      The general options shown below can also be specified on any of the
      (sub)commands as well as the command line.

      For more detailed documentation, see:

          https://pywbemtools.readthedocs.io/en/stable/

    Options:
      -s, --server URI                Hostname or IP address with scheme of the
                                      WBEM server in format:
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
                                      This
                                      option, the --name, and --mock-server are
                                      mututally exclusive since each defines a
                                      WBEM server.
                                      (EnvVar: PYWBEMCLI_SERVER)
      -n, --name NAME                 Name for the connection.  If this option
                                      exists and the server option does not exist
                                      pywbemcli retrieves the connection
                                      information from the connections file
                                      (pywbemcliservers.json). This option,
                                      --server, and --mock-server are mutually
                                      exclusive since each defines a WBEM server.
                                      (EnvVar: PYWBEMCLI_NAME)
      -d, --default-namespace NAMESPACE
                                      Default namespace to use in the target WBEM
                                      server if no namespace is defined in a
                                      command.
                                      (EnvVar: PYWBEMCLI_NAME)
                                      [Default:
                                      root/cimv2]
      -u, --user USER                 User name for the WBEM server connection.
                                      (EnvVar: PYWBEMCLI_USER)
      -p, --password PASSWORD         Password for the WBEM server. Will be
                                      requested as part  of initialization if user
                                      name exists and it is not  provided by this
                                      option.
                                      (EnvVar: PYWBEMCLI_PASSWORD)
      -t, --timeout INTEGER           Client timeout completion of WBEM server
                                      operation in seconds.
                                      (EnvVar:
                                      PYWBEMCLI_TIMEOUT)
      -N, --no-verify                 If set, client does not verify WBEM server
                                      certificates.(EnvVar: PYWBEMCLI_NO_VERIFY).
      -c, --certfile TEXT             X.509 client certificate presented to the
                                      WBEM server during the TLS/SSL handshake for
                                      2 way authentication(EnvVar:
                                      PYWBEMCLI_CERTFILE).
      -k, --keyfile FILE PATH         X.509 client private key file containing
                                      private key belonging to tpublic key in
                                      X.509 certificate ``--certfile``. Not
                                      required if private key is part of
                                      --certfile file. 
                                      (EnvVar:
                                      PYWBEMCLI_KEYFILE)
      --ca-certs TEXT                 File or directory containing certificates
                                      that will be matched against certificate
                                      received from WBEM server. Set --no-verify
                                      option to bypass client verification of the
                                      WBEM server certificate.
                                      (EnvVar:
                                      PYWBEMCLI_CA_CERTS)
                                      [Default: Searches for
                                      matching certificates in the following
                                      system directories:
                                      /etc/pki/ca-
                                      trust/extracted/openssl/ca-bundle.trust.crt,
                                      /etc/ssl/certs,
                                      /etc/ssl/certificates]
      -o, --output-format <choice>    Choice for command output data format.
                                      pywbemcli may override the format choice
                                      depending on the command-group and command
                                      since not all formats apply to all output
                                      data types. Choices further defined in
                                      pywbemcli documentation.
                                      Choices: Table:
                                      [table|plain|simple|grid|psql|rst|html],
                                      Object: [mof|xml|repr|txt]
                                      [Default:
                                      "simple"]
      -U, --use-pull [yes|no|either]  Determines whether pull operations are used
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
                                      first pull and then traditional operations.
                                      (EnvVar: PYWBEMCLI_USE_PULL) [Default:
                                      either]
      --pull-max-cnt INTEGER          Maximium object count of objects to be
                                      returned for each request if pull operations
                                      are used. Must be  a positive non-zero
                                      integer.
                                      (EnvVar: PYWBEMCLI_PULL_MAX_CNT)
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
                                      single file_path.This option, --server, and
                                      --name are mutually exclusive since each
                                      defines a WBEM server. See the pywbemtools
                                      documentation for more information.
                                      (EnvVar:
                                      PYWBEMCLI_MOCK_SERVER)
      --version                       Show the version of this command and the
                                      pywbem package and exit.
      -h, --help                      Show this message and exit.

    Commands:
      class       Command-group for CIM classes.
      connection  Command group for persistent WBEM connections.
      help        Show help message for interactive mode.
      instance    Command group for CIM instances.
      qualifier   Command group for CIM qualifier declarations.
      repl        Enter interactive mode (default).
      server      Command group for WBEM servers.


.. _`pywbemcli class --help`:

pywbemcli class --help
----------------------



The following defines the help output for the `pywbemcli class --help` command


::

    Usage: pywbemcli class [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command-group for CIM classes.

      This command-group defines commands to inspect classes, to invoke methods
      on classes, and to delete classes.

      Creation and modification of classes is not currently supported.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      'class' keyword.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      associators   List the classes associated with a class.
      delete        Delete a class.
      enumerate     List the top classes or subclasses of a class in a...
      find          List the classes with matching class names on the server.
      get           Get a class.
      invokemethod  Invoke a method on a class.
      references    List the classes referencing a class.
      tree          Show the subclass or superclass inheritance tree of a class.


.. _`pywbemcli class associators --help`:

pywbemcli class associators --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class associators --help` command


::

    Usage: pywbemcli class associators [COMMAND-OPTIONS] CLASSNAME

      List the classes associated with a class.

      List the CIM classes that are associated with the specified class
      (CLASSNAME argument) or subclasses thereof in the specified CIM namespace
      (--namespace option). If no namespace was specified, the default namespace
      of the connection is used.

      The classes to be retrieved can be filtered by the --role, --result-role,
      --assoc-class, and --result-class options.

      The --include-classorigin, --no-qualifiers, and --propertylist options
      determine which parts are included in each retrieved class.

      The --names-only option can be used to show only the class paths.

      In the output, the classes and class paths will be formatted as defined by
      the --output-format general option. Table formats on classes will be
      replaced with MOF format.

      Examples:

        pywbemcli -n myconn class associators CIM_Foo -n interop

    Options:
      -a, --assoc-class <class name>  Filter by the association class name
                                      provided. Each returned class (or class
                                      name) should be associated to the source
                                      class through this class or its subclasses.
                                      Optional.
      -C, --result-class <class name>
                                      Filter the returned objects by the class
                                      name provided. Each returned class (or class
                                      name) should be this class or one of its
                                      subclasses. Optional
      -r, --role <role name>          Filter by the role name provided. Each
                                      returned class (or class name)should be
                                      associated with the source class (CLASSNAME)
                                      through an association with this role
                                      (property name in the association that
                                      matches this parameter). Optional.
      -R, --result-role <role name>   Filter by the result role name provided.
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
      -c, --include-classorigin       Request that server include classorigin in
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
      -n, --namespace <name>          Namespace to use for this operation, instead
                                      of the default namespace of the connection
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli class delete --help`:

pywbemcli class delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class delete --help` command


::

    Usage: pywbemcli class delete [COMMAND-OPTIONS] CLASSNAME

      Delete a class.

      Delete a CIM class (CLASSNAME argument) in a CIM namespace (--namespace
      option). If no namespace was specified, the default namespace of the
      connection is used.

      If the class has subclasses, the command is rejected.

      If the class has instances, the command is rejected, unless the --force
      option was specified, in which case the instances are also deleted.

      WARNING: Deleting classes can cause damage to the server: It can impact
      instance providers and other components in the server. Use this with
      command with caution.

      Some servers may refuse the operation altogether.

      Example:

        pywbemcli -n myconn class delete CIM_Foo -n interop

    Options:
      -f, --force             Force the delete request to be issued even if there
                              are instances in the server or subclasses to this
                              class. The WBEM server may still refuse the request.
      -n, --namespace <name>  Namespace to use for this operation, instead of the
                              default namespace of the connection
      -h, --help              Show this message and exit.


.. _`pywbemcli class enumerate --help`:

pywbemcli class enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class enumerate --help` command


::

    Usage: pywbemcli class enumerate [COMMAND-OPTIONS] CLASSNAME

      List the top classes or subclasses of a class in a namespace.

      Enumerate CIM classes starting either at the top of the class hierarchy in
      the specified CIM namespace (--namespace option), or at the specified
      class (CLASSNAME argument) in the specified namespace. If no namespace was
      specified, the default namespace of the connection is used.

      The --local-only, --include-classorigin, --no-qualifiers, and
      --propertylist options determine which parts are included in each
      retrieved class.

      The --deep-inheritance option defines whether or not the complete subclass
      hierarchy of the classes is retrieved.

      The --names-only option can be used to show only the class paths.

      In the output, the classes and class paths will be formatted as defined by
      the --output-format general option. Table formats on classes will be
      replaced with MOF format.

      Examples:

        pywbemcli -n myconn class enumerate -n interop   pywbemcli -n myconn
        class enumerate CIM_Foo -n interop

    Options:
      -d, --deep-inheritance     If set, request server to return complete
                                 subclass hiearchy for this class. The default is
                                 False which requests only one level of
                                 subclasses.
      -l, --local-only           Show only local properties of the class(s).
      --no-qualifiers            If set, request server to not include qualifiers
                                 in the returned class(s). The default behavior is
                                 to request qualifiers in returned class(s).
      -c, --include-classorigin  Request that server include classorigin in the
                                 result.On some WBEM operations, server may ignore
                                 this option.
      -o, --names-only           Retrieve only the returned object names.
      -n, --namespace <name>     Namespace to use for this operation, instead of
                                 the default namespace of the connection
      -S, --summary              Return only summary of objects (count).
      -h, --help                 Show this message and exit.


.. _`pywbemcli class find --help`:

pywbemcli class find --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class find --help` command


::

    Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME-GLOB

      List the classes with matching class names on the server.

      Find the CIM classes whose class name matches the specified wildcard
      expression (CLASSNAME-GLOB argument) in all CIM namespaces of the WBEM
      server, or in the specified namespace (--namespace option).

      The CLASSNAME-GLOB argument is a wildcard expression that is matched on
      the class names case insensitively. The special characters known from file
      nme wildcarding are supported: `*` to match zero or more characters, and
      `?` to match a single character. In order to not have the shell expand the
      wildcards, the CLASSNAME-GLOB argument should be put in quotes.

      For example, `pywbem_*` returns classes whose name begins with `PyWBEM_`,
      `pywbem_`, etc. '*system*' returns classes whose names include the case
      insensitive string `system`.

      In the output, the classes will formatted as defined by the --output-
      format general option if it specifies table output. Otherwise the classes
      will be in the form `<namespace>:<classname>`.

      Examples:

        pywbemcli -n myconn class find "CIM_*" -n interop   pywbemcli -n myconn
        class find CIM_Foo

    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined only
                              those namespaces are searched rather than all
                              available namespaces. ex: -n root/interop -n
                              root/cimv2
      -h, --help              Show this message and exit.


.. _`pywbemcli class get --help`:

pywbemcli class get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class get --help` command


::

    Usage: pywbemcli class get [COMMAND-OPTIONS] CLASSNAME

      Get a class.

      Get a CIM class (CLASSNAME argument) in a CIM namespace (--namespace
      option). If no namespace was specified, the default namespace of the
      connection is used.

      The --local-only, --include-classorigin, --no-qualifiers, and
      --propertylist options determine which parts are included in each
      retrieved class.

      In the output, the class will be formatted as defined by the --output-
      format general option. Table formats are replaced with MOF format.

      Example:

        pywbemcli -n myconn class get CIM_Foo -n interop

    Options:
      -l, --local-only                Show only local properties of the class(s).
      --no-qualifiers                 If set, request server to not include
                                      qualifiers in the returned class(s). The
                                      default behavior is to request qualifiers in
                                      returned class(s).
      -c, --include-classorigin       Request that server include classorigin in
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
      -n, --namespace <name>          Namespace to use for this operation, instead
                                      of the default namespace of the connection
      -h, --help                      Show this message and exit.


.. _`pywbemcli class invokemethod --help`:

pywbemcli class invokemethod --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class invokemethod --help` command


::

    Usage: pywbemcli class invokemethod [COMMAND-OPTIONS] CLASSNAME METHODNAME

      Invoke a method on a class.

      Invoke a static CIM method (METHODNAME argument) on a CIM class (CLASSNAME
      argument) in a CIM namespace (--namespace option), and display the method
      return value and output parameters. If no namespace was specified, the
      default namespace of the connection is used.

      The method input parameters are specified using the --parameter option,
      which can be specified multiple times.

      Pywbemcli retrieves the class definition from the server in order to
      verify that the specified input parameters are consistent with the
      parameter characteristics in the method definition.

      Use the 'instance invokemethod' command to invoke CIM methods on CIM
      instances.

      Example:

        pywbemcli -n myconn class invokemethod CIM_Foo methodx -p p1=9 -p
        p2=Fred

    Options:
      -p, --parameter parameter  Optional multiple method parameters of form
                                 name=value
      -n, --namespace <name>     Namespace to use for this operation, instead of
                                 the default namespace of the connection
      -h, --help                 Show this message and exit.


.. _`pywbemcli class references --help`:

pywbemcli class references --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class references --help` command


::

    Usage: pywbemcli class references [COMMAND-OPTIONS] CLASSNAME

      List the classes referencing a class.

      List the CIM (association) classes that reference the specified class
      (CLASSNAME argument) or subclasses thereof in the specified CIM namespace
      (--namespace option). If no namespace was specified, the default namespace
      of the connection is used.

      The classes to be retrieved can be filtered by the --role and --result-
      class options.

      The --include-classorigin, --no-qualifiers, and --propertylist options
      determine which parts are included in each retrieved class.

      The --names-only option can be used to show only the class paths.

      In the output, the classes and class paths will be formatted as defined by
      the --output-format general option. Table formats on classes will be
      replaced with MOF format.

      Examples:

        pywbemcli -n myconn class references CIM_Foo -n interop

    Options:
      -R, --result-class <class name>
                                      Filter by the classname provided. Each
                                      returned class (or classname) should be this
                                      class or its subclasses. Optional.
      -r, --role <role name>          Filter by the role name provided. Each
                                      returned class (or classname) should refer
                                      to the target class through a property with
                                      a name that matches the value of this
                                      parameter. Optional.
      --no-qualifiers                 If set, request server to not include
                                      qualifiers in the returned class(s). The
                                      default behavior is to request qualifiers in
                                      returned class(s).
      -c, --include-classorigin       Request that server include classorigin in
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
      -n, --namespace <name>          Namespace to use for this operation, instead
                                      of the default namespace of the connection
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli class tree --help`:

pywbemcli class tree --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class tree --help` command


::

    Usage: pywbemcli class tree [COMMAND-OPTIONS] CLASSNAME

      Show the subclass or superclass inheritance tree of a class.

      List the subclass or superclass hierarchy of a CIM class (CLASSNAME
      argument) or CIM namespace (--namespace option):

      - If CLASSNAME is omitted, the complete class hierarchy of the specified
      namespace is retrieved.

      - If CLASSNAME is specified but not --superclasses, the class and its
      subclass hierarchy in the specified namespace are retrieved.

      - If CLASSNAME and --superclasses are specified, the class and its
      superclass ancestry up to the top-level class in the specified namespace
      are retrieved.

      If no namespace was specified, the default namespace of the connection is
      used.

      In the output, the classes will formatted as a ASCII graphical tree; the
      --output-format general option is ignored.

      Examples:

        pywbemcli -n myconn class tree -n interop   pywbemcli -n myconn class
        tree CIM_Foo -n interop   pywbemcli -n myconn class tree CIM_Foo
        --superclasses -n interop

    Options:
      -s, --superclasses      Display the superclasses to CLASSNAME as a tree.
                              When this option is set, the CLASSNAME argument is
                              required
      -n, --namespace <name>  Namespace to use for this operation, instead of the
                              default namespace of the connection
      -h, --help              Show this message and exit.


.. _`pywbemcli connection --help`:

pywbemcli connection --help
---------------------------



The following defines the help output for the `pywbemcli connection --help` command


::

    Usage: pywbemcli connection [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group for persistent WBEM connections.

      This command group defines commands to manage persistent WBEM connections
      that have a name. The connections are stored in a connections file named
      'pywbemcliservers.json' in the current directory. The connection name can
      be used as a shorthand for the WBEM server via the '--name' general
      option.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      'connection' keyword.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      add     Add a persistent WBEM connection from specified conn info.
      delete  Delete a persistent WBEM connection.
      export  Display the commands for exporting the current connection.
      list    List the persistent WBEM connections.
      save    Save current connection as a persistent WBEM connection.
      select  Interactively select a persistent WBEM connection for use.
      show    Show connection info of current or persistent WBEM connection.
      test    Test current connection with a predefined WBEM request.


.. _`pywbemcli connection add --help`:

pywbemcli connection add --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection add --help` command


::

    Usage: pywbemcli connection add [COMMAND-OPTIONS]

      Add a persistent WBEM connection from specified conn info.

      This command creates and saves a named connection from the input options
      in the connections file.

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
                                      of the WBEM server in format:
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
      -n, --name NAME                 Required name for the connection(optional,
                                      see --server).  This is the name for this
                                      defined WBEM server in the connections file
                                      [required]
      -d, --default-namespace NAMESPACE
                                      Default namespace to use in the target WBEM
                                      server if no namespace is defined in the
                                      command (Default: root/cimv2).
      -u, --user TEXT                 User name for the WBEM server connection.
      -p, --password TEXT             Password for the WBEM server. Will be
                                      requested as part  of initialization if user
                                      name exists and it is not  provided by this
                                      option.
      -t, --timeout INTEGER RANGE     Operation timeout for the WBEM server in
                                      seconds. Default: 30
      -N, --no-verify                 If set, client does not verify server
                                      certificate.
      -c, --certfile TEXT             Server certfile. Ignored if no-verify flag
                                      set.
      -k, --keyfile TEXT              Client private key file.
      -U, --use-pull [yes|no|either]  Determines whether pull operations are used
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
      --pull-max-cnt INTEGER          Maximium object count of objects to be
                                      returned for each request if pull operations
                                      are used. Must be  a positive non-zero
                                      integer.[Default: 1000]
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



The following defines the help output for the `pywbemcli connection delete --help` command


::

    Usage: pywbemcli connection delete [COMMAND-OPTIONS] NAME

      Delete a persistent WBEM connection.

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



The following defines the help output for the `pywbemcli connection export --help` command


::

    Usage: pywbemcli connection export [COMMAND-OPTIONS]

      Display the commands for exporting the current connection.

      Creates an export statement for each connection variable and outputs the
      statements to the console.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection list --help`:

pywbemcli connection list --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection list --help` command


::

    Usage: pywbemcli connection list [COMMAND-OPTIONS]

      List the persistent WBEM connections.

      This command displays all entries in the connections file as a table using
      the command line output_format to define the table format.

      An "*" after the name indicates the currently selected connection.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection save --help`:

pywbemcli connection save --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection save --help` command


::

    Usage: pywbemcli connection save [COMMAND-OPTIONS]

      Save current connection as a persistent WBEM connection.

      Saves the current connection to the connections file if it does not
      already exist in that file.

      This is useful when you have defined a connection on the command line and
      want to set it into the connections file.

    Options:
      -n, --name Connection name  If defined, this changes the name of the
                                  connection to be saved. This allows renaming the
                                  current connection as part of saving it.
      -V, --verify                If set, The change is displayed and verification
                                  requested before the change is executed
      -h, --help                  Show this message and exit.


.. _`pywbemcli connection select --help`:

pywbemcli connection select --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection select --help` command


::

    Usage: pywbemcli connection select [COMMAND-OPTIONS] NAME

      Interactively select a persistent WBEM connection for use.

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



The following defines the help output for the `pywbemcli connection show --help` command


::

    Usage: pywbemcli connection show [COMMAND-OPTIONS] NAME

      Show connection info of current or persistent WBEM connection.

      This command displays all the variables that make up the current WBEM
      connection if the optional NAME argument is NOT provided. If NAME not
      supplied, a list of connections from the connections definition file is
      presented with a prompt for the user to select a NAME.

      The information on the connection named is displayed if that name is in
      the persistent repository.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection test --help`:

pywbemcli connection test --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection test --help` command


::

    Usage: pywbemcli connection test [COMMAND-OPTIONS]

      Test current connection with a predefined WBEM request.

      This executes a predefined request against the current WBEM server to
      confirm that the connection exists and is working.

      It executes EnumerateClassNames on the default namespace as the test.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli help --help`:

pywbemcli help --help
---------------------



The following defines the help output for the `pywbemcli help --help` command


::

    Usage: pywbemcli help [OPTIONS]

      Show help message for interactive mode.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli instance --help`:

pywbemcli instance --help
-------------------------



The following defines the help output for the `pywbemcli instance --help` command


::

    Usage: pywbemcli instance [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group for CIM instances.

      This command-group  defines commands to inspect instances, to invoke
      methods on instances, and to create and delete instances.

      Modification of instances is not currently supported.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      'instance' keyword.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      associators   List the instances associated with an instance.
      count         Count the instances of each class with matching class name.
      create        Create an instance of a class in a namespace.
      delete        Delete an instance of a class.
      enumerate     List the instances of a class.
      get           Get an instance of a class.
      invokemethod  Invoke a method on an instance.
      modify        Modify an instance of a class.
      query         Execute a query on instances in a namespace.
      references    List the instances referencing an instance.


.. _`pywbemcli instance associators --help`:

pywbemcli instance associators --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance associators --help` command


::

    Usage: pywbemcli instance associators [COMMAND-OPTIONS] INSTANCENAME

      List the instances associated with an instance.

      List the CIM instances that are associated with the specified CIM
      instance, and display the returned instances, or instance paths if
      --names-only was specified.

      The CIM instance can be specified in two ways:

      1. By specifying an untyped WBEM URI of an instance path in the
      INSTANCENAME argument. The CIM namespace in which the instance is looked
      up is the namespace specified in the WBEM URI, or otherwise the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection. Any host name in the WBEM URI will be ignored.

      2. By specifying the --interactive option and a CIM class name in the
      INSTANCENAME argument. The instances of the specified class are displayed
      and the user is prompted for an index number to select an instance. The
      CIM namespace in which the instances are looked up is the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection.

      The instances to be retrieved can be filtered by the --filter-query,
      --role, --result-role, --assoc-class, and --result-class options.

      The --include-qualifiers, --include-classorigin, and --propertylist
      options determine which parts are included in each retrieved instance.

      The --names-only option can be used to show only the instance paths.

      In the output, the instances and instance paths will be formatted as
      defined by the --output-format general option. Table formats on instances
      will be replaced with MOF format.

    Options:
      -a, --assoc-class <class name>  Filter by the association class name
                                      provided.Each returned instance (or instance
                                      name) should be associated to the source
                                      instance through this class or its
                                      subclasses. Optional.
      -c, --result-class <class name>
                                      Filter by the result class name provided.
                                      Each returned instance (or instance name)
                                      should be a member of this class or one of
                                      its subclasses. Optional
      -r, --role <role name>          Filter by the role name provided. Each
                                      returned instance (or instance name)should
                                      be associated with the source instance
                                      (INSTANCENAME) through an association with
                                      this role (property name in the association
                                      that matches this parameter). Optional.
      -R, --result-role <role name>   Filter by the result role name provided.
                                      Each returned instance (or instance
                                      name)should be associated with the source
                                      instance name (`INSTANCENAME`) through an
                                      association with returned object having this
                                      role (property name in the association that
                                      matches this parameter). Optional.
      -q, --include-qualifiers        If set, requests server to include
                                      qualifiers in the returned instances. This
                                      command may use either pull or traditional
                                      operations depending on the server and the "
                                      --use-pull" general option. If pull
                                      operations are used, qualifiers will not be
                                      included, even if this option is specified.
                                      If traditional operations are used,
                                      inclusion of qualifiers depends on the
                                      server.
      -c, --include-classorigin       Request that server include classorigin in
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
      -n, --namespace <name>          Namespace to use for this operation, instead
                                      of the default namespace of the connection
      -i, --interactive               If set, `INSTANCENAME` argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -S, --summary                   Return only summary of objects (count).
      -f, --filter-query TEXT         A filter query to be passed to the server if
                                      the pull operations are used. If this option
                                      is defined and the --filter-query-language
                                      is None, pywbemcli assumes DMTF:FQL. If this
                                      option is defined and the traditional
                                      operations are used, the filter is not sent
                                      to the server. See the documentation for
                                      more information. (Default: None)
      --filter-query-language TEXT    A filter-query language to be used with a
                                      filter query defined by --filter-query.
                                      (Default: None)
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance count --help`:

pywbemcli instance count --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance count --help` command


::

    Usage: pywbemcli instance count [COMMAND-OPTIONS] CLASSNAME-GLOB

      Count the instances of each class with matching class name.

      Display the count of the instances of each CIM class whose class name
      matches the specified wildcard expression (CLASSNAME-GLOB) in all CIM
      namespaces of the WBEM server, or in the specified namespace (--namespace
      option).

      The CLASSNAME-GLOB argument is a wildcard expression that is matched on
      the class names case insensitively. The special characters known from file
      nme wildcarding are supported: `*` to match zero or more characters, and
      `?` to match a single character. In order to not have the shell expand the
      wildcards, the CLASSNAME-GLOB argument should be put in quotes.

      For example, `pywbem_*` returns classes whose name begins with `PyWBEM_`,
      `pywbem_`, etc. '*system*' returns classes whose names include the case
      insensitive string `system`.

      This operation can take a long time to execute since it potentially
      enumerates all classes in all namespaces.

    Options:
      -s, --sort              Sort by instance count. Otherwise sorted by
                              classname
      -n, --namespace <name>  Namespace to use for this operation, instead of the
                              default namespace of the connection
      -h, --help              Show this message and exit.


.. _`pywbemcli instance create --help`:

pywbemcli instance create --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance create --help` command


::

    Usage: pywbemcli instance create [COMMAND-OPTIONS] CLASSNAME

      Create an instance of a class in a namespace.

      Create a CIM instance of the specified creation class (CLASSNAME argument)
      in the specified CIM namespace (--namespace option), with the specified
      properties (--property options) and display the CIM instance path of the
      created instance. If no namespace was specified, the default namespace of
      the connection is used.

      The properties to be initialized and their new values are specified using
      the --property option, which can be specified multiple times.

      Pywbemcli retrieves the class definition from the server in order to
      verify that the specified properties are consistent with the property
      characteristics in the class definition.

      Example:

        pywbemcli instance create CIM_blah -p id=3 -p strp="bla bla"

    Options:
      -P, --property name=value  Optional property names of the form name=value.
                                 Multiple definitions allowed, one for each
                                 property to be included in the createdinstance.
                                 Array property values defined by comma-separated-
                                 values. EmbeddedInstance not allowed.
      -V, --verify               If set, The change is displayed and verification
                                 requested before the change is executed
      -n, --namespace <name>     Namespace to use for this operation, instead of
                                 the default namespace of the connection
      -h, --help                 Show this message and exit.


.. _`pywbemcli instance delete --help`:

pywbemcli instance delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance delete --help` command


::

    Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME

      Delete an instance of a class.

      The CIM instance to be deleted can be specified as follows:

      1. By specifying an untyped WBEM URI of an instance path in the
      INSTANCENAME argument. The CIM namespace in which the instance is looked
      up is the namespace specified in the WBEM URI, or otherwise the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection. Any host name in the WBEM URI will be ignored.

      2. By specifying the --interactive option and a CIM class name in the
      INSTANCENAME argument. The instances of the specified class are displayed
      and the user is prompted for an index number to select an instance. The
      CIM namespace in which the instances are looked up is the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection.

    Options:
      -i, --interactive       If set, `INSTANCENAME` argument must be a class
                              rather than an instance and user is presented with a
                              list of instances of the class from which the
                              instance to process is selected.
      -n, --namespace <name>  Namespace to use for this operation, instead of the
                              default namespace of the connection
      -h, --help              Show this message and exit.


.. _`pywbemcli instance enumerate --help`:

pywbemcli instance enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance enumerate --help` command


::

    Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME

      List the instances of a class.

      Enumerate the CIM instances of the specified class (CLASSNAME argument),
      including instances of subclasses in the specified CIM namespace
      (--namespace option), and display the returned instances, or instance
      paths if --names-only was specified. If no namespace was specified, the
      default namespace of the connection is used.

      The instances to be retrieved can be filtered by the --filter-query
      option.

      The --local-only, --deep-inheritance, --include-qualifiers, --include-
      classorigin, and --propertylist options determine which parts are included
      in each retrieved instance.

      The --names-only option can be used to show only the instance paths.

      In the output, the instances and instance paths will be formatted as
      defined by the --output-format general option. Table formats on instances
      will be replaced with MOF format.

    Options:
      -l, --local-only                Show only local properties of the instances.
                                      This command may use either pull or
                                      traditional operations depending on the
                                      server and the --use-pull general option. If
                                      pull operations are used, this parameters
                                      will not be included, even if specified. If
                                      traditional operations are used, some
                                      servers do not process the parameter.
      -d, --deep-inheritance          If set, requests server to return properties
                                      in subclasses of the target instances class.
                                      If option not specified only properties from
                                      target class are returned
      -q, --include-qualifiers        If set, requests server to include
                                      qualifiers in the returned instances. This
                                      command may use either pull or traditional
                                      operations depending on the server and the "
                                      --use-pull" general option. If pull
                                      operations are used, qualifiers will not be
                                      included, even if this option is specified.
                                      If traditional operations are used,
                                      inclusion of qualifiers depends on the
                                      server.
      -c, --include-classorigin       Request that server include classorigin in
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
      -n, --namespace <name>          Namespace to use for this operation, instead
                                      of the default namespace of the connection
      -o, --names-only                Retrieve only the returned object names.
      -S, --summary                   Return only summary of objects (count).
      -f, --filter-query TEXT         A filter query to be passed to the server if
                                      the pull operations are used. If this option
                                      is defined and the --filter-query-language
                                      is None, pywbemcli assumes DMTF:FQL. If this
                                      option is defined and the traditional
                                      operations are used, the filter is not sent
                                      to the server. See the documentation for
                                      more information. (Default: None)
      --filter-query-language TEXT    A filter-query language to be used with a
                                      filter query defined by --filter-query.
                                      (Default: None)
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance get --help`:

pywbemcli instance get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance get --help` command


::

    Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME

      Get an instance of a class.

      The instance can be specified in two ways:

      * By specifying an untyped WBEM URI of an instance path in the
      INSTANCENAME   argument. The namespace in which the instance is looked up
      is the   namespace specified in the WBEM URI, or otherwise the namespace
      specified   in the --namespace option, or otherwise the default namespace
      of the   connection. Any host name in the WBEM URI will be ignored.

      * By specifying the --interactive option and a class name in the
      INSTANCENAME argument. The instances of the specified class are displayed
      and the user is prompted for an index number to select an instance.   The
      namespace in which the instances are looked up is the namespace
      specified in the --namespace option, or otherwise the default namespace
      of the connection.

      In the output, the instance will formatted as defined by the --output-
      format general option.

    Options:
      -l, --local-only                Show only local properties of the instance.
                                      Some servers may not process this parameter.
      -q, --include-qualifiers        If set, requests server to include
                                      qualifiers in the returned instances. Not
                                      all servers return qualifiers on instances
      -c, --include-classorigin       Request that server include classorigin in
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
      -n, --namespace <name>          Namespace to use for this operation, instead
                                      of the default namespace of the connection
      -i, --interactive               If set, `INSTANCENAME` argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance invokemethod --help`:

pywbemcli instance invokemethod --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance invokemethod --help` command


::

    Usage: pywbemcli instance invokemethod [COMMAND-OPTIONS] INSTANCENAME
                                           METHODNAME

      Invoke a method on an instance.

      Invoke a CIM method (METHODNAME argument) on a CIM instance with the
      specified input parameters (--parameter options), and display the method
      return value and output parameters.

      The CIM instance can be specified in two ways:

      1. By specifying an untyped WBEM URI of an instance path in the
      INSTANCENAME argument. The CIM namespace in which the instance is looked
      up is the namespace specified in the WBEM URI, or otherwise the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection. Any host name in the WBEM URI will be ignored.

      2. By specifying the --interactive option and a CIM class name in the
      INSTANCENAME argument. The instances of the specified class are displayed
      and the user is prompted for an index number to select an instance. The
      CIM namespace in which the instances are looked up is the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection.

      The method input parameters are specified using the --parameter option,
      which can be specified multiple times.

      Pywbemcli retrieves the class definition of the creation class of the
      instance from the server in order to verify that the specified input
      parameters are consistent with the parameter characteristics in the method
      definition.

      Use the 'class invokemethod' command to invoke CIM methods on CIM classes.

      Example:

        pywbemcli -n myconn instance invokemethod CIM_x.id='hi" methodx -p id=3

    Options:
      -p, --parameter name=value  Multiple definitions allowed, one for each
                                  parameter to be included in the new instance.
                                  Array parameter values defined by comma-
                                  separated-values. EmbeddedInstance not allowed.
      -i, --interactive           If set, `INSTANCENAME` argument must be a class
                                  rather than an instance and user is presented
                                  with a list of instances of the class from which
                                  the instance to process is selected.
      -n, --namespace <name>      Namespace to use for this operation, instead of
                                  the default namespace of the connection
      -h, --help                  Show this message and exit.


.. _`pywbemcli instance modify --help`:

pywbemcli instance modify --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance modify --help` command


::

    Usage: pywbemcli instance modify [COMMAND-OPTIONS] INSTANCENAME

      Modify an instance of a class.

      The CIM instance to be modified can be specified in two ways:

      1. By specifying an untyped WBEM URI of an instance path in the
      INSTANCENAME argument. The CIM namespace in which the instance is looked
      up is the namespace specified in the WBEM URI, or otherwise the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection. Any host name in the WBEM URI will be ignored.

      2. By specifying the --interactive option and a CIM class name in the
      INSTANCENAME argument. The instances of the specified class are displayed
      and the user is prompted for an index number to select an instance. The
      CIM namespace in which the instances are looked up is the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection.

      The properties to be modified and their new values are specified using the
      --property option, which can be specified multiple times.

      Example:

        pywbemcli instance modify CIM_blah.fred=3 -p id=3 -p strp="bla bla"

    Options:
      -P, --property name=value       Optional property names of the form
                                      name=value. Multiple definitions allowed,
                                      one for each property to be included in the
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
      -n, --namespace <name>          Namespace to use for this operation, instead
                                      of the default namespace of the connection
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance query --help`:

pywbemcli instance query --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance query --help` command


::

    Usage: pywbemcli instance query [COMMAND-OPTIONS] QUERY_STRING

      Execute a query on instances in a namespace.

      Execute the specified query (QUERY_STRING argument) in the specified CIM
      namespace (--namespace option), and display the returned instances. If no
      namespace was specified, the default namespace of the connection is used.

      In the output, the instances will formatted as defined by the --output-
      format general option.

    Options:
      -l, --query-language QUERY LANGUAGE
                                      Use the query language defined. (Default:
                                      DMTF:CQL.
      -n, --namespace <name>          Namespace to use for this operation, instead
                                      of the default namespace of the connection
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance references --help`:

pywbemcli instance references --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance references --help` command


::

    Usage: pywbemcli instance references [COMMAND-OPTIONS] INSTANCENAME

      List the instances referencing an instance.

      List the CIM (association) instances that reference the specified CIM
      instance, and display the returned instances, or instance paths if
      --names-only was specified.

      The CIM instance can be specified in two ways:

      1. By specifying an untyped WBEM URI of an instance path in the
      INSTANCENAME argument. The CIM namespace in which the instance is looked
      up is the namespace specified in the WBEM URI, or otherwise the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection. Any host name in the WBEM URI will be ignored.

      2. By specifying the --interactive option and a CIM class name in the
      INSTANCENAME argument. The instances of the specified class are displayed
      and the user is prompted for an index number to select an instance. The
      CIM namespace in which the instances are looked up is the namespace
      specified in the --namespace option, or otherwise the default namespace of
      the connection.

      The instances to be retrieved can be filtered by the --filter-query,
      --role and --result-class options.

      The --include-qualifiers, --include-classorigin, and --propertylist
      options determine which parts are included in each retrieved instance.

      The --names-only option can be used to show only the instance paths.

      In the output, the instances and instance paths will be formatted as
      defined by the --output-format general option. Table formats on instances
      will be replaced with MOF format.

    Options:
      -R, --resultclass <class name>  Filter by the result class name provided.
                                      Each returned instance (or instance name)
                                      should be a member of this class or its
                                      subclasses. Optional
      -r, --role <role name>          Filter by the role name provided. Each
                                      returned instance (or instance name) should
                                      refer to the target instance through a
                                      property with a name that matches the value
                                      of this parameter. Optional.
      -q, --include-qualifiers        If set, requests server to include
                                      qualifiers in the returned instances. This
                                      command may use either pull or traditional
                                      operations depending on the server and the "
                                      --use-pull" general option. If pull
                                      operations are used, qualifiers will not be
                                      included, even if this option is specified.
                                      If traditional operations are used,
                                      inclusion of qualifiers depends on the
                                      server.
      -c, --include-classorigin       Request that server include classorigin in
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
      -n, --namespace <name>          Namespace to use for this operation, instead
                                      of the default namespace of the connection
      -i, --interactive               If set, `INSTANCENAME` argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -S, --summary                   Return only summary of objects (count).
      -f, --filter-query TEXT         A filter query to be passed to the server if
                                      the pull operations are used. If this option
                                      is defined and the --filter-query-language
                                      is None, pywbemcli assumes DMTF:FQL. If this
                                      option is defined and the traditional
                                      operations are used, the filter is not sent
                                      to the server. See the documentation for
                                      more information. (Default: None)
      --filter-query-language TEXT    A filter-query language to be used with a
                                      filter query defined by --filter-query.
                                      (Default: None)
      -h, --help                      Show this message and exit.


.. _`pywbemcli qualifier --help`:

pywbemcli qualifier --help
--------------------------



The following defines the help output for the `pywbemcli qualifier --help` command


::

    Usage: pywbemcli qualifier [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group for CIM qualifier declarations.

      This command-group  defines commands to inspect qualifier declarations.

      Creation, modification and deletion of qualifier declarations is not
      currently supported.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      'qualifier' keyword.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      enumerate  List the qualifier declarations in a namespace.
      get        Get a qualifier declaration.


.. _`pywbemcli qualifier enumerate --help`:

pywbemcli qualifier enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli qualifier enumerate --help` command


::

    Usage: pywbemcli qualifier enumerate [COMMAND-OPTIONS]

      List the qualifier declarations in a namespace.

      Enumerate the CIM qualifier declarations in the specified CIM namespace
      (--namespace option). If no namespace was specified, the default namespace
      of the connection is used.

      In the output, the qualifier declaration will formatted as defined by the
      --output-format general option.

    Options:
      -n, --namespace <name>  Namespace to use for this operation, instead of the
                              default namespace of the connection
      -S, --summary           Return only summary of objects (count).
      -h, --help              Show this message and exit.


.. _`pywbemcli qualifier get --help`:

pywbemcli qualifier get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli qualifier get --help` command


::

    Usage: pywbemcli qualifier get [COMMAND-OPTIONS] QUALIFIERNAME

      Get a qualifier declaration.

      Get a CIM qualifier declaration (QUALIFIERNAME argument) in a CIM
      namespace (--namespace option). If no namespace was specified, the default
      namespace of the connection is used.

      In the output, the qualifier declaration will formatted as defined by the
      --output-format general option.

    Options:
      -n, --namespace <name>  Namespace to use for this operation, instead of the
                              default namespace of the connection
      -h, --help              Show this message and exit.


.. _`pywbemcli repl --help`:

pywbemcli repl --help
---------------------



The following defines the help output for the `pywbemcli repl --help` command


::

    Usage: pywbemcli repl [OPTIONS]

      Enter interactive mode (default).

      Enters the interactive mode where commands can be entered interactively
      and load the command history file.

      If no options are specified on the command line, the interactive mode is
      entered. The prompt is changed to 'pywbemcli>' in the interactive mode.

      Pywbemcli may be terminated from this mode by entering <CTRL-D>, :q,
      :quit, :exit

      Parameters:

        ctx (:class:`click.Context`): The click context object. Created by the
        ``@click.pass_context`` decorator.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server --help`:

pywbemcli server --help
-----------------------



The following defines the help output for the `pywbemcli server --help` command


::

    Usage: pywbemcli server [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group for WBEM servers.

      This command group defines commands to inspect and manage core components
      of a WBEM server including server attributes, namespaces, the Interop
      namespace, management profiles, and access to profile central instances.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      'server' keyword.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      brand             Get the brand of the server.
      connection        Get connection info used by this server.
      get-centralinsts  List central instances of mgmt profiles on the server.
      info              Get information about the server.
      interop           Get the Interop namespace of the server.
      namespaces        List the namespaces of the server.
      profiles          List management profiles advertized by the server.


.. _`pywbemcli server brand --help`:

pywbemcli server brand --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server brand --help` command


::

    Usage: pywbemcli server brand [COMMAND-OPTIONS]

      Get the brand of the server.

      Brand information is defined by the server implementor and may or may not
      be available. Pywbem attempts to collect the brand information from
      multiple sources.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server connection --help`:

pywbemcli server connection --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server connection --help` command


::

    Usage: pywbemcli server connection [COMMAND-OPTIONS]

      Get connection info used by this server.

      Display the information about the connection used to connect to the WBEM
      server.

      This is equivalent to the 'connection show' command.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server get-centralinsts --help`:

pywbemcli server get-centralinsts --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server get-centralinsts --help` command


::

    Usage: pywbemcli server get-centralinsts [COMMAND-OPTIONS]

      List central instances of mgmt profiles on the server.

      Retrieve the CIM instances that are central instances of the specified
      WBEM management profiles, and display these instances. By default, all
      management profiles advertized on the server are used. The profiles can be
      filtered by using the --organization and --profile options.

      The central instances are determined using all methodologies defined in
      DSP1033 V1.1 in the order of GetCentralInstances, central class, and
      scoping class methodology.

      Profiles that only use the scoping class methodology require the
      specification of the --central-class, --scoping-class, and --scoping-path
      options because additional information is needed to perform the scoping
      class methodology.

      The retrieved central instances are displayed along with the organization,
      name, and version of the profile they belong to, formatted as a table. The
      --output-format general option is ignored unless it specifies a table
      format.

    Options:
      -o, --organization <org name>   Filter by the defined organization. (ex. -o
                                      DMTF
      -p, --profile <profile name>    Filter by the profile name. (ex. -p Array
      -c, --central-class <classname>
                                      Optional. Required only if profiles supports
                                      only scopig methodology
      -s, --scoping-class <classname>
                                      Optional. Required only if profiles supports
                                      only scopig methodology
      -S, --scoping-path <pathname>   Optional. Required only if profiles supports
                                      only scopig methodology. Multiples allowed
      -r, --reference-direction [snia|dmtf]
                                      Navigation direction for association.
                                      [default: dmtf]
      -h, --help                      Show this message and exit.


.. _`pywbemcli server info --help`:

pywbemcli server info --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server info --help` command


::

    Usage: pywbemcli server info [COMMAND-OPTIONS]

      Get information about the server.

      The information includes CIM namespaces and server brand.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server interop --help`:

pywbemcli server interop --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server interop --help` command


::

    Usage: pywbemcli server interop [COMMAND-OPTIONS]

      Get the Interop namespace of the server.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server namespaces --help`:

pywbemcli server namespaces --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server namespaces --help` command


::

    Usage: pywbemcli server namespaces [COMMAND-OPTIONS]

      List the namespaces of the server.

    Options:
      -s, --sort  Sort into alphabetical order by classname.
      -h, --help  Show this message and exit.


.. _`pywbemcli server profiles --help`:

pywbemcli server profiles --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server profiles --help` command


::

    Usage: pywbemcli server profiles [COMMAND-OPTIONS]

      List management profiles advertized by the server.

      Retrieve the CIM instances representing the WBEM management profiles
      advertized by the WBEM server, and display information about each profile.
      WBEM management profiles are defined by DMTF and SNIA and define the
      management functionality that is available.

      The retrieved profiles can be filtered using the --organization and
      --profile options.

      The output is formatted as a table showing the organization, name, and
      version for each profile. The --output-format option is ignored unless it
      specifies a table format.

    Options:
      -o, --organization <org name>  Filter by the defined organization. (ex. -o
                                     DMTF
      -p, --profile <profile name>   Filter by the profile name. (ex. -p Array
      -h, --help                     Show this message and exit.

